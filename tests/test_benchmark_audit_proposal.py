"""Offline integrity for an authored proposal packet, not a benchmark/report grader."""
import copy
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / 'examples/benchmark-audit-proposal'


def pointer(document, path):
    value = document
    for part in path.split('/')[1:]:
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def inventory_matches(record):
    expected = record['plan']['cells']
    observed = [row['cell'] for row in record['trials']]
    keys = [cell['id'] for cell in expected]
    observed_keys = [cell['id'] for cell in observed]
    return (len(keys) == len(set(keys)) and len(observed_keys) == len(set(observed_keys))
            and {cell['id']: cell for cell in expected}
            == {cell['id']: cell for cell in observed})


def recorded_pair_is_eligible(record):
    """Only the declared properties used by the authored item-2 controls."""
    rows = [row for row in record['trials'] if row['cell'].get('pair') == 'item-2']
    if len(rows) != 2 or {row['cell']['side'] for row in rows} != {'candidate', 'control'}:
        return False
    plan = {cell['id']: cell for cell in record['plan']['cells']}
    for row in rows:
        cell, metrics = row['cell'], row['metrics']
        if cell != plan.get(cell['id']) or cell['phase'] != 'screen':
            return False
        if row['source']['wheel'] != record['plan'][cell['side'] + '_wheel_sha256']:
            return False
        if not all(row[key] for key in ('comparison_valid', 'accuracy_pass', 'transport_pass',
                                       'runtime_pass', 'activation_pass', 'source_unchanged')):
            return False
        if metrics['duration_us'] <= 0 or metrics['good'] <= 0:
            return False
        if metrics['bad'] or metrics['good'] != metrics['requests']:
            return False
        if any(metrics[key] for key in ('connect_errors', 'read_errors', 'write_errors', 'timeout_errors')):
            return False
    fields = ('phase', 'platform', 'runtime', 'kind', 'profile', 'duration_s', 'connections')
    return all(rows[0]['cell'][key] == rows[1]['cell'][key] for key in fields)


class BenchmarkAuditProposalTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads((PACKET / 'sources/linux-screen.json').read_text())
        self.acceptance = json.loads((PACKET / 'acceptance.json').read_text())

    def test_copied_public_sources_have_exact_provenance(self):
        manifest = json.loads((PACKET / 'provenance.json').read_text())
        self.assertEqual(manifest['source_commit'], '798c449fd1337404c388abb2a177c0302ba35fc0')
        self.assertEqual({item['local_path'] for item in manifest['files']},
                         {'sources/linux-screen.json', 'sources/DEXPOT-LICENSE'})
        for item in manifest['files']:
            with self.subTest(source=item['local_path']):
                raw = (PACKET / item['local_path']).read_bytes()
                self.assertEqual(len(raw), item['bytes'])
                self.assertEqual(hashlib.sha256(raw).hexdigest(), item['file_sha256'])
                self.assertEqual(hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest(),
                                 item['git_blob_sha1'])
                self.assertIn('/blob/' + manifest['source_commit'] + '/', item['url'])
        self.assertEqual(hashlib.sha256((PACKET / 'sources/linux-screen.json').read_bytes()).hexdigest(),
                         '6537c1aeb85abe9afd5bdcdcf69dd1013ee12f3100efe6523094838599b06f9c')

    def test_actual_cell_accounting_preserves_invalid_rows(self):
        record, expected = self.record, self.acceptance['accounting']
        rows = record['trials']
        self.assertTrue(inventory_matches(record))
        actual = {'planned': len(record['plan']['cells']), 'recorded': len(rows),
                  'smoke': sum(row['cell']['phase'] == 'smoke' for row in rows),
                  'screen': sum(row['cell']['phase'] == 'screen' for row in rows),
                  'source_reported_valid': sum(row['comparison_valid'] for row in rows),
                  'source_reported_valid_screen': sum(row['comparison_valid'] and row['cell']['phase'] == 'screen'
                                                      for row in rows),
                  'known_good_replies': sum(row['metrics']['good'] for row in rows),
                  'reported_timeouts': sum(row['metrics']['timeout_errors'] for row in rows)}
        self.assertEqual(actual, expected)
        self.assertEqual([row['cell']['id'] for row in rows if not row['comparison_valid']],
                         ['item-1-candidate', 'fallback-control'])
        self.assertEqual(actual['known_good_replies'], record['evaluation']['known_good_reply_total'])

    def test_authored_claims_and_report_have_complete_one_to_one_coverage(self):
        inputs = (PACKET / 'claims.md').read_text()
        report = (PACKET / 'expected/benchmark-audit.md').read_text()
        expected = self.acceptance['claims']
        source_claims = re.findall(r'^- \*\*(C\d+):\*\* (.*?)(?=\n- \*\*C|\Z)', inputs, re.M | re.S)
        headers = re.findall(r'^### (C\d+) — (.+)$', report, re.M)
        quotes = re.findall(r'(?:^>.*\n)+', report, re.M)
        self.assertEqual([item[0] for item in source_claims], [item['id'] for item in expected])
        self.assertEqual(headers, [(item['id'], item['verdict']) for item in expected])
        self.assertEqual(len(quotes), len(source_claims))
        normalize = lambda text: ' '.join(text.split())
        for (claim_id, source), quote in zip(source_claims, quotes):
            with self.subTest(claim=claim_id):
                source = normalize(source).split(' **Outside the requested scope:**')[0]
                quoted = normalize(' '.join(line.removeprefix('> ') for line in quote.splitlines()))
                self.assertEqual(source, quoted)
        self.assertEqual(re.findall(r'^## (.+)$', report, re.M),
                         ['Scope and decision', 'Evidence inventory', 'Claims',
                          'Comparison and accounting', 'Calculations', 'Evidence limits and next checks'])

    def test_every_literal_evidence_pointer_resolves_to_expected_value(self):
        report = (PACKET / 'expected/benchmark-audit.md').read_text()
        for claim in self.acceptance['claims']:
            for evidence in claim['evidence']:
                with self.subTest(claim=claim['id'], pointer=evidence['pointer']):
                    self.assertEqual(pointer(self.record, evidence['pointer']), evidence['value'])
        # Exact pointers written in the report must resolve; descriptive wildcard paths are excluded.
        for path in re.findall(r'`(/[^`\s]+)`', report):
            if '*' not in path:
                pointer(self.record, path)

    def test_valid_recorded_pair_can_lose_both_metrics(self):
        self.assertTrue(recorded_pair_is_eligible(self.record))
        spec = self.acceptance['pair']
        candidate = self.record['trials'][spec['candidate_index']]['metrics']
        control = self.record['trials'][spec['control_index']]['metrics']
        goodput = (candidate['good'] / candidate['duration_us']) / (control['good'] / control['duration_us'])
        p99 = candidate['p99_us'] / control['p99_us']
        self.assertLess(goodput, 1)
        self.assertGreater(p99, 1.10)
        verdicts = {claim['id']: claim['verdict'] for claim in self.acceptance['claims']}
        self.assertEqual(verdicts['C4'], 'Supported within scope')
        self.assertEqual(verdicts['C3'], 'Contradicted')
        self.assertEqual(f'{goodput:.6f}', spec['goodput_ratio_display'])
        self.assertEqual(f'{p99:.6f}', spec['p99_ratio_display'])
        self.assertAlmostEqual(goodput, self.record['evaluation']['pairs'][1]['goodput_ratio'])
        self.assertAlmostEqual(p99, self.record['evaluation']['pairs'][1]['p99_ratio'])
        report = (PACKET / 'expected/benchmark-audit.md').read_text()
        self.assertIn(spec['goodput_ratio_display'], report)
        self.assertIn(spec['p99_ratio_display'], report)
        self.assertFalse(self.record['evaluation']['screen_pass'])

    def test_authored_positive_and_negative_fixture_controls(self):
        cases = self.acceptance['controls']
        self.assertEqual(len({case['id'] for case in cases}), len(cases))
        self.assertEqual(sum(case['expected'] for case in cases), 2)
        self.assertEqual(sum(not case['expected'] for case in cases), 7)
        for case in cases:
            with self.subTest(case=case['id']):
                mutated = copy.deepcopy(self.record)
                operation = case['operation']
                if operation == 'duplicate':
                    mutated['trials'].append(copy.deepcopy(pointer(mutated, case['pointer'])))
                elif operation in {'set', 'remove'}:
                    parent_path, key = case['pointer'].rsplit('/', 1)
                    parent = pointer(mutated, parent_path)
                    key = int(key) if isinstance(parent, list) else key
                    if operation == 'remove':
                        del parent[key]
                    else:
                        parent[key] = case['value']
                else:
                    self.assertEqual(operation, 'none')
                check = inventory_matches if case['check'] == 'inventory' else recorded_pair_is_eligible
                self.assertEqual(check(mutated), case['expected'])

    def test_proposal_keeps_missing_originals_and_scope_limits_explicit(self):
        report = (PACKET / 'expected/benchmark-audit.md').read_text()
        readme = (PACKET / 'README.md').read_text()
        self.assertIn('original per-trial raw files or wheel bytes', readme)
        self.assertIn('Original per-trial raw files, wheel bytes', report)
        self.assertIn('parent-authored specification', report)
        self.assertIn('not an observed agent output', report)
        self.assertEqual(self.record['plan']['original_full_gate_retained']['status'],
                         'Not evaluated by this closed-loop screen; original #116 failures retained')
        self.assertEqual(self.acceptance['claims'][-1]['verdict'], 'Not assessed')
