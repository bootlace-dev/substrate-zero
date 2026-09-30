# Substrate Zero: Ephemeral Secret Lifecycle Testbed

```text
  ███████╗██╗   ██╗██████╗ ███████╗████████╗██████╗  █████╗ ████████╗███████╗    ███████╗███████╗██████╗  ██████╗ 
  ██╔════╝██║   ██║██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝██╔════╝    ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗
  ███████╗██║   ██║██████╔╝███████╗   ██║   ██████╔╝███████║   ██║   █████╗        ███╔╝ █████╗  ██████╔╝██║   ██║
  ╚════██║██║   ██║██╔══██╗╚════██║   ██║   ██╔══██╗██╔══██║   ██║   ██╔══╝       ███╔╝  ██╔══╝  ██╔══██╗██║   ██║
  ███████║╚██████╔╝██████╔╝███████║   ██║   ██║  ██║██║  ██║   ██║   ███████╗    ███████╗███████╗██║  ██║╚██████╔╝
  ╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝    ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ 
```

**Full-Stack Architectural Threat Model & Runtime Verification Testbed for Enterprise Ephemeral Secrets**  
*Maintained by [@bootlace-dev](https://github.com/bootlace-dev)*

---

## Executive Infrastructure Audit Directive (TL;DR for Security Leadership)

For CISOs, VPs of Infrastructure Security, and Principal Security Engineers managing enterprise TLS/mTLS proxies, SSH jump hosts, WireGuard VPN tunnels, HSM daemons, and digital asset custody platforms:

1. **Pillar 1 (Birth): MicroVM & TRNG Entropy Passthrough**
   - Verify all QEMU/KVM hypervisor definitions enforce `virtio-rng` passthrough (`<rng model='virtio'><backend model='random'>/dev/urandom</backend></rng>`).
   - Audit early-boot microVM services (SSH host key generators, mTLS bootstrappers) to guarantee they block on `getrandom()` rather than reading uninitialized `/dev/urandom` pools.
   - Enforce continuous NIST SP 800-90B health monitoring on bare-metal hardware TRNGs.

2. **Pillar 2 (Stretching): VM State Cloning & CSPRNG Reseeding**
   - Mandate `CONFIG_VMGENID=y` in guest kernel builds and hypervisor definitions.
   - Audit CSPRNG state drivers to verify ACPI unpause/restore events trigger immediate `getrandom()` re-seeding and ChaCha20-DRBG state invalidation.

3. **Pillar 3 (Consumption): Nonce Hygiene & Kleptographic Proofing**
   - Mandate hedged RFC 6979 deterministic nonces ($k = \text{HMAC}(x \parallel m \parallel \text{aux\_rand})$) across all signing binaries. Strictly forbid non-hedged random nonces.
   - Run statistical analysis to verify zero bitwise bias across signature nonces.
   - Enforce Sign-to-Contract (S2C) / Anti-Kleptography commitments on external signing hardware.

4. **Pillar 4 (Death - Part I): Compiler Assembly & DSE Verification**
   - Eliminate standard `memset()` for secret cleanup in C/C++ builds; enforce `explicit_bzero()`, C23 `memset_explicit()`, or volatile memory barrier fences (`asm volatile("" : : "r"(buf) : "memory")`).
   - Inspect ELF disassembly (`objdump -d` on `-O3` builds) to verify optimizing compilers have not stripped buffer zeroing via Dead-Store Elimination.

5. **Pillar 4 (Death - Part II): Kernel Memory Pinning & Swap Isolation**
   - Require `LimitMEMLOCK=infinity` and `LimitCORE=0` in systemd service units with explicit `mlock()` `errno` validation.
   - Enforce `madvise(MADV_DONTDUMP)` on secret allocations and execute high-value custody daemons strictly within stateless, swapless RAM disk (`tmpfs`) environments.

---

## The Substrate Boundary Thesis

Modern cybersecurity failures are rarely caused by flawed mathematical protocols or buggy software implementations:

```text
  ┌─────────────────────────┐
  │   1. THE PROTOCOL       │  ✔ Mathematically sound (e.g. secp256k1, TLS 1.3, WireGuard)
  └─────────────────────────┘
               │
               ▼
  ┌─────────────────────────┐
  │   2. THE IMPLEMENTATION │  ✔ Passes unit tests & static analysis (OpenSSL, Libsodium, C/Rust)
  └─────────────────────────┘
               │
               ▼
  ┌─────────────────────────┐
  │   3. THE RUNTIME EXEC   │  ✘ FAILS AT THE PHYSICAL SUBSTRATE
  └─────────────────────────┘    (Uninitialized microVM entropy, VM snapshot clones,
                                  compiler DSE stripping, silent mlock failure, NVMe swap bleed)
```

1. **The Protocol is Sound**: Formal specifications (TLS 1.3, RFC 8446, WireGuard, secp256k1, Ed25519) are mathematically proven.
2. **The Implementation is Compliant**: Software libraries (OpenSSL, Libsodium, custom C/Rust daemons) pass unit test suites and static analysis.
3. **The Substrate Execution Fails**: In production enterprise deployments, dynamic environmental factors—microVM container scaling, thermal load on TRNGs, compiler AST optimization passes (`gcc -O3`), container `rlimits`, and NVMe flash wear-leveling—silently break execution invariants.

Because these failure vectors depend on specific enterprise deployment topologies, **substrate security requires continuous runtime monitoring** rather than one-time compliance audits.

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
