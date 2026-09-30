"""
Pillar 1: Birth - Early-Boot MicroVM Entropy Starvation
Real-World Precedent: Cloud-Init SSH Host Key Collisions / Missing virtio-rng
"""

import time
import hashlib
from rich.console import Console
from rich.table import Table
from substrate_zero.ui import print_header, print_breach, print_defense

console = Console()

def run_chamber():
    print_header(
        1,
        "Early-Boot MicroVM & Cloud-Init Starvation",
        "Demonstrating host key collision across ephemeral nodes with uninitialized entropy pool"
    )

    console.print("\n[bold white]Scenario: Spawning 5 Ephemeral Cloud MicroVMs (AWS Firecracker / GCP Cloud Run)[/bold white]")
    console.print("  [dim]• Hypervisor configuration: Missing virtio-rng device[/dim]")
    console.print("  [dim]• Storage layer: virtio-blk with /sys/block/vda/queue/add_random = 0[/dim]")
    console.print("  [dim]• Execution timing: cloud-init invokes 'ssh-keygen -t ed25519' at T+120ms[/dim]\n")

    # Simulate 5 microVMs booted in the same millisecond window with uninitialized entropy pool
    # The Linux kernel pool has 0 bits of true entropy; output is derived from static initial seed + tick counter
    simulated_tick_base = 0x1000  # Low-entropy static base
    nodes = []
    for node_id in range(1, 6):
        # Two nodes boot at identical tick, others within tiny delta
        tick = simulated_tick_base if node_id in [1, 2] else simulated_tick_base + (node_id * 3)
        mock_pool = hashlib.sha256(f"static_kernel_init_state_tick_{tick}".encode()).digest()
        
        # Derive mock Ed25519 host key public fingerprint
        pubkey = hashlib.sha256(b"ed25519_pub:" + mock_pool).hexdigest()[:32]
        privkey = hashlib.sha256(b"ed25519_priv:" + mock_pool).hexdigest()
        nodes.append({
            "id": f"node-{node_id}.infra.internal",
            "tick": tick,
            "pubkey": pubkey,
            "privkey": privkey,
            "collision": node_id in [1, 2]
        })

    table = Table(title="Generated SSH Host Keys Across 5 Fresh Cloud Nodes", border_style="cyan")
    table.add_column("Node FQDN", style="cyan")
    table.add_column("Kernel Jitter State", style="yellow")
    table.add_column("Ed25519 Host Key Fingerprint (SHA256)", style="white")
    table.add_column("Security Status", style="bold red")

    for node in nodes:
        status = "[bold red]DUPLICATE HOST KEY (CRITICAL)[/bold red]" if node["collision"] else "[green]Independent (Low Entropy)[/green]"
        table.add_row(
            node["id"],
            f"T+{node['tick'] - simulated_tick_base}ms",
            f"SHA256:{node['pubkey'][:16]}...",
            status
        )
    console.print(table)

    print_breach(
        "SSH Host Key / TLS Certificate Collision",
        "Node-1 and Node-2 generated IDENTICAL Ed25519 host keys.\n"
        "An attacker connecting to Node-1 can impersonate Node-2 across the internal VPC,\n"
        "perform complete Man-in-the-Middle (MitM) decryption of administrative SSH tunnels,\n"
        "and inject arbitrary commands without triggering host key mismatch warnings."
    )

    print_defense(
        "Mandatory virtio-rng Hardware Pass-Through & getrandom(2) Blocking",
        "1. Never read from /dev/urandom in early-boot scripts; enforce getrandom(GRND_RANDOM) which blocks until pool is credited.\n"
        "2. Mandatory QEMU/KVM hypervisor directive: '<rng model=\"virtio\"><backend model=\"random\">/dev/urandom</backend></rng>'.\n"
        "3. Systemd service units generating keys must specify: 'After=systemd-random-seed.service'."
    )
