import httpx

def get_ip():
    """Retorna o IP público usando a API ipify"""
    url = "https://api.ipify.org?format=json"
    resp = httpx.get(url, timeout=5)
    return resp.json()["ip"]

if __name__ == "__main__":
    print(f"Seu IP público é: {get_ip()}")
