# code_to_pdf/tree.py
from pathlib import Path

def build_tree(root: Path) -> str:
    """
    (Included for completeness—currently not used in builder)
    """
    lines = ["<div class='tree'><h1>Project Structure</h1><pre>"]
    for path in sorted(root.rglob("*")):
        indent = " " * ((len(path.relative_to(root).parts) - 1) * 2)
        lines.append(f"{indent}{path.name}")
    lines.append("</pre></div>")
    return "\n".join(lines)
