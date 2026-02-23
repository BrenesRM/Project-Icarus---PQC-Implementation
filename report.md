# Project Icarus: Analysis & Lab Execution Findings Report

## 1. Project Analysis
**Project Icarus** is an educational and proof-of-concept cybersecurity project that simulates a "Quantum-Safe Gravitational Variance Telemetry System". 
Its main goal is to demonstrate the principles and implementation of Post-Quantum Cryptography (PQC) to defend against "Harvest Now, Decrypt Later" (HNDL) threats posed by future Cryptographically Relevant Quantum Computers (CRQC).

### Architectural Concepts Covered:
- **Asymmetric Encryption (Key Exchange)**: Uses Lattice-Based cryptography specifically **ML-KEM-768** (FIPS 203) for key encapsulation.
- **Symmetric Encryption**: Uses **AES-256-GCM** to secure the actual telemetry data in the established tunnel, satisfying post-quantum resistance via increased bit lengths (resisting Grover's Algorithm).
- **Integrity**: Employs **SHA-3-256** for payload hashing, avoiding length-extension attacks.
- **Key Derivation**: Implements **HKDF** to stretch the ML-KEM shared secret into a 256-bit AES session key.
- **Crypto-Agility & Perfect Forward Secrecy**: The lab simulates utilizing ephemeral keys for connections and having fallback cryptography modules dynamically adapt to simulated quantum decoherence constraints.

---

## 2. Lab Execution & Test Results

The lab is orchestrated through a main runner `src/run_lab.py` utilizing the `uv` package manager for dependency resolution (as defined in `pyproject.toml`).

### Execution Findings (Windows Environment):
1. **SSL/TLS Certificates Requirement**: Connecting to PyPI using `uv` resulted in `invalid peer certificate` errors initially. This was circumvented by instructing `uv` to use native TLS (`uv run --native-tls icarus`).
2. **Dependency Resolution Failure (`liboqs-python`)**: 
   The lab execution **failed** during the environment build phase.
   - **Error Details**: `liboqs not found... raise RuntimeError(msg)`
   - **Root Cause**: The project relies on `liboqs-python` (Open Quantum Safe wrapper). On Windows, this library lacks a pre-compiled wheel carrying the native bindings out-of-the-box or requires the underlying `liboqs` C library to be explicitly compiled and present in the system PATH before the Python wrapper can be installed.

---

## 3. Recommendations & Next Steps

To successfully execute the lab scenarios (Phases 1 through 5) and allow the simulated MITM attack validations to complete, the runtime environment must be adjusted:

1. **Option A (Containerization / WSL - Recommended)**:
   Run the project within a **Windows Subsystem for Linux (WSL)** instance or a Docker Container running Ubuntu. `liboqs` pre-compiled binaries and Python wheels are generally more accessible and stable on Linux environments.
   
2. **Option B (Native Windows Compilation)**:
   If execution must remain natively on Windows, you must compile the C `liboqs` library from source using CMake and Visual Studio Build Tools, and then point `liboqs-python` to the compiled binaries during the `uv sync` process.

Until the cryptography backend can be successfully compiled, the mathematical and theoretical concepts outlined in `docs/LAB_GUIDE.md` serve as a complete architectural reference for the PQC migration strategy.
