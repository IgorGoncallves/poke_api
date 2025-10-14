import psycopg2
from configuracoes.variaveis_env import DB_HOST,DB_NAME,DB_PASSWORD,DB_PORT,DB_USER

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
