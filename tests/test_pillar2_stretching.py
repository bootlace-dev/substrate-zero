"""
Unit and integration tests for Pillar 2: Stretching.
Validates Libbitcoin Milk Sad PRNG Seeding and VM Snapshot Rollback Nonce Clones.
"""

import unittest
import hashlib
from substrate_zero.chambers.pillar2_stretching.milk_sad_cracker import (
    Mt19937_32,
    run_chamber as run_milk_sad_chamber,
)
from substrate_zero.chambers.pillar2_stretching.vm_snapshot_clone import (
    ChaCha20CSPRNGMock,
    run_chamber as run_vm_snapshot_chamber,
)


class TestPillar2Stretching(unittest.TestCase):

    def test_mt19937_deterministic(self):
        seed = 1683042187
        rng1 = Mt19937_32(seed)
        rng2 = Mt19937_32(seed)
        k1 = rng1.generate_256bit_key()
        k2 = rng2.generate_256bit_key()
        self.assertEqual(len(k1), 32)
        self.assertEqual(k1, k2, "Same 32-bit seed must produce identical 256-bit key")

    def test_milk_sad_crack_simulation(self):
        target_epoch = 1683000000
        victim_rng = Mt19937_32(target_epoch)
        victim_key = victim_rng.generate_256bit_key()
        victim_addr = hashlib.sha256(b"bc1q_" + victim_key).hexdigest()[:24]

        # Brute force search in narrow window
        found_key = None
        for candidate in range(target_epoch - 10, target_epoch + 10):
            cand_key = Mt19937_32(candidate).generate_256bit_key()
            if hashlib.sha256(b"bc1q_" + cand_key).hexdigest()[:24] == victim_addr:
                found_key = cand_key
                break

        self.assertEqual(found_key, victim_key)

    def test_vm_snapshot_nonce_collision(self):
        initial_seed = b"test_hypervisor_prng_seed_32bytes"
        vm = ChaCha20CSPRNGMock(initial_seed, counter=500)
        snapshot = vm.snapshot()

        inst1 = ChaCha20CSPRNGMock(initial_seed)
        inst1.restore(snapshot)

        inst2 = ChaCha20CSPRNGMock(initial_seed)
        inst2.restore(snapshot)

        nonce1 = inst1.next_key()
        nonce2 = inst2.next_key()

        self.assertEqual(nonce1, nonce2, "Hypervisor snapshot restore must trigger nonce collision")

    def test_run_milk_sad_chamber(self):
        run_milk_sad_chamber()

    def test_run_vm_snapshot_chamber(self):
        run_vm_snapshot_chamber()


if __name__ == "__main__":
    unittest.main()
