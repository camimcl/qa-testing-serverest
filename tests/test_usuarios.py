"""
Testes automatizados -- Endpoint /usuarios | ServeRest API
Plano de testes: docs/plano_de_testes_usuarios.md

CT-001 a CT-011: CRUD completo com dados 100% dinamicos.
Organizados por classe (feature): GET, POST, PUT, DELETE.
"""

import pytest

from utils import build_user_payload, USER_FIELDS
from utils.logger import print_test_header
from utils.assertions import (
    assert_status,
    assert_message,
    assert_field_exists,
    assert_field_equals,
    assert_has_fields,
)


# ===========================================================
#  GET /usuarios — Leitura
# ===========================================================

@pytest.mark.get
class TestGetUsuarios:
    """CT-001 a CT-003: Leitura de usuarios."""

    def test_ct001_list_all_users(self, api):
        """CT-001 -- Listar todos os usuarios com sucesso."""
        print_test_header("CT-001", "Listar todos os usuarios")

        response = api.get("/usuarios", "CT-001")
        body = assert_status(response, 200, "CT-001")

        assert isinstance(body["quantidade"], int), (
            f"[CT-001 FALHOU] 'quantidade' deveria ser int, "
            f"eh {type(body['quantidade']).__name__}"
        )
        assert isinstance(body["usuarios"], list), (
            "[CT-001 FALHOU] 'usuarios' deveria ser list"
        )
        if body["usuarios"]:
            assert_has_fields(body["usuarios"][0], USER_FIELDS, "CT-001")

    def test_ct002_get_user_by_valid_id(self, api, session_user):
        """CT-002 -- Buscar usuario por ID existente (dinamico)."""
        print_test_header("CT-002", "Buscar usuario por ID existente")

        uid = session_user["_id"]
        response = api.get(f"/usuarios/{uid}", "CT-002")
        body = assert_status(response, 200, "CT-002")
        assert_has_fields(body, USER_FIELDS, "CT-002")
        assert_field_equals(body, "_id", uid, "CT-002")

    def test_ct003_get_user_by_invalid_id(self, api):
        """CT-003 -- Buscar usuario por ID inexistente."""
        print_test_header("CT-003", "Buscar usuario por ID inexistente")

        response = api.get("/usuarios/idInexistente999", "CT-003")
        body = assert_status(response, 400, "CT-003")
        assert_message(body, "Usuário não encontrado", "CT-003")


# ===========================================================
#  POST /usuarios — Criacao
# ===========================================================

@pytest.mark.post
class TestPostUsuarios:
    """CT-004 a CT-008: Criacao de usuarios."""

    def test_ct004_create_user_success(self, api):
        """CT-004 -- Cadastrar usuario com sucesso (caminho feliz)."""
        print_test_header("CT-004", "Cadastrar usuario com sucesso")

        payload = build_user_payload()
        response = api.post("/usuarios", payload, "CT-004")
        body = assert_status(response, 201, "CT-004")
        assert_message(body, "Cadastro realizado com sucesso", "CT-004")
        assert_field_exists(body, "_id", "CT-004")

        # Cleanup
        api.delete(f"/usuarios/{body['_id']}", "CT-004 CLEANUP")

    def test_ct005_create_user_duplicate_email(self, api, session_user):
        """CT-005 -- Cadastrar usuario com e-mail duplicado (do session_user)."""
        print_test_header("CT-005", "Cadastrar usuario com e-mail duplicado")

        payload = build_user_payload(email=session_user["email"])
        print(f"     !! E-mail duplicado: {session_user['email']}")
        response = api.post("/usuarios", payload, "CT-005")
        body = assert_status(response, 400, "CT-005")
        assert_message(body, "Este email já está sendo usado", "CT-005")

    @pytest.mark.parametrize("field, test_id", [
        ("nome", "CT-006"),
        ("email", "CT-007"),
        ("password", "CT-008"),
    ], ids=["sem_nome", "sem_email", "sem_password"])
    def test_create_user_missing_required_field(self, api, field, test_id):
        """CT-006/007/008 -- Cadastrar usuario sem campo obrigatorio (parametrizado)."""
        print_test_header(test_id, f"Cadastrar usuario sem campo '{field}'")

        payload = build_user_payload(exclude_fields=[field])
        print(f"     !! Campo '{field}' removido propositalmente")
        response = api.post("/usuarios", payload, test_id)
        body = assert_status(response, 400, test_id)
        assert_field_equals(body, field, f"{field} é obrigatório", test_id)


# ===========================================================
#  PUT /usuarios — Atualizacao
# ===========================================================

@pytest.mark.put
class TestPutUsuarios:
    """CT-009 a CT-010: Atualizacao de usuarios."""

    def test_ct009_update_existing_user(self, api, session_user):
        """CT-009 -- Atualizar usuario existente com dados dinamicos."""
        print_test_header("CT-009", "Atualizar usuario existente")

        uid = session_user["_id"]
        payload = build_user_payload(administrador="false")
        print(f"     >> ID: {uid} | Novo email: {payload['email']}")
        response = api.put(f"/usuarios/{uid}", payload, "CT-009")
        body = assert_status(response, 200, "CT-009")
        assert_message(body, "Registro alterado com sucesso", "CT-009")

        # Sincroniza dados da fixture para testes seguintes
        session_user.update(payload)

    def test_ct010_update_nonexistent_user_upsert(self, api):
        """CT-010 -- PUT com ID inexistente deve criar (upsert)."""
        print_test_header("CT-010", "PUT com ID inexistente (upsert)")

        payload = build_user_payload()
        response = api.put("/usuarios/idQueNaoExiste000", payload, "CT-010")
        body = assert_status(response, 201, "CT-010")
        assert_message(body, "Cadastro realizado com sucesso", "CT-010")
        assert_field_exists(body, "_id", "CT-010")

        # Cleanup
        api.delete(f"/usuarios/{body['_id']}", "CT-010 CLEANUP")


# ===========================================================
#  DELETE /usuarios — Exclusao
# ===========================================================

@pytest.mark.delete
class TestDeleteUsuarios:
    """CT-011: Exclusao de usuarios."""

    def test_ct011_delete_existing_user(self, api, temp_user):
        """CT-011 -- Deletar usuario existente e verificar exclusao."""
        print_test_header("CT-011", "Deletar usuario existente")

        # Setup: cria usuario temporario via fixture (cleanup automatico)
        user = temp_user()
        print(f"     >> Usuario temporario criado: ID={user['_id']}")

        # Acao: deletar
        response = api.delete(f"/usuarios/{user['_id']}", "CT-011")
        body = assert_status(response, 200, "CT-011")
        assert_message(body, "Registro excluído com sucesso", "CT-011")

        # Verificacao: confirmar que nao existe mais
        print(f"\n  [VERIFY] Confirmando exclusao do usuario {user['_id']}...")
        verify = api.get(f"/usuarios/{user['_id']}", "CT-011 VERIFY")
        assert_status(verify, 400, "CT-011")
