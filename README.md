# file: README.md
# code-to-pdf

Code-to-PDF is a lightweight, stand-alone CLI tool that transforms an entire project codebase into a single, beautifully formatted PDF—ideal for code reviews, documentation snapshots, or sharing read-only snapshots of your project.

.gitignore-aware: Automatically reads your project’s .gitignore and skips ignored files, so your PDF only includes the source you care about.

Multi-format support: By default it handles .py, .js, .json, .yml, .ini, .txt, Dockerfile, .dev, .prod, and can be extended via CLI flags.

Syntax-highlighted: Uses Pygments (Dark+ theme by default) to reproduce VS Code–style coloring, complete with line numbers.

Per-file pagination: Each source file begins on its own page with the full file path as a header, ensuring clear mapping between code and module.

Table of Contents: Automatically generates a linked TOC with file paths and page numbers for quick navigation.

Project tree: Appends a recursive directory tree (via tree -L 3) at the end of the document, giving a high-level overview of your project structure.

Easy install & run: Simply pip install code-to-pdf, then code2pdf /path/to/project -o output.pdf—no IDE plugins required.

By combining intelligent file filtering, customizable syntax highlighting, and seamless PDF generation, Code-to-PDF makes it trivial to produce a complete, portable, and printable snapshot of your project codebase.

## Setup & Deployment in VS Code
1. **Clone** this repo:
   ```bash
   git clone <url> && cd code_to_pdf
   ```
2. **Open** folder in VS Code:
   ```bash
   code .
   ```
3. **Create** a Python virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # on Windows: .\\venv\\Scripts\\activate
   ```
4. **Install** dependencies:
   ```bash
   pip install --upgrade pip
   pip install .
   ```
5. **Verify** installation:
   ```bash
   code2pdf --help
   ```
6. **Run** on any project:
   ```bash
   code2pdf /path/to/my/project -o project.pdf
   ```
