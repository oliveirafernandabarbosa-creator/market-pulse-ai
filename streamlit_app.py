import streamlit as st
import pandas as pd

# =========================================================
# CONFIGURAÇÃO
# =========================================================

st.set_page_config(
    page_title="Market Pulse AI",
    page_icon="📡",
    layout="wide"
)

# =========================================================
# CARREGAR BASE
# =========================================================

@st.cache_data
def carregar_dados():
    df = pd.read_csv(
        "dados_streaming_market_pulse_novos_players (3).csv"
    )

    df["Mes"] = pd.to_datetime(df["Mes"])

    return df


df = carregar_dados()


# =========================================================
# CABEÇALHO
# =========================================================

st.title("📡 Market Pulse AI")

st.subheader(
    "Inteligência de Mercado potencializada por IA"
)

st.caption(
    "Radar experimental desenvolvido com dados sintéticos "
    "para monitoramento competitivo e identificação de "
    "movimentos de mercado."
)

st.success(
    f"🟢 Radar ativo • {len(df):,.0f} registros analisados"
)


# =========================================================
# FILTROS
# =========================================================

st.sidebar.title("🔎 Filtros de mercado")

players = sorted(df["Player"].dropna().unique())
regioes = sorted(df["Regiao"].dropna().unique())
planos = sorted(df["Plano"].dropna().unique())
faixas = sorted(df["Faixa_Etaria"].dropna().unique())

player = st.sidebar.selectbox(
    "Player",
    ["Todos"] + players
)

regiao = st.sidebar.selectbox(
    "Região",
    ["Todas"] + regioes
)

plano = st.sidebar.selectbox(
    "Plano",
    ["Todos"] + planos
)

faixa = st.sidebar.selectbox(
    "Faixa etária",
    ["Todas"] + faixas
)


# =========================================================
# APLICAR FILTROS
# =========================================================

dados = df.copy()

if player != "Todos":
    dados = dados[dados["Player"] == player]

if regiao != "Todas":
    dados = dados[dados["Regiao"] == regiao]

if plano != "Todos":
    dados = dados[dados["Plano"] == plano]

if faixa != "Todas":
    dados = dados[dados["Faixa_Etaria"] == faixa]


# =========================================================
# CARDS DOS PLAYERS
# =========================================================

st.divider()

st.subheader("🎬 Players monitorados")

p1, p2, p3, p4 = st.columns(4)

with p1:
    st.info("🔴 **NETLEX**\n\nStreaming Entertainment")

with p2:
    st.info("🔵 **PRIMEFLIX**\n\nStreaming & Benefits")

with p3:
    st.info("🟣 **DISNEYA+**\n\nEntertainment & Family")

with p4:
    st.info("⚫ **MAXY**\n\nPremium Entertainment")


# =========================================================
# KPIs
# =========================================================

st.divider()

st.subheader("📊 Visão Executiva")

assinantes = dados["Assinantes"].sum()
novos = dados["Novos_Assinantes"].sum()
cancelamentos = dados["Cancelamentos"].sum()

churn = dados["Churn_Pct"].mean()
nps = dados["NPS"].mean()
satisfacao = dados["Satisfacao"].mean()

receita = dados["Receita_Estimada"].sum()

market_share = (
    dados.groupby("Player")["Market_Share_Pct"]
    .mean()
    .mean()
)

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "👥 Assinantes",
    f"{assinantes / 1_000_000:.1f} M"
)

k2.metric(
    "💰 Receita estimada",
    f"R$ {receita / 1_000_000:.1f} M"
)

k3.metric(
    "📉 Churn médio",
    f"{churn:.1f}%"
)

k4.metric(
    "❤️ NPS médio",
    f"{nps:.0f}"
)

k5, k6, k7, k8 = st.columns(4)

k5.metric(
    "🚀 Novos assinantes",
    f"{novos / 1_000_000:.1f} M"
)

k6.metric(
    "🚪 Cancelamentos",
    f"{cancelamentos / 1_000_000:.1f} M"
)

k7.metric(
    "⭐ Satisfação",
    f"{satisfacao:.1f}/10"
)

k8.metric(
    "🎯 Share médio",
    f"{market_share:.1f}%"
)


# =========================================================
# MARKET SHARE
# =========================================================

st.divider()

st.subheader("🏆 Posicionamento competitivo")

