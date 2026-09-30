"""
Pillar 3: Consumption - High-Throughput Entropy Exhaustion & Fallback Trap
Real-World Precedent: 100k-TPS Gateways, Syscall Lock Contention & EMFILE Silent Fallbacks
"""

import time
import hashlib
from rich.console import Console
from rich.table import Table
from substrate_zero.ui import print_header, print_breach, print_defense

console = Console()

class HighThroughputGateway:
    """Simulates an enterprise TLS/API gateway terminating high connection volumes."""
    def __init__(self, fd_limit=1024):
        self.fd_limit = fd_limit
        self.active_connections = 0

    def generate_tls_session_key(self, conn_id: int):
        self.active_connections += 1
        
        # When file descriptors or syscalls fail under high concurrency
        if self.active_connections > self.fd_limit:
            # FATAL BUG: Silent try-catch fallback in legacy/defective crypto wrappers
            # Rather than failing closed and dropping the connection, developer fell back to time()
            fallback_seed = int(time.time())
            return {
                "conn_id": conn_id,
                "key": hashlib.sha256(f"insecure_time_fallback_{fallback_seed}".encode()).hexdigest(),
                "fallback": True
            }
        else:
            import secrets
            return {
                "conn_id": conn_id,
                "key": secrets.token_hex(32),
                "fallback": False
            }

def run_chamber():
    print_header(
        3,
        "High-Throughput Entropy Starvation & Silent Fallback",
        "Demonstrating EMFILE exhaustion on /dev/urandom and silent degradation to predictable keys"
    )

    console.print("\n[bold white]Scenario: Enterprise Financial Ingress Gateway Under Peak Market Traffic[/bold white]")
    console.print("  [dim]• Ingress Rate: 50,000 TLS 1.3 handshakes / second[/dim]")
    console.print("  [dim]• Host Resource Boundary: RLIMIT_NOFILE = 1,024 file descriptors[/dim]")
    console.print("  [dim]• Library Implementation: open(\"/dev/urandom\", O_RDONLY) inside worker threads[/dim]\n")

    gateway = HighThroughputGateway(fd_limit=100)
    # Simulate connection surge past FD limits
    for cid in range(1, 101):
        gateway.generate_tls_session_key(cid)

    console.print("[yellow]Surge event: Traffic exceeds 100 concurrent workers. open('/dev/urandom') returns EMFILE (-1)...[/yellow]")
    time.sleep(0.4)

    overflow_keys = [gateway.generate_tls_session_key(100 + i) for i in range(1, 5)]

    table = Table(title="Live TLS Session Key Generation Under Resource Exhaustion", border_style="red")
    table.add_column("Connection ID", style="cyan")
    table.add_column("Generated Session Key", style="white")
    table.add_column("Entropy Source", style="yellow")
    table.add_column("Security State", style="bold red")

    for k in overflow_keys:
        table.add_row(
            f"Conn #{k['conn_id']}",
            f"{k['key'][:20]}...{k['key'][-12:]}",
            "time() Fallback (EMFILE)",
            "[bold red]PREDICTABLE (DECRYPTABLE)[/bold red]"
        )
    console.print(table)

    print_breach(
        "Silent Fail-Open to Insecure Pseudorandom Fallback",
        "When the process hit file descriptor limits on /dev/urandom, execution did NOT abort.\n"
        "A legacy try-catch wrapper caught the error and silently fell back to standard time() seeding.\n"
        "Every subsequent TLS session key generated in that time window shared identical keys.\n"
        "Passive network eavesdroppers can decrypt enterprise API traffic in real-time."
    )

    print_defense(
        "vDSO getrandom(2) & Strict Fail-Closed Security",
        "1. Never use open('/dev/urandom') in network daemons; mandate getrandom(2) or vDSO getrandom (Linux >= 6.11).\n"
        "2. Cryptographic operations MUST fail-closed: if entropy acquisition fails, terminate the process (SIGABRT).\n"
        "3. Monitor file-descriptor limits (RLIMIT_NOFILE) and kernel lock contention (%sy) via Prometheus/eBPF."
    )
