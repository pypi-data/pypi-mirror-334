from pentachoron.qubits.gates import QuantumGate
import numpy as np
def test_mohammed_gate():
    n = 5  # Number of qubits
    initial_state = np.zeros(2 ** n, dtype=complex)
    initial_state[16] = 1  # Set the state to |10000⟩

    # Apply the Mohammed Gate
    mohammed_gate = QuantumGate.Mohammed_gate(n)
    final_state = mohammed_gate.apply(initial_state)

    print("Initial state:", initial_state)
    print("Final state:", final_state)


if __name__ == "__main__":
    test_mohammed_gate()
