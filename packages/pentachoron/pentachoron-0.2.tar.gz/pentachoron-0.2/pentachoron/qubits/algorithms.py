import numpy as np
from .circuit import QuantumCircuit
from .gates import QuantumGate, PhaseGate

class GroverCircuit(QuantumCircuit):
    def __init__(self, num_qubits, oracle):
        super().__init__(num_qubits)
        if oracle.matrix.shape != (2 ** num_qubits, 2 ** num_qubits):
            raise ValueError("Oracle size must match the number of qubits.")
        self.oracle = oracle
        self.diffusion_gate = self._create_diffusion_operator()

    def _create_diffusion_operator(self):
        n = 2 ** self.num_qubits
        s = np.ones((n, n), dtype=complex) / n
        I = np.eye(n, dtype=complex)
        return QuantumGate(2 * s - I)

    def build_grover_circuit(self):
        for i in range(self.num_qubits):
            self.add_gate(QuantumGate.hadamard(), [i])
        self.add_gate(self.oracle, list(range(self.num_qubits)))
        self.add_gate(self.diffusion_gate, list(range(self.num_qubits)))





class QFTCircuit(QuantumCircuit):
    def __init__(self, num_qubits):
        super().__init__(num_qubits)

    def apply_qft(self):
        for i in range(self.num_qubits):
            self.add_gate(QuantumGate.hadamard(), [i])
            for j in range(i + 1, self.num_qubits):
                theta = np.pi / (2 ** (j - i))
                self.add_gate(PhaseGate(theta), [j])

    def execute(self):
        super().execute()
        return self.measure_all()


class QuantumDeletionTheory:

    @staticmethod
    def initialize_qubit(state):
        """
        Initialize a qubit in a given state.
        'state' is a tuple of the form (alpha, beta) where |alpha|^2 + |beta|^2 = 1.
        """
        alpha, beta = state
        return np.array([alpha, beta])

    @staticmethod
    def apply_dissipation(state, eta):
        """
        Apply energy dissipation to a quantum state.
        'eta' is the dissipation factor, where 0 <= eta <= 1.
        """
        return eta * state

    @staticmethod
    def fidelity(state1, state2):
        """
        Calculate the fidelity between two quantum states.
        Fidelity is defined as F = |<psi1 | psi2>|^2.
        """
        return np.abs(np.dot(np.conjugate(state1), state2)) ** 2

    @staticmethod
    def calculate_information_loss(eta):
        """
        Calculate information loss based on the dissipation factor.
        L = 1 - eta^2
        """
        return 1 - eta ** 2


from .simulator import Simulator  # Import your custom Simulator
from .gates import QuantumGate, CNOTGate  # Import gate definitions

class Superentanglement:
    @staticmethod
    def normalize_coefficients(a, B):
        """Ensure coefficients satisfy normalization."""
        norm = np.sqrt(abs(a) ** 2 + abs(B) ** 2)
        return a / norm, B / norm

    @staticmethod
    def prepare_superentanglement(a, B):
        """
        Prepare the superentanglement state:
        |superentanglement> = a|entanglement> + B|disentanglement>
        """
        # Normalize coefficients
        a, B = Superentanglement.normalize_coefficients(a, B)

        # Define the simulator and initialize the state
        simulator = Simulator()
        num_qubits = 2
        state = Simulator.initialize_qubits(num_qubits)


        # Define gates
        hadamard = Simulator.H  # Hadamard gate
        cnot = Simulator.CNOT  # CNOT gate

        # Create the entanglement state (|entanglement> = 1/sqrt(2) * (|00> + |11>))
        gates_sequence = [
            (hadamard, [0]),       # Apply Hadamard to qubit 0
            (cnot, [0, 1])         # Apply CNOT to qubits 0 (control) and 1 (target)
        ]

        # Adjust amplitudes based on coefficients a and B
        rotation_a = QuantumGate.rotation_y(2 * np.arccos(abs(a)))  # RY rotation for a
        rotation_B = QuantumGate.rotation_y(2 * np.arccos(abs(B)))  # RY rotation for B

        gates_sequence.append((rotation_a, [0]))  # Rotate qubit 0 by a
        gates_sequence.append((rotation_B, [1]))  # Rotate qubit 1 by B

        return simulator.execute_circuit(num_qubits, gates_sequence)

    @staticmethod
    def measure_superentanglement(state, num_qubits):
        """Measure the superentanglement state."""
        simulator = Simulator()
        outcome, measured_qubits = simulator.measure(state, num_qubits)
        return outcome, measured_qubits

    @staticmethod
    def visualize_superentanglement(state, num_qubits):
        """Visualize the superentanglement state."""
        Simulator.visualize_state(state, num_qubits)
