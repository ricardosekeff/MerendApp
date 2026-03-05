# ESPECIFICAÇÃO FUNCIONAL
**Sistema:** MerendApp
**Tipo:** SaaS Multi-Tenant
**Versão:** 1.0

---

## 1. REQUISITOS FUNCIONAIS – CONTEXTO MULTI-TENANT

### RF-01 – Estrutura Multi-Tenant

O sistema deverá permitir:

- **RF-01.1:** Cadastro de múltiplas Escolas.
- **RF-01.2:** Cada Escola poderá possuir múltiplas Cantinas.
- **RF-01.3:** Separação lógica de dados por Escola e Cantina.
- **RF-01.4:** Isolamento de dados entre cantinas.

---

## 2. REQUISITOS FUNCIONAIS – PAPÉIS E PERMISSÕES

### 2.1 Administrador Master (MerendApp) — RF-02

O Administrador Master deverá poder:

- **RF-02.1:** Cadastrar Escolas.
- **RF-02.2:** Cadastrar Cantinas.
- **RF-02.3:** Cadastrar o Responsável Financeiro da Cantina.
- **RF-02.4:** Habilitar/desabilitar Tótens.
- **RF-02.5:** Bloquear acessos de dispositivos inválidos.
- **RF-02.6:** Gerenciar status global da plataforma.

### 2.2 Gestor de Cantina — RF-03

O Gestor deverá:

- **RF-03.1:** Gerir apenas cantinas às quais esteja vinculado.
- **RF-03.2:** Cadastrar Vendedores.
- **RF-03.3:** Não poder cadastrar outros Gestores.
- **RF-03.4:** Cadastrar Alunos (individual).
- **RF-03.5:** Cadastrar Alunos via CSV (lote).
- **RF-03.6:** Cadastrar Categorias.
- **RF-03.7:** Cadastrar Produtos.
- **RF-03.8:** Cadastrar Combos.
- **RF-03.9:** Configurar validade global de Tokens.
- **RF-03.10:** Expirar Tokens em massa.
- **RF-03.11:** Acessar dashboards.
- **RF-03.12:** Atualizar preços (junto com Responsável Financeiro).

### 2.3 Responsável Financeiro — RF-04

O Responsável Financeiro deverá:

- **RF-04.1:** Realizar devoluções.
- **RF-04.2:** Realizar abastecimento de caixa.
- **RF-04.3:** Atualizar preços (junto com Gestor).

### 2.4 Vendedores — RF-05

O Vendedor deverá:

- **RF-05.1:** Realizar vendas.
- **RF-05.2:** Consultar produtos.
- **RF-05.3:** Não cadastrar produtos/categorias/combos.
- **RF-05.4:** Não realizar devoluções.

### 2.5 Alunos — RF-06

O Aluno deverá:

- **RF-06.1:** Possuir carteira digital única.
- **RF-06.2:** Realizar compras usando exclusivamente saldo da carteira.
- **RF-06.3:** Consultar saldo.
- **RF-06.4:** Consultar histórico de compras.
- **RF-06.5:** Comprar em qualquer cantina cadastrada no sistema.

### 2.6 Pais/Responsáveis — RF-07

O Responsável deverá:

- **RF-07.1:** Carregar créditos via PIX.
- **RF-07.2:** Carregar créditos via Cartão de Débito.
- **RF-07.3:** Visualizar extrato de recargas.
- **RF-07.4:** Visualizar histórico de consumo do aluno.
- **RF-07.5:** Configurar restrições da carteira.

---

## 3. REQUISITOS FUNCIONAIS – WALLET (CARTEIRA)

### RF-08 – Regras da Carteira

- **RF-08.1:** A carteira nunca poderá ter saldo negativo.
- **RF-08.2:** O saldo deverá ser atualizado imediatamente após confirmação do gateway.
- **RF-08.3:** Permitir limite diário.
- **RF-08.4:** Permitir limite semanal.
- **RF-08.5:** Permitir limite mensal.
- **RF-08.6:** Permitir restrição de categorias.
- **RF-08.7:** Permitir restrição de produtos.
- **RF-08.8:** Permitir restrição de recarga (somente responsável).

---

## 4. REQUISITOS FUNCIONAIS – PRODUTOS E ESTOQUE

