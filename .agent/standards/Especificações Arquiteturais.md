# Arquitetura do Sistema – MerendApp
**Versão 1.0**
**Arquitetura SaaS Multi-Tenant**
**Stack:** Python (Flask) + PostgreSQL + Docker + Linode

---

## 1. Visão Geral da Arquitetura

O MerendApp será implementado como um SaaS multi-tenant, hospedado em uma VM Linode, utilizando Docker Compose para orquestração dos serviços.

A arquitetura segue o modelo:

- **Modular Monolith** orientado a Domínio (DDD)
- Preparado para futura evolução para Microservices.

---

## 2. Infraestrutura (Linode)

### 2.1 Ambiente

- VM Linux (Ubuntu 22.04 LTS recomendado)
- Docker
- Docker Compose
- Nginx (Reverse Proxy)
- SSL via Let's Encrypt
- Firewall configurado (UFW)

### 2.2 Serviços Executando via Docker Compose

```yaml
services:
  nginx:
  api:
  postgres:
  redis:
  worker:
```

#### 2.2.1 Nginx

- Reverse proxy
- TLS/SSL
- Rate limiting básico
- Encaminhamento para API Flask

#### 2.2.2 API (Flask + Gunicorn)

- Backend principal
- REST API
- JWT Authentication
- Multi-tenant control

#### 2.2.3 PostgreSQL

- Banco relacional principal
- Armazena dados transacionais
- Transações ACID para operações financeiras

#### 2.2.4 Redis

- Cache
- Rate limiting
- Controle rápido de tokens
- Broker para Celery

#### 2.2.5 Worker (Celery)

- Processamento assíncrono
- Webhooks de pagamento
- Expiração automática de tokens
- Processamentos futuros (relatórios, notificações)

---

## 3. Arquitetura da Aplicação (Flask)

### 3.1 Modelo Arquitetural

Arquitetura baseada em camadas:

```
Client → Nginx → Flask API → Services → Repositories → PostgreSQL
                                  ↓
                               Redis
                                  ↓
                               Celery Worker
```

### 3.2 Organização Interna (Modular Monolith)

```
merendapp/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   │
│   ├── modules/
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
│   │
│   ├── models/
│   ├── services/
│   ├── repositories/
│   ├── middleware/
│   └── utils/
│
├── migrations/
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

## 4. Stack Tecnológica

### Backend

- Python 3.11+
- Flask
- Flask-JWT-Extended
- SQLAlchemy
- Flask-Migrate (Alembic)
- Marshmallow (serialização)
- Celery
- Gunicorn

### Banco de Dados

- PostgreSQL 15+
- UUID como chave primária
- Transações ACID

### Cache e Mensageria

- Redis 7+

---

## 5. Modelo Multi-Tenant

### 5.1 Estratégia

Modelo de isolamento lógico: banco único + coluna `canteen_id` nas entidades operacionais.

### 5.2 Regras de Isolamento

Todas as tabelas operacionais conterão:

```sql
canteen_id UUID NOT NULL
```

**Exceções** (carteira é global ao aluno):

- `students`
- `wallet`
- `wallet_transactions`

### 5.3 Validação de Tenant

O JWT conterá:

- `user_id`
- `role`
- `canteen_id`

O Middleware validará acesso por tenant. Nenhuma consulta deverá ignorar o `canteen_id`.

---

## 6. Segurança

### 6.1 Autenticação

- JWT com expiração curta
- Refresh token
- Controle por roles:
  - `ADMIN_MASTER`
  - `GESTOR`
  - `FINANCEIRO`
  - `VENDEDOR`
  - `RESPONSAVEL`
  - `ALUNO`

### 6.2 Segurança de Infraestrutura

- PostgreSQL sem porta pública
- Redis sem porta pública
- Firewall ativo
- SSL obrigatório
- Validação de assinatura de Webhooks
- Logs auditáveis

### 6.3 Segurança Financeira

- Operações críticas dentro de transações
- Idempotência em recargas
- Controle de concorrência
- Registro de auditoria em:
  - Recargas
  - Vendas
  - Devoluções
  - Alterações de preço

---

## 7. Fluxos Técnicos Principais

### 7.1 Fluxo de Recarga (PIX / Débito)

1. Cliente cria intenção de recarga
2. Sistema cria transação `PENDING`
3. Gateway gera pagamento
4. Gateway envia webhook
5. Sistema valida assinatura
6. Sistema atualiza status para `CONFIRMED`
7. Sistema credita carteira (transação atômica)

**Garantias:**
- Wallet nunca negativa
- Idempotência por `transaction_id`
- Log financeiro persistido

### 7.2 Fluxo de Venda

1. Autenticação do aluno
2. Validação de restrições
3. Validação de saldo
4. Débito da carteira
5. Baixa de estoque
6. Criação da venda
7. Geração de token
8. Geração de QR Code

> Tudo dentro de uma única transação ACID.

### 7.3 Fluxo de Token

**Geração**
- UUID v4
- Status inicial: `VALID`
- Data de expiração baseada na configuração da cantina

**Validação**
1. Verifica existência
2. Verifica status
3. Verifica expiração
4. Marca como `USED`

**Expiração Automática**
- Job Celery executado periodicamente
- Atualiza tokens expirados para `EXPIRED`

### 7.4 Fluxo de Totens

1. Administrador Master registra dispositivo
2. Sistema gera `device_id` e token de autenticação
3. Totem se autentica via API
4. Sistema valida se dispositivo está ativo

> Dispositivos não registrados são bloqueados.

---

## 8. Controle de Concorrência

Operações críticas utilizarão:

- `SELECT FOR UPDATE`
- Transações explícitas
- Lock otimista quando aplicável

Especialmente em:

- Débito de carteira
- Baixa de estoque
- Devoluções

---

## 9. Observabilidade

- Logs estruturados (JSON)
- Logs separados por: Financeiro, Segurança e Sistema
- Monitoramento básico via logs da VM
- Preparado para futura integração com ferramentas APM

---

## 10. Escalabilidade

### Estado Atual (Fase Inicial)

- 1 VM Linode
- Docker Compose
- Escala vertical

### Evolução Natural

Quando houver crescimento:

- Separar banco em VM dedicada
- Separar worker
- Adicionar Load Balancer
- Migrar para Kubernetes
- Separar domínios em microservices:
  - `wallet-service`
  - `payment-service`
  - `sales-service`
  - `token-service`

---

## 11. Estratégia de Backup

- Backup diário automático do PostgreSQL
- Retenção mínima de 7 dias
- Dump externo armazenado fora da VM
- Teste periódico de restauração

---

## 12. Garantias Arquiteturais

O sistema garante:

- Isolamento multi-tenant
- Integridade financeira
- Wallet nunca negativa
- Token não reutilizável
- Alta rastreabilidade
- Preparação para crescimento nacional

---

## 13. Resumo Arquitetural

| Camada | Tecnologia |
|---|---|
| Reverse Proxy | Nginx |
| Backend | Flask + Gunicorn |
| Banco | PostgreSQL |
| Cache | Redis |
| Worker | Celery |
| Infra | Linode |
| Orquestração | Docker Compose |