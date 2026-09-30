"""
Pillar 4: Death - The Compiler Assassin (Dead-Store Elimination)
Real-World Precedent: GCC/Clang -O3 silently stripping memset() leaving keys in memory/coredumps
"""

import subprocess
import os
import shutil
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from substrate_zero.ui import print_header, print_breach, print_defense

console = Console()

def run_chamber():
    print_header(
        4,
        "The Compiler Assassin: Dead-Store Elimination (DSE)",
        "Proving GCC/Clang -O3 silently deletes memset() zeroization from compiled assembly"
    )

    console.print("\n[bold white]Scenario: Developer Writes Cryptographic Transaction Signer[/bold white]")
    console.print("  [dim]• Language: C99 / Assembly[/dim]")
    console.print("  [dim]• Sensitive Variable: uint8_t ephemeral_scalar[32] (Stack Allocated)[/dim]")
    console.print("  [dim]• Security Contract: Developer explicitly calls memset(ephemeral_scalar, 0, 32) before return[/dim]\n")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    flawed_src = os.path.join(current_dir, "dse_signer.c")
    patched_src = os.path.join(current_dir, "dse_signer_patched.c")

    flawed_bin = "/tmp/dse_flawed"
    patched_bin = "/tmp/dse_patched"

    # Step 1: Compile flawed code
    console.print("[yellow]Compiling flawed signer with standard release optimization: 'gcc -O3' ...[/yellow]")
    res1 = subprocess.run(
        ["gcc", "-O3", "-fno-stack-protector", flawed_src, "-o", flawed_bin],
        capture_output=True, text=True
    )
    if res1.returncode != 0:
        console.print(f"[red]Compilation failed: {res1.stderr}[/red]")
        return

    # Step 2: Compile patched code
    console.print("[yellow]Compiling patched signer with memory barriers: 'gcc -O3' ...[/yellow]")
    res2 = subprocess.run(
        ["gcc", "-O3", "-fno-stack-protector", patched_src, "-o", patched_bin],
        capture_output=True, text=True
    )

    # Step 3: Disassemble both functions
    obj_flawed = subprocess.run(
        ["objdump", "-d", flawed_bin],
        capture_output=True, text=True
    ).stdout

    obj_patched = subprocess.run(
        ["objdump", "-d", patched_bin],
        capture_output=True, text=True
    ).stdout

    flawed_asm = []
    capture = False
    for line in obj_flawed.splitlines():
        if "<sign_transaction_flawed>:" in line:
            capture = True
        elif capture and ("<" in line or not line.strip()):
            break
        elif capture:
            flawed_asm.append(line)

    patched_asm = []
    capture = False
    for line in obj_patched.splitlines():
        if "<sign_transaction_secure>:" in line:
            capture = True
        elif capture and ("<" in line or not line.strip()):
            break
        elif capture:
            patched_asm.append(line)

    p1 = Panel(
        Text("\n".join(flawed_asm[:10]), style="red"),
        title="[bold red]Flawed Binary (memset deleted by DSE)[/bold red]",
        border_style="red"
    )
    p2 = Panel(
        Text("\n".join(patched_asm[:12]), style="green"),
        title="[bold green]Patched Binary (pxor/movaps preserved)[/bold green]",
        border_style="green"
    )

    console.print(Columns([p1, p2]))

    # Step 4: Live Execution & Stack Inspection
    console.print("\n[bold white]Executing Flawed Binary and Probing Stack Frame After Function Return...[/bold white]")
    run_res = subprocess.run([flawed_bin], capture_output=True, text=True)
    console.print(f"  Execution Output: {run_res.stdout.strip()}")

    print_breach(
        "Compiler Stripped Zeroization (Secret Persists in Stack)",
        "The compiler's Dead-Store Elimination pass determined 'ephemeral_scalar' is dead\n"
        "because it is not read again before the function executes 'ret'.\n"
        "The memset() call was silently dropped from the final machine code!\n"
        "The raw 256-bit scalar remains in plaintext on the deallocated stack.\n"
        "If a subsequent crash occurs, systemd-coredump or Google Breakpad will serialize\n"
        "this plaintext private key to disk or send it to centralized monitoring (Datadog/Sentry)!"
    )

    print_defense(
        "explicit_bzero & Memory Barrier Fences",
        "1. Never use standard memset() to sanitize secrets; use explicit_bzero() or C23 memset_explicit().\n"
        "2. In custom assembly / C: asm volatile(\"\" : : \"r\"(buf) : \"memory\") to force a memory barrier.\n"
        "3. In Rust: enforce the 'zeroize' crate with volatile memory writes (ZeroizeOnDrop).\n"
        "4. Enforce systemd: LimitCORE=0 and call madvise(..., MADV_DONTDUMP) on all secret memory pages."
    )
