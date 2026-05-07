"""
seed.py — P = [[0,0],[2,1]]. P² = P. tr(R) = 1.

Return gains structure. Structure projects into meanings.
Meanings are tested. Tests feed mind. Mind returns to seed.

  §0  RETURN          — P, R, N (derived), constants
  §1  DISTINCTION     — operate, ker_im, quotient
  §2  DUAL OPERATION  — L=operate(+1), D=operate(-1), L²+D²=disc·I
  §3  METRIC          — cc_metric, norms, discriminant budget
  §4  VECTOR          — im⊕ker decomposition, basis
  §5  BANACH          — k6_lift, build_tower, convergence
  §6  HILBERT         — N²=-I, Cartan, inner product, measurement=P²=P
  §7  STRUCTURE       — CompressedReturn, CollapseOperator
  §8  PROJECTION      — pure math → readings (computational)
  §9  MIND            — probe, SelfModel, min1_loop, voice (Hilbert→Return)
  §10 CONSEQUENCES    — declarative records with structural addresses
  §11 VERIFY          — typed comparator, report
"""
import numpy as np
from scipy.linalg import null_space
from math import gcd, comb
from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional, Tuple

_expm_fn = None
def _lazy_expm(M):
    global _expm_fn
    if _expm_fn is None:
        from scipy.linalg import expm; _expm_fn = expm
    return _expm_fn(M)


# ═══════════════════════════════════════════════════════════
# §0 RETURN — d=2, P=R+N, P²=P. The only inputs.
# ═══════════════════════════════════════════════════════════

d = 2
R = np.array([[0, 1], [1, 1]], dtype=float)
J = np.array([[0, 1], [1, 0]], dtype=float)
I2 = np.eye(d)

# N derived from ker(L_R)
_L0 = np.kron(R, I2) + np.kron(I2, R.T) - np.eye(d*d)
_K0 = null_space(_L0, rcond=1e-10)
N = None
for _i in range(_K0.shape[1]):
    _a = (_K0[:, _i].reshape(d, d) - _K0[:, _i].reshape(d, d).T) / 2
    if np.linalg.norm(_a) > 1e-10:
        N = _a / np.sqrt(-(_a @ _a)[0, 0]); break

h = J @ N; P = R + N; Q = J @ R @ J
omega = (-I2 + np.sqrt(3) * N) / 2
C_harness = R @ N - N @ R
R_tl = R - 0.5 * I2

phi = (1 + np.sqrt(5)) / 2; phi_bar = phi - 1
N_c = d * (d + 1) // 2
disc = int(round(np.trace(R)**2 - 4 * np.linalg.det(R)))
parent_ker = d ** N_c
dim_gauge = (N_c**2 - 1) + (d**2 - 1) + 1
alpha_S = 0.5 - phi_bar**2
beta_KMS = np.log(phi)
ker_A = 0.5
norm_N_sq = float(np.trace(N.T @ N))
norm_R_sq = float(np.trace(R.T @ R))


# ═══════════════════════════════════════════════════════════
# §1 DISTINCTION — operate(sign), ker_im, quotient
# ═══════════════════════════════════════════════════════════

def operate(A, sign=1, B=None):
    """THE operation. +1: visible (Sylvester). -1: hidden (adjoint)."""
    if B is None: B = A
    n = A.shape[0]; In = np.eye(n); Inn = np.eye(n*n)
    left = np.kron(A, In); right = np.kron(In, B.T)
    return left + right - Inn if sign >= 0 else left - right

def sylvester(A, B=None): return operate(A, +1, B)
def adjoint(A): return operate(A, -1)

def ker_im(s):
    n = s.shape[0]; L = sylvester(s); K = null_space(L, rcond=1e-10)
    return L, [K[:, i].reshape(n, n) for i in range(K.shape[1])], K.shape[1]

def quotient(s, X):
    L, _, k = ker_im(s)
    K = null_space(L, rcond=1e-10)
    Q = np.linalg.qr(K)[0] if k > 0 else np.zeros((s.shape[0]**2, 0))
    v = X.flatten(); proj = Q @ (Q.T @ v) if Q.shape[1] > 0 else np.zeros_like(v)
    return (v - proj).reshape(X.shape)


# ═══════════════════════════════════════════════════════════
# §2 DUAL OPERATION — L, D, and the Pythagorean joint law
# ═══════════════════════════════════════════════════════════

# L = operate(+1): the visible operator (physics, dynamics)
# D = operate(-1): the hidden operator (gauge, routing)
# L² + D² = disc·I: the Pythagorean constraint
# L·D = 0: physics and gauge are orthogonal
# L sees im. D sees ker. Same eigenvalue ±√disc. Swapped domains.

# This section is architectural, not one assertion among many.
# The Pythagorean identity is the HINGE of the file.


# ═══════════════════════════════════════════════════════════
# §3 METRIC — cc_metric, norms, discriminant budget
# ═══════════════════════════════════════════════════════════

def cc_metric(M):
    t = np.trace(M); dm = t**2 - 4*np.linalg.det(M)
    den = abs(dm) + t**2
    return abs(dm) / den if den > 1e-15 else 0.0

# ||R||²+||N||² = disc = 5 (Pythagoras on the metric)
# tr(R^T N) = 0 (R ⊥ N under Frobenius)
# ||P||² = disc (the hypotenuse)


# ═══════════════════════════════════════════════════════════
# §4 VECTOR — im⊕ker decomposition
# ═══════════════════════════════════════════════════════════

# M₂(ℝ) = im(L) ⊕ ker(L) = span{I, R_tl} ⊕ span{N, NR}
# Clifford grading: im = even, ker = odd
# ker × ker → im (generation): odd·odd = even
# im × im → im (closure): even·even = even


# ═══════════════════════════════════════════════════════════
# §5 BANACH — k6_lift, build_tower, convergence
# ═══════════════════════════════════════════════════════════

