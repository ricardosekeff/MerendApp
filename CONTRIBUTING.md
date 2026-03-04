# 📋 Guia de Contribuição — MerendApp

## Gitflow & Nomenclatura de Branches

Cada issue deve ser desenvolvida em uma branch dedicada. O nome da branch **deve seguir** o padrão abaixo:

| Tipo de Issue | Label | Branch |
|---|---|---|
| Nova funcionalidade | `enhancement` | `feat/issue-{N}` |
| Correção de bug | `bug` | `bug/issue-{N}` |
| Hotfix em produção | `hotfix` | `hotfix/issue-{N}` |

**Exemplos:**
```
feat/issue-1     → ISSUE-01: Setup Inicial do Projeto
feat/issue-24    → ISSUE-24: Fluxo de Venda
bug/issue-12     → Correção na Carteira Digital
hotfix/issue-6   → Hotfix urgente em Autenticação
```

## Fluxo de Trabalho (Gitflow)

```
main         ← branch de produção (protegida, somente via PR)
  └── develop  ← branch de integração (base para features)
        └── feat/issue-{N}   ← branch da issue
        └── bug/issue-{N}
```

### Passo a Passo

1. **Nunca commite diretamente na `main`** — toda mudança deve passar por PR.
2. Crie a branch a partir de `develop` (ou `main` para hotfixes):
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feat/issue-{N}
   ```
3. Desenvolva e commite usando [Conventional Commits](https://www.conventionalcommits.org/):
   ```bash
   git commit -m "feat(auth): implementa login e logout de usuários"
   ```
4. Abra um **Pull Request** de `feat/issue-{N}` → `develop` (ou `main` para hotfixes).
5. Na descrição do PR, referencie a issue:
   ```
   Closes #N
   ```
6. Após aprovação e merge, a **GitHub Action** fecha a issue automaticamente.

## Commits Convencionais

```
feat:     nova funcionalidade
fix:      correção de bug
docs:     mudança em documentação
refactor: refatoração sem mudança de comportamento
test:     adição/ajuste de testes
chore:    tarefas de manutenção (CI, deps, etc)
```

## Proteção da Branch `main`

A branch `main` está protegida:
- ❌ Push direto bloqueado
- ✅ Merge apenas via Pull Request aprovado
- ✅ CI deve passar antes do merge
