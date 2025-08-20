import httpx
 
 
def get_github_user(username: str) -> dict:
    """
    Consulta a API pública do GitHub e retorna informações de um usuário.
 
    Args:
        username (str): Nome de usuário no GitHub.
 
    Returns:
        dict: Dicionário com os dados principais do usuário.
    """
    url = f"https://api.github.com/users/{username}"
    response = httpx.get(url, timeout=10)
 
    # Levanta exceção se a resposta for inválida
    response.raise_for_status()
 
    data = response.json()
    return {
        "login": data.get("login"),
        "name": data.get("name"),
        "public_repos": data.get("public_repos"),
        "followers": data.get("followers"),
        "following": data.get("following"),
        "url": data.get("html_url"),
    }

def get_ip():
    """Retorna o IP público usando a API ipify"""
    url = "https://api.ipify.org?format=json"
    resp = httpx.get(url, timeout=5)
    return resp.json()["ip"]
 
if __name__ == "__main__":
    # Exemplo de uso: consultar o próprio usuário do GitHub
    user = get_github_user("octocat")
    print(f"Usuário encontrado: {user} | Seu IP público é: {get_ip()}")