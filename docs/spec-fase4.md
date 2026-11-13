# Spec — Fase 4: Skill de Busca, Bootstrap e Atualização Incremental

**Ref. PRD:** Seções 5.1, 5.4, 5.6
**Depende de:** Fase 3
**Bloqueia:** Fase 5

## Objetivo

Tornar o pacote instalável de ponta a ponta em qualquer repositório: um comando que
registra o MCP, instala a skill de busca e já deixa o índice pronto (bootstrap). Além
disso, implementar a atualização incremental automática via git hook.

## Escopo

Incluso:
- `skill/SKILL.md` (skill de busca de contexto).
- `install.sh` — orquestra registro do MCP + cópia da skill + bootstrap.
- `bootstrap_index.py` — indexação inicial completa, reaproveitando Fases 1-3.
- `.rag_state.json` — snapshot de estado pós-bootstrap.
- Git hook (`post-commit`/`post-merge`) para reindexação incremental.
- Idempotência: reinstalar não duplica nem corrompe o índice.

Fora de escopo:
- Skill de documentação (Fase 6).
- Publicação/distribuição do pacote como repositório próprio (Fase 5).

## Design técnico

### `skill/SKILL.md` (frontmatter)
```yaml
name: rag-legado-busca
description: Consulta a base de conhecimento local (RAG) do repositório para responder perguntas sobre comportamento de módulos, funções ou decisões do sistema legado. Use sempre que a pergunta exigir contexto que não está explícito no código aberto no editor, antes de assumir ou inferir comportamento.
```
Corpo do arquivo: instruções de quando preferir chamar `buscar_contexto` a
responder de memória, como interpretar os campos de metadata retornados (ex:
`last_commit_date` para avisar se a informação pode estar desatualizada).

### `install.sh` — fluxo
1. Validar que está na raiz de um repositório Git (`git rev-parse --show-toplevel`).
2. Verificar se já existe `.rag_state.json`:
   - Se sim → perguntar: reindexar do zero ou manter incremental.
   - Se não → seguir para bootstrap.
3. Copiar `skill/` para `.claude/skills/rag-legado-busca/` e para
   `.github/skills/rag-legado-busca/`.
4. Registrar o MCP server no `.mcp.json` do projeto (criar se não existir, fazer
   merge se já existir).
5. Rodar `bootstrap_index.py`.
6. Instalar o git hook (`post-commit`, `post-merge`) em `.git/hooks/`.
7. Imprimir relatório final (arquivos indexados, chunks, tempo, avisos).

### `bootstrap_index.py`
- Reaproveita `ingest`, `index`, `retrieve` das Fases 1-2 diretamente (sem passar
  pelo MCP — é execução local direta, mais rápida para lote grande).
- Processa em batches de 50 arquivos, com barra de progresso no terminal.
- Ao final, grava `.rag_state.json`:
  ```json
  {
    "last_indexed_commit": "<hash>",
    "indexed_at": "<iso8601>",
    "total_files": 0,
    "total_chunks": 0
  }
  ```

### Atualização incremental (git hook)
- Hook shell simples que chama `python mcp_server/incremental_update.py`.
- `incremental_update.py`:
  1. Lê `last_indexed_commit` de `.rag_state.json`.
  2. `git diff --name-only <last_indexed_commit> HEAD` → lista de arquivos alterados.
  3. Para arquivos deletados: remove chunks correspondentes do índice (por
     `file_path`).
  4. Para arquivos modificados/novos: reprocessa (parse → chunk → embed → upsert).
  5. Atualiza `.rag_state.json` com o novo HEAD.
- Roda em background (não deve travar o `git commit` do usuário) — usar processo
  desacoplado (`nohup`/`&` ou fila simples).

### Idempotência
- `chunk_id` determinístico (hash do conteúdo) garante que reprocessar o mesmo
  conteúdo faz upsert, não duplicação.
- `install.sh` detecta instalação prévia (skill já copiada, MCP já registrado) e
  não duplica entradas de configuração.

## Critérios de aceite

- [ ] Rodar `install.sh` em um repositório limpo faz bootstrap completo e deixa o
      MCP + skill prontos para uso no Claude Code, sem passos manuais adicionais.
- [ ] Rodar `install.sh` de novo no mesmo repositório não duplica configuração nem
      reindexação (comportamento idempotente confirmado).
- [ ] Um commit após a instalação dispara o hook, e o índice reflete a mudança em
      até alguns segundos/minutos, sem exigir ação manual do usuário.
- [ ] Arquivo deletado no commit tem seus chunks removidos do índice
      (validado consultando `status_indice`).
- [ ] `install.sh` funciona em uma máquina limpa (sem dependências pré-instaladas
      além de Python), instalando o que for necessário ou reportando claramente o
      que falta.

## Tarefas

1. Escrever `skill/SKILL.md` com a description afinada (testar auto-invocação).
2. `bootstrap_index.py`.
3. `install.sh` (detecção de repo, cópia de skill, registro de MCP).
4. `incremental_update.py` + script de hook.
5. Testes de idempotência (rodar install.sh 2x, commitar 2x).
6. Testar fluxo completo do zero em um repositório de exemplo.
