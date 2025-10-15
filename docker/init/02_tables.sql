--CAMADA STAGE 

CREATE TABLE IF NOT EXISTS stage.stg_pokemon (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    hp INT,
    attack INT,
    defense INT,
    sp_attack INT,
    sp_defense INT,
    speed INT,
    generation VARCHAR(10),
    legendary VARCHAR(10),
    types VARCHAR(255)  
);

CREATE TABLE IF NOT EXISTS stage.stg_batalha (
    first_pokemon INT,
    second_pokemon INT,
    winner INT
);


--CAMADA DW (Snowflake)

--Dimensão de Tipos
CREATE TABLE IF NOT EXISTS dw.dim_tipo (
    id_tipo SERIAL PRIMARY KEY,
    nome_tipo VARCHAR(50) UNIQUE NOT NULL
);

--Dimensão de Pokemons 
CREATE TABLE IF NOT EXISTS dw.dim_pokemon (
    id_pokemon INT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    hp INT,
    ataque INT,
    defesa INT,
    ataque_especial INT,
    defesa_especial INT,
    velocidade INT,
    geracao INT,
    lendario BOOLEAN DEFAULT FALSE
);

--Bridge Pokémon > Tipo
CREATE TABLE IF NOT EXISTS dw.bridge_pokemon_tipo (
    id_pokemon INT NOT NULL,
    id_tipo INT NOT NULL,
    tipo_ordem SMALLINT,
    PRIMARY KEY (id_pokemon, id_tipo),
    FOREIGN KEY (id_pokemon) REFERENCES dw.dim_pokemon(id_pokemon),
    FOREIGN KEY (id_tipo) REFERENCES dw.dim_tipo(id_tipo)
);

--Fato batalhas 
CREATE TABLE IF NOT EXISTS dw.fato_batalha (
    id_batalha SERIAL PRIMARY KEY,
    id_pokemon_1 INT REFERENCES dw.dim_pokemon(id_pokemon),
    id_pokemon_2 INT REFERENCES dw.dim_pokemon(id_pokemon),
    id_vencedor INT REFERENCES dw.dim_pokemon(id_pokemon)
);
