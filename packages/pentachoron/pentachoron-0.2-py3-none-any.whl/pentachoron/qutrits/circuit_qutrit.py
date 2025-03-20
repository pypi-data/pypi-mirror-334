import numpy as np
from .Qutrit import Qutrit
from .gates_qutrit import QuantumGate, CNOTGate, ControlledGate
import random

class QuantumCircuit:
    def __init__(self, num_qutrits):
        self.num_qutrits = num_qutrits
        self.qutrits = [Qutrit(i) for i in range(num_qutrits)]
        self.gates = []

    def add_gate(self, gate, qutrit_indices):
        self.gates.append((gate, qutrit_indices))

    def execute(self):
        for gate, qutrit_indices in self.gates:
            if isinstance(gate, QuantumGate) and len(qutrit_indices) == 1:
                self.qutrits[qutrit_indices[0]].apply_gate(gate)
            elif isinstance(gate, CNOTGate):
                gate.apply_to(self.qutrits[qutrit_indices[0]], self.qutrits[qutrit_indices[1]])
            elif isinstance(gate, ControlledGate):
                gate.apply_to()  # You should define how controlled gates are applied
            else:
                combined_state = self._get_combined_state(qutrit_indices)
                combined_state = np.dot(gate.matrix, combined_state)
                self._set_combined_state(qutrit_indices, combined_state)

    def _get_combined_state(self, qutrit_indices):
        combined_state = self.qutrits[qutrit_indices[0]].state
        for i in qutrit_indices[1:]:
            combined_state = np.kron(combined_state, self.qutrits[i].state)
        return combined_state

    def _set_combined_state(self, qutrit_indices, combined_state):
        for i, qutrit in enumerate(qutrit_indices):
            self.qutrits[qutrit].state = combined_state[3 * i:3 * (i + 1)]

    def measure_all(self):
        # Here you would implement the measurement logic.
        measurements = []
        for qutrit in self.qutrits:
            # Assume each qubit has a method `measure()` that returns its measurement result
            measurement = qutrit.measure()  # This method needs to be defined in the Qubit class
            measurements.append(measurement)
        return measurements
    def __repr__(self):
        """String representation of the circuit."""
        circuit_str = f"Quantum Circuit with {self.num_qutrits} qutrits:\n"
        for gate, qutrits in self.gates:
            circuit_str += f"Gate: {gate} on qutrits {qutrits}\n"
        return circuit_str

