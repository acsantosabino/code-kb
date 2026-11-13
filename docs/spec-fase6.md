# Spec — Fase 6: Skill de Documentação

**Ref. PRD:** Seção 9 (Fase 6)
**Depende de:** Fase 3 (tools MCP), Fase 4 (skill + convenções de instalação)
**Bloqueia:** —

## Objetivo

Adicionar uma segunda skill que usa a base RAG já construída para gerar/atualizar
documentação estruturada de funcionalidades do sistema, sob demanda explícita do
usuário, gravando o resultado como arquivos markdown versionados no próprio
repositório.

## Escopo

Incluso:
- Tool `gerar_doc_modulo` no MCP server.
- `skill/rag-legado-doc/SKILL.md` (segunda skill, instalada junto com a Fase 4).
- Template fixo de documento gerado.
- Lógica de merge inteligente (preserva seções manuais em regeneração).
- Gravação em `docs/features/<nome-modulo>.md`.

Fora de escopo (conforme decisão do produto):
- Gatilho automático após post-mortem — **explicitamente fora de escopo por
  decisão do usuário**; geração é sempre sob demanda.
- Publicação da doc em qualquer lugar fora do repositório (Confluence, wiki
  externa, etc.).

## Design técnico

### Tool: `gerar_doc_modulo`
```
gerar_doc_modulo(caminho_ou_nome: str, modo: Literal["criar", "atualizar"] = "criar") -> dict
```
- `caminho_ou_nome`: caminho de arquivo/pasta ou nome lógico do módulo (resolvido
  via busca por `file_path_prefix` na base).
- Fluxo interno:
  1. Chama `buscar_contexto` internamente com filtro no módulo/caminho alvo,
     trazendo os chunks de código e de documentação já existente relacionados.
  2. Monta o documento seguindo o template fixo (ver abaixo), preenchendo cada
     seção a partir dos chunks recuperados.
  3. Se `modo="atualizar"` e o arquivo de destino já existir: extrai o conteúdo
     entre os marcadores `<!-- manual:start -->` / `<!-- manual:end -->` e
     preserva; regenera apenas as seções automáticas.
  4. Grava em `docs/features/<slug-do-modulo>.md`.
- Retorno:
  ```json
  {
    "caminho_gerado": "docs/features/billing.md",
    "modo": "criar",
    "secoes_manuais_preservadas": 0,
    "fontes_usadas": ["src/billing/service.py", "src/billing/README.md"]
  }
  ```

### Template de saída
```markdown
# <Nome do módulo/funcionalidade>

<!-- gerado automaticamente por rag-legado-doc — não editar diretamente abaixo,
     exceto dentro dos blocos manual:start/manual:end -->

## O que faz
(resumo funcional, gerado a partir do contexto recuperado)

## Como funciona
(fluxo principal, componentes envolvidos)

## Pontos de entrada
(arquivos, funções, endpoints relevantes — com link para o caminho no repo)

## Comportamentos conhecidos / edge cases
<!-- manual:start -->
<!-- Espaço para observações humanas, post-mortems relacionados, etc. -->
<!-- manual:end -->

## Última atualização
Gerado em: <data> | Baseado no commit: <hash>
```

### Resolução de "módulo"
- v1: resolução simples por prefixo de caminho (`caminho_ou_nome` bate com
  `file_path` dos chunks) ou por busca semântica se o usuário passar um nome
  livre (ex: "billing" em vez de `src/billing/`).
- Se a busca inicial não encontrar chunks suficientes, retornar erro claro em vez
  de gerar um documento vazio/genérico.

### `skill/rag-legado-doc/SKILL.md` (frontmatter)
```yaml
name: rag-legado-doc
description: Gera ou atualiza documentação de funcionalidades do sistema legado em docs/features/, a partir da base de conhecimento RAG já indexada. Use apenas quando o usuário pedir explicitamente para documentar, gerar doc de, ou explicar em formato de documento um módulo ou funcionalidade — não é acionada automaticamente.
```

## Critérios de aceite

- [ ] `gerar_doc_modulo` em `modo="criar"` para um módulo real do repositório
      produz um documento coerente, sem alucinação perceptível de comportamento
      não presente no código/docs indexados.
- [ ] Rodar `modo="atualizar"` após uma edição manual dentro do bloco
      `manual:start/end` preserva esse conteúdo integralmente.
- [ ] Rodar `modo="atualizar"` reflete mudanças reais de código nas seções
      automáticas (ex: nova função pública aparece em "Pontos de entrada").
- [ ] Skill não é invocada automaticamente em conversas que não pedem
      explicitamente geração de documentação (validar com prompts variados).
- [ ] Módulo sem contexto suficiente na base retorna erro claro, não um
      documento vazio ou genérico demais.

## Tarefas

1. Implementar resolução de módulo (por caminho e por nome livre).
2. Implementar `gerar_doc_modulo` (modo criar) usando o template fixo.
3. Implementar parsing/preservação dos blocos `manual:start/end` (modo atualizar).
4. Escrever `SKILL.md` da skill de documentação, testar precisão de invocação.
5. Testar em pelo menos 3 módulos reais do monólito, revisar qualidade do output
   com o time.
6. Documentar o fluxo no README geral do pacote (Fase 5).
