#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════╗
║         PROJECT ICARUS — PHASE 5: DECOHERENCE SIMULATION                ║
║         Shared Instability: Quantum Computers & Antigravity Fields       ║
╚══════════════════════════════════════════════════════════════════════════╝

CYBERSECURITY CONCEPT: System Reliability, Resilience & Graceful Degradation
---------------------------------------------------------------------------
Decoherence is the process by which a quantum system loses its quantum
properties (superposition, entanglement) due to interaction with its
environment. It is the #1 engineering challenge in quantum computing.

WHY THIS MATTERS FOR CYBERSECURITY:
  1. QUANTUM THREATS ARE NOT IMMINENT (but plan NOW):
       Practical fault-tolerant quantum computers capable of running Shor's
       algorithm at scale are estimated to be 10–15 years away, precisely
       because decoherence makes large-scale quantum circuits unreliable.
       BUT: "Harvest Now, Decrypt Later" attacks are happening TODAY.

  2. OPERATIONAL RESILIENCE PARALLEL:
       Our theoretical antigravity field has the same vulnerability —
       it requires maintaining a coherent quantum mass-energy state.
       A small thermal perturbation collapses the field, just as noise
       collapses a quantum computation.

  3. CRYPTOGRAPHIC AGILITY:
       If our PQC algorithm is ever broken (due to new mathematical attacks,
       NOT quantum computers), we need a FALLBACK. This phase simulates
       graceful cryptographic degradation.

DAILY RELEVANCE:
  • Incident Response: what happens WHEN (not if) a system fails?
  • Cryptographic agility: NIST recommends hybrid classical+PQC for transition
  • Zero-trust: never assume stability; authenticate continuously
