{{ config(
    materialized='table',
    schema='auth'
) }}

SELECT *
FROM (
    VALUES
        (1, 'Kaizen Platinum','kaizenplatinum@teste.com', '12345678900', '$2b$12$6JCcHh6G8TjsqVZFqRf3heFjOuBak2Tb6v31AeldW1entfF3X8uc6', 'platinum'),
        (2, 'Kaizen Bronze','kaizenbronze@teste.com', '98765432100', '$2b$12$6JCcHh6G8TjsqVZFqRf3heFjOuBak2Tb6v31AeldW1entfF3X8uc6', 'bronze')
) AS t(id_usuario, nome_usuario,email, cpf, senha_hash, prioridades)
