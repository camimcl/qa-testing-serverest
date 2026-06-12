# Plano de Testes — Endpoint de Usuários | ServeRest API

> **API Base URL:** `https://compassuol.serverest.dev/`  
> **Endpoint:** `/usuarios`  
> **Versão:** 1.0

---

## Contexto

A ServeRest é uma API REST de prática voltada a estudos de QA. O endpoint `/usuarios` permite operações completas de CRUD:

| Método | Rota              | Descrição                     |
|--------|-------------------|-------------------------------|
| GET    | `/usuarios`       | Lista todos os usuários       |
| GET    | `/usuarios/{id}`  | Retorna um usuário pelo ID    |
| POST   | `/usuarios`       | Cadastra um novo usuário      |
| PUT    | `/usuarios/{id}`  | Atualiza um usuário pelo ID   |
| DELETE | `/usuarios/{id}`  | Remove um usuário pelo ID     |

### Campos do payload

| Campo          | Tipo    | Obrigatório | Descrição                         |
|----------------|---------|-------------|-----------------------------------|
| `nome`         | string  | Sim         | Nome completo do usuário          |
| `email`        | string  | Sim         | E-mail único                      |
| `password`     | string  | Sim         | Senha do usuário                  |
| `administrador`| string  | Sim         | `"true"` ou `"false"`             |

---

## Cenários de Teste

---

### CT-001 — Listar todos os usuários com sucesso

**Método:** `GET /usuarios`

```gherkin
Dado que a API ServeRest está disponível
Quando uma requisição GET é enviada para "/usuarios"
Então o status HTTP retornado deve ser 200
E o corpo da resposta deve conter o campo "quantidade" do tipo inteiro
E o corpo da resposta deve conter o campo "usuarios" do tipo array
E cada item do array deve possuir os campos "_id", "nome", "email", "password" e "administrador"
```

**Resposta esperada (200 OK):**
```json
{
  "quantidade": 2,
  "usuarios": [
    {
      "nome": "Fulano da Silva",
      "email": "fulano@qa.com",
      "password": "teste",
      "administrador": "true",
      "_id": "0uxuPY0cbmQhpEz1"
    }
  ]
}
```

---

### CT-002 — Buscar usuário por ID existente

**Método:** `GET /usuarios/{id}`

```gherkin
Dado que existe um usuário cadastrado com o ID "0uxuPY0cbmQhpEz1"
Quando uma requisição GET é enviada para "/usuarios/0uxuPY0cbmQhpEz1"
Então o status HTTP retornado deve ser 200
E o corpo da resposta deve conter os campos "_id", "nome", "email", "password" e "administrador"
E o valor do campo "_id" deve ser "0uxuPY0cbmQhpEz1"
```

**Resposta esperada (200 OK):**
```json
{
  "nome": "Fulano da Silva",
  "email": "fulano@qa.com",
  "password": "teste",
  "administrador": "true",
  "_id": "0uxuPY0cbmQhpEz1"
}
```

---

### CT-003 — Buscar usuário por ID inexistente

**Método:** `GET /usuarios/{id}`

```gherkin
Dado que não existe nenhum usuário com o ID "idInexistente999"
Quando uma requisição GET é enviada para "/usuarios/idInexistente999"
Então o status HTTP retornado deve ser 400
E o corpo da resposta deve conter o campo "message"
E o valor de "message" deve ser "Usuário não encontrado"
```

**Resposta esperada (400 Bad Request):**
```json
{
  "message": "Usuário não encontrado"
}
```

---

### CT-004 — Cadastrar usuário com sucesso

**Método:** `POST /usuarios`

```gherkin
Dado que todos os campos obrigatórios estão preenchidos corretamente
E o e-mail informado ainda não está cadastrado na base de dados
Quando uma requisição POST é enviada para "/usuarios" com o payload válido
Então o status HTTP retornado deve ser 201
E o corpo da resposta deve conter o campo "message" com o valor "Cadastro realizado com sucesso"
E o corpo da resposta deve conter o campo "_id" com o identificador gerado
```

**Payload enviado:**
```json
{
  "nome": "João Silva",
  "email": "joao.silva@qa.com",
  "password": "senha123",
  "administrador": "true"
}
```

**Resposta esperada (201 Created):**
```json
{
  "message": "Cadastro realizado com sucesso",
  "_id": "abc123xyz"
}
```

---

### CT-005 — Cadastrar usuário com e-mail já existente (duplicado)

**Método:** `POST /usuarios`

```gherkin
Dado que já existe um usuário cadastrado com o e-mail "fulano@qa.com"
Quando uma requisição POST é enviada para "/usuarios" com o mesmo e-mail "fulano@qa.com"
Então o status HTTP retornado deve ser 400
E o corpo da resposta deve conter o campo "message"
E o valor de "message" deve ser "Este email já está sendo usado"
```

**Payload enviado:**
```json
{
  "nome": "Outro Usuário",
  "email": "fulano@qa.com",
  "password": "senha456",
  "administrador": "false"
}
```

**Resposta esperada (400 Bad Request):**
```json
{
  "message": "Este email já está sendo usado"
}
```

---

### CT-006 — Cadastrar usuário sem o campo "nome"

**Método:** `POST /usuarios`

```gherkin
Dado que o payload de criação de usuário está incompleto
E o campo "nome" está ausente do corpo da requisição
Quando uma requisição POST é enviada para "/usuarios" sem o campo "nome"
Então o status HTTP retornado deve ser 400
E o corpo da resposta deve conter o campo "nome"
E o valor de "nome" deve indicar que o campo é obrigatório
```

**Payload enviado:**
```json
{
  "email": "sem.nome@qa.com",
  "password": "senha123",
  "administrador": "false"
}
```

