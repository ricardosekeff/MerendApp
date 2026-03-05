# SOFTWARE ARCHITECTURE DOCUMENT (SAD)
**Sistema:** MerendApp
**Versão:** 1.0
**Data:** 2026
**Status:** Arquitetura Base

---

## 1. Introdução

### 1.1 Propósito

Este documento descreve a arquitetura técnica do sistema MerendApp, uma plataforma SaaS multi-tenant para gestão e digitalização de cantinas escolares.

O objetivo deste documento é:

- Definir decisões arquiteturais
- Formalizar padrões técnicos
- Documentar infraestrutura
- Garantir rastreabilidade e segurança
- Servir como base para evolução futura

### 1.2 Escopo

O MerendApp é um sistema SaaS que permite:

- Gestão de cantinas escolares
- Venda digital via carteira de créditos
- Controle financeiro
- Gestão de estoque
- Controle parental
- Operação via Web e Totens

### 1.3 Definições

| Termo | Definição |
|---|---|
| Tenant | Unidade lógica isolada (Cantina) |
| Wallet | Carteira digital do aluno |
| Token | Identificador único de retirada |
| Admin Master | Administrador global do sistema |

---

## 2. Visão Geral do Sistema

### 2.1 Modelo Arquitetural

O sistema adota:

- **Arquitetura SaaS Multi-Tenant**
- **Modular Monolith** orientado a Domínio (DDD)

Preparado para evolução futura para Microservices.

### 2.2 Visão de Alto Nível

```
Usuário
   ↓
Nginx (Reverse Proxy + SSL)
   ↓
Flask API (Gunicorn)
   ↓
Services (Domain Layer)
   ↓
PostgreSQL
   ↓
Redis
   ↓
Celery Worker
```

---

## 3. Decisões Arquiteturais

### 3.1 Linguagem e Framework

- Python 3.11+
- Flask
- Gunicorn (WSGI Server)

**Motivo:** Simplicidade, baixo custo operacional, alta produtividade e facilidade de manutenção.

### 3.2 Banco de Dados

- PostgreSQL 15+
- Modelo relacional
- Transações ACID

**Motivo:** Integridade financeira, suporte a UUID e alta confiabilidade.

### 3.3 Cache e Assíncrono

- Redis 7+
- Celery

**Motivo:** Processamento de webhooks, expiração automática de tokens e escalabilidade futura.

### 3.4 Infraestrutura

- VM Linode
- Docker
- Docker Compose
- Nginx

**Motivo:** Baixo custo inicial, simplicidade operacional e escalabilidade vertical.

---

## 4. Arquitetura de Software

### 4.1 Estrutura do Código

```
app/
 ├── modules/
 │    ├── auth
 │    ├── schools
 │    ├── canteens
 │    ├── users
 │    ├── students
 │    ├── wallet
 │    ├── payments
 │    ├── products
 │    ├── sales
 │    ├── tokens
 │    ├── devices
 │    └── dashboards
 ├── services
 ├── repositories
 ├── middleware
 └── models
```

### 4.2 Camadas

**API Layer**
- Controllers (Flask Blueprints)
- Validação de request
- Serialização

**Service Layer**
- Regras de negócio
- Orquestração
- Controle transacional

**Repository Layer**
- Abstração de acesso ao banco

**Domain Layer**
- Entidades
- Regras críticas
- Invariantes

---

## 5. Modelo Multi-Tenant

### 5.1 Estratégia

Isolamento lógico por `canteen_id`. Todas as entidades operacionais incluem:

```sql
canteen_id UUID NOT NULL
```

**Exceções** (carteira é global ao aluno):

- `students`
- `wallet`
- `wallet_transactions`

### 5.2 Garantias

- Middleware valida tenant via JWT
- Nenhuma query ignora `canteen_id`
- Logs segregados por tenant

---

## 6. Segurança

### 6.1 Autenticação

- JWT com expiração curta
- Refresh Token

JWT contém:
- `user_id`
- `role`
- `canteen_id`

### 6.2 Autorização

RBAC (Role-Based Access Control):

| Role | Permissões |
|---|---|
| `ADMIN_MASTER` | Global |
| `GESTOR` | Cantina |
| `FINANCEIRO` | Financeiro |
| `VENDEDOR` | Venda |
| `RESPONSAVEL` | Controle aluno |
| `ALUNO` | Compra |

### 6.3 Segurança de Infraestrutura

- PostgreSQL sem porta pública
- Redis interno
- Firewall ativo
- SSL obrigatório
- Validação de webhook por assinatura

### 6.4 Segurança Financeira

- Operações críticas com transação
- `SELECT FOR UPDATE`
- Idempotência em recargas
- Auditoria obrigatória

---

## 7. Fluxos Críticos

### 7.1 Recarga

1. Criação da transação `PENDING`
2. Integração com Gateway
3. Webhook
4. Validação
5. Crédito da carteira (ACID)

**Garantias:** Wallet nunca negativa. Transação idempotente.

### 7.2 Venda

1. Autenticação do aluno
2. Validação de restrições
3. Validação de saldo
4. Débito carteira
5. Baixa estoque
6. Geração token

> Tudo em uma única transação.

### 7.3 Token

**Estados:**

- `VALID`
- `USED`
- `EXPIRED`

Expiração automática via Celery.

---

## 8. Infraestrutura

### 8.1 Docker Compose

Serviços:

- `nginx`
- `api`
- `postgres`
- `redis`
- `worker`

### 8.2 Deploy

- Build da imagem
- Migrations automáticas
- Restart policy `always`
- Backup diário

---

## 9. Escalabilidade

### 9.1 Fase Atual

- Escala vertical
- 1 VM
- Modular Monolith

### 9.2 Evolução

- Separar banco
- Separar worker
- Load balancer
- Microservices

---

## 10. Observabilidade

- Logs estruturados (JSON)
- Log financeiro separado
- Auditoria completa
- Monitoramento via logs

---

## 11. Backup e Recuperação

- Backup diário do PostgreSQL
- Retenção mínima de 7 dias
- Armazenamento externo
- Testes periódicos de restore

---

## 12. Requisitos Não Funcionais

| Categoria | Requisito |
|---|---|
| Disponibilidade | >= 99% |
| Tempo de resposta | <= 2 segundos |
| Integridade | 100% transações ACID |
| Segurança | LGPD compliant |
| Escalabilidade | Preparado para 1000+ cantinas |

---

## 13. Riscos Arquiteturais

| Risco | Mitigação |
|---|---|
| Crescimento rápido | Separação futura de serviços |
| Alta concorrência | Lock transacional |
| Falha em webhook | Retry + idempotência |
| Sobrecarga da VM | Monitoramento |

---

## 14. Conclusão

A arquitetura do MerendApp:

- É segura financeiramente
- É escalável
- É economicamente viável
- É preparada para crescimento
- Atende requisitos multi-tenant
- Garante integridade transacional

---

*SAD – MerendApp | Versão 1.0*