"""
Unit and integration tests for Pillar 4: Death.
Validates Compiler Dead-Store Elimination (DSE) and Memory Hygiene / mlock() / NVMe Bleed.
"""

import unittest
from substrate_zero.chambers.pillar4_death.dse_assassin import (
    run_chamber as run_dse_chamber,
)
from substrate_zero.chambers.pillar4_death.memory_hygiene import (
    run_chamber as run_memory_hygiene_chamber,
)


class TestPillar4Death(unittest.TestCase):

    def test_run_dse_chamber(self):
        # Must compile both flawed and patched binaries, verify DSE stripping, and succeed
        run_dse_chamber()

    def test_run_memory_hygiene_chamber(self):
        # Must inspect host RLIMIT_MEMLOCK and complete cleanly
        run_memory_hygiene_chamber()


if __name__ == "__main__":
    unittest.main()
