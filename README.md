# Testes Automatizados API ServeRest — Endpoint `/usuarios`

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Testing Framework](https://img.shields.io/badge/test-pytest-green.svg)](https://docs.pytest.org/)
[![API Tool](https://img.shields.io/badge/API-ServeRest-orange.svg)](https://compassuol.serverest.dev/)

Este repositório contém o projeto de automação de testes de API desenvolvido para o endpoint `/usuarios` da plataforma **ServeRest** (`https://compassuol.serverest.dev`). O projeto implementa testes de integração abrangentes e robustos (do CT-001 ao CT-011) que cobrem operações de CRUD completas, validação de regras de negócio, dados dinâmicos e controle de ciclo de vida (setup e cleanup automatizados).

---

## 🚀 Destaques do Projeto

*   **Arquitetura Modular (Page/Client Pattern)**: Isolamento completo de requisições HTTP, geradores de payloads, asserções reutilizáveis e lógica de testes em camadas separadas.
*   **Dados 100% Dinâmicos**: E-mails e nomes são gerados em tempo de execução via `uuid4`, garantindo independência entre execuções e eliminando colisões de dados na API.
*   **Controle de Estado & Ciclo de Vida**: Utilização de fixtures do `pytest` com escopos de `session` e `function` que criam dados sementes e executam **cleanup automático (DELETE)** pós-testes, deixando a API limpa.
*   **Feedback Visual Avançado**: Logs estruturados em tempo real no console exibindo detalhes de cada Request, Response (JSON indentado) e o status detalhado das asserções (`[PASS]` / `[FAIL]`).
*   **Testes Parametrizados**: Redução drástica de boilerplate de código usando `@pytest.mark.parametrize` para testar múltiplos cenários de campos obrigatórios (ausência de `nome`, `email` ou `password`) em uma única lógica de teste.

---

## 📁 Estrutura do Projeto

O projeto está organizado da seguinte forma:

```text
qa-serverest/
├── .gitignore               # Arquivos ignorados pelo controle de versão (ex: .venv, caches, reports)
├── conftest.py              # Fixtures globais do pytest (cliente de API, usuário semente, fábrica temporária)
├── requirements.txt         # Definição das dependências e bibliotecas externas do Python
├── main.py                  # Script de entrada padrão (gerado pelo PyCharm, não utilizado nos testes)
├── docs/
│   └── plano_de_testes_usuarios.md   # Plano de testes descrevendo detalhadamente os cenários de CT-001 a CT-011
├── tests/
│   └── test_usuarios.py     # Arquivo contendo as classes e métodos de testes agrupados por operação
└── utils/                   # Módulos auxiliares e helpers de apoio
    ├── __init__.py          # Constantes globais (BASE_URL, USER_FIELDS) e fábrica de dados dinâmicos
    ├── api_client.py        # Classe ServeRestClient (encapsula requests HTTP e gera logs automáticos)
    ├── assertions.py        # Helpers personalizados de asserção (assert_status, assert_message, etc.)
    └── logger.py            # Funções utilitárias de print e formatação de console
```

---

## ⚙️ Detalhes das Implementações

### 1. `utils/` (Helpers e Configurações)
*   **`api_client.py`**: Contém a classe `ServeRestClient` que herda/utiliza a biblioteca `requests`. Toda requisição HTTP (`GET`, `POST`, `PUT`, `DELETE`) feita por meio deste cliente gera automaticamente um log estruturado com a URL visitada, método, headers, payload enviado e o JSON retornado pela API.
*   **`assertions.py`**: Funções reutilizáveis que combinam a cláusula `assert` do Python com prints formatados. Se uma validação falhar, ela joga uma exceção com uma mensagem legível detalhando o que foi esperado e o que foi de fato recebido.
*   **`__init__.py`**: Contém funções utilitárias como `build_user_payload()` que gera dados válidos ou aceita overrides (sobreposição de valores) para testar fluxos de erro ou payloads incompletos.

### 2. `conftest.py` (Ciclo de Vida)
*   **`api`**: Fornece uma instância persistente do `ServeRestClient`.
*   **`session_user`**: Cria um usuário admin válido no início da execução dos testes e remove esse usuário ao término de toda a sessão de testes.
*   **`temp_user`**: Uma fixture do tipo fábrica (`yield _create`) que permite aos testes criarem usuários temporários no meio de sua execução. Todos os usuários criados através desta fábrica são coletados e deletados no pós-teste (`teardown`).

### 3. `tests/test_usuarios.py` (Suíte de Testes)
Os testes estão agrupados em classes organizadas por feature do endpoint `/usuarios`:
*   `TestListarBuscarUsuarios` (`GET`): Cobre listagem geral, busca por ID existente e busca por ID inexistente.
*   `TestCadastrarUsuarios` (`POST`): Cobre criação de usuário válido, validação de e-mail duplicado e validação de campos obrigatórios (parametrizado).
*   `TestAtualizarUsuarios` (`PUT`): Cobre atualização de usuário cadastrado e criação de usuário inexistente via `PUT` (upsert).
*   `TestExcluirUsuarios` (`DELETE`): Cobre deleção de usuário cadastrado e tentativa de deleção de usuário inexistente.

---

## 📦 Dependências

O projeto utiliza as seguintes dependências principais do Python

1.  **`requests` (==2.32.3)**: Biblioteca HTTP para envio das requisições e consumo da API RESTful.
2.  **`pytest` (==8.3.5)**: Framework de testes utilizado para estruturar a suíte de validações, fixtures e parametrizações.
3.  **`pytest-html` (==4.1.1)**: Plugin responsável por gerar relatórios HTML elegantes a partir dos resultados dos testes executados.
---

## Casos de Teste

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


## 🛠️ Como Executar o Projeto (Windows)

Siga os passos abaixo no terminal do Windows (PowerShell ou CMD) para rodar o projeto localmente.

### Passo 1: Clonar e abrir o diretório do projeto
Navegue até a pasta raiz do projeto:
```powershell
cd qa-serverest
```

### Passo 2: Criar o Ambiente Virtual (venv)
Para isolar as dependências do projeto, crie um ambiente virtual executando:
```powershell
python -m venv .venv
```

### Passo 3: Ativar o Ambiente Virtual
*   **No PowerShell:**
    ```powershell
    .venv\Scripts\Activate.ps1
    ```
*   **No CMD:**
    ```cmd
    .venv\Scripts\activate.bat
    ```

### Passo 4: Instalar as Dependências
Com o ambiente virtual ativado, instale os pacotes necessários:
```powershell
pip install -r requirements.txt
```

### Passo 5: Executar os Testes

*   **Execução Padrão com Logs Detalhados no Console (Recomendado):**
    ```powershell
    pytest -v -s
    ```
    *(O parâmetro `-v` ativa o modo verboso e `-s` exibe todos os outputs estruturados e logs detalhados das requests no terminal).*

*   **Executar Gerando Relatório HTML:**
    ```powershell
    pytest --html=report.html --self-contained-html
    ```
    *(Isso criará um arquivo `report.html` auto-contido na raiz do projeto com o resumo gráfico de toda a execução dos testes).*

*   **Executar apenas um cenário de teste específico:**
    ```powershell
    pytest tests/test_usuarios.py -k "TestCadastrarUsuarios" -v -s
    ```
