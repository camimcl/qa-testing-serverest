"""
Cliente HTTP para a API ServeRest com logging automatico.
Encapsula requests.get/post/put/delete + print de request/response
em uma unica chamada, eliminando repeticao nos testes.
"""

import requests

from utils.logger import print_request_details, print_response_details


class ServeRestClient:
    """
    Cada metodo (get, post, put, delete) automaticamente:
    1. Monta a URL completa (base_url + path)
    2. Imprime [REQUEST] com metodo, URL e payload
    3. Executa a chamada HTTP
    4. Imprime [RESPONSE] com status, tempo e body
    5. Retorna o objeto Response
    """

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get(self, path: str, test_id: str = "") -> requests.Response:
        url = f"{self.base_url}{path}"
        print_request_details("GET", url)
        response = requests.get(url)
        print_response_details(response, test_id)
        return response

    def post(self, path: str, payload: dict, test_id: str = "") -> requests.Response:
        url = f"{self.base_url}{path}"
        print_request_details("POST", url, payload)
        response = requests.post(url, json=payload)
        print_response_details(response, test_id)
        return response

    def put(self, path: str, payload: dict, test_id: str = "") -> requests.Response:
        url = f"{self.base_url}{path}"
        print_request_details("PUT", url, payload)
        response = requests.put(url, json=payload)
        print_response_details(response, test_id)
        return response

    def delete(self, path: str, test_id: str = "") -> requests.Response:
        url = f"{self.base_url}{path}"
        print_request_details("DELETE", url)
        response = requests.delete(url)
        print_response_details(response, test_id)
        return response