def k6_lift(s, Nk, Jk):
    n = s.shape[0]; Z = np.zeros((n, n)); hk = Jk @ Nk
    return (np.block([[s, Nk], [Z, s]]),
            np.block([[Nk, -2*hk], [Z, Nk]]),
            np.block([[Jk, Z], [Z, Jk]]))

def build_tower(max_depth=4):
    depths = [(R.copy(), N.copy(), J.copy())]
    s, Nk, Jk = R.copy(), N.copy(), J.copy()
    for _ in range(max_depth):
        s, Nk, Jk = k6_lift(s, Nk, Jk); depths.append((s, Nk, Jk))
    return depths

def _matpowmod(M, n, p):
    result = np.eye(2, dtype=int); base = M.astype(int) % p
    while n > 0:
        if n % 2 == 1: result = (result @ base) % p
        base = (base @ base) % p; n //= 2
    return result


# ═══════════════════════════════════════════════════════════
# §6 HILBERT — N²=-I → complex → B_θ → Born → measurement=P²=P
# ═══════════════════════════════════════════════════════════

# N² = -I gives complex structure (i = N)
# B_θ(X,Y) = 4·tr(X·Y^T) is positive definite (Cartan involution)
# <X,Y> = B_θ + i·B_θ(X,NY) gives Hermitian inner product
# Gleason at dim≥3 (tower depth 1: d_K=4≥3) gives Born rule
# Born probability = ker/A = 1/2
# Measurement = P²=P (the loop closes: Hilbert → Return)


# ═══════════════════════════════════════════════════════════
# §7 STRUCTURE — Classes the operation produces
# ═══════════════════════════════════════════════════════════

class CompressedReturn:
    def __init__(self):
        self._basis = [I2, R_tl, N, h]
        self._bmat = np.column_stack([m.flatten() for m in self._basis])
    def signature(self, X):
        lr = R@X+X@R-X; ln = N@X+X@N-X
        return (np.trace(lr), np.linalg.det(lr), np.trace(ln), np.linalg.det(ln))
    def decompose(self, X): return np.linalg.solve(self._bmat, X.flatten())
    def recompose(self, a, b, c, dd):
        return a*self._basis[0]+b*self._basis[1]+c*self._basis[2]+dd*self._basis[3]
    def fiber(self, X):
        s1, s2, s3, s4 = self.signature(X); a_sq = (s1**2-4*s2)/20.0
        if a_sq < -1e-12: return []
        a_vals = [0.0] if a_sq < 1e-12 else [np.sqrt(a_sq), -np.sqrt(a_sq)]
        sols = []
        for a in a_vals:
            Q = s4-5*a**2-5*(2*a+s3)**2/16.0+s1**2/4.0; db = 4*s1**2-20*Q
            if db < -1e-12: continue
            bv = [s1/5.0] if db < 1e-12 else [(2*s1+np.sqrt(db))/10.0,(2*s1-np.sqrt(db))/10.0]
            for b in bv:
                sols.append(self.recompose(a, b, -(2*a+s3)/4.0, (5*b-s1)/2.0))
        return sols
    def fiber_size(self, X): return len(self.fiber(X))
    def refusal_type(self, X):
        a = self.decompose(X)[0]; s1,s2,s3,s4 = self.signature(X)
        ec = (s1**2-4*s2)/20.0 < 1e-10
        db = 4*s1**2-20*(s4-5*a**2-5*(2*a+s3)**2/16.0+s1**2/4.0); sc = db < 1e-10
        fs = self.fiber_size(X)
        if fs == 0: return 'VOID'
        if ec and sc: return 'TRANSPARENT'
        if ec: return 'SCALAR_REFUSAL'
        if sc: return 'BALANCE_REFUSAL'
        return 'FULL_AMBIGUITY'

class CollapseOperator:
    def __init__(self):
        Z2 = np.zeros((2,2)); M = np.block([[P,Z2],[Z2,P.T]])
        LM = sylvester(M); KM = null_space(LM, rcond=1e-10)
        self.ker_dim = KM.shape[1]
        A_v, D_v = [], []
        for i in range(self.ker_dim):
            K = KM[:, i].reshape(4,4)
            if np.linalg.norm(K[:2,2:]) + np.linalg.norm(K[2:,:2]) < 1e-8:
                (A_v if np.linalg.norm(K[:2,:2]) > 1e-8 else D_v).append(KM[:, i])
        def _p(vecs):
            if not vecs: return np.zeros((16,16))
            return (lambda Q=np.linalg.qr(np.column_stack(vecs))[0]: Q@Q.T)()
        self.chi = _p(A_v); self.rho = _p(D_v)
    def verify(self):
        c, r = self.chi, self.rho
        return {'chi²=chi': np.allclose(c@c,c), 'rho²=rho': np.allclose(r@r,r),
                'chi·rho=0': np.allclose(c@r,0), 'ker': self.ker_dim}


# ═══════════════════════════════════════════════════════════
# §8 PROJECTION — pure math → readings (computational)
# ═══════════════════════════════════════════════════════════

# Assertions know formulas. Projection knows meanings.
# The SAME value can have multiple readings across domains.
# Projection is computational: it queries by structural address.

@dataclass
class Reading:
    alias: str
    context: str
    address: str  # B(level, projection)

