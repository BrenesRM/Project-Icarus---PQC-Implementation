#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════╗
║         PROJECT ICARUS — PHASE 4: QUANTUM MAN-IN-THE-MIDDLE ATTACK      ║
║         10,000-Qubit Adversary vs ML-KEM-768                            ║
╚══════════════════════════════════════════════════════════════════════════╝

CYBERSECURITY CONCEPT: Man-in-the-Middle (MITM) Attacks
-------------------------------------------------------
A MITM attack occurs when an adversary secretly intercepts and potentially
alters communications between two parties who believe they are talking directly
to each other.

CLASSICAL MITM:
  An attacker intercepts a Diffie-Hellman key exchange and substitutes their
  own public key. They talk to Alice pretending to be Bob, and vice versa.
  Both sides think they have a secure channel — but the attacker sees all.

THE QUANTUM UPGRADE:
  Our adversary ("Quantum Specter") operates a 10,000-qubit processor.
  Against classical RSA/ECC, they would:
    1. Run Shor's Algorithm to factor the public key modulus in polynomial time.
    2. Derive the private key.
    3. Impersonate the receiver.

WHY ML-KEM RESISTS THIS:
  ML-KEM security is based on MLWE — Module Learning With Errors.
  The best known quantum attack on MLWE is a combination of:
    - Grover's Algorithm:  provides √ speedup on exhaustive search
    - Lattice sieving:     best known classical method to find short vectors

  For ML-KEM-768, the estimated post-quantum security level is:
      ≈ 2^161 quantum operations to break (NIST Category 3)

  Even a 10,000-qubit machine would need:
    - All qubits to be LOGICAL (error-corrected), requiring ~1000 physical
      qubits per logical qubit → 10M+ physical qubits needed for real attacks.
    - Decoherence: current quantum processors lose state in microseconds;
      a lattice attack would take years of sustained computation.

DAILY RELEVANCE:
  The MITM scenario maps to real-world threats:
    • ARP poisoning on a LAN
    • BGP route hijacking between ISPs
    • SSL stripping attacks on HTTP→HTTPS redirects
    • Evil-twin Wi-Fi access points
  PQC makes stolen key material useless even against future quantum computers.
