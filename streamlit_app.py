import streamlit as st

st.set_page_config(
    page_title="Market Pulse AI",
    page_icon="📡",
    layout="wide"
)

st.title("📡 Market Pulse AI")
st.subheader("Inteligência de Mercado potencializada por IA")

st.write(
    "Monitoramento inteligente para detectar movimentos, "
    "anomalias e oportunidades de mercado."
)

st.success("🟢 Monitoramento de mercado ativo")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Movimentos detectados", "3")

with col2:
    st.metric("Players monitorados", "4")

with col3:
    st.metric("Alertas críticos", "1")

st.divider()

st.subheader("🚨 Movimento relevante detectado")

st.warning(
    "Flixora apresentou crescimento de +4,1 p.p. "
    "de participação no último período."
)

if st.button("✨ Investigar com IA"):
    st.info(
        "Analisando automaticamente churn, audiência, "
        "perfil de consumo e comportamento competitivo..."
    )
