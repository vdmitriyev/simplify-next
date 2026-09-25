#!/usr/bin/env python
"""Generate a Stork config.toml indexing every Markdown/reST file under content/."""
import re
import sys
from pathlib import Path

from pelican.settings import DEFAULT_CONFIG
from pelican.utils import slugify

CONTENT_DIR = Path(__file__).parent / "content"
ARTICLE_PATHS = {"blog"}
TITLE_RE = re.compile(r"^(?:Title:\s*|:title:\s*)(.+)$", re.IGNORECASE)


def extract_title(path: Path) -> str:
    with path.open(encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                break
            match = TITLE_RE.match(line)
            if match:
                return match.group(1).strip()
    return path.stem.replace("_", " ").replace("-", " ").title()


def build_url(rel_path: Path, title: str) -> str:
    slug = slugify(title, regex_subs=DEFAULT_CONFIG["SLUG_REGEX_SUBSTITUTIONS"])
    if rel_path.parts[0] in ARTICLE_PATHS:
        return f"blog/{slug}.html"
    return f"pages/{slug}.html"


def toml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def main() -> None:
    entries = []
    for path in sorted(CONTENT_DIR.rglob("*")):
        if path.suffix.lower() not in {".md", ".rst"}:
            continue
        rel_path = path.relative_to(CONTENT_DIR)
        title = extract_title(path)
        url = build_url(rel_path, title)
        entries.append((rel_path.as_posix(), url, title))

    if not entries:
        print("No Markdown/reST files found under content/", file=sys.stderr)
        sys.exit(1)

    lines = ['[input]', 'base_directory = "."', ""]
    for path, url, title in entries:
        filetype = "Markdown" if path.lower().endswith(".md") else "PlainText"
        lines.append("[[input.files]]")
        lines.append(f'path = "{toml_escape(path)}"')
        lines.append(f'url = "{toml_escape(url)}"')
        lines.append(f'title = "{toml_escape(title)}"')
        lines.append(f'filetype = "{filetype}"')
        lines.append("")

    (CONTENT_DIR / "config.toml").write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote config.toml with {len(entries)} entries")


if __name__ == "__main__":
    main()
