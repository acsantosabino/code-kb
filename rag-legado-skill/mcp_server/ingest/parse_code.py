import hashlib
import re
import subprocess
from pathlib import Path
from typing import Any

from mcp_server.ingest.discover import get_tracked_files


def get_git_commit_info(file_path: Path, repo_root: Path) -> dict[str, str]:
    try:
        rel_p = str(file_path.relative_to(repo_root))
        res = subprocess.run(
            ["git", "log", "-1", "--format=%H|%an|%ad", "--date=iso", "--", rel_p],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            check=True
        )
        out = res.stdout.strip()
        if out:
            parts = out.split("|")
            return {
                "last_commit_hash": parts[0],
                "last_commit_author": parts[1] if len(parts) > 1 else "",
                "last_commit_date": parts[2] if len(parts) > 2 else ""
            }
    except Exception:
        pass
    return {
        "last_commit_hash": "unknown",
        "last_commit_author": "unknown",
        "last_commit_date": ""
    }


def generate_chunk_id(file_path: str, start_line: int, end_line: int, content: str) -> str:
    raw = f"{file_path}:{start_line}:{end_line}:{content}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def parse_code_file_fallback(
    file_path: Path,
    repo_root: Path,
    language: str
) -> list[dict[str, Any]]:
    """Fallback chunker splitting by functions/classes via regex or line blocks."""
    try:
        text = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []

    lines = text.splitlines()
    if not lines:
        return []

    commit_info = get_git_commit_info(file_path, repo_root)
    rel_path_str = str(file_path.relative_to(repo_root))
    chunks: list[dict[str, Any]] = []

    # Regex patterns for function/class definitions in standard languages
    pattern = re.compile(
        r"^(?:class|def|function|async def|public class|private class|func|class-like)\s+([A-Za-z0-9_]+)",
        re.MULTILINE
    )

    matches = list(pattern.finditer(text))
    if not matches:
        # Fallback to chunking by 100-line windows if no symbols found
        window_size = 80
        overlap = 15
        for i in range(0, len(lines), window_size - overlap):
            chunk_lines = lines[i:i + window_size]
            if not chunk_lines:
                break
            content = "\n".join(chunk_lines)
            start_l = i + 1
            end_l = min(i + window_size, len(lines))
            c_id = generate_chunk_id(rel_path_str, start_l, end_l, content)
            chunks.append({
                "chunk_id": c_id,
                "file_path": rel_path_str,
                "language": language,
                "symbol_name": f"block_{start_l}_{end_l}",
                "symbol_type": "block",
                "start_line": start_l,
                "end_line": end_l,
                "last_commit_hash": commit_info["last_commit_hash"],
                "last_commit_date": commit_info["last_commit_date"],
                "last_commit_author": commit_info["last_commit_author"],
                "chunk_type": "code",
                "content": content
            })
        return chunks

    line_offsets = [0]
    for line in lines:
        line_offsets.append(line_offsets[-1] + len(line) + 1)

    def get_line_num(char_idx: int) -> int:
        for l_num, offset in enumerate(line_offsets):
            if offset > char_idx:
                return max(1, l_num)
        return len(lines)

    for i, m in enumerate(matches):
        sym_name = m.group(1)
        start_char = m.start()
        start_l = get_line_num(start_char)

        if i + 1 < len(matches):
            end_char = matches[i + 1].start()
            end_l = max(start_l, get_line_num(end_char) - 1)
        else:
            end_l = len(lines)

        content = "\n".join(lines[start_l - 1:end_l])
        sym_type = "class" if "class" in m.group(0) else "function"

        c_id = generate_chunk_id(rel_path_str, start_l, end_l, content)
        chunks.append({
            "chunk_id": c_id,
            "file_path": rel_path_str,
            "language": language,
            "symbol_name": sym_name,
            "symbol_type": sym_type,
            "start_line": start_l,
            "end_line": end_l,
            "last_commit_hash": commit_info["last_commit_hash"],
            "last_commit_date": commit_info["last_commit_date"],
            "last_commit_author": commit_info["last_commit_author"],
            "chunk_type": "code",
            "content": content
        })

    return chunks


def parse_code_file(
    file_path: Path,
    repo_root: Path
) -> list[dict[str, Any]]:
    ext_to_lang = {
        ".py": "python",
        ".js": "javascript",
        ".jsx": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".java": "java",
        ".go": "go",
        ".rb": "ruby",
        ".php": "php"
    }
    ext = file_path.suffix.lower()
    language = ext_to_lang.get(ext, "code")

    try:
        import tree_sitter
        import tree_sitter_languages
        
        ts_lang = tree_sitter_languages.get_language(language)
        parser = tree_sitter.Parser()
        parser.set_language(ts_lang)

        text = file_path.read_text(encoding="utf-8", errors="ignore")
        tree = parser.parse(bytes(text, "utf-8"))
        root_node = tree.root_node

        commit_info = get_git_commit_info(file_path, repo_root)
        rel_path_str = str(file_path.relative_to(repo_root))
        lines = text.splitlines()

        chunks: list[dict[str, Any]] = []

        def traverse(node):
            node_type = node.type
            if node_type in ("function_definition", "class_definition", "method_definition", "function_declaration", "method_declaration"):
                start_line = node.start_point[0] + 1
                end_line = node.end_point[0] + 1
                
                # Check for preceding comments/docstrings
                comment_lines = []
                prev = node.prev_sibling
                while prev and prev.type in ("comment", "line_comment", "block_comment", "expression_statement"):
                    p_start = prev.start_point[0]
                    p_end = prev.end_point[0]
                    comment_lines = lines[p_start:p_end + 1] + comment_lines
                    prev = prev.prev_sibling
                
                body_content = lines[start_line - 1:end_line]
                full_lines = comment_lines + body_content
                content = "\n".join(full_lines)

                # Extract symbol name
                name_node = node.child_by_field_name("name")
                sym_name = name_node.text.decode("utf-8") if name_node and name_node.text else f"symbol_{start_line}"
                sym_type = "class" if "class" in node_type else "function"

                c_id = generate_chunk_id(rel_path_str, start_line, end_line, content)
                chunks.append({
                    "chunk_id": c_id,
                    "file_path": rel_path_str,
                    "language": language,
                    "symbol_name": sym_name,
                    "symbol_type": sym_type,
                    "start_line": start_line,
                    "end_line": end_line,
                    "last_commit_hash": commit_info["last_commit_hash"],
                    "last_commit_date": commit_info["last_commit_date"],
                    "last_commit_author": commit_info["last_commit_author"],
                    "chunk_type": "code",
                    "content": content
                })
            else:
                for child in node.children:
                    traverse(child)

        traverse(root_node)
        if chunks:
            return chunks
    except Exception:
        pass

    return parse_code_file_fallback(file_path, repo_root, language)
