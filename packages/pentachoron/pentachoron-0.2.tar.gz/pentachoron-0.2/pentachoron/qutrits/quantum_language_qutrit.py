# quantum_language.py
from .circuit_qutrit import QuantumCircuit
from .gates_qutrit import QuantumGate, CNOTGate,  ControlledGate

class QuantumLanguage:
    def __init__(self):
        self.circuit = None

    def create_circuit(self, num_qutrits):
        self.circuit = QuantumCircuit(num_qutrits)

    def add_phase_gate(self, qutrit_index):
        self.circuit.add_gate(QuantumGate.phase_gate(theta = 0), [qutrit_index])

    def add_cycle_gate(self, qutrit_index):
        self.circuit.add_gate(QuantumGate.cycle_gate(), [qutrit_index])

    def add_cnot(self, control_index, target_index):
        self.circuit.add_gate(CNOTGate(), [control_index, target_index])


    def add_controlled_gate(self, control_index, target_index, gate):
        controlled_gate = ControlledGate(self.circuit.qutrits[control_index], self.circuit.qutrits[target_index], gate)
        self.circuit.add_gate(controlled_gate, [control_index, target_index])

    def execute(self):
        return self.circuit.execute()

    def measure_all(self):
        return self.circuit.measure_all()

    def visualize(self):
        for gate, qutrits in self.circuit.gates:
            qutrit_str = ', '.join(str(q) for q in qutrits)
            print(f"Gate: {gate.__class__.__name__}, Applied to Qutrit(s): {qutrit_str}")