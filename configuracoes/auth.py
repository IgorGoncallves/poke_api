import pandas as pd
import bcrypt
from configuracoes.conexao_db import get_connection


def autenticar_usuario(email, senha):
    conn = get_connection()
    query = "SELECT * FROM dw_auth.user WHERE email = %s;"
    df = pd.read_sql(query, conn, params=(email,))
    conn.close()

    if df.empty:
        return None

    usuario = df.iloc[0]
    senha_hash = usuario["senha_hash"]

    if bcrypt.checkpw(senha.encode("utf-8"), senha_hash.encode("utf-8")):
        return usuario
    else:
        return None
