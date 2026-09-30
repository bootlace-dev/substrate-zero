# Substrate Zero: Ephemeral Secret Lifecycle Testbed

```text
  ███████╗██╗   ██╗██████╗ ███████╗████████╗██████╗  █████╗ ████████╗███████╗    ███████╗███████╗██████╗  ██████╗ 
  ██╔════╝██║   ██║██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝██╔════╝    ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗
  ███████╗██║   ██║██████╔╝███████╗   ██║   ██████╔╝███████║   ██║   █████╗        ███╔╝ █████╗  ██████╔╝██║   ██║
  ╚════██║██║   ██║██╔══██╗╚════██║   ██║   ██╔══██╗██╔══██║   ██║   ██╔══╝       ███╔╝  ██╔══╝  ██╔══██╗██║   ██║
  ███████║╚██████╔╝██████╔╝███████║   ██║   ██║  ██║██║  ██║   ██║   ███████╗    ███████╗███████╗██║  ██║╚██████╔╝
  ╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝    ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ 
```

**Full-Stack Architectural Threat Model & Verification Testbed for Enterprise Ephemeral Secrets**  
*Maintained by [@bootlace-dev](https://github.com/bootlace-dev)*

---

## Executive Architectural Summary

Enterprise security models—from TLS 1.3/mTLS session negotiation, SSH host authentication, WireGuard/IPsec VPN tunnels, zero-trust tokens, and Hardware Security Modules (HSMs), to high-value digital asset custody—depend fundamentally on the **ephemeral secret lifecycle**.

Catastrophic compromise rarely stems from mathematical breaks of underlying cryptographic primitives (such as computing discrete logarithms on prime-order elliptic curves). Instead, failure occurs at the **substrate layer**: the divergence between formal mathematical specifications and physical runtime execution across silicon, hypervisors, compilers, and operating system kernel boundaries.

`substrate-zero` is a deterministic threat model and executable verification testbed that demonstrates how mathematically pristine cryptographic implementations collapse across the four phases of the ephemeral secret lifecycle: **Birth, Stretching, Consumption, and Death**.

---

## Ephemeral Secret Lifecycle Threat Matrix

| Lifecycle Phase | Vulnerability Vector | Underlying Mechanism | Affected Systems | Remediation Invariant | Executable Chamber |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Birth** | Silicon TRNG Entropy Collapse | Thermal droop, voltage fluctuation, or disabled hardware macros lock ring oscillators into low-entropy loops. | HSMs, COTS Hardware Signers, Bare-Metal Nodes | Multi-source continuous entropy mixing & hardware TRNG health checks | `Chamber 1` |
| **Birth** | Cloud MicroVM Pool Starvation | Ephemeral containers booting in $<100$ms without `virtio-rng` read uninitialized `/dev/urandom` pools. | Cloud-Init SSH Host Keys, TLS Ephemeral ECDHE, Microservices | Mandate `virtio-rng` passthrough & block early execution until `getrandom()` initializes | `Chamber 2` |
| **Stretching** | Low-Entropy CSPRNG Seeding | Seeding random number generators with low-resolution system clock ticks yields $< 2^{32}$ searchable seed states. | Session Key Generation, Ephemeral Tokens, Key Derivation | Cryptographically secure CSPRNGs (ChaCha20-DRBG) seeded strictly from OS entropy pools | `Chamber 3` |
| **Stretching** | Hypervisor State Cloning | Virtual machine snapshot restores and hypervisor clones duplicate internal CSPRNG state vectors. | WireGuard Tunnels, TLS Gateways, Replicated Signers | Implement Linux `VMGENID` notifications to trigger CSPRNG re-seeding on VM unpause | `Chamber 4` |
| **Consumption** | Nonce Bitwise Bias | Microscopic bitwise bias in ECDSA/EdDSA nonces enables lattice reduction to extract master private keys. | Ephemeral Signing Daemons, mTLS Clients, PKI Authorities | Mandate hedged RFC 6979 deterministic nonces ($k = \text{HMAC}(x \parallel m \parallel \text{aux\_rand})$) | `Chamber 5` |
| **Consumption** | Anti-Kleptographic Exfiltration | Compromised firmware channels private master seeds through public signature nonce commitments. | Air-Gapped Signers, Isolated HSMs, Firmware Nodes | Enforce Sign-to-Contract (S2C) / Anti-Kleptography host entropy commitments | `Chamber 6` |
| **Consumption** | High-Throughput Resource Depletion | API gateways exhausting file descriptors (`EMFILE`) under 100k TPS fall back to non-cryptographic random calls. | High-Throughput TLS Proxies, Microservice Mesh Gateways | Pre-allocated entropy buffers & fail-closed system circuit breakers | `Chamber 7` |
| **Death** | Compiler Dead-Store Elimination (DSE) | Optimizing compilers (`gcc -O3`, `clang`) strip `memset()` calls on deallocated stack buffers as dead code. | C/C++ Ephemeral Cryptographic Libraries (OpenSSL, Libsodium) | Mandatory `explicit_bzero()`, C23 `memset_explicit()`, or memory barrier assembly fences | `Chamber 8` |
| **Death** | Kernel Swap & Memory Bleed | `mlock()` fails silently under default container limits, allowing secret memory pages to swap to persistent storage. | Containerized Daemons, Systemd Services, Cloud VM Hosts | Enforce strict `mlock()` assertions, `madvise(MADV_DONTDUMP)`, `LimitCORE=0`, and swapless RAM disks | `Chamber 9` |

---

## Architectural Lifecycle Pipeline

```text
       [ PILLAR 1: BIRTH ]              [ PILLAR 2: STRETCHING ]
      Physical & Kernel TRNG             CSPRNG Expansion & State
    (Silicon, virtio-rng, ACPI)         (VMGENID, ChaCha20-DRBG)
                │                                   │
                ▼                                   ▼
    ┌───────────────────────┐           ┌───────────────────────┐
    │  EPHEMERAL SECRET     │ ────────► │  SESSION / SIGNING    │
    │  Symmetric / Scalar   │           │  Ephemeral Nonce (k)  │
    └───────────────────────┘           └───────────────────────┘
                │                                   │
                ▼                                   ▼
       [ PILLAR 4: DEATH ]             [ PILLAR 3: CONSUMPTION ]
       Memory Destruction                 Protocol Nonce Hygiene
     (DSE memset, mlock, NVMe)           (Lattice HNP, Kleptography)
```

### Pillar 1: Birth (Entropy Generation & Hardware Boundaries)
Cryptographic security relies on non-deterministic physical entropy. 
- **Silicon TRNG Health**: Demonstrates hardware ring-oscillator lockup where thermal noise degradation causes silent entropy collapse down to 64-bit predictable state sequences.
- **Early-Boot Cloud MicroVMs**: Demonstrates identical SSH host key generation across cloud instances when ephemeral microVMs execute authentication daemons before `getrandom()` pool initialization.

### Pillar 2: Stretching (State Maintenance & CSPRNG Safety)
Expanding entropy seeds into continuous pseudo-random streams requires state isolation.
- **Timestamp Seeding Vulnerabilities**: Demonstrates full keyspace exhaustion ($< 2^{32}$ states) resulting from seeding pseudo-random generators with wall-clock microsecond timestamps.
- **Hypervisor VM Snapshot Duplication**: Demonstrates how restoring virtual machine snapshots duplicates the ChaCha20 counter state across parallel instances, producing identical ephemeral session nonces.

### Pillar 3: Consumption (Protocol Execution & Nonce Hygiene)
During active transport or signing operations, nonce bias compromises underlying long-term secrets.
- **Lattice Reduction (Hidden Number Problem)**: Demonstrates how a microscopic 4-bit nonce bias across public signatures allows Lenstra–Lenstra–Lovász (LLL) matrix reduction to extract the master private key in milliseconds.
- **Kleptographic Seed Leakage**: Demonstrates how malicious or compromised device firmware covertly encodes master keys into innocent signature structures without network egress.
- **High-Throughput Starvation**: Demonstrates resource exhaustion under high transaction volume causing silent fallback to non-cryptographic state generators.

### Pillar 4: Death (Secret Destruction & Memory Isolation)
Ephemeral secrets must be completely sanitized from process memory immediately after use.
- **Compiler Optimization Traps (DSE)**: Compiles C code under `gcc -O3` and inspects generated assembly to demonstrate how compilers delete sanitization `memset()` calls, leaving private keys readable in uninitialized stack memory.
- **Kernel Swap & Physical NVMe Persistence**: Demonstrates silent `mlock()` failure under standard container rlimits, causing unpinned secret pages to spill onto physical NVMe flash storage where hardware wear-leveling preserves data controllers across reboots.

---

## Enterprise Defense Invariants

For engineering organizations operating mission-critical infrastructure, TLS/mTLS gateways, PKI services, and digital asset signers:

1. **Continuous Entropy Auditing**: Never assume hardware TRNG health. Implement continuous health tests (NIST SP 800-90B) and mix multiple independent physical and kernel entropy sources.
2. **Hypervisor Reseeding**: Enforce Linux `VMGENID` drivers in all cloud microVM images to force immediate CSPRNG re-seeding upon VM snapshot restoration or unpause.
3. **Hedged Ephemeral Nonces**: Utilize hedged deterministic nonces ($k = \text{HMAC}(x \parallel m \parallel \text{aux\_rand})$) to combine deterministic safety with external entropy.
4. **Guaranteed Memory Sanitization**: Prohibit standard `memset()` for zeroing sensitive memory. Mandate `explicit_bzero()`, C23 `memset_explicit()`, or volatile memory barrier fences (`asm volatile("" : : "r"(buf) : "memory")`).
5. **Kernel Memory Pinning & Core Invalidation**: Assert `mlock()` return codes, set `madvise(MADV_DONTDUMP)`, enforce `LimitCORE=0` in systemd units, and execute signing processes on stateless, amnesic RAM disk environments.

---

## Execution & Verification

### Containerized Execution
Execute the verification suite within an isolated container:

```bash
docker run --rm -it bootlace-dev/substrate-zero:latest
```

### Local Execution & Testing
Requires Python $\ge 3.10$ and GCC:

```bash
git clone https://github.com/bootlace-dev/substrate-zero.git
cd substrate-zero
pip install -r requirements.txt

# Launch interactive demonstration interface
python3 -m substrate_zero.cli

# Execute automated test suite
make test
```

---

## License

MIT License. Authored by [@bootlace-dev](https://github.com/bootlace-dev) for sovereign infrastructure security and cryptographic defense.
