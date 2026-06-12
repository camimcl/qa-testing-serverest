"""
Utilitarios compartilhados para os testes da API ServeRest.
Geracaoo dinamica de dados e payload factory.
"""

import uuid


# ------------------------------------------
#  BASE URL - Centralizada para facil manutencao
# ------------------------------------------
BASE_URL = "https://compassuol.serverest.dev"

# Campos obrigatorios de um usuario na API
USER_FIELDS = {"_id", "nome", "email", "password", "administrador"}


def generate_unique_email() -> str:
    """Gera e-mail unico via UUID4. Ex: user_a1b2c3d4e5f6@qatest.com"""
    return f"user_{uuid.uuid4().hex[:12]}@qatest.com"


def generate_unique_name() -> str:
    """Gera nome unico via UUID4. Ex: QA User a1b2c3d4"""
    return f"QA User {uuid.uuid4().hex[:8]}"


def build_user_payload(
    nome: str = None,
    email: str = None,
    password: str = "senha123",
    administrador: str = "true",
    exclude_fields: list = None
) -> dict:
    """
    Factory para payloads de usuario. Gera dados dinamicos por padrao.
    Use exclude_fields para remover campos (testes de validacao).
    """
    payload = {
        "nome": nome or generate_unique_name(),
        "email": email or generate_unique_email(),
        "password": password,
        "administrador": administrador
    }
    if exclude_fields:
        for field in exclude_fields:
            payload.pop(field, None)
    return payload
