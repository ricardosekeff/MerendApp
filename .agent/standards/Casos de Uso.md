# Casos de Uso – MerendApp

---

## 1. Atores do Sistema

- Administrador Master
- Gestor de Cantina
- Vendedor
- Responsável Financeiro
- Aluno
- Responsável pelo Aluno
- Gateway de Pagamento (Sistema Externo)
- Totem (Dispositivo Externo)

---

## 2. Lista Consolidada de Casos de Uso

| Código | Descrição |
|---|---|
| UC01 | Cadastrar Escola |
| UC02 | Cadastrar Cantina |
| UC03 | Cadastrar Gestor Financeiro |
| UC04 | Cadastrar Gestor |
| UC05 | Cadastrar Vendedor |
| UC06 | Designar Responsável Financeiro |
| UC07 | Cadastrar Aluno |
| UC08 | Importar Alunos via CSV |
| UC09 | Cadastrar Responsável de Aluno |
| UC10 | Configurar Restrições da Carteira |
| UC11 | Realizar Recarga de Créditos |
| UC12 | Processar Pagamento |
| UC13 | Consultar Extrato |
| UC14 | Cadastrar Categoria |
| UC15 | Cadastrar Produto |
| UC16 | Atualizar Preço de Produto |
| UC17 | Cadastrar Combo |
| UC18 | Atualizar Preço de Combo |
| UC19 | Realizar Venda |
| UC20 | Gerar Token de Venda |
| UC21 | Validar Token |
| UC22 | Marcar Token como Utilizado |
| UC23 | Expirar Tokens |
| UC24 | Realizar Devolução |
| UC25 | Abastecer Caixa |
| UC26 | Consultar Dashboard Financeiro |
| UC27 | Consultar Dashboard Operacional |
| UC28 | Habilitar Totem |
| UC29 | Autenticar Aluno |
| UC30 | Autenticar Usuário do Sistema |

---

## 3. Especificação Textual dos Casos de Uso

### UC01 – Cadastrar Escola

**Ator:** Administrador Master
**Pré-condição:** Administrador autenticado

**Fluxo Principal:**
1. Informar dados da escola.
2. Sistema valida unicidade.
3. Sistema salva registro.

**Pós-condição:** Escola cadastrada.

---

### UC05 – Cadastrar Vendedor

**Ator:** Gestor
**Pré-condição:** Gestor autenticado e vinculado à cantina

**Fluxo Principal:**
1. Informar dados do vendedor.
2. Sistema valida vínculo com cantina.
3. Sistema salva registro.

**Pós-condição:** Vendedor apto a realizar vendas.

---

### UC07 – Cadastrar Aluno

**Ator:** Gestor

**Fluxo Principal:**
1. Informar dados do aluno.
2. Sistema cria carteira associada.
3. Saldo inicial = 0.

---

### UC08 – Importar Alunos via CSV

**Ator:** Gestor

**Fluxo Principal:**
1. Upload do arquivo CSV.
2. Sistema valida estrutura.
3. Sistema processa registros.
4. Sistema cria carteiras automaticamente.

**Fluxo Alternativo:**
- Arquivo inválido → operação cancelada.

---

### UC11 – Realizar Recarga de Créditos

**Ator:** Aluno ou Responsável
**Pré-condição:** Autenticado

**Fluxo Principal:**
1. Informar valor.
2. Sistema chama UC12.
3. Gateway confirma pagamento.
4. Sistema credita carteira.

> `<<include>>` UC12 – Processar Pagamento

---

### UC12 – Processar Pagamento

**Ator:** Gateway de Pagamento

**Fluxo Principal:**
1. Sistema envia requisição.
2. Gateway retorna status.
3. Sistema registra transação.

---

### UC19 – Realizar Venda

**Ator:** Vendedor ou Gestor
**Pré-condição:** Aluno autenticado

**Fluxo Principal:**
1. Selecionar produtos/combos.
2. Sistema calcula total.
3. Sistema valida saldo.
4. Debita carteira.
5. Sistema executa UC20.

> `<<include>>` UC20 – Gerar Token

**Fluxo Alternativo:**
- Saldo insuficiente → venda negada.

---

### UC20 – Gerar Token de Venda

**Ator:** Sistema

**Fluxo Principal:**
1. Gerar identificador único criptograficamente seguro.
2. Definir validade.
3. Gerar QR Code.
4. Salvar token.

---

### UC21 – Validar Token

**Ator:** Vendedor / Totem

**Fluxo Principal:**
1. Ler QR Code.
2. Verificar validade.
3. Verificar status.
4. Se válido → UC22.

---

### UC22 – Marcar Token como Utilizado

**Ator:** Sistema

**Fluxo Principal:**
1. Atualizar status para "utilizado".
2. Registrar data/hora.

---

### UC23 – Expirar Tokens

**Ator:** Gestor

**Fluxo Principal:**
1. Selecionar opção expirar todos.
2. Sistema altera status dos tokens válidos.

---

### UC24 – Realizar Devolução

