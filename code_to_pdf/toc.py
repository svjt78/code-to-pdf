# code_to_pdf/toc.py
from pathlib import Path

def build_toc(entries):
    lines = ['<nav class="toc"><h1>Table of Contents</h1><ol>']
    for relpath, fid in entries:
        name = Path(relpath).name
        lines.append(f'<li><a href="#{fid}">{name}</a></li>')
    lines.append("</ol></nav>")
    return "\n".join(lines)
