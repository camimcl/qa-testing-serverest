"""
Funcoes de logging para feedback visual dos testes no terminal.
"""

import json


def print_test_header(test_id: str, description: str) -> None:
    """Imprime cabecalho visual do cenario de teste."""
    sep = "=" * 70
    print(f"\n{sep}")
    print(f"  [TEST] {test_id} -- {description}")
    print(f"{sep}")


def print_request_details(method: str, url: str, payload: dict = None) -> None:
    """Imprime metodo, URL e payload da requisicao."""
    print(f"\n  [REQUEST]")
    print(f"     Metodo:  {method}")
    print(f"     URL:     {url}")
    if payload is not None:
        print(f"     Payload: {json.dumps(payload, indent=2, ensure_ascii=False)}")


def print_response_details(response, test_id: str) -> None:
    """Imprime status code, tempo e body formatado da resposta."""
    print(f"\n  [RESPONSE] ({test_id}):")
    print(f"     Status Code: {response.status_code}")
    print(f"     Tempo:       {response.elapsed.total_seconds():.3f}s")
    try:
        body = response.json()
        print(f"     Body:")
        for line in json.dumps(body, indent=2, ensure_ascii=False).split("\n"):
            print(f"       {line}")
    except ValueError:
        print(f"     Body (raw): {response.text[:500]}")


def print_assertion_result(test_id: str, passed: bool, detail: str = "") -> None:
    """Imprime [PASS] ou [FAIL] com detalhe da assercao."""
    icon = "[PASS]" if passed else "[FAIL]"
    status = "PASSOU" if passed else "FALHOU"
    msg = f"\n  {icon} {test_id} -- {status}"
    if detail:
        msg += f" | {detail}"
    print(msg)
