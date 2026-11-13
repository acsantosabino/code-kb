---
name: rag-legado-busca
description: Consulta a base de conhecimento local (RAG) do repositório para responder perguntas sobre comportamento de módulos, funções ou decisões do sistema legado. Use sempre que a pergunta exigir contexto que não está explícito no código aberto no editor, antes de assumir ou inferir comportamento.
---

# RAG Legado — Busca de Contexto

Esta skill permite consultar o repositório através da base de conhecimento local RAG (Retrieval-Augmented Generation), utilizando busca híbrida (vetorial dense + BM25 keyword) e reranking por cross-encoder.

## Quando usar
- Para entender regras de negócio ou comportamentos de módulos antigos/legados não visíveis no arquivo atual.
- Antes de responder a dúvidas sobre arquitetura, assinaturas de funções ou integrações entre componentes.
- Para verificar histórico de commits e autores de funções/classes críticas.

## Ferramenta principal
Invoque a tool MCP `buscar_contexto`:
```json
{
  "query": "Como funciona o calculo de frete e impostos",
  "top_k": 5,
  "filtros": {
    "chunk_type": "code"
  }
}
```

### Parâmetros de Filtro Suportados:
- `chunk_type`: `"code"` para código fonte ou `"doc"` para documentação markdown.
- `language`: ex: `"python"`, `"typescript"`, `"java"`.
- `file_path_prefix`: ex: `"src/billing/"`.

## Interpretando os resultados
- `file_path`: Caminho exato do arquivo no repositório.
- `start_line` e `end_line`: Intervalo de linhas onde a função/classe reside.
- `symbol_name`: Nome da função ou classe identificada via AST (tree-sitter).
- `last_commit_date` e `last_commit_hash`: Metadados do último commit que alterou o trecho. Se a data for antiga, atente-se para possíveis alterações recentes não sincronizadas.
