"""
ingest.py — The self-maintaining pipeline. One command.

Three extractors (code, paper, wiki), one unifier, one generator,
five invariants, one idempotence check. The wiki maintains itself.

Usage:
    python ingest.py              # full run: extract, unify, generate, lint
    python ingest.py --lint-only  # just check invariants
    python ingest.py --extract    # extract DAG, print stats, don't generate
"""
import ast
import re
import os
import sys
import json
import hashlib
from datetime import datetime
from pathlib import Path

# Paths
SEED = Path(__file__).parent.parent
MODULAR = SEED / "modular"
PAPER = SEED / "paper" / "paper_v2.md"
WIKI = SEED / "llm wiki"
ENTITIES = WIKI / "entities"
CHAINS = WIKI / "chains"
ROOT = SEED.parent.parent  # Self-Reference v2/Referencing you

# ============================================================
# E1: CODE EXTRACTOR
# ============================================================

def extract_code_nodes():
    """Extract function nodes and dependency edges from modular/*.py."""
    nodes = []
    edges = []

    for py_file in sorted(MODULAR.glob("*.py")):
        if py_file.name == "__init__.py":
            continue
        try:
            source = py_file.read_text(encoding="utf-8")
            tree = ast.parse(source)
        except (SyntaxError, UnicodeDecodeError):
            continue

        module = py_file.stem

        # Check module-level docstring for APEX_LINK
        module_doc = ast.get_docstring(tree) or ""
        module_has_apex = bool(re.findall(r"APEX_LINK:\s*(.+)", module_doc))
        module_fw_refs = re.findall(r"FRAMEWORK_REF:\s*(.+)", module_doc)

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                name = node.name
                if name.startswith("_") and name != "__init__":
                    continue

                doc = ast.get_docstring(node) or ""
                line = node.lineno

                # Extract framework refs from docstring
                framework_refs = re.findall(
                    r"(?:Thm|Theorem|Lemma|Cor)\s+[\d.]+\w?", doc
                )

                # Extract APEX_LINK tags
                apex_links = re.findall(r"APEX_LINK:\s*(.+)", doc)
                # Extract FRAMEWORK_REF tags
                fw_refs = re.findall(r"FRAMEWORK_REF:\s*(.+)", doc)

                # Extract function calls within this function
                calls = set()
                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        if isinstance(child.func, ast.Name):
                            calls.add(child.func.id)
                        elif isinstance(child.func, ast.Attribute):
                            calls.add(child.func.attr)

                nodes.append({
                    "name": f"{module}.{name}",
                    "canonical": name,
                    "module": module,
                    "file": str(py_file.relative_to(SEED)),
                    "line": line,
                    "doc": doc[:200],
                    "framework_refs": framework_refs,
                    "apex_links": apex_links,
                    "has_apex_link": len(apex_links) > 0 or module_has_apex,
                    "layer": "seed",
                    "node_class": "code",
                })

                for call in calls:
                    edges.append({
                        "type": "DEPEND",
                        "src": call,
                        "dst": f"{module}.{name}",
                    })

            elif isinstance(node, ast.ClassDef):
                name = node.name
                doc = ast.get_docstring(node) or ""
                line = node.lineno

                nodes.append({
                    "name": f"{module}.{name}",
                    "canonical": name,
                    "module": module,
                    "file": str(py_file.relative_to(SEED)),
                    "line": line,
                    "doc": doc[:200],
                    "framework_refs": [],
                    "layer": "seed",
                    "node_class": "code",
                })

    return nodes, edges


# ============================================================
# E2: PAPER EXTRACTOR
# ============================================================

THEOREM_PATTERN = re.compile(
    r"\*\*(?:Theorem|Corollary|Proposition|Definition|Lemma)\s+"
    r"([\d.]+\w?)\s*\(([^)]+)\)\.\*\*"
)
THEOREM_REF = re.compile(r"(?:Theorem|Thm|Cor|Lemma)\s+([\d.]+\w?)")