"""

import time
import random
import numpy as np
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.text import Text

console = Console()


class GravityFieldDecoherenceSimulator:
    """
    Models the coherence decay of a theoretical quantum-stabilized antigravity field.
    Maps directly to quantum computing decoherence timescales.
    """

    def __init__(self, initial_coherence: float = 1.0, decay_rate: float = 0.05):
        """
        Args:
            initial_coherence: Normalized coherence [0,1]. 1.0 = fully coherent.
            decay_rate:        Per-tick exponential decay constant.
        """
        self.coherence = initial_coherence
        self.decay_rate = decay_rate
        self.history   = []
        self.tick      = 0

    def step(self, perturbation_noise: float = 0.0) -> float:
        """
        Advance one time step with optional external noise perturbation.

        Real quantum systems use T1 (energy relaxation) and T2 (dephasing)
        timescales. We model a simplified exponential decay + stochastic noise.
        """
        # Exponential decay (T2 dephasing analog)
        self.coherence *= (1 - self.decay_rate)
        # Add stochastic noise (thermal fluctuation / environmental coupling)
        noise = random.gauss(0, perturbation_noise)
        self.coherence = max(0.0, min(1.0, self.coherence + noise))
        self.tick += 1
        self.history.append(round(self.coherence, 4))
        return self.coherence

    def coherence_bar(self) -> str:
        """Return a visual coherence bar."""
        filled = int(self.coherence * 40)
        color  = "green" if self.coherence > 0.6 else ("yellow" if self.coherence > 0.3 else "red")
        bar    = f"[{color}]{'█' * filled}{'░' * (40 - filled)}[/{color}]"
        return bar

    def is_coherent(self, threshold: float = 0.25) -> bool:
        """Is the field/system still coherently operational?"""
        return self.coherence >= threshold


class CryptographicAgility:
    """
    Simulates a fallback mechanism when the primary PQC algorithm becomes unavailable.
    Mirrors real-world implementation of NIST's recommendation for crypto-agility.
    """

    ALGORITHM_CHAIN = [
        {"name": "ML-KEM-768",    "pqc": True,  "nist_level": 3, "status": "PRIMARY"},
        {"name": "ML-KEM-1024",   "pqc": True,  "nist_level": 5, "status": "FALLBACK-1"},
        {"name": "ML-DSA-65+AES", "pqc": True,  "nist_level": 3, "status": "FALLBACK-2"},
        {"name": "X25519+AES256", "pqc": False, "nist_level": None, "status": "EMERGENCY (classical)"},
    ]

    def negotiate_algorithm(self, field_coherence: float) -> dict:
        """
        Select the best available algorithm based on system stability.
        When the field is degenerating, fall back to simpler/more stable options.
        """
        if field_coherence > 0.7:
            return self.ALGORITHM_CHAIN[0]
        elif field_coherence > 0.4:
            return self.ALGORITHM_CHAIN[1]
        elif field_coherence > 0.2:
            return self.ALGORITHM_CHAIN[2]
        else:
            return self.ALGORITHM_CHAIN[3]


def run_decoherence_timeline(steps: int = 30, noise_std: float = 0.02):
    """
    Run the full decoherence simulation timeline with live terminal visualization.
    """
    field = GravityFieldDecoherenceSimulator(initial_coherence=1.0, decay_rate=0.06)
    agility = CryptographicAgility()

    console.print(Panel(
        "[bold]Monitoring antigravity field coherence + cryptographic algorithm selection...[/bold]\n"
        "As the field degrades, the PQC tunnel auto-negotiates to the safest available algorithm.\n\n"
        "[yellow]T1 (relaxation) analog:[/yellow] exponential amplitude decay\n"
        "[yellow]T2 (dephasing) analog:[/yellow] stochastic noise accumulation",
        title="[bold blue]PHASE 5 — Decoherence Timeline[/bold blue]",
        border_style="blue"
    ))

    console.print()
    previous_algo = None
    for step in range(steps):
        coherence  = field.step(perturbation_noise=noise_std)
        algo       = agility.negotiate_algorithm(coherence)
        bar        = field.coherence_bar()
        algo_color = "green" if algo["pqc"] else "red"

        console.print(
            f"  t={step:02d}  {bar}  "
            f"[bold]{coherence:.3f}[/bold]  "
            f"[{algo_color}]{algo['name']}[/{algo_color}]"
            + (" [bold yellow]← ALGORITHM SWITCH[/bold yellow]" if algo["name"] != previous_algo and previous_algo else "")
        )
        previous_algo = algo["name"]
        time.sleep(0.15)

        if coherence < 0.05:
            console.print("\n  [bold red]⚠ FIELD COLLAPSE — tunnel session terminated[/bold red]")
            break

    return field.history


def print_decoherence_cybersecurity_bridge():
    """Bridge the decoherence concept to everyday cybersecurity."""
    table = Table(
        title="Decoherence: Physics ↔ Cybersecurity Parallels",
        border_style="magenta"
    )
    table.add_column("Decoherence Effect",     style="yellow")
    table.add_column("Physics Analog",         style="cyan")
    table.add_column("Cybersecurity Analog",   style="green")
    table.add_column("Mitigation",             style="white")

    rows = [
        ("State Loss",         "Qubit collapses from |ψ⟩ to |0⟩ or |1⟩",
                               "Session key expires / memory wiped",        "Key rotation + ephemeral keys"),
        ("Environmental Noise","Thermal photons disturb qubit",
                               "Side-channel EM leakage, timing attacks",    "Hardware shielding, const-time code"),
        ("Entanglement Break", "Bell state fidelity degrades < 1",
                               "Trust relationship revoked (cert expiry)",   "OCSP / CRL / OSCP stapling"),
        ("Threshold Failure",  "Below T2 coherence threshold → useless",
                               "Below SLA → failover required",              "Cryptographic agility / 2ndary KEM"),
        ("Error Cascade",      "One faulty qubit corrupts register",
                               "One compromised cert → chain of trust fails", "Certificate pinning, CT logs"),
    ]
    for row in rows:
        table.add_row(*row)
    console.print(table)


if __name__ == "__main__":
    console.print("\n[bold white on magenta]  PROJECT ICARUS — PHASE 5  [/bold white on magenta]\n")

    history = run_decoherence_timeline(steps=30, noise_std=0.025)
    console.print()
    print_decoherence_cybersecurity_bridge()

    console.print(Panel(
        "[bold green]KEY TAKEAWAYS FROM PHASE 5:[/bold green]\n\n"
        "1. [yellow]Decoherence limits quantum computers[/yellow] — they cannot sustain\n"
        "   enough coherent qubits long enough to attack ML-KEM-768 today.\n\n"
        "2. [yellow]Cryptographic agility is mandatory[/yellow] — systems MUST be able to\n"
        "   switch algorithms without redesigning the application. Hard-coded\n"
        "   'RSA-2048 forever' is a liability.\n\n"
        "3. [yellow]Ephemeral keys limit damage[/yellow] — even if a session is somehow\n"
        "   broken (by a future quantum computer), all other sessions remain safe.\n\n"
        "4. [yellow]Plan for PQC migration NOW[/yellow] — NIST finalized ML-KEM (FIPS 203),\n"
        "   ML-DSA (FIPS 204), and SLH-DSA (FIPS 205) in August 2024.\n"
        "   Organizations should begin inventory and migration today.",
        title="[bold green]Mission Debrief[/bold green]",
        border_style="green"
    ))

    console.print("\n[bold green]✓ ALL PHASES COMPLETE — PROJECT ICARUS SIMULATION FINISHED[/bold green]\n")
