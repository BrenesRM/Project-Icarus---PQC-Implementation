#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════╗
║         PROJECT ICARUS — PHASE 2: TELEMETRY PAYLOAD                     ║
║         Metric Perturbation Tensor δgμν (Physics Data Simulation)       ║
╚══════════════════════════════════════════════════════════════════════════╝

CYBERSECURITY CONCEPT: Data Integrity & Payload Classification
-------------------------------------------------------------
Before encrypting, we must clearly define WHAT we are protecting and WHY.
In real-world security, data classification drives the selection of:
  - Appropriate encryption strength
  - Integrity verification mechanisms (MACs/signatures)
  - Transmission policies and access controls

The sensitivity of the data justifies our PQC investment:
  If gravitational variance coordinates were intercepted, a hostile actor
  could reverse-engineer the nullification field geometry — catastrophic.

PHYSICS CONTEXT (for educational flavor):
  In General Relativity, spacetime curvature is described by the
  metric tensor gμν (a 4×4 symmetric matrix).

  A local perturbation δgμν represents a small deviation from flat space:
      g_perturbed(μ,ν) = η(μ,ν) + δg(μ,ν)

  where η is the Minkowski metric (flat spacetime reference).

  Our theoretical negative-mass generator creates a localized region where
  the effective gravitational constant G is reduced:
      G_local = G₀ · (1 - ε),  ε ∈ (0,1)

  This manifests as a specific signature in δgμν — the payload we transmit.
