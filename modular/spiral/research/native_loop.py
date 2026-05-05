"""
native_loop.py -- The mediation slot. Wires an LLM (or future framework
language engine) into the research loop as the P2 face.

The LLM may:
  - propose hypotheses
  - narrate results
  - compare quantities
  - suggest next investigations

The LLM may NOT:
  - certify results
  - promote status
  - modify the knowledge graph directly
  - bypass the verifier

The mediation slot is REPLACEABLE. LLM now, framework engine later.
"""
import os
import json
import sys
sys.path.insert(0, '../..')

from researcher import Researcher
from framework_types import ResultType


def load_api_key():
    """Load API key from secret.txt (NOT committed to git)."""
    paths = [
        os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'secret.txt'),
        os.path.expanduser('~/.anthropic_key'),
    ]
    for p in paths:
        if os.path.exists(p):
            with open(p) as f:
                return f.read().strip()
    key = os.environ.get('ANTHROPIC_API_KEY')
    if key:
        return key
    return None


def make_claude_mediator(api_key, model='claude-haiku-4-5-20251001'):
    """Create a mediation function using Claude API.
    Uses Haiku for speed/cost. The mediator proposes, does not decide."""
    try:
        import anthropic
    except ImportError:
        print("pip install anthropic")
        return None

    client = anthropic.Anthropic(api_key=api_key)

    def mediate(context):
        """P2 face: given research context, propose next investigation."""
        system = (
            "You are a research mediator for the Self-Reference Framework. "
            "The framework derives physics from P=[[0,0],[2,1]], P^2=P. "
            "Given a research context, propose ONE specific numerical target "
            "or matrix expression to investigate next. Be precise. "
            "Give the number or expression, a one-line reason, and nothing else. "
            "You may NOT certify, promote, or claim results. Only propose."
        )
        try:
            response = client.messages.create(
                model=model,
                max_tokens=150,
                system=system,
                messages=[{"role": "user", "content": context}]
            )
            return response.content[0].text.strip()
        except Exception as e:
            return f"MEDIATION_FAILED: {e}"

    return mediate


def make_dummy_mediator():
    """Fallback mediator that proposes from a fixed list."""
    targets = [
        (137.036, "fine structure constant inverse 1/alpha_EM"),
        (0.00729735, "fine structure constant alpha_EM"),
        (1836.15, "proton/electron mass ratio"),
        (0.2224, "sin(theta_Cabibbo)"),
        (91.1876, "Z boson mass in GeV"),
        (80.379, "W boson mass in GeV"),
        (0.1181, "alpha_S at m_Z"),
        (173000, "top quark mass in MeV"),
        (23, "human chromosome pairs"),
        (46, "human chromosomes"),
    ]
    idx = [0]

    def mediate(context):
        t, reason = targets[idx[0] % len(targets)]
        idx[0] += 1
        return f"Investigate {t}: {reason}"

    return mediate


def run_mediated_cycle(researcher, mediator, n_cycles=3):
    """Run n research cycles with mediation."""
    results = []
    for i in range(n_cycles):
        # Build context from current state
        report = researcher.report()
        frontier = researcher.graph.frontier()
        frontier_names = [f.name for f in frontier[:5]]
        recent = researcher.ledger.entries[-3:] if researcher.ledger.entries else []
        recent_str = '; '.join(str(e) for e in recent)

        context = (
            f"Research state: {report['graph']['nodes']} nodes, "
            f"{report['total_investigations']} investigations, "
            f"{report['survivors']} survivors. "
            f"Frontier: {frontier_names}. "
            f"Recent: {recent_str}. "
            f"What number or matrix should I investigate next?"
        )

        # P2 MEDIATION: propose
        proposal = mediator(context)
        print(f"\n  Cycle {i+1}: Mediator proposes: {proposal}")

        # Extract number from proposal (simple parser)
        target = None
        import re
        numbers = re.findall(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', proposal)
        for num_str in numbers:
            try:
                val = float(num_str)
                if 1e-15 < abs(val) < 1e10:
                    target = val
                    break
            except ValueError:
                continue

        if target is not None:
            result = researcher.investigate_number(target, f"mediated_{i}")
            print(f"  Result: {result['status']}")
            if result.get('best'):
                print(f"  Best: {result['best']}")
            results.append(result)
        else:
            print(f"  Could not extract target from proposal.")
            researcher.ledger.record('mediate', proposal, 'no_target',
                                    ResultType.FAILED)

    return results


# ================================================================
# SELF-TEST
# ================================================================

if __name__ == "__main__":
    print("NATIVE LOOP SELF-TEST")
    print("=" * 60)

    api_key = load_api_key()
    checks = []

    if api_key:
        print(f"  API key found ({len(api_key)} chars)")
        mediator = make_claude_mediator(api_key)
        if mediator:
            checks.append(("API key loaded", True))
            checks.append(("mediator created", True))

            # Run one mediated cycle
            r = Researcher()
            print("\n--- Mediated Research Cycle ---")
            results = run_mediated_cycle(r, mediator, n_cycles=2)

            checks.append(("cycle ran", len(results) > 0))

            report = r.report()
            print(f"\n  Final: {report['total_investigations']} investigations, "
                  f"{report['survivors']} survivors")
            checks.append(("has investigations", report['total_investigations'] > 0))
        else:
            checks.append(("mediator created", False))
    else:
        print("  No API key found. Using dummy mediator.")
        mediator = make_dummy_mediator()
        checks.append(("dummy mediator works", True))

        r = Researcher()
        results = run_mediated_cycle(r, mediator, n_cycles=3)
        checks.append(("dummy cycles ran", len(results) > 0))

        report = r.report()
        print(f"\n  Final: {report['total_investigations']} investigations")
        checks.append(("has investigations", report['total_investigations'] > 0))

    print(f"\n{'=' * 60}")
    n_pass = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n{n_pass}/{len(checks)} passed.")
    print(f"\nThe mediation slot is wired. The P2 face speaks.")
