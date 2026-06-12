"""
Assertion helpers com logging automatico.
Cada funcao combina assert + mensagem de erro detalhada + print [PASS]/[FAIL],
eliminando ~5 linhas de repeticao por validacao nos testes.
"""

import json

from utils.logger import print_assertion_result


def assert_status(response, expected_status: int, test_id: str, context: str = "") -> dict:
    """
    Valida status code e retorna o body como dict.
    Em caso de falha, exibe status recebido + body completo.
    """
    body = response.json()
    assert response.status_code == expected_status, (
        f"[{test_id} FALHOU] Esperava status {expected_status}, "
        f"recebeu {response.status_code}.\n"
        f"{context}\n"
        f"Body: {json.dumps(body, indent=2, ensure_ascii=False)}"
    )
    print_assertion_result(test_id, True, f"Status code = {response.status_code}")
    return body


def assert_message(body: dict, expected_msg: str, test_id: str) -> None:
    """Valida o campo 'message' da resposta."""
    actual = body.get("message")
    assert actual == expected_msg, (
        f"[{test_id} FALHOU] Mensagem esperada: '{expected_msg}'\n"
        f"Mensagem recebida: '{actual}'"
    )
    print_assertion_result(test_id, True, f"message = '{actual}'")


def assert_field_exists(body: dict, field: str, test_id: str) -> None:
    """Valida que um campo existe na resposta."""
    assert field in body, (
        f"[{test_id} FALHOU] Campo '{field}' nao encontrado.\n"
        f"Campos presentes: {list(body.keys())}"
    )
    print_assertion_result(test_id, True, f"Campo '{field}' presente = '{body[field]}'")


def assert_field_equals(body: dict, field: str, expected, test_id: str) -> None:
    """Valida que um campo tem o valor esperado."""
    actual = body.get(field)
    assert actual == expected, (
        f"[{test_id} FALHOU] {field} esperado: '{expected}'\n"
        f"{field} recebido: '{actual}'"
    )
    print_assertion_result(test_id, True, f"{field} = '{actual}'")


def assert_has_fields(body: dict, fields: set, test_id: str) -> None:
    """Valida que todos os campos obrigatorios estao presentes."""
    missing = fields - set(body.keys())
    assert not missing, (
        f"[{test_id} FALHOU] Campos faltando: {missing}\n"
        f"Campos presentes: {list(body.keys())}"
    )
    print_assertion_result(test_id, True, f"Campos presentes: {sorted(fields)}")
