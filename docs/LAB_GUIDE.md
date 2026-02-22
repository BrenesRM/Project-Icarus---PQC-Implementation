# 📋 Project Icarus — Class Lab Guide
### *Post-Quantum Cryptography in Action: A Daily Cybersecurity Perspective*

> **Audience:** Security students, SysAdmins, and Cybersecurity practitioners  
> **Duration:** ~90 minutes  
> **Difficulty:** Intermediate  
> **Prerequisites:** Basic Python, familiarity with symmetric/asymmetric encryption concepts

---

## 🧪 Lab Objective

You are a **Research Scientist at the Icarus Division**. Your mission: establish a tamper-proof, quantum-safe telemetry channel between a theoretical *Negative-Mass Generator* field station and a remote *Observation Post*.

A well-funded adversary code-named **"Quantum Specter"**, operating a **10,000-qubit quantum processor**, will attempt to intercept the gravitational variance coordinates mid-transmission.

You must defeat them.

---

## 🔑 Why This Matters Every Day

Before diving into the sci-fi scenario, let's ground every concept in **daily cybersecurity reality**:

| Lab Scenario | Real-World Equivalent | Daily Impact |
|---|---|---|
| Telemetry from gravity generator | API telemetry, sensor data, SCADA | Industrial control compromise |
| ML-KEM key exchange | Future TLS 1.3 handshake | Every HTTPS connection you make |
| Quantum MITM attacker | Nation-state threat actor | Critical infrastructure attacks |
| SHA-3 integrity hash | File integrity, blockchain, PKI | Software supply chain security |
| Ephemeral keys (PFS) | Signal, WhatsApp, WireGuard VPN | Privacy for communications |
| Cryptographic agility | System migration readiness | "Harvest Now, Decrypt Later" |

> **⚠ The Real Threat:** Adversaries are **already harvesting encrypted traffic today** to decrypt it once quantum computers mature. This is called a **"Harvest Now, Decrypt Later" (HNDL)** attack. Organizations that don't migrate to PQC now are accepting that their data will eventually be exposed.

---

## 📐 Mathematical Foundation

### The Lattice — Security Backbone of ML-KEM

A **lattice** in n-dimensional space is defined as:

```
L(v₁, v₂, ..., vₙ) = { Σ aᵢvᵢ | aᵢ ∈ ℤ }
```

Visualize it as an infinite grid of points in n-dimensional space, where every point is reachable by taking integer combinations of the basis vectors `v₁...vₙ`.

The **Shortest Vector Problem (SVP)**: *Given a lattice basis, find the shortest non-zero vector in the lattice.*

```
         ·  ·  ·  ·  ✦  ·  ·          ← ✦ is the shortest vector from origin
         ·  ·  ·  ·  ·  ·  ·
         ·  ·  O  ·  ·  ·  ·          ← O is the origin
         ·  ·  ·  ·  ·  ·  ·
         ·  ·  ·  ·  ·  ·  ·
```

**Why SVP is the security backbone:**
- With a "good basis" (nearly orthogonal vectors → **private key**): SVP is easy to solve in polynomial time.
- With a "bad basis" (non-orthogonal vectors → **public key**): SVP requires **exponential time** even on quantum computers.
- ML-KEM stores the private key as the good basis and releases only the bad basis publicly.

**ML-KEM Security Levels:**

| Parameter Set | Lattice Dimension | Classical Security | Post-Quantum Security | Use Case |
|---|---|---|---|---|
| ML-KEM-512 | 512 | ~2^140 | ~2^118 | IoT, constrained devices |
| ML-KEM-768 | 768 | ~2^178 | **~2^161** | General purpose (**our lab**) |
| ML-KEM-1024 | 1024 | ~2^218 | ~2^200 | Top-secret, long-term |

---

### The Metric Tensor — Our Telemetry Data

In General Relativity, spacetime geometry is described by the **metric tensor** gμν — a 4×4 symmetric matrix:

```
         [g_tt  g_tx  g_ty  g_tz]
gμν  =   [g_xt  g_xx  g_xy  g_xz]
         [g_yt  g_yx  g_yy  g_yz]
         [g_zt  g_zx  g_zy  g_zz]
```

For flat spacetime (Minkowski), gμν = diag(-1, +1, +1, +1).

Our generator creates a **perturbation** δgμν:
```
g_perturbed(μ,ν) = η(μ,ν) + δg(μ,ν)
```

The dominant component `δg_tt` encodes the gravitational constant reduction:
```
G_local = G₀ × (1 - ε),    where ε = 0.073  (7.3% reduction)
```

