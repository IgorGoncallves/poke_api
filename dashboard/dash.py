import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import plotly.express as px
from configuracoes.conexao_db import get_connection
from configuracoes.auth import autenticar_usuario
from pathlib import Path
import base64


st.set_page_config(page_title="Dashboard", layout="wide", page_icon="https://img.pokemondb.net/sprites/items/master-ball.png")

background_path = Path(__file__).parent / "imgs" / "bg.jpg"
with open(background_path, "rb") as img_file:
    encoded = base64.b64encode(img_file.read()).decode()

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


css_path = os.path.join(os.path.dirname(__file__), "styles", "style.css")
load_css(css_path)

if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False
    st.session_state["usuario"] = None

if not st.session_state["autenticado"]:
    st.markdown(
        f"""
        <style>
            [data-testid="stAppViewContainer"] {{
                background-image: 
                    linear-gradient(rgba(255,255,255,1), rgba(255,255,255,0.7)), /* camada branca transparente */
                    url("data:image/jpg;base64,{encoded}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}

            [data-testid="stHeader"] {{
                background: rgba(0, 0, 0, 0);
            }}

            [data-testid="stSidebar"] {{
                background-color: rgba(30, 41, 59, 0.9);
            }}
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <style>
            /* Remove o botão de fullscreen da imagem */
            [data-testid="stElementToolbar"] {
                display: none !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )


    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image("imgs/logo_pokemon.png", width=500)

    st.title(" Login")
    st.markdown("Entre com suas credenciais para acessar o dashboard.")

    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        usuario = autenticar_usuario(email, senha)
        if usuario is not None:
            st.session_state["autenticado"] = True
            st.session_state["usuario"] = usuario
            st.success(f"Bem-vindo(a), {usuario['nome_usuario']}!")
            st.rerun()
        else:
            st.error("E-mail ou senha incorretos.")
    st.stop() 

else:
    usuario = st.session_state["usuario"]
    st.sidebar.markdown(
        f" **Usuário:** {usuario['nome_usuario']}  \n"
        f" **Prioridade:** {usuario['prioridades'].capitalize()}",
        unsafe_allow_html=True
    )
    prioridade = usuario["prioridades"].lower()

    @st.cache_data
    def carregar_dados():
        conn = get_connection()

        query_dashboard = "SELECT * FROM dw.vw_geral;"
        query_media = "SELECT * FROM dw.vw_media_atributos_tipo;"
        query_tipos = "SELECT * FROM dw.vw_distribuicao_tipos;"

        df_dash = pd.read_sql(query_dashboard, conn)
        df_media = pd.read_sql(query_media, conn)
        df_tipos = pd.read_sql(query_tipos, conn)

        conn.close()
        return df_dash, df_media, df_tipos


    df_dash, df_media, df_tipos = carregar_dados()

    st.markdown("""
        <h1 style='text-align: center; color: #00a5ac; margin-bottom: 0;'>
             Dashboard Pokémon
        </h1>
        <h4 style='text-align: center; color: #707070; margin-top: 5px;'>
            Análises e Estatísticas dos Pokémons
        </h4>
        <hr style='margin-top: 10px; margin-bottom: 30px;'>
    """, unsafe_allow_html=True)

    

    col1, col2, col3, col4 = st.columns(4) 
    col1.metric("Pokémons Cadastrados", df_dash.shape[0])
    col2.metric("Tipos Existentes", df_tipos.shape[0])
    col3.metric("Com Vitórias", (df_dash["vitorias"] > 0).sum())
    col4.metric("Total de Vitórias", int(df_dash["vitorias"].sum()))


    if prioridade == "platinum":
        tab1, tab2, tab3, tab4 = st.tabs(["Top 10 Pokémons Vitoriosos", "Distribuição por Tipo", "Atributos Médios por Tipo","Detalhes do Pokémon"])

        with tab1:

            top_vitorias = df_dash.sort_values(by="vitorias", ascending=False).head(10)

            fig_ranking = px.bar(
                top_vitorias,
                x="nome",
                y="vitorias",
                color="nome_tipo",
                text="vitorias",
                color_discrete_sequence=px.colors.qualitative.Vivid,
                labels={"nome": "Pokémon", "vitorias": "Vitórias", "nome_tipo": "Tipo"}
            )

            fig_ranking.update_traces(
                texttemplate="<b>%{text}</b>",
                textposition="outside",
                marker_line_color="#ffffff",
                marker_line_width=1.2,
                opacity=0.9
            )

            fig_ranking.update_xaxes(categoryorder="total descending")

            fig_ranking.update_layout(
                xaxis=dict(
                    title="Pokémon",
                    tickfont=dict(size=12, color="#707070"),
                    showgrid=False
                ),
                yaxis=dict(
                    title="Vitórias",
                    tickfont=dict(size=12, color="#707070"),
                    gridcolor="rgba(0,0,0,0.05)"
                ),
                plot_bgcolor="#ffffff",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=40, r=40, t=0, b=60),
                showlegend=True,
                legend=dict(
                    title="Tipo",
                    orientation="h",
                    yanchor="bottom",
                    y=-0.3,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=12, color="#707070")
                )
            )

            st.plotly_chart(fig_ranking, use_container_width=True)


        with tab2:

            fig_tipos = px.pie(
                df_tipos,
                values="quantidade",
                names="nome_tipo",
                hole=0.35, 
                color_discrete_sequence=px.colors.qualitative.Vivid
            )

            fig_tipos.update_traces(
                textinfo="label+percent",
                textfont=dict(size=13, color="#333"),
                hovertemplate="<b>%{label}</b><br>Pokémons: %{value}<br>Percentual: %{percent}<extra></extra>",
                pull=[0.05 if i == df_tipos["quantidade"].idxmax() else 0 for i in range(len(df_tipos))],  
            )

            fig_tipos.update_layout(
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.35,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=12, color="#707070")
                ),
                margin=dict(t=0, b=100, l=20, r=20),
                paper_bgcolor="rgba(0,0,0,0)",
            )

            st.plotly_chart(fig_tipos, use_container_width=True)


        with tab3:

            df_attr_melt = df_media.melt(
                id_vars="nome_tipo",
                var_name="Atributo",
                value_name="Média"
            )

            df_attr_melt["Atributo"] = df_attr_melt["Atributo"].str.replace("_", " ").str.title()

            fig_attr = px.bar(
                df_attr_melt,
                x="nome_tipo",
                y="Média",
                color="Atributo",
                barmode="group",
                color_discrete_sequence=px.colors.qualitative.Vivid,
                labels={"nome_tipo": "Tipo", "Média": "Média dos Atributos"},
                height=400
            )

            fig_attr.update_traces(
                marker_line_color="#ffffff",
                marker_line_width=1.2,
                opacity=0.9
            )

            fig_attr.update_layout(
                xaxis=dict(
                    title="Tipo de Pokémon",
                    tickfont=dict(size=13, color="#505050"),
                    showgrid=False
                ),
                yaxis=dict(
                    title="Média dos Atributos",
                    tickfont=dict(size=13, color="#505050"),
                    gridcolor="rgba(0,0,0,0.05)"
                ),
                bargap=0.25,          
                bargroupgap=0.1,      
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                legend=dict(
                    title="Atributos",
                    orientation="h",        
                    yanchor="top",
                    y=-0.25,                
                    xanchor="center",
                    x=0.5,
                    font=dict(size=12, color="#333")
                ),
                margin=dict(t=0, b=100, l=60, r=40)
            )

            st.plotly_chart(fig_attr, use_container_width=True)

        with tab4:
            df_ordenado = df_dash.sort_values(by="id_pokemon")

            pokemon_escolhido = st.selectbox(
                "Selecione um Pokémon",
                df_ordenado["nome"].tolist()
            )

            poke = df_ordenado[df_ordenado["nome"] == pokemon_escolhido].iloc[0]

            col_img, col_info = st.columns([1, 2])

            with col_img:
                st.markdown(
                    f"""
                    <div style="
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100%;
                        background-color: rgba(255,255,255,0.9);
                        border-radius: 15px;
                        padding: 20px;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                    ">
                        <img src="{poke['sprite_url']}" width="340" style="max-width:100%;">
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col_info:
                st.markdown(
                    f"""
                    <div style="
                        background-color: rgba(255,255,255,0.95);
                        border-radius: 15px;
                        padding: 25px;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                    ">
                        <h2 style="color:#00a5ac; margin-bottom: 5px;">{poke['nome']}</h2>
                        <p style="color:#555; font-size:16px; margin-top: 0;">
                            Geração {poke['geracao']} • { '⭐ Lendário' if poke['lendario'] else 'Comum' }
                        </p>
                        <p style="font-size:15px; color:#333;">
                            <b>Tipos:</b> {poke['nome_tipo']}<br>
                            <b>Vitórias:</b> {int(poke['vitorias'])}
                        </p>
                        <p style="
                            font-size:15px;
                            color:#333;
                            line-height:1.6;
                            margin: 0;
                        ">
                            <b>HP:</b> {poke['hp']}<br>
                            <b>Ataque:</b> {poke['ataque']}<br>
                            <b>Defesa:</b> {poke['defesa']}<br>
                            <b>Atq. Especial:</b> {poke['ataque_especial']}<br>
                            <b>Def. Especial:</b> {poke['defesa_especial']}<br>
                            <b>Velocidade:</b> {poke['velocidade']}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    elif prioridade == "bronze":
        tab1, tab2, tab3 = st.tabs(["Top 10 Pokémons Vitoriosos", "Distribuição por Tipo","Detalhes do Pokémon"])

        with tab1:

            top_vitorias = df_dash.sort_values(by="vitorias", ascending=False).head(10)

            fig_ranking = px.bar(
                top_vitorias,
                x="nome",
                y="vitorias",
                color="nome_tipo",
                text="vitorias",
                color_discrete_sequence=px.colors.qualitative.Vivid,
                labels={"nome": "Pokémon", "vitorias": "Vitórias", "nome_tipo": "Tipo"}
            )

            fig_ranking.update_traces(
                texttemplate="<b>%{text}</b>",
                textposition="outside",
                marker_line_color="#ffffff",
                marker_line_width=1.2,
                opacity=0.9
            )

            fig_ranking.update_xaxes(categoryorder="total descending")

            fig_ranking.update_layout(
                xaxis=dict(
                    title="Pokémon",
                    tickfont=dict(size=12, color="#707070"),
                    showgrid=False
                ),
                yaxis=dict(
                    title="Vitórias",
                    tickfont=dict(size=12, color="#707070"),
                    gridcolor="rgba(0,0,0,0.05)"
                ),
                plot_bgcolor="#ffffff",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=40, r=40, t=0, b=60),
                showlegend=True,
                legend=dict(
                    title="Tipo",
                    orientation="h",
                    yanchor="bottom",
                    y=-0.3,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=12, color="#707070")
                )
            )

            st.plotly_chart(fig_ranking, use_container_width=True)


        with tab2:

            fig_tipos = px.pie(
                df_tipos,
                values="quantidade",
                names="nome_tipo",
                hole=0.35, 
                color_discrete_sequence=px.colors.qualitative.Vivid
            )

            fig_tipos.update_traces(
                textinfo="label+percent",
                textfont=dict(size=13, color="#333"),
                hovertemplate="<b>%{label}</b><br>Pokémons: %{value}<br>Percentual: %{percent}<extra></extra>",
                pull=[0.05 if i == df_tipos["quantidade"].idxmax() else 0 for i in range(len(df_tipos))],  
            )

            fig_tipos.update_layout(
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.35,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=12, color="#707070")
                ),
                margin=dict(t=0, b=100, l=20, r=20),
                paper_bgcolor="rgba(0,0,0,0)",
            )

            st.plotly_chart(fig_tipos, use_container_width=True)

        with tab3:
            df_ordenado = df_dash.sort_values(by="id_pokemon")

            pokemon_escolhido = st.selectbox(
                "Selecione um Pokémon",
                df_ordenado["nome"].tolist()
            )

            poke = df_ordenado[df_ordenado["nome"] == pokemon_escolhido].iloc[0]

            col_img, col_info = st.columns([1, 2])

            with col_img:
                st.markdown(
                    f"""
                    <div style="
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100%;
                        background-color: rgba(255,255,255,0.9);
                        border-radius: 15px;
                        padding: 20px;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                    ">
                        <img src="{poke['sprite_url']}" width="340" style="max-width:100%;">
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col_info:
                st.markdown(
                    f"""
                    <div style="
                        background-color: rgba(255,255,255,0.95);
                        border-radius: 15px;
                        padding: 25px;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                    ">
                        <h2 style="color:#00a5ac; margin-bottom: 5px;">{poke['nome']}</h2>
                        <p style="color:#555; font-size:16px; margin-top: 0;">
                            Geração {poke['geracao']} • { '⭐ Lendário' if poke['lendario'] else 'Comum' }
                        </p>
                        <p style="font-size:15px; color:#333;">
                            <b>Tipos:</b> {poke['nome_tipo']}<br>
                            <b>Vitórias:</b> {int(poke['vitorias'])}
                        </p>
                        <p style="
                            font-size:15px;
                            color:#333;
                            line-height:1.6;
                            margin: 0;
                        ">
                            <b>HP:</b> {poke['hp']}<br>
                            <b>Ataque:</b> {poke['ataque']}<br>
                            <b>Defesa:</b> {poke['defesa']}<br>
                            <b>Atq. Especial:</b> {poke['ataque_especial']}<br>
                            <b>Def. Especial:</b> {poke['defesa_especial']}<br>
                            <b>Velocidade:</b> {poke['velocidade']}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.warning("Prioridade desconhecida. Contate o administrador.")

    if st.sidebar.button("Sair"):
        st.session_state["autenticado"] = False
        st.session_state["usuario"] = None
        st.rerun()
