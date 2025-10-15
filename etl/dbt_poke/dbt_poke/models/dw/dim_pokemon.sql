{{ config(materialized='incremental', unique_key='id_pokemon') }}

SELECT
    CAST(id AS INT) AS id_pokemon,
    CAST(name AS VARCHAR(255)) AS nome,
    CAST(hp AS INT) AS hp,
    CAST(attack AS INT) AS ataque,
    CAST(defense AS INT) AS defesa,
    CAST(sp_attack AS INT) AS ataque_especial,
    CAST(sp_defense AS INT) AS defesa_especial,
    CAST(speed AS INT) AS velocidade,

    --trata os 2 casos que vem Gen2 deixando tudo como inteiro
    CAST(
        CASE
            WHEN generation ~ '^[0-9]+$' THEN generation
            WHEN LOWER(generation) LIKE 'gen%' THEN REGEXP_REPLACE(generation, '[^0-9]', '', 'g')
            ELSE NULL
        END
    AS INT) AS geracao,

    CASE
        WHEN LOWER(legendary) IN ('true', '1', 'yes', 't') THEN TRUE
        ELSE FALSE
    END AS lendario

FROM {{ ref('stg_pokemon') }}
