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


@pytest.fixture
def isolated_user(api):
    """
    Cria um usuario exclusivo por teste e remove ao final (escopo function).

    Substitui o antigo 'session_user' (scope=session) que era nao-confiavel
    contra a API publica ServeRest: IDs criados no setup podiam expirar antes
    dos testes CT-002, CT-005 e CT-009 chegarem a usa-los.

    Cada teste recebe um usuario novo, com ID garantidamente valido.
    """
    payload = build_user_payload(administrador="true")
    response = api.post("/usuarios", payload, "ISOLATED_SETUP")

    assert response.status_code == 201, (
        f"[ISOLATED_SETUP FALHOU] Nao foi possivel criar usuario isolado.\n"
        f"Status: {response.status_code} | Body: {response.text}"
    )

    data = response.json()
    user = {"_id": data["_id"], **payload}
    print(f"\n  [ISOLATED_SETUP] Usuario criado: ID={user['_id']} | Email={user['email']}")

    yield user

    api.delete(f"/usuarios/{user['_id']}", "ISOLATED_TEARDOWN")
    print(f"\n  [ISOLATED_TEARDOWN] Usuario {user['_id']} removido.")


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
