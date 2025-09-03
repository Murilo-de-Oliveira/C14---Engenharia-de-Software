import httpx
from typing import Optional


class GitHubUserNotFound(Exception):
    """Exceção para usuário inexistente no GitHub."""


class InvalidUsername(Exception):
    """Exceção para nome de usuário inválido."""


class GitHubClient:
    BASE_URL = "https://api.github.com/users"

    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def get_user(self, username: str) -> dict:
        """
        Consulta a API do GitHub para obter informações de um usuário.
        """
        if not username or not username.strip():
            raise InvalidUsername("O username não pode ser vazio.")

        url = f"{self.BASE_URL}/{username}"
        try:
            response = httpx.get(url, timeout=self.timeout)
            if response.status_code == 404:
                raise GitHubUserNotFound(f"Usuário '{username}' não encontrado.")
            response.raise_for_status()
        except httpx.TimeoutException:
            raise TimeoutError("A requisição para o GitHub excedeu o tempo limite.")

        data = response.json()
        return {
            "login": data.get("login"),
            "name": data.get("name"),
            "public_repos": data.get("public_repos", 0),
            "followers": data.get("followers", 0),
            "following": data.get("following", 0),
            "url": data.get("html_url"),
        }

    def user_exists(self, username: str) -> bool:
        """Retorna True se o usuário existir no GitHub."""
        try:
            self.get_user(username)
            return True
        except (GitHubUserNotFound, TimeoutError):
            return False


class NetworkUtils:
    @staticmethod
    def get_ip(timeout: int = 5) -> str:
        """Retorna o IP público usando a API ipify"""
        url = "https://api.ipify.org?format=json"
        try:
            resp = httpx.get(url, timeout=timeout)
            resp.raise_for_status()
        except httpx.TimeoutException:
            raise TimeoutError("Timeout ao consultar IP público.")
        return resp.json().get("ip", "")
