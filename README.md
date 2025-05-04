# file: README.md
# code-to-pdf

A CLI utility to export a codebase to PDF with syntax highlighting and project tree.

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