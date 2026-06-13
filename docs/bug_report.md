# Bug Report — ServeRest API

> **Repositório:** qa-serverest  
> **API:** `https://compassuol.serverest.dev/`  
> **Versão da API:** 3.2.0  
> **Data de início:** 2025-06-13

---

## Como usar este documento

Este documento registra **bugs e comportamentos inesperados** encontrados durante a implementação e execução dos testes automatizados. Cada entrada segue o padrão de bug report para ser migrada diretamente como **Issue no GitHub**.

### Severidade

| Nível    | Descrição                                                       |
|----------|-----------------------------------------------------------------|
| 🔴 Alta  | Falha de segurança, perda de dados ou funcionalidade bloqueante |
| 🟡 Média | Comportamento incorreto mas com workaround possível             |
| 🟢 Baixa | Inconsistência cosmética, de documentação ou de boas práticas   |

---

## Bugs Encontrados

---

### BUG-001 — Senhas de usuários expostas em texto plano via GET /usuarios

**Severidade:** 🔴 Alta  
**Endpoint:** `GET /usuarios` e `GET /usuarios/{id}`  
**Encontrado em:** Execução dos testes CT-001 e CT-002 (`test_usuarios.py`)

#### Passos para Reproduzir

1. Cadastrar um usuário via `POST /usuarios` com o payload:
   ```json
   {
     "nome": "Teste Senha",
     "email": "teste.senha@qa.com",
     "password": "minhaSenhaSecreta",
     "administrador": "true"
   }
   ```
2. Fazer uma requisição `GET /usuarios` (sem autenticação).
3. Observar o campo `password` no corpo da resposta.

#### Resultado Esperado

O campo `password` **não deveria ser retornado** nas respostas de leitura, ou deveria ser retornado como hash (ex: `$2b$10$...`). Expor senhas em texto plano é uma falha de segurança crítica, mesmo em uma API de estudos.

#### Resultado Obtido

A senha é retornada **exatamente como foi enviada**, em texto plano, para qualquer pessoa que consulte o endpoint (sem necessidade de autenticação):

```json
{
  "nome": "Teste Senha",
  "email": "teste.senha@qa.com",
  "password": "minhaSenhaSecreta",   // ⚠️ Texto plano!
  "administrador": "true",
  "_id": "abc123"
}
```

#### Evidência

Trecho do log de execução do teste CT-001:
```
[RESPONSE] (CT-001):
   Status Code: 200
   Body:
     {
       "quantidade": 2,
       "usuarios": [
         {
           "nome": "QA User f8dffc8d",
           "email": "user_5e2e4de2c1b5@qatest.com",
           "password": "senha123",          // ← exposta em texto plano
           "administrador": "true",
           "_id": "y37QzZLWJuo8PJ6A"
         }
       ]
     }
```

#### Impacto

- Qualquer pessoa com acesso à rede pode capturar senhas de todos os usuários.
- O endpoint `GET /usuarios` é **público** (não exige autenticação), agravando o risco.
- Viola o princípio de **menor privilégio** e boas práticas de segurança (OWASP).

---

### BUG-002 — Endpoint GET /usuarios retorna dados sem paginação

**Severidade:** 🟢 Baixa  
**Endpoint:** `GET /usuarios`  
**Encontrado em:** Execução do teste CT-001 (`test_usuarios.py`)

#### Passos para Reproduzir

1. Fazer uma requisição `GET /usuarios` sem parâmetros.
2. Observar que **todos** os usuários são retornados de uma vez.

#### Resultado Esperado

A API deveria suportar paginação (ex: `?page=1&limit=10`) para evitar respostas excessivamente grandes quando a base de dados cresce.

#### Resultado Obtido

Todos os registros são retornados em uma única resposta, sem limite. O campo `quantidade` reflete o total absoluto de registros.

#### Evidência

Confirmado pela ausência de parâmetros de paginação na documentação Swagger e pelo comportamento observado em tempo de execução.

#### Impacto

- Em bases de dados grandes, a resposta pode ficar muito lenta ou causar timeout.
- Não é bloqueante para testes atuais, pois a API pública reseta dados periodicamente.

---

### BUG-003 — Endpoint POST /login retorna mensagem genérica para e-mail inexistente e senha errada (observação)

**Severidade:** 🟢 Baixa (por design, mas vale documentar)  
**Endpoint:** `POST /login`  
**Encontrado em:** Execução dos testes CT-013 e CT-014 (`test_login.py`)

#### Passos para Reproduzir

1. Fazer `POST /login` com um e-mail que **existe** mas senha **errada**.
2. Fazer `POST /login` com um e-mail que **não existe**.
3. Comparar as respostas.

#### Resultado Esperado (discussão)

Do ponto de vista de **segurança**, retornar a mesma mensagem genérica é a prática correta — impede que um atacante descubra quais e-mails estão cadastrados (enumeração de usuários).

#### Resultado Obtido

Ambos os cenários retornam exatamente:
```json
{
  "message": "Email e/ou senha inválidos"
}
```

#### Observação

Este **não é um bug** — é um comportamento de segurança adequado. Documentado aqui para consciência do time, pois a mensagem genérica pode confundir usuários legítimos que digitaram o e-mail errado.

**Status:** ✅ Comportamento correto por design.

---

## Observações de Infraestrutura

---

### OBS-001 — Configuração `retries` e `retry_delay` não reconhecidas pelo pytest

**Severidade:** 🟡 Média (afeta infraestrutura de testes, não a API)  
**Arquivo:** `pytest.ini`  
**Encontrado em:** Todas as execuções de testes

#### Descrição

O pytest emite warnings durante a execução:

```
PytestConfigWarning: Unknown config option: retries
PytestConfigWarning: Unknown config option: retry_delay
```

#### Causa Provável

O plugin `pytest-retry` (v1.7.0) pode usar nomes de configuração diferentes (`--retries` como argumento CLI, não como opção de `pytest.ini`), ou a versão instalada não suporta essas opções via arquivo de configuração.

#### Ação Sugerida

Verificar a documentação do `pytest-retry` 1.7.0 para os nomes corretos de configuração, ou migrar a configuração de retries para a CLI:
```bash
pytest --retries 2 --retry-delay 1
```

---

## Resumo

| ID      | Tipo         | Severidade | Endpoint           | Status       |
|---------|--------------|------------|--------------------|--------------|
| BUG-001 | Bug (API)    | 🔴 Alta    | GET /usuarios      | 📋 A reportar |
| BUG-002 | Bug (API)    | 🟢 Baixa   | GET /usuarios      | 📋 A reportar |
| BUG-003 | Observação   | 🟢 Baixa   | POST /login        | ✅ Por design |
| OBS-001 | Infra        | 🟡 Média   | pytest.ini         | 🔧 A corrigir |

---

*Este documento será atualizado conforme novos bugs forem encontrados durante a implementação dos testes de `/produtos` (CT-017 a CT-028).*