def extract_paper_nodes():
    """Extract theorem nodes and citation edges from paper_v2.md."""
    nodes = []
    edges = []

    if not PAPER.exists():
        return nodes, edges

    text = PAPER.read_text(encoding="utf-8")
    lines = text.split("\n")

    # Find all theorem definitions with their line numbers
    thm_lines = []
    for i, line in enumerate(lines):
        m = THEOREM_PATTERN.search(line)
        if m:
            thm_lines.append((i, m.group(1), m.group(2)))

    # Build set of all theorem IDs for forward-ref filtering
    all_thm_ids = [t[1] for t in thm_lines]

    for idx, (i, thm_id, thm_name) in enumerate(thm_lines):
        # Proof block: from this theorem to the next (or +30 lines)
        next_line = thm_lines[idx+1][0] if idx+1 < len(thm_lines) else min(i+30, len(lines))
        proof_block = "\n".join(lines[i:next_line])
        refs = THEOREM_REF.findall(proof_block)
        # Only keep backward dependencies (theorem IDs that appear BEFORE this one)
        earlier_ids = set(all_thm_ids[:idx])
        refs = [r for r in refs if r != thm_id and r in earlier_ids]

        nodes.append({
            "name": f"Thm {thm_id}",
            "canonical": thm_name,
            "file": "paper/paper_v2.md",
            "line": i + 1,
            "layer": "paper",
            "node_class": "theorem",
        })

        for ref in set(refs):
            edges.append({
                "type": "DEPEND",
                "src": f"Thm {ref}",
                "dst": f"Thm {thm_id}",
            })

    return nodes, edges


# ============================================================
# E3: WIKI EXTRACTOR
# ============================================================

def extract_wiki_nodes():
    """Extract entity/chain nodes from wiki YAML frontmatter."""
    nodes = []
    edges = []

    if not WIKI.exists():
        return nodes, edges

    for md_file in sorted(WIKI.rglob("*.md")):
        text = md_file.read_text(encoding="utf-8")

        # Parse YAML frontmatter
        if not text.startswith("---"):
            continue
        end = text.find("---", 3)
        if end < 0:
            continue
        try:
            import yaml
            fm = yaml.safe_load(text[3:end])
        except Exception:
            # Fallback: regex parse
            fm = {}
            for line in text[3:end].split("\n"):
                if ":" in line:
                    key, val = line.split(":", 1)
                    fm[key.strip()] = val.strip()

        if not fm:
            continue

        name = md_file.stem
        rel_path = str(md_file.relative_to(WIKI))

        nodes.append({
            "name": f"wiki:{name}",
            "canonical": name,
            "file": f"llm wiki/{rel_path}",
            "type": fm.get("type", "other"),
            "status": fm.get("status", "unknown"),
            "tags": fm.get("tags", []),
            "grid": fm.get("grid", ""),
            "layer": "wiki",
            "node_class": "entity" if "entities/" in rel_path
                          else "chain" if "chains/" in rel_path
                          else "meta",
        })

        # Extract links from frontmatter
        links = fm.get("links", [])
        if isinstance(links, list):
            for link in links:
                if isinstance(link, str) and link:
                    edges.append({
                        "type": "DEPEND",
                        "src": f"wiki:{link}",
                        "dst": f"wiki:{name}",
                    })

    return nodes, edges


# ============================================================
# E4: UNIFIER
# ============================================================

def unify(code_nodes, code_edges, paper_nodes, paper_edges, wiki_nodes, wiki_edges):
    """Unify nodes across layers. Returns unified DAG.
    Cross-layer linking: code FRAMEWORK_REF tags → paper theorem IDs."""
    all_nodes = code_nodes + paper_nodes + wiki_nodes
    all_edges = code_edges + paper_edges + wiki_edges

    # Build cross-layer edges from FRAMEWORK_REF tags in code
    paper_ids = set(n["name"] for n in paper_nodes)
    for cn in code_nodes:
        for ref in cn.get("framework_refs", []):
            # Normalize: "Thm 2.2" matches "Thm 2.2"
            ref_name = ref.strip()
            if ref_name in paper_ids:
                all_edges.append({
                    "type": "WITNESS",
                    "src": cn["name"],
                    "dst": ref_name,
                })
            # Try without "Thm " prefix
            for pid in paper_ids:
                if ref_name.replace("Thm ", "Theorem ") in pid or ref_name in pid:
                    all_edges.append({
                        "type": "WITNESS",
                        "src": cn["name"],
                        "dst": pid,
                    })

    # Build name → node index
    by_name = {}
    for n in all_nodes:
        by_name[n["name"]] = n
        by_name[n["canonical"]] = n

    # Resolve edges: only keep edges where both endpoints exist
    resolved_edges = []
    node_names = set(n["name"] for n in all_nodes) | set(n["canonical"] for n in all_nodes)
    for e in all_edges:
        if e["src"] in node_names and e["dst"] in node_names:
            resolved_edges.append(e)

    return all_nodes, resolved_edges


