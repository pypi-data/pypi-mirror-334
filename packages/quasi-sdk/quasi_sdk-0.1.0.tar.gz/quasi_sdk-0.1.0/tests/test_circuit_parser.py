from quasi.circuit_parser import CircuitParser
from qiskit import QuantumCircuit

def test_qiskit_parser():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    parser = CircuitParser()
    ir = parser.convert_to_ir(qc)
    assert ir["qubits"] == 2
    assert ir["gates"][0]["name"] == "H"
    assert ir["gates"][1]["name"] == "CX"