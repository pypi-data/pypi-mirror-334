import numpy as np


class Qutrit:
    def __init__(self, index, state=None):
        self.index = index
        if state is None:
            # Start in the |0⟩ state if no initial state is provided
            self.state = np.array([1, 0, 0], dtype=complex)
        else:
            # Custom initial state
            self.state = state

    def apply_gate(self, gate):
        """Apply a quantum gate to the qubit's state."""
        self.state = np.dot(gate.matrix, self.state)

    def measure(self):
        """Measure the qubit's state, returning 0 or 1."""
        probabilities = np.abs(self.state) ** 2
        probabilities /= np.sum(probabilities)  # Normalize probabilities
        result = np.random.choice([2, 1, 0], p=probabilities)
        return result

    @staticmethod
    def create_qutrit(alpha, beta , gamma):
        """Create a custom qubit with the specified alpha and beta states."""
        # Ensure normalization: |α|^2 + |β|^2 = 1, with tolerance for floating-point precision
        if not np.isclose(abs(alpha) ** 2 + abs(beta) ** 2 + abs(gamma) , 1.0):
            raise ValueError("The state must be normalized (|α|^2 + |β|^2 + |c|^2 = 1).")

        # Return a Qubit instance with the custom state vector
        state = np.array([alpha, beta, gamma], dtype=complex)
        return Qutrit(index=None, state=state)