**Resposta esperada (400 Bad Request):**
```json
{
  "nome": "nome é obrigatório"
}
```

---

### CT-007 — Cadastrar usuário sem o campo "email"

**Método:** `POST /usuarios`

```gherkin
Dado que o payload de criação de usuário está incompleto
E o campo "email" está ausente do corpo da requisição
Quando uma requisição POST é enviada para "/usuarios" sem o campo "email"
Então o status HTTP retornado deve ser 400
E o corpo da resposta deve conter o campo "email"
E o valor de "email" deve indicar que o campo é obrigatório
```

**Payload enviado:**
```json
{
  "nome": "Usuário Sem Email",
  "password": "senha123",
  "administrador": "false"
}
```

**Resposta esperada (400 Bad Request):**
```json
{
  "email": "email é obrigatório"
}
```

---

### CT-008 — Cadastrar usuário sem o campo "password"

**Método:** `POST /usuarios`

```gherkin
Dado que o payload de criação de usuário está incompleto
E o campo "password" está ausente do corpo da requisição
Quando uma requisição POST é enviada para "/usuarios" sem o campo "password"
Então o status HTTP retornado deve ser 400
E o corpo da resposta deve conter o campo "password"
E o valor de "password" deve indicar que o campo é obrigatório
```

**Payload enviado:**
```json
{
  "nome": "Usuário Sem Senha",
  "email": "sem.senha@qa.com",
  "administrador": "false"
}
```

**Resposta esperada (400 Bad Request):**
```json
{
  "password": "password é obrigatório"
}
```

---

### CT-009 — Atualizar usuário existente com dados válidos

**Método:** `PUT /usuarios/{id}`

```gherkin
Dado que existe um usuário cadastrado com o ID "0uxuPY0cbmQhpEz1"
E o payload de atualização contém todos os campos obrigatórios preenchidos
E o e-mail informado não pertence a outro usuário
Quando uma requisição PUT é enviada para "/usuarios/0uxuPY0cbmQhpEz1" com o payload válido
Então o status HTTP retornado deve ser 200
E o corpo da resposta deve conter o campo "message" com o valor "Registro alterado com sucesso"
```

**Payload enviado:**
```json
{
  "nome": "Fulano Atualizado",
  "email": "fulano.atualizado@qa.com",
  "password": "novaSenha123",
  "administrador": "false"
}
```

**Resposta esperada (200 OK):**
```json
{
  "message": "Registro alterado com sucesso"
}
```

---

### CT-010 — Atualizar usuário com ID inexistente (deve criar novo registro)

**Método:** `PUT /usuarios/{id}`

```gherkin
Dado que não existe nenhum usuário com o ID "idQueNaoExiste000"
E o payload de atualização contém todos os campos obrigatórios preenchidos
E o e-mail informado não está em uso por outro usuário
Quando uma requisição PUT é enviada para "/usuarios/idQueNaoExiste000"
Então o status HTTP retornado deve ser 201
E o corpo da resposta deve conter o campo "message" com o valor "Cadastro realizado com sucesso"
E o corpo da resposta deve conter o campo "_id" com o identificador gerado
```

**Payload enviado:**
```json
{
  "nome": "Novo Usuário Via PUT",
  "email": "novo.put@qa.com",
  "password": "senha789",
  "administrador": "true"
}
```

**Resposta esperada (201 Created):**
```json
{
  "message": "Cadastro realizado com sucesso",
  "_id": "novoIdGerado123"
}
```

---

### CT-011 — Deletar usuário existente com sucesso

**Método:** `DELETE /usuarios/{id}`

```gherkin
Dado que existe um usuário cadastrado com o ID "0uxuPY0cbmQhpEz1"
E esse usuário não possui carrinho ativo associado
Quando uma requisição DELETE é enviada para "/usuarios/0uxuPY0cbmQhpEz1"
Então o status HTTP retornado deve ser 200
E o corpo da resposta deve conter o campo "message" com o valor "Registro excluído com sucesso"
```

**Resposta esperada (200 OK):**
```json
{
  "message": "Registro excluído com sucesso"
}
```

---

## Resumo dos Cenários

| ID     | Operação | Método | Cenário                                | Status Esperado |
|--------|----------|--------|----------------------------------------|-----------------|
| CT-001 | Read     | GET    | Listar todos os usuários               | 200             |
| CT-002 | Read     | GET    | Buscar usuário por ID existente        | 200             |
| CT-003 | Read     | GET    | Buscar usuário por ID inexistente      | 400             |
| CT-004 | Create   | POST   | Cadastrar usuário com sucesso          | 201             |
| CT-005 | Create   | POST   | E-mail duplicado                       | 400             |
| CT-006 | Create   | POST   | Campo "nome" ausente                   | 400             |
| CT-007 | Create   | POST   | Campo "email" ausente                  | 400             |
| CT-008 | Create   | POST   | Campo "password" ausente               | 400             |
| CT-009 | Update   | PUT    | Atualizar usuário com dados válidos    | 200             |
| CT-010 | Update   | PUT    | Atualizar com ID inexistente (upsert)  | 201             |
| CT-011 | Delete   | DELETE | Deletar usuário existente              | 200             |

---

## Observações Técnicas

- A ServeRest reseta seus dados periodicamente — IDs usados nos cenários devem ser obtidos dinamicamente via `GET /usuarios` antes de executar testes que dependem de ID.
- O comportamento do `PUT` com ID inexistente é um **upsert**: cria o recurso caso não exista.
- O campo `administrador` aceita apenas os valores `"true"` ou `"false"` como string.
- Não é necessário autenticação para o endpoint `/usuarios`, mas outros endpoints como `/produtos` e `/carrinhos` exigem token Bearer obtido via `POST /login`.
