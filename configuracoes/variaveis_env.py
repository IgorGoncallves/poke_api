from dotenv import load_dotenv
import os
from pathlib import Path

env = Path(__file__).resolve().parent / ".env"

load_dotenv(dotenv_path=env)

api_url = os.getenv("api_url")
api_usuario = os.getenv("api_usuario") 
api_senha = os.getenv("api_senha")


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")