         import streamlit as st
import pandas as pd
import altair as alt
import os

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Market Pulse AI",
    page_icon="📡",
    layout="wide"
)

# ============================================================
# BASE
# ============================================================

ARQUIVOS_POSSIVEIS = [
    "dados_streaming_market_pulse_novos_players (3).csv",
    "dados_streaming_market_pulse_novos_players.csv",
    "dados_streaming_market_pulse.csv",
]

arquivo_base = None

for arquivo in ARQUIVOS_POSSIVEIS:
    if os.path.exists(arquivo):
        arquivo_base = arquivo
        break

if arquivo_base is None:
    st.error("Base de dados não encontrada no repositório.")
    st.stop()

df = pd.read_csv(arquivo_base)

# ============================================================
# PADRONIZAÇÃO DOS NOMES DAS COLUNAS
# ============================================================

df.columns = [
    str(c).strip().lower().replace(" ", "_")
    for c in df.columns
]

def localizar_coluna(possiveis):
    for nome in possiveis:
        if nome in df.columns:
            return nome

    for coluna in df.columns:
        for nome in possiveis:
            if nome in coluna:
                return coluna

    return None


col_player = localizar_coluna([
    "player", "operadora", "empresa"
])

col_periodo = localizar_coluna([
    "periodo", "período", "mes", "mês", "data"
])

col_regiao = localizar_coluna([
    "regiao", "região", "uf", "estado"
])

col_share = localizar_coluna([
    "market_share", "share"
])

col_assinantes = localizar_coluna([
    "assinantes", "assinaturas", "clientes", "base_clientes"
])

col_churn = localizar_coluna([
    "churn", "churn_medio"
])

col_nps = localizar_coluna([
    "nps"
])

col_satisfacao = localizar_coluna([
    "satisfacao", "satisfação", "csat"
])

# ============================================================
# CONVERTER INDICADORES PARA NÚMERO
# ============================================================

colunas_numericas = [
    col_share,
    col_assinantes,
    col_churn,
    col_nps,
    col_satisfacao
]

for coluna in colunas_numericas:
    if coluna and coluna in df.columns:
        df[coluna] = pd.to_numeric(
            df[coluna]
            .astype(str)
            .str.replace("%", "", regex=False)
            .str.replace(",", ".", regex=False),
            errors="coerce"
        )

# ============================================================
# TÍTULO
# ============================================================

st.title("📡 Market Pulse AI")

st.subheader("Inteligência de Mercado potencializada por IA")

st.caption(
    "Radar experimental desenvolvido com dados sintéticos para "
    "identificação de movimentos competitivos, riscos e oportunidades."
)

# ============================================================
# FILTROS
# ============================================================

st.sidebar.header("🔎 Filtros")

df_filtrado = df.copy()

if col_player:
    players = sorted(
        df[col_player].dropna().astype(str).unique().tolist()
    )

    player_selecionado = st.sidebar.selectbox(
        "Player",
        ["Todos"] + players
    )

    if player_selecionado != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado[col_player].astype(str) == player_selecionado
        ]


if col_regiao:
    regioes = sorted(
        df[col_regiao].dropna().astype(str).unique().tolist()
    )

    regiao_selecionada = st.sidebar.selectbox(
        "Região",
        ["Todas"] + regioes
    )

    if regiao_selecionada != "Todas":
        df_filtrado = df_filtrado[
            df_filtrado[col_regiao].astype(str) == regiao_selecionada
        ]


if col_periodo:
    periodos = sorted(
        df[col_periodo].dropna().astype(str).unique().tolist()
    )

    periodo_selecionado = st.sidebar.selectbox(
        "Período",
        ["Todos"] + periodos
    )

    if periodo_selecionado != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado[col_periodo].astype(str) == periodo_selecionado
        ]

# ============================================================
# STATUS
# ============================================================

st.success(
    f"🟢 Monitoramento ativo • "
    f"{len(df_filtrado):,.0f} registros analisados"
    .replace(",", ".")
)

