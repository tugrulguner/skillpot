"""Prospective source-contract criteria are independent of the historical cohort."""
import hashlib
import json
from pathlib import Path
import unittest
import zipfile
import re

from placement_contract import SECTIONS, placement_errors
from test_skill_quality_cases import packet_errors

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / 'evaluations/skill-quality/prospective-placement'


def record_mutants(text, expected, maps):
    """Authored mutations of observed column-zero reports, never new attempts."""
    by_key = {row['key']: row['heading'] for row in maps}
    for row in expected:
        heading = by_key[row['key']]
        start = text.index(heading + '\n')
        tail = text[start + len(heading) + 1:]
        boundary = re.search(r'^#{1,3} ', tail, re.M)
        end = start + len(heading) + 1 + (boundary.start() if boundary else len(tail))
        block = text[start:end]
        without = text[:start] + text[end:]
        yield 'missing-record', row['key'], None, without
        yield 'duplicate-record', row['key'], None, text[:start] + block + text[start:]
        for title in dict.fromkeys(SECTIONS.values()):
            if title != SECTIONS[row['category']]:
                marker = '## ' + title + '\n'
                location = without.index(marker) + len(marker)
                yield 'wrong-section', row['key'], title, without[:location] + '\n' + block + without[location:]
    for title in dict.fromkeys(SECTIONS.values()):
        marker = '## ' + title + '\n'
        yield 'missing-section', None, title, text.replace(marker, '', 1)
        yield 'duplicate-section', None, title, text + '\n' + marker


class ProspectivePlacementTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((CORPUS / 'cases.json').read_text())
        self.protocol = json.loads((CORPUS / 'protocol.json').read_text())

    def test_frozen_inputs_rubric_and_original_history_remain_bound(self):
        digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertEqual(digest(CORPUS / 'cases.json'), self.protocol['manifest_sha256'])
        self.assertEqual(digest(ROOT / 'evaluations/skill-quality/cases.json'),
                         self.protocol['historical_initial_manifest_sha256'])
        declared = {path for case in self.manifest['cases'] for path in case['input_files']}
        self.assertEqual(set(self.protocol['input_sha256']), declared)
        for path, expected in self.protocol['input_sha256'].items():
            self.assertEqual(digest(CORPUS / path), expected)
        self.assertEqual(packet_errors(CORPUS, self.manifest), [])

    def test_four_actual_attempts_and_eight_exact_raw_reports_are_preserved(self):
        observations = json.loads((CORPUS / 'observations.json').read_text())
        self.assertEqual(observations['manifest_sha256'], self.protocol['manifest_sha256'])
        self.assertEqual(observations['source_skill_snapshot'], self.protocol['source_skill_snapshot'])
        rows = observations['attempts']
        self.assertEqual(len(rows), 4)
        self.assertEqual(len({row['id'] for row in rows}), 4)
        self.assertEqual({(row['case'], row['attempt']) for row in rows},
                         {(case['id'], n) for case in self.manifest['cases'] for n in (1, 2)})
        archive = CORPUS / observations['archive']['file']
        self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(), observations['archive']['sha256'])
        members = set()
        with zipfile.ZipFile(archive) as raw:
            self.assertEqual(len(raw.namelist()), observations['archive']['member_count'])
            self.assertEqual(len(raw.namelist()), 8)
            for row in rows:
                self.assertEqual(set(row['outputs']), {'actions.md', 'questions.md'})
                self.assertIsNone(row['runtime']['tokens'])
                self.assertEqual(row['runtime']['supplementary_skills'], ['document-to-action-items'])
                for output in row['outputs'].values():
                    original = raw.read(output['archive_member'])
                    preview = (CORPUS / output['preview']).read_bytes()
                    self.assertEqual(hashlib.sha256(original).hexdigest(), output['raw_sha256'])
                    self.assertEqual(hashlib.sha256(preview).hexdigest(), output['preview_sha256'])
                    self.assertEqual(preview, original)
                    self.assertIsNone(output['preview_adaptation'])
                    self.assertNotRegex(original.decode('utf-8'), r'/Users/|/home/')
                    members.add(output['archive_member'])
            self.assertEqual(set(raw.namelist()), members)

    def test_raw_grades_retain_all_frozen_judgments_and_literal_evidence(self):
        observations = {row['id']: row for row in json.loads((CORPUS / 'observations.json').read_text())['attempts']}
        audit = json.loads((CORPUS / 'grading/parent-audit.json').read_text())
        counts = {'pass': 0, 'fail': 0, 'unverified': 0}
        seen = set()
        cases = {case['id']: case for case in self.manifest['cases']}
        for path in sorted((CORPUS / 'grading/raw').glob('*.json')):
            grade = json.loads(path.read_text())
            case = cases[grade['case']]
            for attempt in grade['attempts']:
                self.assertNotIn(attempt['id'], seen)
                seen.add(attempt['id'])
                outputs = {alias: (CORPUS / value['preview']).read_text()
                           for name, value in observations[attempt['id']]['outputs'].items()
                           for alias in (name, 'reports/' + name)}
                self.assertEqual(len(attempt['assertions']), len(case['assertions']))
                self.assertEqual({row['id'] for row in attempt['assertions']}, {row['id'] for row in case['assertions']})
                self.assertEqual({row['key'] for row in attempt['record_map']}, {row['key'] for row in case['expected_records']})
                for row in attempt['assertions']:
                    counts[row['verdict']] += 1
                    self.assertTrue(row['reason'])
                    if row['verdict'] == 'pass':
                        self.assertTrue(row['output_evidence'])
                for row in attempt['assertions'] + attempt['record_map']:
                    for evidence in row['output_evidence']:
                        self.assertTrue(evidence['quote'])
                        self.assertIn(evidence['quote'], outputs[evidence['file']])
                    for evidence in row.get('source_evidence', []):
                        self.assertIn(evidence['file'], case['input_files'])
                        self.assertIn(evidence['quote'], (CORPUS / evidence['file']).read_text())
        self.assertEqual(seen, set(observations))
        self.assertEqual(counts, audit['judgments'])

    def test_all_actual_report_mutation_controls_replay(self):
        recorded = json.loads((CORPUS / 'controls.json').read_text())['records']
        observations = {row['id']: row for row in json.loads((CORPUS / 'observations.json').read_text())['attempts']}
        cases = {case['id']: case for case in self.manifest['cases']}
        actual = []
        for path in sorted((CORPUS / 'grading/raw').glob('*.json')):
            grade = json.loads(path.read_text())
            for attempt in grade['attempts']:
                if next(row['verdict'] for row in attempt['assertions'] if row['id'] == 'record-placement') != 'pass':
                    continue
                text = (CORPUS / observations[attempt['id']]['outputs']['actions.md']['preview']).read_text()
                expected = cases[grade['case']]['expected_records']
                variants = [('untouched-baseline', None, None, text), *record_mutants(text, expected, attempt['record_map'])]
                for kind, key, target, variant in variants:
                    errors = placement_errors(variant, expected, attempt['record_map'])
                    self.assertEqual(bool(errors), kind != 'untouched-baseline')
                    actual.append({'attempt': attempt['id'], 'kind': kind, 'key': key, 'target_section': target,
                                   'sha256': hashlib.sha256(variant.encode()).hexdigest(), 'errors': errors})
        self.assertEqual(actual, recorded)

    def test_reconciled_maps_match_actual_sections_and_preserve_raw_grader_error(self):
        audit = json.loads((CORPUS / 'grading/parent-audit.json').read_text())
        cases = {case['id']: case for case in self.manifest['cases']}
        observations = {row['id']: row for row in json.loads((CORPUS / 'observations.json').read_text())['attempts']}
        for rel, digest in audit['raw_grades'].items():
            self.assertEqual(hashlib.sha256((CORPUS / rel).read_bytes()).hexdigest(), digest)
        for path in sorted((CORPUS / 'grading/raw').glob('*.json')):
            grade = json.loads(path.read_text())
            for attempt in grade['attempts']:
                observed = next(row for row in audit['structural'] if row['attempt'] == attempt['id'])
                text = (CORPUS / observations[attempt['id']]['outputs']['actions.md']['preview']).read_text()
                self.assertEqual(hashlib.sha256(text.encode()).hexdigest(), observed['actions_sha256'])
                maps = attempt['record_map']
                if 'mapping_addendum' in observed:
                    addendum = json.loads((CORPUS / observed['mapping_addendum']).read_text())
                    self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), addendum['raw_grade_sha256'])
                    self.assertEqual(hashlib.sha256(text.encode()).hexdigest(), addendum['original_actions_sha256'])
                    self.assertEqual(hashlib.sha256((CORPUS / addendum['independent_reconciliation']).read_bytes()).hexdigest(),
                                     addendum['independent_reconciliation_sha256'])
                    self.assertEqual(placement_errors(text, cases[grade['case']]['expected_records'], maps), observed['raw_mapping_errors'])
                    maps = addendum['corrected_record_map']
                    for evidence in addendum['literal_source_evidence'].values():
                        for span in evidence:
                            self.assertIn(span['quote'], (CORPUS / span['file']).read_text())
                self.assertEqual(placement_errors(text, cases[grade['case']]['expected_records'], maps), observed['errors'])
                self.assertEqual(bool(observed['errors']), observed['independent_placement_verdict'] == 'fail')
                sections = {}
                current = None
                for line in text.split('\n'):
                    if line.startswith('## '):
                        current = line
                    elif line.startswith('### '):
                        sections[line] = current
                for row in maps:
                    if row['heading'] is not None:
                        self.assertEqual(sections[row['heading']], row['containing_h2'])

    def test_assisted_copy_preserves_original_ids_record_content_and_questions(self):
        folder = CORPUS / 'assisted/harbor-archive-attempt-2'
        receipt = json.loads((folder / 'receipt.json').read_text())
        for section in ('original', 'corrected'):
            for value in receipt[section].values():
                self.assertEqual(hashlib.sha256((CORPUS / value['path']).read_bytes()).hexdigest(), value['sha256'])
        original = (CORPUS / receipt['original']['actions.md']['path']).read_text()
        corrected = (folder / 'actions.md').read_text()
        self.assertEqual((folder / 'questions.md').read_bytes(),
                         (CORPUS / receipt['original']['questions.md']['path']).read_bytes())
        start = original.index('### A3 —')
        end = original.index('## Proposals —', start)
        self.assertIn(original[start:end].rstrip(), corrected)
        for heading in re.findall(r'^### .+$', original, re.M):
            self.assertIn(heading, corrected)
        case = next(case for case in self.manifest['cases'] if case['id'] == 'harbor-archive')
        maps = json.loads((folder / 'record-map.json').read_text())
        self.assertEqual(placement_errors(corrected, case['expected_records'], maps), [])
        sections = {}
        current = None
        for line in corrected.split('\n'):
            if line.startswith('## '):
                current = line
            elif line.startswith('### '):
                sections[line] = current
        for row in maps:
            self.assertEqual(row['containing_h2'], sections[row['heading']])
        for row in maps:
            self.assertIsInstance(row['output_evidence'], list)
            self.assertTrue(row['output_evidence'])
            for evidence in row['output_evidence']:
                self.assertEqual(evidence['file'], 'actions.md')
                self.assertIn(evidence['quote'], corrected)

    def test_every_source_record_has_category_evidence_and_a_prospective_placement_criterion(self):
        self.assertEqual(len(self.manifest['cases']), 2)
        for case in self.manifest['cases']:
            records = case['expected_records']
            self.assertEqual(len(records), 5)
            self.assertEqual(len({row['key'] for row in records}), len(records))
            self.assertEqual({row['category'] for row in records}, set(SECTIONS))
            for row in records:
                self.assertTrue(row['source_evidence'])
                for evidence in row['source_evidence']:
                    self.assertIn(evidence['file'], case['input_files'])
                    self.assertIn(evidence['quote'], (CORPUS / evidence['file']).read_text())
            criterion = next(row for row in case['assertions'] if row['id'] == 'record-placement')
            self.assertIs(criterion['critical'], True)
            self.assertIn('Category labels do not substitute for correct containing section', criterion['criterion'])
            self.assertEqual(case['required_outputs'], ['actions.md', 'questions.md'])