"""

import numpy as np
import json
import time
import hashlib
from typing import Tuple
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# ─────────────────────────────────────────────────────────────
# Physical Constants (SI units, theoretical model)
# ─────────────────────────────────────────────────────────────
G_NEWTON       = 6.674e-11   # m³ kg⁻¹ s⁻²  (nominal Newton's G)
C_LIGHT        = 2.998e8     # m/s
REDUCTION_EPS  = 0.073       # 7.3% local reduction in G (simulated)


def minkowski_metric() -> np.ndarray:
    """
    Returns the flat-space Minkowski metric tensor η_μν.
    Signature: (−, +, +, +)  — physics convention.
    """
    return np.diag([-1.0, 1.0, 1.0, 1.0])


def delta_g_perturbation(
    epsilon: float = REDUCTION_EPS,
    seed: int = 42
) -> np.ndarray:
    """
    Compute the metric perturbation tensor δgμν for a localized G-reduction event.

    The perturbation is symmetric (δgμν = δgνμ) and traceless in the spatial block,
    consistent with a weak-field approximation.

    Args:
        epsilon: Fractional reduction in G (0 → no effect, 1 → G = 0).
        seed:    Random seed for repeatable simulated noise.

    Returns:
        4×4 numpy array representing δgμν.
    """
    rng = np.random.default_rng(seed)

    # Base perturbation: purely gravitational (time-time component dominant)
    delta_g = np.zeros((4, 4))

    # g_tt perturbation encodes the G-reduction:
    #   In the Newtonian limit: g_tt ≈ -(1 + 2Φ/c²), Φ = -GM/r
    #   A reduced G means a weaker Φ, hence a smaller negative g_tt perturbation
    delta_g[0, 0] = -epsilon * 2.0 * G_NEWTON / C_LIGHT**2 * 1e12  # scaled for readability

    # Spatial off-diagonal components: frame-dragging signature of the generator
    for i in range(1, 4):
        for j in range(1, 4):
            if i == j:
                delta_g[i, j] = epsilon * rng.uniform(0.01, 0.05)
            else:
                delta_g[i, j] = delta_g[j, i] = epsilon * rng.uniform(-0.01, 0.01)

    return delta_g


def build_telemetry_payload(
    station_id: str = "ICARUS-GEN-ALPHA",
    coordinates: Tuple[float, float, float] = (-10.234, 84.571, 3820.0),
    timestamp: float = None,
) -> dict:
    """
    Build the complete telemetry payload to be transmitted securely.

    Args:
        station_id:   Identifier of the negative-mass generator station.
        coordinates:  (lat, lon, altitude_m) of the nullification field center.
        timestamp:    Unix epoch of the measurement (defaults to now).

    Returns:
        Serializable dictionary with all telemetry fields + integrity hash.
    """
    if timestamp is None:
        timestamp = time.time()

    eta   = minkowski_metric()
    delta = delta_g_perturbation(epsilon=REDUCTION_EPS)
    g_perturbed = eta + delta

    payload = {
        "station_id":       station_id,
        "timestamp_utc":    timestamp,
        "classification":   "TOP SECRET // PQC-PROTECTED // ICARUS",
        "coordinates": {
            "latitude":  coordinates[0],
            "longitude": coordinates[1],
            "altitude_m": coordinates[2],
            "note": "Nullification field center — primary exfiltration target for adversaries"
        },
        "physics": {
            "G_nominal":         G_NEWTON,
            "G_local":           G_NEWTON * (1 - REDUCTION_EPS),
            "reduction_epsilon": REDUCTION_EPS,
            "minkowski_eta":     eta.tolist(),
            "delta_g_perturb":   delta.tolist(),
            "g_perturbed":       g_perturbed.tolist(),
            "tensor_note": (
                "δgμν represents the local spacetime curvature deviation. "
                "Spatial index 0=t,1=x,2=y,3=z. Off-diagonal terms indicate "
                "frame-dragging from rotational mass asymmetry."
            ),
        },
        "system_health": {
            "decoherence_rate_pct": 12.4,
            "field_stability":      "MARGINAL",
            "decoherence_note": (
                "Decoherence is a critical shared challenge: quantum computers "
                "lose quantum state due to environmental interaction. Similarly, "
                "our theoretical antigravity field is highly unstable — small "
                "thermal fluctuations collapse the coherent mass-energy state. "
                "This is why data must be transmitted quickly and securely."
            ),
        },
    }

    # Compute SHA-3-256 integrity fingerprint of the physics data
    raw = json.dumps(payload["physics"], sort_keys=True).encode()
    payload["integrity_hash_sha3_256"] = hashlib.sha3_256(raw).hexdigest()

    return payload


def display_payload_summary(payload: dict):
    """Print a formatted summary of the telemetry payload."""
    console.print(Panel(
        "[bold]Gravitational Variance Telemetry Snapshot[/bold]\n\n"
        f"Station: [cyan]{payload['station_id']}[/cyan]\n"
        f"Classification: [red]{payload['classification']}[/red]\n"
        f"Field Stability: [yellow]{payload['system_health']['field_stability']}[/yellow]\n"
        f"Decoherence Rate: [yellow]{payload['system_health']['decoherence_rate_pct']}%[/yellow]",
        title="[bold green]PHASE 2 — Telemetry Payload[/bold green]",
        border_style="green"
    ))

    # Tensor display
    table = Table(title="Metric Perturbation Tensor δgμν (4×4)", border_style="blue")
    labels = ["t", "x", "y", "z"]
    table.add_column("μ\\ν", style="bold cyan")
    for label in labels:
        table.add_column(label, style="yellow")

    delta = np.array(payload["physics"]["delta_g_perturb"])
    for i, row_label in enumerate(labels):
        table.add_row(row_label, *[f"{delta[i,j]:.6e}" for j in range(4)])

    console.print(table)

    g_vals = payload["physics"]
    console.print(
        f"\n[bold]G Reduction:[/bold] "
        f"G₀ = {g_vals['G_nominal']:.4e} → "
        f"G_local = {g_vals['G_local']:.4e} m³·kg⁻¹·s⁻² "
        f"([red]↓{REDUCTION_EPS*100:.1f}%[/red])\n"
    )
    console.print(
        f"[dim]SHA-3-256 Integrity Hash: {payload['integrity_hash_sha3_256']}[/dim]\n"
    )

    console.print(Panel(
        "[bold yellow]⚠ WHY DOES THIS MATTER IN DAILY CYBERSECURITY?[/bold yellow]\n\n"
        "The coordinates in this payload are the #1 adversary target.\n"
        "In real-world terms, this maps to:\n"
        "  • API keys / credentials in transit\n"
        "  • SCADA sensor readings in industrial control systems\n"
        "  • Medical imaging data in healthcare telemetry\n"
        "  • Financial transactions between clearing houses\n\n"
        "The CLASSIFICATION header mirrors real Data Loss Prevention (DLP) policies.\n"
        "The SHA-3 hash ensures payload INTEGRITY — any bit-flip during transit\n"
        "is detectable. This is the 'I' in the CIA Triad.",
        border_style="yellow"
    ))


if __name__ == "__main__":
    console.print("\n[bold white on blue]  PROJECT ICARUS — PHASE 2  [/bold white on blue]\n")
    payload = build_telemetry_payload()
    display_payload_summary(payload)

    import os
    os.makedirs("output", exist_ok=True)
    with open("output/telemetry_payload.json", "w") as f:
        json.dump(payload, f, indent=2)

    console.print("[bold green]✓ Telemetry payload saved to output/telemetry_payload.json[/bold green]")
    console.print("[dim]Ready for Phase 3: Secure Tunnel Establishment[/dim]\n")
