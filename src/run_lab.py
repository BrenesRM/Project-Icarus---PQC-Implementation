#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════╗
║    PROJECT ICARUS — FULL LAB ORCHESTRATOR                                ║
║    Runs all 5 phases sequentially with timing and summary reporting      ║
╚══════════════════════════════════════════════════════════════════════════╝

Usage (uv — recommended):
    uv run icarus                  # run all 5 phases
    uv run icarus --phase 1        # run a single phase

Usage (direct):
    uv run python src/run_lab.py
    uv run python src/run_lab.py --phase 2

Prerequisites:
    uv sync   # installs all dependencies into the managed .venv
"""

import argparse
import json
import os
import sys
import time

# ── Import resolution: support both `uv run icarus` (package) and direct exec ──
# When run as `src.run_lab:main` via the entry point, `src` is on sys.path.
# When run directly as `python src/run_lab.py`, we add src/ manually.
_SRC_DIR = os.path.dirname(os.path.abspath(__file__))
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

# Project root (one level up from src/) — output/ lives here
_ROOT_DIR = os.path.dirname(_SRC_DIR)

from rich.console import Console
from rich.panel   import Panel
from rich.table   import Table
from rich.rule    import Rule

# Phase modules (resolved via sys.path above)
import phase1_key_generation      as p1
import phase2_telemetry_payload   as p2
import phase3_secure_tunnel       as p3
import phase4_quantum_mitm_attack as p4
import phase5_decoherence_simulation as p5

console = Console()

LAB_BANNER = """
██████╗ ██████╗  ██████╗      ██╗███████╗ ██████╗████████╗
██╔══██╗██╔══██╗██╔═══██╗     ██║██╔════╝██╔════╝╚══██╔══╝
██████╔╝██████╔╝██║   ██║     ██║█████╗  ██║        ██║   
██╔═══╝ ██╔══██╗██║   ██║██   ██║██╔══╝  ██║        ██║   
██║     ██║  ██║╚██████╔╝╚█████╔╝███████╗╚██████╗   ██║   
╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚══════╝ ╚═════╝   ╚═╝   
     ██╗ ██████╗ █████╗ ██████╗ ██╗   ██╗███████╗          
     ██║██╔════╝██╔══██╗██╔══██╗██║   ██║██╔════╝          
     ██║██║     ███████║██████╔╝██║   ██║███████╗          
     ██║██║     ██╔══██║██╔══██╗██║   ██║╚════██║          
     ██║╚██████╗██║  ██║██║  ██║╚██████╔╝███████║          
     ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝          
