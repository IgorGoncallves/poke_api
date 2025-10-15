{{ config(
    materialized='table',
    alias='vw_geral'
) }}

with base as (
    select
        p.id_pokemon,
        p.nome,
        p.hp,
        p.ataque,
        p.defesa,
        p.ataque_especial,
        p.defesa_especial,
        p.velocidade,
        p.geracao,
        p.lendario,
        p.sprite_url
    from {{ ref('dim_pokemon') }} p
),


tipos as (
    select
        b.id_pokemon,
        string_agg(t.nome_tipo, '/' order by b.tipo_ordem) as nome_tipo
    from {{ ref('bridge_pokemon_tipo') }} b
    join {{ ref('dim_tipo') }} t on b.id_tipo = t.id_tipo
    group by b.id_pokemon
),

vitorias as (
    select
        f.id_vencedor as id_pokemon,
        count(*) as vitorias
    from {{ ref('fato_batalha') }} f
    where f.id_vencedor is not null
    group by f.id_vencedor
),

final as (
    select
        b.*,
        coalesce(t.nome_tipo, 'Desconhecido') as nome_tipo,
        coalesce(v.vitorias, 0) as vitorias
    from base b
    left join tipos t on b.id_pokemon = t.id_pokemon
    left join vitorias v on b.id_pokemon = v.id_pokemon
)

select * from final