"""

import json
import time
import random
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

console = Console()


# ─────────────────────────────────────────────────────────────────────────────
# ADVERSARY MODEL
# ─────────────────────────────────────────────────────────────────────────────

class QuantumSpecterAdversary:
    """
    Simulates a well-resourced quantum adversary ('Quantum Specter').

    This class models what a 10,000-qubit adversary CAN and CANNOT do
    against ML-KEM-768 protected transmissions.
    """

    QUBIT_COUNT     = 10_000
    COHERENCE_TIME_US = 87      # microseconds — real-world SOTA ~100–1000 µs
    LATTICE_DIMENSION = 768     # ML-KEM-768 lattice dimension (mod q)
    MODULUS_Q       = 3329      # ML-KEM prime modulus

    def __init__(self):
        self.intercept_log = []
        console.print(Panel(
            f"[bold red]QUANTUM SPECTER ONLINE[/bold red]\n\n"
            f"Qubit Count:       [yellow]{self.QUBIT_COUNT:,}[/yellow] physical qubits\n"
            f"Coherence Time:    [yellow]{self.COHERENCE_TIME_US} µs[/yellow] (thermal decoherence limit)\n"
            f"Target:            ML-KEM-768 KEM Ciphertext\n"
            f"Objective:         Recover gravity-nullification coordinates\n"
            f"Attack Strategy:   Shor-family lattice reduction + Grover oracle",
            title="[bold red]⚠ ADVERSARY INITIALIZED[/bold red]",
            border_style="red"
        ))

    def intercept_packet(self, kem_ciphertext_hex: str, aes_nonce_hex: str,
                          aes_ciphertext_hex: str, aad: str) -> dict:
        """Intercept the full tunnel packet."""
        console.print("\n[red]QUANTUM SPECTER:[/red] Intercepting tunnel packet...")
        packet = {
            "kem_ciphertext": kem_ciphertext_hex,
            "aes_nonce":      aes_nonce_hex,
            "aes_ciphertext": aes_ciphertext_hex,
            "aad":            aad,
            "intercept_time": time.time(),
        }
        self.intercept_log.append(packet)
        console.print(f"  [red]✓[/red] Packet captured: {len(kem_ciphertext_hex)//2 + len(aes_ciphertext_hex)//2} bytes total")
        return packet

    def attempt_lattice_attack(self) -> bool:
        """
        Simulate the quantum adversary's lattice attack against ML-KEM-768.

        In reality, breaking ML-KEM-768 requires solving MLWE in a 768-dimensional
        module lattice over Zq (q=3329). The adversary would use:
          1. BKZ (Block Korkine-Zolotarev) lattice sieving
          2. Quantum speedup via Grover's search

        We simulate the computation with realistic estimates of time-to-solution.
        """
        console.print("\n[bold red]QUANTUM SPECTER:[/bold red] Initiating lattice basis reduction attack...\n")
        console.print(
            f"  Target: MLWE instance, dimension n={self.LATTICE_DIMENSION}, q={self.MODULUS_Q}\n"
            f"  Method: Quantum-enhanced BKZ-β sieving\n"
        )

        steps = [
            ("Generating lattice basis from KEM ciphertext",    1.2, False),
            ("Running BKZ-β (β=40) preprocessing",              2.1, False),
            ("Applying Grover oracle for short-vector search",   2.8, False),
            ("Quantum coherence maintained...",                  0.8, False),
            ("Hit coherence time limit — qubit state COLLAPSED", 1.0, True),
            ("Re-initializing quantum register...",              0.7, True),
            ("Second attempt: BKZ-β (β=60)",                    1.5, True),
            ("Coherence LOST again — decoherence threshold",     0.6, True),
            ("Estimated completion time: 2^161 operations remaining", 0.5, True),
            ("ATTACK FAILED — insufficient error correction overhead", 0.5, True),
        ]

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("[red]Quantum Attack Progress", total=len(steps))
            for description, delay, is_failure in steps:
                color = "red" if is_failure else "yellow"
                progress.update(task, description=f"[{color}]{description}[/{color}]", advance=1)
                time.sleep(delay)

        console.print(Panel(
            "[bold red]ATTACK RESULT: FAILED[/bold red]\n\n"
            "The adversary could NOT recover the ML-KEM private key or shared secret.\n\n"
            "[bold]Root Causes of Failure:[/bold]\n"
            "  1. [yellow]Decoherence:[/yellow] Quantum state collapsed after ~87µs — far too short\n"
            "     to complete BKZ lattice sieving (would require years of coherent runtime).\n\n"
            "  2. [yellow]Qubit Overhead:[/yellow] 10,000 physical qubits → ~10 logical qubits\n"
            "     (error correction reduces effective count by ~1000×). Need ~1M logical\n"
            "     qubits for meaningful lattice attacks at this dimension.\n\n"
            "  3. [yellow]SVP Hardness:[/yellow] Even with ideal hardware, ML-KEM-768 provides\n"
            "     ≈ 2^161 post-quantum security. At 10^15 ops/sec, that's 10^33 years.\n\n"
            "  4. [yellow]Ephemeral Keys:[/yellow] Even if PAST sessions were somehow broken,\n"
            "     each session uses a freshly generated key pair — no key reuse to exploit.",
            title="[bold red]🛡 ML-KEM DEFENSE HOLDS[/bold red]",
            border_style="green"
        ))
        return False  # Attack failed

    def attempt_payload_tampering(self, aes_ciphertext_hex: str, aes_nonce_hex: str,
                                   aad: str) -> str:
        """
        Even without breaking the KEM, the adversary tries to tamper with
        the ciphertext (a bit-flip attack) to corrupt coordinates.

        AES-256-GCM detects this via its authentication tag.
        """
        console.print("\n[bold red]QUANTUM SPECTER:[/bold red] Attempting ciphertext bit-flip attack...")
        ciphertext_bytes = bytearray(bytes.fromhex(aes_ciphertext_hex))
        # Flip a random bit in the ciphertext
        idx = random.randint(0, len(ciphertext_bytes) - 17)  # avoid the 16-byte GCM tag
        bit = random.randint(0, 7)
        ciphertext_bytes[idx] ^= (1 << bit)
        console.print(f"  [red]✓[/red] Flipped bit {bit} of byte {idx} — crafting modified ciphertext...")
        return bytes(ciphertext_bytes).hex()


def simulate_tampered_decryption(aes_key: bytes, nonce_hex: str,
                                  tampered_ciphertext_hex: str, aad: str):
    """Attempt to decrypt a tampered ciphertext — will raise InvalidTag."""
    try:
        nonce      = bytes.fromhex(nonce_hex)
        ciphertext = bytes.fromhex(tampered_ciphertext_hex)
        aesgcm     = AESGCM(aes_key)
        aesgcm.decrypt(nonce, ciphertext, aad.encode())
        console.print("  [yellow]⚠ Decryption succeeded (unexpected)[/yellow]")
    except InvalidTag:
        console.print(Panel(
            "[bold green]GCM AUTHENTICATION FAILED — AS EXPECTED[/bold green]\n\n"
            "The receiver's AES-256-GCM verification detected the bit-flip.\n"
            "The modified ciphertext produces an invalid authentication tag.\n\n"
            "Result: Payload DISCARDED. Receiver alerted to potential tampering.\n\n"
            "[bold]This is the 'I' (Integrity) in the CIA Triad working in real time.\n"
            "Even without knowing the key, the adversary cannot modify ciphertext\n"
            "without our knowing — AES-GCM is an Authenticated Encryption scheme.[/bold]",
            title="[bold green]🛡 AES-GCM Integrity Protected[/bold green]",
            border_style="green"
        ))


def print_mitm_comparison_table():
    """Print classical vs quantum MITM comparison for educational purposes."""
    table = Table(
        title="Classical vs Quantum MITM — What Changes with PQC?",
        border_style="cyan"
    )
    table.add_column("Property",           style="bold white",  no_wrap=True)
    table.add_column("Classical MITM",     style="red")
    table.add_column("Quantum MITM (now)", style="yellow")
    table.add_column("PQC Defense",        style="green")

    rows = [
        ("Key Exchange Target",   "RSA/ECC public key",       "RSA/ECC public key",     "ML-KEM (lattice-based)"),
        ("Attack Algorithm",       "Baby-step Giant-step",     "Shor's Algorithm",       "No efficient quantum alg."),
        ("Complexity",             "2^128 classical",          "Polynomial (Shor)",      "2^161 post-quantum"),
        ("Ciphertext Tampering",   "Detectable via MAC",       "Detectable via GCM",     "AES-256-GCM auth tag"),
        ("Ephemeral Keys Help?",   "Yes (PFS)",                "Yes (limits blast rad.)", "Yes (PFS + PQC)"),
        ("Decoherence Risk",       "N/A",                      "Critical blocker",        "Not attacker's problem"),
        ("Real-World Status",      "Actively exploited",       "Theoretical (2026)",     "NIST standard as of 2024"),
    ]
    for row in rows:
        table.add_row(*row)
    console.print(table)


if __name__ == "__main__":
    console.print("\n[bold white on red]  PROJECT ICARUS — PHASE 4: QUANTUM MITM ATTACK  [/bold white on red]\n")

    # Load tunnel record
    with open("output/tunnel_record.json") as f:
        tunnel = json.load(f)

    # Load keys for tampered decryption demonstration
    with open("output/keys.json") as f:
        key_data = json.load(f)

    # Reconstruct AES key (in a real MITM the attacker does NOT have this)
    from phase3_secure_tunnel import receiver_decapsulate, derive_aes_key
    shared_secret = receiver_decapsulate(key_data["private_key"], tunnel["kem_ciphertext"], key_data["algorithm"])
    aes_key       = derive_aes_key(shared_secret)

    # ── ADVERSARY ACTIVATES ───────────────────────────────────────────────
    specter = QuantumSpecterAdversary()
    packet  = specter.intercept_packet(
        tunnel["kem_ciphertext"], tunnel["aes_nonce"], tunnel["aes_ciphertext"], tunnel["aad"]
    )

    # ── ATTACK 1: Lattice Attack (attempt to recover private key) ─────────
    specter.attempt_lattice_attack()

    # ── ATTACK 2: Bit-Flip / Tampering Attack ─────────────────────────────
    tampered = specter.attempt_payload_tampering(
        tunnel["aes_ciphertext"], tunnel["aes_nonce"], tunnel["aad"]
    )
    simulate_tampered_decryption(aes_key, tunnel["aes_nonce"], tampered, tunnel["aad"])

    # ── COMPARISON TABLE ─────────────────────────────────────────────────
    print_mitm_comparison_table()

    console.print("\n[bold green]✓ Phase 4 complete — all attacks repelled[/bold green]")
    console.print("[dim]Ready for Phase 5: Decoherence Simulation[/dim]\n")
