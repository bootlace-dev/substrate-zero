"""
UI formatting, ASCII banners, and terminal helpers using Rich.
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()

BANNER_ART = r"""
  ███████╗██╗   ██╗██████╗ ███████╗████████╗██████╗  █████╗ ████████╗███████╗    ███████╗███████╗██████╗  ██████╗ 
  ██╔════╝██║   ██║██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝██╔════╝    ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗
  ███████╗██║   ██║██████╔╝███████╗   ██║   ██████╔╝███████║   ██║   █████╗        ███╔╝ █████╗  ██████╔╝██║   ██║
  ╚════██║██║   ██║██╔══██╗╚════██║   ██║   ██╔══██╗██╔══██║   ██║   ██╔══╝       ███╔╝  ██╔══╝  ██╔══██╗██║   ██║
  ███████║╚██████╔╝██████╔╝███████║   ██║   ██║  ██║██║  ██║   ██║   ███████╗    ███████╗███████╗██║  ██║╚██████╔╝
  ╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝    ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ 
"""

def print_banner():
    banner_text = Text(BANNER_ART, style="bold cyan")
    subtitle = Text(
        "WHERE CRYPTOGRAPHIC MATHEMATICS COLLIDE WITH PHYSICAL REALITY\n"
        "Full-Stack Ephemeral Secret Lifecycle Testbed | @bootlace-dev",
        style="bold white"
    )
    console.print(Panel(Text.assemble(banner_text, "\n", subtitle), border_style="cyan", expand=False))

def print_header(pillar_num: int, title: str, subtitle: str):
    header_text = Text()
    header_text.append(f"PILLAR {pillar_num}: {title.upper()}\n", style="bold yellow")
    header_text.append(subtitle, style="dim white")
    console.print(Panel(header_text, border_style="yellow", expand=False))

def print_breach(title: str, details: str):
    breach_text = Text()
    breach_text.append("🚨 CRYPTOGRAPHIC SUBSTRATE BREACH CONFIRMED\n", style="bold red")
    breach_text.append(f"Vector: {title}\n\n", style="bold white")
    breach_text.append(details, style="red")
    console.print(Panel(breach_text, border_style="red", expand=False))

def print_defense(title: str, details: str):
    defense_text = Text()
    defense_text.append("🛡️ INSTITUTIONAL HARDENING INVARIANT ENFORCED\n", style="bold green")
    defense_text.append(f"Remediation: {title}\n\n", style="bold white")
    defense_text.append(details, style="green")
    console.print(Panel(defense_text, border_style="green", expand=False))
