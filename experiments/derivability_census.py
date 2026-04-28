"""
derivability_census.py — How many framework expressions match SM constants?

Methodological test: enumerate all expressions of complexity <= 2
from the framework's generators {phi, phi_bar, 1/2, disc, integers}
and check how many land within 5% of known SM dimensionless constants.

If the framework's claimed identifications are forced, the number of
alternative expressions near each target should be LOW. If the framework
is just a flexible number-generator, it should be HIGH.

Result: 2.6x random baseline. Modest enrichment. The strongest claims
are structural (census-immune) or isolated-numerical (few alternatives).
The crowded-numerical claims require derivation-chain evaluation.
"""
import numpy as np

phi = (1 + np.sqrt(5)) / 2
phi_bar = phi - 1

# SM dimensionless constants (targets)
sm_constants = {
    "alpha_S": 0.1179,
    "alpha_em": 1/137.036,
    "sin2_tW_MZ": 0.2312,
    "sin2_tW_GUT": 0.375,
    "m_e/m_mu": 0.00484,
    "m_mu/m_tau": 0.0595,
    "m_u/m_t": 1.3e-5,
    "m_d/m_b": 1.1e-3,
    "m_s/m_b": 0.024,
    "m_c/m_t": 7.4e-3,
    "V_us": 0.2243,
    "V_cb": 0.0422,
    "V_ub": 0.00394,
    "Koide_Q": 0.6667,
    "m_H/v": 0.508,
    "eta_B": 6.12e-10,
    "m_p/Lambda_QCD": 4.47,
    "Omega_Lambda": 0.685,
    "Omega_m": 0.315,
}

# Generate all expressions of complexity <= 2
values = {}

# Level 0: primitives
for name, val in [("phi", phi), ("phi_bar", phi_bar), ("1/2", 0.5), ("disc", 5.0)]:
    values[name] = val
for n in range(1, 6):
    values[str(n)] = float(n)

# Level 1: powers
for base_name, base_val in [("phi", phi), ("phi_bar", phi_bar)]:
    for exp in range(-10, 40):
        if exp in (0, 1):
            continue
        val = base_val ** exp
        if 1e-15 < abs(val) < 1e15:
            values[f"{base_name}^{exp}"] = val

# Level 1b: combinations with 1/2 and disc
for name, val in list(values.items()):
    if abs(val) > 1e-10:
        values[f"1/2-{name}"] = 0.5 - val
        values[f"1/2+{name}"] = 0.5 + val
        values[f"1/2*{name}"] = 0.5 * val
        values[f"{name}/disc"] = val / 5
        values[f"disc*{name}"] = 5 * val

# Level 2: pairwise operations on base items
base = [("phi", phi), ("phi_bar", phi_bar), ("1/2", 0.5), ("disc", 5.0)]
base += [(f"phi^{n}", phi**n) for n in range(2, 8)]
base += [(f"phi_bar^{n}", phi_bar**n) for n in range(2, 8)]
for n1, v1 in base:
    for n2, v2 in base:
        if abs(v2) > 1e-10:
            values[f"({n1})/({n2})"] = v1/v2
        values[f"({n1})*({n2})"] = v1*v2
        values[f"({n1})+({n2})"] = v1+v2
        values[f"({n1})-({n2})"] = v1-v2

# Census
tolerance = 0.05
matches = {}
for expr_name, expr_val in values.items():
    if expr_val == 0 or not np.isfinite(expr_val):
        continue
    for sm_name, sm_val in sm_constants.items():
        if sm_val == 0:
            continue
        if abs(expr_val - sm_val) / abs(sm_val) < tolerance:
            matches.setdefault(sm_name, []).append(
                (expr_name, expr_val, abs(expr_val - sm_val) / abs(sm_val))
            )

# Report
print(f"Expressions: {len(values)}")
print(f"SM targets: {len(sm_constants)}")
print(f"Tolerance: {tolerance*100:.0f}%")
print()

total = 0
for sm_name in sorted(sm_constants):
    hits = sorted(matches.get(sm_name, []), key=lambda x: x[2])
    total += len(hits)
    best = f"{hits[0][0]}={hits[0][1]:.4g} ({hits[0][2]*100:.1f}%)" if hits else "none"
    print(f"  {sm_name:20s} = {sm_constants[sm_name]:12.4g}: {len(hits):3d} matches  best: {best}")

print(f"\nTotal matches: {total}")
print(f"Average per target: {total/len(sm_constants):.1f}")

# Random baseline
pos_vals = [v for v in values.values() if np.isfinite(v) and v > 0]
log_range = np.log10(max(pos_vals)) - np.log10(min(pos_vals))
accept = np.log10(1.05/0.95)
expected = len(pos_vals) * len(sm_constants) * accept / log_range
print(f"\nRandom baseline: {expected:.0f}")
print(f"Ratio actual/expected: {total/expected:.2f}x")
