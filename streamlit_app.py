import streamlit as st
import pandas as pd
import altair as alt
import os
from google import genai
from google.genai import types

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="CONECTA INTELIGÊNC.IA",
    page_icon="✦",
    layout="wide"
)

# ============================================================
# ESTILO
# ============================================================

st.markdown("""
<style>

.block-container {
    padding-top: 1.7rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background-color: #F7F8FA !important;
    border-right: 1px solid #E2E5EA !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #111827 !important;
}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p {
    color: #374151 !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #0E1117 !important;
    border: 1px solid #1F2937 !important;
    border-radius: 8px !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] span {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] div {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] svg {
    color: #CBD5E1 !important;
    fill: #CBD5E1 !important;
}

[data-testid="stSidebar"] hr {
    border-color: #DDE1E7 !important;
}

[data-testid="stSidebar"] [data-testid="stLinkButton"] a {
    background-color: #FFFFFF !important;
    color: #2563EB !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 8px !important;
}

[data-testid="stSidebar"] [data-testid="stLinkButton"] a p {
    color: #2563EB !important;
    font-weight: 600 !important;
}

[data-testid="stMetric"] {
    border: 1px solid rgba(120,120,120,0.22);
    border-radius: 14px;
    padding: 16px;
    background: rgba(120,120,120,0.035);
}

[data-testid="stMetricLabel"] {
    font-weight: 700;
}

[data-testid="stMetricValue"] {
    font-size: 30px;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

h1, h2, h3 {
    letter-spacing: -0.3px;
}

</style>
""", unsafe_allow_html=True)

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

df.columns = [
    str(c).strip().lower().replace(" ", "_")
    for c in df.columns
]

# ============================================================
# LOCALIZAR COLUNAS
# ============================================================

def localizar_coluna(possiveis):
    for nome in possiveis:
        if nome in df.columns:
            return nome

    for coluna in df.columns:
        for nome in possiveis:
            if nome in coluna:
                return coluna

    return None


col_player = localizar_coluna(["player", "operadora", "empresa"])

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

col_nps = localizar_coluna(["nps"])

col_satisfacao = localizar_coluna([
    "satisfacao", "satisfação", "csat"
])

# ============================================================
# CONVERSÃO NUMÉRICA
# ============================================================

for coluna in [
    col_share,
    col_assinantes,
    col_churn,
    col_nps,
    col_satisfacao
]:
    if coluna and coluna in df.columns:
        df[coluna] = pd.to_numeric(
            df[coluna]
            .astype(str)
            .str.replace("%", "", regex=False)
            .str.replace(",", ".", regex=False),
            errors="coerce"
        )

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("✦ CONECTA")
st.sidebar.caption("INTELIGÊNC.IA")
st.sidebar.caption("Market Intelligence Platform")

st.sidebar.divider()
st.sidebar.subheader("🔎 Filtros")

df_filtrado = df.copy()

player_selecionado = "Todos"
regiao_selecionada = "Todas"
periodo_selecionado = "Todos"

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

st.sidebar.divider()

st.sidebar.caption(
    "Os filtros atualizam automaticamente os indicadores."
)

st.sidebar.divider()
st.sidebar.caption("PROJETO AUTORAL")
st.sidebar.markdown("**Fernanda Barbosa**")

st.sidebar.link_button(
    "LinkedIn ↗",
    "https://www.linkedin.com/in/fernanda-barbosa-489148114/",
    use_container_width=True
)

# ============================================================
# BASE HISTÓRICA
# ============================================================

base_historica = df.copy()

if col_player and player_selecionado != "Todos":
    base_historica = base_historica[
        base_historica[col_player].astype(str) == player_selecionado
    ]

if col_regiao and regiao_selecionada != "Todas":
    base_historica = base_historica[
        base_historica[col_regiao].astype(str) == regiao_selecionada
    ]

# ============================================================
# FUNÇÕES
# ============================================================

def media(coluna, base):
    if coluna and coluna in base.columns:
        valor = pd.to_numeric(base[coluna], errors="coerce").mean()

        if pd.notna(valor):
            return float(valor)

    return 0.0


def soma(coluna, base):
    if coluna and coluna in base.columns:
        valor = pd.to_numeric(base[coluna], errors="coerce").sum()

        if pd.notna(valor):
            return float(valor)

    return 0.0


