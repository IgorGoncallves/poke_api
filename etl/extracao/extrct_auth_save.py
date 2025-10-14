import requests
from configuracoes.variaveis_env import api_url,api_usuario,api_senha
from pathlib import Path
import json

def get_token():
    payload = {"username": api_usuario, "password": api_senha}
    res = requests.post(f"{api_url}/login", json=payload)
    res.raise_for_status()
    token = res.json()["access_token"]
    print("Token JWT obtido com sucesso.")
    return token

def auth_header(token):
    return {"Authorization": f"Bearer {token}"}

def save_raw(data, filename):
    path = Path("data/raw")
    path.mkdir(parents=True, exist_ok=True)
    with open(path / f"{filename}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Arquivo salvo em data/raw/{filename}.json")
