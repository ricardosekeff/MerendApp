# DOCUMENTO DE SEGURANÇA DA INFORMAÇÃO E LGPD
**Sistema:** MerendApp
**Versão:** 1.0
**Data:** 2026
**Classificação:** Confidencial

---

## 1. Introdução

### 1.1 Objetivo

Este documento define as políticas, controles e práticas de segurança da informação adotadas pelo MerendApp, bem como sua adequação à Lei Geral de Proteção de Dados (Lei nº 13.709/2018 – LGPD).

O objetivo é garantir:

- Proteção de dados pessoais
- Segurança financeira
- Integridade das transações
- Conformidade regulatória
- Mitigação de riscos operacionais

---

## 2. Escopo

Este documento cobre:

- Dados armazenados
- Processamento de dados
- Segurança da infraestrutura
- Segurança da aplicação
- Controles de acesso
- Tratamento de incidentes
- Conformidade com LGPD

---

## 3. Classificação de Dados

### 3.1 Tipos de Dados Tratados

| Tipo de Dado | Classificação | Exemplo |
|---|---|---|
| Dados pessoais de alunos | Sensível | Nome, CPF (se aplicável) |
| Dados de responsáveis | Sensível | Nome, e-mail, telefone |
| Dados financeiros | Crítico | Transações, saldo |
| Dados operacionais | Interno | Vendas, estoque |
| Dados técnicos | Restrito | Logs, IP |

### 3.2 Dados NÃO Armazenados

- Dados completos de cartão
- CVV
- Informações bancárias sensíveis

> Pagamentos são processados por Gateway certificado.

---

## 4. Base Legal (LGPD)

O MerendApp fundamenta o tratamento de dados nas seguintes bases legais:

| Finalidade | Base Legal |
|---|---|
| Execução do serviço | Art. 7º, V |
| Cumprimento de obrigação legal | Art. 7º, II |
| Legítimo interesse | Art. 7º, IX |
| Consentimento (quando aplicável) | Art. 7º, I |

---

## 5. Papéis segundo a LGPD

| Papel | Definição |
|---|---|
| Controlador | Escola / Cantina |
| Operador | MerendApp |
| Titular | Aluno / Responsável |

---

## 6. Segurança da Infraestrutura

### 6.1 Ambiente

- Hospedagem em VM Linode
- Sistema operacional atualizado
- Firewall ativo
- Acesso SSH via chave pública
- Sem exposição pública de banco ou Redis

### 6.2 Comunicação

- HTTPS obrigatório
- TLS 1.2 ou superior
- Certificado SSL válido
- Criptografia em trânsito

### 6.3 Banco de Dados

- PostgreSQL protegido
- Sem acesso público
- Backup diário
- Controle de acesso restrito
- Logs de auditoria

---

## 7. Segurança da Aplicação

### 7.1 Autenticação

- JWT com expiração curta
- Refresh token
- Hash de senha com algoritmo seguro (bcrypt)
- Proteção contra brute force

### 7.2 Autorização

RBAC (Role-Based Access Control):

- `ADMIN_MASTER`
- `GESTOR`
- `FINANCEIRO`
- `VENDEDOR`
- `RESPONSAVEL`
- `ALUNO`

Permissões segregadas por tenant.

### 7.3 Proteções Implementadas

- Validação de input
- Proteção contra SQL Injection (ORM)
- Proteção contra XSS
- Rate limiting
- CSRF protection
- Logs de auditoria

---

## 8. Segurança Financeira

### 8.1 Transações

- Operações ACID
- `SELECT FOR UPDATE`
- Idempotência de recargas
- Registro imutável de transações

### 8.2 Tokens de Venda

- UUID único
- Não reutilizável
- Validação de status
- Expiração automática
- Auditoria completa

---

## 9. Logs e Auditoria

### 9.1 Eventos Auditáveis

- Login
- Recarga
- Venda
- Devolução
- Alteração de preço
- Expiração de token

### 9.2 Retenção de Logs

- Retenção mínima: 6 meses
- Logs financeiros: retenção mínima de 5 anos (recomendado)

---

## 10. Gestão de Incidentes

### 10.1 Processo

1. Identificação
2. Contenção
3. Análise
4. Correção
5. Comunicação

### 10.2 Comunicação de Incidentes

Em caso de incidente relevante:

- Notificação ao controlador (Escola/Cantina)
- Notificação à ANPD quando aplicável
- Notificação aos titulares quando necessário

---

## 11. Direitos dos Titulares

O sistema permitirá:

- Acesso aos dados
- Correção de dados
- Exclusão quando permitido
- Portabilidade (exportação)
- Revogação de consentimento (quando aplicável)

> Solicitações deverão ser atendidas em até 15 dias.

---

## 12. Retenção e Exclusão de Dados

### 12.1 Política

- Dados mantidos enquanto houver relação contratual
- Dados financeiros mantidos conforme legislação fiscal
- Dados inativos poderão ser anonimizados

### 12.2 Exclusão

- Soft delete operacional
- Hard delete mediante solicitação válida e análise legal

---

## 13. Backup e Recuperação

- Backup diário automatizado
- Armazenamento externo
- Teste periódico de restauração
- Plano de recuperação documentado

---

## 14. Controle de Acesso Interno

- Acesso mínimo necessário
- Acesso administrativo restrito
- Logs de acesso administrativo
- Senhas fortes obrigatórias

---

## 15. Avaliação de Risco

| Risco | Mitigação |
|---|---|
| Vazamento de dados | Criptografia + controle de acesso |
| Ataque externo | Firewall + SSL |
| Fraude interna | Auditoria + logs |
| Ataque de força bruta | Rate limit |
| Falha financeira | Transação ACID |

---

## 16. Conformidade com LGPD

O MerendApp:

- Trata apenas dados necessários
- Implementa segurança técnica e administrativa
- Permite exercício de direitos do titular
- Possui registro de operações de tratamento
- Não comercializa dados
- Não compartilha dados com terceiros sem base legal

---

## 17. Melhorias Futuras Planejadas

- MFA para gestores
- Criptografia em repouso
- SIEM
- Monitoramento avançado
- WAF dedicado
- Auditoria externa anual

---

## 18. Declaração Final

O MerendApp adota medidas técnicas e administrativas adequadas para proteger dados pessoais, garantir integridade financeira e assegurar conformidade com a LGPD.

> Este documento deve ser revisado anualmente ou sempre que houver alteração relevante na arquitetura.

---

*Segurança e LGPD – MerendApp | Versão 1.0*