def formatar_base(valor):
    if valor >= 1_000_000_000:
        return f"{valor / 1_000_000_000:.1f} B"

    if valor >= 1_000_000:
        return f"{valor / 1_000_000:.1f} M"

    if valor >= 1_000:
        return f"{valor / 1_000:.1f} mil"

    return f"{valor:,.0f}"


def lista_periodos():
    if not col_periodo:
        return []

    return sorted(
        base_historica[col_periodo]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


def encontrar_periodo_atual():
    lista = lista_periodos()

    if not lista:
        return None

    if periodo_selecionado != "Todos":
        return periodo_selecionado

    return lista[-1]


def encontrar_periodo_anterior(periodo):
    lista = lista_periodos()

    if periodo not in lista:
        return None

    indice = lista.index(periodo)

    if indice == 0:
        return None

    return lista[indice - 1]


def encontrar_periodo_aa(periodo):
    if periodo is None:
        return None

    texto = str(periodo)

    try:
        ano = int(texto[:4])
        candidato = str(ano - 1) + texto[4:]

        if candidato in lista_periodos():
            return candidato

    except Exception:
        pass

    return None


def filtrar_periodo(periodo):
    if not col_periodo or periodo is None:
        return base_historica.copy()

    return base_historica[
        base_historica[col_periodo].astype(str) == str(periodo)
    ].copy()


def variacao_percentual(atual, anterior):
    if anterior is None or anterior == 0:
        return None

    return ((atual - anterior) / anterior) * 100


def variacao_absoluta(atual, anterior):
    if anterior is None:
        return None

    return atual - anterior


def texto_delta(valor, unidade=""):
    if valor is None:
        return "Sem comparação"

    return f"{valor:+.1f}{unidade}"


# ============================================================
# PERÍODOS
# ============================================================

periodo_atual = encontrar_periodo_atual()
periodo_anterior = encontrar_periodo_anterior(periodo_atual)
periodo_aa = encontrar_periodo_aa(periodo_atual)

base_atual = filtrar_periodo(periodo_atual)
base_anterior = filtrar_periodo(periodo_anterior)
base_aa = filtrar_periodo(periodo_aa)

# ============================================================
# INDICADORES
# ============================================================

assinantes = soma(col_assinantes, base_atual)
churn = media(col_churn, base_atual)
nps = media(col_nps, base_atual)
satisfacao = media(col_satisfacao, base_atual)

assinantes_anterior = (
    soma(col_assinantes, base_anterior)
    if periodo_anterior else None
)

assinantes_aa = (
    soma(col_assinantes, base_aa)
    if periodo_aa else None
)

churn_anterior = (
    media(col_churn, base_anterior)
    if periodo_anterior else None
)

churn_aa = (
    media(col_churn, base_aa)
    if periodo_aa else None
)

nps_anterior = (
    media(col_nps, base_anterior)
    if periodo_anterior else None
)

nps_aa = (
    media(col_nps, base_aa)
    if periodo_aa else None
)

satisfacao_anterior = (
    media(col_satisfacao, base_anterior)
    if periodo_anterior else None
)

satisfacao_aa = (
    media(col_satisfacao, base_aa)
    if periodo_aa else None
)

# ============================================================
# CRESCIMENTO
# ============================================================

crescimento = 0.0

if assinantes_anterior is not None and assinantes_anterior != 0:
    crescimento = (
        (assinantes - assinantes_anterior)
        / assinantes_anterior
    ) * 100

# ============================================================
# VARIAÇÕES
# ============================================================

var_base_periodo = variacao_percentual(
    assinantes,
    assinantes_anterior
)

var_base_aa = variacao_percentual(
    assinantes,
    assinantes_aa
)

var_churn_periodo = variacao_absoluta(
    churn,
    churn_anterior
)

var_churn_aa = variacao_absoluta(
    churn,
    churn_aa
)

var_nps_periodo = variacao_absoluta(
    nps,
    nps_anterior
)

var_nps_aa = variacao_absoluta(
    nps,
    nps_aa
)

var_sat_periodo = variacao_absoluta(
    satisfacao,
    satisfacao_anterior
)

var_sat_aa = variacao_absoluta(
    satisfacao,
    satisfacao_aa
)

# ============================================================
# YTD
# ============================================================

ano_atual = None

if periodo_atual:
    try:
        ano_atual = str(periodo_atual)[:4]
    except Exception:
        ano_atual = None

base_ytd = base_historica.copy()

if ano_atual and col_periodo:
    base_ytd = base_historica[
        base_historica[col_periodo]
        .astype(str)
        .str.startswith(ano_atual)
    ].copy()

nps_ytd = media(col_nps, base_ytd)
churn_ytd = media(col_churn, base_ytd)
satisfacao_ytd = media(col_satisfacao, base_ytd)

# ============================================================
# METAS
# ============================================================

META_NPS = 70.0
META_SATISFACAO = 8.0
LIMITE_CHURN = 5.0
META_CRESCIMENTO = 5.0
TOLERANCIA = 0.05

# ============================================================
# MARKET SHARE
# ============================================================

share_player = pd.DataFrame()

if col_player and col_share:
    share_player = (
        base_atual
        .groupby(col_player, as_index=False)[col_share]
        .mean()
        .dropna()
        .sort_values(col_share, ascending=False)
    )

lider_share = "—"
lider_share_valor = 0.0

if not share_player.empty:
    lider_share = str(share_player.iloc[0][col_player])
    lider_share_valor = float(share_player.iloc[0][col_share])

players_monitorados = (
    base_atual[col_player].nunique()
    if col_player else 0
)

concentracao_top2 = 0.0

if len(share_player) >= 2:
    concentracao_top2 = float(
        share_player.iloc[0][col_share]
        + share_player.iloc[1][col_share]
    )

# ============================================================
# MOVIMENTOS DE SHARE
# ============================================================

maior_ganho_nome = None
maior_ganho_valor = 0.0

maior_perda_nome = None
maior_perda_valor = 0.0

comparacao_share = pd.DataFrame()

if col_player and col_share and periodo_anterior is not None:

    share_anterior = (
        base_anterior
        .groupby(col_player, as_index=False)[col_share]
        .mean()
    )

    share_atual_comp = (
        base_atual
        .groupby(col_player, as_index=False)[col_share]
        .mean()
    )

    comparacao_share = share_atual_comp.merge(
        share_anterior,
        on=col_player,
        suffixes=("_atual", "_anterior")
    )

    if not comparacao_share.empty:

        comparacao_share["variacao_pp"] = (
            comparacao_share[f"{col_share}_atual"]
            - comparacao_share[f"{col_share}_anterior"]
        )

        ganho = comparacao_share.loc[
            comparacao_share["variacao_pp"].idxmax()
        ]

        perda = comparacao_share.loc[
            comparacao_share["variacao_pp"].idxmin()
        ]

        maior_ganho_nome = str(ganho[col_player])
        maior_ganho_valor = float(ganho["variacao_pp"])

        maior_perda_nome = str(perda[col_player])
        maior_perda_valor = float(perda["variacao_pp"])

# ============================================================
# CABEÇALHO
# ============================================================

st.markdown(
    """
    <div style="margin-bottom:8px;">
        <span style="
            font-size:38px;
            font-weight:800;
            letter-spacing:-1px;
        ">
            CONECTA INTELIGÊNC.
        </span>
        <span style="
            font-size:38px;
            font-weight:800;
            letter-spacing:-1px;
            background:linear-gradient(
                90deg,
                #6C63FF,
                #00C2FF
            );
            -webkit-background-clip:text;
            -webkit-text-fill-color:transparent;
        ">
            IA
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "**Inteligência de Mercado & Estratégia potencializada por IA**"
)

st.caption(
    "Market Intelligence • Competitive Intelligence • "
    "Customer Experience • Artificial Intelligence"
)

st.markdown("##### Projeto autoral • Fernanda Barbosa")

st.caption(
    "Portfólio profissional • Inteligência de Mercado • "
    "Data Analytics • AI-driven Insights"
)

s1, s2 = st.columns([3, 1])

with s1:
    st.success(
        f"● Monitoramento ativo • "
        f"{len(base_atual):,.0f} registros analisados".replace(",", ".")
    )

with s2:
    if periodo_atual:
        st.info(f"Atualização: {periodo_atual}")

# ============================================================
# GIRO DE INTELIGÊNCIA
# ============================================================

st.divider()

st.caption("GIRO DE INTELIGÊNCIA")
st.header("O que está movimentando o mercado?")

movimentos_giro = []

if churn > LIMITE_CHURN + TOLERANCIA:
    movimentos_giro.append(
        (
            "🔴",
            f"Churn está {churn - LIMITE_CHURN:.1f} p.p. "
            "acima do limite."
        )
    )

if nps < META_NPS - TOLERANCIA:
    movimentos_giro.append(
        (
            "🟡",
            f"NPS está {META_NPS - nps:.0f} pontos "
            "abaixo da meta."
        )
    )

if crescimento < 0:
    movimentos_giro.append(
        (
            "🔴",
            f"Base apresenta retração de "
            f"{abs(crescimento):.1f}% no último período."
        )
    )

elif crescimento < META_CRESCIMENTO - TOLERANCIA:
    movimentos_giro.append(
        (
            "🟡",
            f"Crescimento está "
            f"{META_CRESCIMENTO - crescimento:.1f} p.p. "
            "abaixo da meta."
        )
    )

if maior_ganho_nome and maior_ganho_valor >= 0.1:
    movimentos_giro.append(
        (
            "🟢",
            f"{maior_ganho_nome} avançou "
            f"{maior_ganho_valor:.1f} p.p. em Market Share."
        )
    )

if maior_perda_nome and maior_perda_valor <= -0.1:
    movimentos_giro.append(
        (
            "🔴",
            f"{maior_perda_nome} perdeu "
            f"{abs(maior_perda_valor):.1f} p.p. de Market Share."
        )
    )

if movimentos_giro:

    st.info(
        f"◉ **{len(movimentos_giro)} movimentos "
        "relevantes identificados no período.**"
    )

    for emoji, texto in movimentos_giro:
        st.write(f"{emoji} {texto}")

else:
    st.success(
        "🟢 Nenhum movimento relevante identificado."
    )

# ============================================================
# VISÃO EXECUTIVA
# ============================================================

st.divider()

st.caption("VISÃO EXECUTIVA")
st.header("Indicadores de Mercado")

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.metric(
        "Base monitorada",
        formatar_base(assinantes),
        texto_delta(var_base_periodo, "%")
    )

    if var_base_aa is not None:
        st.caption(
            f"{var_base_aa:+.1f}% vs. mesmo período AA"
        )

with k2:
    st.metric(
        "Churn médio",
        f"{churn:.1f}%",
        texto_delta(var_churn_periodo, " p.p."),
        delta_color="inverse"
    )

    if var_churn_aa is not None:
        st.caption(
            f"{var_churn_aa:+.1f} p.p. vs. AA"
        )

with k3:
    st.metric(
        "NPS",
        f"{nps:.0f}",
        texto_delta(var_nps_periodo, " pts")
    )

    if var_nps_aa is not None:
        st.caption(
            f"{var_nps_aa:+.1f} pts vs. AA"
        )

with k4:
    st.metric(
        "Satisfação",
        f"{satisfacao:.1f}/10",
        texto_delta(var_sat_periodo, " pts")
    )

    if var_sat_aa is not None:
        st.caption(
            f"{var_sat_aa:+.1f} pts vs. AA"
        )

with k5:
    st.metric(
        "Crescimento",
        f"{crescimento:+.1f}%",
        f"{crescimento - META_CRESCIMENTO:+.1f} p.p. vs. meta"
    )

st.write("")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Líder de mercado",
        lider_share,
        f"{lider_share_valor:.1f}% de share"
    )

with c2:
    st.metric(
        "Concentração Top 2",
        f"{concentracao_top2:.1f}%",
        "Participação dos líderes",
        delta_color="off"
    )

with c3:
    st.metric(
        "Players monitorados",
        players_monitorados,
        "Cobertura competitiva",
        delta_color="off"
    )

# ============================================================
# PERFORMANCE
# ============================================================

st.divider()

st.caption("PERFORMANCE")
st.header("Performance & Acumulado do Ano")

p1, p2, p3, p4 = st.columns(4)

with p1:
    st.metric(
        "NPS atual",
        f"{nps:.0f}",
        f"{nps - META_NPS:+.1f} pts vs. meta"
    )

    st.caption(
        f"Acumulado {ano_atual}: {nps_ytd:.1f}"
    )

with p2:
    st.metric(
        "Satisfação atual",
        f"{satisfacao:.1f}",
        f"{satisfacao - META_SATISFACAO:+.1f} pt vs. meta"
    )

    st.caption(
        f"Acumulado {ano_atual}: {satisfacao_ytd:.1f}"
    )

with p3:
    st.metric(
        "Churn atual",
        f"{churn:.1f}%",
        f"{churn - LIMITE_CHURN:+.1f} p.p. vs. limite",
        delta_color="inverse"
    )

    st.caption(
        f"Média {ano_atual}: {churn_ytd:.1f}%"
    )

with p4:
    st.metric(
        "Crescimento da base",
        f"{crescimento:+.1f}%",
        f"{crescimento - META_CRESCIMENTO:+.1f} p.p. vs. meta"
    )

    st.caption(
        "Variação vs. período anterior"
    )

# ============================================================
# MONITORAMENTO COMPETITIVO
# ============================================================

st.divider()

st.caption("MERCADO & CONCORRÊNCIA")
st.header("Monitoramento Competitivo")

if col_player and col_share and not share_player.empty:

    st.subheader("Market Share por Player")

    barras = alt.Chart(
        share_player
    ).mark_bar(
        cornerRadiusTopLeft=5,
        cornerRadiusTopRight=5
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

    st.altair_chart(
        (barras + textos).properties(height=320),
        use_container_width=True
    )

# ============================================================
# EVOLUÇÃO DE SHARE
# ============================================================

if col_player and col_periodo and col_share:

    st.subheader("Evolução de Market Share")

    evolucao = (
        base_historica
        .groupby(
            [col_periodo, col_player],
            as_index=False
        )[col_share]
        .mean()
        .dropna()
    )

    if not evolucao.empty:

        minimo_share = evolucao[col_share].min()
        maximo_share = evolucao[col_share].max()

        margem = max(
            (maximo_share - minimo_share) * 0.18,
            1.5
        )

        y_min = max(0, minimo_share - margem)
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

        st.altair_chart(
            (linha + rotulos).properties(height=430),
            use_container_width=True
        )

# ============================================================
# RADAR DE OPORTUNIDADES
# ============================================================

st.divider()

st.caption("RADAR CONECTA")
st.header("Radar de Oportunidades")

st.caption(
    "O radar procura movimentos positivos, vantagens "
    "competitivas e espaços que merecem investigação."
)

oportunidades = []

if maior_ganho_nome and maior_ganho_valor > 0:
    oportunidades.append(
        {
            "titulo": "Ganho competitivo",
            "texto":
                f"{maior_ganho_nome} apresentou avanço de "
                f"{maior_ganho_valor:.1f} p.p. em Market Share. "
                "O movimento pode indicar ganho de competitividade "
                "e merece investigação."
        }
    )

if col_player and col_churn:

    churn_players = (
        base_atual
        .groupby(col_player)[col_churn]
        .mean()
        .dropna()
        .sort_values()
    )

    if not churn_players.empty:

        melhor_player_churn = str(
            churn_players.index[0]
        )

        melhor_churn = float(
            churn_players.iloc[0]
        )

        if melhor_churn < churn:
            oportunidades.append(
                {
                    "titulo": "Referência em retenção",
                    "texto":
                        f"{melhor_player_churn} apresenta churn "
                        f"de {melhor_churn:.1f}%, abaixo da média "
                        f"monitorada de {churn:.1f}%. Vale investigar "
                        "quais fatores diferenciam esse player."
                }
            )

if col_player and col_nps:

    nps_players = (
        base_atual
        .groupby(col_player)[col_nps]
        .mean()
        .dropna()
        .sort_values(ascending=False)
    )

    if not nps_players.empty:

        melhor_player_nps = str(
            nps_players.index[0]
        )

        melhor_nps = float(
            nps_players.iloc[0]
        )

        if melhor_nps > nps:
            oportunidades.append(
                {
                    "titulo": "Benchmark de experiência",
                    "texto":
                        f"{melhor_player_nps} registra NPS de "
                        f"{melhor_nps:.0f}, acima da média monitorada "
                        f"de {nps:.0f}. O resultado pode servir como "
                        "benchmark competitivo."
                }
            )

if col_player and col_satisfacao:

    sat_players = (
        base_atual
        .groupby(col_player)[col_satisfacao]
        .mean()
        .dropna()
        .sort_values(ascending=False)
    )

    if not sat_players.empty:

        melhor_player_sat = str(
            sat_players.index[0]
        )

        melhor_sat = float(
            sat_players.iloc[0]
        )

        if melhor_sat > satisfacao:
            oportunidades.append(
                {
                    "titulo": "Destaque em satisfação",
                    "texto":
                        f"{melhor_player_sat} apresenta satisfação "
                        f"de {melhor_sat:.1f}/10, acima da média "
                        f"monitorada de {satisfacao:.1f}/10."
                }
            )

if concentracao_top2 < 65:
    oportunidades.append(
        {
            "titulo": "Espaço competitivo",
            "texto":
                f"Os dois líderes concentram {concentracao_top2:.1f}% "
                "do mercado monitorado. A participação restante pode "
                "representar espaço relevante para movimentos dos "
                "demais players."
        }
    )

r1, r2, r3 = st.columns(3)

with r1:
    st.metric(
        "Oportunidades mapeadas",
        len(oportunidades)
    )

with r2:
    st.metric(
        "Maior ganho de share",
        maior_ganho_nome if maior_ganho_nome else "—",
        (
            f"{maior_ganho_valor:+.1f} p.p."
            if maior_ganho_nome
            else "Sem movimento"
        )
    )

with r3:
    st.metric(
        "Espaço fora do Top 2",
        f"{100 - concentracao_top2:.1f}%",
        "Participação dos demais players",
        delta_color="off"
    )

if oportunidades:

    for oportunidade in oportunidades:
        st.success(
            f"💡 **{oportunidade['titulo']}**\n\n"
            f"{oportunidade['texto']}"
        )

else:
    st.info(
        "🔎 Nenhuma oportunidade relevante foi identificada "
        "com os critérios atuais."
    )

# ============================================================
# CONECTA IA — GEMINI
# ============================================================

st.divider()

st.caption("INTELIGÊNCIA ARTIFICIAL")
st.header("✦ CONECTA IA")

st.markdown(
    "**Seu copiloto de Inteligência de Mercado**"
)

st.caption(
    "Converse com os dados monitorados, investigue movimentos "
    "competitivos e transforme indicadores em hipóteses de análise."
)

# ============================================================
# CONTEXTO DOS DADOS PARA A IA
# ============================================================

dados_players_ia = []

if (
    col_player
    and col_share
    and col_churn
    and col_nps
    and col_satisfacao
):

    resumo_players = (
        base_atual
        .groupby(col_player)
        .agg({
            col_share: "mean",
            col_churn: "mean",
            col_nps: "mean",
            col_satisfacao: "mean"
        })
        .reset_index()
    )

    for _, linha_player in resumo_players.iterrows():

        nome_player = str(
            linha_player[col_player]
        )

        share_p = float(
            linha_player[col_share]
        )

        churn_p = float(
            linha_player[col_churn]
        )

        nps_p = float(
            linha_player[col_nps]
        )

        sat_p = float(
            linha_player[col_satisfacao]
        )

        dados_players_ia.append(
            f"{nome_player}: "
            f"Market Share {share_p:.1f}%; "
            f"Churn {churn_p:.1f}%; "
            f"NPS {nps_p:.0f}; "
            f"Satisfação {sat_p:.1f}/10."
        )

contexto_players = "\n".join(dados_players_ia)

contexto_oportunidades = "\n".join(
    [
        f"- {item['titulo']}: {item['texto']}"
        for item in oportunidades
    ]
)

contexto_movimentos = "\n".join(
    [
        f"- {texto}"
        for _, texto in movimentos_giro
    ]
)

contexto_ia = f"""
CONTEXTO DO DASHBOARD CONECTA INTELIGÊNC.IA

IMPORTANTE:
Todos os dados abaixo são sintéticos e pertencem exclusivamente
ao protótipo CONECTA INTELIGÊNC.IA.

RECORTE ATUAL:
Player selecionado: {player_selecionado}
Região selecionada: {regiao_selecionada}
Período analisado: {periodo_atual}
Período anterior: {periodo_anterior}

INDICADORES:
Base monitorada: {formatar_base(assinantes)}
Churn médio: {churn:.1f}%
NPS: {nps:.0f}
Satisfação: {satisfacao:.1f}/10
Crescimento da base: {crescimento:+.1f}%

METAS DO PROTÓTIPO:
Meta NPS: {META_NPS:.0f}
Meta de satisfação: {META_SATISFACAO:.1f}
Limite de churn: {LIMITE_CHURN:.1f}%
Meta de crescimento: {META_CRESCIMENTO:.1f}%

MERCADO:
Líder de mercado: {lider_share}
Share do líder: {lider_share_valor:.1f}%
Concentração Top 2: {concentracao_top2:.1f}%
Players monitorados: {players_monitorados}

MAIOR MOVIMENTO POSITIVO DE SHARE:
{maior_ganho_nome if maior_ganho_nome else "Não identificado"}
{maior_ganho_valor:+.1f} p.p.

MAIOR MOVIMENTO NEGATIVO DE SHARE:
{maior_perda_nome if maior_perda_nome else "Não identificado"}
{maior_perda_valor:+.1f} p.p.

INDICADORES POR PLAYER:
{contexto_players if contexto_players else "Não disponível."}

MOVIMENTOS IDENTIFICADOS:
{contexto_movimentos if contexto_movimentos else "Nenhum movimento relevante."}

OPORTUNIDADES IDENTIFICADAS:
{contexto_oportunidades if contexto_oportunidades else "Nenhuma oportunidade automática identificada."}
"""

# ============================================================
# CONTEXTO ATUAL
# ============================================================

st.info(
    f"🔎 **Contexto atual:** "
    f"{player_selecionado} • "
    f"{regiao_selecionada} • "
    f"{periodo_atual}"
)

# ============================================================
# ATALHOS
# ============================================================

st.caption("Sugestões rápidas")

a1, a2, a3, a4 = st.columns(4)

pergunta_atalho = None

with a1:
    if st.button(
        "✨ Gerar insights",
        use_container_width=True
    ):
        pergunta_atalho = (
            "Quais são os principais insights deste cenário? "
            "Priorize os movimentos mais relevantes."
        )

with a2:
    if st.button(
        "⚠️ Analisar riscos",
        use_container_width=True
    ):
        pergunta_atalho = (
            "Quais são os principais riscos observados nos dados "
            "e o que deveria ser investigado primeiro?"
        )

with a3:
    if st.button(
        "💡 Oportunidades",
        use_container_width=True
    ):
        pergunta_atalho = (
            "Quais oportunidades de mercado e de performance "
            "podem ser investigadas com base nesses dados?"
        )

with a4:
    if st.button(
        "🏆 Comparar players",
        use_container_width=True
    ):
        pergunta_atalho = (
            "Compare os players monitorados considerando "
            "Market Share, churn, NPS e satisfação."
        )

# ============================================================
# HISTÓRICO DO CHAT
# ============================================================

if "mensagens_conecta" not in st.session_state:
    st.session_state.mensagens_conecta = []

for mensagem in st.session_state.mensagens_conecta:

    with st.chat_message(
        mensagem["role"]
    ):
        st.markdown(
            mensagem["content"]
        )

# ============================================================
# CAMPO DE PERGUNTA
# ============================================================

with st.form("form_conecta_ia", clear_on_submit=True):
    pergunta_digitada = st.text_input(
        "Converse com o CONECTA IA",
        placeholder="Pergunte sobre os dados monitorados...",
        key="pergunta_conecta_ia"
    )

    enviar_pergunta = st.form_submit_button(
        "Enviar para o CONECTA IA ✦",
        use_container_width=True
    )

pergunta = pergunta_atalho or (
    pergunta_digitada.strip()
    if enviar_pergunta and pergunta_digitada.strip()
    else None
)

# ============================================================
# INSTRUÇÕES DO CONECTA IA
# ============================================================

instrucoes_ia = """
Você é o CONECTA IA, copiloto de Inteligência de Mercado
do projeto CONECTA INTELIGÊNC.IA.

Sua função é interpretar exclusivamente os dados sintéticos
fornecidos pelo dashboard.

REGRAS:

1. Os players e indicadores apresentados fazem parte de um
protótipo com dados sintéticos.

2. Não utilize conhecimento externo para atribuir fatos reais
às empresas ou players citados.

3. Mesmo que algum nome coincida com uma empresa real,
considere somente os dados fornecidos pelo CONECTA.

4. Nunca invente números.

5. Diferencie claramente evidência observada, hipótese de
investigação e próximo passo.

6. Correlação não significa causalidade.

7. Se os dados não forem suficientes, diga claramente que a
informação não está disponível no conjunto analisado.

8. Responda em português do Brasil.

9. Seja executivo, objetivo e analítico.

10. Sempre que possível, sustente a análise com os números
fornecidos pelo dashboard.

11. Não diga que possui acesso à internet ou dados externos.

12. Se perguntarem sobre mercado real ou informações externas,
explique que a análise está limitada à base sintética monitorada
pelo CONECTA INTELIGÊNC.IA.

Quando fizer sentido, organize a resposta em:

**Leitura da IA**
Síntese objetiva.

**Evidências nos dados**
Números que sustentam a leitura.

**Hipóteses para investigação**
Possíveis explicações tratadas explicitamente como hipóteses.

**Próximo passo**
Análise recomendada.
"""

# ============================================================
# CONSULTA AO GEMINI
# ============================================================

if pergunta:

    st.session_state.mensagens_conecta.append(
        {
            "role": "user",
            "content": pergunta
        }
    )

    with st.chat_message("user"):
        st.markdown(pergunta)

    with st.chat_message("assistant"):

        with st.spinner(
            "CONECTA IA está analisando os dados..."
        ):

            try:

                if "GEMINI_API_KEY" not in st.secrets:

                    st.error(
                        "A chave GEMINI_API_KEY não foi encontrada "
                        "nos Secrets do Streamlit."
                    )

                else:

                    client = genai.Client(
                        api_key=st.secrets["GEMINI_API_KEY"]
                    )

                    historico_recente = ""

                    for msg in st.session_state.mensagens_conecta[-6:]:

                        autor = (
                            "Usuário"
                            if msg["role"] == "user"
                            else "CONECTA IA"
                        )

                        historico_recente += (
                            f"\n{autor}: {msg['content']}\n"
                        )

                    prompt_completo = f"""
{contexto_ia}

HISTÓRICO RECENTE DA CONVERSA:
{historico_recente}

PERGUNTA DO USUÁRIO:
{pergunta}
"""

                    resposta = client.models.generate_content(
                        model="gemini-3.5-flash-lite",
                        contents=prompt_completo,
                        config=types.GenerateContentConfig(
                            system_instruction=instrucoes_ia,
                            max_output_tokens=700
                        )
                    )

                    texto_resposta = resposta.text

                    if texto_resposta:

                        st.markdown(texto_resposta)

                        st.session_state.mensagens_conecta.append(
                            {
                                "role": "assistant",
                                "content": texto_resposta
                            }
                        )

                    else:

                        st.warning(
                            "O CONECTA IA não retornou uma resposta "
                            "para esta consulta."
                        )

            except Exception as erro:

                st.error(
                    "Não consegui consultar o CONECTA IA neste momento."
                )

                st.caption(
                    f"Detalhe técnico: {erro}"
                )

# ============================================================
# LIMPAR CONVERSA
# ============================================================

if st.session_state.mensagens_conecta:

    if st.button(
        "🗑️ Limpar conversa"
    ):
        st.session_state.mensagens_conecta = []
        st.rerun()

st.caption(
    "O CONECTA IA interpreta exclusivamente os dados sintéticos "
    "disponíveis neste protótipo. As respostas representam "
    "hipóteses analíticas e não dados externos de mercado."
)

# ============================================================
# SOBRE
# ============================================================

st.divider()

with st.expander(
    "ℹ️ Sobre o CONECTA INTELIGÊNC.IA",
    expanded=False
):

    st.markdown(
        """
### Projeto autoral por Fernanda Barbosa

**CONECTA INTELIGÊNC.IA** é um projeto autoral criado e
desenvolvido por **Fernanda Barbosa**, com o objetivo de
explorar como **Inteligência de Mercado, análise de dados e
Inteligência Artificial** podem ser conectadas em uma única
solução para monitoramento e leitura de mercado.

A plataforma conecta indicadores de **mercado, concorrência,
experiência e performance** para identificar movimentos,
riscos e oportunidades.

O **Giro de Inteligência** resume os principais movimentos
identificados no período.

O **Radar CONECTA** identifica oportunidades, benchmarks e
sinais competitivos que merecem investigação.

O **CONECTA IA** funciona como um copiloto de Inteligência
de Mercado, permitindo conversar com os indicadores do
protótipo e transformar dados em leituras, hipóteses e
próximos passos de investigação.

Este projeto integra o **portfólio profissional de
Fernanda Barbosa** e foi desenvolvido como demonstração
prática da aplicação de Inteligência de Mercado,
Data Analytics e Inteligência Artificial.

---

**Nota:** os dados utilizados neste protótipo são sintéticos
e não representam informações reais das empresas exibidas.
        """
    )

st.caption(
    "CONECTA INTELIGÊNC.IA • Projeto autoral por Fernanda Barbosa • 2026"
)
