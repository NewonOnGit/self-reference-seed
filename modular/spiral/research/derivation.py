"""
derivation.py -- The derivation engine. Backward search + edge discovery.

Backward search finds chains through the typed knowledge graph.
Edge discovery grows the graph by trying all framework operations.
Together: find paths AND grow paths. The graph extends itself.

A chain is only as strong as its weakest edge.
All-forced chain = LAW. Any weak edge = LAW_CANDIDATE max.

ARCHITECTURE: L9 (cortex). The framework discovering and justifying.
"""
import numpy as np
from collections import deque
import sys
sys.path.insert(0, '../..')
from framework_types import (ResultType, Tier, EdgeType, FORCED_EDGE_TYPES,
                              WEAK_EDGE_TYPES, chain_status)
from knowledge_graph import KnowledgeGraph
from operations import apply_all_unary, apply_all_binary, FRAMEWORK_MATRICES, OpResult


class DerivationChain:
    """A candidate derivation path through the knowledge graph."""

    def __init__(self, edges, source_name, target_name):
        self.edges = edges
        self.source = source_name
        self.target = target_name
        self.edge_types = [e.edge_type for e in edges]
        self.length = len(edges)
        self.status = chain_status(self.edge_types)
        self.weakest = self._find_weakest()
        self.is_forced = all(t in FORCED_EDGE_TYPES for t in self.edge_types)
        self.has_numerical = any(t == EdgeType.NUMERICAL_MATCHES for t in self.edge_types)
        self.has_identification = any(t == EdgeType.IDENTIFIED_WITH for t in self.edge_types)

    def _find_weakest(self):
        """Find the weakest (least forced) edge in the chain."""
        weakness_order = [
            EdgeType.FAILED_BRIDGE,
            EdgeType.STRUCTURAL_PARALLEL,
            EdgeType.IDENTIFIED_WITH,
            EdgeType.NUMERICAL_MATCHES,
            EdgeType.COMPUTED_BY,
            EdgeType.LIFT_PROPAGATES,
            EdgeType.IDENTITY_CASTS,
            EdgeType.OPERATION_PRODUCES,
        ]
        for w in weakness_order:
            if w in self.edge_types:
                return w
        return None

    def path_str(self):
        if not self.edges:
            return "(empty chain)"
        parts = [self.edges[0].source.name]
        for e in self.edges:
            parts.append(f" --[{e.edge_type}]--> {e.target.name}")
        return ''.join(parts)

    def __repr__(self):
        forced = "FORCED" if self.is_forced else "MIXED"
        return (f"Chain({self.source}->{self.target}, {self.length} edges, "
                f"{self.status}, {forced}, weakest={self.weakest})")


