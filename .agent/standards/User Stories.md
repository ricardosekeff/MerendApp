# USER STORIES – MERENDAPP

---

## ÉPICO 1 – Estrutura Multi-Tenant

### US-01 – Cadastro de Escola

> Como **Administrador Master**, quero cadastrar uma escola, para permitir que ela utilize a plataforma.

**Critérios de Aceitação**

- Dado que sou Administrador Master
- Quando eu cadastrar uma nova escola
- Então a escola deve ser criada com status ativo

---

### US-02 – Cadastro de Cantina

> Como **Administrador Master**, quero cadastrar uma cantina vinculada a uma escola, para permitir operação independente dentro da escola.

**Critérios de Aceitação**

- A cantina deve estar vinculada obrigatoriamente a uma escola
- Uma escola pode ter múltiplas cantinas

---

### US-03 – Isolamento de Dados

> Como **Sistema**, quero isolar dados por cantina, para garantir segurança e separação operacional.

**Critérios de Aceitação**

- Gestor só visualiza dados da sua cantina
- Vendedor só opera na sua cantina

---

## ÉPICO 2 – Gestão de Usuários e Permissões

### US-04 – Cadastro de Gestor Financeiro

> Como **Administrador Master**, quero cadastrar o responsável financeiro da cantina, para garantir controle financeiro formal.

**Critérios de Aceitação**

- Toda cantina deve ter 1 responsável financeiro obrigatório
- Apenas Administrador Master pode cadastrá-lo

---

### US-05 – Cadastro de Vendedor

> Como **Gestor**, quero cadastrar vendedores, para delegar vendas.

**Critérios de Aceitação**

- Gestor não pode cadastrar outro gestor
- Vendedor não pode alterar cadastros estruturais

---

### US-06 – Cadastro de Aluno (Individual)

> Como **Gestor**, quero cadastrar aluno manualmente, para permitir uso da carteira.

---

### US-07 – Cadastro de Aluno via CSV

> Como **Gestor**, quero importar alunos via CSV, para ganhar escala operacional.

**Critérios de Aceitação**

- Sistema deve validar duplicidade
- Sistema deve validar formato do arquivo

---

## ÉPICO 3 – Carteira Digital (Wallet)

### US-08 – Criação Automática de Carteira

> Como **Sistema**, quero criar carteira automaticamente ao cadastrar aluno, para permitir uso imediato.

---

### US-09 – Recarga via PIX

> Como **Responsável ou Aluno**, quero recarregar via PIX, para adicionar crédito na carteira.

**Critérios de Aceitação**

- Saldo atualizado imediatamente após confirmação
- Registro da transação salvo

---

### US-10 – Recarga via Cartão de Débito

> Como **Responsável ou Aluno**, quero recarregar via cartão, para adicionar crédito.

---

### US-11 – Bloqueio de Saldo Negativo

> Como **Sistema**, quero impedir compras sem saldo, para garantir integridade financeira.

---

### US-12 – Definição de Limite de Gasto

> Como **Responsável**, quero definir limite diário/semanal/mensal, para controlar consumo.

---

### US-13 – Restrição de Categorias/Produtos

> Como **Responsável**, quero restringir categorias ou produtos, para controlar alimentação.

---

### US-14 – Restrição de Recarga

> Como **Responsável**, quero impedir que o aluno recarregue sozinho, para manter controle financeiro.

---

## ÉPICO 4 – Gestão de Produtos

### US-15 – Cadastro de Categoria

> Como **Gestor**, quero cadastrar categoria, para organizar produtos.

---

### US-16 – Cadastro de Produto

> Como **Gestor**, quero cadastrar produto, para disponibilizar para venda.

---

### US-17 – Cadastro de Combo

> Como **Gestor**, quero criar combos, para vender kits promocionais.

**Critérios de Aceitação**

- Pode ser soma automática
- Pode ter preço customizado

---

### US-18 – Alteração de Preço

> Como **Gestor ou Responsável Financeiro**, quero alterar preço, para atualizar valores de venda.

**Critérios de Aceitação**

- Vendedor não pode alterar preço
- Histórico deve ser armazenado

---

## ÉPICO 5 – Processo de Venda

### US-19 – Autenticação por Senha

> Como **Aluno**, quero me autenticar por senha, para realizar compra.

---

### US-20 – Venda com Débito em Carteira

> Como **Vendedor ou Sistema**, quero debitar carteira na venda, para registrar transação.

**Critérios de Aceitação**

- Validar saldo
- Validar restrições
- Debitar valor

---

### US-21 – Geração de Token

> Como **Sistema**, quero gerar token único por venda, para controlar retirada do lanche.

---

### US-22 – Geração de QR Code

> Como **Sistema**, quero gerar QR Code associado ao token, para validação na entrega.

---

## ÉPICO 6 – Sistema de Tokens

### US-23 – Validação de Token

> Como **Sistema**, quero validar status do token, para impedir reutilização.

**Critérios de Aceitação**

- Token utilizado deve ser bloqueado
- Token expirado deve ser bloqueado

---

### US-24 – Configuração de Validade

> Como **Gestor**, quero configurar validade global, para controlar tempo de retirada.

---

### US-25 – Expiração em Massa

> Como **Gestor**, quero expirar todos tokens válidos, para encerrar operação do dia.

---

## ÉPICO 7 – Totens

### US-26 – Habilitação de Totem

> Como **Administrador Master**, quero habilitar dispositivo, para permitir operação.

---

### US-27 – Bloqueio de Totem Não Autorizado

> Como **Sistema**, quero bloquear dispositivos não cadastrados, para garantir segurança.

---

## ÉPICO 8 – Dashboards

### US-28 – Dashboard Financeiro

> Como **Gestor**, quero visualizar receitas e despesas, para controlar fluxo de caixa.

---

### US-29 – Dashboard de Vendas

> Como **Gestor**, quero visualizar vendas por produto/categoria, para analisar desempenho.

---

### US-30 – Extrato do Aluno

> Como **Responsável**, quero visualizar extrato detalhado, para acompanhar consumo.

---

## ÉPICO 9 – Devoluções e Caixa

### US-31 – Realizar Devolução

> Como **Gestor ou Responsável Financeiro**, quero realizar devolução, para estornar venda.

---

### US-32 – Abastecimento de Caixa

> Como **Responsável Financeiro**, quero registrar entrada de caixa, para manter controle financeiro.

---

## ORGANIZAÇÃO PARA MVP

### MVP Essencial

- Multi-tenant básico
- Cadastro escola/cantina
- Cadastro aluno
- Wallet
- Recarga PIX
- Venda
- Token
- Dashboard básico
- Cadastro produto

### Fase 2

- Cartão débito
- CSV
- Combos
- Dashboards avançados
- Limites e restrições
- Totens

### Fase 3

- Biometria
- Reconhecimento facial
- IA previsão de demanda