# PRD — Base de Conhecimento (RAG Local) e Skills para Agentes de Código

**Autor:** Arthur
**Status:** Rascunho v2
**Data:** 10/08/2026

---

## 1. Contexto e problema

O time opera um sistema monolítico legado com documentação mínima e alto volume de
incidentes. Hoje, cada agente de programação (Claude Code, GitHub Copilot) atua sem
memória do histórico do repositório: perde contexto sobre decisões, padrões internos e
comportamento de módulos que só existe na cabeça de quem já resolveu incidentes
parecidos antes.

Este projeto cria um pacote **portátil** que qualquer repositório pode instalar para
dar a esses agentes acesso a uma base de conhecimento local (RAG) construída a partir
do próprio repositório — código e documentos — sem depender de serviços externos. O
pacote inclui duas skills complementares:

1. **Skill de busca de contexto** — responde perguntas pontuais consultando a base RAG.
2. **Skill de documentação** — usa a mesma base para gerar/atualizar documentação
   estruturada das funcionalidades do sistema, sob demanda do usuário.

Isso também se conecta ao framework de post-mortems em desenho pelo time: cada
incidente resolvido pode alimentar a base RAG, e a skill de documentação é o mecanismo
que transforma esse conhecimento acumulado em documentação viva do monólito.

## 2. Objetivos

- Permitir que agentes de código (Claude Code e GitHub Copilot) consultem contexto
  semântico relevante do repositório antes de responder ou gerar código.
- Reduzir o tempo gasto por devs explicando contexto do legado manualmente ao agente.
- Tornar a base de conhecimento algo que nasce automaticamente na instalação
  (bootstrap) e se mantém atualizada com o mínimo de esforço manual.
- Ser portátil: mesmo pacote funciona em qualquer repositório, sem reescrever nada
  específico do projeto.

### Não-objetivos (fora de escopo v1)

- Não substitui o processo de post-mortem — é um consumidor futuro dele, não parte dele.
- Não indexa múltiplos repositórios simultaneamente na v1 (fica para fase futura).
- Não usa serviços de embedding pagos/externos — tudo roda local.
- Não é uma ferramenta de busca corporativa geral (Slack, Jira, etc.) — escopo é
  código + documentação do repositório.

## 3. Usuários e casos de uso

- **Devs do time**, usando Claude Code ou GitHub Copilot no dia a dia, perguntando
  coisas como "como esse módulo de billing se comporta?" ou "onde isso já foi tratado
  antes?".
- **Tech lead (Arthur)**, mantendo a base atualizada e usando-a para acelerar
  post-mortems e onboarding de novos membros do time.

## 4. Arquitetura

Duas camadas desacopladas:

1. **MCP Server (motor)** — processo local que executa ingestão, chunking, embeddings,
   armazenamento vetorial e busca híbrida. Exposto como tools que qualquer agente
   compatível com MCP pode chamar.
2. **Skill (`SKILL.md`)** — pacote de instruções no padrão aberto Agent Skills, que
   ensina o agente quando e como usar as tools do MCP. É essa camada que é "instalada"
   em `.claude/skills/` (Claude Code) e `.github/skills/` (GitHub Copilot).

```
rag-legado-skill/
├── mcp_server/
│   ├── server.py            # expõe as tools MCP
│   ├── ingest/
│   │   ├── parse_code.py    # chunking via tree-sitter
│   │   └── parse_docs.py    # chunking de markdown/docs
│   ├── index/
│   │   ├── embed.py
│   │   └── store.py         # wrapper LanceDB
│   └── retrieve/
│       ├── hybrid_search.py # vetorial + BM25
│       └── rerank.py
├── skill/
│   ├── SKILL.md
│   └── references/
│       └── metadata_schema.md
├── install.sh                # bootstrap + registro nos agentes
├── bootstrap_index.py         # indexação inicial do repo
└── README.md
```

## 5. Requisitos funcionais

### 5.1 Instalação e bootstrap

- `install.sh` roda a partir da raiz de um repositório Git.
- Detecta arquivos rastreados via `git ls-files`, respeitando `.gitignore`
  automaticamente.
- Suporta um `.ragignore` adicional para exclusões específicas (dados sensíveis,
  vendored code).
- Executa a indexação inicial completa (bootstrap): parse → chunk → embed → grava no
  índice vetorial local.
- Processa em batches para controlar uso de memória, com barra/relatório de progresso.
- Ao final, salva `.rag_state.json` com o hash do commit indexado — base para updates
  incrementais.
- Registra o MCP server e a skill nos locais corretos de Claude Code e GitHub Copilot.
- Gera relatório final: nº de arquivos, nº de chunks, tempo total, arquivos ignorados
  (binários, muito grandes, etc.).
- É idempotente: rodar de novo detecta índice existente e pergunta se o usuário quer
  reindexar do zero ou seguir incremental.

