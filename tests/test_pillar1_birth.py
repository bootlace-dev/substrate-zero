"""
Unit and integration tests for Pillar 1: Birth.
Validates Silicon TRNG Collapse and Early-Boot MicroVM Starvation.
"""

import unittest
from substrate_zero.chambers.pillar1_birth.trng_collapse import SiliconTRNGSimulator, run_chamber as run_trng_chamber
from substrate_zero.chambers.pillar1_birth.cloud_init_starvation import run_chamber as run_cloud_init_chamber


class TestPillar1Birth(unittest.TestCase):

    def test_silicon_trng_normal(self):
        trng = SiliconTRNGSimulator(mode="normal")
        k1 = trng.read_hardware_entropy(32)
        k2 = trng.read_hardware_entropy(32)
        self.assertEqual(len(k1), 32)
        self.assertEqual(len(k2), 32)
        self.assertNotEqual(k1, k2, "Normal TRNG must produce distinct 256-bit entropy samples")

    def test_silicon_trng_thermal_collapse(self):
        trng = SiliconTRNGSimulator(mode="thermal_collapse")
        k = trng.read_hardware_entropy(32)
        self.assertEqual(len(k), 32)
        # Verify 8-byte periodic repetition
        self.assertEqual(k[:8], k[8:16])
        self.assertEqual(k[:8], b"\xca\xfe\xba\xbe\xde\xad\xbe\xef")

    def test_silicon_trng_firmware_fallback(self):
        trng = SiliconTRNGSimulator(mode="firmware_fallback")
        k = trng.read_hardware_entropy(32)
        self.assertEqual(len(k), 32)
        self.assertEqual(k, bytes([0x55, 0xaa] * 16))

    def test_run_trng_chamber(self):
        # Must execute without uncaught exceptions
        run_trng_chamber()

    def test_run_cloud_init_chamber(self):
        # Must execute without uncaught exceptions
        run_cloud_init_chamber()


if __name__ == "__main__":
    unittest.main()
