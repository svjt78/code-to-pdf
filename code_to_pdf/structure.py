# code_to_pdf/structure.py

import subprocess
import html
import re
from pathlib import Path

from .scanner import load_gitignore_specs, is_ignored

def generate_structure_txt(root: Path, depth: int = 3) -> str:
    """
    Runs `tree -L <depth>` in `root`, prunes out large/vendor dirs via `-I`,
    filters any remaining entries against .gitignore, and returns the text.
    If `tree` isn’t available or errors, returns a placeholder message.
    """
    root = root.resolve()
    # Load .gitignore specs for this project
    specs = load_gitignore_specs(root)

    # Directories to skip entirely at the tree-walk level
    ignore_dirs = ["node_modules", ".next", "build", "dist", "__pycache__"]
    ignore_pattern = "|".join(ignore_dirs)

    try:
        proc = subprocess.run(
            ["tree", "-L", str(depth), "-I", ignore_pattern],
            cwd=str(root),
            capture_output=True,
            text=True,
            check=True
        )
        raw = proc.stdout
    except FileNotFoundError:
        return "(tree command not available)"
    except subprocess.CalledProcessError as e:
        return f"(error generating project structure: {e})"

    # Post-filter any lines still matching .gitignore
    filtered_lines: list[str] = []
    for i, line in enumerate(raw.splitlines()):
        # Always keep the first line (the root header)
        if i == 0:
            filtered_lines.append(line)
            continue

        # Extract the path text after the tree drawing chars
        m = re.match(r"^[\s│├└┐─]+(.*)$", line)
        path_part = m.group(1) if m else line.strip()

        # Skip if gitignored
        if is_ignored(path_part, specs, root):
            continue

        filtered_lines.append(line)

    return "\n".join(filtered_lines) + "\n"


def render_structure_html(structure_text: str, depth: int = 3) -> str:
    """
    Wraps the filtered tree text in HTML for inclusion in the PDF.
    """
    escaped = html.escape(structure_text)
    return (
        "<div class='project-structure'>"
        f"<h1>Project Structure (depth {depth})</h1>"
        f"<pre>{escaped}</pre>"
        "</div>"
    )
