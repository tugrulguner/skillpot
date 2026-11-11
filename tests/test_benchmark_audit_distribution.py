"""Current benchmark-audit discovery and recorded filesystem distribution."""
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BenchmarkAuditDistributionTests(unittest.TestCase):
    def test_current_discovery_names_the_source_only_report_workflow(self):
        for name in ('README.md', 'catalog/README.md', 'website/src/content/docs/index.mdx',
                     'website/public/llms.txt'):
            text = (ROOT / name).read_text()
            for token in ('benchmark-audit', 'benchmark-audit-first-use.md', 'benchmark-audit.md'):
                with self.subTest(path=name, token=token):
                    self.assertIn(token, text)
        self.assertIn('Published v0.4.1 contains ten skills', (ROOT / 'README.md').read_text())

    def test_complete_public_install_record_matches_current_bundle_bytes(self):
        record = json.loads((ROOT / 'docs/benchmark-audit-distribution.json').read_text())
        package = ROOT / 'skills/benchmark-audit'
        actual = {p.relative_to(package).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in package.rglob('*') if p.is_file()}
        self.assertTrue(actual)
        self.assertEqual(actual, record['source_files'])
        self.assertEqual(len(actual), record['files_verified'])
        self.assertRegex(record['source_commit'], r'^[a-f0-9]{40}$')
        self.assertEqual(record['installer'], 'skills@1.7.6')
        self.assertEqual(set(record['agents']), {'claude-code', 'cursor', 'codex', 'hermes-agent'})
        for field in ('lock_ref_verified', 'sibling_preserved', 'selected_removal_verified', 'no_global_install'):
            self.assertTrue(record[field], field)
        self.assertFalse(record['client_or_model_launched'])
        guide = (ROOT / 'docs/benchmark-audit-first-use.md').read_text()
        first = re.search(r'```sh\n([^\n]+)\n```', guide)
        self.assertIsNotNone(first)
        assert first is not None
        self.assertEqual(first[1], 'npx skills@1.7.6 add https://github.com/tugrulguner/skillpot/tree/'
                         + record['source_commit'] + ' --skill benchmark-audit')

    def test_first_use_is_complete_and_does_not_authorize_benchmarks(self):
        text = (ROOT / 'docs/benchmark-audit-first-use.md').read_text()
        for token in ('not included in published SkillPot v0.4.1', 'read-only',
                      'benchmark-audit.md', 'assets/practice/claims.md', '60,000',
                      'dangling symlinks', 'C7', 'original', 'No benchmark',
                      'Not assessed', 'Insufficient evidence', 'user edits'):
            self.assertIn(token, text)
        self.assertNotIn('SOURCE_PIN_PENDING', text)