"""


def print_banner():
    console.print(f"[bold cyan]{LAB_BANNER}[/bold cyan]")
    console.print(Panel(
        "[bold white]Securing Gravitational Variance Data via Lattice-Based Cryptography[/bold white]\n\n"
        "[yellow]Classification:[/yellow] [red]TOP SECRET // EDUCATIONAL // PQC-PROTECTED[/red]\n"
        "[yellow]Scenario:[/yellow]        Telemetry link: Negative-Mass Generator → Observation Post\n"
        "[yellow]Threat Model:[/yellow]    Quantum adversary (10,000-qubit processor)\n"
        "[yellow]Defense:[/yellow]         NIST FIPS 203 ML-KEM-768 + AES-256-GCM + SHA3-256",
        title="[bold green]PROJECT ICARUS — LAB SIMULATION[/bold green]",
        border_style="cyan"
    ))


def run_all_phases():
    """Execute all five phases sequentially with timing."""
    out_dir = os.path.join(_ROOT_DIR, "output")
    os.makedirs(out_dir, exist_ok=True)
    timings = {}

    # ── PHASE 1 ──────────────────────────────────────────────────────────────
    console.print(Rule("[bold green]PHASE 1 — Key Generation[/bold green]"))
    t0 = time.time()
    p1.lattice_geometry_explainer()
    key_data = p1.generate_mlkem_keypair("ML-KEM-768")
    with open(os.path.join(out_dir, "keys.json"), "w") as f:
        json.dump(key_data, f, indent=2)
    timings["Phase 1"] = time.time() - t0

    # ── PHASE 2 ──────────────────────────────────────────────────────────────
    console.print(Rule("[bold green]PHASE 2 — Telemetry Payload[/bold green]"))
    t0 = time.time()
    payload = p2.build_telemetry_payload()
    p2.display_payload_summary(payload)
    with open(os.path.join(out_dir, "telemetry_payload.json"), "w") as f:
        json.dump(payload, f, indent=2)
    timings["Phase 2"] = time.time() - t0

    # ── PHASE 3 ──────────────────────────────────────────────────────────────
    console.print(Rule("[bold green]PHASE 3 — Secure Tunnel[/bold green]"))
    t0 = time.time()
    plaintext = json.dumps(payload).encode()
    kem_ct_hex, ss_sender = p3.sender_encapsulate(key_data["public_key"], key_data["algorithm"])
    aes_key_s             = p3.derive_aes_key(ss_sender)
    nonce_hex, ct_hex, aad = p3.encrypt_payload(aes_key_s, plaintext)
    p3.display_tunnel_summary(kem_ct_hex, nonce_hex, ct_hex, aad)
    ss_receiver           = p3.receiver_decapsulate(key_data["private_key"], kem_ct_hex, key_data["algorithm"])
    aes_key_r             = p3.derive_aes_key(ss_receiver)
    p3.decrypt_payload(aes_key_r, nonce_hex, ct_hex, aad)
    console.print("[bold green]✓ Secure tunnel verified[/bold green]")
    tunnel_record = {"algorithm": key_data["algorithm"], "kem_ciphertext": kem_ct_hex,
                     "aes_nonce": nonce_hex, "aes_ciphertext": ct_hex, "aad": aad}
    with open(os.path.join(out_dir, "tunnel_record.json"), "w") as f:
        json.dump(tunnel_record, f, indent=2)
    timings["Phase 3"] = time.time() - t0

    # ── PHASE 4 ──────────────────────────────────────────────────────────────
    console.print(Rule("[bold red]PHASE 4 — Quantum MITM Attack[/bold red]"))
    t0 = time.time()
    specter = p4.QuantumSpecterAdversary()
    specter.intercept_packet(kem_ct_hex, nonce_hex, ct_hex, aad)
    specter.attempt_lattice_attack()
    tampered = specter.attempt_payload_tampering(ct_hex, nonce_hex, aad)
    p4.simulate_tampered_decryption(aes_key_r, nonce_hex, tampered, aad)
    p4.print_mitm_comparison_table()
    timings["Phase 4"] = time.time() - t0

    # ── PHASE 5 ──────────────────────────────────────────────────────────────
    console.print(Rule("[bold magenta]PHASE 5 — Decoherence Simulation[/bold magenta]"))
    t0 = time.time()
    p5.run_decoherence_timeline(steps=25, noise_std=0.025)
    p5.print_decoherence_cybersecurity_bridge()
    timings["Phase 5"] = time.time() - t0

    # ── SUMMARY ──────────────────────────────────────────────────────────────
    console.print(Rule("[bold white]LAB COMPLETE[/bold white]"))
    summary_table = Table(title="Phase Execution Summary", border_style="green")
    summary_table.add_column("Phase",      style="bold white")
    summary_table.add_column("Concept",    style="cyan")
    summary_table.add_column("Result",     style="green")
    summary_table.add_column("Time (s)",   style="yellow")
    rows = [
        ("Phase 1",  "ML-KEM-768 Key Generation",          "✓ Key pair generated",         f"{timings['Phase 1']:.2f}"),
        ("Phase 2",  "Metric Tensor δgμν Payload",         "✓ Telemetry built + hashed",    f"{timings['Phase 2']:.2f}"),
        ("Phase 3",  "Hybrid KEM + AES-256-GCM Tunnel",    "✓ Data delivered securely",     f"{timings['Phase 3']:.2f}"),
        ("Phase 4",  "Quantum MITM Attack",                "✓ All attacks REPELLED",        f"{timings['Phase 4']:.2f}"),
        ("Phase 5",  "Decoherence + Crypto Agility",       "✓ Fallback chain simulated",    f"{timings['Phase 5']:.2f}"),
    ]
    for row in rows:
        summary_table.add_row(*row)
    console.print(summary_table)

    console.print(Panel(
        "[bold green]PROJECT ICARUS — MISSION ACCOMPLISHED[/bold green]\n\n"
        "The gravitational variance telemetry was:\n"
        "  ✓ Encrypted with quantum-safe ML-KEM-768\n"
        "  ✓ Authenticated with AES-256-GCM\n"
        "  ✓ Integrity-verified with SHA-3-256\n"
        "  ✓ Protected with ephemeral keys (Perfect Forward Secrecy)\n"
        "  ✓ Resistant to a 10,000-qubit adversary\n\n"
        "[dim]Output artifacts saved to ./output/ directory[/dim]",
        border_style="green"
    ))


def main():
    parser = argparse.ArgumentParser(description="Project Icarus PQC Lab Orchestrator")
    parser.add_argument("--phase", type=int, choices=[1, 2, 3, 4, 5],
                        help="Run only this phase (1-5)")
    args = parser.parse_args()

    print_banner()
    time.sleep(1)

    if args.phase is None:
        run_all_phases()
    else:
        console.print(f"\n[yellow]Running Phase {args.phase} only...[/yellow]\n")
        # Single-phase dispatch
        os.makedirs("output", exist_ok=True)
        if args.phase == 1:
            p1.lattice_geometry_explainer()
            kd = p1.generate_mlkem_keypair()
            out_dir = os.path.join(_ROOT_DIR, "output")
            os.makedirs(out_dir, exist_ok=True)
            with open(os.path.join(out_dir, "keys.json"), "w") as f:
                json.dump(kd, f, indent=2)
        elif args.phase == 2:
            pl = p2.build_telemetry_payload()
            p2.display_payload_summary(pl)
            out_dir = os.path.join(_ROOT_DIR, "output")
            os.makedirs(out_dir, exist_ok=True)
            with open(os.path.join(out_dir, "telemetry_payload.json"), "w") as f:
                json.dump(pl, f, indent=2)
        elif args.phase in (3, 4, 5):
            console.print("[yellow]Phases 3-5 require output from Phases 1-2.[/yellow]")
            console.print("Hint: [bold]uv run icarus[/bold]  (runs all phases)")


if __name__ == "__main__":
    main()
