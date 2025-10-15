{{ config(
    materialized='table',
    alias='vw_distribuicao_tipos'
) }}

select
    t.nome_tipo,
    count(distinct b.id_pokemon) as quantidade
from {{ ref('bridge_pokemon_tipo') }} b
join {{ ref('dim_tipo') }} t on b.id_tipo = t.id_tipo
group by t.nome_tipo
order by quantidade desc