share = (
    dados.groupby("Player")["Market_Share_Pct"]
    .mean()
    .sort_values(ascending=False)
)

st.bar_chart(
    share,
    height=380
)


# =========================================================
# EVOLUÇÃO DO MARKET SHARE
# =========================================================

st.subheader("📈 Evolução do Market Share")

share_tempo = (
    dados.groupby(["Mes", "Player"])["Market_Share_Pct"]
    .mean()
    .reset_index()
)

share_pivot = share_tempo.pivot(
    index="Mes",
    columns="Player",
    values="Market_Share_Pct"
)

st.line_chart(
    share_pivot,
    height=400
)


# =========================================================
# CHURN
# =========================================================

st.divider()

col_graf1, col_graf2 = st.columns(2)

with col_graf1:

    st.subheader("📉 Churn por Player")

    churn_player = (
        dados.groupby("Player")["Churn_Pct"]
        .mean()
        .sort_values(ascending=False)
    )

    st.bar_chart(
        churn_player,
        height=350
    )


# =========================================================
# SATISFAÇÃO
# =========================================================

with col_graf2:

    st.subheader("⭐ Satisfação por Player")

    satisfacao_player = (
        dados.groupby("Player")["Satisfacao"]
        .mean()
        .sort_values(ascending=False)
    )

    st.bar_chart(
        satisfacao_player,
        height=350
    )


# =========================================================
# AQUISIÇÃO X CANCELAMENTO
# =========================================================

st.divider()

st.subheader("👥 Aquisição x Cancelamentos")

movimentacao = (
    dados.groupby("Player")[
        ["Novos_Assinantes", "Cancelamentos"]
    ]
    .sum()
)

st.bar_chart(
    movimentacao,
    height=400
)


# =========================================================
# RECEITA
# =========================================================

st.subheader("💰 Receita estimada por Player")

