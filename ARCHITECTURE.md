# ARCHITECTURE.md — MerendApp
**Versão:** 1.0  
**Status:** Arquitetura Base  
**Documento de referência:** `SAD.md`

---

## 1. Visão Geral

**MerendApp** é uma plataforma SaaS multi-tenant para gestão e digitalização de cantinas escolares. A arquitetura adota o padrão **Modular Monolith** orientado a domínio, preparada para evolução futura a microservices.

### Fluxo de Alto Nível

```
Cliente (Browser / Totem)
        │
        ▼
 ┌─────────────┐
 │    Nginx    │  ← Reverse Proxy + SSL Termination
 └──────┬──────┘
        │
        ▼
 ┌─────────────┐
 │  Gunicorn   │  ← WSGI Server (4 workers)
 └──────┬──────┘
        │
        ▼
 ┌─────────────────────────────────┐
 │         Flask Application       │
 │  ┌────────────┐ ┌────────────┐  │
 │  │  app/api/  │ │  app/web/  │  │  ← Blueprints separados
 │  └────────────┘ └────────────┘  │
 │         Service Layer           │
 │         Repository Layer        │
 └──────┬──────────────────────────┘
        │
   ┌────┴────┐
   ▼         ▼
PostgreSQL  Redis
            │
            ▼
        Celery Worker
```

---

## 2. Stack Tecnológica

| Componente | Tecnologia | Versão |
|---|---|---|
| Linguagem | Python | 3.11+ |
| Framework | Flask | 3.x |
| WSGI Server | Gunicorn | latest |
| Banco de Dados | PostgreSQL | 15+ |
| Cache / Broker | Redis | 7+ |
| Task Queue | Celery | 5.x |
| Reverse Proxy | Nginx | alpine |
| ORM | SQLAlchemy | 3.x |
| Migrations | Alembic (Flask-Migrate) | latest |
| Serialização | Marshmallow | 3.x |
| Auth | Flask-JWT-Extended | latest |
| Formulários | Flask-WTF | latest |
| Containerização | Docker + Compose | latest |

---

## 3. Estrutura do Projeto

Conforme `SCAFFOLD_STANDARD.md`:

```
MerendApp/
├── app/
│   ├── __init__.py             # Application Factory (create_app)
│   ├── extensions.py           # db, migrate, jwt, celery
│   ├── models/
│   │   ├── __init__.py
│   │   └── base.py             # BaseModel com id, created_at, updated_at
│   ├── api/                    # Blueprint REST (Machine-to-Machine)
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── schemas.py          # Marshmallow
│   │   └── errors.py
│   ├── web/                    # Blueprint Web (Human-to-Machine)
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── forms.py            # Flask-WTF
│   ├── modules/                # Módulos de domínio (DDD)
│   │   ├── auth/
│   │   ├── schools/
│   │   ├── canteens/
│   │   ├── users/
│   │   ├── students/
│   │   ├── wallet/
│   │   ├── payments/
│   │   ├── products/
│   │   ├── sales/
│   │   ├── tokens/
│   │   ├── devices/
│   │   └── dashboards/
│   ├── services/               # Regras de negócio e orquestração
│   ├── repositories/           # Abstração de acesso ao banco
│   ├── middleware/             # Tenant resolution, RBAC
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   └── templates/
│       ├── base.html
│       └── components/
├── tests/
│   ├── conftest.py
│   └── test_routes.py
├── config.py                   # Config, DevelopmentConfig, ProductionConfig
├── run.py                      # Entrypoint (from app import create_app)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

---

## 4. Multi-Tenancy

**Estratégia:** Isolamento lógico por `canteen_id` (Single Database, Discriminator Column).

Todas as entidades operacionais possuem:
```sql
canteen_id UUID NOT NULL REFERENCES canteens(id)
```

**Exceções** (escopo global por aluno):
- `students` — aluno existe independente de cantina
- `wallet` — carteira única por aluno
- `wallet_transactions` — histórico global

**Garantias:**
- Middleware resolve o tenant via JWT (`canteen_id` no payload)
- Nenhuma query ignora o filtro de `canteen_id`
- Logs segregados por tenant

---

## 5. Segurança

### Autenticação — JWT
```json
{
  "user_id": "uuid",
  "role": "GESTOR",
  "canteen_id": "uuid",
  "exp": 1234567890
}
```
- Access Token: expiração curta (15 min)
- Refresh Token: expiração longa (7 dias)

### Autorização — RBAC

| Role | Escopo | Permissões Principais |
|---|---|---|
| `ADMIN_MASTER` | Global | Tudo |
| `GESTOR` | Cantina | Produtos, alunos, vendas, tokens |
| `FINANCEIRO` | Cantina | Devoluções, preços, caixa |
| `VENDEDOR` | Cantina | Realizar vendas apenas |
| `RESPONSAVEL` | Aluno | Recargas, restrições |
| `ALUNO` | Próprio | Compras, extrato |

### Infra

- PostgreSQL e Redis **sem** portas públicas (rede Docker interna)
- SSL obrigatório via Nginx
- Firewall: apenas portas 80 e 443 expostas
- Webhook de pagamento validado por assinatura HMAC

---

## 6. Fluxos Críticos

### 6.1 Venda (tudo em uma única transação ACID)
```
1. Autenticar aluno (matrícula + senha)
2. Selecionar produtos/combos
3. Calcular total
4. BEGIN TRANSACTION
   4a. Validar saldo (SELECT FOR UPDATE)
   4b. Validar restrições (limite, categorias bloqueadas)
   4c. Debitar carteira
   4d. Atualizar estoque
   4e. Gerar token UUID único
   4f. COMMIT
5. Gerar QR Code
```
**Rollback** em qualquer falha nos passos 4a–4e.

### 6.2 Recarga (assíncrono via Celery)
```
1. Criar transação status=PENDING
2. Redirecionar ao gateway (PIX/Débito)
3. Gateway envia webhook assinado
4. Celery valida assinatura HMAC
5. Idempotência: transação já CONFIRMED? Ignorar.
6. Creditar carteira (ACID)
7. Status → CONFIRMED, registro auditável
```

### 6.3 Token — Ciclo de Vida
```
VALID ──(usado)──→ USED
VALID ──(expirado automaticamente via Celery)──→ EXPIRED
VALID ──(expirado em massa pelo Gestor)──→ EXPIRED
```

---

## 7. Infraestrutura Docker

| Serviço | Imagem | Porta Interna | Porta Pública |
|---|---|---|---|
| `nginx` | nginx:alpine | 80 | 80, 443 |
| `api` | build local | 8000 | — |
| `postgres` | postgres:15-alpine | 5432 | — |
| `redis` | redis:7-alpine | 6379 | — |
| `worker` | build local (mesmo da api) | — | — |

---

## 8. Variáveis de Ambiente

Ver `.env.example` na raiz do projeto.

---

## 9. Escalabilidade

| Fase | Estratégia |
|---|---|
| Atual | Escala vertical — 1 VM Linode, Modular Monolith |
| Fase 2 | Separar banco e worker em VMs dedicadas |
| Fase 3 | Load balancer + múltiplas instâncias da API |
| Fase 4 | Extração gradual para Microservices por domínio |

---

## 10. Requisitos Não Funcionais

| Categoria | Requisito |
|---|---|
| Disponibilidade | ≥ 99% |
| Tempo de resposta | ≤ 2 segundos |
| Integridade | 100% transações ACID |
| Segurança | LGPD compliant |
| Escalabilidade | Preparado para 1000+ cantinas |

---

*ARCHITECTURE.md — MerendApp v1.0 | Gerado pelo Solution Architect Agent*
