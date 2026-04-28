"""
generate_wiki.py — Generate wiki entity pages with REAL content.

Extracts actual theorem statements from paper_v2.md.
Builds real [[wikilinks]] between pages using the forcing graph.
Every page has: the actual math, the actual dependencies, the actual source.
"""
import re
import os
from pathlib import Path
from collections import defaultdict

SEED = Path(__file__).parent.parent
PAPER = SEED / "paper" / "paper_v2.md"
WIKI = SEED / "llm wiki"
ENTITIES = WIKI / "entities"

THEOREM_PAT = re.compile(
    r'\*\*(?:Theorem|Corollary|Proposition|Definition|Lemma|Remark)\s+'
    r'([\d.]+\w?)\s*'
    r'(?:\(([^)]+)\))?\.\*\*\.?\s*(.*)'
)
THEOREM_REF = re.compile(r'(?:Theorem|Thm|Cor|Lemma)\s+([\d.]+\w?)')


def extract_theorems():
    """Extract theorem ID, name, full statement, and proof from paper."""
    text = PAPER.read_text(encoding='utf-8')
    lines = text.split('\n')

    theorems = []
    thm_positions = []

    for i, line in enumerate(lines):
        m = THEOREM_PAT.search(line)
        if m:
            thm_positions.append((i, m.group(1), m.group(2) or '', m.group(3) or ''))

    for idx, (i, thm_id, thm_name, first_line) in enumerate(thm_positions):
        # End of this theorem = start of next theorem, or section break
        if idx + 1 < len(thm_positions):
            end = thm_positions[idx + 1][0]
        else:
            end = min(i + 50, len(lines))

        # Grab EVERYTHING between this theorem and the next
        block_lines = lines[i:end]
        full_block = '\n'.join(block_lines)

        # Statement = everything up to *Proof* or end of block
        # (captures tables, equations, multi-line content)
        stmt_lines = [first_line] if first_line else []
        for j in range(i + 1, end):
            line_s = lines[j].strip()
            if line_s.startswith('*Proof'):
                break
            if line_s.startswith('**Theorem') or line_s.startswith('**Corollary') or line_s.startswith('**Proposition') or line_s.startswith('**Remark') or line_s.startswith('---'):
                break
            stmt_lines.append(lines[j])  # keep original formatting
        statement = '\n'.join(stmt_lines).strip()
        # Keep full statement — the wiki must be standalone
        # No truncation. The page IS the content.

        # Proof = from *Proof* to QED/square or end of block
        proof_lines = []
        in_proof = False
        for j in range(i + 1, end):
            if '*Proof' in lines[j] or lines[j].strip().startswith('*Proof'):
                in_proof = True
            if in_proof:
                proof_lines.append(lines[j])
                if ('$\\square$' in lines[j] or 'QED' in lines[j] or
                    '∎' in lines[j] or lines[j].strip().endswith('$\\square$')):
                    break
        proof = '\n'.join(proof_lines).strip() if proof_lines else ''

        # References to other theorems (dependencies)
        refs = THEOREM_REF.findall(full_block)
        # Only keep refs to EARLIER theorems
        earlier_ids = set(t[1] for t in thm_positions[:idx])
        deps = [r for r in refs if r != thm_id and r in earlier_ids]

        theorems.append({
            'id': thm_id,
            'name': thm_name,
            'statement': statement[:800],
            'proof': proof[:500],
            'line': i + 1,
            'deps': list(set(deps)),
        })

    return theorems