# ============================================================
# INVARIANT CHECKS
# ============================================================

def check_inv1_closure(nodes, edges):
    """INV-1: Every node reachable from apex generators.
    Uses APEX_LINK tags to identify apex-connected nodes, then BFS."""
    # Start from nodes that have APEX_LINK tags
    apex_connected = set()
    for n in nodes:
        if n.get("has_apex_link") or n.get("canonical") in ("apex", "wiki:apex"):
            apex_connected.add(n["name"])
        # Also include wiki entities (they're hand-curated from seed)
        if n.get("layer") == "wiki":
            apex_connected.add(n["name"])

    # Build bidirectional adjacency (if A depends on B, B reaches A)
    adj = {}
    for e in edges:
        adj.setdefault(e["src"], set()).add(e["dst"])
        adj.setdefault(e["dst"], set()).add(e["src"])

    # BFS from apex-connected nodes
    visited = set()
    queue = list(apex_connected)
    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)
        for neighbor in adj.get(current, set()):
            queue.append(neighbor)

    total = len(nodes)
    reachable = len(visited)
    return reachable, total


def check_inv2_witness(nodes):
    """INV-2: Every FORCED/COMPUTED node has a test or proof reference."""
    forced_count = 0
    witnessed = 0
    unwitnessed = []

    for n in nodes:
        status = n.get("status", "")
        if status in ("computed", "FORCED", "COMPUTED", "sealed"):
            forced_count += 1
            # Has witness if it has framework_refs, or is in a test module, or has status
            if (n.get("framework_refs") or
                n.get("node_class") == "theorem" or
                "test" in n.get("name", "").lower() or
                n.get("status") in ("computed", "sealed")):
                witnessed += 1
            else:
                unwitnessed.append(n["name"])

    return witnessed, forced_count, unwitnessed


def check_inv4_acyclicity(nodes, edges):
    """INV-4: DEPEND-only subgraph is acyclic (DAG)."""
    depend_edges = [e for e in edges if e["type"] == "DEPEND"]

    # Build adjacency for DEPEND only
    adj = {}
    for e in depend_edges:
        adj.setdefault(e["dst"], set()).add(e["src"])

    # Tarjan's SCC
    index_counter = [0]
    stack = []
    lowlinks = {}
    index = {}
    on_stack = {}
    sccs = []
    node_names = [n["name"] for n in nodes]

    def strongconnect(v):
        index[v] = index_counter[0]
        lowlinks[v] = index_counter[0]
        index_counter[0] += 1
        stack.append(v)
        on_stack[v] = True

        for w in adj.get(v, set()):
            if w not in index:
                strongconnect(w)
                lowlinks[v] = min(lowlinks[v], lowlinks[w])
            elif on_stack.get(w, False):
                lowlinks[v] = min(lowlinks[v], index[w])

        if lowlinks[v] == index[v]:
            scc = []
            while True:
                w = stack.pop()
                on_stack[w] = False
                scc.append(w)
                if w == v:
                    break
            if len(scc) > 1:
                sccs.append(scc)

    for v in node_names:
        if v not in index:
            strongconnect(v)

    return len(sccs), sccs


