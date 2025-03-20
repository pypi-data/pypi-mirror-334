import numpy as np
from .Qutrit import Qutrit

class QuantumGate:
    def __init__(self, matrix):
        self.matrix = matrix
        self.size = matrix.shape[0]  # Store the size of the gate

    def to_matrix(self):
        """Return the matrix representation of the gate."""
        return self.matrix

    @staticmethod
    def identity_qutrit():
        """3x3 identity gate for qutrit."""
        return QuantumGate(np.eye(3, dtype=complex))

    @staticmethod
    def cycle_gate():
        """Qutrit 'X' gate that cycles |0⟩ -> |1⟩, |1⟩ -> |2⟩, |2⟩ -> |0⟩."""
        return QuantumGate(np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex))

    @staticmethod
    def phase_gate(theta):
        """Phase gate for qutrit."""
        return QuantumGate(np.array([
            [1, 0, 0],
            [0, np.exp(1j * theta), 0],
            [0, 0, 1]
        ], dtype=complex))


class CNOTGate(QuantumGate):
    def __init__(self):
        # Define a 9x9 matrix for a CNOT gate on qutrits
        matrix = np.eye(9, dtype=complex)  # Identity for cases where control is in |0⟩ or |2⟩
        # Define the flip when control qutrit is in |1⟩ state
        matrix[4, 4] = 0
        matrix[4, 5] = 1
        matrix[5, 5] = 0
        matrix[5, 4] = 1
        super().__init__(matrix)

    def apply_to(self, control_qutrit: Qutrit, target_qutrit: Qutrit):
        """Applies the CNOT gate to the given control and target qutrits."""
        # Compute tensor product of control and target qutrit states
        combined_state = np.kron(control_qutrit.state, target_qutrit.state)  # 9-dimensional vector
        print(f"Combined state: {combined_state}")  # Debugging line

        # Apply the 9x9 matrix (CNOT)
        new_state = np.dot(self.matrix, combined_state)
        print(f"New state after applying CNOT: {new_state}")  # Debugging line

        # Extract control state index (active state of control)
        control_index = control_qutrit.state.argmax()  # Get the active control state (0, 1, or 2)
        print(f"Control index: {control_index}")  # Debugging line

        # Extract the target state's new value based on control index
        target_start = control_index * 3
        target_end = target_start + 3
        target_state = new_state[target_start:target_end]  # Extract the target portion
        print(f"Target state after applying gate: {target_state}")  # Debugging line

        # Ensure that target state is correctly assigned (only one non-zero component)
        if np.sum(np.abs(target_state)) != 0:
            target_state = target_state / np.linalg.norm(target_state)  # Normalize target state

        # Update the control qutrit state
        control_qutrit.state = np.zeros(3, dtype=complex)
        control_qutrit.state[control_index] = 1  # Keep control at its original state

        # Update the target qutrit state
        target_qutrit.state = target_state  # Assign the new target state

        # Debugging output after updating qutrits
        print(f"Updated control qutrit state: {control_qutrit.state}")
        print(f"Updated target qutrit state: {target_qutrit.state}")



class ControlledGate(QuantumGate):
    def __init__(self, control_qutrit: Qutrit, target_qutrit: Qutrit, base_gate: QuantumGate):
        super().__init__(base_gate.to_matrix())  # Initialize with the base gate matrix
        self.control_qutrit = control_qutrit
        self.target_qutrit = target_qutrit
        self.base_gate = base_gate

    def apply_to(self):
        """Applies the base gate to the target qutrit if the control qutrit is in the |1⟩ state."""
        if np.abs(self.control_qutrit.state[1]) > 0.5:  # Threshold for "in state |1⟩"
            self.target_qutrit.apply_gate(self.base_gate)


