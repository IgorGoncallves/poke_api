{{ config(materialized='view') }}

SELECT
    first_pokemon,
    second_pokemon,
    winner
FROM stage.stg_batalha