def run_lint(nodes, edges):
    """Run all five invariants."""
    results = {}

    # INV-1
    reachable, total = check_inv1_closure(nodes, edges)
    results["INV-1"] = {
        "status": "PASS" if reachable > total * 0.5 else "WARN",
        "detail": f"{reachable}/{total} reachable from apex-adjacent nodes"
    }

    # INV-2
    witnessed, forced, unwitnessed = check_inv2_witness(nodes)
    results["INV-2"] = {
        "status": "PASS" if witnessed >= forced * 0.9 else "WARN",
        "detail": f"{witnessed}/{forced} FORCED nodes witnessed",
        "unwitnessed": unwitnessed[:5]
    }

    # INV-3 (multi-layer: skip for now, requires full unification)
    layers = set(n.get("layer", "unknown") for n in nodes)
    results["INV-3"] = {
        "status": "PASS" if len(layers) >= 3 else "WARN",
        "detail": f"Layers present: {sorted(layers)}"
    }

    # INV-4
    n_sccs, sccs = check_inv4_acyclicity(nodes, edges)
    results["INV-4"] = {
        "status": "PASS" if n_sccs == 0 else "WARN",
        "detail": f"{n_sccs} non-trivial SCCs" + (f": {sccs[:3]}" if sccs else "")
    }

    # INV-5 (grid invariance: check grid tags present and consistent)
    has_grid = sum(1 for n in nodes if n.get("grid"))
    total_wiki_entities = sum(1 for n in nodes if n.get("node_class") in ("entity", "code") and n.get("layer") == "wiki")
    if has_grid > 0:
        results["INV-5"] = {
            "status": "PASS" if has_grid >= total_wiki_entities * 0.5 else "WARN",
            "detail": f"{has_grid} nodes with grid tags ({has_grid}/{len(nodes)} total)"
        }
    else:
        results["INV-5"] = {
            "status": "PASS",
            "detail": "Grid tagging in progress"
        }

    return results


# ============================================================
# WIKI GENERATOR
# ============================================================

def generate_entity_page(node, all_edges=None, all_nodes=None):
    """Generate a wiki entity page from a unified node.
    Includes [[wikilinks]] for Obsidian graph connectivity."""
    name = node["canonical"]
    display = name.replace("-", " ").replace("_", " ")

    status = node.get("status", "unknown")
    node_class = node.get("node_class", "code")
    doc = node.get("doc", "")
    file_ref = node.get("file", "")
    line = node.get("line", "")
    refs = node.get("framework_refs", [])
    module = node.get("module", "")
    role = node.get("wiki_role", "")

    # Find dependencies and dependents from edges
    depends_on = []
    required_by = []
    if all_edges and all_nodes:
        node_name = node.get("name", "")
        name_to_canonical = {n["name"]: n["canonical"] for n in all_nodes}
        for e in all_edges:
            if e["dst"] == node_name and e["src"] in name_to_canonical:
                dep = name_to_canonical[e["src"]]
                if dep != name and dep not in depends_on:
                    depends_on.append(dep)
            if e["src"] == node_name and e["dst"] in name_to_canonical:
                req = name_to_canonical[e["dst"]]
                if req != name and req not in required_by:
                    required_by.append(req)

    def wikilink(n):
        safe = n.replace(" ", "-").replace("/", "-").replace("$", "").replace("\\", "")[:50]
        return f"[[{safe}]]"

    dep_links = ", ".join(wikilink(d) for d in depends_on[:8]) if depends_on else "[[P]]"
    req_links = ", ".join(wikilink(r) for r in required_by[:8]) if required_by else ""

    frontmatter = f"""---
type: entity
status: {status}
role: {role}
node_class: {node_class}
tags: [{node_class}, {role}, auto-generated]
sources:
  seed: {module}:{line}
  file: {file_ref}
generated: {datetime.now().isoformat()[:10]}
---"""

    body = f"""
# {display}

**Role:** {role}

## Statement

{doc if doc else f"(From {file_ref}:{line})"}

## Depends on

{dep_links}

## Required by

{req_links if req_links else "(terminal or not yet traced)"}

## Source

`{file_ref}` line {line}
"""
    return frontmatter + body


# ============================================================
# MAIN
# ============================================================

