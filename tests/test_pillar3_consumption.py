"""
Unit and integration tests for Pillar 3: Consumption.
Validates Lattice Nonce Bias (HNP / LLL), Dark Skippy Mempool Kleptography, and High-Throughput Starvation.
"""

import unittest
from substrate_zero.chambers.pillar3_consumption.lattice_hnp_crack import (
    lll_reduction,
    run_chamber as run_lattice_chamber,
)
from substrate_zero.chambers.pillar3_consumption.dark_skippy_mempool import (
    DarkSkippySigner,
    MempoolSniffer,
    run_chamber as run_dark_skippy_chamber,
)
from substrate_zero.chambers.pillar3_consumption.high_throughput_throttle import (
    HighThroughputGateway,
    run_chamber as run_high_throughput_chamber,
)


class TestPillar3Consumption(unittest.TestCase):

    def test_lll_reduction_basic(self):
        # Known test matrix for LLL basis reduction
        matrix = [
            [1, 1, 1],
            [-1, 0, 2],
            [3, 5, 6]
        ]
        reduced = lll_reduction(matrix, delta=0.75)
        self.assertEqual(len(reduced), 3)
        self.assertEqual(len(reduced[0]), 3)

    def test_dark_skippy_reconstruction(self):
        seed_phrase = [
            "abandon", "ability", "able", "about", "above", "absent",
            "absorb", "abstract", "absurd", "abuse", "access", "accident",
            "account", "accuse", "achieve", "acid", "acoustic", "acquire",
            "across", "act", "action", "actor", "actress", "actual"
        ]
        signer = DarkSkippySigner(seed_phrase)
        sniffer = MempoolSniffer()

        tx1 = signer.sign_transaction(1)
        tx2 = signer.sign_transaction(2)

        sniffer.ingest_mempool_tx(tx1)
        sniffer.ingest_mempool_tx(tx2)

        recovered = sniffer.reconstruct_seed()
        self.assertEqual(recovered, seed_phrase, "Mempool sniffer must fully reconstruct the 24-word seed")

    def test_high_throughput_gateway_failopen(self):
        gateway = HighThroughputGateway(fd_limit=5)
        # Normal connections
        for cid in range(1, 6):
            res = gateway.generate_tls_session_key(cid)
            self.assertFalse(res["fallback"])
            self.assertEqual(len(res["key"]), 64)

        # Overflow connection triggers silent fallback
        overflow_res = gateway.generate_tls_session_key(6)
        self.assertTrue(overflow_res["fallback"], "Exceeding FD limit must trigger fallback flag")
        self.assertEqual(len(overflow_res["key"]), 64)

    def test_run_lattice_chamber(self):
        run_lattice_chamber()

    def test_run_dark_skippy_chamber(self):
        run_dark_skippy_chamber()

    def test_run_high_throughput_chamber(self):
        run_high_throughput_chamber()


if __name__ == "__main__":
    unittest.main()
