"""Offline markdown linter covering core markdownlint rules."""

from __future__ import annotations

import sys
from pathlib import Path

RULES = {
    "MD009": "Trailing spaces",
    "MD018": "No space after # in heading",
    "MD047": "File should end with a newline",
}


def check_file(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    for idx, line in enumerate(lines, 1):
        if line.rstrip() != line:
            errors.append(f"{path}:{idx}: MD009 {RULES['MD009']}")
        if line.startswith("#"):
            stripped = line.lstrip("#")
            if not stripped.startswith(" "):
                errors.append(f"{path}:{idx}: MD018 {RULES['MD018']}")
    if text and not text.endswith("\n"):
        errors.append(f"{path}:EOF: MD047 {RULES['MD047']}")
    return errors


def main(paths: list[str]) -> int:
    markdown_files = []
    for target in paths:
        p = Path(target)
        if p.is_dir():
            markdown_files.extend(p.rglob("*.md"))
        else:
            markdown_files.append(p)
    issues: list[str] = []
    for md_file in sorted(markdown_files):
        issues.extend(check_file(md_file))
    for issue in issues:
        print(issue)
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["."]))
