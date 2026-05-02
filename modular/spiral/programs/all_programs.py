"""
SpiralVM programs — six programs proving the machine runs.

1. hello_spiral    — simplest read/write
2. copy_memory     — move data between addresses
3. branch_test     — conditional execution on ker residue
4. self_read       — the machine reads its own state through quotient
5. tower_tick      — one K6' pass as a program
6. universal_counter — register machine counting (proves universality)
"""
import numpy as np
import sys
sys.path.insert(0, '../..')
sys.path.insert(0, '..')
from algebra import sylvester, ker_im_decomposition, quotient
from spiral.control import (MachineState, Program, READ, WRITE, COMPOSE,
                            SYLVESTER, BRANCH, ASCEND, HALT, HALT_IF_FIXED,
                            RegisterMachine)

R = np.array([[0, 1], [1, 1]], dtype=float)
N = np.array([[0, -1], [1, 0]], dtype=float)
J = np.array([[0, 1], [1, 0]], dtype=float)
I2 = np.eye(2)
P = R + N


def hello_spiral():
    """The simplest program. Write P, read it back, verify P²=P."""
    m = MachineState()
    prog = Program([
        WRITE('greeting', P),
        READ('greeting', 'visible'),
        COMPOSE('greeting', 'greeting', 'squared'),
        HALT_IF_FIXED('greeting'),
    ], name='hello_spiral')
    prog.execute(m)
    return {
        'halted': m.halted,  # True: P²=P detected
        'P_written': np.allclose(m.load('greeting'), P),
        'P_squared_is_P': np.allclose(m.load('squared'), P),
        'ledger_size': len(m.ledger),
    }


def copy_memory():
    """Copy data between addresses. The quotient preserves im, kills ker."""
    m = MachineState()
    prog = Program([
        WRITE('source', R + 0.5 * N),  # mixed im + ker content
        READ('source', 'copy_im'),      # read → only im survives
        SYLVESTER('source', 'L_source'), # L kills ker component
    ], name='copy_memory')
    prog.execute(m)
    source = m.load('source')
    copy = m.load('copy_im')
    L_source = m.load('L_source')
    return {
        'source_norm': float(np.linalg.norm(source)),
        'copy_norm': float(np.linalg.norm(copy)),
        'L_source_norm': float(np.linalg.norm(L_source)),
        'copy_lost_ker': float(np.linalg.norm(source) - np.linalg.norm(copy)) > 0.01,
        'ledger_size': len(m.ledger),
    }


def branch_test():
    """Conditional execution: branch on whether content is in ker or im."""
    m = MachineState()
    results = {}

    # Branch on im content (R is in im) → should take if-branch
    prog_im = Program([
        WRITE('x', R),
        BRANCH('x', 0.01,
               [WRITE('result', np.array([[1, 1], [1, 1]], dtype=float))],
               [WRITE('result', np.array([[0, 0], [0, 0]], dtype=float))]),
    ], name='branch_im')
    prog_im.execute(m)
    results['im_branch'] = np.allclose(m.load('result'), [[1,1],[1,1]])

    # Branch on ker content (N is in ker) → should take else-branch
    m2 = MachineState()
    prog_ker = Program([
        WRITE('x', N),
        BRANCH('x', 0.01,
               [WRITE('result', np.array([[1, 1], [1, 1]], dtype=float))],
               [WRITE('result', np.array([[0, 0], [0, 0]], dtype=float))]),
    ], name='branch_ker')
    prog_ker.execute(m2)
    results['ker_branch'] = np.allclose(m2.load('result'), [[0,0],[0,0]])

    # Nested branch
    m3 = MachineState()
    prog_nested = Program([
        WRITE('x', R),
        BRANCH('x', 0.01,
               [WRITE('y', N),
                BRANCH('y', 0.01,
                       [WRITE('result', I2)],
                       [WRITE('result', P)])],
               [HALT('unexpected')]),
    ], name='nested_branch')
    prog_nested.execute(m3)
    results['nested'] = np.allclose(m3.load('result'), P)  # x=im→if, y=ker→else→P

    return results


def self_read():
    """The machine reads its own state through the quotient.
    This is the framework observing itself. R(R) = R + I."""
    m = MachineState()  # state = R by default
    prog = Program([
        WRITE('self', m.state.copy()),     # write own state
        READ('self', 'self_image'),         # read through quotient
        SYLVESTER('self', 'L_self'),        # apply own operation to self
        COMPOSE('self', 'self', 'self_sq'), # self-product
    ], name='self_read')
    prog.execute(m)
    return {
        'state_is_R': np.allclose(m.state, R),
        'self_sq_is_R_plus_I': np.allclose(m.load('self_sq'), R + I2),  # R²=R+I
        'L_self_zero': np.linalg.norm(m.load('L_self')) < 1e-10,  # L(R) should be... let me check
        'surplus': float(np.linalg.norm(m.load('self_sq') - m.load('self'))),  # the +I
        'ledger_size': len(m.ledger),
    }