**The cybersecurity parallel:** Just like the metric tensor precisely describes spacetime, structured telemetry payloads (with defined schemas and integrity hashes) describe real-world sensor environments. Both require **integrity protection** — any modification must be detectable.

---

## 🔬 Lab Phases — Step-by-Step Procedure

---

### 🔑 Phase 1 — Key Generation
**Duration:** 10 minutes  
**File:** `src/phase1_key_generation.py`

#### What Happens
The Observation Post generates an **ephemeral ML-KEM-768 key pair** before any communication occurs.

**Critical Design Decision: Ephemeral Keys**  
Each tunnel session generates a **brand-new** key pair. This provides **Perfect Forward Secrecy (PFS)**:
- Session 1: key pair A
- Session 2: key pair B (no relation to A)
- Session 3: key pair C

If Quantum Specter somehow compromises Session 2's key, Sessions 1, 3, 4, ... are **mathematically unaffected**.

**Daily Relevance — Why You Generate New Keys Per Session:**
> Your bank's website (ECDHE-based today, ML-KEM-based soon) generates a new ephemeral key every time you connect. If someone records your encrypted traffic for years, then breaks your key, they only get THAT session — not your entire account history.

#### Run & Observe
```bash
python src/phase1_key_generation.py
```

**Expected Outputs:**
- ML-KEM-768 public key: **1,184 bytes** (transmitted to generator station)
- ML-KEM-768 private key: **2,400 bytes** (never leaves the observation post)
- `output/keys.json` created

#### Discussion Questions
1. Why is the public key larger than in classical RSA (2048-bit RSA public key = 256 bytes)?
2. What would happen to the security of all past sessions if we reused the same key pair?
3. Compare ML-KEM-768's 2^161 post-quantum security to a 10,000-qubit processor. Is the adversary a realistic threat today?

---

### 📡 Phase 2 — Telemetry Payload Construction
**Duration:** 15 minutes  
**File:** `src/phase2_telemetry_payload.py`

#### What Happens
The generator station builds a structured telemetry packet containing:

1. **Classification header** — mirrors real Data Loss Prevention (DLP) policies
2. **Coordinates** — the primary adversary target
3. **Metric tensor δgμν** — the physics payload (4×4 tensor)
4. **System health / decoherence rate** — operational metadata
5. **SHA-3-256 integrity fingerprint** — computed over the physics block

#### The Integrity Hash — SHA-3-256
```python
hash = SHA3_256(json.dumps(physics_block, sort_keys=True))
```

SHA-3 uses the **Keccak sponge construction** — fundamentally different from SHA-2's Merkle-Damgård design. This means SHA-3 is **not vulnerable** to length-extension attacks that affect some SHA-2 uses.

**Why SHA-3 here?**  
NIST's PQC standards for signatures (ML-DSA, SLH-DSA) internally use SHAKE-256 (a SHA-3 variant). Using SHA-3 for our payload hash maintains **algorithmic consistency** — one quantum-resistant hash family throughout.

#### Daily Relevance — Data Classification
> Every organization with a security policy has a **data classification scheme**: Public → Internal → Confidential → Restricted. This lab's `TOP SECRET // PQC-PROTECTED // ICARUS` header teaches you to think about **what data requires what protection level** — the foundation of risk-based security.

#### Run & Observe
```bash
python src/phase2_telemetry_payload.py
```

**Expected Outputs:**
- Formatted δgμν tensor table (4×4 values)
- SHA-3-256 integrity hash
- `output/telemetry_payload.json` created

#### Discussion Questions
1. Why do we sort the JSON keys (`sort_keys=True`) before hashing? What attack does this prevent?
2. The hash covers only the `physics` block, not the entire payload. What are the pros and cons of this?
3. Map the CIA Triad to the payload: what provides Confidentiality, Integrity, Availability?

---

### 🔒 Phase 3 — Secure Tunnel Establishment
**Duration:** 20 minutes  
**File:** `src/phase3_secure_tunnel.py`

#### What Happens: Hybrid Encryption

This phase implements the **hybrid encryption pattern** — the same pattern used in TLS 1.3, Signal, and WireGuard:

```
┌─────────────────────────────────────────────────────────────┐
│                     NETWORK (insecure)                       │
│                                                              │
│  SENDER ──── [ML-KEM ciphertext] ──────────────── RECEIVER  │
│  SENDER ──── [nonce + AES ciphertext + GCM tag] ── RECEIVER │
│  SENDER ──── [AAD: 'icarus-telemetry-channel'] ─── RECEIVER │
│                                                              │
└─────────────────────────────────────────────────────────────┘

  SENDER local only:          RECEIVER local only:
  • ML-KEM shared_secret  ←→  • ML-KEM shared_secret (matched)
  • AES-256-GCM session key   • AES-256-GCM session key (derived same way)
```

