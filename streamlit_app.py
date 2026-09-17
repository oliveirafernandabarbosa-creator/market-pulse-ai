import streamlit as st
import pandas as pd
import altair as alt

# =========================================================
# CONFIGURAÇÃO
# =========================================================

st.set_page_config(
    page_title="Market Pulse AI",
    page_icon="🧠",
    layout="wide"
)

ARQUIVO = "dados_streaming_market_pulse_novos_players (3).csv"


# =========================================================
# CARREGAMENTO
# =========================================================

@st.cache_data
def carregar_dados():
    df = pd.read_csv(ARQUIVO)

    # Tenta reconhecer automaticamente colunas de data
    for coluna in df.columns:
        if "data" in coluna.lower() or "date" in coluna.lower():
            try:
                df[coluna] = pd.to_datetime(df[coluna])
            except:
                pass

    return df


try:
    df = carregar_dados()

except Exception as e:
    st.error("Não consegui carregar a base.")
    st.code(str(e))
    st.stop()


# =========================================================
# IDENTIFICAÇÃO DAS COLUNAS
# =========================================================

def encontrar_coluna(palavras):
    for coluna in df.columns:
        nome = coluna.lower().strip()

        if any(palavra in nome for palavra in palavras):
            return coluna

    return None


col_player = encontrar_coluna(
    ["player", "empresa", "plataforma", "marca"]
)

col_regiao = encontrar_coluna(
    ["regiao", "região", "region"]
)

col_periodo = encontrar_coluna(
    ["periodo", "período", "mes", "mês", "data", "date"]
)

col_assinantes = encontrar_coluna(
    ["assinantes", "assinatura", "clientes", "base"]
)

col_churn = encontrar_coluna(
    ["churn"]
)

col_satisfacao = encontrar_coluna(
    ["satisfacao", "satisfação", "csat"]
)

col_nps = encontrar_coluna(
    ["nps"]
)

col_share = encontrar_coluna(
    ["market_share", "market share", "share"]
)

col_crescimento = encontrar_coluna(
    ["crescimento", "growth"]
)


# =========================================================
# CABEÇALHO
# =========================================================

st.title("🧠 Market Pulse — Radar Inteligente")

st.subheader(
    "Inteligência de Mercado potencializada por IA"
)

st.caption(
    "Protótipo experimental desenvolvido com dados sintéticos "
    "para identificação de movimentos competitivos."
)

st.success(
    f"🟢 Monitoramento ativo • {len(df):,.0f} registros analisados"
)


# =========================================================
# FILTROS
# =========================================================

st.sidebar.header("🔎 Filtros")

df_filtrado = df.copy()


if col_player:

    players = sorted(
        df[col_player].dropna().astype(str).unique()
    )

    player = st.sidebar.selectbox(
        "Player",
        ["Todos"] + players
    )

    if player != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado[col_player].astype(str) == player
        ]


if col_regiao:

    regioes = sorted(
        df[col_regiao].dropna().astype(str).unique()
    )

    regiao = st.sidebar.selectbox(
        "Região",
        ["Todas"] + regioes
    )

    if regiao != "Todas":
        df_filtrado = df_filtrado[
            df_filtrado[col_regiao].astype(str) == regiao
        ]


if col_periodo:

    periodos = sorted(
        df[col_periodo]
        .dropna()
        .astype(str)
        .unique()
    )

    periodo = st.sidebar.selectbox(
        "Período",
        ["Todos"] + periodos
    )

    if periodo != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado[col_periodo].astype(str) == periodo
        ]


# =========================================================
# METAS DO PROTÓTIPO
# =========================================================

META_NPS = 70
META_SATISFACAO = 8.0
META_CHURN = 5.0
META_CRESCIMENTO = 5.0

st.sidebar.divider()

st.sidebar.subheader("🎯 Metas")

st.sidebar.caption("NPS ≥ 70")
st.sidebar.caption("Satisfação ≥ 8,0")
st.sidebar.caption("Churn ≤ 5%")
st.sidebar.caption("Crescimento ≥ 5%")

