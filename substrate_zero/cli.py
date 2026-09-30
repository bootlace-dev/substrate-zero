"""
Command-Line Interface & Interactive Terminal Menu for substrate-zero.
"""

import sys
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

from substrate_zero.ui import print_banner, console
from substrate_zero.chambers.pillar1_birth import trng_collapse, cloud_init_starvation
from substrate_zero.chambers.pillar2_stretching import milk_sad_cracker, vm_snapshot_clone
from substrate_zero.chambers.pillar3_consumption import lattice_hnp_crack, dark_skippy_mempool, high_throughput_throttle
from substrate_zero.chambers.pillar4_death import dse_assassin, memory_hygiene

CHAMBERS = {
    "1": ("Pillar 1: Silicon TRNG Collapse & #ifdef Fallbacks", trng_collapse.run_chamber),
    "2": ("Pillar 1: Early-Boot MicroVM & Cloud-Init Starvation", cloud_init_starvation.run_chamber),
    "3": ("Pillar 2: Libbitcoin 'Milk Sad' (CVE-2023-39910) 32-bit Seed Cracker", milk_sad_cracker.run_chamber),
    "4": ("Pillar 2: Virtual Machine Snapshot Rollback & PRNG Clones", vm_snapshot_clone.run_chamber),
    "5": ("Pillar 3: Lattice Nonce Bias (Hidden Number Problem) LLL Heist", lattice_hnp_crack.run_chamber),
    "6": ("Pillar 3: Dark Skippy Kleptographic Mempool Exfiltration", dark_skippy_mempool.run_chamber),
    "7": ("Pillar 3: High-Throughput Entropy Starvation & Insecure Fallback", high_throughput_throttle.run_chamber),
    "8": ("Pillar 4: The Compiler Assassin (Dead-Store Elimination / DSE)", dse_assassin.run_chamber),
    "9": ("Pillar 4: Memory Hygiene, mlock() Traps & NVMe Flash Bleed", memory_hygiene.run_chamber),
}

def run_all():
    print_banner()
    for key in sorted(CHAMBERS.keys(), key=int):
        title, func = CHAMBERS[key]
        console.rule(f"[bold cyan]{title}[/bold cyan]")
        func()
        console.print("\n")

def interactive_menu():
    while True:
        print_banner()
        table = Table(title="Interactive Substrate Zero Testbed Chambers", border_style="cyan")
        table.add_column("Key", style="bold yellow", width=5)
        table.add_column("Chamber Name & Vulnerability Vector", style="bold white")
        table.add_column("Pillar Category", style="dim cyan")

        for k in sorted(CHAMBERS.keys(), key=int):
            title, _ = CHAMBERS[k]
            pillar = title.split(":")[0]
            name = title.split(":")[1].strip()
            table.add_row(k, name, pillar)

        table.add_row("A", "Run All Chambers Sequentially (Full Suite)", "All Pillars")
        table.add_row("Q", "Exit Substrate Zero", "Exit")

        console.print(table)
        choice = Prompt.ask("\n[bold yellow]Select a Chamber to Execute[/bold yellow]", default="A").strip().upper()

        if choice == "Q":
            console.print("[dim]Exiting Substrate Zero. Substrate invariants preserved.[/dim]")
            sys.exit(0)
        elif choice == "A":
            run_all()
            Prompt.ask("\n[bold green]Press Enter to return to menu...[/bold green]")
        elif choice in CHAMBERS:
            title, func = CHAMBERS[choice]
            console.rule(f"[bold cyan]{title}[/bold cyan]")
            func()
            Prompt.ask("\n[bold green]Press Enter to return to menu...[/bold green]")
        else:
            console.print("[red]Invalid selection. Try again.[/red]")

@click.command()
@click.option("--all", "run_all_flag", is_flag=True, help="Execute all chambers sequentially.")
@click.option("--chamber", "chamber_id", type=str, help="Execute a specific chamber by number (1-9).")
def main(run_all_flag, chamber_id):
    """Substrate Zero: The Full-Stack Cryptographic Substrate & Ephemeral Secret Failure Testbed."""
    if run_all_flag:
        run_all()
    elif chamber_id:
        if chamber_id in CHAMBERS:
            title, func = CHAMBERS[chamber_id]
            print_banner()
            console.rule(f"[bold cyan]{title}[/bold cyan]")
            func()
        else:
            console.print(f"[red]Error: Unknown chamber ID '{chamber_id}'. Valid: 1-9.[/red]")
            sys.exit(1)
    else:
        interactive_menu()

if __name__ == "__main__":
    main()
