# PRD: rag-legado-skill/mcp_server/ingest

<!-- gerado automaticamente por rag-legado-doc — não editar diretamente abaixo, exceto dentro dos blocos manual:start/manual:end -->

## 1. Executive Summary & Objectives
- **load_ragignore_patterns** (`rag-legado-skill/mcp_server/ingest/discover.py`): def load_ragignore_patterns(repo_root: Path) -> list[str]:
- **get_tracked_files** (`rag-legado-skill/mcp_server/ingest/discover.py`): def get_tracked_files(repo_root: Path | str) -> tuple[list[Path], list[dict]]:
- **block_1_1** (`rag-legado-skill/mcp_server/ingest/__init__.py`): """Ingestion and parsing module for code and markdown."""
- **parse_code_file_fallback** (`rag-legado-skill/mcp_server/ingest/parse_code.py`): def parse_code_file_fallback(
- **parse_markdown_file** (`rag-legado-skill/mcp_server/ingest/parse_docs.py`): def parse_markdown_file(

## 2. User Stories & Use Cases
- Como desenvolvedor/sistema, necessito que `load_ragignore_patterns` execute conforme especificado em `rag-legado-skill/mcp_server/ingest/discover.py` para garantir o funcionamento correto da funcionalidade `rag-legado-skill/mcp_server/ingest`.
- Como desenvolvedor/sistema, necessito que `get_tracked_files` execute conforme especificado em `rag-legado-skill/mcp_server/ingest/discover.py` para garantir o funcionamento correto da funcionalidade `rag-legado-skill/mcp_server/ingest`.
- Como desenvolvedor/sistema, necessito que `block_1_1` execute conforme especificado em `rag-legado-skill/mcp_server/ingest/__init__.py` para garantir o funcionamento correto da funcionalidade `rag-legado-skill/mcp_server/ingest`.
- Como desenvolvedor/sistema, necessito que `parse_code_file_fallback` execute conforme especificado em `rag-legado-skill/mcp_server/ingest/parse_code.py` para garantir o funcionamento correto da funcionalidade `rag-legado-skill/mcp_server/ingest`.
- Como desenvolvedor/sistema, necessito que `parse_markdown_file` execute conforme especificado em `rag-legado-skill/mcp_server/ingest/parse_docs.py` para garantir o funcionamento correto da funcionalidade `rag-legado-skill/mcp_server/ingest`.

## 3. Functional Requirements
### load_ragignore_patterns
- **Localização**: `rag-legado-skill/mcp_server/ingest/discover.py` (linhas 15-32)
- **Descrição**: def load_ragignore_patterns(repo_root: Path) -> list[str]:
- **Regra de Negócio**: Deve processar entradas válidas sem falhas e garantir a integridade dos dados retornados.

### get_tracked_files
- **Localização**: `rag-legado-skill/mcp_server/ingest/discover.py` (linhas 48-107)
- **Descrição**: def get_tracked_files(repo_root: Path | str) -> tuple[list[Path], list[dict]]:
- **Regra de Negócio**: Deve processar entradas válidas sem falhas e garantir a integridade dos dados retornados.

### block_1_1
- **Localização**: `rag-legado-skill/mcp_server/ingest/__init__.py` (linhas 1-1)
- **Descrição**: """Ingestion and parsing module for code and markdown."""
- **Regra de Negócio**: Deve processar entradas válidas sem falhas e garantir a integridade dos dados retornados.

### parse_code_file_fallback
- **Localização**: `rag-legado-skill/mcp_server/ingest/parse_code.py` (linhas 42-138)
- **Descrição**: def parse_code_file_fallback(
- **Regra de Negócio**: Deve processar entradas válidas sem falhas e garantir a integridade dos dados retornados.

### parse_markdown_file
- **Localização**: `rag-legado-skill/mcp_server/ingest/parse_docs.py` (linhas 8-91)
- **Descrição**: def parse_markdown_file(
- **Regra de Negócio**: Deve processar entradas válidas sem falhas e garantir a integridade dos dados retornados.

## 4. Non-Functional Requirements & Constraints
- **Desempenho**: Resposta em tempo hábil para chamadas do módulo.
- **Confiabilidade**: Tratamento robusto de erros e exceções.

## 5. Data Models & System Architecture
Composto pelos seguintes componentes principais no repositório:
- Componente `load_ragignore_patterns` em `rag-legado-skill/mcp_server/ingest/discover.py`
- Componente `get_tracked_files` em `rag-legado-skill/mcp_server/ingest/discover.py`
- Componente `block_1_1` em `rag-legado-skill/mcp_server/ingest/__init__.py`
- Componente `parse_code_file_fallback` em `rag-legado-skill/mcp_server/ingest/parse_code.py`
- Componente `parse_markdown_file` em `rag-legado-skill/mcp_server/ingest/parse_docs.py`
- Componente `parse_code_file` em `rag-legado-skill/mcp_server/ingest/parse_code.py`

## 6. Dependencies & Integrations
- Importações/Dependências de `rag-legado-skill/mcp_server/ingest/__init__.py`
- Importações/Dependências de `rag-legado-skill/mcp_server/ingest/parse_code.py`
- Importações/Dependências de `rag-legado-skill/mcp_server/ingest/parse_docs.py`
- Importações/Dependências de `rag-legado-skill/mcp_server/ingest/discover.py`

## 7. Edge Cases & Error Handling
- Falha ou entrada inválida em `load_ragignore_patterns` (`rag-legado-skill/mcp_server/ingest/discover.py`): validar tratamento de erros e exceções esperadas.
- Falha ou entrada inválida em `get_tracked_files` (`rag-legado-skill/mcp_server/ingest/discover.py`): validar tratamento de erros e exceções esperadas.
- Falha ou entrada inválida em `block_1_1` (`rag-legado-skill/mcp_server/ingest/__init__.py`): validar tratamento de erros e exceções esperadas.
- Falha ou entrada inválida em `parse_code_file_fallback` (`rag-legado-skill/mcp_server/ingest/parse_code.py`): validar tratamento de erros e exceções esperadas.
- Falha ou entrada inválida em `parse_markdown_file` (`rag-legado-skill/mcp_server/ingest/parse_docs.py`): validar tratamento de erros e exceções esperadas.

## 8. TDD Test Suites (Unit, Integration & E2E)
### Test Spec: `load_ragignore_patterns`
- **Dado (Given)**: Instância de `load_ragignore_patterns` configurada com contexto válido em `rag-legado-skill/mcp_server/ingest/discover.py`.
- **Quando (When)**: Invocado com parâmetros padrão e de limite.
- **Então (Then)**: Deve retornar o resultado esperado e satisfazer as asserções sem efeitos colaterais imprevistos.
- **Mocks**: Isolar dependências externas ou de E/S.

### Test Spec: `get_tracked_files`
- **Dado (Given)**: Instância de `get_tracked_files` configurada com contexto válido em `rag-legado-skill/mcp_server/ingest/discover.py`.
- **Quando (When)**: Invocado com parâmetros padrão e de limite.
- **Então (Then)**: Deve retornar o resultado esperado e satisfazer as asserções sem efeitos colaterais imprevistos.
- **Mocks**: Isolar dependências externas ou de E/S.

### Test Spec: `block_1_1`
- **Dado (Given)**: Instância de `block_1_1` configurada com contexto válido em `rag-legado-skill/mcp_server/ingest/__init__.py`.
- **Quando (When)**: Invocado com parâmetros padrão e de limite.
- **Então (Then)**: Deve retornar o resultado esperado e satisfazer as asserções sem efeitos colaterais imprevistos.
- **Mocks**: Isolar dependências externas ou de E/S.

### Test Spec: `parse_code_file_fallback`
- **Dado (Given)**: Instância de `parse_code_file_fallback` configurada com contexto válido em `rag-legado-skill/mcp_server/ingest/parse_code.py`.
- **Quando (When)**: Invocado com parâmetros padrão e de limite.
- **Então (Then)**: Deve retornar o resultado esperado e satisfazer as asserções sem efeitos colaterais imprevistos.
- **Mocks**: Isolar dependências externas ou de E/S.

### Test Spec: `parse_markdown_file`
- **Dado (Given)**: Instância de `parse_markdown_file` configurada com contexto válido em `rag-legado-skill/mcp_server/ingest/parse_docs.py`.
- **Quando (When)**: Invocado com parâmetros padrão e de limite.
- **Então (Then)**: Deve retornar o resultado esperado e satisfazer as asserções sem efeitos colaterais imprevistos.
- **Mocks**: Isolar dependências externas ou de E/S.

## 9. Full Reproduction Blueprint
### Passos de Reprodução:
1. Implementar estrutura de `load_ragignore_patterns` em `rag-legado-skill/mcp_server/ingest/discover.py` conforme especificações funcionais.
1. Implementar estrutura de `get_tracked_files` em `rag-legado-skill/mcp_server/ingest/discover.py` conforme especificações funcionais.
1. Implementar estrutura de `block_1_1` em `rag-legado-skill/mcp_server/ingest/__init__.py` conforme especificações funcionais.
1. Implementar estrutura de `parse_code_file_fallback` em `rag-legado-skill/mcp_server/ingest/parse_code.py` conforme especificações funcionais.
1. Implementar estrutura de `parse_markdown_file` em `rag-legado-skill/mcp_server/ingest/parse_docs.py` conforme especificações funcionais.

### Checklist de Validação:
- [ ] Suíte de testes unitários passando
- [ ] Contratos de interface verificados
- [ ] Tratamento de erros validado

## Pontos de Entrada (Código Fonte)
- [rag-legado-skill/mcp_server/ingest/discover.py#L15-L32](file://rag-legado-skill/mcp_server/ingest/discover.py) — `load_ragignore_patterns`
- [rag-legado-skill/mcp_server/ingest/discover.py#L48-L107](file://rag-legado-skill/mcp_server/ingest/discover.py) — `get_tracked_files`
- [rag-legado-skill/mcp_server/ingest/__init__.py#L1-L1](file://rag-legado-skill/mcp_server/ingest/__init__.py) — `block_1_1`
- [rag-legado-skill/mcp_server/ingest/parse_code.py#L42-L138](file://rag-legado-skill/mcp_server/ingest/parse_code.py) — `parse_code_file_fallback`
- [rag-legado-skill/mcp_server/ingest/parse_docs.py#L8-L91](file://rag-legado-skill/mcp_server/ingest/parse_docs.py) — `parse_markdown_file`
- [rag-legado-skill/mcp_server/ingest/parse_code.py#L139-L224](file://rag-legado-skill/mcp_server/ingest/parse_code.py) — `parse_code_file`
- [rag-legado-skill/mcp_server/ingest/parse_code.py#L37-L41](file://rag-legado-skill/mcp_server/ingest/parse_code.py) — `generate_chunk_id`
- [rag-legado-skill/mcp_server/ingest/parse_code.py#L10-L36](file://rag-legado-skill/mcp_server/ingest/parse_code.py) — `get_git_commit_info`

## Comportamentos Conhecidos / Observações Manuais
<!-- manual:start -->
<!-- Espaço para observações humanas, post-mortems relacionados, etc. -->
<!-- manual:end -->

## Última Atualização
Gerado em: 2026-09-03 01:07:34 | Baseado no commit: unknown