# ============================================================
# FUNÇÕES
# ============================================================

def media(coluna, base=None):
    if base is None:
        base = df_filtrado

    if coluna and coluna in base.columns:
        valor = pd.to_numeric(
            base[coluna],
            errors="coerce"
        ).mean()

        if pd.notna(valor):
            return float(valor)

    return 0.0


def soma(coluna, base=None):
    if base is None:
        base = df_filtrado

    if coluna and coluna in base.columns:
        valor = pd.to_numeric(
            base[coluna],
            errors="coerce"
        ).sum()

        if pd.notna(valor):
            return float(valor)

    return 0.0


# ============================================================
# INDICADORES PRINCIPAIS
# ============================================================

assinantes = soma(col_assinantes)

churn = media(col_churn)

nps = media(col_nps)

satisfacao = media(col_satisfacao)

players_monitorados = (
    df_filtrado[col_player].nunique()
    if col_player
    else 0
)

# ============================================================
# CRESCIMENTO
# Calculado sobre a base SEM o filtro de período.
# Assim, selecionar um mês não destrói a comparação histórica.
# ============================================================

crescimento = 0.0

base_crescimento = df.copy()

# mantém filtros de Player e Região
if col_player and "player_selecionado" in locals():
    if player_selecionado != "Todos":
        base_crescimento = base_crescimento[
            base_crescimento[col_player].astype(str)
            == player_selecionado
        ]

if col_regiao and "regiao_selecionada" in locals():
    if regiao_selecionada != "Todas":
        base_crescimento = base_crescimento[
            base_crescimento[col_regiao].astype(str)
            == regiao_selecionada
        ]

if col_periodo and col_assinantes:

    crescimento_periodo = (
        base_crescimento
        .groupby(col_periodo, as_index=False)[col_assinantes]
        .sum()
    )

    crescimento_periodo["_periodo_ordem"] = (
        crescimento_periodo[col_periodo].astype(str)
    )

    crescimento_periodo = crescimento_periodo.sort_values(
        "_periodo_ordem"
    )

    # Se um período específico estiver selecionado,
    # compara esse período com o imediatamente anterior.
    if (
        "periodo_selecionado" in locals()
        and periodo_selecionado != "Todos"
    ):

        lista_periodos = (
            crescimento_periodo[col_periodo]
            .astype(str)
            .tolist()
        )

        if periodo_selecionado in lista_periodos:

            indice = lista_periodos.index(periodo_selecionado)

            if indice > 0:
                anterior = crescimento_periodo.iloc[
                    indice - 1
                ][col_assinantes]

                atual = crescimento_periodo.iloc[
                    indice
                ][col_assinantes]

                if anterior != 0:
                    crescimento = (
                        (atual - anterior) / anterior
                    ) * 100

    elif len(crescimento_periodo) >= 2:

        anterior = crescimento_periodo.iloc[-2][col_assinantes]
        atual = crescimento_periodo.iloc[-1][col_assinantes]

        if anterior != 0:
            crescimento = (
                (atual - anterior) / anterior
            ) * 100

# ============================================================
# KPIs
# ============================================================

st.markdown("## 📊 Visão Executiva")

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    if assinantes >= 1_000_000:
        st.metric(
            "Assinantes monitorados",
            f"{assinantes / 1_000_000:.1f} M"
        )
    else:
        st.metric(
            "Assinantes monitorados",
            f"{assinantes:,.0f}"
        )

with k2:
    st.metric(
        "Churn médio",
        f"{churn:.1f}%"
    )

with k3:
    st.metric(
        "NPS",
        f"{nps:.0f}"
    )

with k4:
    st.metric(
        "Satisfação",
        f"{satisfacao:.1f}/10"
    )

with k5:
    st.metric(
        "Crescimento",
        f"{crescimento:+.1f}%"
    )

st.caption(
    f"Players monitorados: {players_monitorados}"
)

st.divider()

# ============================================================
# PERFORMANCE VS META
# ============================================================