### 4.1 Categorias — RF-09

O sistema deverá permitir cadastro de Categoria com:

- Código único (obrigatório)
- Nome
- Nome curto
- Estoque de segurança
- Imagem (opcional)
- Status (Ativo/Inativo)

### 4.2 Produtos — RF-10

Cadastro de Produto contendo:

- Código único
- Nome
- Nome curto
- Estoque atual
- Histórico de preço de custo
- Preço de venda
- Status (Ativo/Inativo)

### 4.3 Combos — RF-11

- **RF-11.1:** Combos deverão permitir múltiplos produtos.
- **RF-11.2:** Preço poderá ser:
  - Soma automática
  - Valor customizado pelo Gestor
- **RF-11.3:** Alteração de preço somente Gestor + Financeiro.

---

## 5. REQUISITOS FUNCIONAIS – PROCESSO DE VENDA

### RF-12 – Autenticação do Aluno

O sistema deverá permitir:

- Reconhecimento facial (futuro)
- Biometria digital (futuro)
- Senha

### RF-13 – Fluxo de Venda

Ao realizar uma venda:

1. Selecionar produtos
2. Validar restrições
3. Validar saldo
4. Debitar carteira
5. Gerar Token único
6. Gerar QR Code

---

## 6. REQUISITOS FUNCIONAIS – SISTEMA DE TOKENS

### RF-14

- **RF-14.1:** Token único por venda.
- **RF-14.2:** Token associado a QR Code.
- **RF-14.3:** Token não poderá ser reutilizado.
- **RF-14.4:** Token não deverá ser deletado.
- **RF-14.5:** Token poderá ter status:
  - Válido
  - Utilizado
  - Expirado

### RF-15 – Validade

- **RF-15.1:** Validade configurável por Cantina.
- **RF-15.2:** Gestor poderá expirar todos tokens válidos em massa.
- **RF-15.3:** Sistema deve bloquear uso de tokens utilizados ou expirados.

---

## 7. REQUISITOS FUNCIONAIS – TÓTENS

### RF-16

- **RF-16.1:** Totens deverão ser habilitados pelo Administrador Master.
- **RF-16.2:** Totens não habilitados deverão ser bloqueados.
- **RF-16.3:** Totens funcionarão como ponto de venda.

---

## 8. REQUISITOS FUNCIONAIS – DASHBOARDS

### 8.1 Financeiro — RF-17

Dashboard deverá apresentar:

- Receitas
- Despesas
- Fluxo de caixa
- Projeção mensal
- Entradas e saídas

### 8.2 Vendas — RF-18

- Vendas por produto
- Vendas por categoria
- Rotatividade
- Histórico de preços
- Projeção de vendas

---

## 9. REQUISITOS FUNCIONAIS – INTEGRAÇÕES

### RF-19

- **RF-19.1:** Integração com Gateway de Pagamento (PIX + Débito).
- **RF-19.2:** APIs para biometria (futuro).
- **RF-19.3:** Infraestrutura para reconhecimento facial (futuro).
- **RF-19.4:** Controle de dispositivos (tótens).

---

## 10. REGRAS CRÍTICAS DE NEGÓCIO

| Regra | Descrição |
|---|---|
| **RN-01** | Wallet nunca pode ficar negativa. |
| **RN-02** | Token não pode ser reutilizado. |
| **RN-03** | Totem não habilitado deve ser bloqueado. |
| **RN-04** | Gestor não pode cadastrar outro Gestor. |
| **RN-05** | Somente Gestor cadastra produtos/categorias/combos. |
| **RN-06** | Somente Gestor + Financeiro alteram preços. |
| **RN-07** | Somente Gestor + Financeiro realizam devoluções. |

---

## 11. REQUISITOS NÃO FUNCIONAIS (SUGERIDOS)

- **RNF-01:** Arquitetura SaaS escalável.
- **RNF-02:** Disponibilidade mínima 99,5%.
- **RNF-03:** Logs auditáveis de transações financeiras.
- **RNF-04:** LGPD compliance.
- **RNF-05:** Tempo de resposta máximo de 2 segundos para venda.

---

## Resultado

Este documento está estruturado para:

- Desenvolvimento
- Arquitetura
- QA/Testes
- Criação de backlog técnico
- Derivação para User Stories