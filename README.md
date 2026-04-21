# Qube Quantum Engine (Verified on real IBM Quantum hardware with 98.23% stability across multiple backends).

> A hybrid quantum learning engine for encoding and optimizing classical data in quantum states. 

---

## Overview

Qube is a compact variational quantum learning engine that maps classical data into quantum states and optimizes them using hybrid classical-quantum training.

It provides a clean and minimal implementation of a quantum learning pipeline:

* Classical data encoding
* Variational quantum circuits
* Batch optimization

---

## Features

* Data encoding using rotation gates (RY)
* Trainable variational layers (RY + RZ)
* Multi-sample training with batch loss
* Supports supervised and unsupervised modes
* Lightweight and easy to understand

---

## Installation

Clone the repository and install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

```python
from qube_engine import QubeEngine
import numpy as np

engine = QubeEngine()

dataset = [
    (np.array([0.2, -0.5, 0.8, -0.1]), 0.5),
    (np.array([-0.3, 0.1, 0.6, -0.7]), -0.2),
    (np.array([0.9, -0.4, 0.2, 0.3]), 0.8),
]

params, loss = engine.train(dataset)

print("Final Loss:", loss)

for x, y in dataset:
    pred = engine.evaluate(x, params)
    print(pred, "vs", y)
```

---

## How It Works

```
Classical Data
    ↓
Memory Vector (normalized)
    ↓
Quantum Encoding (RY gates)
    ↓
Variational Circuit (RY + RZ + entanglement)
    ↓
Measurement (Pauli-Z observable)
    ↓
Optimization (COBYLA)
```

---

## Performance Highlights 

Based on final verification tests on **March 29, 2026**:

- **Ultra-High Precision:** Achieved a single-sample training loss of **1.32e-10**.
- **Robust Generalization:** Successfully aligned multi-sample manifolds with a final dataset loss of **0.0005**.
- **Advanced Ansatz:** Implements a localized RY+RZ variational layer with Z-Observable expectation mapping for maximum expressivity.

---

## Hardware Benchmark **(IBM Quantum Validation)**

Qube Quantum Engine has been validated on real-world superconducting quantum hardware using the IBM Quantum Platform (Heron-class processors) acheiving an elite 98.23% Stability Score. Verified on **April 3, 2026**

Average Hardware Fidelity: **98.23%**
- Verified across ibm_fez, ibm_kingston, and ibm_marrakesh backends.
  
  *Navigate to benchmarks for more details.

## Dataset Qube Application 

https://github.com/gulfamh1999-afk/qube-cancer-atlas

---

## 📄 Associated Publication

If you use or reference this work, please cite:

> Hussain, G. (2026). *Qube Engine: Noise-Resilient Quantum Learning Framework for NISQ Systems (v1.2)*. Zenodo.  
> https://doi.org/10.5281/zenodo.19415679

## ⚖️ Intellectual Property & Copyright
The underlying algorithmic logic, specific ansatz architecture, and quantum-classical hybrid optimization strategies contained within this repository are the original intellectual property of the author and are formally registered with the United States Copyright Office. 

© 2026 Gulfam Hussain. Licensed under MIT (Community) / Proprietary (Enterprise).

## 🔓 Licensing
This software is dual-licensed:

Community Edition (MIT License): This specific public implementation is provided for individual research, academic exploration, and community innovation. Permission is granted to use, modify, and build upon this code provided that this original copyright notice and license are included in all copies.

Enterprise & Commercial Edition: For enterprise production environments, high-performance proprietary dataset integration, or commercial applications, a separate Commercial License is required.

For commercial inquiries or to discuss the Qube Engine program, please reach out via gulfamh1999@gmail.com.
