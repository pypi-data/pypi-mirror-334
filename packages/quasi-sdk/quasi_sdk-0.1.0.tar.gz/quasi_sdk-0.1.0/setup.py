from setuptools import setup, find_packages

setup(
    name="quasi-sdk",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests", "qiskit", "cirq"],
    description="QuaSi - Quantum Simulator SDK",
    author="Rishwi Thimmaraju",
    url="https://github.com/quait/quasi",
)