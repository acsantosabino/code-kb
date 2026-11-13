# Spec — Fase 5: Empacotamento e Distribuição

**Ref. PRD:** Seção 9 (Fase 5), requisito de portabilidade (Seção 6)
**Depende de:** Fase 4
**Bloqueia:** Fase 6 (pode rodar em paralelo, mas Fase 6 assume que a distribuição já
existe para facilitar testes em múltiplos repositórios)

## Objetivo

Transformar o pacote validado nas fases anteriores em algo que qualquer projeto do
time (ou de outros times) possa adotar com um único comando, sem depender de cópia
manual de arquivos.

## Escopo

Incluso:
- Repositório Git próprio para o pacote (`rag-legado-skill`), versionado
  independentemente dos projetos que o consomem.
- Comando único de instalação a partir de um projeto-alvo (ex: via `curl` + script,
  ou `pip install` + comando CLI).
- Versionamento semântico do pacote.
- README com guia de instalação, requisitos, troubleshooting.
- Checklist de compatibilidade (linguagens suportadas pelo tree-sitter, versões
  mínimas de Claude Code / GitHub Copilot testadas).

Fora de escopo:
- CI/CD completo (pode ser um item futuro, não crítico para v1 de distribuição).
- Publicação em índice público (PyPI, etc.) — v1 é uso interno do time.

## Design técnico

### Formato de distribuição
Duas opções a avaliar e decidir na implementação (não bloqueante para o resto do
projeto, mas precisa ser decidido nesta fase):

- **Opção A — pacote Python instalável**: `pip install git+<repo-url>` expõe um
  comando `rag-legado init` que executa o equivalente ao `install.sh`.
- **Opção B — script standalone**: `curl -sSL <url>/install.sh | bash`, sem
  dependência de um pacote Python publicado.

Recomendação: começar pela Opção B (mais simples, sem overhead de empacotamento
Python), migrar para A se o pacote crescer em complexidade de dependências.

### Versionamento
- SemVer (`vMAJOR.MINOR.PATCH`).
- Cada instalação registra a versão do pacote em `.rag_state.json` para permitir
  detectar desatualização e sugerir update.

### Atualização de instalações existentes
- Comando `rag-legado update` (ou `install.sh --update`): atualiza o MCP server e a
  skill sem tocar no índice já construído, a menos que a versão nova exija
  migração de schema (ver abaixo).
- Se o schema de metadata dos chunks mudar entre versões, incluir script de
  migração (`migrations/vX_to_vY.py`).

## Critérios de aceite

- [ ] Um dev consegue instalar o pacote em um projeto novo com um único comando
      documentado, sem precisar clonar/copiar arquivos manualmente.
- [ ] README cobre: requisitos (Python, versões), passo a passo de instalação,
      como verificar que funcionou, troubleshooting dos erros mais comuns.
- [ ] Testado em pelo menos 2 repositórios diferentes do time, confirmando que o
      pacote não tem nada hardcoded específico do primeiro projeto testado.
- [ ] Comando de update funciona sem exigir reindexação completa (quando não há
      mudança de schema).

## Tarefas

1. Decidir e implementar formato de distribuição (Opção A ou B).
2. Criar repositório próprio do pacote, com tag de versão inicial.
3. Escrever README completo.
4. Testar instalação do zero em um segundo repositório do time (validação de
   portabilidade real).
5. Implementar comando/fluxo de update.
6. Checklist de compatibilidade documentado.
