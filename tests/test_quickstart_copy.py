"""Run the documented POSIX copy recipe, never a harness or installer."""
from pathlib import Path
import os
import re
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class QuickstartCopyTests(unittest.TestCase):
    def recipe(self, destination):
        source = (ROOT / 'README.md').read_text()
        match = re.search(r'(?ms)^\(\n  set -eu\n.*?^\)', source)
        if match is None:
            self.fail('README must retain a complete fail-closed copy recipe')
        return subprocess.run(['sh', '-c', match.group()], cwd=ROOT,
                              env={**os.environ, 'SKILL_ROOT': str(destination)},
                              capture_output=True, text=True)

    def test_complete_selected_folder_is_copied_without_siblings(self):
        with tempfile.TemporaryDirectory(prefix='skillpot-copy-') as directory:
            destination = Path(directory) / 'project-skills'
            result = self.recipe(destination)
            self.assertEqual(result.returncode, 0, result.stderr)
            source = ROOT / 'skills/intpot-python'
            expected = {str(p.relative_to(source)): p.read_bytes() for p in source.rglob('*') if p.is_file()}
            target = destination / 'intpot-python'
            actual = {str(p.relative_to(target)): p.read_bytes() for p in target.rglob('*') if p.is_file()}
            self.assertEqual(actual, expected)
            self.assertEqual([p.name for p in destination.iterdir()], ['intpot-python'])

    def test_existing_directory_and_local_edits_are_preserved(self):
        with tempfile.TemporaryDirectory(prefix='skillpot-copy-') as directory:
            destination = Path(directory)
            target = destination / 'intpot-python'
            target.mkdir()
            (target / 'SKILL.md').write_text('LOCAL EDITS')
            self.assertNotEqual(self.recipe(destination).returncode, 0)
            self.assertEqual((target / 'SKILL.md').read_text(), 'LOCAL EDITS')
            self.assertEqual([p.name for p in target.iterdir()], ['SKILL.md'])

    def test_existing_file_is_preserved(self):
        with tempfile.TemporaryDirectory(prefix='skillpot-copy-') as directory:
            destination = Path(directory)
            target = destination / 'intpot-python'
            target.write_text('EXISTING FILE')
            self.assertNotEqual(self.recipe(destination).returncode, 0)
            self.assertEqual(target.read_text(), 'EXISTING FILE')

    def test_same_name_symlink_does_not_redirect_the_copy(self):
        with tempfile.TemporaryDirectory(prefix='skillpot-copy-') as directory:
            destination = Path(directory) / 'skills'
            destination.mkdir()
            outside = Path(directory) / 'other-owned-directory'
            outside.mkdir()
            (outside / 'sentinel').write_text('UNCHANGED')
            (destination / 'intpot-python').symlink_to(outside, target_is_directory=True)
            self.assertNotEqual(self.recipe(destination).returncode, 0)
            self.assertEqual([p.name for p in outside.iterdir()], ['sentinel'])
            self.assertEqual((outside / 'sentinel').read_text(), 'UNCHANGED')
