import numpy as np
import matplotlib.pyplot as plt
import os

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, thermal_relaxation_error, ReadoutError
from scipy.optimize import minimize

from qiskit_ibm_runtime import QiskitRuntimeService, Sampler


class QubeEngine:

    def __init__(self, backend=None, noise=False, shots=512):
        self.noise = noise
        self.shots = shots

        if backend:
            self.backend = backend
        else:
            self.backend = self._build_simulator()

    def _build_simulator(self):
        if not self.noise:
            return AerSimulator()

        noise_model = NoiseModel()

        error_1 = depolarizing_error(0.006, 1)
        error_2 = depolarizing_error(0.012, 2)

        noise_model.add_all_qubit_quantum_error(error_1, ['ry', 'rz'])
        noise_model.add_all_qubit_quantum_error(error_2, ['cx'])

        t1, t2 = 60e3, 80e3
        thermal_error = thermal_relaxation_error(t1, t2, 80)
        noise_model.add_all_qubit_quantum_error(thermal_error, ['id'])

        readout_error = ReadoutError([[0.94, 0.06], [0.06, 0.94]])
        noise_model.add_all_qubit_readout_error(readout_error)

        return AerSimulator(noise_model=noise_model)

    def _build_ansatz(self, angles, params):
        n = len(angles)
        qc = QuantumCircuit(n, n)

        for i, theta in enumerate(angles):
            qc.ry(theta, i)
            qc.ry(params[i], i)
            qc.rz(params[i + n], i)

        if n > 1:
            qc.cx(0, 1)
            if n > 3:
                qc.cx(2, 3)

        qc.measure(range(n), range(n))
        return qc

    def evaluate(self, memory, params):
        angles = (np.array(memory) + 1.0) * (np.pi / 2.0)
        qc = self._build_ansatz(angles, params)

        compiled = transpile(qc, self.backend)

        if "ibm" in str(self.backend).lower():

            sampler = Sampler(mode=self.backend)
            job = sampler.run([compiled], shots=self.shots)
            result = job.result()

            data_bin = result[0].data

            if hasattr(data_bin, "c"):
                counts = data_bin.c.get_counts()
            elif hasattr(data_bin, "meas"):
                counts = data_bin.meas.get_counts()
            else:
                counts = data_bin.get_counts()

            # 🔥 simple readout mitigation (normalize bias)
            total = sum(counts.values())
            corrected = {}

            for k, v in counts.items():
                corrected[k] = v / total

            exp = 0
            for bitstring, prob in corrected.items():
                z_val = sum([1 if b == '0' else -1 for b in bitstring])
                exp += z_val * prob

            raw = exp / qc.num_qubits
            return np.tanh(raw)

        # Local
        result = self.backend.run(compiled, shots=self.shots).result()
        counts = result.get_counts()

        exp = 0
        total = sum(counts.values())

        for bitstring, count in counts.items():
            z_val = sum([1 if b == '0' else -1 for b in bitstring])
            exp += z_val * count

        raw = exp / (total * len(memory))
        return np.tanh(raw)

    def _loss(self, params, dataset):
        data = dataset if isinstance(dataset, list) else [dataset]
        return np.mean([(self.evaluate(x, params) - y) ** 2 for x, y in data])

    def train(self, dataset, maxiter=120):
        n = len(dataset[0][0])
        initial_params = np.random.rand(2 * n) * 2 * np.pi

        result = minimize(
            self._loss,
            initial_params,
            args=(dataset,),
            method='COBYLA',
            options={'maxiter': maxiter}
        )

        return result.x


# -------------------------------
# IBM Backend
# -------------------------------
def get_ibm_backend():

    token = os.getenv("IBM_QUANTUM_TOKEN")

    if token is None:
        raise ValueError(
            "❌ IBM_QUANTUM_TOKEN not found. Set it using environment variables."
        )

    service = QiskitRuntimeService(
        channel="ibm_cloud",
        token=token,
        instance="open-instance"
    )

    print("✅ Connected to IBM Quantum")

    backend = service.least_busy(simulator=False)
    print(f"⚛️ Using backend: {backend.name}")

    return backend, service


# -------------------------------
# TEST FUNCTIONS
# -------------------------------

def stability_score(ideal_engine, ibm_engine, dataset, params):
    diffs = []

    for memory, _ in dataset:
        diff = abs(
            ideal_engine.evaluate(memory, params)
            - ibm_engine.evaluate(memory, params)
        )
        diffs.append(diff)

    score = (1 - np.mean(diffs)) * 100
    print(f"\n🔥 Stability Score: {score:.2f}%")
    return score


def stability_test(engine, dataset, params):
    results = np.array([
        [engine.evaluate(x, params) for x, _ in dataset]
        for _ in range(5)
    ])

    print("\n📊 Std Dev:", np.std(results, axis=0))


def compare_backends(service, dataset, params):
    print("\n⚙️ Backend Comparison")

    for backend in service.backends(simulator=False)[:3]:
        engine = QubeEngine(backend=backend, shots=256)
        print(f"\n⚛️ {backend.name}")

        for i, (x, _) in enumerate(dataset):
            print(f"Sample {i+1}: {engine.evaluate(x, params):.4f}")


def scaling_test():
    print("\n🧠 Scaling Test (6 qubits)")

    memory = np.random.uniform(-1, 1, 6)
    params = np.random.rand(12) * 2 * np.pi

    engine = QubeEngine()
    val = engine.evaluate(memory, params)

    print("6-qubit output:", val)


def plot_results(local_engine, ibm_engine, dataset, params):
    ideal = [local_engine.evaluate(x, params) for x, _ in dataset]
    ibm = [ibm_engine.evaluate(x, params) for x, _ in dataset]

    plt.figure()
    plt.plot(ideal, marker='o', label="Ideal")
    plt.plot(ibm, marker='x', label="IBM")
    plt.legend()
    plt.title("Quantum Output Comparison")
    plt.show()


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":

    dataset = [
        (np.array([0.2, -0.5, 0.8, -0.1]), 0.5),
        (np.array([-0.3, 0.1, 0.6, -0.7]), -0.2),
        (np.array([0.9, -0.4, 0.2, 0.3]), 0.8),
    ]

    print("\n⚛️ Training locally...\n")

    local_engine = QubeEngine()
    params = local_engine.train(dataset)

    print("✅ Training complete.\n")

    ibm_backend, service = get_ibm_backend()
    ibm_engine = QubeEngine(backend=ibm_backend)

    for i, (x, _) in enumerate(dataset):
        print(f"Sample {i+1}")
        print(f"Ideal: {local_engine.evaluate(x, params):.4f}")
        print(f"IBM:   {ibm_engine.evaluate(x, params):.4f}\n")

    # 🔥 ALL TESTS
    stability_score(local_engine, ibm_engine, dataset, params)
    stability_test(ibm_engine, dataset, params)
    compare_backends(service, dataset, params)
    scaling_test()
    plot_results(local_engine, ibm_engine, dataset, params)
