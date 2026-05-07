"""
cross_check.py — Cross-validation between compressed/seed.py and modular/{physics,production}.py

Verifies that shared computations give identical results in both codebases.
Run from the compressed/ directory.
"""
import sys
import os
import numpy as np

# Add modular directory to path for imports
modular_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, modular_dir)

# Import from compressed seed
import seed as compressed

# Import from modular
from production import Production
from physics import (
    _seed_constants, pmns_mixing, koide_delta,
    bell_test_optimal, bell_test_framework
)


def cross_check():
    """Compare shared computations between compressed and modular."""
    results = []

    # --- Get modular values ---
    d_m, N_c_m, disc_m, pk_m, dg_m, phi_m, phi_bar_m, alpha_S_m, beta_KMS_m = _seed_constants()

    prod = Production()
    prod_data = prod.derive()

    # --- 1. alpha_S ---
    alpha_S_compressed = compressed.alpha_S
    alpha_S_modular = prod_data['alpha_S']
    match = np.allclose(alpha_S_compressed, alpha_S_modular)
    results.append(('alpha_S', alpha_S_compressed, alpha_S_modular, match))

    # --- 2. disc ---
    disc_compressed = compressed.disc
    disc_modular = disc_m
    match = disc_compressed == disc_modular
    results.append(('disc', disc_compressed, disc_modular, match))

    # --- 3. PMNS angles ---
    s13_c, s12_c, s23_c = compressed.pmns_angles()
    pmns_m = pmns_mixing()
    s13_m = pmns_m['sin2_13']
    s12_m = pmns_m['sin2_12']
    s23_m = pmns_m['sin2_23']
    match_13 = np.allclose(s13_c, s13_m)
    match_12 = np.allclose(s12_c, s12_m)
    match_23 = np.allclose(s23_c, s23_m)
    results.append(('PMNS sin2_13', s13_c, s13_m, match_13))
    results.append(('PMNS sin2_12', s12_c, s12_m, match_12))
    results.append(('PMNS sin2_23', s23_c, s23_m, match_23))

    # --- 4. Koide delta ---
    koide_c = compressed.koide_delta()
    koide_m = koide_delta()
    delta_c = koide_c['delta']
    delta_m = koide_m['delta_framework']
    match = np.allclose(delta_c, delta_m)
    results.append(('Koide delta', delta_c, delta_m, match))

    # --- 5. Bell test S_optimal ---
    bt_c = compressed.bell_test()
    S_opt_c = bt_c['S_optimal']
    S_opt_m = bell_test_optimal()
    match = np.allclose(S_opt_c, S_opt_m)
    results.append(('Bell S_optimal', S_opt_c, S_opt_m, match))

    # --- 6. Tower ker/A at depths 0-2 ---
    tower_c = compressed.tower_invariants(2)
    for depth_info in tower_c:
        dep = depth_info['depth']
        ker_frac_c = depth_info['ker_frac']
        # Modular: use algebra.py ker_im_decomposition on tower matrices
        from algebra import ker_im_decomposition
        tower_mats = compressed.build_tower(2)
        s_d = tower_mats[dep][0]
        _, _, k_dim_m, _ = ker_im_decomposition(s_d)
        dim_A = s_d.shape[0] ** 2
        ker_frac_m = k_dim_m / dim_A
        match = np.allclose(ker_frac_c, ker_frac_m)
        results.append((f'ker/A depth {dep}', ker_frac_c, ker_frac_m, match))

    # --- Report ---
    print("\n  CROSS-VALIDATION: compressed/seed.py vs modular/")
    print("  " + "=" * 60)
    all_pass = True
    for name, val_c, val_m, ok in results:
        status = "+" if ok else "FAIL"
        if not ok:
            all_pass = False
        print(f"  {status} {name}: compressed={val_c}, modular={val_m}")

    print("  " + "-" * 60)
    n_pass = sum(1 for _, _, _, ok in results if ok)
    n_total = len(results)
    print(f"  {'ALL MATCH' if all_pass else 'DISCREPANCIES FOUND'}: {n_pass}/{n_total}")
    return all_pass


if __name__ == "__main__":
    success = cross_check()
    sys.exit(0 if success else 1)