#### Step A — Key Encapsulation (ML-KEM)
```
sender.encap(PK_receiver) → (kem_ciphertext, shared_secret)
receiver.decap(SK_receiver, kem_ciphertext) → shared_secret
```
Both parties now share the **same secret** without ever transmitting it!

#### Step B — Key Derivation (HKDF)
```
session_key = HKDF-SHA3-256(shared_secret, info="icarus-tunnel-v1")
```
HKDF **stretches and randomizes** the ML-KEM output into a proper 256-bit AES key.  
The `info` parameter acts as a **domain separator** — the same shared secret cannot accidentally produce identical keys in different protocol contexts.

#### Step C — Authenticated Encryption (AES-256-GCM)
```
(ciphertext, auth_tag) = AES-256-GCM.Encrypt(key, nonce, plaintext, AAD)
```
AES-GCM provides:
- **Confidentiality:** Data is unreadable without the key
- **Integrity:** Any modification invalidates the auth_tag
- **Authentication:** Only the key holder could produce this ciphertext

#### Why AES-256 Is Quantum-Safe
Grover's Algorithm provides a **quadratic speedup** on brute-force search:
- AES-128: Classical 2^128 → Quantum 2^64 (**NOT safe**)
- AES-256: Classical 2^256 → Quantum 2^128 (**Safe — matches desired security level**)

#### Run & Observe
```bash
python src/phase3_secure_tunnel.py
```

#### Discussion Questions
1. Why use hybrid encryption instead of encrypting everything with ML-KEM directly?
2. The nonce is randomly generated per message. What happens if the SAME nonce is used twice with the same key in GCM mode?
3. The AAD is transmitted in plaintext but authenticated. Why would you want authenticated-but-not-encrypted data?

---

### ⚔️ Phase 4 — Quantum Man-in-the-Middle Attack
**Duration:** 20 minutes  
**File:** `src/phase4_quantum_mitm_attack.py`

#### The Adversary: Quantum Specter

```
Qubit Count:    10,000 physical qubits
Coherence Time: ~87 microseconds
Goal:           Recover gravity-nullification coordinates
Method:         Shor-family lattice reduction + Grover oracle
```

#### Attack 1 — Lattice Attack on ML-KEM

The adversary intercepts the KEM ciphertext and attempts to recover the private key by solving the underlying MLWE problem.

**Why it fails:**

| Obstacle | Explanation |
|---|---|
| **Decoherence** | 87µs coherence time. A lattice sieving computation would require continuous quantum operation for years |
| **Logical qubit overhead** | Error correction requires ~1,000 physical qubits per logical qubit. 10,000 physical → ~10 logical. Need ~1M logical qubits for ML-KEM-768 attacks |
| **SVP complexity** | Best known quantum algorithms for MLWE offer at most polynomial speedup, not exponential |
| **Post-quantum security** | ML-KEM-768 provides ~2^161 operations to break — at 10^15 ops/sec, that's 10^33 years |

#### Attack 2 — Bit-Flip / Tampering Attack

Even without breaking the key, the adversary tries a **bit-flip attack** on the AES ciphertext — hoping to corrupt the coordinates.

**Why it fails:** AES-256-GCM computes an authentication tag over both the ciphertext and the AAD. A single bit flip produces a different tag → `InvalidTag` exception → **payload discarded**.

#### Daily Relevance — Real MITM Threats Today

The MITM scenario is not science fiction — it happens constantly:

| MITM Vector | Description | Mitigation |
|---|---|---|
| **ARP Poisoning** | Attacker maps their MAC to victim's IP on a LAN | Dynamic ARP Inspection, 802.1X |
| **BGP Hijacking** | Rogue router announces false routing paths | RPKI, BGP route filtering |
| **SSL Stripping** | Downgrades HTTPS to HTTP before the user sees the lock | HSTS preloading |
| **Evil Twin AP** | Malicious Wi-Fi access point mimics a trusted network | 802.1X authentication, VPN |
| **DNS Spoofing** | Returns false IP addresses for domain queries | DNSSEC |

ML-KEM defends against the quantum-enhanced version of key-exchange interception.

#### Run & Observe
```bash
python src/phase4_quantum_mitm_attack.py
```

#### Discussion Questions
1. Why is "Harvest Now, Decrypt Later" classified as a current (not future) threat?
2. What role does Perfect Forward Secrecy play in limiting HNDL blast radius?
3. Can AES-256-GCM be broken by a quantum computer? Justify using Grover's algorithm complexity.

