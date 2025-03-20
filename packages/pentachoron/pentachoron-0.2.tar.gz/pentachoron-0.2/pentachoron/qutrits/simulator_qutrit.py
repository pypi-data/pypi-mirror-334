import itertools
import numpy as np
from .gates_qutrit import QuantumGate, CNOTGate, ControlledGate

class Simulator:

    C = QuantumGate.cycle_gate()
    P = QuantumGate.phase_gate(theta=0)
    CNOT = CNOTGate  # Controlled-NOT


    # Custom gates
    @staticmethod
    def custom_gate(matrix):
        """Create a custom gate given a user-defined matrix."""
        matrix = np.array(matrix)
        if matrix.shape != (3, 3) or np.linalg.norm(matrix.dot(matrix.T.conj()) - np.eye(3)) > 1e-10:
            raise ValueError("The provided matrix must be unitary.")
        return matrix

    @staticmethod
    def tensor_product(gate, num_qutrits, target_qutrits):
        """Expand a single qutrit gate to act on the specified qutrits in a multi-qutrit system."""
        i = np.eye(3)
        full_op = np.eye(3)  # Start with a 3x3 identity matrix for a single qutrit

        # Convert gate to its matrix if it's an instance of a class
        if isinstance(gate, QuantumGate):
            gate_matrix = gate.to_matrix()  # Correct way to call the instance method
  # or use the correct method to obtain the matrix

        for qutrit in range(num_qutrits):
            if qutrit in target_qutrits:
                full_op = np.kron(full_op, gate)  # Apply the gate to the target qutrit
            else:
                full_op = np.kron(full_op, i)  # Apply an identity operation to the non-target qutrit

        return full_op

    def apply_gate(self, state, gate, num_qutrits, target_qutrits):
        if not isinstance(gate, QuantumGate):
            print(f"Received gate type: {type(gate)}")  # Debugging line
            raise ValueError("gate must be an instance of QuantumGate")


        gate_matrix = gate.to_matrix()

        # Use the number of target qutrits directly
        expected_size = 3 ** len(target_qutrits)  # Assuming target_qutrits is a list of indices

        if gate_matrix.shape != (expected_size, expected_size):
            raise ValueError(
                f"Gate matrix size mismatch: expected {expected_size}x{expected_size}, got {gate_matrix.shape[0]}x{gate_matrix.shape[1]}"
            )

        full_op = np.kron(gate_matrix, np.eye(3 ** (num_qutrits - len(target_qutrits))))

        if full_op.shape[1] != state.shape[0]:
            raise ValueError(f"Dimension mismatch: {full_op.shape[1]} vs {state.shape[0]}")

        return np.dot(full_op, state)

    def execute_circuit(self, num_qutrits, gates_sequence):
        """Execute a full quantum circuit given a sequence of gates."""
        state = self.initialize_qutrits(num_qutrits)

        for gate, target_qutrits in gates_sequence:
            state = self.apply_gate(state, gate, num_qutrits, target_qutrits)
            state = self.add_noise(state, noise_level=0.01)  # Add noise
        return state

    # Step 3: Initialize a multi-qutrit system
    @staticmethod
    def initialize_qutrits(num_qutrits):
        """Initialize a quantum system of num_qutrits in the |00...0> state."""
        state = np.zeros(3 ** num_qutrits, dtype=complex)
        state[0] = 1
        return state

    # Step 4: Measurement
    @staticmethod
    def measure(state, num_qutrits):
        """Perform measurement on all qubits."""
        probabilities = np.abs(state) ** 2
        outcome = np.random.choice(len(state), p=probabilities)
        return outcome, num_qutrits

    # Step 5: Add Noise (optional)
    @staticmethod
    def add_noise(state, noise_level=0.01):
        """Simulate noise by adding random perturbations to the state."""
        noise = (np.random.randn(*state.shape) + 1j * np.random.randn(*state.shape)) * noise_level
        noisy_state = state + noise
        noisy_state /= np.linalg.norm(noisy_state)  # Renormalize
        return noisy_state

    # Step 6: Execute a full circuit
    def execute_circuit(self, num_qutrits, gates_sequence):
        """Execute a full quantum circuit given a sequence of gates."""
        state = self.initialize_qutrits(num_qutrits)

        for gate, target_qutrits in gates_sequence:
            state = self.apply_gate(state, gate, num_qutrits, target_qutrits)
            state = self.add_noise(state, noise_level=0.01)  # Add some noise to simulate real-world conditions

        return state

    # Step 7: Visualization (text-based)
    @staticmethod
    def visualize_state(state, num_qutrits):
        """Visualize the state vector as probabilities of each basis state."""
        probabilities = np.abs(state) ** 2
        for i, prob in enumerate(probabilities):
            if prob > 0.01:  # Display only non-trivial probabilities
                print(f" State Index {i}: Probability {prob:.4f}")
