"""
Testes automatizados -- Endpoint /login | ServeRest API
Plano de testes: docs/plano_de_testes.md (secao 4.2)

CT-012 a CT-016: Autenticacao (login com sucesso, credenciais invalidas, campos ausentes).
Organizados por classe (feature): Login com Sucesso, Login com Falha, Validacao de Campos.
"""

import pytest

from utils import build_login_payload, LOGIN_SUCCESS_FIELDS
from utils.logger import print_test_header
from utils.assertions import (
    assert_status,
    assert_message,
    assert_field_exists,
    assert_field_equals,
    assert_has_fields,
)


# ===========================================================
#  POST /login — Autenticacao
# ===========================================================

@pytest.mark.login
@pytest.mark.post
class TestPostLogin:
    """CT-012 a CT-016: Autenticacao via /login."""

    def test_ct012_login_with_valid_credentials(self, api, temp_user):
        """CT-012 -- Login com credenciais corretas (admin).

        Cria usuario admin temporario via fixture, faz login com as
        credenciais corretas e valida que o token Bearer e retornado.
        """
        print_test_header("CT-012", "Login com credenciais corretas (admin)")

        # Setup: cria usuario admin com credenciais conhecidas
        user = temp_user(administrador="true")
        print(f"     >> Usuario criado: {user['email']} | senha: {user['password']}")

        # Acao: faz login com as credenciais do usuario criado
        payload = build_login_payload(
            email=user["email"],
            password=user["password"]
        )
        response = api.post("/login", payload, "CT-012")
        body = assert_status(response, 200, "CT-012")

        # Validacao: resposta deve conter message e authorization
        assert_message(body, "Login realizado com sucesso", "CT-012")
        assert_has_fields(body, LOGIN_SUCCESS_FIELDS, "CT-012")

        # Validacao: token deve comecar com "Bearer "
        token = body.get("authorization", "")
        assert token.startswith("Bearer "), (
            f"[CT-012 FALHOU] Token nao comeca com 'Bearer '.  "
            f"Recebido: '{token[:30]}...'"
        )
        print(f"\n  [PASS] CT-012 -- Token Bearer recebido: {token[:50]}...")

    def test_ct013_login_with_wrong_password(self, api, temp_user):
        """CT-013 -- Login com senha errada.

        Cria usuario temporario e tenta login com a senha incorreta.
        """
        print_test_header("CT-013", "Login com senha errada")

        # Setup: cria usuario com senha conhecida
        user = temp_user(administrador="true")
        print(f"     >> Usuario: {user['email']} | senha real: {user['password']}")

        # Acao: tenta login com senha errada
        payload = build_login_payload(
            email=user["email"],
            password="senhaErrada999"
        )
        print(f"     !! Senha enviada: 'senhaErrada999' (incorreta)")
        response = api.post("/login", payload, "CT-013")
        body = assert_status(response, 401, "CT-013")
        assert_message(body, "Email e/ou senha inválidos", "CT-013")

    def test_ct014_login_with_nonexistent_email(self, api):
        """CT-014 -- Login com e-mail inexistente.

        Usa um e-mail gerado dinamicamente que nao existe na base.
        """
        print_test_header("CT-014", "Login com e-mail inexistente")

        payload = build_login_payload(
            email="inexistente_naoexiste@qatest.com",
            password="qualquerSenha123"
        )
        print(f"     !! E-mail inexistente: '{payload['email']}'")
        response = api.post("/login", payload, "CT-014")
        body = assert_status(response, 401, "CT-014")
        assert_message(body, "Email e/ou senha inválidos", "CT-014")

    @pytest.mark.parametrize("field, test_id", [
        ("email", "CT-015"),
        ("password", "CT-016"),
    ], ids=["sem_email", "sem_password"])
    def test_login_missing_required_field(self, api, field, test_id):
        """CT-015/CT-016 -- Login sem campo obrigatorio (parametrizado).

        Envia payload sem o campo indicado e valida que a API retorna
        erro 400 informando que o campo e obrigatorio.
        """
        print_test_header(test_id, f"Login sem campo '{field}'")

        payload = build_login_payload(exclude_fields=[field])
        print(f"     !! Campo '{field}' removido propositalmente")
        response = api.post("/login", payload, test_id)
        body = assert_status(response, 400, test_id)
        assert_field_equals(body, field, f"{field} é obrigatório", test_id)
