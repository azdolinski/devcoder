#!/usr/bin/env python3
"""Generate a Markdown document with a Mermaid dependency graph for s6-rc.

The script scans the s6-overlay configuration directory that holds the
`s6-rc.d` definitions, extracts every module's dependencies, and emits a
Markdown file (`dependency_tree.md`) containing a Mermaid `graph TD` block.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List

REPO_ROOT = Path(__file__).resolve().parent
S6_TREE = Path(os.environ.get("S6_TREE", str(REPO_ROOT / "data/config/tmp/s6-overlay/s6-rc.d"))).expanduser()
OUTPUT_FILE = Path(os.environ.get("OUTPUT_FILE", str(REPO_ROOT / "dependency_tree.md"))).expanduser()


def slug(name: str) -> str:
    """Return a Mermaid-friendly identifier by replacing hyphens."""
    return name.replace("-", "_")


def read_dependencies(base_path: Path) -> Dict[str, List[str]]:
    """Collect dependency lists for every module directory."""
    deps: Dict[str, List[str]] = {}
    for entry in sorted(base_path.iterdir()):
        if not entry.is_dir():
            continue
        module = entry.name
        dep_dir = entry / "dependencies.d"
        parents: List[str] = []
        if dep_dir.is_dir():
            for dep_file in sorted(dep_dir.iterdir()):
                if dep_file.is_file():
                    parents.append(dep_file.name)
        deps[module] = parents
    return deps


def build_mermaid(deps: Dict[str, List[str]]) -> str:
    """Produce a Mermaid graph definition covering all modules."""
    lines: List[str] = ["graph TD"]
    standalone: List[str] = []

    for module, parents in sorted(deps.items()):
        target = slug(module)
        if parents:
            for parent in parents:
                lines.append(f"    {slug(parent)} --> {target}")
        else:
            standalone.append(target)

    # Include dependencies that exist only as parents (no module dir)
    referenced_only = sorted({slug(parent)
                              for parents in deps.values()
                              for parent in parents
                              if parent not in deps})

    for node in sorted(set(standalone)):
        lines.append(f"    {node}")
    for node in referenced_only:
        lines.append(f"    {node}")

    return "\n".join(lines) + "\n"


def build_markdown(mermaid_graph: str) -> str:
    """Wrap the Mermaid graph in a Markdown document."""
    content = [
        "# Drzewo zależności modułów s6-overlay",
        "",
        "Wykres generowany automatycznie na podstawie plików `s6-rc.d`.",
        "",
        "```mermaid",
        mermaid_graph.rstrip(),
        "```",
        "",
    ]
    return "\n".join(content)


def main() -> None:
    if not S6_TREE.is_dir():
        raise SystemExit(f"Directory not found: {S6_TREE}")

    deps = read_dependencies(S6_TREE)
    mermaid = build_mermaid(deps)
    markdown = build_markdown(mermaid)
    OUTPUT_FILE.write_text(markdown, encoding="utf-8")
    print(f"Markdown graph written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
