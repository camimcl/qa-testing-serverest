# Plano de Testes — Suíte de API | ServeRest

> **API Base URL:** `https://compassuol.serverest.dev/`  
> **Versão da API:** 3.2.0  
> **Versão do plano:** 2.0  
> **Data:** 2025-06-13  
> **Autor:** QA Team — Trilha Compass

---

## 1. Objetivo da Suíte

Validar de forma automatizada o comportamento dos endpoints **Usuários**, **Login** e **Produtos** da API ServeRest, garantindo que:

- O CRUD de usuários funcione de acordo com o contrato Swagger (já implementado — CT-001 a CT-011).
- O fluxo de autenticação via `/login` retorne tokens válidos para credenciais corretas e rejeite credenciais inválidas com mensagens apropriadas.
- O CRUD de produtos respeite a política de autorização: operações de escrita (POST, PUT, DELETE) exijam token Bearer de um usuário **administrador**, enquanto leitura (GET) permaneça pública.
- Respostas de erro sigam os padrões documentados no Swagger (status code + campo `message`).

---

## 2. Estratégia de Testes

### 2.1 Tipo de Teste

| Tipo                       | Descrição                                                                                     |
|----------------------------|-----------------------------------------------------------------------------------------------|
| **Funcional de API**       | Testes de contrato e comportamento dos endpoints REST (happy path + cenários negativos).       |
| **Validação de Contrato**  | Verifica campos obrigatórios, tipos de dados e estrutura da resposta conforme Swagger.         |
| **Teste de Autenticação**  | Garante que rotas protegidas rejeitam acesso sem token, com token inválido ou de não-admin.    |

### 2.2 Camada de Teste

```
┌─────────────────────────────────────────────┐
│              Testes de API (E2E)             │
│        HTTP Client → ServeRest API          │
│  Camada: Integração de serviço (black-box)  │
└─────────────────────────────────────────────┘
```

- **Camada:** Testes de integração de API (black-box). Não há acesso ao banco de dados nem ao código-fonte do servidor.
- **Ambiente:** API pública `https://compassuol.serverest.dev/` — sujeita a reset periódico (~60s), mitigado por retries automáticos.

### 2.3 Ferramentas

| Ferramenta        | Versão   | Propósito                                                   |
|-------------------|----------|-------------------------------------------------------------|
| **Python**        | 3.x      | Linguagem dos testes                                        |
| **pytest**        | 8.3.5    | Framework de testes + organização em classes e marks         |
| **requests**      | 2.32.3   | Cliente HTTP para chamadas à API                            |
| **pytest-html**   | 4.1.1    | Geração de relatórios HTML                                  |
| **pytest-retry**  | 1.7.0    | Retry automático contra instabilidade da API pública        |

### 2.4 Arquitetura do Projeto

```
qa-serverest/
├── conftest.py          # Fixtures globais (api, isolated_user, temp_user, admin_token)
├── pytest.ini           # Marks e configuração de retries
├── requirements.txt     # Dependências
├── utils/
│   ├── __init__.py      # BASE_URL, payload factories, constantes
│   ├── api_client.py    # ServeRestClient (GET/POST/PUT/DELETE com logging)
│   ├── assertions.py    # Helpers de asserção com logging automático
│   └── logger.py        # Print formatado de request/response
├── tests/
│   ├── test_usuarios.py # ✅ Implementado (CT-001 a CT-011)
│   ├── test_login.py    # 🔜 A implementar (CT-012 a CT-016)
│   └── test_produtos.py # 🔜 A implementar (CT-017 a CT-028)
└── docs/
    ├── plano_de_testes.md            # Este documento (suíte completa)
    └── plano_de_testes_usuarios.md   # Documento original (apenas usuários)
```

---

## 3. Escopo

### 3.1 Dentro do Escopo ✅

| Endpoint            | Métodos              | Cobertura                                                   |
|---------------------|----------------------|-------------------------------------------------------------|
| `/usuarios`         | GET, POST, PUT, DELETE | CRUD completo, validação de campos, e-mail duplicado, upsert |
| `/login`            | POST                 | Credenciais válidas, senha errada, e-mail inexistente, campos vazios |
| `/produtos`         | GET, POST, PUT, DELETE | CRUD completo, autenticação (com/sem token), autorização (admin vs. não-admin) |

### 3.2 Fora do Escopo ❌