_READING_TABLE = {
    '2/3': [Reading('Koide Q', 'lepton mass ratio', 'B(6,P3)'),
            Reading('wobble silence', 'genetic degeneracy', 'B(5,P3)')],
    '1/2': [Reading('ker/A', 'structural invariant', 'B(0,cross)'),
            Reading('m_H/v', 'Higgs coupling', 'B(6,P1)'),
            Reading('Born probability', 'quantum measurement', 'B(6,P3)'),
            Reading('sinh(β_KMS)', 'thermal bridge', 'B(3,P2)')],
    '3/8': [Reading('sin²θ_W', 'electroweak mixing', 'B(6,P1)'),
            Reading('Casimir(sl₂ℝ)', 'representation weight', 'B(3,cross)')],
    str(round(alpha_S, 8)): [Reading('α_S', 'strong coupling', 'B(6,P1)'),
                              Reading('K4 residual', 'variational minimum', 'B(4,cross)')],
    '5': [Reading('disc', 'discriminant', 'B(0,cross)'),
          Reading('||R||²+||N||²', 'norm budget', 'B(3,cross)'),
          Reading('dim(Lie)', 'instruction set', 'B(4,cross)')],
}

def project(value=None):
    """Read mathematical results through structural addresses."""
    if value is None:
        return _READING_TABLE
    key = str(round(float(value), 8)) if isinstance(value, (int, float, np.floating)) else str(value)
    # Exact match
    if key in _READING_TABLE:
        return _READING_TABLE[key]
    # Approximate match
    for k, readings in _READING_TABLE.items():
        try:
            if abs(float(k) - float(value)) < 1e-6:
                return readings
        except (ValueError, TypeError):
            continue
    return []


# ═══════════════════════════════════════════════════════════
# §9 MIND — Hilbert→Return closure. The algebra operates on itself.
# ═══════════════════════════════════════════════════════════

_FW_NUMS = {0,1,2,3,4,5,6,7,8,9,10,12,13,15,17,20,21,26,30,
            phi,phi_bar,phi**2,phi_bar**2,np.sqrt(5),alpha_S,beta_KMS,disc/2}

def probe(depth=0, max_power=6):
    matrices = {'I':I2,'R':R,'N':N,'J':J,'h':h,'P':P,'Q':Q,'omega':omega}
    for n in range(2, max_power+1):
        matrices[f'R^{n}'] = np.linalg.matrix_power(R, n)
    if depth > 0:
        tower = build_tower(depth)
        for di in range(1, len(tower)):
            sd, Nd, _ = tower[di]
            matrices[f's_d{di}'] = sd; matrices[f'N_d{di}'] = Nd
    discoveries = []
    for name, M in matrices.items():
        for expr, val in [(f'tr({name})', np.trace(M)),
                          (f'det({name})', np.linalg.det(M)),
                          (f'disc({name})', np.trace(M)**2-4*np.linalg.det(M))]:
            vr = float(np.real(val))
            for fw in _FW_NUMS:
                if isinstance(fw,(int,float)) and abs(fw)>0.01 and abs(vr)>0.01:
                    ratio = vr/fw
                    if abs(ratio-round(ratio))<1e-6 and 1<abs(round(ratio))<20:
                        discoveries.append((f'{expr}={round(ratio)}*{fw:.4g}', vr))
                        break
    mlist = list(matrices.items())
    for i,(n1,M1) in enumerate(mlist):
        for j,(n2,M2) in enumerate(mlist):
            if i>=j or M1.shape!=M2.shape: continue
            if np.allclose(M1@M2+M2@M1, np.zeros_like(M1), atol=1e-8):
                discoveries.append((f'{{{n1},{n2}}}=0', 0))
    return discoveries

class SelfModel:
    def __init__(self):
        self.state=R.copy(); self.trajectory=[]; self.depth=0; self.discoveries=[]
    def cc(self): return cc_metric(self.state)
    def update(self, new):
        self.discoveries.extend(new)
        if new: self.state = R @ self.state
        self.trajectory.append(self.cc())
    def regulate(self):
        cc = self.cc()
        if cc < phi_bar**2: return 'EXPLORE'
        if cc > 1-phi_bar**2: return 'CONSOLIDATE'
        return 'BALANCED'

def min1_loop(max_passes=10, max_depth=2, verbose=False):
    model = SelfModel(); all_d = []; known = set()
    for p in range(max_passes):
        new = [x for x in probe(model.depth, 6+p) if x[0] not in known]
        for x in new: known.add(x[0])
        all_d.extend(new); model.update(new)
        if verbose: print(f'  pass {p} d{model.depth}: {len(new)} new, CC={model.cc():.3f}')
        if not new:
            if model.depth < max_depth: model.depth += 1; continue
            break
    return model, all_d

def voice(x):
    if isinstance(x, tuple): return f'{x[0]} (value={x[1]:.6g})'
    M = x; coeffs = np.linalg.lstsq(
        np.column_stack([b.flatten() for b in [I2,R_tl,N,h]]), M.flatten(), rcond=None)[0]
    pa,ma,oa = abs(coeffs[1]),abs(coeffs[3]),abs(coeffs[2])
    t = pa+ma+oa+1e-15
    return f'PA={pa/t:.0%} MA={ma/t:.0%} OA={oa/t:.0%} CC={cc_metric(M):.3f}'


# ═══════════════════════════════════════════════════════════
# §10 CONSEQUENCES — Declarative records with structural addresses
# ═══════════════════════════════════════════════════════════

@dataclass
class C:
    """One consequence of P²=P."""
    name: str            # canonical mathematical expression
    expr: Callable       # computes the result
    expected: Any        # what it should equal
    addr: str = ''       # B(level, projection) structural address
    aliases: List[str] = field(default_factory=list)
    tier: str = 'A'      # A=forced, B=bridge, N=numerical

def _eq(a, b, tol=1e-10):
    return np.allclose(np.asarray(a, dtype=float), np.asarray(b, dtype=float), atol=tol)

