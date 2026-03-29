import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp
from scipy.optimize import minimize


class QubeEngine:
    """
    Qube Core: High-fidelity Quantum Kernel Alignment for Industrial Datasets.

    Features:
    - Compact variational quantum circuit (RY + RZ)
    - Supports single-sample and multi-sample training
    - Supervised and unsupervised modes
    - Clean, minimal, stable design
    """

    # -------------------------------
    # 1. Circuit
    # -------------------------------
    def _build_ansatz(self, angles, params):
        n = len(angles)
        qc = QuantumCircuit(n)

        for i, theta in enumerate(angles):
            qc.ry(theta, i)        # Encode data
            qc.ry(params[i], i)    # Train amplitude
            qc.rz(params[i+n], i)  # Train phase

        for i in range(n - 1):
            qc.cx(i, i + 1)        # Entangle

        return qc

    # -------------------------------
    # 2. Evaluate
    # -------------------------------
    def evaluate(self, memory, params):
        angles = (np.array(memory) + 1.0) * (np.pi / 2.0)

        qc = self._build_ansatz(angles, params)

        observable = SparsePauliOp.from_list([
            ("I"*i + "Z" + "I"*(qc.num_qubits-i-1), 1.0)
            for i in range(qc.num_qubits)
        ])

        state = Statevector.from_instruction(qc)
        return np.real(state.expectation_value(observable))

    # -------------------------------
    # 3. Loss (Robust)
    # -------------------------------
    def _loss(self, params, dataset):

        # Normalize input → always list of (memory, target)
        if isinstance(dataset, tuple):
            data = [dataset]
        else:
            data = dataset

        total = 0

        for memory, target in data:
            pred = self.evaluate(memory, params)

            # Supervised
            if target is not None:
                total += (pred - target) ** 2
            # Unsupervised (VQE-style)
            else:
                total += pred

        return total / len(data)

    # -------------------------------
    # 4. Train
    # -------------------------------
    def train(self, dataset, maxiter=200):
        """
        dataset:
        - Single: (memory_vector, target)
        - Multi: [(memory_vector, target), ...]
        """

        # Extract sample size safely
        if isinstance(dataset, tuple):
            sample = dataset[0]
        else:
            sample = dataset[0][0]

        n = len(sample)

        initial_params = np.random.rand(2 * n) * 2 * np.pi

        result = minimize(
            self._loss,
            initial_params,
            args=(dataset,),
            method='COBYLA',
            options={'maxiter': maxiter}
        )

        return result.x, result.fun


# -------------------------------
# 5. Example Usage
# -------------------------------
if __name__ == "__main__":

    engine = QubeEngine()

    # --- Single Sample ---
    single_sample = (np.array([0.2, -0.5, 0.8, -0.1]), 0.5)

    params_s, loss_s = engine.train(single_sample)
    pred_s = engine.evaluate(single_sample[0], params_s)

    print("Single Sample:")
    print("Prediction:", pred_s)
    print("Target:", single_sample[1])
    print("Loss:", loss_s)

    # --- Multi Sample Dataset ---
    dataset = [
        (np.array([0.2, -0.5, 0.8, -0.1]), 0.5),
        (np.array([-0.3, 0.1, 0.6, -0.7]), -0.2),
        (np.array([0.9, -0.4, 0.2, 0.3]), 0.8),
    ]

    params_d, loss_d = engine.train(dataset)

    print("\nDataset Training:")
    print("Final Loss:", loss_d)

    print("\nPredictions:")
    for i, (x, y) in enumerate(dataset):
        pred = engine.evaluate(x, params_d)
        print(f"Sample {i+1}: Pred={pred:.4f}, Target={y}")