"""Strip LaTeX from wiki entity pages. Make them readable."""
import re
import os

wiki_dir = os.path.join(os.path.dirname(__file__), '..', 'llm wiki', 'entities')

def delatex(text):
    # Remove dollar-sign math delimiters
    text = re.sub(r'\$\$([^$]+)\$\$', r'\1', text)
    text = re.sub(r'\$([^$]+)\$', r'\1', text)

    # LaTeX commands -> plain text
    subs = [
        (r'\\mathfrak\{([^}]+)\}', r'\1'),
        (r'\\mathrm\{([^}]+)\}', r'\1'),
        (r'\\mathbb\{([^}]+)\}', r'\1'),
        (r'\\bar\{?\\varphi\}?', 'phi_bar'),
        (r'\\varphi', 'phi'),
        (r'\\sqrt\{([^}]+)\}', r'sqrt(\1)'),
        (r'\\frac\{([^}]+)\}\{([^}]+)\}', r'(\1)/(\2)'),
        (r'\\tfrac\{([^}]+)\}\{([^}]+)\}', r'(\1)/(\2)'),
        (r'\\begin\{pmatrix\}', '['),
        (r'\\end\{pmatrix\}', ']'),
        (r'\\neq', '!='),
        (r'\\leq', '<='),
        (r'\\geq', '>='),
        (r'\\approx', '~'),
        (r'\\times', 'x'),
        (r'\\cdot', '*'),
        (r'\\circ', ' o '),
        (r'\\otimes', ' x '),
        (r'\\oplus', ' + '),
        (r'\\langle', '<'),
        (r'\\rangle', '>'),
        (r'\\left', ''),
        (r'\\right', ''),
        (r'\\text\{([^}]+)\}', r'\1'),
        (r'\\quad', ' '),
        (r'\\,', ' '),
        (r'\\;', ' '),
        (r'\\!', ''),
        (r'\\infty', 'inf'),
        (r'\\pi', 'pi'),
        (r'\\alpha', 'alpha'),
        (r'\\beta', 'beta'),
        (r'\\theta', 'theta'),
        (r'\\lambda', 'lambda'),
        (r'\\Lambda', 'Lambda'),
        (r'\\mu', 'mu'),
        (r'\\nu', 'nu'),
        (r'\\eta', 'eta'),
        (r'\\delta', 'delta'),
        (r'\\Delta', 'Delta'),
        (r'\\Sigma', 'Sigma'),
        (r'\\sigma', 'sigma'),
        (r'\\gamma', 'gamma'),
        (r'\\Gamma', 'Gamma'),
        (r'\\omega', 'omega'),
        (r'\\varepsilon', 'eps'),
        (r'\\dim', 'dim'),
        (r'\\ker', 'ker'),
        (r'\\det', 'det'),
        (r'\\sum', 'sum'),
        (r'\\int', 'int'),
        (r'\\partial', 'd'),
        (r'\\nabla', 'nabla'),
        (r'\\square', 'QED'),
        (r'\\ldots', '...'),
        (r'\\cdots', '...'),
    ]
    for pat, rep in subs:
        text = re.sub(pat, rep, text)

    # Strip remaining \commands but keep the argument if braced
    text = re.sub(r'\\[a-zA-Z]+\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\[a-zA-Z]+', '', text)

    # Clean up
    text = re.sub(r'\s+', ' ', text)
    # But preserve newlines for markdown
    return text


count = 0
for fname in sorted(os.listdir(wiki_dir)):
    if not fname.endswith('.md'):
        continue
    path = os.path.join(wiki_dir, fname)
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    changed = False
    for line in lines:
        if '\\' in line or '$' in line:
            new_line = delatex(line)
            if new_line != line:
                changed = True
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        count += 1

print(f"De-LaTeXed {count} files")