st.sidebar.caption(
    "Metas ilustrativas definidas exclusivamente para o protótipo."
)


# =========================================================
# FUNÇÕES
# =========================================================

def media(coluna, padrao=0):

    if coluna and coluna in df_filtrado.columns:

        valor = pd.to_numeric(
            df_filtrado[coluna],
            errors="coerce"
        ).mean()

        if pd.notna(valor):
            return valor

    return padrao


def soma(coluna, padrao=0):

    if coluna and coluna in df_filtrado.columns:

        valor = pd.to_numeric(
            df_filtrado[coluna],
            errors="coerce"
        ).sum()

        if pd.notna(valor):
            return valor

    return padrao


# =========================================================
# KPIs
# =========================================================

assinantes = soma(col_assinantes)

churn = media(col_churn)

satisfacao = media(col_satisfacao)

nps = media(col_nps)

crescimento = media(col_crescimento)

players_monitorados = (
    df_filtrado[col_player].nunique()
    if col_player else 0
)


st.divider()

st.subheader("📊 Visão Executiva")

k1, k2, k3, k4, k5 = st.columns(5)


with k1:

    if assinantes >= 1_000_000:
        valor_assinantes = f"{assinantes / 1_000_000:.1f} M"

    elif assinantes >= 1_000:
        valor_assinantes = f"{assinantes / 1_000:.1f} mil"

    else:
        valor_assinantes = f"{assinantes:,.0f}"

    st.metric(
        "Assinantes monitorados",
        valor_assinantes
    )


with k2:

    st.metric(
        "Churn médio",
        f"{churn:.1f}%",
        delta=f"{META_CHURN - churn:.1f} p.p. vs limite",
        delta_color="normal" if churn <= META_CHURN else "inverse"
    )


with k3:

    st.metric(
        "Satisfação",
        f"{satisfacao:.1f}/10",
        delta=f"{satisfacao - META_SATISFACAO:+.1f} vs meta"
    )


with k4:

    st.metric(
        "NPS",
        f"{nps:.0f}",
        delta=f"{nps - META_NPS:+.0f} pts vs meta"
    )


with k5:

    st.metric(
        "Players monitorados",
        players_monitorados
    )


# =========================================================
# PERFORMANCE VS META
# =========================================================

st.divider()

st.subheader("🎯 Performance vs. Meta")


p1, p2, p3, p4 = st.columns(4)


with p1:

    st.metric(
        "NPS",
        f"{nps:.0f}",
        f"Meta ≥ {META_NPS}"
    )

    if nps >= META_NPS:
        st.success("Meta atingida")
    else:
        st.warning("Abaixo da meta")


with p2:

    st.metric(
        "Satisfação",
        f"{satisfacao:.1f}",
        f"Meta ≥ {META_SATISFACAO}"
    )

    if satisfacao >= META_SATISFACAO:
        st.success("Meta atingida")
    else:
        st.warning("Abaixo da meta")


with p3:

    st.metric(
        "Churn",
        f"{churn:.1f}%",
        f"Limite ≤ {META_CHURN}%"
    )

    if churn <= META_CHURN:
        st.success("Dentro do limite")
    else:
        st.error("Acima do limite")


with p4:

    st.metric(
        "Crescimento",
        f"{crescimento:.1f}%",
        f"Meta ≥ {META_CRESCIMENTO}%"
    )

    if crescimento >= META_CRESCIMENTO:
        st.success("Meta atingida")
    else:
        st.warning("Abaixo da meta")


# =========================================================
# GRÁFICOS POR PLAYER
# =========================================================

st.divider()

st.subheader("📡 Monitoramento Competitivo")


# MARKET SHARE
if col_player and col_share:

    dados_share = (
        df_filtrado
        .groupby(col_player)[col_share]
        .mean()
        .reset_index()
    )

    dados_share[col_share] = pd.to_numeric(
        dados_share[col_share],
        errors="coerce"
    )

    grafico_share = (
        alt.Chart(dados_share)
        .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
        .encode(
            x=alt.X(
                f"{col_player}:N",
                title="Player",
                sort="-y"
            ),
            y=alt.Y(
                f"{col_share}:Q",
                title="Market Share"
            ),
            tooltip=[
                col_player,
                alt.Tooltip(
                    col_share,
                    format=".1f"
                )
            ]
        )
        .properties(
            height=350,
            title="Market Share por Player"
        )
    )

    st.altair_chart(
        grafico_share,
        use_container_width=True
    )


