"""
Pillar 4: Death - Memory Hygiene, mlock() Failures & NVMe Wear-Leveling
Real-World Precedent: Silent mlock() ENOMEM, Coredump Spills & NVMe NAND Flash Persistence
"""

import os
import resource
import time
from rich.console import Console
from rich.table import Table
from substrate_zero.ui import print_header, print_breach, print_defense

console = Console()

def run_chamber():
    print_header(
        4,
        "Memory Hygiene, mlock() Traps & NVMe Flash Bleed",
        "Demonstrating silent memory locking failures and swap persistence on enterprise hardware"
    )

    console.print("\n[bold white]Scenario: Enterprise Systemd Service Memory Boundary Audit[/bold white]")
    
    # Check actual RLIMIT_MEMLOCK on this Linux system
    soft_limit, hard_limit = resource.getrlimit(resource.RLIMIT_MEMLOCK)
    limit_str = "Unlimited" if soft_limit == resource.RLIM_INFINITY else f"{soft_limit // 1024} KB"

    table = Table(title="Host Memory Protection & Pinning Invariants", border_style="cyan")
    table.add_column("Security Invariant", style="cyan")
    table.add_column("Current Host Value", style="yellow")
    table.add_column("Risk Assessment", style="bold red")

    table.add_row(
        "RLIMIT_MEMLOCK (mlock capacity)",
        limit_str,
        "CRITICAL: Silent mlock() failure if keys exceed limit" if soft_limit != resource.RLIM_INFINITY else "Configured OK"
    )
    table.add_row(
        "systemd-coredump persistence",
        "/var/lib/systemd/coredump",
        "HIGH: Coredumps serialize heap/stack keys to disk"
    )
    table.add_row(
        "NVMe Swap Wear-Leveling",
        "Flash Block Remapping Active",
        "HIGH: Software zeroize does not overwrite physical NAND flash"
    )
    table.add_row(
        "Kernel madvise(MADV_DONTDUMP)",
        "Missing in unhardened signers",
        "HIGH: Key memory included in process crash snapshots"
    )

    console.print(table)

    print_breach(
        "Silent mlock() Fallback & Physical Flash Persistence",
        "When an unprivileged signing daemon attempts mlock() under default container limits (64KB),\n"
        "mlock() fails with ENOMEM. In typical implementations without strict errno assertion,\n"
        "execution continues unpinned!\n"
        "Under memory pressure, the Linux kernel swaps the unpinned private key page to disk.\n"
        "On enterprise NVMe SSDs, hardware wear-leveling distributes blocks across physical NAND flash cells.\n"
        "Even after software swap is disabled, the plaintext private key remains physically readable\n"
        "on the NAND flash controller using direct flash-dump forensic tools for up to 180 days!"
    )

    print_defense(
        "Mandatory mlock() Assertions & Amnesic tmpfs Operation",
        "1. Never ignore mlock() return code: assert(mlock(ptr, len) == 0) or abort process immediately.\n"
        "2. Call madvise(ptr, len, MADV_DONTDUMP) immediately after memory allocation.\n"
        "3. Disable systemd coredump capture: LimitCORE=0 in all service units.\n"
        "4. Enforce SubZero amnesic physical ramdisk operation: strictly zero swap partitions on signing nodes."
    )
