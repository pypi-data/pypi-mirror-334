import numpy as np
from .qubit import Qubit
from .gates import QuantumGate, CNOTGate, ControlledGate
import random

class QuantumCircuit:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.qubits = [Qubit(i) for i in range(num_qubits)]
        self.gates = []

    def add_gate(self, gate, qubit_indices):
        self.gates.append((gate, qubit_indices))

    def execute(self):
        for gate, qubit_indices in self.gates:
            if isinstance(gate, QuantumGate) and len(qubit_indices) == 1:
                self.qubits[qubit_indices[0]].apply_gate(gate)
            elif isinstance(gate, CNOTGate):
                gate.apply_to(self.qubits[qubit_indices[0]], self.qubits[qubit_indices[1]])
            elif isinstance(gate, ControlledGate):
                gate.apply_to()  # You should define how controlled gates are applied
            else:
                combined_state = self._get_combined_state(qubit_indices)
                combined_state = np.dot(gate.matrix, combined_state)
                self._set_combined_state(qubit_indices, combined_state)

    def _get_combined_state(self, qubit_indices):
        combined_state = self.qubits[qubit_indices[0]].state
        for i in qubit_indices[1:]:
            combined_state = np.kron(combined_state, self.qubits[i].state)
        return combined_state

    def _set_combined_state(self, qubit_indices, combined_state):
        for i, qubit in enumerate(qubit_indices):
            self.qubits[qubit].state = combined_state[2 * i:2 * (i + 1)]

    def measure_all(self):
        # Here you would implement the measurement logic.
        measurements = []
        for qubit in self.qubits:
            # Assume each qubit has a method `measure()` that returns its measurement result
            measurement = qubit.measure()  # This method needs to be defined in the Qubit class
            measurements.append(measurement)
        return measurements
    def __repr__(self):
        """String representation of the circuit."""
        circuit_str = f"Quantum Circuit with {self.num_qubits} qubits:\n"
        for gate, qubits in self.gates:
            circuit_str += f"Gate: {gate} on qubits {qubits}\n"
        return circuit_str