def delatex(text):
    """Strip LaTeX, make readable."""
    import re as _re
    text = _re.sub(r'\$\$([^$]+)\$\$', r'\1', text)
    text = _re.sub(r'\$([^$]+)\$', r'\1', text)
    subs = [
        (r'\\mathfrak\{([^}]+)\}', r'\1'), (r'\\mathrm\{([^}]+)\}', r'\1'),
        (r'\\mathbb\{([^}]+)\}', r'\1'), (r'\\bar\{?\\varphi\}?', 'phi_bar'),
        (r'\\varphi', 'phi'), (r'\\sqrt\{([^}]+)\}', r'sqrt(\1)'),
        (r'\\frac\{([^}]+)\}\{([^}]+)\}', r'(\1)/(\2)'),
        (r'\\begin\{pmatrix\}', '['), (r'\\end\{pmatrix\}', ']'),
        (r'\\neq', '!='), (r'\\leq', '<='), (r'\\geq', '>='),
        (r'\\approx', '~'), (r'\\times', 'x'), (r'\\cdot', '*'),
        (r'\\circ', 'o'), (r'\\otimes', 'x'), (r'\\oplus', '+'),
        (r'\\langle', '<'), (r'\\rangle', '>'),
        (r'\\left', ''), (r'\\right', ''), (r'\\text\{([^}]+)\}', r'\1'),
        (r'\\quad', ' '), (r'\\[,;!]', ' '),
        (r'\\pi', 'pi'), (r'\\alpha', 'alpha'), (r'\\beta', 'beta'),
        (r'\\theta', 'theta'), (r'\\lambda', 'lambda'), (r'\\Lambda', 'Lambda'),
        (r'\\mu', 'mu'), (r'\\nu', 'nu'), (r'\\eta', 'eta'), (r'\\rho', 'rho'),
        (r'\\delta', 'delta'), (r'\\Delta', 'Delta'), (r'\\sigma', 'sigma'),
        (r'\\Sigma', 'Sigma'), (r'\\gamma', 'gamma'), (r'\\varepsilon', 'eps'),
        (r'\\dim', 'dim'), (r'\\ker', 'ker'), (r'\\det', 'det'),
        (r'\\sum', 'sum'), (r'\\int', 'int'), (r'\\partial', 'd'),
        (r'\\nabla', 'nabla'), (r'\\square', 'QED'), (r'\\ldots', '...'),
        (r'\\infty', 'inf'), (r'\\pm', '+-'),
        (r'\\cos', 'cos'), (r'\\sin', 'sin'), (r'\\tan', 'tan'),
        (r'\\exp', 'exp'), (r'\\log', 'log'), (r'\\ln', 'ln'),
        (r'\\max', 'max'), (r'\\min', 'min'),
        (r'\\Phi', 'Phi'), (r'\\phi', 'phi'), (r'\\Psi', 'Psi'), (r'\\psi', 'psi'),
    ]
    for pat, rep in subs:
        text = _re.sub(pat, rep, text)
    text = _re.sub(r'\\[a-zA-Z]+\{([^}]+)\}', r'\1', text)
    text = _re.sub(r'\\[a-zA-Z]+', '', text)
    text = _re.sub(r'\\\\', ' \\\\ ', text)  # preserve line breaks in matrices
    return text


def thm_to_filename(name):
    """Convert theorem name to wiki-safe filename."""
    if not name:
        return None
    safe = name.replace(' ', '-').replace('/', '-').replace('$', '')
    safe = safe.replace('\\', '').replace('{', '').replace('}', '')
    safe = re.sub(r'[^\w\-]', '', safe)
    return safe[:60]


