{{ config(materialized='view') }}

SELECT
    id,
    name,
    hp,
    attack,
    defense,
    sp_attack,
    sp_defense,
    speed,
    generation,
    legendary,
    types,
    sprite_url
FROM stage.stg_pokemon
