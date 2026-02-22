#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════╗
║         PROJECT ICARUS — PHASE 1: KEY GENERATION                        ║
║         ML-KEM Lattice-Based Asymmetric Key Pair                        ║
╚══════════════════════════════════════════════════════════════════════════╝

CYBERSECURITY CONCEPT: Asymmetric Key Generation (PQC Edition)
--------------------------------------------------------------
In classical PKI, RSA or ECC key pairs protect data in transit.
A quantum computer running Shor's Algorithm can break RSA-2048 in hours.

ML-KEM (formerly Kyber) is the NIST-standardized replacement.
Its security comes from the Module Learning With Errors (MLWE) problem —
a generalization of the Shortest Vector Problem (SVP) on a lattice.

LATTICE PRIMER:
  A lattice L is the set of all integer linear combinations of basis vectors:
      L = { Σ aᵢvᵢ | aᵢ ∈ ℤ }

  Given a lattice with a "bad" (nearly orthogonal) basis,
  finding the SHORTEST vector in L is believed to be hard even for quantum
  computers. ML-KEM encodes the private key as a trapdoor into this geometry.

DAILY RELEVANCE:
  Every time you visit https:// a website, TLS 1.3 performs a key exchange.
  In a Post-Quantum world, ML-KEM replaces ECDH in that handshake.
  Organizations must audit and migrate TODAY because "Harvest Now, Decrypt Later"
  attacks are real — adversaries record encrypted traffic now to decrypt once
  quantum computers mature.
"""

import os
import json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import oqs  # liboqs-python bindings

console = Console()


def generate_mlkem_keypair(security_level: str = "ML-KEM-768") -> dict:
    """
    Generate an ML-KEM key pair for the observation post (server).

    ML-KEM security levels:
      ML-KEM-512  → NIST Security Level 1 (AES-128 equivalent)
      ML-KEM-768  → NIST Security Level 3 (AES-192 equivalent) ← recommended
      ML-KEM-1024 → NIST Security Level 5 (AES-256 equivalent)

    Args:
        security_level: The ML-KEM parameter set to use.

    Returns:
        A dict containing the public key, private key, and metadata.
    """
    console.print(Panel(
        f"[bold cyan]Initializing ML-KEM Key Pair Generation[/bold cyan]\n"
        f"Algorithm: [yellow]{security_level}[/yellow]\n"
        f"Security Level: NIST Level 3 (≈ AES-192 classical equivalent)\n"
        f"Quantum Threat Model: Resistant to Grover + Shor algorithms",
        title="[bold green]PHASE 1 — Key Generation[/bold green]",
        border_style="green"
    ))

    with oqs.KeyEncapsulation(security_level) as kem:
        # Generate the public/private key pair
        public_key = kem.generate_keypair()
        private_key = kem.export_secret_key()

        key_data = {
            "algorithm": security_level,
            "public_key": public_key.hex(),    # Shared with sender (generator station)
            "private_key": private_key.hex(),  # Kept secret at observation post
            "public_key_bytes": len(public_key),
            "private_key_bytes": len(private_key),
            "nist_level": 3,
        }

    # Display key statistics
    table = Table(title="ML-KEM Key Metrics", border_style="cyan")
    table.add_column("Property", style="bold white")
    table.add_column("Value", style="yellow")
    table.add_row("Algorithm", key_data["algorithm"])
    table.add_row("Public Key Size", f"{key_data['public_key_bytes']} bytes ({key_data['public_key_bytes'] * 8} bits)")
    table.add_row("Private Key Size", f"{key_data['private_key_bytes']} bytes")
    table.add_row("SVP Hardness (estimated)", "≥ 2^178 classical operations")
    table.add_row("Quantum Resistance", "✓ Grover's speedup limited to √ search space")
    table.add_row("Key Type", "EPHEMERAL (generated fresh per session)")
    console.print(table)

    console.print(
        "\n[bold magenta]⚡ Ephemeral Key Note:[/bold magenta] "
        "This key pair is generated fresh for EVERY tunnel session. "
        "If one session is ever compromised, past and future sessions remain secure. "
        "This property is called [bold]Perfect Forward Secrecy (PFS)[/bold].\n"
    )

    return key_data


def lattice_geometry_explainer():
    """Print a visual explanation of the lattice structure underpinning ML-KEM."""
    console.print(Panel(
        "[bold]How the Lattice Protects Our Keys:[/bold]\n\n"
        "Imagine a 2D grid of points (scale this to 1024+ dimensions for ML-KEM):\n\n"
        "    ·  ·  ·  ·  ✦  ·  ·  ·\n"
        "    ·  ·  ·  ·  ·  ·  ·  ·\n"
        "    ·  ·  [SK]·  ·  ·  ·  ·    ← Private key = short vector to origin\n"
        "    ·  ·  ·  ·  ·  ·  ·  ·\n"
        "    ·  ·  ·  ·  ·  ·  ·  ·\n\n"
        "The PUBLIC KEY is a 'bad basis' representation of the same lattice.\n"
        "Computing the SHORT VECTOR from the bad basis (SVP) requires\n"
        "exponential time even on quantum hardware.\n\n"
        "[yellow]L = { Σ aᵢvᵢ | aᵢ ∈ ℤ }[/yellow]\n\n"
        "The private key IS the trapdoor — the good basis that makes SVP easy.",
        title="[bold blue]🔷 Lattice Geometry Primer[/bold blue]",
        border_style="blue"
    ))


if __name__ == "__main__":
    console.print("\n[bold white on blue]  PROJECT ICARUS — PHASE 1  [/bold white on blue]\n")
    lattice_geometry_explainer()
    key_data = generate_mlkem_keypair("ML-KEM-768")

    # Persist keys for use in subsequent phases
    os.makedirs("output", exist_ok=True)
    with open("output/keys.json", "w") as f:
        json.dump(key_data, f, indent=2)

    console.print("[bold green]✓ Keys saved to output/keys.json[/bold green]")
    console.print("[dim]Ready for Phase 2: Telemetry Payload Generation[/dim]\n")
