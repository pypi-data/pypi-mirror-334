from quasi.api import APIClient

def test_submit_circuit():
    api_client = APIClient(api_key="test_key")
    circuit_ir = {"qubits": 2, "gates": [{"name": "H", "qubits": [0]}]}
    job_id = api_client.submit_circuit(circuit_ir)
    assert job_id is not None