# PRODUCT REQUIREMENTS DOCUMENT (PRD)
## MerendApp – Sistema Multi-Tenant de Gestão e Vendas para Cantinas Escolares

---

## 1. Visão do Produto

MerendApp é uma plataforma SaaS multi-tenant para gestão e digitalização de cantinas escolares, permitindo vendas 100% digitais via carteira de créditos, eliminando dinheiro físico e oferecendo controle financeiro completo para gestores e responsáveis.

### Objetivo Estratégico

Criar uma solução integrada, escalável e financeiramente sustentável para venda de lanches em escolas, eliminando dinheiro físico e oferecendo controle total de consumo e fluxo financeiro.

---

## 2. Stakeholders

| Papel | Tipo |
|---|---|
| Gestores de Cantina | Principal Decisor (Pagante) |
| Gestores de Cantina | Usuário Operacional |
| Responsáveis Financeiros | Usuário Operacional |
| Vendedores | Usuário Operacional |
| Alunos | Usuário Operacional |
| Pais/Responsáveis | Usuário Operacional |
| Administrador Master do Sistema | Usuário Operacional |

---

## 3. Problemas Identificados

### Para Gestores
- Uso de dinheiro físico
- Falta de controle financeiro estruturado
- Falta de previsibilidade de vendas
- Dificuldade de controle de estoque
- Gestão manual de caixa

### Para Pais/Responsáveis
- Falta de controle sobre gastos do aluno
- Falta de restrições de consumo
- Necessidade de enviar dinheiro físico

### Para Escolas
- Circulação de dinheiro físico
- Risco de perdas e conflitos

---

## 4. Modelo de Monetização

### Modelo Híbrido

**Mensalidade por Cantina**
- Valor fixo recorrente (ex: R$99–R$199)

**Taxa de Serviço sobre Recarga**
- Percentual sobre transações de recarga (ex: 1,5%–2,5%)
- Aplicado no momento da compra via PIX ou Cartão de Débito

---

## 5. Arquitetura do Produto

**Modelo: Multi-Tenant**

- Uma Escola → múltiplas Cantinas
- Uma Cantina → múltiplos Gestores e Vendedores
- Um Aluno → pode comprar em qualquer cantina de qualquer escola
- Wallet central por aluno

---

## 6. Papéis e Permissões

### 6.1 Administrador Master (MerendApp)
- Cadastrar escolas
- Cadastrar responsável financeiro da cantina
- Habilitar/desabilitar tótens
- Gestão global da plataforma

### 6.2 Gestor de Cantina
- Gerir apenas suas cantinas
- Cadastrar vendedores
- Cadastrar alunos (individual ou CSV)
- Cadastrar categorias
- Cadastrar produtos
- Cadastrar combos
- Atualizar preços (junto com responsável financeiro)
- Configurar validade global de tokens
- Expirar tokens em massa
- Acessar dashboards

### 6.3 Responsável Financeiro
- Realizar devoluções
- Abastecimento de caixa
- Atualização de preços (junto com gestor)

### 6.4 Vendedores
- Realizar vendas
- Consultar produtos

### 6.5 Alunos
- Realizar compras
- Consultar saldo
- Visualizar histórico

### 6.6 Pais/Responsáveis
- Carregar créditos
- Definir restrições
- Visualizar extrato

---

## 7. Wallet (Carteira Digital)

### Regras
- Nunca pode ter saldo negativo
- Créditos via PIX ou Cartão de Débito
- Atualização imediata após confirmação

### Configurações possíveis
- Limite diário/semanal/mensal
- Restrição de categorias
- Restrição de produtos
- Restrição de recarga (somente responsável pode carregar)

---

## 8. Processo de Venda

### Autenticação do Aluno
- Reconhecimento facial
- Biometria digital
- Senha

### Canais
- Web App
- Mobile App (futuro)
- Totens (futuro)

### Fluxo
1. Aluno seleciona produtos
2. Sistema valida restrições
3. Sistema valida saldo
4. Gera Token único de venda
5. Gera QR Code
6. Debita carteira

---

## 9. Sistema de Tokens

### Regras
- Token único por venda
- QR Code associado
- Não reutilizável
- Não deletado, apenas marcado como:
  - Utilizado
  - Expirado

### Configurações
- Validade global configurável por cantina
- Gestor pode expirar todos tokens válidos em massa

---

## 10. Gestão de Produtos

### Categoria
- Código único
- Nome
- Nome curto
- Estoque de segurança
- Imagem (opcional)
- Status (Ativo/Inativo)

### Produto
- Código único
- Nome
- Nome curto
- Estoque atual
- Histórico de preço de custo
- Preço de venda
- Status

### Combo
- Conjunto de produtos
- Preço automático (soma)
- OU preço customizado

---

## 11. Dashboards

### Financeiro
- Receitas
- Despesas
- Fluxo de caixa
- Projeção mensal

### Vendas
- Por produto
- Por categoria
- Rotatividade
- Histórico de preços

---

## 12. Integrações

- Gateway de pagamento (PIX + Débito)
- APIs futuras para biometria
- Infraestrutura para reconhecimento facial
- Controle de dispositivos (tótens)

---

## 13. Regras Críticas de Negócio

- Wallet nunca pode ficar negativa
- Token não pode ser reutilizado
- Totem não habilitado deve ser bloqueado
- Gestor não pode cadastrar outro gestor
- Apenas gestor pode cadastrar produtos/categorias/combos
- Apenas gestor + financeiro podem alterar preços
- Apenas gestor + financeiro podem realizar devoluções

---

## 14. Escalabilidade

- Arquitetura SaaS multi-tenant
- Separação lógica por escola e cantina
- Controle granular de permissões
- Preparado para milhares de cantinas

---

## 15. Roadmap Futuro

- Aplicativo mobile
- Programa de fidelidade
- Assinatura mensal de lanche
- Crédito patrocinado por escola
- Integração com catraca escolar
- IA para previsão de demanda

---

## Definição de Sucesso (KPIs)

- Redução de uso de dinheiro físico
- Volume de recargas mensais
- Ticket médio por aluno
- Retenção de cantinas
- Crescimento MRR
- Churn rate

---

## Conclusão

O **MerendApp** se posiciona como uma infraestrutura financeira e operacional para cantinas escolares, com foco em escalabilidade, controle e digitalização total do processo de vendas.

**Resolve:**
- Circulação de dinheiro físico
- Falta de controle parental
- Falta de gestão financeira estruturada

Com modelo híbrido sustentável e arquitetura preparada para crescimento nacional.