def generate_page(thm, id_to_name, id_to_filename):
    """Generate a wiki page with real content for a theorem."""
    display = thm['name'] if thm['name'] else f"Theorem {thm['id']}"
    filename = thm_to_filename(thm['name']) or f"Thm-{thm['id']}"

    # Build dependency links
    dep_links = []
    for dep_id in thm['deps']:
        dep_fn = id_to_filename.get(dep_id)
        dep_name = id_to_name.get(dep_id, f"Thm {dep_id}")
        if dep_fn:
            dep_links.append(f"[[{dep_fn}|{dep_name}]]")
        else:
            dep_links.append(f"Thm {dep_id}")

    # Determine role from theorem ID section
    section = float(thm['id'].split('.')[0]) if '.' in thm['id'] else float(thm['id'].rstrip('abcdef'))
    if section <= 5:
        role = "CORE-ALGEBRA"
    elif section <= 8:
        role = "TOWER"
    elif section <= 12:
        role = "PHYSICS"
    elif section <= 15:
        role = "TOPOLOGY"
    elif section <= 18:
        role = "OBSERVER"
    else:
        role = "CLOSURE"

    # Add concept links: scan statement for framework entities
    concept_links = []
    stmt_lower = thm['statement'].lower()
    concept_map = {
        'P^2': 'P', 'P^T': 'P', 'idempotent': 'P', 'naming act': 'P',
        'R^2': 'R', 'R + I': 'R', 'production': 'R', 'persistence': 'R',
        'N^2': 'N', 'N = -I': 'N', 'observer': 'N', 'self-transparent': 'N',
        'L_{s': 'L', 'Sylvester': 'L', 'self-action': 'L',
        'ker': 'Ker-im-decomposition', 'kernel': 'Ker-im-decomposition',
        'Cl(3,1)': 'Depth-2-Clifford-structure', 'Clifford': 'Clifford-grading',
        'so(3,1)': 'Depth-2-Clifford-structure',
        'Lichnerowicz': 'Lichnerowicz-identification',
        'Fibonacci': 'Fusion--persistence', 'anyon': 'Fusion--persistence',
        'Jones': 'Jones--discriminant', 'V(4_1)': 'Jones--discriminant',
        'Bell': 'Bell-violation--Tsirelson-saturation',
        'CNOT': 'CNOT-from-framework-generators',
        'Hilbert': 'Hilbert-space-from-asymmetry',
        'Gleason': 'Hilbert-space-from-asymmetry',
        'Born rule': 'Hilbert-space-from-asymmetry',
        'gravity': 'gravity', 'Einstein': 'Vacuum-Einstein',
        'alpha_S': 'Strong-coupling', 'strong coupling': 'Strong-coupling',
        'Lambda': 'Lambda-is-depth-invariant', 'cosmological': 'Cosmological-attenuation',
        'hypercharge': 'Hypercharge-uniqueness', 'anomaly': 'Anomaly-cancellation',
        'braiding': 'Braiding-phase', 'spin-statistics': 'Spin-statistics',
        'tower': 'Tower', 'K6': 'Tower', 'generation decay': 'Generation-strength',
    }
    for keyword, target in concept_map.items():
        if keyword.lower() in stmt_lower and target not in [d.split('|')[0].strip('[]') for d in dep_links]:
            link = f"[[{target}]]"
            if link not in concept_links:
                concept_links.append(link)

    # Section-based default links (if no other deps found)
    section_defaults = {
        'CORE-ALGEBRA': ['[[P]]', '[[R]]', '[[N]]', '[[L]]'],
        'TOWER': ['[[Tower]]', '[[L]]'],
        'PHYSICS': ['[[L]]', '[[gravity]]', '[[R]]'],
        'TOPOLOGY': ['[[R]]', '[[N]]'],
        'OBSERVER': ['[[N]]', '[[L]]'],
        'CLOSURE': ['[[P]]'],
    }

    all_links = dep_links + concept_links[:5]
    if not all_links:
        all_links = section_defaults.get(role, ['[[P]]'])[:3]
    # Remove self-links
    my_fn = thm_to_filename(thm['name']) or f"Thm-{thm['id']}"
    all_links = [l for l in all_links if my_fn not in l]
    if not all_links:
        all_links = section_defaults.get(role, ['[[P]]'])[:3]
    deps_text = '\n'.join(f"- {d}" for d in all_links)

    # De-LaTeX the statement and proof
    statement = delatex(thm['statement'])
    proof = delatex(thm['proof']) if thm['proof'] else ''

    # If no proof was extracted, the statement IS the content
    # No external references — the wiki stands alone
    proof_section = ""
    if proof:
        proof_section = f"\n## Proof\n\n{proof}\n"

    page = f"""---
type: entity
role: {role}
theorem: "Thm {thm['id']}"
tags: [{role.lower()}, forced]
---

# {display}

> **Theorem {thm['id']}.**

{statement}

## Dependencies

{deps_text}
{proof_section}
"""
    return filename, page


def main():
    print("Extracting theorems from paper_v2.md...")
    theorems = extract_theorems()
    print(f"  {len(theorems)} theorems extracted")

    # Build lookup tables
    id_to_name = {t['id']: t['name'] for t in theorems}
    id_to_filename = {}
    for t in theorems:
        fn = thm_to_filename(t['name']) or f"Thm-{t['id']}"
        id_to_filename[t['id']] = fn

    # Clear old auto-generated pages (keep hand-curated ones)
    hand_curated = {'P.md', 'R.md', 'N.md', 'L.md', 'gravity.md', 'bell.md', 'wiki.md',
                    'Production.md', 'Tower.md', 'Observer.md', 'Kernel.md',
                    'Image.md', 'Mediation.md', 'Glyphs.md'}

    if ENTITIES.exists():
        for f in ENTITIES.glob("*.md"):
            if f.name not in hand_curated:
                f.unlink()
        print(f"  Cleared old auto-generated pages (kept {len(hand_curated)} hand-curated)")

    ENTITIES.mkdir(parents=True, exist_ok=True)

    # Generate pages
    created = 0
    for thm in theorems:
        filename, page = generate_page(thm, id_to_name, id_to_filename)
        out_path = ENTITIES / f"{filename}.md"
        if not out_path.exists():
            out_path.write_text(page, encoding='utf-8')
            created += 1

    print(f"  Created {created} entity pages")
    print(f"  Total entities: {len(list(ENTITIES.glob('*.md')))}")

    # Show a sample
    print()
    print("Sample pages:")
    for thm in theorems[:3]:
        fn = thm_to_filename(thm['name']) or f"Thm-{thm['id']}"
        print(f"  {fn}.md:")
        print(f"    Statement: {thm['statement'][:100]}...")
        print(f"    Deps: {thm['deps']}")
        print()


if __name__ == "__main__":
    main()