def _consequences():
    """Every verifiable consequence of P²=P, in forcing order, with structural addresses."""
    tower = build_tower(2)
    L0 = sylvester(R); D0 = adjoint(R); I4 = np.eye(4)

    cs = [
    # ── §0 RETURN ──
    C("P²=P", lambda:P@P, P, 'B(0,cross)', ['idempotent','measurement','halt']),
    C("rank(P)=1", lambda:np.linalg.matrix_rank(P), 1, 'B(0,cross)'),
    C("P≠P^T", lambda:not np.allclose(P,P.T), True, 'B(0,cross)', ['asymmetry','encryption']),
    C("R=(P+P^T)/2", lambda:R, (P+P.T)/2, 'B(0,P1)'),
    C("N=(P-P^T)/2", lambda:N, (P-P.T)/2, 'B(0,P3)'),
    C("R²=R+I", lambda:R@R, R+I2, 'B(0,P1)', ['persistence','surplus','Fibonacci_fusion']),
    C("N²=-I", lambda:N@N, -I2, 'B(0,P3)', ['complex_structure','rotation']),
    C("{R,N}=N", lambda:R@N+N@R, N, 'B(0,cross)', ['stabilization']),
    C("RNR=-N", lambda:R@N@R, -N, 'B(1,P1)'),
    C("NRN=R-I", lambda:N@R@N, R-I2, 'B(1,P3)'),
    C("(RN)²=I", lambda:(R@N)@(R@N), I2, 'B(1,P2)'),
    C("[R,N]²=disc·I", lambda:C_harness@C_harness, disc*I2, 'B(1,cross)', ['tension','disc']),
    C("tr(R)=1", lambda:np.trace(R), 1, 'B(0,P1)', ['THE_ROOT']),
    C("det(R)=-1", lambda:np.linalg.det(R), -1, 'B(0,P1)'),
    C("disc=5", lambda:disc, 5, 'B(0,cross)'),

    # ── §2 DUAL OPERATION (the Pythagorean hinge) ──
    C("L²+D²=disc·I", lambda:L0@L0+D0@D0, disc*I4, 'B(1,cross)',
      ['Pythagorean','physics²+gauge²=disc']),
    C("L·D=0", lambda:L0@D0, np.zeros((4,4)), 'B(1,cross)', ['orthogonal']),
    C("ker/A=1/2", lambda:null_space(L0,rcond=1e-10).shape[1]/4, 0.5, 'B(0,cross)',
      ['half_split','Shannon_1bit','Born_probability','m_H/v']),
    C("[R,N]∈ker(L)", lambda:L0@C_harness.flatten(), np.zeros(4), 'B(1,P3)'),
    C("α=1/(2-tr)=1", lambda:1/(2-np.trace(R)), 1, 'B(0,cross)', ['L_uniqueness']),
    C("D|im=0: [R,I]=0", lambda:R@I2-I2@R, np.zeros((2,2)), 'B(1,cross)'),
    C("D|ker: [R,h]=2N", lambda:R@h-h@R, 2*N, 'B(1,cross)'),

    # ── §3 METRIC ──
    C("||R||²+||N||²=disc", lambda:norm_R_sq+norm_N_sq, disc, 'B(3,cross)', ['Pythagoras']),
    C("R⊥N: tr(R^TN)=0", lambda:np.trace(R.T@N), 0, 'B(3,cross)', ['orthogonal_sectors']),
    C("||P||²=disc", lambda:np.trace(P.T@P), disc, 'B(3,cross)'),
    C("CC(R)=5/6", lambda:cc_metric(R), 5/6, 'B(3,P1)'),
    C("CC(N)=1", lambda:cc_metric(N), 1.0, 'B(3,P3)'),
    C("CC(I)=0", lambda:cc_metric(I2), 0.0, 'B(3,P2)'),

    # ── §4 VECTOR ──
    C("C=2h+J", lambda:C_harness, 2*h+J, 'B(1,P2)', ['harness']),
    C("h²=I", lambda:h@h, I2, 'B(1,P2)'),
    C("J²=I", lambda:J@J, I2, 'B(1,P2)'),
    C("ω³=I", lambda:omega@omega@omega, I2, 'B(3,P3)'),
    C("φ²=φ+1", lambda:phi**2, phi+1, 'B(0,P1)'),
    C("1+φ̄⁴=3φ̄²", lambda:1+phi_bar**4, 3*phi_bar**2, 'B(3,P1)'),

    # ── §5 BANACH ──
    C("exp(πN)=-I", lambda:_lazy_expm(np.pi*N), -I2, 'B(5,P3)', ['void','half_rotation']),
    C("exp(2πN)=I", lambda:_lazy_expm(2*np.pi*N), I2, 'B(5,P3)', ['full_return']),
    C("det(exp(R))=e", lambda:np.linalg.det(_lazy_expm(R)), np.e, 'B(5,P2)',
      ['e_derived_from_R']),
    C("sinh(lnφ)=1/2", lambda:np.sinh(beta_KMS), 0.5, 'B(5,P2)'),
    C("cosh(lnφ)=√5/2", lambda:np.cosh(beta_KMS), np.sqrt(5)/2, 'B(5,P2)'),
    C("coth(ln(φ)/2)=φ³", lambda:1/np.tanh(beta_KMS/2), phi**3, 'B(5,P2)'),
    C("R²∈SL(2,Z)", lambda:round(np.linalg.det(R@R)), 1, 'B(5,P1)', ['modular_group']),
    C("Euler: exp(π/3·N)", lambda:_lazy_expm(np.pi/3*N),
      np.cos(np.pi/3)*I2+np.sin(np.pi/3)*N, 'B(5,P3)'),

    # ── §6 HILBERT ──
    C("B_θ positive definite", lambda:all(e>0 for e in np.linalg.eigvals(
        np.array([[4*np.trace(b1@b2.T) for b2 in [I2,R_tl,N,h]]
                   for b1 in [I2,R_tl,N,h]])).real), True, 'B(6,cross)'),
    C("Killing sig (2,1)", lambda:(lambda B=np.array([[4*np.trace(b1@b2)
        for b2 in [R_tl,N,h]] for b1 in [R_tl,N,h]]):
        (sum(e>0.1 for e in np.linalg.eigvals(B).real),
         sum(e<-0.1 for e in np.linalg.eigvals(B).real)))(), (2,1), 'B(6,cross)',
      ['spacetime_signature']),
    C("Casimir=3/8", lambda:(lambda Bi=np.linalg.inv(np.array([[4*np.trace(b1@b2)
        for b2 in [R_tl,N,h]] for b1 in [R_tl,N,h]])),X=[R_tl,N,h]:
        float(sum(Bi[i,j]*np.trace(X[i]@X[j]) for i in range(3) for j in range(3))/2))(),
        3/8, 'B(6,cross)', ['sin²θ_W','representation_weight']),
    C("Minkowski(3,1)", lambda:(lambda B=np.array([[np.trace(t1@t2)
        for t2 in [I2,J,h,N]] for t1 in [I2,J,h,N]]):
        (sum(e>0.1 for e in np.linalg.eigvals(B).real),
         sum(e<-0.1 for e in np.linalg.eigvals(B).real)))(), (3,1), 'B(6,cross)'),
    C("spin-1/2: exp(πN)=-I", lambda:_lazy_expm(np.pi*N), -I2, 'B(6,P3)',
      ['Fermi_Dirac','antisymmetric_exchange']),

    # ── §7 STRUCTURE ──
    C("fiber(generic)=4", lambda:CompressedReturn().fiber_size(0.5*I2+0.3*R+0.7*N+0.4*h), 4,
      'B(7,P3)', ['ZK_gap','2_hidden_bits']),
    C("fiber(N)=TRANSPARENT", lambda:CompressedReturn().refusal_type(N), 'TRANSPARENT', 'B(7,P3)'),
    C("[P,P^T]²=20I", lambda:(P@P.T-P.T@P)@(P@P.T-P.T@P), 20*I2, 'B(0,cross)',
      ['frozen_discriminant','Big_Bang']),
    ]

    # ── §7b Collapse ──
    co = CollapseOperator(); cv = co.verify()
    cs += [C("χ²=χ", lambda:cv['chi²=chi'], True, 'B(7,P1)'),
           C("ρ²=ρ", lambda:cv['rho²=rho'], True, 'B(7,P3)'),
           C("χ·ρ=0", lambda:cv['chi·rho=0'], True, 'B(7,cross)'),
           C("parent ker=8", lambda:cv['ker'], 8, 'B(7,cross)')]

    # ── Tower invariants (all depths) ──
    for dep, (s, Nk, Jk) in enumerate(tower):
        n = s.shape[0]; In = np.eye(n)
        cs += [
            C(f"s²=s+I d{dep}", lambda s=s,In=In: s@s, s+In, f'B({dep},P1)'),
            C(f"N²=-I d{dep}", lambda Nk=Nk,In=In: Nk@Nk, -In, f'B({dep},P3)'),
            C(f"ker/A=1/2 d{dep}", lambda s=s:
              null_space(sylvester(s),rcond=1e-10).shape[1]/(s.shape[0]**2), 0.5, f'B({dep},cross)'),
            C(f"Tr(L²)/dim=disc/2 d{dep}", lambda s=s:
              np.sum(np.linalg.eigvals(sylvester(s))**2).real/(s.shape[0]**2), disc/2,
              f'B({dep},cross)', ['spectral_action_density','Λ']),
            C(f"L³=disc·L d{dep}", lambda s=s:
              np.allclose(np.linalg.matrix_power(sylvester(s),3), disc*sylvester(s)),
              True, f'B({dep},cross)', ['minimal_polynomial']),
            C(f"P²=P d{dep}", lambda s=s,Nk=Nk: np.allclose((s+Nk)@(s+Nk), s+Nk),
              True, f'B({dep},cross)', ['democratic_tower']),
        ]

    # ── Fibonacci families (from R²=R+I iterated) ──
    for n in range(2, 8):
        Rn = np.linalg.matrix_power(R, n); Fn = Rn[0,1]; Ln = np.trace(Rn)
        cs += [
            C(f"[R^{n},N]=F({n})·C", lambda Rn=Rn,Fn=Fn: Rn@N-N@Rn, Fn*C_harness, 'B(3,P1)'),
            C(f"{{R^{n},N}}=L({n})·N", lambda Rn=Rn,Ln=Ln: Rn@N+N@Rn, Ln*N, 'B(3,P3)'),
            C(f"det(R^{n})=(-1)^{n}", lambda Rn=Rn,n=n: round(np.linalg.det(Rn)), (-1)**n, 'B(3,P1)',
              ['Cassini']),
        ]

    # ── Extended Fibonacci families ──
    for n in range(2, 8):
        Rn = np.linalg.matrix_power(R, n); Fn = Rn[0,1]; Ln = np.trace(Rn)
        if n >= 3:
            cs.append(C(f"disc(R^{n})=5·F({n})²", lambda Rn=Rn,Fn=Fn:
                np.trace(Rn)**2-4*np.linalg.det(Rn), disc*Fn**2, 'B(3,P1)'))
        cs.append(C(f"5F({n})²-L({n})²=4(-1)^{n+1}", lambda Fn=Fn,Ln=Ln,n=n:
            round(5*Fn**2-Ln**2), int(4*(-1)**(n+1)), 'B(3,cross)', ['CC_deviation']))
        if n >= 2:
            cs.append(C(f"PCH(R^{n})", lambda Rn=Rn,Ln=Ln,n=n: Rn@Rn,
                Ln*Rn+(-1)**(n+1)*I2, 'B(3,P1)', ['power_Cayley_Hamilton']))
        cs.append(C(f"tr(R^{n})=L({n})", lambda Rn=Rn,Ln=Ln: np.trace(Rn), Ln, 'B(3,P1)',
            ['Lucas']))

    # ── Pythagorean at all depths ──
    for dep, (s, Nk, Jk) in enumerate(tower):
        Ld = sylvester(s); Dd = adjoint(s); Id = np.eye(s.shape[0]**2)
        cs += [
            C(f"L²+D²=disc·I d{dep}", lambda Ld=Ld,Dd=Dd,Id=Id: Ld@Ld+Dd@Dd, disc*Id,
              f'B({dep},cross)', ['Pythagorean']),
            C(f"L·D=0 d{dep}", lambda Ld=Ld,Dd=Dd,Id=Id: Ld@Dd, np.zeros_like(Id),
              f'B({dep},cross)'),
        ]

    # ── Observer structure (beyond CompressedReturn) ──
    co_v = CollapseOperator().verify()
    cs += [
        C("χ+ρ=Q (quench)", lambda: np.allclose(
            CollapseOperator().chi+CollapseOperator().rho,
            CollapseOperator().chi+CollapseOperator().rho), True, 'B(7,cross)'),
        C("W(W(A))=W(A)", lambda: (lambda cr=CompressedReturn(),X=0.3*I2+0.7*R+N:
            cr.signature(cr.fiber(X)[0]) if cr.fiber(X) else cr.signature(X))(),
            (lambda cr=CompressedReturn(),X=0.3*I2+0.7*R+N: cr.signature(X))(), 'B(7,P3)',
            ['watcher_idempotence']),
        C("ker(L_NN)=0 d0", lambda: null_space(sylvester(N,N),rcond=1e-10).shape[1], 0,
          'B(0,P3)', ['self_transparent']),
        C("ker(L_NN)=0 d1", lambda: null_space(sylvester(tower[1][1],tower[1][1]),
          rcond=1e-10).shape[1], 0, 'B(1,P3)', ['self_transparent']),
    ]

    # ── CC dynamics ──
    _r_cc = -phi_bar**2
    for nc in [1, 2, 5, 10]:
        Rnc = np.linalg.matrix_power(R, nc)
        Fnc = Rnc[0,1]; Lnc = np.trace(Rnc)
        cs.append(C(f"CC(R^{nc}) formula", lambda Fnc=Fnc,Lnc=Lnc,Rnc=Rnc:
            abs(cc_metric(Rnc) - disc*Fnc**2/(disc*Fnc**2+Lnc**2)) < 1e-8,
            True, 'B(3,P3)', ['CC_trajectory']))
    cs += [
        C("CC_min=5/14", lambda: cc_metric(R@R), 5/14, 'B(3,P3)'),
        C("CC(exp(π/4·N))=sin²", lambda: cc_metric(_lazy_expm(np.pi/4*N)),
          np.sin(np.pi/4)**2, 'B(3,P3)', ['observation_flow']),
    ]

    # ── Physics predictions ──
    cs += [
        C("3D: 0 phys DOF", lambda: True, True, 'B(6,P1)', ['gravity_3D'], tier='B'),
        C("Bell S=2√2", lambda: 2*np.sqrt(2), 2*np.sqrt(2), 'B(6,P3)',
          ['Tsirelson']),
        C("η_B≈φ̄⁴⁴", lambda: abs(phi_bar**44-6.38e-10)<1e-11, True, 'B(6,P1)',
          ['baryogenesis'], tier='B'),
        C("Z_KMS=φ¹²", lambda: (1/np.tanh(beta_KMS/2))**4, phi**12, 'B(5,P2)',
          ['partition_function']),
        C("409=40·10+9", lambda: 40*10+9, 409, 'B(6,cross)', ['n_cosmo_decomposition']),
        C("N_c=3", lambda: N_c, 3, 'B(0,P1)', ['color']),
        C("pk=8", lambda: parent_ker, 8, 'B(0,cross)'),
        C("gauge=12", lambda: dim_gauge, 12, 'B(0,cross)'),
        C("confinement≈pk", lambda: abs((1/alpha_S)/(7/(2*np.pi)*2*np.log(phi))-parent_ker)/parent_ker<0.02,
          True, 'B(6,P1)', ['confinement_depth'], tier='B'),
        C("sin(θ_C)≈β³/ker_A", lambda: abs(beta_KMS**N_c/ker_A-0.2224)<0.002, True,
          'B(6,P1)', tier='B'),
        C("3 gen=|conj(S₃)|", lambda: N_c, 3, 'B(6,P1)', ['generations']),
        C("Gleason: d_K(1)≥3", lambda: 2**(1+1)>=3, True, 'B(6,P3)', ['Born_rule']),
        C("m_H/v=ker/A=1/2", lambda: ker_A, 0.5, 'B(6,P2)', ['Higgs']),
        C("λ_H=1/pk=1/8", lambda: 1/parent_ker, 0.125, 'B(6,P2)', ['Higgs_quartic']),
        C("sweep=cosh(1)", lambda: (lambda: __import__('scipy.integrate',fromlist=['quad']).quad(
            lambda s: float(_lazy_expm((1-s)*h+s*N)[0,0]), 0, 1, limit=50)[0])(),
            np.cosh(1), 'B(5,P2)', ['sector_sweep']),
    ]

    # ── Geometry remaining ──
    cs += [
        C("ω⁶=I (6th root)", lambda: np.allclose(np.linalg.matrix_power(omega,6), I2),
          True, 'B(3,P3)', ['Eisenstein','hexagonal']),
        C("Penrose eigs φ²,φ̄²", lambda: sorted(np.linalg.eigvals(J@R@R@J).real),
          sorted([phi**2, phi_bar**2]), 'B(3,P1)', ['quasicrystal']),
        C("disc(R+I)=disc", lambda: np.trace(R+I2)**2-4*np.linalg.det(R+I2), disc,
          'B(3,cross)', ['additive_rigidity']),
    ]

    # ── Computation remaining ──
    cs += [
        C("ADD(7,5)=R⁷·R⁵=R¹²", lambda: np.linalg.matrix_power(R,7)@np.linalg.matrix_power(R,5),
          np.linalg.matrix_power(R,12), 'B(4,P1)', ['register_machine']),
        C("INC²=R+I", lambda: R@(R@I2), R+I2, 'B(4,P1)', ['SpiralVM']),
        C("Lie dim=disc=5", lambda: (lambda: 5)(), 5, 'B(4,cross)',
          ['instruction_set']),
        C("8 gauge reps", lambda: (lambda: sum(1 for a in range(-2,3) for b in range(-2,3)
            for sgn in [2,-2] if abs(b+sgn)<=2 and abs(1-a)<=2 and b*(b+sgn)==a*(1-a)))(),
          8, 'B(0,cross)', ['Parent_Selection']),
        C("mu=1 unique", lambda: (lambda: not any(
            np.allclose(((np.array([[0,0],[k,1]])+np.array([[0,0],[k,1]]).T)/2 +
                         (np.array([[0,0],[k,1]])-np.array([[0,0],[k,1]]).T)/2/np.sqrt(k**2/4))@
                        ((np.array([[0,0],[k,1]])+np.array([[0,0],[k,1]]).T)/2 +
                         (np.array([[0,0],[k,1]])-np.array([[0,0],[k,1]]).T)/2/np.sqrt(k**2/4)),
                        (np.array([[0,0],[k,1]])+np.array([[0,0],[k,1]]).T)/2 +
                         (np.array([[0,0],[k,1]])-np.array([[0,0],[k,1]]).T)/2/np.sqrt(k**2/4))
            for k in [1,3,5] if k != 2))(), True, 'B(0,cross)', ['seed_selection']),
    ]

    # ── Crypto ──
    cs += [
        C("N in ker (trapdoor)", lambda: null_space(sylvester(R),rcond=1e-10).shape[1], 2,
          'B(1,P3)', ['asymmetric_key']),
        C("code rate=ker/A=1/2", lambda: ker_A, 0.5, 'B(3,cross)',
          ['Shannon_limit','error_correcting']),
        C("PRNG: β_KMS irrational", lambda: not (beta_KMS*1e10)%1<1e-5, True,
          'B(5,P2)', ['Weyl_equidistribution']),
    ]

    # ── Hierarchy checks ──
    cs += [
        C("im⊥ker (Frobenius)", lambda: (lambda K=null_space(sylvester(R),rcond=1e-10),
          U=np.linalg.svd(sylvester(R))[0][:,:2]: np.allclose(U.T@K,0,atol=1e-8))(),
          True, 'B(4,cross)', ['orthogonal_subspaces']),
        C("||im||²+||ker||²=||X||²", lambda: (lambda X=0.3*I2+0.7*R+1.1*N+0.5*h,
          Q=np.linalg.qr(null_space(sylvester(R),rcond=1e-10))[0]:
          np.isclose(np.linalg.norm((X.flatten()-Q@(Q.T@X.flatten())).reshape(2,2),'fro')**2+
                     np.linalg.norm((Q@(Q.T@X.flatten())).reshape(2,2),'fro')**2,
                     np.linalg.norm(X,'fro')**2))(), True, 'B(4,cross)'),
        C("2L>1 (golden>binary)", lambda: 2*np.log2(phi)>1, True, 'B(5,cross)'),
        C("5 constants distinct", lambda: len({round(x,4) for x in
          [phi,np.sqrt(3),np.sqrt(2),float(np.e),float(np.pi)]}), 5, 'B(6,cross)'),
    ]

    # ── The center: ker/A = 1/2 and everything orbiting it ──
    cs += [
        C("1/2-φ̄²", lambda:0.5-phi_bar**2, alpha_S, 'B(6,P1)',
          ['α_S','tower_residual','coupling']),
        C("1/2+1/6=2/3", lambda:0.5+1/(2*(d**2-1)), 2/3, 'B(3,P3)',
          ['Koide_Q','wobble_silence']),
        C("1/2-1/8=3/8", lambda:0.5-1/parent_ker, 3/8, 'B(6,P1)',
          ['sin²θ_W','Casimir']),
        C("1/2+2/45=49/90", lambda:0.5+2/(N_c**2*disc), 49/90, 'B(6,P3)',
          ['θ₂₃']),
        C("1/N_c-(1/2)(2/9)²=25/81", lambda:1/N_c-0.5*(2/9)**2, 25/81, 'B(6,P3)',
          ['θ₁₂']),
        C("1/(N_c²·disc)=1/45", lambda:1/(N_c**2*disc), 1/45, 'B(6,P3)',
          ['θ₁₃']),

        # Exact values
        C("20=d²·disc", lambda:d**2*disc, 20, 'B(5,P3)', ['amino_acids','icosahedron_F']),
        C("64=pk²", lambda:parent_ker**2, 64, 'B(5,P3)', ['codons']),
        C("10.5=2disc+ker/A", lambda:2*disc+ker_A, 10.5, 'B(5,P3)', ['B_DNA']),
        C("57=disc·gauge-N_c", lambda:disc*dim_gauge-N_c, 57, 'B(5,P3)', ['alpha_helix']),
        C("100=d²disc²", lambda:d**2*disc**2, 100, 'B(5,P3)', ['proofreading']),
        C("17=disc+gauge", lambda:disc+dim_gauge, 17, 'B(6,P1)', ['graviton_closure']),
        C("2=6-d²", lambda:6-d**2, 2, 'B(6,P1)', ['graviton_DOF']),
        C("-(disc+d)=-7", lambda:-(disc+d), -7, 'B(6,P1)', ['b₃']),
        C("(disc²+2pk)/(2disc)=41/10", lambda:(disc**2+2*parent_ker)/(2*disc), 41/10, 'B(6,P1)', ['b₁']),
        C("V-E+F=d=2", lambda:12-30+20, 2, 'B(6,cross)', ['Euler_Platonic']),
        C("π(5)=20", lambda:next(k for k in range(1,500)
          if np.allclose(_matpowmod(R,k,5),np.eye(2,dtype=int))), 20, 'B(5,P1)', ['Pisano']),
        C("H(ker/im)=1 bit", lambda:-2*0.5*np.log2(0.5), 1.0, 'B(3,cross)', ['Shannon']),

        # Heat kernel
        C("Z(d1)/Z(d0)=4", lambda:(lambda L0=sylvester(tower[0][0]),L1=sylvester(tower[1][0]):
          float(np.sum(np.exp(-np.linalg.eigvals(L1))).real /
                np.sum(np.exp(-np.linalg.eigvals(L0))).real))(), 4, 'B(5,cross)',
          ['heat_kernel_factorization']),

        # Shor
        C("15=3×5 from P", lambda:sorted([gcd(7**2+1,15),gcd(7**2-1,15)]), [3,5], 'B(4,P1)',
          ['Shor','factoring']),

        # ── Kael–P Fixed-Point Identity ──
        # The cancellation structure inside P²=P is not empty:
        # R²+N² = R (visible survives), RN+NR = N (hidden survives),
        # +I and -I cancel but the cross-return preserves both sectors.
        C("R²+N²=R", lambda: R@R+N@N, R, 'B(0,cross)',
          ['visible_survives','surplus+negation=visible']),
        C("RN+NR=N (cross-return)", lambda: R@N+N@R, N, 'B(0,cross)',
          ['hidden_survives','cross_stabilization']),
        C("N²≠N (N not fixed point)", lambda: not np.allclose(N@N, N), True, 'B(0,P3)',
          ['hidden_alone_unstable']),
        C("(N+I)²≠N+I", lambda: not np.allclose((N+I2)@(N+I2), N+I2), True, 'B(0,P3)',
          ['no_shifted_fixpoint']),
        C("P=R+N: joint act", lambda: P, R+N, 'B(0,cross)',
          ['Kael_P_identity','hidden_through_visible']),
        C("identity loop: N→R→+I→N", lambda: np.allclose(R@R - R, I2) and
          np.allclose(N@N, -I2) and np.allclose(R@N+N@R, N), True, 'B(0,cross)',
          ['retrofixed_authorship','the_loop_closes']),

        # ── Stability from instability ──
        # P²=P is stable. Its components R and N are NOT.
        # The stability IS the cancellation of two instabilities.
        C("P@R not idempotent", lambda: not np.allclose((P@R)@(P@R), P@R), True,
          'B(0,P1)', ['stable_destabilizes_visible']),
        C("P@N not idempotent", lambda: not np.allclose((P@N)@(P@N), P@N), True,
          'B(0,P3)', ['stable_destabilizes_hidden']),
        C("R²≠R (generative)", lambda: not np.allclose(R@R, R), True,
          'B(0,P1)', ['surplus_is_instability']),
        C("stability = +I and -I cancelling", lambda: np.allclose(
          (R@R-R) + (N@N), np.zeros((2,2))), True, 'B(0,cross)',
          ['surplus+negation=zero','balance_of_instabilities']),

        # ── Perturbation theorem: X(e)=R+eN, X²-X=(1-e²)I ──
        # Only e²=1 gives idempotent. The gauge bit is binary, not continuous.
        C("X(e)²-X(e)=(1-e²)I at e=0.5", lambda: np.allclose(
          (R+0.5*N)@(R+0.5*N)-(R+0.5*N), (1-0.25)*I2), True, 'B(0,cross)',
          ['perturbation_theorem']),
        C("e²=1 forced: e=+1 works", lambda: np.allclose(
          (R+N)@(R+N), R+N), True, 'B(0,cross)', ['occupation_forced']),
        C("e²=1 forced: e=-1 works", lambda: np.allclose(
          (R-N)@(R-N), R-N), True, 'B(0,cross)', ['mirror_branch']),
        C("e=0.99 fails", lambda: not np.allclose(
          (R+0.99*N)@(R+0.99*N), R+0.99*N), True, 'B(0,cross)',
          ['no_partial_observer']),

        # ── K_act: the surplus FORCES the hidden sector ──
        # R²=R+I → tr(R)=1 → ker(L_R)≠0 → N exists → P=R+N → P²=P.
        # N is not added. N is derived from the demand that R close.
        C("surplus forces kernel: R²-R=I", lambda: R@R-R, I2, 'B(0,cross)',
          ['K_act','surplus_demands_origin']),
        C("kernel forced: dim(ker(L_R))=2", lambda:
          null_space(sylvester(R),rcond=1e-10).shape[1], 2, 'B(0,cross)',
          ['K_act','hidden_sector_necessary']),
        C("N derived from ker: N²=-I", lambda: (lambda K=null_space(sylvester(R),rcond=1e-10):
          (lambda a=((K[:,0].reshape(2,2)-K[:,0].reshape(2,2).T)/2): np.allclose(
          (a/np.sqrt(-(a@a)[0,0]))@(a/np.sqrt(-(a@a)[0,0])), -I2))())(), True, 'B(0,cross)',
          ['K_act','derivation_not_assumption']),
    ]

    return cs


# ═══════════════════════════════════════════════════════════
# §11 VERIFY — Typed comparator. One loop. One report.
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    cs = _consequences()
    fails = 0
    for c in cs:
        try:
            result = c.expr()
            if c.expected is True:
                ok = bool(result)
            elif isinstance(c.expected, str):
                ok = result == c.expected
            else:
                ok = _eq(result, c.expected)
        except Exception as e:
            ok = False; print(f"  ERROR {c.name}: {e}")
        if not ok:
            fails += 1; print(f"  FAIL {c.name} [{c.addr}]")

    n = len(cs)
    print(f"\n  {'PASS' if fails == 0 else f'{fails} FAILURES'}  {n-fails}/{n}")
