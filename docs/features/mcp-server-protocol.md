# PRD: rag-legado-skill/mcp_server/server.py

<!-- gerado automaticamente por rag-legado-doc — não editar diretamente abaixo, exceto dentro dos blocos manual:start/manual:end -->

## 1. Executive Summary & Objectives
- **gerar_doc_modulo** (`rag-legado-skill/mcp_server/server.py`): def gerar_doc_modulo(caminho_ou_nome: str, modo: str = "criar") -> dict[str, Any]:
- **buscar_contexto** (`rag-legado-skill/mcp_server/server.py`): def buscar_contexto(query: str, filtros: dict[str, Any] | None = None, top_k: int = 5) -> dict[str, Any]:
- **main** (`rag-legado-skill/mcp_server/server.py`): def main():
- **get_repo_root** (`rag-legado-skill/mcp_server/server.py`): def get_repo_root() -> Path:
- **reindexar** (`rag-legado-skill/mcp_server/server.py`): def reindexar(escopo: str | None = None) -> dict[str, Any]:

## 2. User Stories & Use Cases
- Como desenvolvedor/sistema, necessito que `gerar_doc_modulo` execute conforme especificado em `rag-legado-skill/mcp_server/server.py` para garantir o funcionamento correto da funcionalidade `rag-legado-skill/mcp_server/server.py`.
- Como desenvolvedor/sistema, necessito que `buscar_contexto` execute conforme especificado em `rag-legado-skill/mcp_server/server.py` para garantir o funcionamento correto da funcionalidade `rag-legado-skill/mcp_server/server.py`.
- Como desenvolvedor/sistema, necessito que `main` execute conforme especificado em `rag-legado-skill/mcp_server/server.py` para garantir o funcionamento correto da funcionalidade `rag-legado-skill/mcp_server/server.py`.
- Como desenvolvedor/sistema, necessito que `get_repo_root` execute conforme especificado em `rag-legado-skill/mcp_server/server.py` para garantir o funcionamento correto da funcionalidade `rag-legado-skill/mcp_server/server.py`.
- Como desenvolvedor/sistema, necessito que `reindexar` execute conforme especificado em `rag-legado-skill/mcp_server/server.py` para garantir o funcionamento correto da funcionalidade `rag-legado-skill/mcp_server/server.py`.

## 3. Functional Requirements
### gerar_doc_modulo
- **Localização**: `rag-legado-skill/mcp_server/server.py` (linhas 133-139)
- **Descrição**: def gerar_doc_modulo(caminho_ou_nome: str, modo: str = "criar") -> dict[str, Any]:
- **Regra de Negócio**: Deve processar entradas válidas sem falhas e garantir a integridade dos dados retornados.

### buscar_contexto
- **Localização**: `rag-legado-skill/mcp_server/server.py` (linhas 23-40)
- **Descrição**: def buscar_contexto(query: str, filtros: dict[str, Any] | None = None, top_k: int = 5) -> dict[str, Any]:
- **Regra de Negócio**: Deve processar entradas válidas sem falhas e garantir a integridade dos dados retornados.

### main
- **Localização**: `rag-legado-skill/mcp_server/server.py` (linhas 140-145)
- **Descrição**: def main():
- **Regra de Negócio**: Deve processar entradas válidas sem falhas e garantir a integridade dos dados retornados.

### get_repo_root
- **Localização**: `rag-legado-skill/mcp_server/server.py` (linhas 18-22)
- **Descrição**: def get_repo_root() -> Path:
- **Regra de Negócio**: Deve processar entradas válidas sem falhas e garantir a integridade dos dados retornados.

### reindexar
- **Localização**: `rag-legado-skill/mcp_server/server.py` (linhas 41-107)
- **Descrição**: def reindexar(escopo: str | None = None) -> dict[str, Any]:
- **Regra de Negócio**: Deve processar entradas válidas sem falhas e garantir a integridade dos dados retornados.

## 4. Non-Functional Requirements & Constraints
- **Desempenho**: Resposta em tempo hábil para chamadas do módulo.
- **Confiabilidade**: Tratamento robusto de erros e exceções.

## 5. Data Models & System Architecture
Composto pelos seguintes componentes principais no repositório:
- Componente `gerar_doc_modulo` em `rag-legado-skill/mcp_server/server.py`
- Componente `buscar_contexto` em `rag-legado-skill/mcp_server/server.py`
- Componente `main` em `rag-legado-skill/mcp_server/server.py`
- Componente `get_repo_root` em `rag-legado-skill/mcp_server/server.py`
- Componente `reindexar` em `rag-legado-skill/mcp_server/server.py`
- Componente `status_indice` em `rag-legado-skill/mcp_server/server.py`

## 6. Dependencies & Integrations
- Importações/Dependências de `rag-legado-skill/mcp_server/server.py`

