{{ config(
    materialized='table',
    alias='vw_media_atributos_tipo'
) }}


with bridge as (
    select
        b.id_pokemon,
        t.nome_tipo
    from {{ ref('bridge_pokemon_tipo') }} b
    join {{ ref('dim_tipo') }} t on b.id_tipo = t.id_tipo
),

joined as (
    select
        br.nome_tipo,
        p.ataque,
        p.defesa,
        p.ataque_especial,
        p.defesa_especial,
        p.velocidade
    from bridge br
    join {{ ref('dim_pokemon') }} p on br.id_pokemon = p.id_pokemon
),

media_atributos as (
    select
        nome_tipo,
        avg(ataque) as media_ataque,
        avg(defesa) as media_defesa,
        avg(ataque_especial) as media_ataque_especial,
        avg(defesa_especial) as media_defesa_especial,
        avg(velocidade) as media_velocidade
    from joined
    group by nome_tipo
)

select * from media_atributos
order by nome_tipo
