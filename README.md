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

##Performance Highlights

Based on final verification tests on **March 29, 2026**:

- **Ultra-High Precision:** Achieved a single-sample training loss of **1.32e-10**.
- **Robust Generalization:** Successfully aligned multi-sample manifolds with a final dataset loss of **0.0005**.
- **Advanced Ansatz:** Implements a localized RY+RZ variational layer with Z-Observable expectation mapping for maximum expressivity.

---

##Hardware Benchmark **(IBM Quantum Validation)**

Qube Quantum Engine has been validated on real-world superconducting quantum hardware using the IBM Quantum Platform (Heron-class processors) acheiving an elite 98.23% Stability Score. Verified on **April 3, 2026**

Average Hardware Fidelity: **98.23%**
- Verified across ibm_fez, ibm_kingston, and ibm_marrakesh backends.
  
  *Navigate to benchmarks for more details.
---

## License

MIT License — free to use, modify, and build upon.
Attribution to the original author is appreciated.
