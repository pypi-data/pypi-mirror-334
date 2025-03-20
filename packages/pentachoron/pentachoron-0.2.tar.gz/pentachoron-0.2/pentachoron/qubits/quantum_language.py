# quantum_language.py
from .circuit import QuantumCircuit
from .gates import QuantumGate, CNOTGate, PhaseGate, TGate, ControlledGate

class QuantumLanguage:
    def __init__(self):
        self.circuit = None

    def create_circuit(self, num_qubits):
        self.circuit = QuantumCircuit(num_qubits)

    def add_hadamard(self, qubit_index):
        self.circuit.add_gate(QuantumGate.hadamard(), [qubit_index])

    def add_pauli_x(self, qubit_index):
        self.circuit.add_gate(QuantumGate.pauli_x(), [qubit_index])

    def add_cnot(self, control_index, target_index):
        self.circuit.add_gate(CNOTGate(), [control_index, target_index])

    def add_phase(self, qubit_index, theta):
        self.circuit.add_gate(PhaseGate(theta), [qubit_index])

    def add_t(self, qubit_index):
        self.circuit.add_gate(TGate(), [qubit_index])

    def add_controlled_gate(self, control_index, target_index, gate):
        controlled_gate = ControlledGate(self.circuit.qubits[control_index], self.circuit.qubits[target_index], gate)
        self.circuit.add_gate(controlled_gate, [control_index, target_index])

    def execute(self):
        return self.circuit.execute()

    def measure_all(self):
        return self.circuit.measure_all()

    def visualize(self):
        for gate, qubits in self.circuit.gates:
            qubit_str = ', '.join(str(q) for q in qubits)
            print(f"Gate: {gate.__class__.__name__}, Applied to Qubit(s): {qubit_str}")
