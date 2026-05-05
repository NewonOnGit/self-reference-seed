"""
edge_discoverer.py -- Makes the knowledge graph self-extending.

Takes two graph nodes. Tries all framework operations. Reports which
ones connect them. Proposes new typed edges. The graph GROWS.

This is what turns backward_search from "traverse what's given"
into "discover what's connectable."

ARCHITECTURE: L9 (cortex). The framework discovering its own connections.
"""
import numpy as np
import sys
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
    from backward_search import BackwardSearch
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
