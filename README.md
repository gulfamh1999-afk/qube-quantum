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

---

## Architecture & Workflow

Classical Genomic Data (CCLE / GDSC)
│
PCA Preprocessing (Dimensionality Reduction)
│
Feature Map Engine (RY Rotation Encoding)
│
Variational Circuit (RY + RZ + Linear CNOT Chain)
│
Quantum Measurement (Pauli-Z Expectation Value)
│
Hybrid Optimization Loop (COBYLA / SPSA)
│
Target Output (IC50 Drug Sensitivity Prediction)

## Performance & Optimization Dynamics

* **Single-Sample Convergence:** On isolated sample vectors, the COBYLA optimizer achieves loss values on the order of $10^{-10}$ in ideal simulation environments.
* **Multi-Sample Manifold Loss:** Evaluated on batch datasets, demonstrating stable parameter convergence on low-dimensional manifolds.
* **Ansatz Expressivity:** Utilizes localized $RY+RZ$ variational layers mapped to Pauli-$Z$ observables ($\sum_i \langle Z_i \rangle$).

---

## Hardware Execution & QPU Variance (IBM Quantum)

Qube Quantum Engine has been benchmarked on superconducting QPUs via the IBM Quantum Platform (Heron-class and Eagle-class architectures).

* **Tested Backends:** `ibm_marrakesh`, `ibm_fez`, `ibm_kingston`.
* **Execution Features:** Transpiled via `preset_pass_manager` (Optimization Level 3, Sabre routing) with dynamical decoupling enabled.
* **Hardware Stability Analysis:** Measures cross-backend variance and hardware execution drift between noiseless statevector simulation (`AerSimulator`) and physical QPUs.

---

## Application to Genomic Datasets

For complete end-to-end pipelines applying Qube Engine to Cancer Cell Line Encyclopedia (CCLE) and Genomics of Drug Sensitivity in Cancer (GDSC) datasets, see:  
👉 [Qube Cancer Atlas Pipeline Repository](https://github.com/gulfamh1999-afk/qube-cancer-atlas)

---

## 📄 Publication & Citation

If you use or reference this work in your research, please cite the updated preprint:

> Hussain, G. (2026). *Variational Quantum Regression for Genomic Drug Sensitivity Prediction on NISQ Hardware*. Zenodo.  
> https://doi.org/10.5281/zenodo.19415679

---

## ⚖️ Intellectual Property & Licensing

© 2026 Gulfam Hussain.

This repository is dual-licensed:
* **Community Edition (MIT License):** Available for individual academic research, open-source development, and educational purposes.
* **Enterprise Edition:** For enterprise integration, proprietary dataset training, or commercial deployments, a separate commercial license is required.

For licensing inquiries or collaboration, contact: `gulfamh1999@gmail.com`
