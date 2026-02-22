#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════╗
║         PROJECT ICARUS — PHASE 3: SECURE TUNNEL ESTABLISHMENT           ║
║         ML-KEM Key Encapsulation + AES-256-GCM Authenticated Encryption ║
╚══════════════════════════════════════════════════════════════════════════╝

CYBERSECURITY CONCEPT: Hybrid Encryption & Secure Channel
---------------------------------------------------------
This phase mirrors exactly what happens when your browser opens a TLS 1.3
connection to a bank's website. It is a TWO-STEP process:

  STEP A — Key Exchange (PQC Asymmetric):
    The sender (generator station) uses the receiver's PUBLIC KEY to
    'encapsulate' a random shared secret. Only the receiver's PRIVATE KEY
    can 'decapsulate' it. This is ML-KEM Key Encapsulation Mechanism (KEM).

  STEP B — Data Encryption (Symmetric):
    The shared secret derived from KEM is fed into HKDF to produce an
    AES-256-GCM session key. The actual payload is then encrypted
    symmetrically — fast, authenticated, and quantum-resistant (Grover's
    attack on AES-256 only halves the effective key space to 128-bits,
    which remains secure).

WHY HYBRID?  Pure asymmetric encryption is slow (~10,000× slower than
             symmetric). We use PQC only to exchange the session key, then
             switch to AES for bulk data. This is exactly how TLS works.

DAILY RELEVANCE:
  • VPN tunnels (IPsec / WireGuard) use exactly this pattern.
  • Signal / WhatsApp use a similar hybrid scheme for message encryption.
  • NIST's PQC standards are already being integrated into OpenSSL 3.x,
    which will transition real TLS deployments starting 2026–2028.