### 5.2 Ingestão e chunking

- Código: chunking AST-aware via `tree-sitter`, por função/classe/método, preservando
  assinatura, docstring e imports relevantes.
- Documentos: chunking por seção (headers de markdown), com overlap pequeno.
- Cada chunk carrega metadata: caminho do arquivo, linguagem, nome da
  função/classe, autor e data do último commit que tocou o trecho.

### 5.3 Indexação e busca

- Embeddings gerados localmente (modelo especializado em código para trechos de
  código; modelo multilíngue para documentação em português).
- Armazenamento em LanceDB (embarcado, sem servidor externo).
- Busca híbrida: vetorial + BM25 (keyword), combinadas.
- Reranking dos top-k resultados antes de retornar ao agente.

### 5.4 Atualização incremental

- Git hook (`post-commit` / `post-merge`) compara HEAD atual com o hash salvo em
  `.rag_state.json`.
- Reprocessa apenas os arquivos alterados (`git diff --name-only`), não o repositório
  inteiro.

### 5.5 Tools expostas via MCP

| Tool | Função |
|---|---|
| `buscar_contexto(query, filtros?)` | Busca híbrida + rerank, retorna chunks relevantes com metadata |
| `reindexar(escopo?)` | Força reindexação total ou de arquivos específicos |
| `status_indice()` | Retorna estatísticas do índice (nº chunks, último commit indexado, data) |

### 5.6 Skill (`SKILL.md`)

- Frontmatter com `description` específica e "pushy" o suficiente para o agente
  auto-invocar a tool sempre que a pergunta envolver comportamento do sistema, módulos
  do legado, ou contexto de código não explícito no que já está aberto no editor.
- Instruções de quando preferir `buscar_contexto` a assumir/alucinar contexto.

## 6. Requisitos não-funcionais

- **Local-first**: nenhuma dependência de API paga ou envio de código para fora da
  máquina do usuário.
- **Performance**: bootstrap de um repo médio (10k–100k linhas) deve levar minutos, não
  horas, em CPU comum.
- **Portabilidade**: mesmo pacote funciona em qualquer projeto Git, sem edição manual.
- **Idempotência**: reinstalar ou reindexar não deve corromper ou duplicar o índice.

## 7. Stack técnica

| Camada | Escolha |
|---|---|
| Linguagem | Python puro (sem framework tipo LangChain) |
| Parsing de código | `tree-sitter` + `tree-sitter-languages` |
| Parsing de docs | `markdown-it-py` |
| Embeddings | `sentence-transformers` (modelo local, ex: `bge-m3` / `bge-code-v1`) |
| Vector store | `LanceDB` (embarcado) |
| Busca por keyword | `rank-bm25` |
| Reranking | cross-encoder local (ex: `bge-reranker-base`) |
| Protocolo de integração | MCP (`mcp` SDK) |
| Formato de skill | Agent Skills open standard (`SKILL.md`) |

## 8. Métricas de sucesso

- Tempo médio de bootstrap em repositório médio.
- % de perguntas dos devs ao agente que passam a usar `buscar_contexto` (proxy de
  adoção).
- Redução percebida no tempo de onboarding / resolução de incidentes (qualitativo,
  via feedback do time).
- Cobertura do índice: % de arquivos rastreados pelo Git que estão indexados.

## 9. Fases de entrega

1. **Fase 1 — Motor core**: ingestão + chunking de código, embeddings, LanceDB, busca
   manual via script.
2. **Fase 2 — Busca híbrida + rerank**: adicionar BM25 e reranking, validar qualidade
   com queries reais do time.
3. **Fase 3 — MCP server**: expor as tools (`buscar_contexto`, `reindexar`,
   `status_indice`).
4. **Fase 4 — Skill + bootstrap**: `SKILL.md`, `install.sh`, indexação inicial
   automática, atualização incremental via git hook.
5. **Fase 5 — Empacotamento e distribuição**: publicar como repositório instalável em
   qualquer projeto do time.
6. **Fase 6 — Skill de documentação**: tool `gerar_doc_modulo`, template de saída,
   merge inteligente com conteúdo manual, gravação em `docs/features/`.

## 10. Riscos e questões abertas

- Qualidade dos embeddings locais em código legado com padrões atípicos — validar com
  queries reais antes de expandir para todo o time.
- Tamanho do índice e tempo de bootstrap em repositórios muito maiores que o estimado
  (100k+ linhas) — pode exigir indexação assíncrona/particionada.
- Governança de conteúdo sensível: garantir que `.ragignore` seja adotado antes da
  primeira indexação em repositórios com segredos ou dados sensíveis versionados.
- Como conectar futuramente esse índice à saída do processo de post-mortem (fase fora
  do escopo desta v1, mas é a motivação de fundo do projeto).