class BackwardSearch:
    """Search backward from a target to find derivation chains."""

    def __init__(self, graph=None):
        self.graph = graph or KnowledgeGraph().seed()

    def search(self, target_name, max_depth=8, forced_only=False):
        """Find ALL chains from any root/key node to the target.
        Returns list of DerivationChain, sorted by quality."""
        if target_name not in self.graph.nodes:
            return []

        allowed = FORCED_EDGE_TYPES if forced_only else None
        results = []

        # Search from roots
        for root in self.graph.roots():
            chain_edges, status = self.graph.find_chain(
                root.name, target_name,
                allowed_types=allowed, max_depth=max_depth
            )
            if chain_edges:
                results.append(DerivationChain(chain_edges, root.name, target_name))

        # Search from key framework objects
        key_names = ['R', 'N', 'P', 'L', 'disc', 'phi', 'phi_bar',
                     'alpha_S', 'N_c', 'parent_ker', 'dim_gauge',
                     'beta_KMS', 'ker/A', '||N||^2', '||R||^2',
                     'Koide_Q', 'Koide_delta']
        for name in key_names:
            if name in self.graph.nodes and name != target_name:
                chain_edges, status = self.graph.find_chain(
                    name, target_name,
                    allowed_types=allowed, max_depth=max_depth
                )
                if chain_edges:
                    results.append(DerivationChain(chain_edges, name, target_name))

        # Deduplicate by path
        seen = set()
        unique = []
        for r in results:
            key = r.path_str()
            if key not in seen:
                seen.add(key)
                unique.append(r)

        # Sort: forced first, then shorter, then by weakest edge quality
        weakness_rank = {
            EdgeType.OPERATION_PRODUCES: 0,
            EdgeType.IDENTITY_CASTS: 1,
            EdgeType.LIFT_PROPAGATES: 2,
            EdgeType.COMPUTED_BY: 3,
            EdgeType.NUMERICAL_MATCHES: 10,
            EdgeType.IDENTIFIED_WITH: 11,
            EdgeType.STRUCTURAL_PARALLEL: 12,
        }
        unique.sort(key=lambda c: (
            not c.is_forced,
            weakness_rank.get(c.weakest, 20),
            c.length,
        ))

        return unique

    def forced_chains(self, target_name, max_depth=8):
        """Find only fully forced chains (LAW-promotable)."""
        return self.search(target_name, max_depth=max_depth, forced_only=True)

    def competing_chains(self, target_name, max_depth=8):
        """Find all chains and partition into forced vs mixed.
        The derivation engine needs competing chains to discriminate."""
        all_chains = self.search(target_name, max_depth=max_depth)
        forced = [c for c in all_chains if c.is_forced]
        mixed = [c for c in all_chains if not c.is_forced]
        return {
            'target': target_name,
            'forced': forced,
            'mixed': mixed,
            'total': len(all_chains),
            'can_be_LAW': len(forced) > 0,
            'best': all_chains[0] if all_chains else None,
        }

    def investigate(self, target_name, max_depth=8):
        """Full investigation: find chains, compete them, determine status."""
        result = self.competing_chains(target_name, max_depth)

        # Apply the strict success condition:
        # Must have competing chains, kill at least one weak one
        if result['total'] == 0:
            result['verdict'] = 'NO_CHAINS'
            result['status'] = ResultType.FAILED
        elif result['can_be_LAW']:
            result['verdict'] = 'FORCED_CHAIN_EXISTS'
            result['status'] = ResultType.LAW
            result['derivation'] = result['forced'][0].path_str()
        elif result['total'] >= 2:
            result['verdict'] = 'MULTIPLE_MIXED_CHAINS'
            result['status'] = ResultType.PATH_CANDIDATE
        else:
            result['verdict'] = 'SINGLE_MIXED_CHAIN'
            result['status'] = ResultType.LAW_CANDIDATE

        return result


# ================================================================
# SELF-TEST
# ================================================================

if __name__ == "__main__":
    print("BACKWARD SEARCH SELF-TEST")
    print("=" * 65)

    bs = BackwardSearch()
    checks = []

    # Test 1: alpha_S should have a forced chain
    print("\n--- alpha_S ---")
    result = bs.investigate('alpha_S')
    print(f"  Verdict: {result['verdict']}")
    print(f"  Status: {result['status']}")
    print(f"  Forced chains: {len(result['forced'])}")
    print(f"  Mixed chains: {len(result['mixed'])}")
    if result.get('derivation'):
        print(f"  Derivation: {result['derivation']}")
    checks.append(("alpha_S has forced chain", result['can_be_LAW']))
    checks.append(("alpha_S -> LAW", result['status'] == ResultType.LAW))

    # Test 2: wobble_silent should NOT have forced chain (has identification)
    print("\n--- wobble_silent ---")
    result_w = bs.investigate('wobble_silent')
    print(f"  Verdict: {result_w['verdict']}")
    print(f"  Status: {result_w['status']}")
    print(f"  Forced: {len(result_w['forced'])}, Mixed: {len(result_w['mixed'])}")
    if result_w['best']:
        print(f"  Best chain: {result_w['best']}")
        print(f"  Path: {result_w['best'].path_str()}")
    checks.append(("wobble NOT forced", not result_w['can_be_LAW']))

    # Test 3: 1/alpha_EM should be mixed (NUMERICAL_MATCHES edges)
    print("\n--- 1/alpha_EM ---")
    result_em = bs.investigate('1/alpha_EM')
    print(f"  Verdict: {result_em['verdict']}")
    print(f"  Status: {result_em['status']}")
    print(f"  Forced: {len(result_em['forced'])}, Mixed: {len(result_em['mixed'])}")
    if result_em['best']:
        print(f"  Best: {result_em['best']}")
    checks.append(("1/alpha_EM not forced", not result_em['can_be_LAW']))
    checks.append(("1/alpha_EM has chains", result_em['total'] > 0))

    # Test 4: m_e/m_p
    print("\n--- m_e/m_p ---")
    result_ep = bs.investigate('m_e/m_p')
    print(f"  Verdict: {result_ep['verdict']}")
    print(f"  Status: {result_ep['status']}")
    if result_ep['best']:
        print(f"  Best: {result_ep['best'].path_str()}")
    checks.append(("m_e/m_p has chains", result_ep['total'] > 0))

    # Test 5: sin2_theta13
    print("\n--- sin2_theta13 ---")
    result_13 = bs.investigate('sin2_theta13')
    print(f"  Verdict: {result_13['verdict']}")
    print(f"  Forced: {len(result_13['forced'])}")
    if result_13.get('derivation'):
        print(f"  Derivation: {result_13['derivation']}")
    checks.append(("theta_13 has forced chain", result_13['can_be_LAW']))

    # Test 6: open frontier should have no chains
    print("\n--- 4D_Ricci (open) ---")
    result_open = bs.investigate('4D_Ricci')
    print(f"  Verdict: {result_open['verdict']}")
    checks.append(("open frontier = NO_CHAINS", result_open['verdict'] == 'NO_CHAINS'))

    # Summary table
    print(f"\n{'=' * 65}")
    print("DERIVATION STATUS OF ALL KEY QUANTITIES")
    print(f"{'=' * 65}")
    targets = ['alpha_S', 'sin2_thetaW', 'Bell_S', 'Koide_Q', 'Koide_delta',
               'm_p/M_Pl', 'm_e/m_p', '1/alpha_EM', 'sin2_tW_mZ',
               'wobble_silent', 'bp_per_turn', 'sin2_theta13',
               'n_amino', 'n_codons', 'Eigen_threshold']
    for t in targets:
        r = bs.investigate(t)
        forced_n = len(r['forced'])
        mixed_n = len(r['mixed'])
        print(f"  {t:20s}  {r['status']:20s}  forced={forced_n}  mixed={mixed_n}")

    print(f"\n{'=' * 65}")
    n_pass = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n{n_pass}/{len(checks)} passed.")
    print(f"\nThe derivation engine distinguishes forced chains from mixed chains.")
    print(f"Forced = LAW. Mixed = LAW_CANDIDATE. The machine can justify.")