# =========================================================
# CHURN + META
# =========================================================

if col_player and col_churn:

    dados_churn = (
        df_filtrado
        .groupby(col_player)[col_churn]
        .mean()
        .reset_index()
    )

    dados_churn[col_churn] = pd.to_numeric(
        dados_churn[col_churn],
        errors="coerce"
    )

    barras = (
        alt.Chart(dados_churn)
        .mark_bar()
        .encode(
            x=alt.X(
                f"{col_player}:N",
                title="Player"
            ),
            y=alt.Y(
                f"{col_churn}:Q",
                title="Churn (%)"
            ),
            tooltip=[
                col_player,
                alt.Tooltip(
                    col_churn,
                    format=".1f"
                )
            ]
        )
    )

    linha_meta = (
        alt.Chart(
            pd.DataFrame(
                {"Meta": [META_CHURN]}
            )
        )
        .mark_rule(
            strokeDash=[6, 4],
            size=2
        )
        .encode(
            y="Meta:Q"
        )
    )

    grafico_churn = (
        barras + linha_meta
    ).properties(
        height=330,
        title=f"Churn por Player | Limite: {META_CHURN}%"
    )

    st.altair_chart(
        grafico_churn,
        use_container_width=True
    )


# =========================================================
# NPS + META
# =========================================================

if col_player and col_nps:

    dados_nps = (
        df_filtrado
        .groupby(col_player)[col_nps]
        .mean()
        .reset_index()
    )

    dados_nps[col_nps] = pd.to_numeric(
        dados_nps[col_nps],
        errors="coerce"
    )

    barras_nps = (
        alt.Chart(dados_nps)
        .mark_bar()
        .encode(
            x=alt.X(
                f"{col_player}:N",
                title="Player"
            ),
            y=alt.Y(
                f"{col_nps}:Q",
                title="NPS"
            ),
            tooltip=[
                col_player,
                alt.Tooltip(
                    col_nps,
                    format=".0f"
                )
            ]
        )
    )

    meta_nps = (
        alt.Chart(
            pd.DataFrame(
                {"Meta": [META_NPS]}
            )
        )
        .mark_rule(
            strokeDash=[6, 4],
            size=2
        )
        .encode(
            y="Meta:Q"
        )
    )

    grafico_nps = (
        barras_nps + meta_nps
    ).properties(
        height=330,
        title=f"NPS por Player | Meta: {META_NPS}"
    )

    st.altair_chart(
        grafico_nps,
        use_container_width=True
    )


# =========================================================
# SATISFAÇÃO
# =========================================================

if col_player and col_satisfacao:

    dados_sat = (
        df_filtrado
        .groupby(col_player)[col_satisfacao]
        .mean()
        .reset_index()
    )

    dados_sat[col_satisfacao] = pd.to_numeric(
        dados_sat[col_satisfacao],
        errors="coerce"
    )

    barras_sat = (
        alt.Chart(dados_sat)
        .mark_bar()
        .encode(
            x=alt.X(
                f"{col_player}:N",
                title="Player"
            ),
            y=alt.Y(
                f"{col_satisfacao}:Q",
                title="Satisfação",
                scale=alt.Scale(domain=[0, 10])
            ),
            tooltip=[
                col_player,
                alt.Tooltip(
                    col_satisfacao,
                    format=".1f"
                )
            ]
        )
    )

    meta_sat = (
        alt.Chart(
            pd.DataFrame(
                {"Meta": [META_SATISFACAO]}
            )
        )
        .mark_rule(
            strokeDash=[6, 4],
            size=2
        )
        .encode(
            y="Meta:Q"
        )
    )

    st.altair_chart(
        (barras_sat + meta_sat).properties(
            height=330,
            title=f"Satisfação por Player | Meta: {META_SATISFACAO}"
        ),
        use_container_width=True
    )


