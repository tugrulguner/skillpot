"""Offline regression checks for the production deployment authority boundary."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]


class WebsiteWorkflowTests(unittest.TestCase):
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
