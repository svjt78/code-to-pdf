# code_to_pdf/scanner.py

import logging
from pathlib import Path
from pathspec import GitIgnoreSpec
from binaryornot.check import is_binary

def load_gitignore_specs(root: Path) -> list[tuple[Path, GitIgnoreSpec]]:
    """
    Recursively find all .gitignore files under root and load their specs.
    Returns a list of (directory, GitIgnoreSpec) tuples.
    """
    specs: list[tuple[Path, GitIgnoreSpec]] = []
    for gitignore_path in root.rglob(".gitignore"):
        base_dir = gitignore_path.parent
        lines = gitignore_path.read_text(encoding="utf-8", errors="ignore").splitlines()
        logging.debug(f"⚙️  Loaded {len(lines)} patterns from {gitignore_path.relative_to(root)}")
        spec = GitIgnoreSpec.from_lines(lines)
        specs.append((base_dir, spec))
    return specs

def is_ignored(rel_path: str, specs: list[tuple[Path, GitIgnoreSpec]], root: Path) -> bool:
    """
    Check all loaded gitignore specs to see if rel_path should be ignored.
    A spec applies if its base_dir is a parent of the file.
    """
    for base_dir, spec in specs:
        try:
            # Determine the file path relative to the .gitignore's directory
            rel_to_spec = Path(rel_path).relative_to(base_dir.relative_to(root))
        except Exception:
            continue
        if spec.match_file(str(rel_to_spec.as_posix())):
            logging.debug(f"     • SKIP (ignored by {base_dir.relative_to(root)}/.gitignore)")
            return True
    return False

def scan_files(
    root: Path,
    exts: list[str] = None,
    names: list[str] = None,
    max_size: int = 2 * 1024 * 1024
):
    """
    Yield source files under root that:
      - have extensions in `exts`, or filenames in `names`
      - are not gitignored (at any level)
      - are not binary
      - are <= max_size
    """
    root = root.resolve()
    logging.debug(f"📦  Scanning directory tree: {root}")

    # Load all .gitignore specs once
    specs = load_gitignore_specs(root)

    # Defaults
    exts = exts or [
        "py", "js", "json", "yml", "ini", "txt", "dev", "prod",
        "ts", "tsx", "java", "cpp", "css", "html", "md"
    ]
    names = names or ["Dockerfile"]

    logging.debug(f"🔧  scan_files will include extensions: {exts}")
    logging.debug(f"🔧  scan_files will include filenames: {names}")

    # Helper to test a path
    def consider(path: Path, tag: str):
        if not path.is_file():
            logging.debug(f"🔎  skipping {path.relative_to(root)} (not a file)")
            return False

        rel = path.relative_to(root).as_posix()
        logging.debug(f"🔎  considering {rel} ({tag})")

        # Skip the generated project structure file
        if path.name == "project_structure.txt":
            logging.debug(f"     • SKIP (generated structure file)")
            return False

        # Skip npm lockfile (we don’t want that in our PDF)
        if path.name == "package-lock.json":
            logging.debug(f"     • SKIP (npm lockfile)")
            return False

        if is_ignored(rel, specs, root):
            return False

        # Binary check
        try:
            bin_flag = is_binary(str(path))
        except Exception as e:
            bin_flag = True
            logging.debug(f"   ↳ is_binary threw {e!r}, marking as binary")
        if bin_flag:
            logging.debug("     • SKIP (binary)")
            return False

        # Size guard
        size = path.stat().st_size
        if size > max_size:
            logging.debug(f"     • SKIP (> {max_size} bytes)")
            return False

        logging.debug(f"   ✅ yielding {rel}")
        return True

    # 1) By extension
    for ext in exts:
        for path in sorted(root.rglob(f"*.{ext}")):
            if consider(path, f"ext={ext}"):
                yield path

    # 2) By exact filename
    for name in names:
        for path in sorted(root.rglob(name)):
            if consider(path, f"name={name}"):
                yield path