| Item                              | Motivo                                                         |
|-----------------------------------|----------------------------------------------------------------|
| `/carrinhos`                      | Será coberto em uma fase futura do projeto                     |
| Testes de performance / carga     | Fora do objetivo da suíte funcional                            |
| Testes de UI (front.serverest.dev)| Projeto focado exclusivamente em testes de API                 |
| Testes de segurança avançados     | Injeção SQL, XSS, etc. — fora do escopo atual                 |
| Expiração de token (TTL de 600s)  | Exigiria waits longos; validado indiretamente por token inválido |

---

## 4. Cenários de Teste

### Legenda de status

| Símbolo | Significado      |
|---------|------------------|
| ✅      | Implementado     |
| 🔜      | A implementar    |

---

### 4.1 Endpoint: `/usuarios` — CRUD de Usuários ✅

> **Arquivo:** `tests/test_usuarios.py`  
> **Auth requerida:** Nenhuma  
> **Referência:** [plano_de_testes_usuarios.md](./plano_de_testes_usuarios.md)

| ID     | Status | Operação | Método | Cenário                                | Status HTTP |
|--------|--------|----------|--------|----------------------------------------|-------------|
| CT-001 | ✅     | Read     | GET    | Listar todos os usuários               | 200         |
| CT-002 | ✅     | Read     | GET    | Buscar usuário por ID existente        | 200         |
| CT-003 | ✅     | Read     | GET    | Buscar usuário por ID inexistente      | 400         |
| CT-004 | ✅     | Create   | POST   | Cadastrar usuário com sucesso          | 201         |
| CT-005 | ✅     | Create   | POST   | E-mail duplicado                       | 400         |
| CT-006 | ✅     | Create   | POST   | Campo "nome" ausente                   | 400         |
| CT-007 | ✅     | Create   | POST   | Campo "email" ausente                  | 400         |
| CT-008 | ✅     | Create   | POST   | Campo "password" ausente               | 400         |
| CT-009 | ✅     | Update   | PUT    | Atualizar usuário com dados válidos    | 200         |
| CT-010 | ✅     | Update   | PUT    | Atualizar com ID inexistente (upsert)  | 201         |
| CT-011 | ✅     | Delete   | DELETE | Deletar usuário existente              | 200         |

---

### 4.2 Endpoint: `/login` — Autenticação 🔜

> **Arquivo:** `tests/test_login.py`  
> **Auth requerida:** Nenhuma (o endpoint *gera* o token)  
> **Dependência de setup:** Requer um usuário cadastrado via `/usuarios` antes dos testes.

| ID     | Status | Cenário                                            | Status HTTP | Validação Esperada                                                                |
|--------|--------|----------------------------------------------------|-------------|-----------------------------------------------------------------------------------|
| CT-012 | 🔜     | Login com credenciais corretas (admin)              | 200         | `message` = "Login realizado com sucesso", campo `authorization` presente (Bearer) |
| CT-013 | 🔜     | Login com senha errada                              | 401         | `message` = "Email e/ou senha inválidos"                                          |
| CT-014 | 🔜     | Login com e-mail inexistente                        | 401         | `message` = "Email e/ou senha inválidos"                                          |
| CT-015 | 🔜     | Login com campo "email" vazio/ausente               | 400         | Corpo da resposta indica que `email` é obrigatório                                |
| CT-016 | 🔜     | Login com campo "password" vazio/ausente            | 400         | Corpo da resposta indica que `password` é obrigatório                             |

#### Detalhamento dos cenários de Login

---

#### CT-012 — Login com credenciais corretas (admin)

**Método:** `POST /login`

```gherkin
Dado que existe um usuário administrador cadastrado na base
Quando uma requisição POST é enviada para "/login" com e-mail e senha válidos
Então o status HTTP retornado deve ser 200
E o corpo da resposta deve conter o campo "message" com valor "Login realizado com sucesso"
E o corpo da resposta deve conter o campo "authorization" começando com "Bearer "
```

**Payload enviado:**
```json
{
  "email": "<email_do_usuario_cadastrado>",
  "password": "<senha_do_usuario_cadastrado>"
}
```

