# substrate-zero

```
  ███████╗██╗   ██╗██████╗ ███████╗████████╗██████╗  █████╗ ████████╗███████╗    ███████╗███████╗██████╗  ██████╗ 
  ██╔════╝██║   ██║██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝██╔════╝    ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗
  ███████╗██║   ██║██████╔╝███████╗   ██║   ██████╔╝███████║   ██║   █████╗        ███╔╝ █████╗  ██████╔╝██║   ██║
  ╚════██║██║   ██║██╔══██╗╚════██║   ██║   ██╔══██╗██╔══██║   ██║   ██╔══╝       ███╔╝  ██╔══╝  ██╔══██╗██║   ██║
  ███████║╚██████╔╝██████╔╝███████║   ██║   ██║  ██║██║  ██║   ██║   ███████╗    ███████╗███████╗██║  ██║╚██████╔╝
  ╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝    ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ 
```

**Where Cryptographic Mathematics Collide with Physical Reality.**  
*The Full-Stack Cryptographic Substrate & Ephemeral Secret Failure Testbed (Silicon to Cloud)*  
*Maintained by [@bootlace-dev](https://github.com/bootlace-dev)*

---

## Executive Summary

When securing billions of dollars in corporate cryptocurrency reserves or sovereign infrastructure, catastrophic security breaches rarely stem from mathematical breaks of the underlying curves (e.g. solving discrete logarithms on $secp256k1$). 

They occur at **the substrate**: the unholy divergence between cryptographic specifications and physical execution.

`substrate-zero` is an interactive, runnable testbed and architectural threat model demonstrating how flawless 256-bit cryptography collapses across the four lifecycle phases of an ephemeral secret: **Birth, Stretching, Consumption, and Death**.

---

## The Executive Matrix: The 60-Second Reality Check

| Phase | Vulnerability Vector | The Illusion (Why the CTO Slept) | The Physical Reality (How Billions Were Lost) | Real-World Incident | Chamber Demo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Birth** | **Silicon TRNG Collapse** | "Our hardware wallet uses dual secure elements with an internal TRNG." | Thermal droop or compiler macros disabled the TRNG; firmware silently fell back to uninitialized SRAM. | Coldcard 2026 / Infineon ROCA | `Chamber 1` |
| **Birth** | **MicroVM Starvation** | "Our cloud nodes run ephemeral microVMs with fresh OS entropy." | MicroVMs booted in 50ms without `virtio-rng`; `/dev/urandom` emitted identical initial seeds across nodes. | Cloud-Init SSH Host Key Collisions | `Chamber 2` |
| **Stretching** | **Timestamp PRNG Seeding** | "Our microservice seeds keys with high-precision system clock ticks." | Microsecond timestamps yield $< 2^{32}$ entropy states, searchable on a commodity laptop in seconds. | Libbitcoin Milk Sad ($3M+ drained) | `Chamber 3` |
| **Stretching** | **Hypervisor VM Clones** | "Our signing gateways run in isolated hypervisor containers." | VM snapshot restore rolled back the ChaCha20 state vector; two nodes generated identical nonces. | VMGENID Race / Android SecureRandom | `Chamber 4` |
| **Consumption** | **Lattice Nonce Bias** | "Our signatures pass 100% of NIST statistical randomness tests." | A microscopic 4-bit bias in nonces allows LLL lattice reduction to recover the master private key in $<1$s. | Hidden Number Problem (Polynonce) | `Chamber 5` |
| **Consumption** | **Dark Skippy Kleptography** | "Every transaction signed by our cold storage passes verification." | Compromised firmware encoded the 24-word master seed into two public mempool signatures. | Dark Skippy (DEF CON 32) | `Chamber 6` |
| **Consumption** | **100k-TPS Starvation** | "Our high-throughput gateway has redundant crypto worker threads." | Process exhausted file descriptors on `/dev/urandom`; silent fallback downgraded to insecure `time()`. | API Gateway Silent Insecure Fallback | `Chamber 7` |
| **Death** | **Compiler Assassin (DSE)** | "Our developers explicitly called `memset(key, 0, 32)` on exit." | The compiler optimizer identified the buffer as dead and deleted the zeroization; keys leaked in coredump. | OpenSSL CVE-2008-0166 / LLVM DSE | `Chamber 8` |
| **Death** | **Memory Hygiene Decay** | "Our daemon runs under systemd with memory limits." | `mlock()` failed silently under default limits; private key swapped to NVMe NAND flash wear-leveling. | Coredump Spills & NVMe Flash Bleed | `Chamber 9` |

---

## Quickstart: Running the Demonstration Suite

### Option 1: Standalone Container Execution (Zero Host Dependencies)
Run the entire interactive suite in an isolated container:

```bash
docker run --rm -it bootlace-dev/substrate-zero:latest
```

### Option 2: Local Python Execution
Requires Python $\ge 3.10$ and GCC:

```bash
git clone https://github.com/bootlace-dev/substrate-zero.git
cd substrate-zero
pip install -r requirements.txt

# Launch interactive terminal UI
python3 -m substrate_zero.cli

# Or execute all chambers in headless CI mode
python3 scripts/run_all_chambers.py
```

---

## The 4 Pillars of the Ephemeral Secret Lifecycle

```
       [ PILLAR 1: BIRTH ]              [ PILLAR 2: STRETCHING ]
      Physical & Kernel TRNG             CSPRNG Expansion & State
    (Silicon, virtio-rng, ACPI)         (VMGENID, mt19937, Seeds)
                │                                   │
                ▼                                   ▼
    ┌───────────────────────┐           ┌───────────────────────┐
    │  EPHEMERAL SECRET     │ ────────► │  TRANSACTION SIGNING  │
    │  256-bit Scalar (x)   │           │  Nonce Commitment (k) │
    └───────────────────────┘           └───────────────────────┘
                │                                   │
                ▼                                   ▼
      [ PILLAR 4: DEATH ]             [ PILLAR 3: CONSUMPTION ]
      Memory Destruction                 Protocol Nonce Hygiene
    (DSE memset, mlock, NVMe)           (LLL Lattice, Dark Skippy)
```

### Pillar 1: Birth (Physical & Kernel Generation)
True random generation requires physical entropy from chaotic quantum or thermodynamic phenomena (thermal noise, avalanche breakdown, ring oscillator jitter).
- **Chamber 1 (Silicon TRNG Collapse):** Demonstrates how minor voltage droop or elevated temperature locks ring oscillators into harmonic loops, silently dropping entropy from 256 bits to a 64-bit periodic pattern without asserting a hardware error flag.
- **Chamber 2 (Early-Boot MicroVM Starvation):** Demonstrates how cloud-init scripts invoking `ssh-keygen` or `openssl` at T+120ms inside microVMs without `virtio-rng` read from an uninitialized `/dev/urandom` pool, generating identical host keys across independent nodes.

### Pillar 2: Stretching (State Duplication & Seeding)
A cryptographically secure pseudorandom number generator (CSPRNG) must expand a finite physical seed into an unpredictable stream.
- **Chamber 3 (Libbitcoin Milk Sad - CVE-2023-39910):** Live demonstration of cracking a 256-bit Bitcoin cold-storage wallet in $<1$ second because `bx seed` seeded Mersenne Twister (`mt19937`) with seconds-since-epoch.
- **Chamber 4 (VM Snapshot Rollback & PRNG Clones):** Demonstrates hypervisor snapshot rollbacks freezing the ChaCha20 state counter, causing cloned gateway instances to issue identical ECDSA nonces ($k_1 == k_2$) and exposing master private keys via schoolbook modular division.

### Pillar 3: Consumption (Protocol Nonce Hygiene & High-Throughput)
Even if the seed is pristine, cryptographic protocols consume nonces at massive scale. Any mathematical leakage in the nonce destroys the private key.
- **Chamber 5 (Lattice Nonce Bias / Hidden Number Problem):** Demonstrates how an attacker collecting public mempool signatures with a microscopic 4-bit nonce bias constructs a Kannan embedding matrix and runs Lenstra–Lenstra–Lovász (LLL) lattice reduction to extract the 256-bit private key in milliseconds.
- **Chamber 6 (Dark Skippy Kleptography):** Demonstrates how malicious firmware embeds a 24-word master seed into the public $r, s$ values of two innocent-looking mempool transactions, exfiltrating the entire wallet across an air-gap without network access.
- **Chamber 7 (High-Throughput Insecure Fallback):** Demonstrates an enterprise TLS/API gateway exhausting file descriptors (`EMFILE`) under 100k TPS and silently falling back to insecure `time()` nonces.

### Pillar 4: Death (Secret Destruction & Memory Hygiene)
Cryptographic secrets must be sanitized immediately upon completion of the mathematical operation.
- **Chamber 8 (The Compiler Assassin - Dead-Store Elimination):** Compiles live C signing code with `gcc -O3` and disassembles the machine code to prove that the compiler optimizer silently stripped `memset(scalar, 0, 32)`, leaving raw 256-bit private keys plaintext on the deallocated stack.
- **Chamber 9 (Memory Hygiene, mlock Traps & NVMe Flash Bleed):** Demonstrates silent `mlock()` failures under default container `RLIMIT_MEMLOCK` limits, causing private keys to swap to NVMe NAND flash memory where hardware wear-leveling preserves the key on the drive controller for months.

---

## Institutional Hardening Invariants

For organizations managing multi-billion dollar cryptocurrency reserves or Tier-1 infrastructure:

1. **Hedged Nonces (BIP-340 / Synthetic Nonces):** Never rely purely on RFC 6979 deterministic nonces (vulnerable to single-clock voltage fault injection) nor raw hardware TRNG nonces. Mandate hedged nonces: $k = \text{HMAC}(x \parallel m \parallel \text{aux\_rand})$.
2. **Anti-Kleptographic Verification (Sign-to-Contract / S2C):** Forbid blind signing on unverified firmware. Enforce Sign-to-Contract where the host coordinator injects external unpredictable entropy into the nonce commitment ($R' = R + e \cdot G$).
3. **Explicit Memory Sanitization:** Ban raw `memset()` in all cryptographic codebases. Enforce `explicit_bzero()`, C23 `memset_explicit()`, or volatile assembly memory barriers (`asm volatile("" : : "r"(buf) : "memory")`).
4. **Coredump Invalidation:** Configure systemd service units with `LimitCORE=0`, `MemoryDump=no`, and invoke `madvise(ptr, len, MADV_DONTDUMP)` on all secret allocations.
5. **Physical Amnesic Environments:** Execute high-value signing ceremonies exclusively in stateless RAM disks (SubZero architecture) on generic COTS hardware, bypassing persistent NAND flash storage.

---

## License

MIT License. Developed by [@bootlace-dev](https://github.com/bootlace-dev) for sovereign cryptographic defense.