---

### 🌪️ Phase 5 — Decoherence & Cryptographic Agility
**Duration:** 15 minutes  
**File:** `src/phase5_decoherence_simulation.py`

#### Decoherence — The Quantum Achilles Heel

**Quantum decoherence** is the process by which a quantum system loses its quantum properties (superposition, entanglement) through interaction with its environment.

```
|ψ⟩ = α|0⟩ + β|1⟩  →  (decoherence)  →  |0⟩ or |1⟩  (classical state)
```

Current quantum processors have coherence times measured in **microseconds to milliseconds** (IBM Eagle: ~100µs, Google Sycamore: ~10–100µs). A meaningful attack on ML-KEM would require sustained coherent operation over years of computation — impossible with today's hardware.

This is why the threat is **real but not imminent** — and why we must **start migrating now**.

#### Cryptographic Agility

The simulation also demonstrates a **cryptographic agility fallback chain**:

```
System Health > 70%:  ML-KEM-768    (NIST Level 3  — ideal)
System Health > 40%:  ML-KEM-1024   (NIST Level 5  — heavier but more secure)
System Health > 20%:  ML-DSA+AES    (signature-based, still PQC)
System Health < 20%:  X25519+AES256 (classical emergency — NOT quantum-safe)
```

**Cryptographic agility** means your system can swap algorithms without changing the application layer. Hard-coding a single algorithm is a **maintenance and security debt**.

#### Daily Relevance — Why Plan for Agility?

The history of cryptography is a history of algorithm retirements:
- MD5 (deprecated 2004), SHA-1 (deprecated 2017), RSA-512 (broken 1999)
- Each retirement required emergency migrations for organizations that hard-coded these algorithms

NIST and CISA now **mandate cryptographic agility** as a security requirement for federal systems.

#### Run & Observe
```bash
python src/phase5_decoherence_simulation.py
```

---

## 📊 Expected Lab Results Summary

| Phase | Output File | Key Metric | Security Proof |
|---|---|---|---|
| 1 | `output/keys.json` | 1,184-byte public key | 2^161 post-quantum operations to break |
| 2 | `output/telemetry_payload.json` | 4×4 δgμν tensor + SHA3 hash | Integrity detectable |
| 3 | `output/tunnel_record.json` | 1,088-byte KEM ciphertext | Hybrid encryption verified |
| 4 | (terminal) | Attack simulation | Both attacks FAILED |
| 5 | (terminal) | Algorithm switch log | Agility chain exercised |

---

## 🏆 Assessment Criteria

| Criterion | Points |
|---|---|
| Correctly explains SVP and its role in ML-KEM security | 20 |
| Describes the hybrid encryption pattern and WHY it's used | 15 |
| Explains why the MITM quantum attack failed (2 reasons minimum) | 20 |
| Draws a parallel between decoherence and a real-world cybersecurity concept | 15 |
| Identifies 3 daily cybersecurity scenarios this lab applies to | 15 |
| Correctly defines ephemeral keys and Perfect Forward Secrecy | 15 |
| **Total** | **100** |

---

## 📚 Instructor Notes

### Discussion Topics for Each Phase

**After Phase 1:**
- Draw the lattice on the whiteboard. Show a "good basis" vs "bad basis."
- Ask: Why is 768 dimensions hard even for quantum computers?

**After Phase 3:**
- Draw the TLS 1.3 handshake. Replace ECDHE with ML-KEM.
- Show that the DATA travels via AES, not ML-KEM — WHY? (Performance)

**After Phase 4:**
- Live demonstration: Manually flip a bit in `output/tunnel_record.json`'s ciphertext field, then re-run Phase 3's decryption. The GCM tag rejection should be immediate and visceral.

**After Phase 5:**
- Timeline exercise: When should your organization complete PQC migration?
  - CISA recommendation: Begin inventory 2024, pilot 2025–2026, complete 2030.

### Extending the Lab (Advanced Students)

1. **Add ML-DSA Signatures:** Sign the telemetry payload with ML-DSA-65 before encrypting. Verify the signature at the receiver.
2. **Implement a Real MITM:** Use Python's `socket` library to create an actual network proxy between sender and receiver, then demonstrate the GCM auth tag rejection.
3. **Benchmark Classical vs PQC:** Use `timeit` to compare ML-KEM vs ECDH latency. Calculate the TLS handshake overhead of the transition.

---

*Project Icarus Lab Guide — Icarus Division, Quantum-Safe Systems Group*  
*For educational use only. The physics data is entirely theoretical.*