# =========================================================
# EVOLUÇÃO TEMPORAL
# =========================================================

if col_periodo and col_share and col_player:

    st.divider()

    st.subheader("📈 Evolução de Market Share")

    evolucao = (
        df_filtrado
        .groupby(
            [col_periodo, col_player]
        )[col_share]
        .mean()
        .reset_index()
    )

    evolucao[col_share] = pd.to_numeric(
        evolucao[col_share],
        errors="coerce"
    )

    grafico_evolucao = (
        alt.Chart(evolucao)
        .mark_line(
            point=True
        )
        .encode(
            x=alt.X(
                f"{col_periodo}:N",
                title="Período"
            ),
            y=alt.Y(
                f"{col_share}:Q",
                title="Market Share"
            ),
            color=alt.Color(
                f"{col_player}:N",
                title="Player"
            ),
            tooltip=[
                col_periodo,
                col_player,
                alt.Tooltip(
                    col_share,
                    format=".1f"
                )
            ]
        )
        .properties(
            height=380
        )
    )

    st.altair_chart(
        grafico_evolucao,
        use_container_width=True
    )


# =========================================================
# RADAR INTELIGENTE
# =========================================================

st.divider()

st.subheader("🚨 Radar Inteligente")

alertas = []


if churn > META_CHURN:

    alertas.append(
        f"Churn médio em {churn:.1f}%, "
        f"acima do limite de {META_CHURN:.1f}%."
    )


if nps < META_NPS:

    alertas.append(
        f"NPS em {nps:.0f}, "
        f"{META_NPS - nps:.0f} pontos abaixo da meta."
    )


if satisfacao < META_SATISFACAO:

    alertas.append(
        f"Satisfação em {satisfacao:.1f}, "
        f"abaixo da meta de {META_SATISFACAO:.1f}."
    )


if crescimento < META_CRESCIMENTO:

    alertas.append(
        f"Crescimento de {crescimento:.1f}%, "
        f"abaixo da meta de {META_CRESCIMENTO:.1f}%."
    )


if len(alertas) == 0:

    st.success(
        "🟢 Nenhum desvio crítico identificado "
        "nos indicadores monitorados."
    )

else:

    st.warning(
        f"⚠️ {len(alertas)} ponto(s) de atenção identificado(s)."
    )

    for alerta in alertas:
        st.write("🔎", alerta)


# =========================================================
# INVESTIGAÇÃO
# =========================================================

if st.button("✨ Investigar movimento"):

    st.subheader("🧠 Diagnóstico automático")

    if len(alertas) == 0:

        st.success(
            "Os indicadores selecionados estão dentro "
            "dos parâmetros definidos para o protótipo."
        )

        st.write(
            "O monitoramento deve continuar para identificar "
            "mudanças relevantes nos próximos períodos."
        )

    else:

        st.write(
            "O radar identificou indicadores que merecem "
            "investigação mais aprofundada:"
        )

        for alerta in alertas:
            st.write("•", alerta)

        st.info(
            "💡 Próximo passo analítico: cruzar os desvios "
            "com evolução de Market Share, aquisição, "
            "satisfação e comportamento dos concorrentes."
        )


# =========================================================
# METODOLOGIA
# =========================================================

st.divider()

with st.expander("ℹ️ Sobre o projeto"):

    st.markdown(
        """
        **Market Pulse AI** é um protótipo experimental de
        Inteligência de Mercado desenvolvido para demonstrar
        como dados competitivos podem ser utilizados na
        identificação automática de movimentos de mercado.

        O projeto combina:

        - monitoramento competitivo;
        - KPIs de mercado e experiência;
        - comparação entre players;
        - metas e limites de performance;
        - detecção automática de desvios;
        - geração de alertas analíticos;
        - preparação para análises com IA generativa.

        **Importante:** os dados utilizados são sintéticos e
        foram criados exclusivamente para fins de demonstração
        e portfólio.

        As metas apresentadas também são ilustrativas e não
        representam metas oficiais das empresas analisadas.
        """
    )
