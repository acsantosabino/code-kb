# Spec — Fase 2: Busca Híbrida + Reranking

**Ref. PRD:** Seção 5.3
**Depende de:** Fase 1
**Bloqueia:** Fase 3

## Objetivo

Melhorar a qualidade da recuperação combinando busca vetorial (semântica) com busca
por keyword (BM25), e aplicar reranking sobre os candidatos antes de retornar o
resultado final. Código costuma ter nomes exatos (função, variável, classe) que a
busca puramente vetorial não prioriza bem — BM25 resolve isso.

## Escopo

Incluso:
- Índice BM25 sobre o mesmo conjunto de chunks (paralelo ao índice vetorial).
- Combinação dos dois rankings (fusão de scores).
- Reranking dos top-N candidatos combinados via cross-encoder local.
- Script CLI atualizado para comparar busca simples (Fase 1) vs. híbrida (Fase 2).
- Suíte mínima de queries de avaliação (golden set) definida com o time.

Fora de escopo:
- Exposição via MCP (Fase 3).
- Filtros avançados por metadata na interface final de tool (isso é detalhado na
  Fase 3, mas o mecanismo de filtro por metadata já deve existir no `store.py`).

## Design técnico

### Índice BM25
- Construído a partir do texto bruto de cada chunk (`content` + `symbol_name`/
  `section_title` com peso maior).
- Persistido em disco (ex: pickle do `rank_bm25.BM25Okapi`) ao lado do LanceDB,
  reconstruído nas reindexações.

### Fusão de rankings
- Estratégia: Reciprocal Rank Fusion (RRF) entre o top-K vetorial e o top-K BM25,
  em vez de combinar scores brutos (escalas diferentes).
- Parâmetro `k` da fórmula RRF configurável (default: 60).
- Retornar top-N (default: 20) candidatos fundidos para a etapa de reranking.

### Reranking
- Cross-encoder local (`bge-reranker-base` ou equivalente) recebe pares
  `(query, chunk.content)` para os N candidatos e reordena.
- Retornar top-K final (default: 5) após reranking, com score de relevância anexado.

### Avaliação
- Golden set: 15-20 pares (query real do time, chunk esperado) documentados em
  `eval/golden_set.jsonl`.
- Métrica simples: recall@5 (o chunk esperado está entre os 5 retornados?).
- Rodar avaliação comparando busca simples vs. híbrida+rerank, documentar ganho.

## Interfaces

```bash
python scripts/search_test.py --query "..." --mode hybrid --top-k 5
python scripts/evaluate.py --golden-set eval/golden_set.jsonl
```

## Critérios de aceite

- [ ] Busca híbrida implementada e funcionando sobre o índice da Fase 1, sem
      necessidade de reindexar do zero.
- [ ] Reranking aplicado e mensuravelmente melhora a ordenação em pelo menos 3 das
      queries do golden set (comparado a vetorial puro).
- [ ] `evaluate.py` roda e reporta recall@5 para busca simples vs. híbrida+rerank.
- [ ] Tempo de resposta de uma busca híbrida+rerank fica abaixo de 2s em máquina
      local comum, para um índice de repositório médio.

## Tarefas

1. `retrieve/bm25_index.py` — construção e persistência do índice BM25.
2. `retrieve/hybrid_search.py` — fusão RRF entre vetorial e BM25.
3. `retrieve/rerank.py` — cross-encoder local.
4. `eval/golden_set.jsonl` — golden set inicial (colaborativo com o time).
5. `scripts/evaluate.py` — script de avaliação com recall@5.
6. Ajustar parâmetros (K de fusão, top-N pré-rerank, top-K final) com base na
   avaliação.