st.markdown("## 🎯 Performance vs. Meta")

META_NPS = 70
META_SATISFACAO = 8.0
LIMITE_CHURN = 5.0
META_CRESCIMENTO = 5.0

dif_nps = nps - META_NPS
dif_satisfacao = satisfacao - META_SATISFACAO

# Para churn, positivo = pior que o limite
dif_churn = churn - LIMITE_CHURN

dif_crescimento = crescimento - META_CRESCIMENTO

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        "NPS",
        f"{nps:.0f}",
        f"{dif_nps:+.1f} pts vs. meta"
    )

    if nps >= META_NPS:
        st.success("Meta atingida")
    else:
        st.warning("Abaixo da meta")


with m2:
    st.metric(
        "Satisfação",
        f"{satisfacao:.1f}",
        f"{dif_satisfacao:+.1f} pt vs. meta"
    )

    if satisfacao >= META_SATISFACAO:
        st.success("Meta atingida")
    else:
        st.warning("Abaixo da meta")


with m3:
    st.metric(
        "Churn",
        f"{churn:.1f}%",
        f"{dif_churn:+.1f} p.p. vs. limite",
        delta_color="inverse"
    )

    if churn <= LIMITE_CHURN:
        st.success("Dentro do limite")
    else:
        st.error("Acima do limite")


with m4:
    st.metric(
        "Crescimento",
        f"{crescimento:+.1f}%",
        f"{dif_crescimento:+.1f} p.p. vs. meta"
    )

    if crescimento >= META_CRESCIMENTO:
        st.success("Meta atingida")
    else:
        st.warning("Abaixo da meta")

st.divider()

# ============================================================
# MONITORAMENTO COMPETITIVO
# ============================================================

st.markdown("## 📡 Monitoramento Competitivo")

# ============================================================
# MARKET SHARE POR PLAYER
# ============================================================