**Ator:** Gestor ou Responsável Financeiro

**Fluxo Principal:**
1. Selecionar venda.
2. Sistema estorna valor.
3. Atualiza saldo da carteira.

---

### UC29 – Autenticar Aluno

**Ator:** Aluno

**Fluxo Principal:**
1. Escolher método:
   - Senha
   - Biometria
   - Reconhecimento facial
2. Sistema valida identidade.

---

### UC30 – Autenticar Usuário do Sistema

**Ator:** Administrador, Gestor, Vendedor, Responsável Financeiro

**Fluxo Principal:**
1. Inserir credenciais.
2. Sistema valida.
3. Sistema aplica RBAC.

---

## 4. Relações UML

**`<<include>>`**
- UC11 → UC12
- UC19 → UC20
- UC21 → UC22

**`<<extend>>`**
- UC29 pode estender autenticação padrão
- UC23 estende gerenciamento de tokens

---

## 5. Observações Arquiteturais

- **Realizar Venda** é o caso de uso central do sistema.
- **Carteira** é o agregado financeiro principal.
- **Token** é mecanismo antifraude e desacoplamento entre pagamento e retirada.
- **Totem** atua como ator secundário gerando tokens de compra.

---

## 6. Complemento – Casos Administrativos Consolidados

### UC14 – Gerenciar Categorias

**Ator:** Gestor
**Inclui:** Criar, Atualizar, Ativar/Inativar

**Fluxo Principal:**
1. Informar código único.
2. Informar nome e nome curto.
3. Definir estoque de segurança.
4. Opcional: enviar imagem.
5. Definir status.
6. Sistema valida unicidade.
7. Sistema persiste dados.

**Regras:**
- Código deve ser único por cantina.
- Categoria inativa não pode ser associada a novos produtos.
- Alteração de status não remove histórico.

---

### UC15 – Gerenciar Produtos

**Ator:** Gestor

**Fluxo Principal:**
1. Informar código único.
2. Associar categoria ativa.
3. Definir estoque inicial.
4. Informar preço de venda.
5. Registrar preço de custo (com histórico).
6. Definir status.

**Regras:**
- Produto inativo não pode ser vendido.
- Atualização de preço deve manter histórico.
- Estoque não pode ser negativo.

---

### UC16 – Atualizar Preço de Produto

**Ator:** Gestor ou Responsável Financeiro

**Fluxo:**
1. Informar novo preço.
2. Sistema registra data/hora.
3. Sistema armazena histórico.

**Regra crítica:** Alteração não afeta vendas já realizadas.

---

### UC17 – Gerenciar Combos

**Ator:** Gestor

**Fluxo Principal:**
1. Selecionar produtos ativos.
2. Definir modo de preço:
   - Soma automática
   - Preço manual
3. Salvar.

**Regras:**
- Todos os produtos do combo devem estar ativos.
- Estoque dos produtos deve ser abatido individualmente na venda.

---

### UC25 – Abastecer Caixa

**Ator:** Gestor ou Responsável Financeiro

**Fluxo:**
1. Informar valor.
2. Informar justificativa.
3. Sistema registra operação financeira.
4. Atualiza saldo de caixa.

**Regra:** Operação auditável e não pode ser excluída.

---

### UC28 – Habilitar Totem

**Ator:** Administrador Master

**Fluxo:**
1. Registrar identificador único do dispositivo.
2. Associar a uma cantina.
3. Gerar credencial de autenticação.
4. Salvar.

**Regras:**
- Totem não habilitado deve ter requisições recusadas.
- Revogação invalida imediatamente o acesso.

---

## 7. Casos Críticos – Refinamento Técnico

### UC19 – Realizar Venda (Versão Técnica Refinada)

**Ator:** Vendedor / Gestor

**Pré-condições:**
- Aluno autenticado.
- Token de sessão válido.
- Produtos ativos.

**Fluxo Principal:**
1. Selecionar itens.
2. Sistema calcula total.
3. Sistema abre transação ACID.
4. Sistema valida saldo da carteira.
5. Sistema valida restrições (categoria, limite diário, etc).
6. Debita saldo.
7. Atualiza estoque.
8. Executa geração de token.
9. Commit da transação.

**Fluxos Alternativos:**

- **A1 – Saldo insuficiente:** Sistema cancela transação e retorna erro.
- **A2 – Estoque insuficiente:** Sistema cancela transação.
- **A3 – Token não gerado:** Rollback completo.

**Pós-condição:**
- Venda registrada.
- Token criado.
- Estoque atualizado.
- Saldo consistente.

---

### UC11 – Recarga de Créditos (Versão Técnica Refinada)

**Fluxo Principal:**
1. Solicitação de recarga.
2. Registro inicial com status "pendente".
3. Redirecionamento ao gateway.
4. Recebimento de callback assinado.
5. Validação de assinatura.
6. Atualização status para "confirmado".
7. Crédito na carteira.
8. Registro auditável.

**Regra Crítica:** Crédito só ocorre após confirmação assíncrona do gateway.