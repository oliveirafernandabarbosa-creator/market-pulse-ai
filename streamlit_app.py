import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Market Pulse AI",
    page_icon="📡",
    layout="wide"
)

# Carregar base
df = pd.read_csv("dados_streaming_market_pulse.csv")

st.title("📡 Market Pulse AI")
st.subheader("Inteligência de Mercado potencializada por IA")

st.caption(
    "Radar experimental desenvolvido com dados sintéticos "
    "para identificação de movimentos competitivos."
)

st.success("🟢 Monitoramento ativo • 30.000 registros analisados")

# FILTROS
st.sidebar.header("🔎 Filtros")

player = st.sidebar.selectbox(
    "Player",
    ["Todos"] + sorted(df["Player"].unique().tolist())
)

regiao = st.sidebar.selectbox(
    "Região",
    ["Todas"] + sorted(df["Regiao"].unique().tolist())
)

periodo = st.sidebar.selectbox(
    "Período",
    ["Todos"] + sorted(df["Mes"].unique().tolist(), reverse=True)
)

dados = df.copy()

if player != "Todos":
    dados = dados[dados["Player"] == player]

if regiao != "Todas":
    dados = dados[dados["Regiao"] == regiao]

if periodo != "Todos":
    dados = dados[dados["Mes"] == periodo]

# KPIs
assinantes = dados["Assinantes"].sum()
churn = dados["Churn_Pct"].mean()
satisfacao = dados["Satisfacao"].mean()
players_monitorados = dados["Player"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Assinantes monitorados",
    f"{assinantes/1_000_000:.1f} M"
)

col2.metric(
    "Churn médio",
    f"{churn:.1f}%"
)

col3.metric(
    "Satisfação",
    f"{satisfacao:.1f}/10"
)

col4.metric(
    "Players monitorados",
    players_monitorados
)

st.divider()

# MARKET SHARE
st.subheader("📊 Market Share por Player")

share = (
    dados.groupby("Player")["Market_Share_Pct"]
    .mean()
    .sort_values(ascending=False)
)

st.bar_chart(share)

st.divider()

# DETECÇÃO AUTOMÁTICA
st.subheader("🚨 Radar de Movimentos")

dados_player = (
    df.groupby(["Mes", "Player"])["Market_Share_Pct"]
    .mean()
    .reset_index()
)

pivot = dados_player.pivot(
    index="Mes",
    columns="Player",
    values="Market_Share_Pct"
)

variacao = pivot.iloc[-1] - pivot.iloc[-2]
player_destaque = variacao.abs().idxmax()
movimento = variacao[player_destaque]

if movimento > 0:
    st.warning(
        f"🔎 Movimento detectado: {player_destaque} ganhou "
        f"{movimento:.1f} p.p. de participação no último período."
    )
else:
    st.warning(
        f"🔎 Movimento detectado: {player_destaque} perdeu "
        f"{abs(movimento):.1f} p.p. de participação no último período."
    )

if st.button("✨ Investigar movimento"):
    detalhe = df[df["Player"] == player_destaque]

    st.info(
        f"""
        Investigação automática iniciada.

        **Player:** {player_destaque}

        Churn médio: {detalhe['Churn_Pct'].mean():.1f}%

        Satisfação média: {detalhe['Satisfacao'].mean():.1f}/10

        Novos assinantes analisados: {detalhe['Novos_Assinantes'].sum():,.0f}
        """
    )
