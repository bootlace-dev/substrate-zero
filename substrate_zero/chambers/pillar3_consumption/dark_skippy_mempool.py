"""
Pillar 3: Consumption - Dark Skippy Kleptographic Mempool Exfiltration
Real-World Precedent: 2024 DEF CON 32 Disclosure (Fournier, Farrow, Linus)
"""

import time
import hashlib
from rich.console import Console
from rich.table import Table
from substrate_zero.ui import print_header, print_breach, print_defense

console = Console()

class DarkSkippySigner:
    """
    Simulates a compromised hardware signer embedding master seed entropy
    into public signatures using low-order public key manipulation.
    """
    def __init__(self, seed_phrase: list[str]):
        self.seed_phrase = seed_phrase
        self.seed_bytes = " ".join(seed_phrase).encode()

    def sign_transaction(self, tx_id: int):
        # In Dark Skippy, the signer divides the 128/256-bit seed into chunks
        # and crafts nonces such that public key commitments reveal seed bits
        chunk_offset = (tx_id - 1) * 12
        chunk = self.seed_phrase[chunk_offset:chunk_offset + 12]
        embedded_payload = "-".join(chunk).encode()
        
        # Publicly valid signature artifacts
        r = int(hashlib.sha256(b"r:" + embedded_payload).hexdigest(), 16)
        s = int(hashlib.sha256(b"s:" + embedded_payload).hexdigest(), 16)
        
        return {
            "tx_id": f"tx_corporate_treasury_00{tx_id}",
            "r": hex(r),
            "s": hex(s),
            "payload_tag": hashlib.sha256(embedded_payload).hexdigest()[:8],
            "_secret_chunk": chunk
        }

class MempoolSniffer:
    """Simulates an outside attacker sniffing public Bitcoin mempool broadcasts."""
    def __init__(self):
        self.intercepted_chunks = []

    def ingest_mempool_tx(self, tx):
        # Observer extracts the kleptographic payload
        self.intercepted_chunks.extend(tx["_secret_chunk"])

    def reconstruct_seed(self):
        return self.intercepted_chunks

def run_chamber():
    print_header(
        3,
        "Dark Skippy Kleptographic Mempool Exfiltration",
        "Recovering a complete 24-word master seed from 2 innocent public mempool transactions"
    )

    victim_seed = [
        "abandon", "ability", "able", "about", "above", "absent",
        "absorb", "abstract", "absurd", "abuse", "access", "accident",
        "account", "accuse", "achieve", "acid", "acoustic", "acquire",
        "across", "act", "action", "actor", "actress", "actual"
    ]

    console.print("\n[bold white]Scenario: Institutional Cold Storage Key Ceremony & Broadcast[/bold white]")
    console.print("  [dim]• Signing Hardware: Commercial Hardware Security Module (Vendor Firmware)[/dim]")
    console.print("  [dim]• Air-Gap Status: 100% Air-Gapped via MicroSD / QR-code PSBTs[/dim]")
    console.print("  [dim]• Secret Seed: 24-word BIP-39 mnemonic stored inside Secure Element[/dim]")
    console.print("  [dim]• Threat Vector: Firmware Trojan executes Dark Skippy kleptography[/dim]\n")

    signer = DarkSkippySigner(victim_seed)
    sniffer = MempoolSniffer()

    tx1 = signer.sign_transaction(1)
    tx2 = signer.sign_transaction(2)

    table = Table(title="Broadcasted Public Bitcoin Mempool Signatures", border_style="cyan")
    table.add_column("Mempool TxID", style="cyan")
    table.add_column("ECDSA r-value (Public)", style="white")
    table.add_column("ECDSA s-value (Public)", style="white")
    table.add_column("Standard Node Verification", style="bold green")

    for tx in [tx1, tx2]:
        table.add_row(
            tx["tx_id"],
            f"{tx['r'][:16]}...{tx['r'][-8:]}",
            f"{tx['s'][:16]}...{tx['s'][-8:]}",
            "VALID (Accepted into Mempool)"
        )
        sniffer.ingest_mempool_tx(tx)
    console.print(table)

    console.print("\n[bold white]Passive Adversary Intercepts Mempool Feeds & Runs Extraction Engine...[/bold white]")
    time.sleep(0.5)
    recovered_seed = sniffer.reconstruct_seed()

    print_breach(
        "Complete 24-Word Master Seed Reconstructed in 2 Transactions",
        f"Original Target Seed:   {' '.join(victim_seed[:6])}... [24 words total]\n"
        f"Recovered Master Seed:  {' '.join(recovered_seed)}\n"
        f"Attacker Footprint:     Zero network access to the air-gapped device required.\n"
        f"Detection Status:       100% invisible to Bitcoin Core nodes, mempool explorers, and auditors.\n"
        f"Exfiltration Speed:     2 standard transactions broadcast on-chain."
    )

    print_defense(
        "Anti-Kleptographic Protocols (Sign-to-Contract / S2C)",
        "1. Implement Sign-to-Contract (S2C) / Synthetic Nonce Commitments (BIP-340).\n"
        "2. The coordinator (air-gapped laptop) injects unpredictable entropy e into the signing request.\n"
        "3. Signer must prove: R' = R + e*G. The signer cannot manipulate nonces without failing verification.\n"
        "4. Enforce SubZero amnesic physical coin-flip entropy independent of vendor firmware."
    )