"""

import os
import json
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import oqs

console = Console()


# ─────────────────────────────────────────────────────────────────────────────
# SENDER SIDE (Negative-Mass Generator Station)
# ─────────────────────────────────────────────────────────────────────────────

def sender_encapsulate(public_key_hex: str, algorithm: str = "ML-KEM-768") -> tuple:
    """
    Generator station encapsulates a shared secret using the observation post's
    public key. This produces:
      - ciphertext_kem: sent over the network; useless without private key
      - shared_secret:  kept locally; used to derive the AES session key

    Args:
        public_key_hex: Observation post's public key (hex string).
        algorithm:      ML-KEM variant.

    Returns:
        (ciphertext_kem_hex, shared_secret_bytes)
    """
    public_key_bytes = bytes.fromhex(public_key_hex)

    console.print("\n[bold cyan]SENDER:[/bold cyan] Encapsulating shared secret with receiver's ML-KEM public key...")

    with oqs.KeyEncapsulation(algorithm) as kem:
        ciphertext_kem, shared_secret = kem.encap_secret(public_key_bytes)

    console.print(f"  [green]✓[/green] KEM Ciphertext generated ({len(ciphertext_kem)} bytes) — safe to transmit")
    console.print(f"  [green]✓[/green] Local Shared Secret derived ({len(shared_secret)} bytes) — NEVER transmitted")
    return ciphertext_kem.hex(), shared_secret


def derive_aes_key(shared_secret: bytes, context: bytes = b"icarus-tunnel-v1") -> bytes:
    """
    Derive a 256-bit AES key from the ML-KEM shared secret using HKDF-SHA3-256.

    HKDF (HMAC-based Key Derivation Function) is used because raw ML-KEM output
    may not be uniformly distributed. HKDF extracts and expands it into a
    cryptographically secure key of the desired length.

    Args:
        shared_secret: Raw bytes from ML-KEM encapsulation.
        context:       Domain separator — prevents key reuse across protocols.

    Returns:
        32-byte AES-256 key.
    """
    hkdf = HKDF(
        algorithm=hashes.SHA3_256(),
        length=32,
        salt=None,
        info=context,
    )
    return hkdf.derive(shared_secret)


def encrypt_payload(aes_key: bytes, plaintext: bytes) -> tuple:
    """
    Encrypt the telemetry payload using AES-256-GCM (Authenticated Encryption).

    AES-GCM provides both:
      - CONFIDENTIALITY: data is unreadable without the key
      - INTEGRITY/AUTHENTICATION: any tampering is detected via the auth tag

    Args:
        aes_key:    32-byte AES-256 key.
        plaintext:  Raw bytes of the serialized telemetry payload.

    Returns:
        (nonce_hex, ciphertext_hex, aad)
    """
    nonce = os.urandom(12)  # 96-bit nonce — MUST be unique per encryption
    aad   = b"icarus-telemetry-channel"  # Additional Authenticated Data

    aesgcm    = AESGCM(aes_key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, aad)

    console.print(f"\n[bold cyan]SENDER:[/bold cyan] Encrypting telemetry payload with AES-256-GCM...")
    console.print(f"  [green]✓[/green] Nonce (random, unique): {nonce.hex()}")
    console.print(f"  [green]✓[/green] AAD: '{aad.decode()}' (authenticated but NOT encrypted)")
    console.print(f"  [green]✓[/green] Ciphertext: {len(ciphertext)} bytes (payload + 16-byte GCM auth tag)")

    return nonce.hex(), ciphertext.hex(), aad.decode()


# ─────────────────────────────────────────────────────────────────────────────
# RECEIVER SIDE (Remote Observation Post)
# ─────────────────────────────────────────────────────────────────────────────

def receiver_decapsulate(private_key_hex: str, ciphertext_kem_hex: str,
                          algorithm: str = "ML-KEM-768") -> bytes:
    """
    Observation post decapsulates the shared secret using its private key.

    Args:
        private_key_hex:    The receiver's secret key (hex string).
        ciphertext_kem_hex: The KEM ciphertext received from sender.
        algorithm:          ML-KEM variant.

    Returns:
        shared_secret_bytes — must match sender's shared secret exactly.
    """
    private_key_bytes  = bytes.fromhex(private_key_hex)
    ciphertext_kem_bytes = bytes.fromhex(ciphertext_kem_hex)

    console.print("\n[bold magenta]RECEIVER:[/bold magenta] Decapsulating shared secret with private key...")

    with oqs.KeyEncapsulation(algorithm, secret_key=private_key_bytes) as kem:
        shared_secret = kem.decap_secret(ciphertext_kem_bytes)

    console.print(f"  [green]✓[/green] Shared Secret recovered ({len(shared_secret)} bytes)")
    return shared_secret


def decrypt_payload(aes_key: bytes, nonce_hex: str, ciphertext_hex: str, aad: str) -> bytes:
    """
    Decrypt and authenticate the telemetry payload.

    If the ciphertext or AAD has been tampered with, AESGCM raises
    cryptography.exceptions.InvalidTag — this is how we detect the MITM attack.

    Args:
        aes_key:        32-byte AES-256 key derived from shared secret.
        nonce_hex:      Nonce used during encryption.
        ciphertext_hex: Encrypted payload.
        aad:            Additional authenticated data.

    Returns:
        Decrypted plaintext bytes.
    """
    from cryptography.exceptions import InvalidTag

    nonce      = bytes.fromhex(nonce_hex)
    ciphertext = bytes.fromhex(ciphertext_hex)
    aesgcm     = AESGCM(aes_key)

    console.print("\n[bold magenta]RECEIVER:[/bold magenta] Decrypting and authenticating payload...")

    try:
        plaintext = aesgcm.decrypt(nonce, ciphertext, aad.encode())
        console.print("  [green]✓[/green] GCM Authentication Tag VALID — payload integrity confirmed")
        console.print("  [green]✓[/green] Decryption successful")
        return plaintext
    except InvalidTag:
        console.print("  [red]✗ AUTHENTICATION FAILED — payload has been TAMPERED[/red]")
        console.print("  [red]  → DISCARDING payload. Possible Man-in-the-Middle attack![/red]")
        raise


def display_tunnel_summary(ciphertext_kem_hex: str, nonce_hex: str,
                             ciphertext_hex: str, aad: str):
    """Display what gets transmitted over the (insecure) network vs what stays local."""
    console.print(Panel(
        "[bold]NETWORK TRANSMISSION (visible to adversary):[/bold]\n"
        f"  KEM Ciphertext:    {ciphertext_kem_hex[:48]}... ({len(ciphertext_kem_hex)//2} bytes)\n"
        f"  AES Nonce:         {nonce_hex}\n"
        f"  AES Ciphertext:    [first 48 hex chars shown]...\n"
        f"  AAD (plaintext):   '{aad}'\n\n"
        "[bold green]WHAT ADVERSARY LEARNS FROM THIS:[/bold green] Nothing useful.\n"
        "The KEM ciphertext is quantum-safe — decoding it requires solving SVP\n"
        "on a 768-dimensional lattice (≈ 2^178 operations on best known algorithms).",
        title="[bold blue]Tunnel Packet Analysis[/bold blue]",
        border_style="blue"
    ))


if __name__ == "__main__":
    console.print("\n[bold white on blue]  PROJECT ICARUS — PHASE 3  [/bold white on blue]\n")

    # Load key material from Phase 1
    with open("output/keys.json") as f:
        key_data = json.load(f)

    # Load telemetry payload from Phase 2
    with open("output/telemetry_payload.json") as f:
        payload = json.load(f)

    plaintext = json.dumps(payload).encode()

    # ── SENDER ──────────────────────────────────────────────────────────────
    ciphertext_kem_hex, shared_secret_sender = sender_encapsulate(
        key_data["public_key"], key_data["algorithm"]
    )
    aes_key_sender = derive_aes_key(shared_secret_sender)
    nonce_hex, ciphertext_hex, aad = encrypt_payload(aes_key_sender, plaintext)

    display_tunnel_summary(ciphertext_kem_hex, nonce_hex, ciphertext_hex, aad)

    # ── RECEIVER ─────────────────────────────────────────────────────────────
    shared_secret_receiver = receiver_decapsulate(
        key_data["private_key"], ciphertext_kem_hex, key_data["algorithm"]
    )
    aes_key_receiver = derive_aes_key(shared_secret_receiver)
    plaintext_recovered = decrypt_payload(aes_key_receiver, nonce_hex, ciphertext_hex, aad)

    # Verify secrets match
    assert shared_secret_sender == shared_secret_receiver, "SHARED SECRET MISMATCH!"
    assert json.loads(plaintext_recovered) == payload, "PAYLOAD MISMATCH!"

    console.print("\n[bold green]✓ SECURE TUNNEL ESTABLISHED AND VERIFIED[/bold green]")
    console.print("[bold green]✓ telemetry delivered with CONFIDENTIALITY + INTEGRITY[/bold green]")

    # Save tunnel artifacts
    tunnel_record = {
        "algorithm":         key_data["algorithm"],
        "kem_ciphertext":    ciphertext_kem_hex,
        "aes_nonce":         nonce_hex,
        "aes_ciphertext":    ciphertext_hex,
        "aad":               aad,
    }
    with open("output/tunnel_record.json", "w") as f:
        json.dump(tunnel_record, f, indent=2)

    console.print("[bold green]✓ Tunnel record saved to output/tunnel_record.json[/bold green]")
    console.print("[dim]Ready for Phase 4: Quantum Man-in-the-Middle Attack Simulation[/dim]\n")
