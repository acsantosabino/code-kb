#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo "")"

if [ -z "$REPO_ROOT" ]; then
  echo "Error: Must be run within a Git repository."
  exit 1
fi

cd "$REPO_ROOT"

echo "=== RAG Legado Installer ==="
echo "Target Repository: $REPO_ROOT"

# 1. Virtual Environment Setup
VENV_DIR="$REPO_ROOT/.venv"
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating Python virtual environment at .venv..."
  python3 -m venv "$VENV_DIR"
fi

echo "Installing/Updating Python dependencies..."
"$VENV_DIR/bin/pip" install -q --upgrade pip
if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
  "$VENV_DIR/bin/pip" install -q -r "$SCRIPT_DIR/requirements.txt"
fi

# 2. Register MCP Server in .mcp.json
MCP_JSON="$REPO_ROOT/.mcp.json"
echo "Configuring MCP server in .mcp.json..."

if [ ! -f "$MCP_JSON" ]; then
  cat <<EOF > "$MCP_JSON"
{
  "mcpServers": {
    "rag-legado": {
      "command": "$VENV_DIR/bin/python",
      "args": ["$SCRIPT_DIR/mcp_server/server.py"],
      "cwd": "$REPO_ROOT"
    }
  }
}
EOF
else
  # Merge MCP server entry if jq is available or via python snippet
  "$VENV_DIR/bin/python" -c "
import json
p = '$MCP_JSON'
with open(p, 'r') as f:
    data = json.load(f)
if 'mcpServers' not in data:
    data['mcpServers'] = {}
data['mcpServers']['rag-legado'] = {
    'command': '$VENV_DIR/bin/python',
    'args': ['$SCRIPT_DIR/mcp_server/server.py'],
    'cwd': '$REPO_ROOT'
}
with open(p, 'w') as f:
    json.dump(data, f, indent=2)
"
fi

# 3. Copy Agent Skills
echo "Installing Agent Skills..."
mkdir -p "$REPO_ROOT/.claude/skills/rag-legado-busca"
mkdir -p "$REPO_ROOT/.agent/skills/rag-legado-busca"

if [ -f "$SCRIPT_DIR/skill/SKILL.md" ]; then
  cp "$SCRIPT_DIR/skill/SKILL.md" "$REPO_ROOT/.claude/skills/rag-legado-busca/SKILL.md"
  cp "$SCRIPT_DIR/skill/SKILL.md" "$REPO_ROOT/.agent/skills/rag-legado-busca/SKILL.md"
fi

if [ -d "$SCRIPT_DIR/skill/rag-legado-doc" ]; then
  mkdir -p "$REPO_ROOT/.claude/skills/rag-legado-doc"
  mkdir -p "$REPO_ROOT/.agent/skills/rag-legado-doc"
  cp "$SCRIPT_DIR/skill/rag-legado-doc/SKILL.md" "$REPO_ROOT/.claude/skills/rag-legado-doc/SKILL.md" 2>/dev/null || true
  cp "$SCRIPT_DIR/skill/rag-legado-doc/SKILL.md" "$REPO_ROOT/.agent/skills/rag-legado-doc/SKILL.md" 2>/dev/null || true
fi

# 4. Install Git Hooks
if [ -d "$REPO_ROOT/.git/hooks" ]; then
  echo "Installing Git post-commit and post-merge hooks..."
  if [ -f "$SCRIPT_DIR/hooks/post-commit" ]; then
    cp "$SCRIPT_DIR/hooks/post-commit" "$REPO_ROOT/.git/hooks/post-commit"
    chmod +x "$REPO_ROOT/.git/hooks/post-commit"
  fi
  if [ -f "$SCRIPT_DIR/hooks/post-merge" ]; then
    cp "$SCRIPT_DIR/hooks/post-merge" "$REPO_ROOT/.git/hooks/post-merge"
    chmod +x "$REPO_ROOT/.git/hooks/post-merge"
  fi
fi

# 5. Execute Bootstrap Indexing
echo "Running initial repository bootstrap..."
PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH" "$VENV_DIR/bin/python" "$SCRIPT_DIR/bootstrap_index.py" "$REPO_ROOT"

echo "=== RAG Legado Installation Complete! ==="