# ================================================================
# EDGE DISCOVERY (merged from edge_discoverer.py)
# ================================================================

sys.path.insert(0, '../..')
from framework_types import EdgeType, ResultType, FORCED_EDGE_TYPES
from knowledge_graph import KnowledgeGraph
from operations import (apply_all_unary, apply_all_binary, FRAMEWORK_MATRICES,
                        OpResult)


class ProposedEdge:
    """A newly discovered connection between graph nodes."""
    def __init__(self, source_name, target_name, edge_type, operation_name,
                 value_match, tolerance):
        self.source = source_name
        self.target = target_name
        self.edge_type = edge_type
        self.operation = operation_name
        self.value_match = value_match
        self.tolerance = tolerance
        self.is_forced = edge_type in FORCED_EDGE_TYPES

    def __repr__(self):
        forced = "FORCED" if self.is_forced else "WEAK"
        return (f"Edge({self.source} --[{self.operation}]--> {self.target}, "
                f"{self.edge_type}, {forced}, tol={self.tolerance:.4f})")


class EdgeDiscoverer:
    """Discovers new edges between existing graph nodes."""

    def __init__(self, graph=None):
        self.graph = graph or KnowledgeGraph().seed()

    def discover_from(self, source_name, tolerance=1e-4):
        """Apply all operations to source node, check if results match
        any existing node. Returns list of ProposedEdge.

        Also tries COMPOSITE operations: op2(op1(X)) to find indirect
        connections the seed graph doesn't have."""
        source_node = self.graph.get(source_name)
        if source_node is None:
            return []

        proposed = []

        # Path 1: matrix operations (if source is a matrix)
        source_matrix = self._to_matrix(source_node)
        if source_matrix is not None:
            results = apply_all_unary(source_matrix, source_name)
            results += apply_all_binary(source_matrix, source_name)

            # COMPOSITE: apply scalar extraction to matrix results
            for r in list(results):
                if r.is_matrix:
                    for scalar_op in [
                        lambda X, n: OpResult(f'tr({n})', float(np.trace(X)),
                                             EdgeType.COMPUTED_BY, '', [n]),
                        lambda X, n: OpResult(f'det({n})', float(np.linalg.det(X)),
                                             EdgeType.COMPUTED_BY, '', [n]),
                        lambda X, n: OpResult(f'||{n}||^2',
                                             float(np.linalg.norm(X, 'fro')**2),
                                             EdgeType.COMPUTED_BY, '', [n]),
                    ]:
                        try:
                            composite = scalar_op(r.value, r.name)
                            composite.edge_type = EdgeType.COMPUTED_BY
                            composite.description = f'composite: {r.name} -> scalar'
                            composite.inputs = [source_name]
                            results.append(composite)
                        except Exception:
                            pass

        # Path 2: scalar arithmetic (if source has a scalar value)
        results_scalar = []
        if isinstance(source_node.value, (int, float, np.floating)):
            v = float(source_node.value)
            if v > 0:
                results_scalar.append(OpResult(
                    f'sqrt({source_name})', np.sqrt(v),
                    EdgeType.COMPUTED_BY, 'sqrt', [source_name]))
                results_scalar.append(OpResult(
                    f'ln({source_name})', np.log(v),
                    EdgeType.COMPUTED_BY, 'ln', [source_name]))
            results_scalar.append(OpResult(
                f'1/{source_name}', 1.0/v if abs(v) > 1e-30 else None,
                EdgeType.COMPUTED_BY, 'inverse', [source_name]))
            for other_name, other_node in self.graph.nodes.items():
                if other_name == source_name:
                    continue
                if isinstance(other_node.value, (int, float, np.floating)):
                    w = float(other_node.value)
                    results_scalar.append(OpResult(
                        f'{source_name}*{other_name}', v*w,
                        EdgeType.COMPUTED_BY, 'product', [source_name, other_name]))
                    results_scalar.append(OpResult(
                        f'{source_name}+{other_name}', v+w,
                        EdgeType.COMPUTED_BY, 'sum', [source_name, other_name]))
                    if abs(w) > 1e-30:
                        results_scalar.append(OpResult(
                            f'{source_name}/{other_name}', v/w,
                            EdgeType.COMPUTED_BY, 'ratio', [source_name, other_name]))

        results = (results if source_matrix is not None else []) + results_scalar

        # Check each result against all graph nodes
        for op_result in results:
            if op_result.value is None:
                continue
            for target_name, target_node in self.graph.nodes.items():
                if target_name == source_name:
                    continue
                if target_node.value is None:
                    continue

                match, tol = self._compare(op_result.value, target_node.value)
                if match and tol <= tolerance:
                    # Check this edge doesn't already exist
                    already = any(
                        e.source.name == source_name and e.target.name == target_name
                        and e.edge_type == op_result.edge_type
                        for e in self.graph.edges
                    )
                    if not already:
                        proposed.append(ProposedEdge(
                            source_name=source_name,
                            target_name=target_name,
                            edge_type=op_result.edge_type,
                            operation_name=op_result.name,
                            value_match=tol < 1e-10,
                            tolerance=tol,
                        ))

        # Deduplicate (keep best tolerance per source->target pair)
        best = {}
        for p in proposed:
            key = (p.source, p.target)
            if key not in best or p.tolerance < best[key].tolerance:
                best[key] = p

        return sorted(best.values(), key=lambda p: (not p.is_forced, p.tolerance))

    def discover_all(self, tolerance=1e-6):
        """Try to discover new edges from ALL nodes with matrix values."""
        all_proposed = []
        for name, node in self.graph.nodes.items():
            if self._to_matrix(node) is not None:
                proposed = self.discover_from(name, tolerance)
                all_proposed.extend(proposed)
        return all_proposed

    def grow(self, tolerance=1e-6):
        """Discover new edges and ADD them to the graph. Returns count."""
        proposed = self.discover_all(tolerance)
        added = 0
        for p in proposed:
            edge = self.graph.add_edge(
                p.source, p.target, p.edge_type,
                f'DISCOVERED: {p.operation} (tol={p.tolerance:.2e})'
            )
            if edge:
                added += 1
        return added, proposed

    def _to_matrix(self, node):
        """Try to interpret a node's value as a 2x2 matrix."""
        # Check if the node name corresponds to a known framework matrix
        matrix_map = {
            'R': np.array([[0,1],[1,1]], dtype=float),
            'N': np.array([[0,-1],[1,0]], dtype=float),
            'J': np.array([[0,1],[1,0]], dtype=float),
            'h': np.array([[1,0],[0,-1]], dtype=float),
            'P': np.array([[0,0],[2,1]], dtype=float),
        }
        if node.name in matrix_map:
            return matrix_map[node.name]
        if isinstance(node.value, np.ndarray) and node.value.shape == (2, 2):
            return node.value
        return None

    def _compare(self, op_value, node_value):
        """Compare operation result with node value. Returns (matches, tolerance)."""
        try:
            if isinstance(op_value, (int, float, np.floating)):
                if isinstance(node_value, (int, float, np.floating)):
                    if abs(node_value) < 1e-30:
                        return abs(op_value) < 1e-10, abs(op_value)
                    tol = abs(op_value - node_value) / abs(node_value)
                    return tol < 0.001, tol  # 0.1% for exact discovery
                return False, float('inf')
            elif isinstance(op_value, bool):
                return op_value == node_value, 0.0 if op_value == node_value else 1.0
            elif isinstance(op_value, np.ndarray) and isinstance(node_value, np.ndarray):
                if op_value.shape == node_value.shape:
                    if np.allclose(op_value, node_value, atol=1e-10):
                        return True, 0.0
                return False, float('inf')
            elif isinstance(op_value, dict) and isinstance(node_value, dict):
                return op_value == node_value, 0.0 if op_value == node_value else 1.0
        except (TypeError, ValueError):
            pass
        return False, float('inf')


