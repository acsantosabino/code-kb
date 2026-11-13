import re
from pathlib import Path
from typing import Any

from mcp_server.ingest.parse_code import generate_chunk_id, get_git_commit_info


def parse_markdown_file(
    file_path: Path,
    repo_root: Path
) -> list[dict[str, Any]]:
    """Parse Markdown files into structural chunks based on header hierarchy."""
    try:
        text = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []

    lines = text.splitlines()
    if not lines:
        return []

    commit_info = get_git_commit_info(file_path, repo_root)
    rel_path_str = str(file_path.relative_to(repo_root))

    header_regex = re.compile(r"^(#{1,6})\s+(.+)$")
    
    sections = []
    current_title = "Overview"
    current_level = 1
    current_lines: list[str] = []
    start_line = 1

    for idx, line in enumerate(lines, start=1):
        m = header_regex.match(line)
        if m:
            if current_lines:
                sections.append({
                    "section_title": current_title,
                    "header_level": current_level,
                    "start_line": start_line,
                    "end_line": idx - 1,
                    "lines": current_lines
                })
            current_level = len(m.group(1))
            current_title = m.group(2).strip()
            current_lines = [line]
            start_line = idx
        else:
            current_lines.append(line)

    if current_lines:
        sections.append({
            "section_title": current_title,
            "header_level": current_level,
            "start_line": start_line,
            "end_line": len(lines),
            "lines": current_lines
        })

    chunks: list[dict[str, Any]] = []

    for i, sec in enumerate(sections):
        content = "\n".join(sec["lines"]).strip()
        if not content:
            continue

        # Check for overlap from previous section tail if long enough
        if i > 0 and len(sections[i - 1]["lines"]) > 5:
            prev_tail = "\n".join(sections[i - 1]["lines"][-3:])
            content = f"{prev_tail}\n\n{content}"

        c_id = generate_chunk_id(rel_path_str, sec["start_line"], sec["end_line"], content)

        chunks.append({
            "chunk_id": c_id,
            "file_path": rel_path_str,
            "language": "markdown",
            "section_title": sec["section_title"],
            "header_level": sec["header_level"],
            "symbol_name": sec["section_title"],
            "symbol_type": "section",
            "start_line": sec["start_line"],
            "end_line": sec["end_line"],
            "last_commit_hash": commit_info["last_commit_hash"],
            "last_commit_date": commit_info["last_commit_date"],
            "last_commit_author": commit_info["last_commit_author"],
            "chunk_type": "doc",
            "content": content
        })

    return chunks
