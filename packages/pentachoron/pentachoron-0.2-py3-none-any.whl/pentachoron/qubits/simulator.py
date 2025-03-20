import itertools
import numpy as np
from .gates import QuantumGate, CNOTGate, PhaseGate, TGate, ControlledGate

class Simulator:
    # Initialize common gates
    H = QuantumGate.hadamard()  # Hadamard
    X = QuantumGate.pauli_x()  # Pauli-X
    Y = QuantumGate.pauli_y()  # Pauli-Y
    Z = QuantumGate.pauli_z()  # Pauli-Z
    T = TGate  # T-gate (π/4 phase)

    # Two-qubit gates
    CNOT = CNOTGate  # Controlled-NOT

    @staticmethod
    def custom_gate(matrix):
        """Create a custom gate given a user-defined matrix."""
        matrix = np.array(matrix)
        if matrix.shape[0] != matrix.shape[1] or np.linalg.norm(
                matrix.dot(matrix.T.conj()) - np.eye(matrix.shape[0])) > 1e-10:
            raise ValueError("The provided matrix must be unitary.")
        return matrix

    @staticmethod
    def tensor_product(gate_matrix, num_qubits, target_qubits):
        """Create the full operator by applying the gate to the specified target qubits within num_qubits qubits."""
        identity = np.eye(2, dtype=complex)
        op = gate_matrix if isinstance(gate_matrix, np.ndarray) else gate_matrix.matrix

        expected_size = 2 ** num_qubits  # The expected size of the full operator
        if op.shape == (expected_size, expected_size):
            return op  # If the gate is already the right size, return it

        # Handle single-qubit gates
        if len(target_qubits) == 1:
            full_operator = np.eye(1, dtype=complex)
            for i in range(num_qubits):
                if i in target_qubits:
                    full_operator = np.kron(full_operator, op)
                else:
                    full_operator = np.kron(full_operator, identity)

        # Handle two-qubit CNOT gate (assuming only 2 qubits for now)
        elif len(target_qubits) == 2 and num_qubits == 2:
            control, target = target_qubits
            if control == 0 and target == 1:
                full_operator = np.array([
                    [1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 0, 1],
                    [0, 0, 1, 0]
                ], dtype=complex)  # Standard CNOT for 2 qubits
            else:
                raise ValueError("CNOT gate for other configurations not implemented yet.")
        else:
            raise ValueError(f"Unsupported qubit count or operation: num_qubits={num_qubits}, target_qubits={target_qubits}")

        # Final size check
        if full_operator.shape != (expected_size, expected_size):
            raise ValueError(f"Incorrect operator size: got {full_operator.shape}, expected ({expected_size}, {expected_size})")

        return full_operator

    @staticmethod
    def apply_gate(state, gate, num_qubits, target_qubits):
        """Apply a quantum gate to specific qubits in the system."""
        if isinstance(gate, type):  # Check if it's a class, not an instance
            gate = gate()  # Instantiate it

        full_op = Simulator.tensor_product(gate.get_matrix(), num_qubits, target_qubits)
        return np.dot(full_op, state)

    @staticmethod
    def initialize_qubits(num_qubits):
        """Initialize a quantum system of num_qubits in the |00...0> state."""
        state = np.zeros(2 ** num_qubits, dtype=complex)
        state[0] = 1
        return state

    @staticmethod
    def measure(state, num_qubits):
        """Perform measurement on all qubits."""
        probabilities = np.abs(state) ** 2
        outcome = np.random.choice(len(state), p=probabilities)
        return np.binary_repr(outcome, num_qubits)

    @staticmethod
    def add_noise(state, noise_level=0.01):
        """Simulate noise by adding random perturbations to the state."""
        noise = (np.random.randn(*state.shape) + 1j * np.random.randn(*state.shape)) * noise_level
        noisy_state = state + noise
        noisy_state /= np.linalg.norm(noisy_state)  # Renormalize
        return noisy_state

    @staticmethod
    def execute_circuit(num_qubits, gates_sequence):
        """Execute a full quantum circuit given a sequence of gates."""
        state = Simulator.initialize_qubits(num_qubits)

        for gate, target_qubits in gates_sequence:
            state = Simulator.apply_gate(state, gate, num_qubits, target_qubits)
            state = Simulator.add_noise(state, noise_level=0.01)  # Add some noise to simulate real-world conditions

        return state

    @staticmethod
    def visualize_state(state, num_qubits):
        """Visualize the state vector as probabilities of each basis state."""
        probabilities = np.abs(state) ** 2
        for i, prob in enumerate(probabilities):
            if prob > 0.01:  # Display only non-trivial probabilities
                print(f"|{np.binary_repr(i, num_qubits)}> : {prob:.4f}")
