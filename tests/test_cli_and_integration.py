"""
Integration and CLI tests for substrate-zero.
Validates chamber indexing, integrity, and menu configuration.
"""

import unittest
from substrate_zero.cli import CHAMBERS


class TestCliAndIntegration(unittest.TestCase):

    def test_chamber_registry_completeness(self):
        # Must have exactly 9 chambers registered
        expected_keys = [str(i) for i in range(1, 10)]
        self.assertEqual(sorted(CHAMBERS.keys(), key=int), expected_keys)

    def test_chamber_callables(self):
        for key, (title, func) in CHAMBERS.items():
            self.assertTrue(callable(func), f"Chamber {key} function must be callable")
            self.assertTrue(len(title) > 0, f"Chamber {key} must have a non-empty title")


if __name__ == "__main__":
    unittest.main()
