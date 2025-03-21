import numpy as np
import scipy.linalg
from numpy.linalg import norm


I = np.array([[1, 0], [0, 1]], dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
H = np.array([[1,  1], [1, -1]], dtype=complex) / np.sqrt(2)
S = np.array([[1, 0], [0, 1j]], dtype=complex)
T = np.array([[1, 0], [0, np.exp(1j * np.pi/4)]], dtype=complex)

def Rx(theta):

    return np.array([[np.cos(theta/2), -1j*np.sin(theta/2)],
                     [-1j*np.sin(theta/2), np.cos(theta/2)]], dtype=complex)

def Ry(theta):

    return np.array([[np.cos(theta/2), -np.sin(theta/2)],
                     [np.sin(theta/2),  np.cos(theta/2)]], dtype=complex)

def Rz(theta):

    return np.array([[np.exp(-1j*theta/2), 0],
                     [0, np.exp(1j*theta/2)]], dtype=complex)

def tensor(*args):

    result = np.array([1], dtype=complex)
    for op in args:
        result = np.kron(result, op)
    return result


def partial_trace(rho, keep, dims):

    num = len(dims)
    trace_over = [i for i in range(num) if i not in keep]
    reshaped_rho = rho.reshape([d for d in dims] * 2)
    for i in sorted(trace_over, reverse=True):
        reshaped_rho = np.trace(reshaped_rho, axis1=i, axis2=i+len(dims))
    final_shape = np.prod([dims[i] for i in keep])
    return reshaped_rho.reshape((final_shape, final_shape))

def fidelity(rho, sigma):

    sqrt_rho = scipy.linalg.sqrtm(rho)
    product = sqrt_rho @ sigma @ sqrt_rho
    sqrt_product = scipy.linalg.sqrtm(product)
    return np.real(np.trace(sqrt_product))**2

# ---------------------------
# Qubit
# ---------------------------
class Qubit:

    def __init__(self, state=None, use_density=False):
        self.use_density = use_density
        if state is None:
            # حالت اولیه |0>
            state = np.array([1, 0], dtype=complex)
        else:
            state = np.array(state, dtype=complex)
            state = state / norm(state)
        if use_density:
            self.state = np.outer(state, np.conjugate(state))
        else:
            self.state = state

    def apply_gate(self, gate):

        if self.use_density:
            self.state = gate @ self.state @ np.conjugate(gate.T)
        else:
            self.state = gate @ self.state

    def measure(self):

        if self.use_density:
            probabilities = np.real(np.diag(self.state))
            outcome = np.random.choice(len(probabilities), p=probabilities)
            proj = np.zeros((2,2), dtype=complex)
            proj[outcome, outcome] = 1.0
            self.state = proj
            return outcome
        else:
            probabilities = np.abs(self.state) ** 2
            outcome = np.random.choice(len(probabilities), p=probabilities)
            new_state = np.zeros_like(self.state)
            new_state[outcome] = 1.0
            self.state = new_state
            return outcome

    def __repr__(self):
        return f"Qubit(state={self.state}, use_density={self.use_density})"

# ---------------------------
# QuantumCircuit
# ---------------------------
class QuantumCircuit:

    def __init__(self, num_qubits, use_density=False):
        self.num_qubits = num_qubits
        self.use_density = use_density
        if use_density:
            psi = np.zeros(2**num_qubits, dtype=complex)
            psi[0] = 1.0
            self.state = np.outer(psi, np.conjugate(psi))
        else:
            self.state = np.zeros(2**num_qubits, dtype=complex)
            self.state[0] = 1.0

    def apply_gate(self, gate, targets):

        if isinstance(targets, int):
            targets = [targets]
        operator = None
        for i in range(self.num_qubits):
            op = gate if i in targets else I
            operator = op if operator is None else np.kron(operator, op)
        if self.use_density:
            self.state = operator @ self.state @ np.conjugate(operator.T)
        else:
            self.state = operator @ self.state

    def apply_controlled_gate(self, gate, control, target):

        dim = 2**self.num_qubits
        if not self.use_density:
            new_state = np.zeros(dim, dtype=complex)
            for i in range(dim):
                if (i >> (self.num_qubits - 1 - control)) & 1:
                    bits = [(i >> (self.num_qubits - 1 - j)) & 1 for j in range(self.num_qubits)]
                    for b in [0, 1]:
                        new_bits = bits.copy()
                        new_bits[target] = b
                        new_index = 0
                        for bit in new_bits:
                            new_index = (new_index << 1) | bit
                        new_state[new_index] += gate[b, bits[target]] * self.state[i]
                else:
                    new_state[i] += self.state[i]
            self.state = new_state
        else:
            operator = np.zeros((dim, dim), dtype=complex)
            for i in range(dim):
                bits = [(i >> (self.num_qubits - 1 - j)) & 1 for j in range(self.num_qubits)]
                if bits[control] == 1:
                    for b in [0, 1]:
                        new_bits = bits.copy()
                        new_bits[target] = b
                        j = 0
                        for bit in new_bits:
                            j = (j << 1) | bit
                        operator[j, i] += gate[b, bits[target]]
                else:
                    operator[i, i] += 1
            self.state = operator @ self.state @ np.conjugate(operator.T)

    def apply_noise_channel(self, channel, targets=None):

        if targets is None:
            targets = list(range(self.num_qubits))
        if isinstance(targets, int):
            targets = [targets]
        operator = None
        for i in range(self.num_qubits):
            op = channel if i in targets else I
            operator = op if operator is None else np.kron(operator, op)
        if self.use_density:
            self.state = operator @ self.state @ np.conjugate(operator.T)
        else:
            psi = self.state
            self.state = np.outer(psi, np.conjugate(psi))
            self.state = operator @ self.state @ np.conjugate(operator.T)

    def measure(self, targets=None):
        if targets is None:
            targets = list(range(self.num_qubits))
        if self.use_density:
            probabilities = np.real(np.diag(self.state))
            outcome_index = np.random.choice(len(probabilities), p=probabilities)
            proj = np.zeros_like(self.state)
            proj[outcome_index, outcome_index] = 1.0
            self.state = proj
            return format(outcome_index, '0{}b'.format(self.num_qubits))
        else:
            probabilities = np.abs(self.state) ** 2
            outcome_index = np.random.choice(len(probabilities), p=probabilities)
            new_state = np.zeros_like(self.state)
            new_state[outcome_index] = 1.0
            self.state = new_state
            return format(outcome_index, '0{}b'.format(self.num_qubits))

    def __repr__(self):
        return f"QuantumCircuit(num_qubits={self.num_qubits}, use_density={self.use_density}, state=\n{self.state})"


def amplitude_damping_channel(gamma):

    K0 = np.array([[1, 0], [0, np.sqrt(1-gamma)]], dtype=complex)
    K1 = np.array([[0, np.sqrt(gamma)], [0, 0]], dtype=complex)
    return [K0, K1]

def phase_damping_channel(gamma):

    K0 = np.sqrt(1-gamma) * I
    K1 = np.sqrt(gamma) * np.array([[1, 0], [0, 0]], dtype=complex)
    K2 = np.sqrt(gamma) * np.array([[0, 0], [0, 1]], dtype=complex)
    return [K0, K1, K2]

def apply_kraus_operators(rho, kraus_ops):

    new_rho = np.zeros_like(rho)
    for K in kraus_ops:
        new_rho += K @ rho @ np.conjugate(K.T)
    return new_rho

def K_operator(num_qubits, K):

    op = None
    for _ in range(num_qubits):
        op = np.kron(op, K) if op is not None else K
    return op

def operator_on_targets(num_qubits, K, targets):

    op = None
    for i in range(num_qubits):
        current = K if i in targets else I
        op = current if op is None else np.kron(op, current)
    return op

# ---------------------------
# AdvancedQuantumCircuit
# ---------------------------
class AdvancedQuantumCircuit(QuantumCircuit):
    def apply_noise_kraus(self, kraus_ops, targets=None):

        if targets is None:
            # اعمال به کل مدار
            if self.use_density:
                new_state = np.zeros_like(self.state)
                for K in kraus_ops:
                    op = K_operator(self.num_qubits, K)
                    new_state += op @ self.state @ np.conjugate(op.T)
                self.state = new_state
            else:
                psi = self.state
                self.state = np.outer(psi, np.conjugate(psi))
                new_state = np.zeros_like(self.state)
                for K in kraus_ops:
                    op = K_operator(self.num_qubits, K)
                    new_state += op @ self.state @ np.conjugate(op.T)
                self.state = new_state
        else:
            if isinstance(targets, int):
                targets = [targets]
            if self.use_density:
                new_state = np.zeros_like(self.state)
                for K in kraus_ops:
                    op = operator_on_targets(self.num_qubits, K, targets)
                    new_state += op @ self.state @ np.conjugate(op.T)
                self.state = new_state
            else:
                psi = self.state
                self.state = np.outer(psi, np.conjugate(psi))
                new_state = np.zeros_like(self.state)
                for K in kraus_ops:
                    op = operator_on_targets(self.num_qubits, K, targets)
                    new_state += op @ self.state @ np.conjugate(op.T)
                self.state = new_state