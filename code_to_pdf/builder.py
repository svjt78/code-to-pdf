# code_to_pdf/builder.py
from pathlib import Path
from weasyprint import HTML

def build_html(root: Path, file_blocks, css_blocks, toc_html: str) -> str:
    """
    Construct the full HTML document, including:
      - line-wrapping CSS for code blocks
      - Pygments CSS (deduplicated)
      - layout rules (page breaks, fonts, colors)
    """
    # Wrap long code lines (WeasyPrint-compatible)
    wrap_css = """
    /* allow code/pre blocks to wrap long lines */
    pre, code {
      white-space: pre-wrap !important;
      overflow-wrap: break-word !important;
    }
    """

    # Combine all Pygments CSS, dedupe
    pygments_css = "\n".join(sorted(set(css_blocks)))

    # Add our page-layout + font + background rules
    layout_css = """
    /* each file-block starts on a fresh page */
    .file-block { page-break-before: always; page-break-inside: auto; }

    /* monospaced font for code */
    body, pre { font-family: Menlo, Consolas, "Courier New", monospace; }

    /* dark+ background and default text color */
    body { background-color: #1e1e1e; color: #d4d4d4; }
    .highlight { background-color: #1e1e1e !important; }
    """

    html_parts = [
        "<html><head><meta charset='utf-8'><style>",
        wrap_css,
        pygments_css,
        layout_css,
        "</style></head><body>",
        toc_html,
    ]
    html_parts.extend(file_blocks)
    html_parts.append("</body></html>")
    return "\n".join(html_parts)

def write_pdf(html: str, output: Path):
    """Render the HTML to PDF using WeasyPrint."""
    HTML(string=html).write_pdf(str(output))
