{{ config(materialized='incremental', unique_key=['id_pokemon','id_tipo']) }}

WITH expande_tipos AS (
    SELECT
        CAST(id AS INT) AS id_pokemon,
        TRIM(
            UNNEST(
                STRING_TO_ARRAY(
                    REGEXP_REPLACE(types, ',', '/'),
                    '/'
                )
            )
        ) AS nome_tipo,
        GENERATE_SERIES(1, array_length(STRING_TO_ARRAY(REGEXP_REPLACE(types, ',', '/'), '/'), 1)) AS tipo_ordem
    FROM {{ ref('stg_pokemon') }}
)

SELECT
    e.id_pokemon,
    t.id_tipo,
    CAST(e.tipo_ordem AS SMALLINT) AS tipo_ordem
FROM expande_tipos e
JOIN {{ ref('dim_tipo') }} t
    ON e.nome_tipo = t.nome_tipo
