# Policy-Based Secure Ephemeral File Sharing Framework

## Overview
A research-oriented framework for ephemeral data sharing utilizing **in-memory decryption** and **OS-level memory isolation**. Designed to eliminate persistent storage artifacts and enforce strict, policy-based lifecycle management.

## Project Structure
* `/src/backend`: Core C++ implementation with OS-level memory pinning (`VirtualLock`).
* `/src/gui`: Python/Tkinter controller for the Policy Engine and user interaction.
* `/tests`: Forensic validation scripts and memory dump analysis workflows.

## Security & Methodology
This project leverages **AES-256-GCM** encryption and **RSA** key management to ensure data confidentiality. Ephemerality is enforced through a state-machine policy engine, with physical memory sanitization on process exit to prevent forensic recovery.