## 7. Edge Cases & Error Handling
- Falha ou entrada inválida em `gerar_doc_modulo` (`rag-legado-skill/mcp_server/server.py`): validar tratamento de erros e exceções esperadas.
- Falha ou entrada inválida em `buscar_contexto` (`rag-legado-skill/mcp_server/server.py`): validar tratamento de erros e exceções esperadas.
- Falha ou entrada inválida em `main` (`rag-legado-skill/mcp_server/server.py`): validar tratamento de erros e exceções esperadas.
- Falha ou entrada inválida em `get_repo_root` (`rag-legado-skill/mcp_server/server.py`): validar tratamento de erros e exceções esperadas.
- Falha ou entrada inválida em `reindexar` (`rag-legado-skill/mcp_server/server.py`): validar tratamento de erros e exceções esperadas.

## 8. TDD Test Suites (Unit, Integration & E2E)
### Test Spec: `gerar_doc_modulo`
- **Dado (Given)**: Instância de `gerar_doc_modulo` configurada com contexto válido em `rag-legado-skill/mcp_server/server.py`.
- **Quando (When)**: Invocado com parâmetros padrão e de limite.
- **Então (Then)**: Deve retornar o resultado esperado e satisfazer as asserções sem efeitos colaterais imprevistos.
- **Mocks**: Isolar dependências externas ou de E/S.

### Test Spec: `buscar_contexto`
- **Dado (Given)**: Instância de `buscar_contexto` configurada com contexto válido em `rag-legado-skill/mcp_server/server.py`.
- **Quando (When)**: Invocado com parâmetros padrão e de limite.
- **Então (Then)**: Deve retornar o resultado esperado e satisfazer as asserções sem efeitos colaterais imprevistos.
- **Mocks**: Isolar dependências externas ou de E/S.

### Test Spec: `main`
- **Dado (Given)**: Instância de `main` configurada com contexto válido em `rag-legado-skill/mcp_server/server.py`.
- **Quando (When)**: Invocado com parâmetros padrão e de limite.
- **Então (Then)**: Deve retornar o resultado esperado e satisfazer as asserções sem efeitos colaterais imprevistos.
- **Mocks**: Isolar dependências externas ou de E/S.

### Test Spec: `get_repo_root`
- **Dado (Given)**: Instância de `get_repo_root` configurada com contexto válido em `rag-legado-skill/mcp_server/server.py`.
- **Quando (When)**: Invocado com parâmetros padrão e de limite.
- **Então (Then)**: Deve retornar o resultado esperado e satisfazer as asserções sem efeitos colaterais imprevistos.
- **Mocks**: Isolar dependências externas ou de E/S.

### Test Spec: `reindexar`
- **Dado (Given)**: Instância de `reindexar` configurada com contexto válido em `rag-legado-skill/mcp_server/server.py`.
- **Quando (When)**: Invocado com parâmetros padrão e de limite.
- **Então (Then)**: Deve retornar o resultado esperado e satisfazer as asserções sem efeitos colaterais imprevistos.
- **Mocks**: Isolar dependências externas ou de E/S.

## 9. Full Reproduction Blueprint
### Passos de Reprodução:
1. Implementar estrutura de `gerar_doc_modulo` em `rag-legado-skill/mcp_server/server.py` conforme especificações funcionais.
1. Implementar estrutura de `buscar_contexto` em `rag-legado-skill/mcp_server/server.py` conforme especificações funcionais.
1. Implementar estrutura de `main` em `rag-legado-skill/mcp_server/server.py` conforme especificações funcionais.
1. Implementar estrutura de `get_repo_root` em `rag-legado-skill/mcp_server/server.py` conforme especificações funcionais.
1. Implementar estrutura de `reindexar` em `rag-legado-skill/mcp_server/server.py` conforme especificações funcionais.

### Checklist de Validação:
- [ ] Suíte de testes unitários passando
- [ ] Contratos de interface verificados
- [ ] Tratamento de erros validado

## Pontos de Entrada (Código Fonte)
- [rag-legado-skill/mcp_server/server.py#L133-L139](file://rag-legado-skill/mcp_server/server.py) — `gerar_doc_modulo`
- [rag-legado-skill/mcp_server/server.py#L23-L40](file://rag-legado-skill/mcp_server/server.py) — `buscar_contexto`
- [rag-legado-skill/mcp_server/server.py#L140-L145](file://rag-legado-skill/mcp_server/server.py) — `main`
- [rag-legado-skill/mcp_server/server.py#L18-L22](file://rag-legado-skill/mcp_server/server.py) — `get_repo_root`
- [rag-legado-skill/mcp_server/server.py#L41-L107](file://rag-legado-skill/mcp_server/server.py) — `reindexar`
- [rag-legado-skill/mcp_server/server.py#L108-L132](file://rag-legado-skill/mcp_server/server.py) — `status_indice`

## Comportamentos Conhecidos / Observações Manuais
<!-- manual:start -->
<!-- Espaço para observações humanas, post-mortems relacionados, etc. -->
<!-- manual:end -->

## Última Atualização
Gerado em: 2026-09-03 01:07:37 | Baseado no commit: unknown
