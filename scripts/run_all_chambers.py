#!/usr/bin/env python3
"""
Automated CI / Regression Test Runner for Substrate Zero.
Executes all 4 pillars and asserts zero execution failures.
"""

import sys
import os
import time

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from substrate_zero.cli import CHAMBERS, console

def main():
    console.print("[bold cyan]Substrate Zero: Commencing Full-Stack CI Chamber Regression...[/bold cyan]\n")
    start_time = time.perf_counter()
    failed = []

    for key in sorted(CHAMBERS.keys(), key=int):
        title, func = CHAMBERS[key]
        console.rule(f"[yellow]Executing {title}[/yellow]")
        try:
            func()
            console.print(f"[green]✓ Chamber {key} passed.[/green]\n")
        except Exception as e:
            console.print(f"[red]✗ Chamber {key} failed: {e}[/red]\n")
            failed.append((key, title, str(e)))

    total_time = time.perf_counter() - start_time
    console.rule("[bold cyan]Regression Summary[/bold cyan]")
    console.print(f"Total Chambers Executed: {len(CHAMBERS)}")
    console.print(f"Elapsed Execution Time:  {total_time:.2f}s")

    if failed:
        console.print(f"[bold red]FAILURES DETECTED ({len(failed)}):[/bold red]")
        for k, t, err in failed:
            console.print(f"  • Chamber {k} ({t}): {err}")
        sys.exit(1)
    else:
        console.print("[bold green]ALL 4 PILLARS & 9 CHAMBERS PASSED WITH VERIFIED BREACH PROOFS.[/bold green]")
        sys.exit(0)

if __name__ == "__main__":
    main()
