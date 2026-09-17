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
# IDENTIFICAÇÃO AUTOMÁTICA DAS COLUNAS
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

col_receita = encontrar_coluna(
    ["receita", "revenue", "faturamento"]
)

col_aquisicao = encontrar_coluna(
    ["aquisicao", "aquisição", "adicoes", "adições"]
)


# =========================================================
# CABEÇALHO
# =========================================================

st.title("🧠 Market Pulse — Radar Inteligente")

st.subheader(
    "Inteligência de Mercado potencializada por IA"
)

st.caption(
    "Radar experimental desenvolvido com dados sintéticos "
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
# METAS ILUSTRATIVAS
# =========================================================

META_NPS = 70
META_SATISFACAO = 8.0
META_CHURN = 5.0
META_CRESCIMENTO = 5.0

st.sidebar.divider()

st.sidebar.subheader("🎯 Metas do Radar")

st.sidebar.caption("NPS ≥ 70")
st.sidebar.caption("Satisfação ≥ 8,0")
st.sidebar.caption("Churn ≤ 5,0%")
st.sidebar.caption("Crescimento ≥ 5,0%")

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
# CÁLCULO DOS KPIs
# =========================================================

assinantes = soma(col_assinantes)

churn = media(col_churn)

satisfacao = media(col_satisfacao)

nps = media(col_nps)

crescimento = media(col_crescimento)

receita = soma(col_receita)

aquisicao = soma(col_aquisicao)

players_monitorados = (
    df_filtrado[col_player].nunique()
    if col_player else 0
)


# Valores arredondados utilizados na exibição e comparação

nps_exib = round(nps)
satisfacao_exib = round(satisfacao, 1)
churn_exib = round(churn, 1)
crescimento_exib = round(crescimento, 1)


# =========================================================
# VISÃO EXECUTIVA
# =========================================================

st.divider()

st.subheader("📊 Visão Executiva")

k1, k2, k3, k4, k5 = st.columns(5)


with k1:

    if assinantes >= 1_000_000:

        valor_assinantes = (
            f"{assinantes / 1_000_000:.1f} M"
        )

    elif assinantes >= 1_000:

        valor_assinantes = (
            f"{assinantes / 1_000:.1f} mil"
        )

    else:

        valor_assinantes = f"{assinantes:,.0f}"

    st.metric(
        "Assinantes monitorados",
        valor_assinantes
    )


with k2:

    st.metric(
        "Churn médio",
        f"{churn_exib:.1f}%"
    )


with k3:

    st.metric(
        "Satisfação",
        f"{satisfacao_exib:.1f}/10"
    )


with k4:

    st.metric(
        "NPS médio",
        f"{nps_exib:.0f}"
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


gap_nps = nps_exib - META_NPS

gap_satisfacao = (
    satisfacao_exib - META_SATISFACAO
)

gap_churn = (
    churn_exib - META_CHURN
)

gap_crescimento = (
    crescimento_exib - META_CRESCIMENTO
)


p1, p2, p3, p4 = st.columns(4)


# NPS
with p1:

    st.metric(
        "NPS",
        f"{nps_exib:.0f}",
        f"Meta ≥ {META_NPS}"
    )

    if gap_nps > 0:

        st.success(
            f"▲ {abs(gap_nps):.0f} pontos acima da meta"
        )

    elif gap_nps < 0:

        st.warning(
            f"▼ {abs(gap_nps):.0f} pontos abaixo da meta"
        )

    else:

        st.success("● Exatamente na meta")


# SATISFAÇÃO
with p2:

    st.metric(
        "Satisfação",
        f"{satisfacao_exib:.1f}",
        f"Meta ≥ {META_SATISFACAO:.1f}"
    )

    if gap_satisfacao > 0:

        st.success(
            f"▲ {abs(gap_satisfacao):.1f} "
            "ponto acima da meta"
        )

    elif gap_satisfacao < 0:

        st.warning(
            f"▼ {abs(gap_satisfacao):.1f} "
            "ponto abaixo da meta"
        )

    else:

        st.success("● Exatamente na meta")


# CHURN
with p3:

    st.metric(
        "Churn",
        f"{churn_exib:.1f}%",
        f"Limite ≤ {META_CHURN:.1f}%"
    )

    if gap_churn > 0:

        st.error(
            f"▲ {abs(gap_churn):.1f} p.p. "
            "acima do limite"
        )

    elif gap_churn < 0:

        st.success(
            f"▼ {abs(gap_churn):.1f} p.p. "
            "abaixo do limite"
        )

    else:

        st.success("● Exatamente no limite")


# CRESCIMENTO
with p4:

    st.metric(
        "Crescimento",
        f"{crescimento_exib:.1f}%",
        f"Meta ≥ {META_CRESCIMENTO:.1f}%"
    )

    if gap_crescimento > 0:

        st.success(
            f"▲ {abs(gap_crescimento):.1f} p.p. "
            "acima da meta"
        )

    elif gap_crescimento < 0:

        st.warning(
            f"▼ {abs(gap_crescimento):.1f} p.p. "
            "abaixo da meta"
        )

    else:

        st.success("● Exatamente na meta")


# =========================================================
# MARKET SHARE ATUAL
# =========================================================

st.divider()

st.subheader("📡 Monitoramento Competitivo")


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

    barras_share = (
        alt.Chart(dados_share)
        .mark_bar(
            cornerRadiusTopLeft=5,
            cornerRadiusTopRight=5
        )
        .encode(

            x=alt.X(
                f"{col_player}:N",
                title="Player",
                sort="-y"
            ),

            y=alt.Y(
                f"{col_share}:Q",
                title="Market Share (%)"
            ),

            tooltip=[

                col_player,

                alt.Tooltip(
                    col_share,
                    title="Market Share",
                    format=".1f"
                )
            ]
        )
    )

    rotulos_share = (
        alt.Chart(dados_share)
        .mark_text(
            dy=-10,
            fontSize=14
        )
        .encode(

            x=alt.X(
                f"{col_player}:N",
                sort="-y"
            ),

            y=f"{col_share}:Q",

            text=alt.Text(
                f"{col_share}:Q",
                format=".1f"
            )
        )
    )

    st.altair_chart(
        (barras_share + rotulos_share)
        .properties(
            height=350,
            title="Market Share por Player (%)"
        ),
        use_container_width=True
    )


# =========================================================
# CHURN POR PLAYER + META
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

    st.altair_chart(
        (barras + linha_meta)
        .properties(
            height=330,
            title=(
                f"Churn por Player | "
                f"Limite: {META_CHURN}%"
            )
        ),
        use_container_width=True
    )


# =========================================================
# NPS POR PLAYER + META
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

    st.altair_chart(
        (barras_nps + meta_nps)
        .properties(
            height=330,
            title=(
                f"NPS por Player | Meta: {META_NPS}"
            )
        ),
        use_container_width=True
    )


# =========================================================
# SATISFAÇÃO POR PLAYER
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
                scale=alt.Scale(
                    domain=[0, 10]
                )
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
        (barras_sat + meta_sat)
        .properties(
            height=330,
            title=(
                "Satisfação por Player | "
                f"Meta: {META_SATISFACAO}"
            )
        ),
        use_container_width=True
    )


# =========================================================
# EVOLUÇÃO DE MARKET SHARE
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

    # Linha
    linhas = (
        alt.Chart(evolucao)
        .mark_line(
            point=True,
            strokeWidth=2
        )
        .encode(

            x=alt.X(
                f"{col_periodo}:N",
                title="Período"
            ),

            y=alt.Y(
                f"{col_share}:Q",
                title="Market Share (%)"
            ),

            color=alt.Color(
                f"{col_player}:N",
                title="Player"
            ),

            tooltip=[

                alt.Tooltip(
                    f"{col_periodo}:N",
                    title="Período"
                ),

                alt.Tooltip(
                    f"{col_player}:N",
                    title="Player"
                ),

                alt.Tooltip(
                    f"{col_share}:Q",
                    title="Market Share",
                    format=".1f"
                )
            ]
        )
    )

    # Números sobre os pontos
    labels = (
        alt.Chart(evolucao)
        .mark_text(
            dy=-10,
            fontSize=10
        )
        .encode(

            x=alt.X(
                f"{col_periodo}:N"
            ),

            y=alt.Y(
                f"{col_share}:Q"
            ),

            color=alt.Color(
                f"{col_player}:N",
                legend=None
            ),

            text=alt.Text(
                f"{col_share}:Q",
                format=".1f"
            )
        )
    )

    grafico_evolucao = (
        linhas + labels
    ).properties(
        height=430
    )

    st.altair_chart(
        grafico_evolucao,
        use_container_width=True
    )

    st.caption(
        "Valores exibidos em pontos percentuais de participação."
    )


# =========================================================
# RADAR INTELIGENTE
# =========================================================

st.divider()

st.subheader("🚨 Radar Inteligente")

alertas = []


# ---------------------------------------------------------
# 1. CHURN
# ---------------------------------------------------------

if churn_exib > META_CHURN:

    desvio = churn_exib - META_CHURN

    alertas.append(
        {
            "nivel": "alto",
            "titulo": "Pressão de retenção",
            "texto": (
                f"Churn médio em {churn_exib:.1f}%, "
                f"{desvio:.1f} p.p. acima do limite "
                f"de {META_CHURN:.1f}%."
            )
        }
    )


# ---------------------------------------------------------
# 2. NPS
# ---------------------------------------------------------

if nps_exib < META_NPS:

    desvio = META_NPS - nps_exib

    alertas.append(
        {
            "nivel": "medio",
            "titulo": "Experiência abaixo da meta",
            "texto": (
                f"NPS em {nps_exib:.0f}, "
                f"{desvio:.0f} pontos abaixo "
                f"da meta de {META_NPS}."
            )
        }
    )


# ---------------------------------------------------------
# 3. SATISFAÇÃO
# ---------------------------------------------------------

if satisfacao_exib < META_SATISFACAO:

    desvio = (
        META_SATISFACAO - satisfacao_exib
    )

    alertas.append(
        {
            "nivel": "medio",
            "titulo": "Satisfação abaixo da meta",
            "texto": (
                f"Satisfação em {satisfacao_exib:.1f}, "
                f"{desvio:.1f} ponto abaixo "
                f"da meta de {META_SATISFACAO:.1f}."
            )
        }
    )


# ---------------------------------------------------------
# 4. CRESCIMENTO
# ---------------------------------------------------------

if crescimento_exib < META_CRESCIMENTO:

    desvio = (
        META_CRESCIMENTO - crescimento_exib
    )

    alertas.append(
        {
            "nivel": "medio",
            "titulo": "Crescimento abaixo do esperado",
            "texto": (
                f"Crescimento de "
                f"{crescimento_exib:.1f}%, "
                f"{desvio:.1f} p.p. abaixo "
                f"da meta de {META_CRESCIMENTO:.1f}%."
            )
        }
    )


# =========================================================
# ALERTAS DE MARKET SHARE
# =========================================================

if (
    col_player
    and col_periodo
    and col_share
):

    tabela_share = (
        df_filtrado
        .groupby(
            [col_periodo, col_player]
        )[col_share]
        .mean()
        .reset_index()
    )

    tabela_share[col_share] = pd.to_numeric(
        tabela_share[col_share],
        errors="coerce"
    )

    periodos_share = sorted(
        tabela_share[col_periodo]
        .astype(str)
        .unique()
    )

    if len(periodos_share) >= 2:

        periodo_anterior = periodos_share[-2]
        periodo_atual = periodos_share[-1]

        share_anterior = (
            tabela_share[
                tabela_share[col_periodo].astype(str)
                == periodo_anterior
            ]
            .set_index(col_player)[col_share]
        )

        share_atual = (
            tabela_share[
                tabela_share[col_periodo].astype(str)
                == periodo_atual
            ]
            .set_index(col_player)[col_share]
        )

        players_comuns = (
            share_atual.index
            .intersection(
                share_anterior.index
            )
        )

        for nome_player in players_comuns:

            variacao = (
                share_atual[nome_player]
                - share_anterior[nome_player]
            )

            # Queda relevante
            if variacao <= -0.5:

                alertas.append(
                    {
                        "nivel": "alto",
                        "titulo": (
                            f"Perda de participação — "
                            f"{nome_player}"
                        ),
                        "texto": (
                            f"{nome_player} perdeu "
                            f"{abs(variacao):.1f} p.p. "
                            f"de Market Share entre "
                            f"{periodo_anterior} e "
                            f"{periodo_atual}."
                        )
                    }
                )

            # Ganho relevante
            elif variacao >= 0.5:

                alertas.append(
                    {
                        "nivel": "oportunidade",
                        "titulo": (
                            f"Movimento competitivo — "
                            f"{nome_player}"
                        ),
                        "texto": (
                            f"{nome_player} ganhou "
                            f"{variacao:.1f} p.p. "
                            f"de Market Share entre "
                            f"{periodo_anterior} e "
                            f"{periodo_atual}."
                        )
                    }
                )


# =========================================================
# CONCENTRAÇÃO DE MERCADO
# =========================================================

if col_player and col_share:

    share_players = (
        df_filtrado
        .groupby(col_player)[col_share]
        .mean()
        .sort_values(
            ascending=False
        )
    )

    if len(share_players) >= 2:

        concentracao_top2 = (
            share_players.iloc[0]
            + share_players.iloc[1]
        )

        if concentracao_top2 >= 60:

            alertas.append(
                {
                    "nivel": "observacao",
                    "titulo": "Concentração competitiva",
                    "texto": (
                        "Os dois maiores players "
                        f"concentram aproximadamente "
                        f"{concentracao_top2:.1f}% "
                        "do Market Share monitorado."
                    )
                }
            )


# =========================================================
# CRUZAMENTO NPS + CHURN
# =========================================================

if (
    nps_exib < META_NPS
    and churn_exib > META_CHURN
):

    alertas.append(
        {
            "nivel": "alto",
            "titulo": "Sinal combinado de experiência e retenção",
            "texto": (
                "NPS abaixo da meta ocorre simultaneamente "
                "a churn acima do limite. O cruzamento merece "
                "investigação para avaliar possível relação "
                "entre experiência e perda de clientes."
            )
        }
    )


# =========================================================
# CRUZAMENTO CRESCIMENTO + CHURN
# =========================================================

if (
    crescimento_exib < META_CRESCIMENTO
    and churn_exib > META_CHURN
):

    alertas.append(
        {
            "nivel": "alto",
            "titulo": "Pressão sobre crescimento da base",
            "texto": (
                "O baixo crescimento ocorre junto de churn "
                "acima do limite, indicando um possível "
                "desafio de retenção para expansão da base."
            )
        }
    )


# =========================================================
# EXIBIÇÃO DOS ALERTAS
# =========================================================

if len(alertas) == 0:

    st.success(
        "🟢 Nenhum ponto crítico identificado "
        "nos indicadores monitorados."
    )

else:

    alertas_altos = len(
        [
            x for x in alertas
            if x["nivel"] == "alto"
        ]
    )

    oportunidades = len(
        [
            x for x in alertas
            if x["nivel"] == "oportunidade"
        ]
    )

    r1, r2, r3 = st.columns(3)

    with r1:
        st.metric(
            "Pontos de atenção",
            len(alertas)
        )

    with r2:
        st.metric(
            "Alta prioridade",
            alertas_altos
        )

    with r3:
        st.metric(
            "Oportunidades",
            oportunidades
        )

    st.warning(
        f"⚠️ {len(alertas)} sinal(is) "
        "identificado(s) pelo radar."
    )

    for alerta in alertas:

        if alerta["nivel"] == "alto":

            icone = "🔴"

        elif alerta["nivel"] == "medio":

            icone = "🟡"

        elif alerta["nivel"] == "oportunidade":

            icone = "🟢"

        else:

            icone = "🔵"

        st.markdown(
            f"""
            **{icone} {alerta['titulo']}**

            {alerta['texto']}
            """
        )


# =========================================================
# INVESTIGAÇÃO AUTOMÁTICA
# =========================================================

if st.button(
    "✨ Investigar movimentos",
    use_container_width=False
):

    st.subheader(
        "🧠 Diagnóstico Analítico"
    )

    if len(alertas) == 0:

        st.success(
            "Os indicadores monitorados estão "
            "dentro dos parâmetros definidos."
        )

    else:

        st.write(
            "O radar encontrou sinais que merecem "
            "investigação mais aprofundada."
        )

        # Prioridades
        prioridades = [
            x for x in alertas
            if x["nivel"] == "alto"
        ]

        if prioridades:

            st.markdown(
                "### 🔴 Prioridades de investigação"
            )

            for item in prioridades:

                st.write(
                    f"• **{item['titulo']}** — "
                    f"{item['texto']}"
                )

        # Hipóteses
        st.markdown(
            "### 🔎 Hipóteses para investigação"
        )

        if (
            churn_exib > META_CHURN
            and nps_exib < META_NPS
        ):

            st.write(
                "• Avaliar se a deterioração da "
                "experiência está associada ao aumento "
                "da saída de clientes."
            )

        if crescimento_exib < META_CRESCIMENTO:

            st.write(
                "• Separar aquisição e cancelamentos "
                "para identificar qual componente está "
                "limitando o crescimento da base."
            )

        if col_share:

            st.write(
                "• Comparar movimentos de Market Share "
                "com churn, satisfação e NPS por player."
            )

        st.info(
            "💡 Estas são hipóteses analíticas geradas "
            "a partir dos indicadores do protótipo. "
            "Elas não representam relações causais comprovadas."
        )


# =========================================================
# PRÓXIMA CAMADA — IA
# =========================================================

st.divider()

st.subheader("🤖 Market Pulse AI")

st.caption(
    "Camada de inteligência generativa — próxima etapa do projeto."
)

st.info(
    "A IA será utilizada para interpretar os sinais detectados "
    "pelo Radar, levantar hipóteses e apoiar a construção de "
    "possíveis planos de ação."
)


# =========================================================
# SOBRE O PROJETO
# =========================================================

st.divider()

with st.expander("ℹ️ Sobre o projeto"):

    st.markdown(
        """
        **Market Pulse AI** é um protótipo experimental
        de Inteligência de Mercado.

        O sistema foi desenvolvido para demonstrar como
        dados competitivos podem apoiar:

        - monitoramento de mercado;
        - acompanhamento de Market Share;
        - análise de experiência;
        - monitoramento de churn;
        - comparação realizado vs. meta;
        - identificação de movimentos competitivos;
        - priorização de sinais de atenção;
        - geração de hipóteses analíticas;
        - apoio à construção de planos de ação com IA.

        **Dados sintéticos**

        Todos os dados utilizados neste projeto são
        sintéticos e foram criados exclusivamente para
        demonstração e portfólio.

        **Metas ilustrativas**

        As metas e limites apresentados também são
        fictícios e não representam metas oficiais
        das empresas exibidas.
        """
    )
