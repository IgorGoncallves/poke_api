{{ config(materialized='incremental', unique_key='nome_tipo') }}

WITH tipos_expandidos AS (
    SELECT
        TRIM(
            UNNEST(
                STRING_TO_ARRAY(
                    REGEXP_REPLACE(types, ',', '/'), 
                    '/'
                )
            )
        ) AS nome_tipo
    FROM {{ ref('stg_pokemon') }}
),
tipos_unicos AS (
    SELECT DISTINCT
        CAST(nome_tipo AS VARCHAR(50)) AS nome_tipo
    FROM tipos_expandidos
    WHERE nome_tipo IS NOT NULL
      AND nome_tipo <> ''
)


SELECT
    ROW_NUMBER() OVER (ORDER BY nome_tipo) AS id_tipo,
    nome_tipo
FROM tipos_unicos
