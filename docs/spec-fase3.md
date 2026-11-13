# Spec — Fase 3: MCP Server

**Ref. PRD:** Seção 5.5
**Depende de:** Fase 2
**Bloqueia:** Fase 4

## Objetivo

Expor o motor de busca (Fases 1-2) como um servidor MCP local, consumível por
qualquer agente compatível (Claude Code, GitHub Copilot). Esta fase transforma
scripts CLI em um serviço de longa duração com tools bem definidas.

## Escopo

Incluso:
- Servidor MCP (`mcp_server/server.py`) usando o `mcp` SDK, rodando via stdio.
- Três tools: `buscar_contexto`, `reindexar`, `status_indice`.
- Configuração local (`.mcp.json` de exemplo) para registro em Claude Code.
- Configuração equivalente documentada para GitHub Copilot.
- Tratamento de erro gracioso (índice inexistente, repo não indexado ainda, etc.).

Fora de escopo:
- Bootstrap automatizado / `install.sh` (Fase 4).
- Tool `gerar_doc_modulo` (Fase 6).

## Design técnico

### Tool: `buscar_contexto`
```
buscar_contexto(query: str, filtros: dict | None = None, top_k: int = 5) -> dict
```
- `filtros` aceita: `chunk_type` (`"code"|"doc"`), `language`, `file_path_prefix`.
- Retorno:
  ```json
  {
    "resultados": [
      {
        "content": "...",
        "file_path": "...",
        "symbol_name": "...",
        "score": 0.87,
        "last_commit_date": "..."
      }
    ],
    "total_encontrado": 5
  }
  ```
- Internamente chama `hybrid_search` + `rerank` da Fase 2.

### Tool: `reindexar`
```
reindexar(escopo: str | None = None) -> dict
```
- `escopo=None` → reindexação completa.
- `escopo="<caminho>"` → reindexa apenas arquivo(s)/pasta específica.
- Retorno com contagem de chunks processados e tempo decorrido.
- **Nota:** nesta fase ainda é reindexação síncrona e manual (chamada explícita pelo
  usuário/agente); o gatilho automático via git hook é Fase 4.

### Tool: `status_indice`
```
status_indice() -> dict
```
- Retorna: nº total de chunks, nº de arquivos indexados, hash do último commit
  indexado (se `.rag_state.json` existir), data da última indexação.
- Se o índice ainda não existe, retorna um estado claro indicando isso (para o
  agente poder orientar o usuário a rodar o bootstrap).

### Tratamento de erros
- Índice ausente → mensagem clara nas três tools, não exception genérica.
- Timeout de embedding/reranking → fallback para busca vetorial pura, com aviso no
  retorno (`degraded: true`).

## Interfaces de configuração

`.mcp.json` (exemplo, raiz do projeto):
```json
{
  "mcpServers": {
    "rag-legado": {
      "command": "python",
      "args": ["mcp_server/server.py"],
      "cwd": "."
    }
  }
}
```

## Critérios de aceite

- [ ] Servidor MCP inicia sem erros e responde ao handshake de um cliente MCP local.
- [ ] `buscar_contexto` chamada a partir do Claude Code retorna resultados
      coerentes para uma pergunta real sobre o repositório indexado.
- [ ] `status_indice` reflete corretamente o estado real do índice (validado com
      índice vazio, parcial e completo).
- [ ] `reindexar` com escopo específico atualiza apenas os chunks daquele
      caminho, sem tocar no resto do índice.
- [ ] Erros de índice ausente não derrubam o servidor — retornam mensagem tratável
      pelo agente.

## Tarefas

1. Setup do `mcp` SDK e esqueleto do servidor.
2. Implementar `buscar_contexto` reaproveitando Fase 2.
3. Implementar `status_indice` (leitura de `.rag_state.json` + contagem no LanceDB).
4. Implementar `reindexar` (completo e por escopo).
5. Tratamento de erros e mensagens de estado degradado.
6. Testar handshake e chamadas reais a partir do Claude Code.
7. Documentar configuração equivalente para GitHub Copilot.
