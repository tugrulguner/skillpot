"""The browser container must exercise deployment's TLS-capable Python too."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ContainerPythonRuntimeTests(unittest.TestCase):
    def test_ci_and_deployment_use_managed_python_and_the_same_source_gates(self):
        for name in ("website.yml", "deploy-website.yml"):
            with self.subTest(workflow=name):
                text = (ROOT / ".github/workflows" / name).read_text()
                self.assertNotIn("actions/setup-python@", text)
                self.assertIn("uv venv --managed-python --python 3.12", text)
                self.assertIn("uv pip install --python", text)
                self.assertIn("import ssl; print(ssl.OPENSSL_VERSION)", text)
                self.assertIn("scripts/check_docs.py", text)
                self.assertIn("scripts/check_project_skills.py", text)
                self.assertIn("-m unittest discover -s tests -v", text)
                self.assertNotIn("allow-insecure-host", text)
                self.assertNotIn("--trusted-host", text)

if __name__ == "__main__":
    unittest.main()
