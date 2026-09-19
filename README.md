# Qube Quantum Engine: Variational Quantum Regression on IBM Quantum Hardware

A hybrid quantum-classical machine learning framework implementing Variational Quantum Regression (VQR) for encoding classical genomic data (CCLE/GDSC) into parameterized quantum states. Evaluated across IBM Quantum superconducting processors (`ibm_marrakesh`, `ibm_fez`, `ibm_kingston`).

---

## Overview

Qube is a compact variational quantum learning engine that maps high-dimensional classical data into quantum states and optimizes them using hybrid classical-quantum optimization loops.

It provides a clean, modular implementation of a variational quantum pipeline:
* **Feature Encoding:** Classical vector mapping into single-qubit rotation gates.
* **Parameterized Ansatz:** $RY + RZ$ rotation layers coupled with linear nearest-neighbor CNOT entangling circuits.
* **Hybrid Optimization:** Parameter updates driven by classical optimizers (COBYLA/SPSA) targeting Mean Squared Error (MSE) loss.

---

## Features

* **Data Encoding:** Direct feature mapping via rotation gates ($RY$).
* **Trainable Variational Layers:** Bounded $RY + RZ$ parameterized layers.
* **Supervised & Unsupervised Modes:** Loss evaluation supports both direct target regression ($MSE$) and Hamiltonian expectation minimization (VQE-style).
* **Hardware Integration:** Native support for local simulation (`AerSimulator`) and IBM Quantum hardware execution via `QiskitRuntimeService` (Sampler V2).

---

## Installation

Clone the repository and install dependencies:

```bash
git clone [https://github.com/gulfamh1999-afk/qube-quantum.git](https://github.com/gulfamh1999-afk/qube-quantum.git)
cd qube-quantum
pip install -r requirements.txt