receita_player = (
    dados.groupby("Player")["Receita_Estimada"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(
    receita_player,
    height=380
)


# =========================================================
# ANÁLISE REGIONAL
# =========================================================

st.divider()

st.subheader("🗺️ Distribuição regional")

regional = (
    dados.groupby("Regiao")["Assinantes"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(
    regional,
    height=350
)


# =========================================================
# PERFIL DE CONSUMO
# =========================================================

c1, c2 = st.columns(2)

with c1:

    st.subheader("👤 Faixa etária")

    idade = (
        dados.groupby("Faixa_Etaria")["Assinantes"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(
        idade,
        height=320
    )


with c2:

    st.subheader("🎬 Preferência de conteúdo")

    genero = (
        dados.groupby("Genero_Preferido")["Assinantes"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(
        genero,
        height=320
    )


# =========================================================
# RADAR AUTOMÁTICO
# =========================================================

st.divider()

st.header("🧠 Market Pulse — Radar Inteligente")

st.caption(
    "O motor analítico compara períodos e procura alterações "
    "relevantes nos indicadores competitivos."
)

radar = (
    df.groupby(["Mes", "Player"])
    .agg(
        Market_Share=("Market_Share_Pct", "mean"),
        Churn=("Churn_Pct", "mean"),
        Satisfacao=("Satisfacao", "mean"),
        Novos=("Novos_Assinantes", "sum")
    )
    .reset_index()
)

meses = sorted(radar["Mes"].unique())

ultimo_mes = meses[-1]
mes_anterior = meses[-2]

atual = radar[
    radar["Mes"] == ultimo_mes
].set_index("Player")

anterior = radar[
    radar["Mes"] == mes_anterior
].set_index("Player")

comparacao = atual.join(
    anterior,
    lsuffix="_atual",
    rsuffix="_anterior"
)

comparacao["Variacao_Share"] = (
    comparacao["Market_Share_atual"]
    - comparacao["Market_Share_anterior"]
)

comparacao["Variacao_Churn"] = (
    comparacao["Churn_atual"]
    - comparacao["Churn_anterior"]
)

comparacao["Variacao_Novos"] = (
    (
        comparacao["Novos_atual"]
        / comparacao["Novos_anterior"]
    ) - 1
) * 100


# =========================================================
# MAIOR MOVIMENTO
# =========================================================

player_movimento = (
    comparacao["Variacao_Share"]
    .abs()
    .idxmax()
)

movimento = comparacao.loc[player_movimento]

variacao_share = movimento["Variacao_Share"]


if abs(variacao_share) >= 1:

    if variacao_share > 0:

        st.warning(
            f"🚨 Movimento competitivo detectado: "
            f"**{player_movimento} ganhou "
            f"{variacao_share:.1f} p.p. de Market Share.**"
        )

    else:

        st.warning(
            f"🚨 Movimento competitivo detectado: "
            f"**{player_movimento} perdeu "
            f"{abs(variacao_share):.1f} p.p. de Market Share.**"
        )

else:

    st.success(
        "🟢 Nenhuma alteração crítica de Market Share "
        "foi identificada no último período."
    )


# =========================================================
# INVESTIGAÇÃO AUTOMÁTICA
# =========================================================

if st.button("✨ Investigar movimento"):

    st.subheader("🔬 Diagnóstico automático")

    churn_var = movimento["Variacao_Churn"]
    novos_var = movimento["Variacao_Novos"]

    d1, d2, d3 = st.columns(3)

    d1.metric(
        "Variação Market Share",
        f"{variacao_share:+.1f} p.p."
    )

    d2.metric(
        "Variação Churn",
        f"{churn_var:+.1f} p.p."
    )

    d3.metric(
        "Novos assinantes",
        f"{novos_var:+.1f}%"
    )


    # =====================================================
    # INVESTIGAÇÃO POR SEGMENTO
    # =====================================================

    detalhe_player = df[
        df["Player"] == player_movimento
    ]

    segmento = (
        detalhe_player[
            detalhe_player["Mes"] == ultimo_mes
        ]
        .groupby(
            ["Regiao", "Faixa_Etaria"]
        )
        .agg(
            Assinantes=("Assinantes", "sum"),
            Share=("Market_Share_Pct", "mean"),
            Churn=("Churn_Pct", "mean")
        )
        .reset_index()
        .sort_values(
            "Assinantes",
            ascending=False
        )
    )

    principal_segmento = segmento.iloc[0]

    st.info(
        f"""
        **🔎 Segmento de maior concentração**

        Região: **{principal_segmento['Regiao']}**

        Faixa etária: **{principal_segmento['Faixa_Etaria']}**

        Assinantes analisados:
        **{principal_segmento['Assinantes']:,.0f}**

        Churn médio:
        **{principal_segmento['Churn']:.1f}%**
        """
    )


    # =====================================================
    # INTERPRETAÇÃO
    # =====================================================

    st.subheader("🧠 Hipótese para investigação")

    if variacao_share > 0 and novos_var > 0:

        st.write(
            f"""
            O movimento de **{player_movimento}** apresenta
            sinais de expansão da base.

            O crescimento simultâneo de Market Share e
            aquisição de novos assinantes indica que o ganho
            pode estar relacionado a uma maior capacidade
            de aquisição no período.

            O próximo passo recomendado pelo radar é analisar
            quais regiões, planos e perfis de consumidores
            concentram esse crescimento.
            """
        )

    elif variacao_share < 0 and churn_var > 0:

        st.write(
            f"""
            O movimento de **{player_movimento}** apresenta
            sinais de pressão competitiva.

            A redução de Market Share acompanhada pelo aumento
            do churn sugere possível perda de assinantes.

            O radar recomenda aprofundar a análise por região,
            faixa etária e plano para identificar onde a
            retração está concentrada.
            """
        )

    else:

        st.write(
            """
            O movimento identificado não apresenta uma causa
            única evidente nos principais indicadores.

            Recomenda-se aprofundar a investigação por
            segmentos antes de estabelecer uma hipótese
            conclusiva.
            """
        )


# =========================================================
# METODOLOGIA
# =========================================================

st.divider()

with st.expander("ℹ️ Sobre o projeto"):

    st.write(
        """
        **Market Pulse AI** é um projeto experimental de
        Inteligência de Mercado desenvolvido para demonstrar
        como automação analítica e Inteligência Artificial
        podem apoiar o monitoramento competitivo.

        A base utilizada contém dados 100% sintéticos.

        Os players apresentados são fictícios e foram criados
        exclusivamente para fins educacionais e demonstrativos.

        Nenhuma informação apresentada representa dados reais
        de empresas do mercado de streaming.
        """
    )

    st.caption(
        "Projeto desenvolvido por Fernanda Barbosa • "
        "Inteligência de Mercado & Analytics"
    )
