import argparse
import logging
import time
from pathlib import Path

from .scanner import scan_files
from .renderer import render_file
from .toc import build_toc
from .builder import build_html, write_pdf
from .structure import generate_structure_txt, render_structure_html

# Default file extensions (without 'txt')
DEFAULT_EXTS = "py,js,json,yml,ini,dev,prod,ts,tsx,java,cpp,css,html,md"
DEFAULT_NAMES = "Dockerfile"

def main():
    # Start timing
    start_time = time.perf_counter()

    parser = argparse.ArgumentParser(
        prog="code2pdf",
        description="Export source files to a syntax-highlighted PDF, with project structure"
    )
    parser.add_argument(
        "root",
        type=Path,
        help="Path to the project root you want to export"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("output.pdf"),
        help="Output PDF filename"
    )
    parser.add_argument(
        "--exts",
        type=str,
        default=DEFAULT_EXTS,
        help="Comma-separated file extensions to include (without the dot)"
    )
    parser.add_argument(
        "--names",
        type=str,
        default=DEFAULT_NAMES,
        help="Comma-separated exact filenames to include (e.g. Dockerfile)"
    )
    parser.add_argument(
        "--tree-depth",
        type=int,
        default=3,
        help="Depth for project structure tree (passed to `tree -L`)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging"
    )
    parser.add_argument(
        "--debug-html",
        action="store_true",
        help="Write debug HTML for inspection"
    )
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s"
    )

    # Resolve project root
    root = args.root.resolve()
    logging.info(f"🔍 Scanning for source files in: {root}")

    # Treat any relative output path as relative to the parent of the project root
    if not args.output.is_absolute():
        args.output = root.parent / args.output

    # Parse include patterns
    exts_list = [e.strip() for e in args.exts.split(",") if e.strip()]
    names_list = [n.strip() for n in args.names.split(",") if n.strip()]

    # Scan for source files
    files = list(scan_files(root, exts=exts_list, names=names_list))
    logging.info(f"    → Found {len(files)} files to render")

    # Render each file to HTML blocks
    file_blocks, css_blocks, toc_entries = [], [], []
    logging.info("🖌️ Rendering files:")
    for path in files:
        rel = path.relative_to(root).as_posix()
        logging.info(f"    • {rel}")
        block, css, fid = render_file(path, root)
        file_blocks.append(block)
        css_blocks.append(css)
        toc_entries.append((rel, fid))

    # Build the Table of Contents and main HTML
    logging.info("📑 Building Table of Contents…")
    toc_html = build_toc(toc_entries)
    html = build_html(root, file_blocks, css_blocks, toc_html)

    # Optionally write debug HTML for inspection
    if args.debug_html:
        debug_path = root / "debug.html"
        with open(debug_path, "w", encoding="utf-8") as df:
            df.write(html)
        logging.info(f"📝 Wrote debug.html at {debug_path}")

    # Generate project structure via `tree -L <depth>`, render and append
    #logging.info(f"🌲 Generating project structure (depth={args.tree_depth})…")
    #tree_txt = generate_structure_txt(root, depth=args.tree_depth)
    #tree_html = render_structure_html(tree_txt, depth=args.tree_depth)
    #html = html.replace("</body></html>", f"{tree_html}</body></html>")

    # Generate the final PDF
    logging.info(f"📄 Writing PDF to {args.output}…")
    write_pdf(html, args.output)
    print(f"✅ PDF generated: {args.output}")

    # End timing and report
    elapsed = time.perf_counter() - start_time
    mins = elapsed / 60
    print(f"Total time taken: {elapsed:.2f} seconds ({mins:.2f} minutes)")


if __name__ == "__main__":
    main()
