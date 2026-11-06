import unittest
from api import fetch_items


class APITests(unittest.TestCase):
    def test_explicit_limit(self):
        self.assertEqual(fetch_items(limit=5), list(range(5)))