**Resposta esperada (200 OK):**
```json
{
  "message": "Login realizado com sucesso",
  "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

#### CT-013 — Login com senha errada

**Método:** `POST /login`

```gherkin
Dado que existe um usuário cadastrado com o e-mail "usuario@qatest.com"
Quando uma requisição POST é enviada para "/login" com o e-mail correto e senha "senhaErrada999"
Então o status HTTP retornado deve ser 401
E o corpo da resposta deve conter o campo "message" com valor "Email e/ou senha inválidos"
```

**Payload enviado:**
```json
{
  "email": "<email_do_usuario_cadastrado>",
  "password": "senhaErrada999"
}
```

**Resposta esperada (401 Unauthorized):**
```json
{
  "message": "Email e/ou senha inválidos"
}
```

---

#### CT-014 — Login com e-mail inexistente

**Método:** `POST /login`

```gherkin
Dado que não existe nenhum usuário com o e-mail "inexistente@qatest.com"
Quando uma requisição POST é enviada para "/login" com esse e-mail e qualquer senha
Então o status HTTP retornado deve ser 401
E o corpo da resposta deve conter o campo "message" com valor "Email e/ou senha inválidos"
```

**Payload enviado:**
```json
{
  "email": "inexistente@qatest.com",
  "password": "qualquerSenha"
}
```

**Resposta esperada (401 Unauthorized):**
```json
{
  "message": "Email e/ou senha inválidos"
}
```

---

#### CT-015 — Login com campo "email" ausente

**Método:** `POST /login`

```gherkin
Dado que o payload de login está incompleto
E o campo "email" está ausente do corpo da requisição
Quando uma requisição POST é enviada para "/login" sem o campo "email"
Então o status HTTP retornado deve ser 400
E o corpo da resposta deve conter o campo "email" indicando que é obrigatório
```

**Payload enviado:**
```json
{
  "password": "senha123"
}
```

**Resposta esperada (400 Bad Request):**
```json
{
  "email": "email é obrigatório"
}
```

---

#### CT-016 — Login com campo "password" ausente

**Método:** `POST /login`

```gherkin
Dado que o payload de login está incompleto
E o campo "password" está ausente do corpo da requisição
Quando uma requisição POST é enviada para "/login" sem o campo "password"
Então o status HTTP retornado deve ser 400
E o corpo da resposta deve conter o campo "password" indicando que é obrigatório
```

**Payload enviado:**
```json
{
  "email": "usuario@qatest.com"
}
```

**Resposta esperada (400 Bad Request):**
```json
{
  "password": "password é obrigatório"
}
```

---

### 4.3 Endpoint: `/produtos` — CRUD de Produtos 🔜

> **Arquivo:** `tests/test_produtos.py`  
> **Auth requerida:** GET é público; POST, PUT e DELETE exigem token Bearer de usuário **administrador**  
> **Dependência de setup:** Requer login de administrador via `/login` para obter token.

| ID     | Status | Operação | Método | Cenário                                              | Status HTTP | Auth      |
|--------|--------|----------|--------|------------------------------------------------------|-------------|-----------|
| CT-017 | 🔜     | Read     | GET    | Listar todos os produtos                             | 200         | Nenhuma   |
| CT-018 | 🔜     | Read     | GET    | Buscar produto por ID existente                      | 200         | Nenhuma   |
| CT-019 | 🔜     | Read     | GET    | Buscar produto por ID inexistente                    | 400         | Nenhuma   |
| CT-020 | 🔜     | Create   | POST   | Cadastrar produto com token de admin                 | 201         | Admin ✅  |
| CT-021 | 🔜     | Create   | POST   | Cadastrar produto com nome duplicado                 | 400         | Admin ✅  |
| CT-022 | 🔜     | Create   | POST   | Cadastrar produto SEM token (não autenticado)        | 401         | Nenhuma ❌ |
| CT-023 | 🔜     | Create   | POST   | Cadastrar produto com token de não-admin              | 403         | Não-Admin ❌ |
| CT-024 | 🔜     | Update   | PUT    | Atualizar produto existente com token de admin        | 200         | Admin ✅  |
| CT-025 | 🔜     | Update   | PUT    | Atualizar produto com ID inexistente (upsert)         | 201         | Admin ✅  |
| CT-026 | 🔜     | Update   | PUT    | Atualizar produto SEM token                           | 401         | Nenhuma ❌ |
| CT-027 | 🔜     | Delete   | DELETE | Excluir produto existente com token de admin          | 200         | Admin ✅  |
| CT-028 | 🔜     | Delete   | DELETE | Excluir produto SEM token                             | 401         | Nenhuma ❌ |

#### Campos do payload de Produto

| Campo        | Tipo    | Obrigatório | Descrição                    |
|--------------|---------|-------------|------------------------------|
| `nome`       | string  | Sim         | Nome do produto (único)      |
| `preco`      | integer | Sim         | Preço em centavos (≥ 1)      |
| `descricao`  | string  | Sim         | Descrição do produto         |
| `quantidade` | integer | Sim         | Quantidade em estoque (≥ 0)  |

#### Detalhamento dos cenários de Produtos

---

#### CT-017 — Listar todos os produtos

**Método:** `GET /produtos`

```gherkin
Dado que a API ServeRest está disponível
Quando uma requisição GET é enviada para "/produtos"
Então o status HTTP retornado deve ser 200
E o corpo da resposta deve conter o campo "quantidade" do tipo inteiro
E o corpo da resposta deve conter o campo "produtos" do tipo array
E cada item do array deve possuir os campos "_id", "nome", "preco", "descricao" e "quantidade"
```

**Resposta esperada (200 OK):**
```json
{
  "quantidade": 2,
  "produtos": [
    {
      "nome": "Logitech MX Vertical",
      "preco": 470,
      "descricao": "Mouse",
      "quantidade": 381,
      "_id": "BeeJh5lz3k6kSIzA"
    }
  ]
}
```

---

#### CT-018 — Buscar produto por ID existente

**Método:** `GET /produtos/{id}`

```gherkin
Dado que existe um produto cadastrado com um ID válido
Quando uma requisição GET é enviada para "/produtos/{id}"
Então o status HTTP retornado deve ser 200
E o corpo da resposta deve conter os campos "_id", "nome", "preco", "descricao" e "quantidade"
```

**Resposta esperada (200 OK):**
```json
{
  "nome": "Logitech MX Vertical",
  "preco": 470,
  "descricao": "Mouse",
  "quantidade": 381,
  "_id": "BeeJh5lz3k6kSIzA"
}
```

---

#### CT-019 — Buscar produto por ID inexistente

**Método:** `GET /produtos/{id}`

```gherkin
Dado que não existe nenhum produto com o ID "idProdutoInexistente999"
Quando uma requisição GET é enviada para "/produtos/idProdutoInexistente999"
Então o status HTTP retornado deve ser 400
E o corpo da resposta deve conter o campo "message" com valor "Produto não encontrado"
```

**Resposta esperada (400 Bad Request):**
```json
{
  "message": "Produto não encontrado"
}
```

---

#### CT-020 — Cadastrar produto com token de admin

**Método:** `POST /produtos`  
**Header:** `Authorization: Bearer <token_admin>`

```gherkin
Dado que o usuário está autenticado como administrador
E o payload contém todos os campos obrigatórios preenchidos
E o nome do produto ainda não está cadastrado na base
Quando uma requisição POST é enviada para "/produtos" com o header Authorization válido
Então o status HTTP retornado deve ser 201
E o corpo da resposta deve conter o campo "message" com valor "Cadastro realizado com sucesso"
E o corpo da resposta deve conter o campo "_id" com o identificador gerado
```

**Payload enviado:**
```json
{
  "nome": "Produto QA Teste <uuid>",
  "preco": 150,
  "descricao": "Produto criado via teste automatizado",
  "quantidade": 50
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

#### CT-021 — Cadastrar produto com nome duplicado

**Método:** `POST /produtos`  
**Header:** `Authorization: Bearer <token_admin>`

```gherkin
Dado que o usuário está autenticado como administrador
E já existe um produto cadastrado com o mesmo nome
Quando uma requisição POST é enviada para "/produtos" com o nome duplicado
Então o status HTTP retornado deve ser 400
E o corpo da resposta deve conter o campo "message" com valor "Já existe produto com esse nome"
```

**Resposta esperada (400 Bad Request):**
```json
{
  "message": "Já existe produto com esse nome"
}
```

---

#### CT-022 — Cadastrar produto SEM token

**Método:** `POST /produtos`  
**Header:** *(sem Authorization)*

```gherkin
Dado que nenhum token de autenticação foi enviado no header
Quando uma requisição POST é enviada para "/produtos" sem o header Authorization
Então o status HTTP retornado deve ser 401
E o corpo da resposta deve conter o campo "message" com valor indicando token ausente/inválido
```

**Resposta esperada (401 Unauthorized):**
```json
{
  "message": "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"
}
```

---

#### CT-023 — Cadastrar produto com token de não-admin

**Método:** `POST /produtos`  
**Header:** `Authorization: Bearer <token_nao_admin>`

```gherkin
Dado que o usuário está autenticado mas NÃO é administrador (administrador = "false")
Quando uma requisição POST é enviada para "/produtos" com o header Authorization de não-admin
Então o status HTTP retornado deve ser 403
E o corpo da resposta deve conter o campo "message" com valor "Rota exclusiva para administradores"
```

**Resposta esperada (403 Forbidden):**
```json
{
  "message": "Rota exclusiva para administradores"
}
```

---

#### CT-024 — Atualizar produto existente com token de admin

**Método:** `PUT /produtos/{id}`  
**Header:** `Authorization: Bearer <token_admin>`

```gherkin
Dado que o usuário está autenticado como administrador
E existe um produto cadastrado com um ID válido
Quando uma requisição PUT é enviada para "/produtos/{id}" com payload atualizado
Então o status HTTP retornado deve ser 200
E o corpo da resposta deve conter o campo "message" com valor "Registro alterado com sucesso"
```

**Resposta esperada (200 OK):**
```json
{
  "message": "Registro alterado com sucesso"
}
```

---

#### CT-025 — Atualizar produto com ID inexistente (upsert)

**Método:** `PUT /produtos/{id}`  
**Header:** `Authorization: Bearer <token_admin>`

```gherkin
Dado que o usuário está autenticado como administrador
E não existe nenhum produto com o ID informado
Quando uma requisição PUT é enviada para "/produtos/idQueNaoExiste000"
Então o status HTTP retornado deve ser 201
E o corpo da resposta deve conter o campo "message" com valor "Cadastro realizado com sucesso"
E o corpo da resposta deve conter o campo "_id" com o identificador gerado
```

**Resposta esperada (201 Created):**
```json
{
  "message": "Cadastro realizado com sucesso",
  "_id": "novoIdGerado456"
}
```

---

#### CT-026 — Atualizar produto SEM token

**Método:** `PUT /produtos/{id}`  
**Header:** *(sem Authorization)*

```gherkin
Dado que nenhum token de autenticação foi enviado no header
Quando uma requisição PUT é enviada para "/produtos/{id}" sem o header Authorization
Então o status HTTP retornado deve ser 401
E o corpo da resposta deve conter o campo "message" com valor indicando token ausente/inválido
```

**Resposta esperada (401 Unauthorized):**
```json
{
  "message": "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"
}
```

---

#### CT-027 — Excluir produto existente com token de admin

**Método:** `DELETE /produtos/{id}`  
**Header:** `Authorization: Bearer <token_admin>`

```gherkin
Dado que o usuário está autenticado como administrador
E existe um produto cadastrado com um ID válido
E o produto não faz parte de nenhum carrinho
Quando uma requisição DELETE é enviada para "/produtos/{id}"
Então o status HTTP retornado deve ser 200
E o corpo da resposta deve conter o campo "message" com valor "Registro excluído com sucesso"
```

**Resposta esperada (200 OK):**
```json
{
  "message": "Registro excluído com sucesso"
}
```

---

#### CT-028 — Excluir produto SEM token

**Método:** `DELETE /produtos/{id}`  
**Header:** *(sem Authorization)*

```gherkin
Dado que nenhum token de autenticação foi enviado no header
Quando uma requisição DELETE é enviada para "/produtos/{id}" sem o header Authorization
Então o status HTTP retornado deve ser 401
E o corpo da resposta deve conter o campo "message" com valor indicando token ausente/inválido
```

**Resposta esperada (401 Unauthorized):**
```json
{
  "message": "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"
}
```

---

## 5. Fluxo de Autenticação — Dependência entre Endpoints

O diagrama abaixo mostra a cadeia de dependências para executar testes de produtos:

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────────────┐
│  POST /usuarios  │────►│   POST /login    │────►│  POST/PUT/DELETE         │
│  (cria user adm) │     │  (obtém token)   │     │  /produtos               │
│                  │     │                  │     │  (usa token no header    │
│  administrador:  │     │  Retorna:        │     │   Authorization)         │
│  "true"          │     │  "Bearer ey..."  │     │                          │
└──────────────────┘     └──────────────────┘     └──────────────────────────┘
```

### Fixture planejada: `admin_token`

```python
@pytest.fixture
def admin_token(api, temp_user):
    """
    Cria usuário admin temporário, faz login, retorna o token Bearer.
    O usuário é removido automaticamente no teardown do temp_user.
    """
    user = temp_user(administrador="true")
    response = api.post("/login", {
        "email": user["email"],
        "password": user["password"]
    }, "AUTH_SETUP")
    assert response.status_code == 200
    return response.json()["authorization"]
```

### Fixture planejada: `non_admin_token`

```python
@pytest.fixture
def non_admin_token(api, temp_user):
    """
    Cria usuário NÃO-admin temporário, faz login, retorna o token Bearer.
    Usado em cenários de teste de autorização (403).
    """
    user = temp_user(administrador="false")
    response = api.post("/login", {
        "email": user["email"],
        "password": user["password"]
    }, "NON_ADMIN_AUTH_SETUP")
    assert response.status_code == 200
    return response.json()["authorization"]
```

---

## 6. Critérios de Qualidade — Definição de "Teste Pronto"

Um caso de teste é considerado **pronto para merge** quando atende a **todos** os critérios abaixo:

### 6.1 Critérios Funcionais

| #  | Critério                                                                                   |
|----|--------------------------------------------------------------------------------------------|
| 1  | O teste valida **exatamente** o cenário descrito neste plano (ID, método, status esperado). |
| 2  | O **status code** da resposta é verificado via `assert_status()`.                          |
| 3  | O **campo `message`** (quando aplicável) é verificado via `assert_message()`.              |
| 4  | Campos obrigatórios da resposta são verificados via `assert_has_fields()` ou `assert_field_exists()`. |
| 5  | O teste é **independente**: não depende da execução de outro teste nem de ordem de execução. |
| 6  | O teste faz **cleanup** dos dados que cria (via fixture teardown ou DELETE explícito).      |

### 6.2 Critérios Técnicos

| #  | Critério                                                                                   |
|----|--------------------------------------------------------------------------------------------|
| 7  | Dados de teste são **gerados dinamicamente** (UUID) — nunca hardcoded.                     |
| 8  | Nenhuma credencial, token ou chave real está hardcoded no código.                          |
| 9  | O teste usa as **assertion helpers** de `utils/assertions.py` (não asserts crus).          |
| 10 | O teste usa `print_test_header()` para logging padronizado.                                |
| 11 | O teste possui **docstring** com o ID e a descrição do cenário.                            |
| 12 | O teste está marcado com o **pytest.mark** correto (`@pytest.mark.get`, `.post`, etc.).    |
| 13 | O teste passa com **retries = 2** (configurado em `pytest.ini`) sem falhas intermitentes recorrentes. |

### 6.3 Critérios de Revisão

| #  | Critério                                                                                   |
|----|--------------------------------------------------------------------------------------------|
| 14 | O teste foi executado localmente com sucesso (`pytest -v`).                                |
| 15 | O relatório HTML gerado (`report.html`) não mostra erros inesperados.                      |
| 16 | O plano de testes (`docs/plano_de_testes.md`) foi atualizado com o status ✅ do cenário.    |

---

## 7. Resumo Geral dos Cenários

| Faixa       | Endpoint     | Qtd. Cenários | Status       |
|-------------|--------------|---------------|--------------|
| CT-001–011  | `/usuarios`  | 11            | ✅ Implementado |
| CT-012–016  | `/login`     | 5             | 🔜 A implementar |
| CT-017–028  | `/produtos`  | 12            | 🔜 A implementar |
| **Total**   |              | **28**        |              |

---

## 8. Marks do pytest (planejados)

Atualizar `pytest.ini` para incluir os novos marks:

```ini
[pytest]
markers =
    get: Testes de endpoints GET
    post: Testes de endpoints POST
    put: Testes de endpoints PUT
    delete: Testes de endpoints DELETE
    login: Testes do endpoint POST /login
    produtos: Testes do endpoint /produtos
    usuarios: Testes do endpoint /usuarios
    auth: Testes que envolvem autenticação/autorização
```

---

## 9. Observações Técnicas

- A ServeRest reseta seus dados periodicamente — IDs usados nos cenários devem ser obtidos **dinamicamente** via fixtures, nunca hardcoded.
- O comportamento do `PUT` com ID inexistente é um **upsert**: cria o recurso caso não exista (vale para `/usuarios` e `/produtos`).
- O campo `administrador` aceita apenas os valores `"true"` ou `"false"` como **string**.
- O token de autenticação tem **TTL de 600 segundos** (10 minutos). Fixtures devem gerar tokens frescos por sessão/teste.
- O `ServeRestClient` precisa ser estendido para suportar headers customizados (token Bearer) nas chamadas de `/produtos`.
- Endpoints `POST /produtos`, `PUT /produtos/{id}` e `DELETE /produtos/{id}` retornam **403** se o token pertence a um usuário com `administrador = "false"`, e **401** se o token está ausente/inválido/expirado.