if col_player and col_share:

    share_player = (
        df_filtrado
        .groupby(col_player, as_index=False)[col_share]
        .mean()
        .dropna()
        .sort_values(
            col_share,
            ascending=False
        )
    )

    st.markdown("**Market Share por Player (%)**")

    barras = alt.Chart(
        share_player
    ).mark_bar(
        cornerRadiusTopLeft=4,
        cornerRadiusTopRight=4
    ).encode(

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

    # RÓTULOS BRANCOS
    textos = alt.Chart(
        share_player
    ).mark_text(
        dy=-10,
        color="white",
        fontSize=13,
        fontWeight="bold"
    ).encode(

        x=alt.X(
            f"{col_player}:N",
            sort="-y"
        ),

        y=alt.Y(
            f"{col_share}:Q"
        ),

        text=alt.Text(
            f"{col_share}:Q",
            format=".1f"
        )
    )

    grafico_share = (
        barras + textos
    ).properties(
        height=320
    )

    st.altair_chart(
        grafico_share,
        use_container_width=True
    )

# ============================================================
# EVOLUÇÃO DO MARKET SHARE
# ============================================================

if col_player and col_periodo and col_share:

    st.markdown("## 📈 Evolução de Market Share")

    # usa histórico, mantendo filtros de Player/Região
    base_historica = df.copy()

    if (
        "player_selecionado" in locals()
        and player_selecionado != "Todos"
    ):
        base_historica = base_historica[
            base_historica[col_player].astype(str)
            == player_selecionado
        ]

    if (
        col_regiao
        and "regiao_selecionada" in locals()
        and regiao_selecionada != "Todas"
    ):
        base_historica = base_historica[
            base_historica[col_regiao].astype(str)
            == regiao_selecionada
        ]

    evolucao = (
        base_historica
        .groupby(
            [col_periodo, col_player],
            as_index=False
        )[col_share]
        .mean()
        .dropna()
    )

    minimo_share = evolucao[col_share].min()
    maximo_share = evolucao[col_share].max()

    # "Zoom" no eixo Y para mostrar as oscilações.
    margem = max(
        (maximo_share - minimo_share) * 0.18,
        1.5
    )

    y_min = max(
        0,
        minimo_share - margem
    )

    y_max = maximo_share + margem

    linha = alt.Chart(
        evolucao
    ).mark_line(
        point=alt.OverlayMarkDef(
            filled=True,
            size=55
        ),
        strokeWidth=2.5
    ).encode(

        x=alt.X(
            f"{col_periodo}:O",
            title="Período",
            sort=None
        ),

        y=alt.Y(
            f"{col_share}:Q",
            title="Market Share (%)",
            scale=alt.Scale(
                domain=[y_min, y_max],
                zero=False
            )
        ),

        color=alt.Color(
            f"{col_player}:N",
            title="Player"
        ),

        tooltip=[
            alt.Tooltip(
                f"{col_periodo}:O",
                title="Período"
            ),
            alt.Tooltip(
                f"{col_player}:N",
                title="Player"
            ),
            alt.Tooltip(
                f"{col_share}:Q",
                title="Share",
                format=".1f"
            )
        ]
    )

    # RÓTULOS EM CIMA DE CADA PONTO
    rotulos = alt.Chart(
        evolucao
    ).mark_text(
        dy=-10,
        fontSize=10,
        fontWeight="bold"
    ).encode(

        x=alt.X(
            f"{col_periodo}:O",
            sort=None
        ),

        y=alt.Y(
            f"{col_share}:Q",
            scale=alt.Scale(
                domain=[y_min, y_max],
                zero=False
            )
        ),

        text=alt.Text(
            f"{col_share}:Q",
            format=".1f"
        ),

        color=alt.Color(
            f"{col_player}:N",
            legend=None
        )
    )

    grafico_evolucao = (
        linha + rotulos
    ).properties(
        height=430
    )

    st.altair_chart(
        grafico_evolucao,
        use_container_width=True
    )

st.divider()

# ============================================================
# RADAR INTELIGENTE
# ============================================================

st.markdown("## 🚨 Radar Inteligente")

alertas = []
oportunidades = []
alta_prioridade = 0

# ------------------------------------------------------------
# 1. CHURN
# ------------------------------------------------------------

if churn > LIMITE_CHURN:

    diferenca = churn - LIMITE_CHURN

    alertas.append({
        "nivel": "🔴",
        "titulo": "Pressão de retenção",
        "texto":
            f"Churn médio em {churn:.1f}%, "
            f"{diferenca:.1f} p.p. acima do "
            f"limite de {LIMITE_CHURN:.1f}%."
    })

    alta_prioridade += 1

elif churn < LIMITE_CHURN - 1:

    oportunidades.append(
        f"Churn de {churn:.1f}% está "
        f"{LIMITE_CHURN - churn:.1f} p.p. "
        "abaixo do limite."
    )

# ------------------------------------------------------------
# 2. NPS
# ------------------------------------------------------------

if nps < META_NPS:

    diferenca = META_NPS - nps

    alertas.append({
        "nivel": "🟡",
        "titulo": "Experiência abaixo da meta",
        "texto":
            f"NPS em {nps:.0f}, "
            f"{diferenca:.0f} pontos abaixo "
            f"da meta de {META_NPS}."
    })

else:

    oportunidades.append(
        f"NPS atingiu {nps:.0f}, "
        f"{nps - META_NPS:.0f} pontos acima "
        "da meta."
    )

# ------------------------------------------------------------
# 3. SATISFAÇÃO
# ------------------------------------------------------------

if satisfacao < META_SATISFACAO:

    alertas.append({
        "nivel": "🟡",
        "titulo": "Satisfação abaixo da meta",
        "texto":
            f"Satisfação em {satisfacao:.1f}, "
            f"{META_SATISFACAO - satisfacao:.1f} "
            "ponto abaixo da meta."
    })

elif satisfacao > META_SATISFACAO:

    oportunidades.append(
        f"Satisfação em {satisfacao:.1f}, "
        f"{satisfacao - META_SATISFACAO:.1f} "
        "ponto acima da meta."
    )

# ------------------------------------------------------------
# 4. CRESCIMENTO
# ------------------------------------------------------------

if crescimento < META_CRESCIMENTO:

    diferenca = META_CRESCIMENTO - crescimento

    alertas.append({
        "nivel": "🟡",
        "titulo": "Crescimento abaixo do esperado",
        "texto":
            f"Crescimento de {crescimento:.1f}%, "
            f"{diferenca:.1f} p.p. abaixo "
            f"da meta de {META_CRESCIMENTO:.1f}%."
    })

else:

    oportunidades.append(
        f"Crescimento de {crescimento:.1f}% está "
        f"{crescimento - META_CRESCIMENTO:.1f} "
        "p.p. acima da meta."
    )

# ------------------------------------------------------------
# 5. CONCENTRAÇÃO COMPETITIVA
# ------------------------------------------------------------

concentracao_top2 = 0

if col_player and col_share:

    share_radar = (
        df_filtrado
        .groupby(col_player)[col_share]
        .mean()
        .sort_values(
            ascending=False
        )
    )

    if len(share_radar) >= 2:

        concentracao_top2 = (
            share_radar.iloc[0]
            + share_radar.iloc[1]
        )

        if concentracao_top2 >= 60:

            alertas.append({
                "nivel": "🔵",
                "titulo": "Concentração competitiva",
                "texto":
                    f"Os dois maiores players concentram "
                    f"aproximadamente {concentracao_top2:.1f}% "
                    "do Market Share monitorado."
            })

        else:

            oportunidades.append(
                "Mercado apresenta menor concentração: "
                f"Top 2 representam {concentracao_top2:.1f}% "
                "do share."
            )

# ------------------------------------------------------------
# 6. EXPERIÊNCIA + RETENÇÃO
# ------------------------------------------------------------

if nps < META_NPS and churn > LIMITE_CHURN:

    alertas.append({
        "nivel": "🔴",
        "titulo":
            "Sinal combinado de experiência e retenção",

        "texto":
            "NPS abaixo da meta ocorre simultaneamente "
            "a churn acima do limite. O cruzamento merece "
            "investigação para avaliar possível relação "
            "entre experiência e perda de clientes."
    })

    alta_prioridade += 1

# ------------------------------------------------------------
# 7. CRESCIMENTO + CHURN
# ------------------------------------------------------------

if (
    crescimento < META_CRESCIMENTO
    and churn > LIMITE_CHURN
):

    alertas.append({
        "nivel": "🔴",
        "titulo":
            "Pressão sobre crescimento da base",

        "texto":
            "Crescimento abaixo da meta ocorre junto de "
            "churn acima do limite, sinalizando possível "
            "pressão de retenção sobre a expansão da base."
    })

    alta_prioridade += 1

# ------------------------------------------------------------
# 8. MOVIMENTO COMPETITIVO RECENTE
# ------------------------------------------------------------

if (
    col_player
    and col_periodo
    and col_share
):

    movimentos = (
        base_crescimento
        .groupby(
            [col_periodo, col_player],
            as_index=False
        )[col_share]
        .mean()
    )

    periodos_mov = sorted(
        movimentos[col_periodo]
        .astype(str)
        .unique()
        .tolist()
    )

    if len(periodos_mov) >= 2:

        p_anterior = periodos_mov[-2]
        p_atual = periodos_mov[-1]

        anterior = movimentos[
            movimentos[col_periodo].astype(str)
            == p_anterior
        ][[col_player, col_share]]

        atual = movimentos[
            movimentos[col_periodo].astype(str)
            == p_atual
        ][[col_player, col_share]]

        comparacao = atual.merge(
            anterior,
            on=col_player,
            suffixes=("_atual", "_anterior")
        )

        comparacao["variacao_pp"] = (
            comparacao[f"{col_share}_atual"]
            - comparacao[f"{col_share}_anterior"]
        )

        if len(comparacao) > 0:

            maior_ganho = comparacao.loc[
                comparacao["variacao_pp"].idxmax()
            ]

            maior_perda = comparacao.loc[
                comparacao["variacao_pp"].idxmin()
            ]

            ganho = float(
                maior_ganho["variacao_pp"]
            )

            perda = float(
                maior_perda["variacao_pp"]
            )

            if ganho >= 0.2:

                oportunidades.append(
                    f"{maior_ganho[col_player]} ganhou "
                    f"{ganho:.1f} p.p. de Market Share "
                    "no período mais recente."
                )

            if perda <= -0.2:

                alertas.append({
                    "nivel": "🟡",
                    "titulo":
                        "Perda recente de Market Share",

                    "texto":
                        f"{maior_perda[col_player]} perdeu "
                        f"{abs(perda):.1f} p.p. de share "
                        "no último período."
                })

# ============================================================
# KPIs DO RADAR
# ============================================================

r1, r2, r3 = st.columns(3)

with r1:
    st.metric(
        "Pontos de atenção",
        len(alertas)
    )

with r2:
    st.metric(
        "Alta prioridade",
        alta_prioridade
    )

with r3:
    st.metric(
        "Oportunidades",
        len(oportunidades)
    )

# ============================================================
# ALERTAS
# ============================================================

if len(alertas) > 0:

    st.warning(
        f"⚠️ {len(alertas)} sinal(is) "
        "identificado(s) pelo radar."
    )

    for alerta in alertas:

        st.markdown(
            f"### {alerta['nivel']} "
            f"{alerta['titulo']}"
        )

        st.write(
            alerta["texto"]
        )

else:

    st.success(
        "🟢 Nenhum sinal crítico identificado."
    )

# ============================================================
# OPORTUNIDADES
# ============================================================

if len(oportunidades) > 0:

    st.markdown("### 🟢 Oportunidades identificadas")

    for oportunidade in oportunidades:
        st.success(
            f"💡 {oportunidade}"
        )

# ============================================================
# IA / PLANOS DE AÇÃO
# ============================================================

st.divider()

st.markdown("## 🧠 Investigação com IA")

st.caption(
    "A camada de IA transforma os sinais encontrados "
    "pelo radar em hipóteses de investigação e possíveis "
    "planos de ação. As recomendações devem ser validadas "
    "com dados de negócio antes da implementação."
)

if st.button("✨ Investigar movimentos"):

    st.markdown("### Recomendações do radar")

    if churn > LIMITE_CHURN:
        st.info(
            "🔎 Retenção: segmentar churn por player, região "
            "e período para localizar onde a perda de clientes "
            "está mais concentrada."
        )

    if nps < META_NPS:
        st.info(
            "🔎 Experiência: cruzar NPS com churn para avaliar "
            "se grupos com pior experiência apresentam maior "
            "saída de clientes."
        )

    if crescimento < META_CRESCIMENTO:
        st.info(
            "🔎 Crescimento: separar aquisição e perda de base "
            "para entender se o resultado está sendo pressionado "
            "por menor entrada ou maior cancelamento."
        )

    if concentracao_top2 >= 60:
        st.info(
            "🔎 Concorrência: acompanhar os movimentos dos "
            "líderes e identificar players menores com ganho "
            "consistente de participação."
        )

    if len(oportunidades) > 0:
        st.success(
            "💡 O radar também identificou movimentos positivos. "
            "Eles podem ser analisados para entender quais práticas "
            "ou segmentos estão contribuindo para o resultado."
        )

# ============================================================
# SOBRE
# ============================================================

st.divider()

with st.expander("ℹ️ Sobre o projeto"):

    st.write(
        """
        Market Pulse AI é um protótipo experimental de
        Inteligência de Mercado desenvolvido para demonstrar
        como dados competitivos podem ser monitorados de forma
        automatizada.

        O radar combina indicadores de Market Share,
        crescimento, churn, NPS e satisfação para identificar
        sinais que merecem investigação.

        Os dados utilizados neste protótipo são sintéticos e
        não representam informações reais das empresas exibidas.
        """
    )
