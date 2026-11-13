---
name: rag-legado-doc
description: Gera ou atualiza documentação de funcionalidades do sistema legado em docs/features/, a partir da base de conhecimento RAG já indexada. Use apenas quando o usuário pedir explicitamente para documentar, gerar doc de, ou explicar em formato de documento um módulo ou funcionalidade — não é acionada automaticamente.
---

# RAG Legado — Geração de PRD Detalhado de Módulo / Feature

Esta skill permite gerar ou atualizar documentação técnica detalhada no formato **PRD (Product Requirement Document)** orientada a TDD para um módulo ou funcionalidade do sistema legado, salvando o documento resultante em `docs/features/<nome-modulo>.md`.

## Quando usar
- Quando o usuário pedir explicitamente: *"gere uma doc do módulo billing"*, *"documente a funcionalidade de busca em formato PRD"*, ou *"atualize a documentação de ingestão"*.
- **Atenção:** Esta skill é acionada estritamente sob demanda explícita do usuário.

## Estrutura Padrão do PRD Gerado
O documento gerado segue obrigatoriamente a estrutura padronizada de PRD:
1. **Executive Summary & Objectives**: Visão geral e metas do módulo.
2. **User Stories & Use Cases**: Histórias de usuário e casos de uso associados.
3. **Functional Requirements**: Especificações detalhadas de funções e regras de negócio.
4. **Non-Functional Requirements & Constraints**: Desempenho, segurança e restrições.
5. **Data Models & System Architecture**: Modelos de dados e arquitetura de componentes.
6. **Dependencies & Integrations**: Módulos e serviços dependentes.
7. **Edge Cases & Error Handling**: Trata de erros e cenários de exceção.
8. **TDD Test Suites (Unit, Integration & E2E)**: Especificações de testes executáveis (Given-When-Then, mocks e asserções).
9. **Full Reproduction Blueprint**: Passo a passo detalhado para reprodução 100% fiel da funcionalidade em um novo projeto.

## Ferramenta principal
Invoque a tool MCP `gerar_doc_modulo`:
```json
{
  "caminho_ou_nome": "mcp_server/ingest",
  "modo": "criar"
}
```

### Modos suportados:
- `"criar"`: Cria um novo documento PRD em `docs/features/<slug>.md`.
- `"atualizar"`: Atualiza o documento PRD preservando integralmente o conteúdo editado manualmente entre os marcadores `<!-- manual:start -->` e `<!-- manual:end -->`.

