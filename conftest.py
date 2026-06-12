"""
Fixtures globais do pytest para os testes da API ServeRest.
Gerencia ciclo de vida dos dados de teste (criacao/limpeza).
"""

import pytest

from utils import BASE_URL, build_user_payload
from utils.api_client import ServeRestClient


@pytest.fixture(scope="session")
def api():
    """Cliente API reutilizado por toda a sessao de testes."""
    return ServeRestClient(BASE_URL)


@pytest.fixture(scope="session")
def session_user(api):
    """
    Cria um usuario 'semente' com dados dinamicos no inicio da sessao.
    Usado pelos testes que precisam de um usuario pre-existente (CT-002, CT-005, CT-009).
    Removido automaticamente no teardown.
    """
    payload = build_user_payload(administrador="true")
    response = api.post("/usuarios", payload, "SETUP")

    assert response.status_code == 201, (
        f"[SETUP FALHOU] Nao foi possivel criar usuario semente.\n"
        f"Status: {response.status_code} | Body: {response.text}"
    )

    data = response.json()
    user = {"_id": data["_id"], **payload}
    print(f"\n  [SETUP] Usuario semente criado: ID={user['_id']} | Email={user['email']}")

    yield user

    api.delete(f"/usuarios/{user['_id']}", "TEARDOWN")
    print(f"\n  [TEARDOWN] Usuario semente {user['_id']} removido.")


@pytest.fixture
def temp_user(api):
    """
    Factory fixture para criar usuarios temporarios com cleanup automatico.

    Uso nos testes:
        user = temp_user()           # cria com dados dinamicos
        user = temp_user(admin="false")  # cria com override

    No teardown, todos os IDs criados sao removidos via DELETE.
    """
    created_ids = []

    def _create(**overrides) -> dict:
        payload = build_user_payload(**overrides)
        response = api.post("/usuarios", payload, "TEMP_SETUP")
        assert response.status_code == 201, (
            f"[TEMP_SETUP FALHOU] {response.text}"
        )
        data = response.json()
        created_ids.append(data["_id"])
        return {"_id": data["_id"], **payload}

    yield _create

    for uid in created_ids:
        api.delete(f"/usuarios/{uid}", "TEMP_CLEANUP")