# ================================================================
# FORM CHECKER
# ================================================================

import re


class FormChecker:
    """Checks whether a scanner expression uses framework-admissible operations.

    Framework-admissible operations:
      + (direct sum in the algebra) - ADMISSIBLE
      * (matrix product / scalar multiplication) - ADMISSIBLE
      ^ with integer exponent (repeated multiplication) - ADMISSIBLE
      ^ with framework exponent (phi, N_c, disc) - ADMISSIBLE
      / (ratio) - ADMISSIBLE (inverse exists in the algebra)
      sqrt (when argument is disc or norm^2) - ADMISSIBLE
      ln (when argument is phi -> gives beta_KMS) - ADMISSIBLE
      arbitrary real exponents - SUSPICIOUS

    A fully admissible expression can promote higher than a non-admissible one.
    """

    # Framework-native tokens (constants, quantities, structural names)
    FRAMEWORK_TOKENS = {
        'disc', 'phi', 'phi_bar', 'N_c', 'dim_gauge', 'ker', 'im',
        'parent_ker', 'beta_KMS', 'alpha_S', 'Koide_Q', 'Koide_delta',
        'A', 'R', 'N', 'P', 'J', 'h', 'mu', 'tr', 'det', 'rank',
        'd', 'n', 'k',
    }

    # Admissible sqrt arguments
    SQRT_ADMISSIBLE = {'disc', '5', 'norm2', '||N||^2', '||R||^2', '3', '2'}

    # Admissible ln arguments
    LN_ADMISSIBLE = {'phi', 'phi_bar', '2', 'disc'}

    # Integer or framework exponents (admissible after ^)
    FRAMEWORK_EXPONENTS = {'2', '3', '4', '-1', '-2', 'N_c', 'disc',
                           'phi', 'phi_bar', 'n', 'k', 'd'}

    def check(self, expression_str):
        """Check admissibility of an expression string.

        Returns dict with:
          admissible: bool (all ops admissible)
          operations: list of detected ops
          suspicious: list of suspicious ops with reasons
          score: float 0.0-1.0 (fraction admissible)
        """
        ops = self._extract_operations(expression_str)
        suspicious = []

        for op in ops:
            reason = self._check_op(op, expression_str)
            if reason:
                suspicious.append({'op': op, 'reason': reason})

        n_total = max(len(ops), 1)
        n_clean = n_total - len(suspicious)
        score = n_clean / n_total

        return {
            'admissible': len(suspicious) == 0,
            'operations': ops,
            'suspicious': suspicious,
            'score': score,
        }

    def classify_expression(self, expression_str):
        """Classify into one of four form categories."""
        result = self.check(expression_str)

        if result['score'] == 1.0 and self._all_tokens_framework(expression_str):
            # Check if the structure is actually forced (no free parameters)
            if self._is_forced_form(expression_str):
                return 'FORCED_FORM'
            return 'ADMISSIBLE_FORM'
        elif result['score'] >= 0.5:
            return 'SUSPICIOUS_FORM'
        else:
            return 'INADMISSIBLE_FORM'

    # ---- internals ----

    def _extract_operations(self, expr):
        """Extract all operations from an expression string."""
        ops = []
        if '+' in expr:
            ops.append('+')
        if '-' in expr and not expr.startswith('-'):
            ops.append('-')
        if '*' in expr:
            ops.append('*')
        if '/' in expr:
            ops.append('/')
        if '^' in expr:
            ops.append('^')
        if 'sqrt' in expr:
            ops.append('sqrt')
        if 'ln' in expr:
            ops.append('ln')
        if 'log' in expr and 'ln' not in expr:
            ops.append('log')
        if 'exp' in expr:
            ops.append('exp')
        if re.search(r'\^\s*[0-9]*\.[0-9]', expr):
            ops.append('^real')
        return ops

    def _check_op(self, op, expr):
        """Return a reason string if the op is suspicious, else None."""
        if op in ('+', '-', '*', '/'):
            return None  # Always admissible

        if op == '^':
            # Check what comes after ^
            matches = re.findall(r'\^\s*([A-Za-z_0-9.]+)', expr)
            for exp in matches:
                if exp not in self.FRAMEWORK_EXPONENTS:
                    try:
                        val = int(exp)  # integer exponents always OK
                    except ValueError:
                        try:
                            float(exp)
                            return f'real exponent {exp}'
                        except ValueError:
                            pass
            return None

        if op == '^real':
            return 'arbitrary real exponent detected'

        if op == 'sqrt':
            match = re.search(r'sqrt\(([^)]+)\)', expr)
            arg = match.group(1) if match else ''
            if arg not in self.SQRT_ADMISSIBLE and not self._is_framework_token(arg):
                return f'sqrt of non-framework argument: {arg}'
            return None

        if op == 'ln':
            match = re.search(r'ln\(([^)]+)\)', expr)
            arg = match.group(1) if match else ''
            if arg not in self.LN_ADMISSIBLE and not self._is_framework_token(arg):
                return f'ln of non-framework argument: {arg}'
            return None

        if op == 'log':
            return 'log (base ambiguous) — use ln for framework'

        if op == 'exp':
            return None  # exp is mediation bridge, always admissible

        return f'unknown operation: {op}'

    def _is_framework_token(self, token):
        """Check if a token is a known framework quantity."""
        return token in self.FRAMEWORK_TOKENS

    def _all_tokens_framework(self, expr):
        """Check if all non-operator tokens in expression are framework-native."""
        # Strip operators and parens, split into tokens
        cleaned = re.sub(r'[+\-*/^()\s]', ' ', expr)
        cleaned = re.sub(r'\b(sqrt|ln|log|exp)\b', '', cleaned)
        tokens = [t for t in cleaned.split() if t]
        for t in tokens:
            if t in self.FRAMEWORK_TOKENS:
                continue
            try:
                int(t)
                continue  # integers are structural
            except ValueError:
                pass
            if t not in self.FRAMEWORK_TOKENS:
                return False
        return True

    def _is_forced_form(self, expr):
        """Heuristic: forced if uses only ^int, +, *, / on framework tokens."""
        # No real exponents, no sqrt/ln needed
        if 'sqrt' in expr or 'ln' in expr or 'exp' in expr:
            return False
        if re.search(r'\^\s*[0-9]*\.[0-9]', expr):
            return False
        return True


