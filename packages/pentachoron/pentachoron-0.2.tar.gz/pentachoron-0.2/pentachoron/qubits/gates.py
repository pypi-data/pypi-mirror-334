import numpy as np
from .qubit import Qubit  # Import the Qubit class


class QuantumGate:
    def __init__(self, matrix):
        self.matrix = matrix
        self.size = matrix.shape[0]

    def get_matrix(self):
        return self.matrix
    def apply(self, state):
        return np.dot(self.matrix, state)
    @staticmethod
    def pauli_x():
        return QuantumGate(np.array([[0, 1], [1, 0]], dtype=complex))

    @staticmethod
    def pauli_y():
        return QuantumGate(np.array([[0, -1j], [1j, 0]], dtype=complex))

    @staticmethod
    def pauli_z():
        return QuantumGate(np.array([[1, 0], [0, -1]], dtype=complex))

    @staticmethod
    def hadamard():
        return QuantumGate((1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex))

    @staticmethod
    def rotation_y(theta):
        return QuantumGate(np.array([
            [np.cos(theta / 2), -np.sin(theta / 2)],
            [np.sin(theta / 2), np.cos(theta / 2)]
        ], dtype=complex))


    @staticmethod
    def Idrees_gate(n):
        """Flip the last three qubits if the first qubit is |1⟩."""
        size = 2 ** n
        I = np.eye(size, dtype=complex)  # Identity matrix of size 2^n

        for i in range(size):
            if (i >> (n - 1)) & 1:  # Check if the first qubit is |1⟩
                print(f"First qubit is |1⟩ at index {i}")
                # Flip the last three qubits
                for j in range(3):
                    flipped_i = i ^ (1 << (n - 1 - j))  # Flip the j-th qubit from the end
                    print(f"Flipping qubit at index {flipped_i} (original {i})")
                    # Modify the identity matrix to apply the flip
                    I[i, flipped_i] = 0  # Remove original state
                    I[flipped_i, flipped_i] = 1  # Set flipped state to 1
                    I[flipped_i, i] = 1  # Swap original state and flipped state
                    I[i, i] = 1  # Set original state back to 1

        return QuantumGate(I)

    @staticmethod
    def apply_cnot(state, control, target, n):
        """Applies a CNOT gate on state between the given control and target qubits."""
        size = 2 ** n
        new_state = np.copy(state)
        for i in range(size):
            if (i >> control) & 1:  # Check if the control qubit is |1⟩
                # Flip the target qubit (toggle the target bit)
                target_state = i ^ (1 << target)  # Flip target qubit using XOR
                # Swap the states between i and target_state
                new_state[i], new_state[target_state] = new_state[target_state], new_state[i]
        return new_state

    @staticmethod
    def Ahmad_gate(n):
        """Applies a cascading CNOT operation from qubit 0 to qubit n-1."""
        size = 2 ** n
        state = np.zeros(size, dtype=complex)
        state[16] = 1  # Example: setting the 16th index to |1⟩

        print("Initial state:", state)

        # Apply the CNOT gates one by one
        for i in range(n - 1):
            print(f"Applying CNOT between qubit {i} (control) and qubit {i + 1} (target).")
            state = QuantumGate.apply_cnot(state, i, i + 1, n)
            print(f"State after CNOT between qubit {i} and qubit {i + 1}:", state)

        return state
    @staticmethod
    def Mohammed_gate(n):
        """Flips the last 6 qubits while iteratively shifting them if the first qubit is |1⟩."""
        size = 2 ** n
        I = np.eye(size, dtype=complex)  # Identity matrix of size 2^n

        for i in range(size):
            if (i >> (n - 1)) & 1:  # Check if the first qubit is |1⟩

                flipped_i = i
                for j in range(6):
                    if (n - 1 - j) >= 0:
                        flipped_i ^= (1 << (n - 1 - j))
                    # Flip the j-th qubit from the end
                    I[i, flipped_i] = 1  # Set the new state
                    I[flipped_i, i] = 1  # Allow bidirectional state change

        return QuantumGate(I)


class PhaseGate(QuantumGate):
    def __init__(self, theta):
        matrix = np.array([
            [1, 0],
            [0, np.exp(1j * theta)]
        ], dtype=complex)
        super().__init__(matrix)


class TGate(PhaseGate):
    def __init__(self):
        super().__init__(np.pi / 4)


class CNOTGate(QuantumGate):
    def __init__(self):
        super().__init__(np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0]
        ], dtype=complex))

    def apply_to(self, control_qubit: Qubit, target_qubit: Qubit):
        combined_state = np.kron(control_qubit.state, target_qubit.state)
        new_state = np.dot(self.matrix, combined_state)
        control_qubit.state, target_qubit.state = new_state[:2], new_state[2:]


class ControlledGate(QuantumGate):
    def __init__(self, control_qubit: Qubit, target_qubit: Qubit, base_gate: QuantumGate):
        self.control_qubit = control_qubit
        self.target_qubit = target_qubit
        self.base_gate = base_gate

    def apply_to(self):
        if np.abs(self.control_qubit.state[1]) > 0:
            self.target_qubit.apply_gate(self.base_gate)
