# code_to_pdf/renderer.py

from pathlib import Path
import logging
from pygments import highlight
from pygments.lexers import guess_lexer_for_filename, TextLexer
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

from .vscodedark import VSDarkPlus

def render_file(path: Path, root: Path):
    """
    Returns (html_block, css_defs, file_id).
    Uses inline (no-table) linenos=False for simplicity.
    Renders the file path relative to the given root directory.
    """
    # Read source (with error replacement)
    code = path.read_text(encoding="utf-8", errors="replace")

    # Pick a lexer, falling back to plain text if none match
    try:
        lexer = guess_lexer_for_filename(str(path.name), code)
    except ClassNotFound:
        logging.debug(f"⚠️  No Pygments lexer for {path.name}, using TextLexer")
        lexer = TextLexer()

    # Format to HTML
    fmt = HtmlFormatter(style=VSDarkPlus, linenos=False)
    css = fmt.get_style_defs(".highlight")
    html_block = highlight(code, lexer, fmt)

    # Build a stable file-block ID
    fid = f"f-{abs(hash(str(path)))}"

    # Compute relative path for the heading
    rel = path.relative_to(root).as_posix()

    block = (
        f'<div class="file-block" id="{fid}">'
        f'<h2 class="path">{rel}</h2>'
        f'{html_block}'
        "</div>"
    )
    return block, css, fid
