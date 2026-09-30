"""
Pillar 2: Stretching - VM Snapshot Rollback & PRNG Clone Race
Real-World Precedent: VMGENID Race Conditions & Android SecureRandom (2013)
"""

import time
import hashlib
from rich.console import Console
from rich.table import Table
from substrate_zero.ui import print_header, print_breach, print_defense

console = Console()

class ChaCha20CSPRNGMock:
    """Mock ChaCha20 48-byte state vector demonstrating snapshot rollback."""
    def __init__(self, seed: bytes, counter: int = 0):
        self.seed = seed
        self.counter = counter

    def snapshot(self):
        return {"seed": self.seed, "counter": self.counter}

    def restore(self, snap):
        self.seed = snap["seed"]
        self.counter = snap["counter"]

    def next_key(self) -> bytes:
        state = hashlib.sha256(self.seed + self.counter.to_bytes(8, "big")).digest()
        self.counter += 1
        return state

def run_chamber():
    print_header(
        2,
        "Virtual Machine Snapshot Rollback & PRNG Clones",
        "Demonstrating state duplication and nonce reuse across cloned hypervisor instances"
    )

    console.print("\n[bold white]Scenario: Enterprise Cloud Signing Gateway Snapshot Execution[/bold white]")
    console.print("  [dim]• Hypervisor takes snapshot 'snap-gold-prod-v1' at T0[/dim]")
    console.print("  [dim]• Guest OS CSPRNG state is frozen: ChaCha20 State Vector Counter = 1,420[/dim]")
    console.print("  [dim]• Snapshot is cloned into 2 independent production instances: 'gateway-east' and 'gateway-west'[/dim]\n")

    initial_seed = b"hypervisor_gold_master_prng_seed"
    vm_base = ChaCha20CSPRNGMock(initial_seed, counter=1420)
    golden_snapshot = vm_base.snapshot()

    # Instance 1 restores snapshot
    gateway_east = ChaCha20CSPRNGMock(initial_seed)
    gateway_east.restore(golden_snapshot)

    # Instance 2 restores snapshot (concurrently or after rollback)
    gateway_west = ChaCha20CSPRNGMock(initial_seed)
    gateway_west.restore(golden_snapshot)

    # Both instances sign 3 outgoing corporate transactions
    east_nonces = [gateway_east.next_key().hex() for _ in range(3)]
    west_nonces = [gateway_west.next_key().hex() for _ in range(3)]

    table = Table(title="Live Nonce Stream Across Independent Cloud Gateways", border_style="red")
    table.add_column("Tx Sequence", style="cyan")
    table.add_column("Gateway-East Nonce (k)", style="yellow")
    table.add_column("Gateway-West Nonce (k)", style="magenta")
    table.add_column("Cryptographic Collision", style="bold red")

    for i in range(3):
        collision = east_nonces[i] == west_nonces[i]
        status = "[bold red]100% COLLISION (KEY EXPOSURE)[/bold red]" if collision else "[green]Unique[/green]"
        table.add_row(
            f"Transaction #{i+1}",
            f"{east_nonces[i][:16]}...{east_nonces[i][-8:]}",
            f"{west_nonces[i][:16]}...{west_nonces[i][-8:]}",
            status
        )
    console.print(table)

    print_breach(
        "Complete Private Key Extraction via Reused Nonces",
        "Gateway-East and Gateway-West generated IDENTICAL nonces ($k_1 == k_2$) for different transactions.\n"
        "Under ECDSA / Schnorr mathematics, given two signatures with the same nonce:\n"
        "  s1 = k^-1 * (z1 + r * x)  (mod n)\n"
        "  s2 = k^-1 * (z2 + r * x)  (mod n)\n"
        "  x = (s1 * z2 - s2 * z1) / (s2 * r - s1 * r)  (mod n)\n"
        "The master private key $x$ is extracted in less than 2 microseconds using basic schoolbook modular arithmetic!"
    )

    print_defense(
        "Hardware Monotonic Counters & Strict Anti-Rollback Write-Ahead Logs",
        "1. Never execute stateful or deterministic signing inside generic virtual machines or ephemeral containers.\n"
        "2. Implement ACPI VMGENID driver integration (Linux >= 5.18 add_vmfork_randomness).\n"
        "3. Stateful multi-party signing (FROST / MuSig2) MUST store nonces in hardware monotonic counters or append-only NVRAM."
    )