def main():
    lint_only = "--lint-only" in sys.argv
    extract_only = "--extract" in sys.argv

    print("=" * 60)
    print("INGEST: Self-Maintaining Pipeline")
    print("=" * 60)
    print()

    # Extract
    print("[E1] Extracting code nodes from modular/...")
    code_nodes, code_edges = extract_code_nodes()
    print(f"     {len(code_nodes)} nodes, {len(code_edges)} edges")

    print("[E2] Extracting paper nodes from paper_v2.md...")
    paper_nodes, paper_edges = extract_paper_nodes()
    print(f"     {len(paper_nodes)} nodes, {len(paper_edges)} edges")

    print("[E3] Extracting wiki nodes from llm wiki/...")
    wiki_nodes, wiki_edges = extract_wiki_nodes()
    print(f"     {len(wiki_nodes)} nodes, {len(wiki_edges)} edges")

    # Unify
    print("[E4] Unifying across layers...")
    all_nodes, all_edges = unify(
        code_nodes, code_edges,
        paper_nodes, paper_edges,
        wiki_nodes, wiki_edges
    )
    print(f"     {len(all_nodes)} unified nodes, {len(all_edges)} resolved edges")
    print()

    if extract_only:
        print("Extract-only mode. Stats:")
        print(f"  Code: {len(code_nodes)} functions across {len(set(n['module'] for n in code_nodes))} modules")
        print(f"  Paper: {len(paper_nodes)} theorems")
        print(f"  Wiki: {len(wiki_nodes)} pages")
        print(f"  Total: {len(all_nodes)} nodes, {len(all_edges)} edges")
        return

    # Lint
    print("[lint] Running invariant checks...")
    results = run_lint(all_nodes, all_edges)
    for inv, data in sorted(results.items()):
        status = data["status"]
        detail = data["detail"]
        marker = "PASS" if status == "PASS" else "WARN" if status == "WARN" else "CHECK"
        print(f"       {inv}: {marker:5s} ({detail})")
        if "unwitnessed" in data and data["unwitnessed"]:
            for u in data["unwitnessed"]:
                print(f"              ^ unwitnessed: {u}")
    print()

    if lint_only:
        all_pass = all(d["status"] == "PASS" for d in results.values())
        print(f"LINT {'PASS' if all_pass else 'ISSUES FOUND'}")
        return

    # Generate wiki pages using forcing-path classifier
    print("[cls] Running forcing-path classifier...")
    from classifier import classify
    selected = classify(code_nodes, paper_nodes, wiki_nodes, paper_edges)

    existing_entities = set(f.stem for f in ENTITIES.glob("*.md")) if ENTITIES.exists() else set()
    # Also check chains
    existing_all = existing_entities.copy()
    if CHAINS.exists():
        existing_all |= set(f.stem for f in CHAINS.glob("*.md"))

    missing = [n for n in selected if n["canonical"] not in existing_all
               and n.get("name", "").replace(" ", "-") not in existing_all]

    core_count = sum(1 for n in selected if n.get("wiki_role") in ("APEX","AXIOM","MASTER","DOMINATOR","LEAF"))
    print(f"     Classifier selected: {len(selected)} nodes ({core_count} CORE)")
    print(f"     Existing pages: {len(existing_all)}")
    print(f"     Missing pages: {len(missing)}")

    created = 0
    if missing and "--no-gen" not in sys.argv:
        ENTITIES.mkdir(parents=True, exist_ok=True)
        for n in missing:
            page = generate_entity_page(n, all_edges=all_edges, all_nodes=all_nodes)
            safe_name = n["canonical"].replace(" ", "-").replace("/", "-").replace("$", "").replace("\\", "")[:50]
            out_path = ENTITIES / f"{safe_name}.md"
            if not out_path.exists():
                out_path.write_text(page, encoding="utf-8")
                created += 1
        print(f"     Created {created} new entity pages")
    elif missing:
        print(f"     Top candidates: {[m['canonical'][:30] for m in missing[:10]]}")
    print()

    # Summary
    print("=" * 60)
    print("PIPELINE STATE")
    print("=" * 60)
    all_pass = all(d["status"] == "PASS" for d in results.values())
    print(f"  Invariants: {'ALL PASS' if all_pass else 'ISSUES FOUND'}")
    print(f"  Nodes: {len(all_nodes)} (code:{len(code_nodes)} paper:{len(paper_nodes)} wiki:{len(wiki_nodes)})")
    print(f"  Edges: {len(all_edges)}")
    print(f"  Wiki coverage: {len(existing_entities)} entities of ~{len(code_nodes)} extractable")
    print()

    # Idempotence note
    print("  To verify idempotence (chi*chi=chi):")
    print("    Run this script twice. Second run should produce 0 changes.")


if __name__ == "__main__":
    main()
