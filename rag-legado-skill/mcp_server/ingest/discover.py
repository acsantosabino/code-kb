import fnmatch
import os
import subprocess
from pathlib import Path

SUPPORTED_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx",
    ".java", ".go", ".rb", ".php",
    ".md", ".mdx", ".rst"
}

MAX_FILE_SIZE_BYTES = 1024 * 1024  # 1MB


def load_ragignore_patterns(repo_root: Path) -> list[str]:
    patterns = [
        "node_modules/*", "vendor/*", ".venv/*", "venv/*",
        "__pycache__/*", "*.pyc", ".git/*", ".lancedb/*",
        "dist/*", "build/*", "*.egg-info/*", ".rag_state.json",
        ".rag_index/*"
    ]
    
    ragignore_path = repo_root / ".ragignore"
    if ragignore_path.exists():
        with open(ragignore_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.append(line)
    return patterns


def is_ignored(rel_path_str: str, patterns: list[str]) -> bool:
    rel_path_str = rel_path_str.replace("\\", "/")
    for pattern in patterns:
        pattern = pattern.strip("/")
        if fnmatch.fnmatch(rel_path_str, pattern) or fnmatch.fnmatch(rel_path_str, f"**/{pattern}"):
            return True
        # Check parent directories
        parts = rel_path_str.split("/")
        for i in range(1, len(parts)):
            sub_path = "/".join(parts[:i])
            if fnmatch.fnmatch(sub_path, pattern):
                return True
    return False


def get_tracked_files(repo_root: Path | str) -> tuple[list[Path], list[dict]]:
    repo_path = Path(repo_root).resolve()
    ragignore_patterns = load_ragignore_patterns(repo_path)
    
    tracked_rel_paths: list[str] = []
    
    try:
        res = subprocess.run(
            ["git", "ls-files", "-c", "-o", "--exclude-standard"],
            cwd=str(repo_path),
            capture_output=True,
            text=True,
            check=True
        )
        tracked_rel_paths = [line.strip() for line in res.stdout.splitlines() if line.strip()]
    except Exception:
        # Fallback if git is unavailable or not a git repo
        for root, _, files in os.walk(repo_path):
            for file in files:
                abs_f = Path(root) / file
                rel_f = str(abs_f.relative_to(repo_path))
                tracked_rel_paths.append(rel_f)
                
    valid_files: list[Path] = []
    ignored_report: list[dict] = []
    
    for rel_str in tracked_rel_paths:
        abs_path = repo_path / rel_str
        if not abs_path.exists() or not abs_path.is_file():
            continue
            
        ext = abs_path.suffix.lower()
        if ext not in SUPPORTED_EXTENSIONS:
            ignored_report.append({
                "file_path": rel_str,
                "reason": f"Unsupported extension '{ext}'"
            })
            continue
            
        if is_ignored(rel_str, ragignore_patterns):
            ignored_report.append({
                "file_path": rel_str,
                "reason": "Matched .ragignore pattern"
            })
            continue
            
        try:
            size = abs_path.stat().st_size
            if size > MAX_FILE_SIZE_BYTES:
                ignored_report.append({
                    "file_path": rel_str,
                    "reason": f"File size exceeds 1MB limit ({size} bytes)"
                })
                continue
        except OSError:
            continue
            
        valid_files.append(abs_path)
        
    return valid_files, ignored_report
