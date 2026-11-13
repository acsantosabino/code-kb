## Why

O projeto `code-kb` evoluiu através de múltiplas mudanças incrementais arquivadas (`local-rag-code-kb`, `detailed-feature-doc-requirements`, `fix-rag-doc-filtering`, `per-feature-prd-docs`), resultando em várias especificações (`mcp-server`, `hybrid-search`, `rag-engine`, `agent-skills`, `feature-doc-isolation`, `per-feature-prd-catalog`). É necessário consolidar em uma nova spec todas as capacidades atuais do ecossistema RAG/Documentação Legada em um catálogo centralizado e atualizado (`system-capabilities`), garantindo clareza arquitetural e completude operacional para o repositório.

## What Changes

- Consolidar as capacidades de indexação local, busca híbrida (BM25 + vetorial), integração via servidor MCP, suporte a skills de agente AI, isolamento de contexto de documentação e catálogo de PRDs por funcionalidade em uma única especificação unificada.
- Criar a nova especificação `system-capabilities` refletindo todos os requisitos comportamentais e contratos do sistema como ele opera atualmente.

## Capabilities

### New Capabilities
- `system-capabilities`: Consolidação de todas as capacidades operacionais e arquiteturais atuais do sistema local-rag-code-kb (RAG local, busca híbrida, servidor MCP, skills de agente, isolamento de docs e catálogo PRD).

### Modified Capabilities
<!-- Nenhuma especificação existente terá seu comportamento alterado; trata-se de uma consolidação de capacidades atuais em uma nova spec. -->

## Impact

- `openspec/specs/system-capabilities/spec.md`: Nova especificação de capacidade consolidada do sistema.
- Nenhuma alteração disruptiva no código-fonte existente do sistema.
