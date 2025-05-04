# code_to_pdf/structure.py

import subprocess
import html
from pathlib import Path

def generate_structure_txt(root: Path, depth: int = 4) -> str:
    """
    Runs `tree -L <depth>` in `root` and returns the raw text.
    If the `tree` command is not available or fails, returns a placeholder message.
    """
    try:
        result = subprocess.run(
            ["tree", "-L", str(depth)],
            cwd=str(root),
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except FileNotFoundError:
        return "(tree command not available)"
    except subprocess.CalledProcessError as e:
        return f"(error generating project structure: {e})"


def render_structure_html(structure_text: str, depth: int = 4) -> str:
    """
    Wraps the `tree` text in HTML so it can be appended to the PDF.
    """
    escaped = html.escape(structure_text)
    return (
        "<div class='project-structure'>"
        f"<h1>Project Structure (depth {depth})</h1>"
        f"<pre>{escaped}</pre>"
        "</div>"
    )
