"""Exercise the LifePot-style verification gate and SkillPot adaptations."""
from itertools import product
from pathlib import Path
import subprocess
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]


def workflow(name):
    return yaml.load((ROOT / '.github/workflows' / name).read_text(), Loader=yaml.BaseLoader)


class CIContractTests(unittest.TestCase):
    def test_every_pr_runs_the_complete_gate_without_path_filters(self):
        ci = workflow('ci.yml')
        self.assertIn('pull_request', ci['on'])
        self.assertFalse((ci['on']['pull_request'] or {}).get('paths'))
        self.assertEqual(ci['jobs']['browser']['uses'], './.github/workflows/website.yml')
        self.assertIn('workflow_call', workflow('website.yml')['on'])
        self.assertNotIn('pull_request', workflow('website.yml')['on'])

    def test_verification_gate_fails_closed_for_all_dependency_results(self):
        gate = workflow('ci.yml')['jobs']['verify']
        self.assertEqual(gate['if'], '${{ always() }}')
        self.assertEqual(gate['needs'], ['checks', 'browser'])
        self.assertEqual(gate['steps'][0]['env'], {
            'CHECKS_RESULT': '${{ needs.checks.result }}',
            'BROWSER_RESULT': '${{ needs.browser.result }}',
        })
        command = gate['steps'][0]['run']
        for checks, browser in product(['success', 'failure', 'cancelled', 'skipped'], repeat=2):
            with self.subTest(checks=checks, browser=browser):
                result = subprocess.run(['sh', '-c', command],
                                        env={'CHECKS_RESULT': checks, 'BROWSER_RESULT': browser},
                                        capture_output=True)
                self.assertEqual(result.returncode == 0, checks == browser == 'success')

    def test_checks_include_real_lint_types_and_supported_python_matrix(self):
        job = workflow('ci.yml')['jobs']['checks']
        self.assertEqual(job['strategy']['matrix']['python-version'], ['3.11', '3.12', '3.13', '3.14'])
        commands = [step.get('run', '') for step in job['steps']]
        for command in ['python -m pip install --requirement requirements-ci.txt',
                        'ruff check --select E9,F63,F7,F82 scripts tests', 'pyright scripts',
                        'python scripts/check_docs.py', 'python scripts/check_project_skills.py',
                        'python -m unittest discover -s tests -v']:
            self.assertIn(command, commands)

    def test_workflows_are_read_only_and_external_actions_are_immutable(self):
        for path in (ROOT / '.github/workflows').glob('*.yml'):
            data = workflow(path.name)
            self.assertEqual(data['permissions'], {'contents': 'read'}, path.name)
            for job in data['jobs'].values():
                for step in job.get('steps', []):
                    uses = step.get('uses', '')
                    if uses and not uses.startswith('./'):
                        self.assertRegex(uses, r'@[0-9a-f]{40}$', path.name)

    def test_website_retains_supported_runtime_build_and_browser_checks(self):
        steps = workflow('website.yml')['jobs']['website']['steps']
        node = next(step for step in steps if step.get('uses', '').startswith('actions/setup-node@'))
        self.assertEqual(node['with']['node-version'], '22.23.4')
        commands = [step.get('run', '') for step in steps]
        for command in ['npm ci', 'npm run build', 'npm run test:browser']:
            self.assertIn(command, commands)

    def test_weekly_dependency_updates_cover_actual_manifests(self):
        config = yaml.load((ROOT / '.github/dependabot.yml').read_text(), Loader=yaml.BaseLoader)
        self.assertEqual({(item['package-ecosystem'], item['directory']) for item in config['updates']},
                         {('npm', '/website'), ('github-actions', '/'), ('pip', '/')})
        for item in config['updates']:
            self.assertEqual(item['schedule']['interval'], 'weekly')
            self.assertEqual(item['open-pull-requests-limit'], '5')

    def test_contribution_forms_reference_existing_labels_and_no_runtime_claims(self):
        forms = ROOT / '.github/ISSUE_TEMPLATE'
        for name, label in [('bug.yml', 'bug'), ('feature.yml', 'enhancement')]:
            form = yaml.load((forms / name).read_text(), Loader=yaml.BaseLoader)
            self.assertEqual(form['labels'], [label])
            self.assertTrue(any(field.get('validations', {}).get('required') == 'true' for field in form['body']))
        config = yaml.load((forms / 'config.yml').read_text(), Loader=yaml.BaseLoader)
        self.assertEqual(config['blank_issues_enabled'], 'false')
        self.assertEqual(config['contact_links'][0]['url'], 'https://discord.gg/u3AANZr6RG')