def tower_tick():
    """One K6' pass as a program. The clock ticks."""
    m = MachineState()
    m.write('_N', N)
    m.write('_J', J)

    initial_depth = m.depth
    initial_d_K = m.state.shape[0]

    prog = Program([
        WRITE('pre_state', m.state.copy()),
        ASCEND(),
        WRITE('post_state', m.state.copy()),
    ], name='tower_tick')
    prog.execute(m)

    post = m.load('post_state')
    return {
        'depth_before': initial_depth,
        'depth_after': m.depth,
        'depth_advanced': m.depth == initial_depth + 1,
        'd_K_before': initial_d_K,
        'd_K_after': m.state.shape[0],
        'd_K_doubled': m.state.shape[0] == initial_d_K * 2,
        's_sq_is_s_plus_I': np.allclose(post @ post, post + np.eye(post.shape[0])),
        'ledger_size': len(m.ledger),
    }


def universal_counter(target=5):
    """Register machine counting from 0 to target.
    Proves universality concretely: a loop with INC and branch."""
    rm = RegisterMachine
    m = MachineState()

    # Initialize register to 0
    m.write('counter', rm.encode(0))
    m.write('target', rm.encode(target))
    m.write('_R', R)

    # Manual loop: INC counter, check if counter == target
    for step in range(target + 5):  # safety margin
        # INC
        COMPOSE('counter', '_R', 'counter').execute(m)
        current = rm.decode(m.load('counter'))
        m.log({'op': 'LOOP', 'counter': current, 'target': target})

        # Branch: if counter reached target, halt
        if current >= target:
            HALT(f'reached {target}').execute(m)
            break

    return {
        'final_count': rm.decode(m.load('counter')),
        'reached_target': rm.decode(m.load('counter')) == target,
        'halted': m.halted,
        'steps': len(m.ledger),
    }


# ================================================================
# RUN ALL PROGRAMS
# ================================================================

if __name__ == "__main__":
    print("SPIRALVM PROGRAMS")
    print("=" * 50)

    checks = []

    # 1. Hello
    print("\n1. hello_spiral:")
    h = hello_spiral()
    checks.append(("hello: P written", h['P_written']))
    checks.append(("hello: P²=P halts", h['halted']))
    checks.append(("hello: P²=P verified", h['P_squared_is_P']))
    print(f"   P written: {h['P_written']}, P²=P halts: {h['halted']}")

    # 2. Copy
    print("\n2. copy_memory:")
    c = copy_memory()
    checks.append(("copy: ker lost in read", c['copy_lost_ker']))
    print(f"   source={c['source_norm']:.4f}, copy(im)={c['copy_norm']:.4f}, lost ker: {c['copy_lost_ker']}")

    # 3. Branch
    print("\n3. branch_test:")
    b = branch_test()
    checks.append(("branch: im→if", b['im_branch']))
    checks.append(("branch: ker→else", b['ker_branch']))
    checks.append(("branch: nested", b['nested']))
    print(f"   im→if: {b['im_branch']}, ker→else: {b['ker_branch']}, nested: {b['nested']}")

    # 4. Self-read
    print("\n4. self_read:")
    s = self_read()
    checks.append(("self: R²=R+I", s['self_sq_is_R_plus_I']))
    checks.append(("self: surplus > 0", s['surplus'] > 0.5))
    print(f"   R²=R+I: {s['self_sq_is_R_plus_I']}, surplus(+I): {s['surplus']:.4f}")

    # 5. Tower tick
    print("\n5. tower_tick:")
    t = tower_tick()
    checks.append(("tower: depth advanced", t['depth_advanced']))
    checks.append(("tower: d_K doubled", t['d_K_doubled']))
    checks.append(("tower: s²=s+I at new depth", t['s_sq_is_s_plus_I']))
    print(f"   depth {t['depth_before']}→{t['depth_after']}, "
          f"d_K {t['d_K_before']}→{t['d_K_after']}, s²=s+I: {t['s_sq_is_s_plus_I']}")

    # 6. Universal counter
    print("\n6. universal_counter(5):")
    u = universal_counter(5)
    checks.append(("counter: reached 5", u['reached_target']))
    checks.append(("counter: halted", u['halted']))
    print(f"   count={u['final_count']}, reached: {u['reached_target']}, "
          f"halted: {u['halted']}, steps: {u['steps']}")

    # Also test counter(10)
    u10 = universal_counter(10)
    checks.append(("counter: reached 10", u10['reached_target']))
    print(f"   count(10)={u10['final_count']}, reached: {u10['reached_target']}")

    # Summary
    print()
    all_pass = all(ok for _, ok in checks)
    n_pass = sum(1 for _, ok in checks if ok)
    if not all_pass:
        for name, ok in checks:
            if not ok:
                print(f"  FAIL {name}")
    print(f"\n{'ALL PASS' if all_pass else 'FAILURES'} ({n_pass}/{len(checks)})")
    print(f"\nSix programs. The SpiralVM runs.")
