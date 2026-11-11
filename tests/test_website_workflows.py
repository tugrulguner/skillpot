"""Offline regression checks for the production deployment authority boundary."""
import json
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]


class WebsiteWorkflowTests(unittest.TestCase):
    def test_browser_jobs_use_a_digest_pinned_version_matched_image(self):
        lock = json.loads((ROOT / 'website/package-lock.json').read_text())
        version = lock['packages']['node_modules/@playwright/test']['version']
        manifest = json.loads((ROOT / 'website/package.json').read_text())
        self.assertEqual(manifest['devDependencies']['@playwright/test'], version)
        images = []
        escaped_version = version.replace('.', r'\.')
        for filename, job_name in [('website.yml', 'website'), ('deploy-website.yml', 'deploy')]:
            with self.subTest(workflow=filename):
                workflow = yaml.safe_load((ROOT / '.github/workflows' / filename).read_text())
                container = workflow['jobs'][job_name].get('container', {})
                image = container.get('image', '')
                self.assertRegex(image, rf'^mcr\.microsoft\.com/playwright:v{escaped_version}-noble@sha256:[0-9a-f]{{64}}$')
                self.assertEqual(container.get('options'), '--init --shm-size=1g')
                images.append(image)
        self.assertEqual(len(set(images)), 1)

    def test_browser_jobs_do_not_install_system_dependencies_at_runtime(self):
        for filename, job_name in [('website.yml', 'website'), ('deploy-website.yml', 'deploy')]:
            with self.subTest(workflow=filename):
                workflow = yaml.safe_load((ROOT / '.github/workflows' / filename).read_text())
                steps = workflow['jobs'][job_name]['steps']
                commands = [step.get('run', '') for step in steps]
                self.assertNotRegex('\n'.join(commands), r'\bapt(?:-get)?\b|\binstall-deps\b|--with-deps')
                self.assertIn('npm ci', commands)
                self.assertIn('npm run build', commands)
                self.assertIn('npm run test:browser', commands)
                self.assertLess(commands.index('npm ci'), commands.index('npm run build'))
                self.assertLess(commands.index('npm run build'), commands.index('npm run test:browser'))
                browser_step = steps[commands.index('npm run test:browser')]
                self.assertNotIn('if', browser_step)
                self.assertNotIn('continue-on-error', browser_step)

    def test_deployment_sets_up_python_before_source_checks_in_container(self):
        workflow = yaml.safe_load((ROOT / '.github/workflows/deploy-website.yml').read_text())
        steps = workflow['jobs']['deploy']['steps']
        setups = [index for index, step in enumerate(steps)
                  if step.get('uses', '').startswith('actions/setup-python@')]
        self.assertEqual(len(setups), 1)
        self.assertEqual(steps[setups[0]]['with']['python-version'], '3.12')
        check = next(index for index, step in enumerate(steps)
                     if step.get('name') == 'Check canonical repository sources')
        self.assertLess(setups[0], check)
        self.assertIn('python3 -m venv', steps[check]['run'])

    def test_manual_deployment_cannot_publish_a_feature_branch(self):
        workflow = yaml.safe_load((ROOT / '.github/workflows/deploy-website.yml').read_text())
        self.assertEqual(workflow['jobs']['deploy'].get('if'), "${{ github.ref == 'refs/heads/main' }}")

    def test_cloudflare_credentials_are_only_exposed_to_the_deploy_step(self):
        workflow = yaml.safe_load((ROOT / '.github/workflows/deploy-website.yml').read_text())
        self.assertEqual(workflow['permissions'], {'contents': 'read'})
        self.assertNotIn('env', workflow)
        job = workflow['jobs']['deploy']
        self.assertNotIn('env', job)
        steps = job['steps']
        secret_steps = [step for step in steps if 'CLOUDFLARE_API_TOKEN' in str(step.get('env', {}))]
        self.assertEqual(len(secret_steps), 1)
        self.assertEqual(secret_steps[0]['name'], 'Deploy the verified static artifact')
        names = [step.get('name', step.get('run', '')) for step in steps]
        self.assertLess(names.index('npm run test:browser'), names.index('Deploy the verified static artifact'))
        self.assertLess(names.index('Deploy the verified static artifact'), names.index('Verify public content after DNS and TLS propagation'))