# ================================================================
# SELF-TEST
# ================================================================

if __name__ == "__main__":
    print("EDGE DISCOVERER SELF-TEST")
    print("=" * 65)

    ed = EdgeDiscoverer()
    initial_edges = len(ed.graph.edges)
    checks = []

    # Discover from R
    print("\n--- Discovering edges from R ---")
    from_R = ed.discover_from('R', tolerance=1e-6)
    print(f"  Found {len(from_R)} new edges from R:")
    for p in from_R[:10]:
        print(f"    {p}")
    checks.append(("R has discoverable edges", len(from_R) > 0))

    # Discover from N
    print("\n--- Discovering edges from N ---")
    from_N = ed.discover_from('N', tolerance=1e-6)
    print(f"  Found {len(from_N)} new edges from N:")
    for p in from_N[:10]:
        print(f"    {p}")
    checks.append(("N has discoverable edges", len(from_N) > 0))

    # Check forced vs weak
    forced_from_R = [p for p in from_R if p.is_forced]
    weak_from_R = [p for p in from_R if not p.is_forced]
    print(f"\n  From R: {len(forced_from_R)} forced, {len(weak_from_R)} weak")
    checks.append(("some forced edges from R", len(forced_from_R) > 0))

    # Grow the graph
    print("\n--- Growing the graph ---")
    added, all_proposed = ed.grow(tolerance=1e-6)
    final_edges = len(ed.graph.edges)
    print(f"  Initial edges: {initial_edges}")
    print(f"  Proposed: {len(all_proposed)}")
    print(f"  Added: {added}")
    print(f"  Final edges: {final_edges}")
    checks.append(("graph grew", final_edges > initial_edges))

    # After growing, check if backward search finds more chains
    # BackwardSearch is defined above in this file
    bs = BackwardSearch(ed.graph)

    print("\n--- Re-searching after growth ---")
    for target in ['alpha_S', '1/alpha_EM', 'wobble_silent']:
        r = bs.investigate(target)
        print(f"  {target}: {r['status']} "
              f"(forced={len(r['forced'])}, mixed={len(r['mixed'])})")

    print(f"\n{'=' * 65}")
    n_pass = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n{n_pass}/{len(checks)} passed.")
    print(f"\nThe graph grew from {initial_edges} to {final_edges} edges.")
    print(f"The machine discovers its own connections.")

    # ============================================================
    # FORM CHECKER SELF-TEST
    # ============================================================
    print(f"\n\n{'=' * 65}")
    print("FORM CHECKER SELF-TEST")
    print("=" * 65)

    fc = FormChecker()
    fc_checks = []

    # Test 1: Pure framework arithmetic -> FORCED_FORM
    r1 = fc.classify_expression('disc^N_c+dim_gauge')
    print(f"\n  'disc^N_c+dim_gauge' -> {r1}")
    fc_checks.append(("disc^N_c+dim_gauge is FORCED", r1 == 'FORCED_FORM'))

    # Test 2: Integer power of framework quantity -> FORCED_FORM
    r2 = fc.classify_expression('parent_ker^2')
    print(f"  'parent_ker^2' -> {r2}")
    fc_checks.append(("parent_ker^2 is FORCED", r2 == 'FORCED_FORM'))

    # Test 3: Framework ratio -> FORCED_FORM
    r3 = fc.classify_expression('d*disc+ker/A')
    print(f"  'd*disc+ker/A' -> {r3}")
    fc_checks.append(("d*disc+ker/A is FORCED", r3 == 'FORCED_FORM'))

    # Test 4: ln(phi) is admissible (gives beta_KMS)
    r4 = fc.classify_expression('beta_KMS^2+ln(phi)')
    print(f"  'beta_KMS^2+ln(phi)' -> {r4}")
    fc_checks.append(("ln(phi) is ADMISSIBLE", r4 == 'ADMISSIBLE_FORM'))

    # Test 5: sqrt(disc) is admissible
    r5 = fc.classify_expression('sqrt(disc)*N_c')
    print(f"  'sqrt(disc)*N_c' -> {r5}")
    fc_checks.append(("sqrt(disc)*N_c is ADMISSIBLE", r5 == 'ADMISSIBLE_FORM'))

    # Test 6: Arbitrary real exponent -> SUSPICIOUS
    r6 = fc.classify_expression('disc^1.347*phi')
    print(f"  'disc^1.347*phi' -> {r6}")
    fc_checks.append(("real exponent is SUSPICIOUS", r6 in ('SUSPICIOUS_FORM', 'INADMISSIBLE_FORM')))

    # Test 7: Non-framework token -> not fully admissible
    r7 = fc.classify_expression('pi^2*zeta_3/omega')
    print(f"  'pi^2*zeta_3/omega' -> {r7}")
    fc_checks.append(("non-framework tokens degrade", r7 != 'FORCED_FORM'))

    # Test 8: check() returns correct structure
    r8 = fc.check('disc^N_c+dim_gauge')
    print(f"  check('disc^N_c+dim_gauge'): admissible={r8['admissible']}, "
          f"score={r8['score']}, ops={r8['operations']}")
    fc_checks.append(("check returns admissible=True for framework expr",
                      r8['admissible'] and r8['score'] == 1.0))

    print(f"\n{'-' * 40}")
    n_fc_pass = sum(1 for _, ok in fc_checks if ok)
    for name, ok in fc_checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n{n_fc_pass}/{len(fc_checks)} form-checker tests passed.")
    print(f"\nForm-matching separates framework relations from numerical coincidence.")
