# Spec — Fase 1: Motor Core (Ingestão, Chunking, Embeddings, Índice)

**Ref. PRD:** Seções 4, 5.1 (parcial), 5.2, 7
**Depende de:** —
**Bloqueia:** Fase 2

## Objetivo

Construir o pipeline que transforma um repositório em um índice vetorial local
consultável, com chunking consciente de estrutura (código e docs). Ao fim desta fase,
deve ser possível rodar um script manual que indexa um repositório e retorna resultados
de busca por similaridade simples (sem híbrido/rerank ainda — isso é Fase 2).

## Escopo

Incluso:
- Descoberta de arquivos rastreados pelo Git (`git ls-files`), respeitando
  `.gitignore` e um `.ragignore` adicional.
- Chunking de código via `tree-sitter` (por função/classe/método).
- Chunking de documentação markdown (por seção/header).
- Geração de embeddings locais (código e texto/PT-BR).
- Persistência em LanceDB.
- Script CLI de teste manual (`scripts/index_repo.py` e `scripts/search_test.py`).

Fora de escopo (fases futuras):
- Busca híbrida (BM25) e reranking.
- Exposição via MCP.
- Bootstrap automatizado / instalação.
- Atualização incremental via git hook.

## Design técnico

### Descoberta de arquivos
```python
def get_tracked_files(repo_root: Path) -> list[Path]:
    """git ls-files, filtrado por extensão suportada e .ragignore"""
```
- Extensões suportadas na v1: `.py, .js, .ts, .java, .go, .rb, .php, .md, .mdx, .rst`
  (ajustável conforme stack real do monólito).
- Arquivos > 1MB são pulados e reportados no log (provável binário/gerado).

### Chunking de código
- Um chunk por unidade lógica (função, método, classe sem métodos longos demais).
- Cada chunk inclui: assinatura, docstring/comentário imediatamente anterior, corpo.
- Metadata obrigatória por chunk:
  ```python
  {
    "chunk_id": str,          # hash determinístico do conteúdo
    "file_path": str,
    "language": str,
    "symbol_name": str,       # nome da função/classe
    "symbol_type": str,       # "function" | "class" | "method"
    "start_line": int,
    "end_line": int,
    "last_commit_hash": str,
    "last_commit_date": str,
    "last_commit_author": str,
    "content": str,
  }
  ```
- Funções/classes maiores que um limite de tokens (definir: ~800 tokens) são
  divididas com overlap de ~50 tokens, mantendo a assinatura no início de cada
  sub-chunk.

### Chunking de documentação
- Split por header (`#`, `##`, `###`), overlap de ~10-15% entre chunks adjacentes.
- Mesma metadata (sem `symbol_name`/`symbol_type`, com `section_title` no lugar).

### Embeddings
- Dois modelos: um para chunks de código, um para chunks de texto/doc (PT-BR).
- Rodar 100% local via `sentence-transformers`.
- Batch de embedding configurável (default: 32).

### Armazenamento (LanceDB)
- Uma tabela única com coluna de vetor + todos os campos de metadata acima, mais
  campo `chunk_type` (`"code"` | `"doc"`) para permitir filtro por tipo.
- Índice ANN configurado no LanceDB para busca por similaridade.

## Interfaces (v1, uso manual via CLI)

```bash
python scripts/index_repo.py --repo-path . 
python scripts/search_test.py --query "como funciona o cálculo de frete" --top-k 5
```

## Critérios de aceite

- [ ] Rodar `index_repo.py` em um repositório real do time gera um índice LanceDB
      sem erros, processando 100% dos arquivos rastreados suportados.
- [ ] Arquivos ignorados (binários, muito grandes, fora do `.gitignore`) aparecem
      listados no relatório final, não silenciosamente descartados.
- [ ] Cada chunk de código tem metadata completa e correta (validar manualmente em
      uma amostra de 20 chunks).
- [ ] Busca por similaridade simples (`search_test.py`) retorna resultados
      relevantes para 5 queries de teste definidas manualmente pelo time.
- [ ] Reprocessar o mesmo repositório duas vezes não duplica chunks (chunk_id
      determinístico evita duplicação).

## Tarefas

1. Setup do projeto (estrutura de pastas, dependências, `pyproject.toml`).
2. `ingest/discover.py` — descoberta de arquivos + filtros.
3. `ingest/parse_code.py` — chunking via tree-sitter.
4. `ingest/parse_docs.py` — chunking de markdown.
5. `index/embed.py` — geração de embeddings.
6. `index/store.py` — wrapper de escrita/leitura no LanceDB.
7. `scripts/index_repo.py` e `scripts/search_test.py`.
8. Testar em repositório real de amostra e ajustar heurísticas de chunking.
