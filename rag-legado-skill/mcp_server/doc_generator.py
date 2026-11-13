import json
import re
import time
from pathlib import Path
from typing import Any

from mcp_server.retrieve.hybrid_search import hybrid_search


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-") or "modulo"


def extract_manual_section(existing_text: str) -> str:
    pattern = re.compile(
        r"(<!--\s*manual:start\s*-->)(.*?)(<!--\s*manual:end\s*-->)",
        re.DOTALL | re.IGNORECASE
    )
    match = pattern.search(existing_text)
    if match:
        return match.group(2).strip()
    return ""


def generate_module_doc(
    repo_root: Path | str,
    caminho_ou_nome: str,
    modo: str = "criar"
) -> dict[str, Any]:
    repo_path = Path(repo_root).resolve()
    slug = slugify(caminho_ou_nome)
    doc_path = repo_path / "docs" / "features" / f"{slug}.md"

    # Search RAG context for module
    query = f"Modulo funcionalidade comportamento {caminho_ou_nome}"
    filters = {}
    if "/" in caminho_ou_nome or "\\" in caminho_ou_nome or caminho_ou_nome.endswith((".py", ".js", ".ts")):
        filters["file_path_prefix"] = caminho_ou_nome.replace("\\", "/")

    chunks = hybrid_search(repo_path, query, top_k=15, filters=filters if filters else None)

    if not chunks:
        # Retry search without prefix filter
        chunks = hybrid_search(repo_path, query, top_k=15)

    # Filter out skill tooling files unless explicitly documenting them
    ignore_prefixes = (".agent/", "rag-legado-skill/", ".claude/", "docs/features/")
    if not any(caminho_ou_nome.startswith(p) for p in ignore_prefixes):
        chunks = [
            c for c in chunks
            if not any(c.get("file_path", "").startswith(p) for p in ignore_prefixes)
        ]

    if not chunks:
        return {
            "status": "error",
            "message": f"Nenhum contexto encontrado na base RAG para '{caminho_ou_nome}'.",
            "caminho_gerado": None
        }

    sources = sorted(list({c.get("file_path", "") for c in chunks if c.get("file_path")}))
    symbols = [c.get("symbol_name") for c in chunks if c.get("symbol_name")]

    # Extract manual notes if updating existing file
    preserved_manual_notes = ""
    sections_preserved = 0
    if modo == "atualizar" and doc_path.exists():
        try:
            existing_content = doc_path.read_text(encoding="utf-8")
            manual_text = extract_manual_section(existing_content)
            if manual_text:
                preserved_manual_notes = manual_text
                sections_preserved = 1
        except Exception:
            pass

    if not preserved_manual_notes:
        preserved_manual_notes = "<!-- Espaço para observações humanas, post-mortems relacionados, etc. -->"

    # Build PRD section contents from retrieved chunks (segmented extraction)
    executive_summary_lines = []
    user_stories_lines = []
    functional_specs = []
    non_functional_lines = []
    architecture_lines = []
    dependencies_lines = []
    edge_cases_lines = []
    tdd_test_lines = []
    reproduction_steps = []
    entry_points = []

    for c in chunks:
        fp = c.get("file_path", "")
        sym = c.get("symbol_name") or c.get("section_title", "") or "Módulo / Função"
        start_l = c.get("start_line", 1)
        end_l = c.get("end_line", 1)

        entry_points.append(f"- [{fp}#L{start_l}-L{end_l}](file://{fp}) — `{sym}`")

        content_snippet = c.get("content", "").strip()
        lines = [l for l in content_snippet.splitlines() if not l.startswith("import") and not l.startswith("from")]
        first_line = lines[0][:120] if lines else "Componente do módulo"

        executive_summary_lines.append(f"- **{sym}** (`{fp}`): {first_line}")
        user_stories_lines.append(f"- Como desenvolvedor/sistema, necessito que `{sym}` execute conforme especificado em `{fp}` para garantir o funcionamento correto da funcionalidade `{caminho_ou_nome}`.")
        functional_specs.append(f"### {sym}\n- **Localização**: `{fp}` (linhas {start_l}-{end_l})\n- **Descrição**: {first_line}\n- **Regra de Negócio**: Deve processar entradas válidas sem falhas e garantir a integridade dos dados retornados.")
        architecture_lines.append(f"- Componente `{sym}` em `{fp}`")
        dependencies_lines.append(f"- Importações/Dependências de `{fp}`")
        edge_cases_lines.append(f"- Falha ou entrada inválida em `{sym}` (`{fp}`): validar tratamento de erros e exceções esperadas.")
        
        tdd_test_lines.append(
            f"### Test Spec: `{sym}`\n"
            f"- **Dado (Given)**: Instância de `{sym}` configurada com contexto válido em `{fp}`.\n"
            f"- **Quando (When)**: Invocado com parâmetros padrão e de limite.\n"
            f"- **Então (Then)**: Deve retornar o resultado esperado e satisfazer as asserções sem efeitos colaterais imprevistos.\n"
            f"- **Mocks**: Isolar dependências externas ou de E/S."
        )

        reproduction_steps.append(f"1. Implementar estrutura de `{sym}` em `{fp}` conforme especificações funcionais.")

    exec_summary = "\n".join(executive_summary_lines[:5]) if executive_summary_lines else "Módulo responsável pelas operações de " + caminho_ou_nome
    user_stories = "\n".join(user_stories_lines[:5]) if user_stories_lines else "- Como desenvolvedor, preciso de especificações claras do módulo."
    func_requirements = "\n\n".join(functional_specs[:5]) if functional_specs else "Requisitos funcionais do módulo."
    non_func_requirements = "- **Desempenho**: Resposta em tempo hábil para chamadas do módulo.\n- **Confiabilidade**: Tratamento robusto de erros e exceções."
    arch_model = "Composto pelos seguintes componentes principais no repositório:\n" + "\n".join(architecture_lines[:6])
    deps_integrations = "\n".join(set(dependencies_lines[:6])) if dependencies_lines else "- Dependências padrão do projeto."
    edge_cases = "\n".join(edge_cases_lines[:5]) if edge_cases_lines else "- Tratar parâmetros nulos e falhas de rede/I/O."
    tdd_suite = "\n\n".join(tdd_test_lines[:5]) if tdd_test_lines else "Suíte de testes TDD a ser implementada."
    repro_blueprint = "### Passos de Reprodução:\n" + "\n".join(reproduction_steps[:5]) + "\n\n### Checklist de Validação:\n- [ ] Suíte de testes unitários passando\n- [ ] Contratos de interface verificados\n- [ ] Tratamento de erros validado"
    pontos_entrada = "\n".join(entry_points[:8]) if entry_points else "- N/A"

    head_commit = "unknown"
    state_file = repo_path / ".rag_state.json"
    if state_file.exists():
        try:
            with open(state_file, "r", encoding="utf-8") as sf:
                s_data = json.load(sf)
                head_commit = s_data.get("last_indexed_commit", "unknown")
        except Exception:
            pass

    now_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    doc_markdown = f"""# PRD: {caminho_ou_nome}

<!-- gerado automaticamente por rag-legado-doc — não editar diretamente abaixo, exceto dentro dos blocos manual:start/manual:end -->

## 1. Executive Summary & Objectives
{exec_summary}

## 2. User Stories & Use Cases
{user_stories}

## 3. Functional Requirements
{func_requirements}

## 4. Non-Functional Requirements & Constraints
{non_func_requirements}

## 5. Data Models & System Architecture
{arch_model}

## 6. Dependencies & Integrations
{deps_integrations}

## 7. Edge Cases & Error Handling
{edge_cases}

## 8. TDD Test Suites (Unit, Integration & E2E)
{tdd_suite}

## 9. Full Reproduction Blueprint
{repro_blueprint}

## Pontos de Entrada (Código Fonte)
{pontos_entrada}

## Comportamentos Conhecidos / Observações Manuais
<!-- manual:start -->
{preserved_manual_notes}
<!-- manual:end -->

## Última Atualização
Gerado em: {now_str} | Baseado no commit: {head_commit[:7]}
"""

    doc_path.parent.mkdir(parents=True, exist_ok=True)
    doc_path.write_text(doc_markdown, encoding="utf-8")

    return {
        "status": "success",
        "caminho_gerado": str(doc_path.relative_to(repo_path)),
        "modo": modo,
        "secoes_manuais_preservadas": sections_preserved,
        "fontes_usadas": sources
    }

