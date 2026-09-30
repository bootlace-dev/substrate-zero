"""
Pillar 1: Birth - Silicon TRNG Collapse & Firmware #ifdef Fallback
Real-World Precedent: Coldcard 2026 #ifdef MICROPY_HW_ENABLE_RNG / Infineon ROCA
"""

import time
import hashlib
from rich.console import Console
from rich.table import Table
from substrate_zero.ui import print_header, print_breach, print_defense

console = Console()

class SiliconTRNGSimulator:
    def __init__(self, mode="normal"):
        self.mode = mode

    def read_hardware_entropy(self, num_bytes=32):
        if self.mode == "normal":
            # Genuine thermal noise simulation
            import secrets
            return secrets.token_bytes(num_bytes)
        elif self.mode == "thermal_collapse":
            # Ring oscillators lock to harmonic under voltage droop/heat
            # Output periodic repeating bitstream
            base_pattern = b"\xca\xfe\xba\xbe\xde\xad\xbe\xef"
            return (base_pattern * (num_bytes // len(base_pattern) + 1))[:num_bytes]
        elif self.mode == "firmware_fallback":
            # Simulates Coldcard #ifndef MICROPY_HW_ENABLE_RNG fallback to uninitialized SRAM
            # Static uninitialized buffer left over from bootloader
            return bytes([0x55, 0xaa] * 16)

def run_chamber():
    print_header(
        1,
        "Silicon & Hardware TRNG Collapse",
        "Demonstrating silent hardware entropy decay & firmware #ifdef fallback"
    )

    console.print("\n[bold white]Phase 1: Standard Hardware TRNG Generation (Nominal Operating Conditions)[/bold white]")
    trng_normal = SiliconTRNGSimulator(mode="normal")
    normal_keys = [trng_normal.read_hardware_entropy().hex() for _ in range(3)]
    for i, k in enumerate(normal_keys, 1):
        console.print(f"  Key {i} (256-bit): [green]{k[:16]}...{k[-16:]}[/green] [dim](Entropy: 256.0 bits)[/dim]")

    console.print("\n[bold white]Phase 2: Inducing Physical Stress / Firmware Macro Misconfiguration[/bold white]")
    console.print("  [yellow]→ Injected Condition: Voltage droop causes Ring Oscillators to lock to harmonic.[/yellow]")
    console.print("  [yellow]→ Firmware Status Register: Fails to assert HAL_RNG_ERROR (Silent Fail-Open).[/yellow]")
    
    time.sleep(0.6)
    trng_collapsed = SiliconTRNGSimulator(mode="thermal_collapse")
    bad_keys = [trng_collapsed.read_hardware_entropy().hex() for _ in range(4)]
    
    table = Table(title="Generated Key Stream Under Substrate Collapse", border_style="red")
    table.add_column("Device Instance", style="cyan")
    table.add_column("Generated 256-bit Key / Seed", style="red")
    table.add_column("Shannon Entropy / Byte", style="yellow")
    table.add_column("Key Status", style="bold red")

    for i, k in enumerate(bad_keys, 1):
        table.add_row(
            f"HWW Node #{i}",
            f"{k[:24]}...{k[-16:]}",
            "1.21 bits",
            "COMPROMISED (Periodic)"
        )
    console.print(table)

    print_breach(
        "Silicon Thermal Collapse & #ifdef Fail-Open",
        "The hardware wallet firmware reported 'Key Generation Successful'.\n"
        "Because status registers were unchecked and no physical dice/coin entropy was mixed,\n"
        "the 256-bit master seed collapsed to a 64-bit periodic pattern.\n"
        "Total search space reduced from 2^256 to < 2^16. Exploitable in 0.04 seconds."
    )

    print_defense(
        "Strict Fail-Closed Architecture & Physical Entropy Verification",
        "1. Firmware must NEVER compile conditional fallbacks for TRNG failure (#error on missing RNG).\n"
        "2. Continuous online NIST SP 800-90B health tests (Repetition Count Test & Adaptive Proportion Test).\n"
        "3. Mandate physical entropy injection (SubZero / physical coin-flips) mixed via HMAC-SHA512."
    )
