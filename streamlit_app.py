import streamlit as st
import pandas as pd
import altair as alt
import os
import math

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="CONECTA INTELIGÊNC.IA",
    page_icon="◉",
    layout="wide"
)

# ============================================================
# IDENTIDADE VISUAL
# ============================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(120,120,120,0.18);
    }

    .conecta-brand {
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 4px;
        opacity: 0.75;
        margin-bottom: 2px;
    }

    .conecta-title {
        font-size: 43px;
        font-weight: 800;
        line-height: 1.05;
        margin-bottom: 5px;
    }

    .conecta-title span {
        background: linear-gradient(
            90deg,
            #7C4DFF,
            #00B8D9
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .conecta-subtitle {
        font-size: 17px;
        opacity: 0.72;
        margin-top: 6px;
        margin-bottom: 4px;
    }

    .conecta-tag {
        display: inline-block;
        padding: 5px 11px;
        border-radius: 20px;
        background: rgba(124,77,255,0.12);
        font-size: 12px;
        font-weight: 600;
        margin-top: 8px;
    }

    .section-label {
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        opacity: 0.6;
        margin-bottom: 5px;
    }

    .giro-box {
        border: 1px solid rgba(124,77,255,0.35);
        border-radius: 16px;
        padding: 20px 22px;
        background:
            linear-gradient(
                135deg,
                rgba(124,77,255,0.10),
                rgba(0,184,217,0.05)
            );
        margin-top: 10px;
        margin-bottom: 22px;
    }

    .giro-title {
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 1.8px;
        margin-bottom: 9px;
    }

    .giro-main {
        font-size: 23px;
        font-weight: 750;
        line-height: 1.3;
        margin-bottom: 7px;
    }

    .giro-text {
        font-size: 14px;
        opacity: 0.75;
        line-height: 1.6;
    }

    .kpi-card {
        border: 1px solid rgba(120,120,120,0.22);
        border-radius: 15px;
        padding: 17px 17px 15px 17px;
        min-height: 165px;
        background: rgba(120,120,120,0.035);
        margin-bottom: 8px;
    }

    .kpi-name {
        font-size: 11px;
        font-weight: 750;
        letter-spacing: 0.9px;
        opacity: 0.65;
        text-transform: uppercase;
    }

    .kpi-value {
        font-size: 31px;
        font-weight: 800;
        margin-top: 7px;
        margin-bottom: 8px;
    }

    .kpi-line {
        font-size: 12px;
        line-height: 1.6;
        opacity: 0.78;
    }

    .positive {
        color: #21c58b;
        font-weight: 700;
    }

    .negative {
        color: #ff5c73;
        font-weight: 700;
    }

    .neutral {
        opacity: 0.75;
        font-weight: 650;
    }

    .status-good {
        display: inline-block;
        margin-top: 9px;
        font-size: 11px;
        font-weight: 750;
        padding: 4px 8px;
        border-radius: 12px;
        background: rgba(33,197,139,0.13);
        color: #21c58b;
    }

    .status-warning {
        display: inline-block;
        margin-top: 9px;
        font-size: 11px;
        font-weight: 750;
        padding: 4px 8px;
        border-radius: 12px;
        background: rgba(255,181,71,0.13);
        color: #ffb547;
    }

    .status-critical {
        display: inline-block;
        margin-top: 9px;
        font-size: 11px;
        font-weight: 750;
        padding: 4px 8px;
        border-radius: 12px;
        background: rgba(255,92,115,0.13);
        color: #ff5c73;
    }

    .mini-card {
        border: 1px solid rgba(120,120,120,0.18);
        border-radius: 14px;
        padding: 15px;
        min-height: 115px;
        background: rgba(120,120,120,0.025);
    }

    .mini-name {
        font-size: 11px;
        font-weight: 700;
        opacity: 0.65;
        text-transform: uppercase;
    }

    .mini-value {
        font-size: 23px;
        font-weight: 800;
        margin-top: 5px;
    }

    .mini-text {
        font-size: 12px;
        opacity: 0.7;
        margin-top: 5px;
    }

    </style>
    """,
    unsafe_allow_html=True
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
# PADRONIZAÇÃO
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
# CONVERSÃO NUMÉRICA
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
# PERÍODO AUXILIAR
# ============================================================

if col_periodo:
    df["_periodo_texto"] = df[col_periodo].astype(str)

    try:
        df["_periodo_data"] = pd.to_datetime(
            df[col_periodo].astype(str),
            errors="coerce"
        )
    except Exception:
        df["_periodo_data"] = pd.NaT

# ============================================================
# FILTROS
# ============================================================

st.sidebar.markdown("## CONECTA")
st.sidebar.caption("Inteligência de Mercado & Estratégia")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔎 Filtros")

df_filtrado = df.copy()

player_selecionado = "Todos"
regiao_selecionada = "Todas"
periodo_selecionado = "Todos"

if col_player:

    players = sorted(
        df[col_player]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    player_selecionado = st.sidebar.selectbox(
        "Player",
        ["Todos"] + players
    )

    if player_selecionado != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado[col_player].astype(str)
            == player_selecionado
        ]


if col_regiao:

    regioes = sorted(
        df[col_regiao]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    regiao_selecionada = st.sidebar.selectbox(
        "Região",
        ["Todas"] + regioes
    )

    if regiao_selecionada != "Todas":
        df_filtrado = df_filtrado[
            df_filtrado[col_regiao].astype(str)
            == regiao_selecionada
        ]


if col_periodo:

    periodos = sorted(
        df[col_periodo]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    periodo_selecionado = st.sidebar.selectbox(
        "Período",
        ["Todos"] + periodos
    )

    if periodo_selecionado != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado[col_periodo].astype(str)
            == periodo_selecionado
        ]

# ============================================================
# BASE HISTÓRICA COM FILTRO DE PLAYER E REGIÃO
# ============================================================

base_historica = df.copy()

if col_player and player_selecionado != "Todos":
    base_historica = base_historica[
        base_historica[col_player].astype(str)
        == player_selecionado
    ]

if col_regiao and regiao_selecionada != "Todas":
    base_historica = base_historica[
        base_historica[col_regiao].astype(str)
        == regiao_selecionada
    ]

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


def formatar_milhoes(valor):

    if abs(valor) >= 1_000_000_000:
        return f"{valor / 1_000_000_000:.1f} B"

    if abs(valor) >= 1_000_000:
        return f"{valor / 1_000_000:.1f} M"

    if abs(valor) >= 1_000:
        return f"{valor / 1_000:.1f} mil"

    return f"{valor:,.0f}"


def classe_variacao(valor, inverso=False):

    if abs(valor) < 0.05:
        return "neutral"

    if inverso:
        return "positive" if valor < 0 else "negative"

    return "positive" if valor > 0 else "negative"


def seta(valor):

    if valor > 0.05:
        return "▲"

    if valor < -0.05:
        return "▼"

    return "●"


def periodo_referencia():

    if not col_periodo:
        return None

    if periodo_selecionado != "Todos":
        return periodo_selecionado

    lista = sorted(
        base_historica[col_periodo]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    if lista:
        return lista[-1]

    return None


def base_do_periodo(periodo):

    if not col_periodo or periodo is None:
        return base_historica.copy()

    return base_historica[
        base_historica[col_periodo].astype(str)
        == str(periodo)
    ].copy()


def lista_periodos_historicos():

    if not col_periodo:
        return []

    return sorted(
        base_historica[col_periodo]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


def encontrar_periodo_anterior(periodo_atual):

    lista = lista_periodos_historicos()

    if str(periodo_atual) not in lista:
        return None

    indice = lista.index(str(periodo_atual))

    if indice <= 0:
        return None

    return lista[indice - 1]


def encontrar_periodo_aa(periodo_atual):

    if periodo_atual is None:
        return None

    texto = str(periodo_atual)

    try:
        data_atual = pd.to_datetime(texto)

        data_aa = data_atual - pd.DateOffset(years=1)

        candidatos = lista_periodos_historicos()

        for candidato in candidatos:

            try:
                data_candidato = pd.to_datetime(candidato)

                if (
                    data_candidato.year == data_aa.year
                    and data_candidato.month == data_aa.month
                ):
                    return candidato

            except Exception:
                pass

    except Exception:
        pass

    # fallback para formatos tipo 2026-08
    try:

        if len(texto) >= 7:

            ano = int(texto[:4])
            resto = texto[4:]

            candidato = str(ano - 1) + resto

            if candidato in lista_periodos_historicos():
                return candidato

    except Exception:
        pass

    return None


def indicador_periodo(coluna, periodo, tipo="media"):

    if periodo is None:
        return None

    base = base_do_periodo(periodo)

    if base.empty or not coluna:
        return None

    serie = pd.to_numeric(
        base[coluna],
        errors="coerce"
    )

    if serie.dropna().empty:
        return None

    if tipo == "soma":
        return float(serie.sum())

    return float(serie.mean())


def variacao_percentual(atual, anterior):

    if atual is None or anterior is None:
        return None

    if anterior == 0:
        return None

    return ((atual - anterior) / anterior) * 100


def variacao_absoluta(atual, anterior):

    if atual is None or anterior is None:
        return None

    return atual - anterior


# ============================================================
# DEFINIÇÃO DOS PERÍODOS DE COMPARAÇÃO
# ============================================================

periodo_atual = periodo_referencia()
periodo_anterior = encontrar_periodo_anterior(periodo_atual)
periodo_aa = encontrar_periodo_aa(periodo_atual)

base_atual = base_do_periodo(periodo_atual)

# ============================================================
# INDICADORES DO PERÍODO ATUAL
# ============================================================

assinantes = soma(
    col_assinantes,
    base_atual
)

churn = media(
    col_churn,
    base_atual
)

nps = media(
    col_nps,
    base_atual
)

satisfacao = media(
    col_satisfacao,
    base_atual
)

players_monitorados = (
    base_atual[col_player].nunique()
    if col_player
    else 0
)

# ============================================================
# VALORES ANTERIORES
# ============================================================

assinantes_anterior = indicador_periodo(
    col_assinantes,
    periodo_anterior,
    "soma"
)

assinantes_aa = indicador_periodo(
    col_assinantes,
    periodo_aa,
    "soma"
)

churn_anterior = indicador_periodo(
    col_churn,
    periodo_anterior
)

churn_aa = indicador_periodo(
    col_churn,
    periodo_aa
)

nps_anterior = indicador_periodo(
    col_nps,
    periodo_anterior
)

nps_aa = indicador_periodo(
    col_nps,
    periodo_aa
)

satisfacao_anterior = indicador_periodo(
    col_satisfacao,
    periodo_anterior
)

satisfacao_aa = indicador_periodo(
    col_satisfacao,
    periodo_aa
)

# ============================================================
# CRESCIMENTO DA BASE
# ============================================================

crescimento = 0.0

if (
    assinantes_anterior is not None
    and assinantes_anterior != 0
):

    crescimento = (
        (assinantes - assinantes_anterior)
        / assinantes_anterior
    ) * 100

# ============================================================
# VARIAÇÕES
# ============================================================

var_assinantes_periodo = variacao_percentual(
    assinantes,
    assinantes_anterior
)

var_assinantes_aa = variacao_percentual(
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

var_satisfacao_periodo = variacao_absoluta(
    satisfacao,
    satisfacao_anterior
)

var_satisfacao_aa = variacao_absoluta(
    satisfacao,
    satisfacao_aa
)

# ============================================================
# METAS
# ============================================================

META_NPS = 70.0
META_SATISFACAO = 8.0
LIMITE_CHURN = 5.0
META_CRESCIMENTO = 5.0

# tolerância para evitar 8.0 aparecer abaixo de 8.0
TOLERANCIA = 0.05

# ============================================================
# MARKET SHARE ATUAL
# ============================================================

share_player = pd.DataFrame()

if col_player and col_share:

    share_player = (
        base_atual
        .groupby(
            col_player,
            as_index=False
        )[col_share]
        .mean()
        .dropna()
        .sort_values(
            col_share,
            ascending=False
        )
    )

lider_share = None
lider_share_valor = 0.0

if not share_player.empty:

    lider_share = share_player.iloc[0][col_player]

    lider_share_valor = float(
        share_player.iloc[0][col_share]
    )

# ============================================================
# CONCENTRAÇÃO
# ============================================================

concentracao_top2 = 0.0

if len(share_player) >= 2:

    concentracao_top2 = float(
        share_player.iloc[0][col_share]
        + share_player.iloc[1][col_share]
    )

# ============================================================
# MOVIMENTOS DE SHARE
# ============================================================

comparacao_share = pd.DataFrame()
maior_ganho_nome = None
maior_ganho_valor = 0.0
maior_perda_nome = None
maior_perda_valor = 0.0

if (
    col_player
    and col_share
    and periodo_anterior is not None
):

    share_anterior = (
        base_do_periodo(periodo_anterior)
        .groupby(
            col_player,
            as_index=False
        )[col_share]
        .mean()
    )

    share_atual_comp = (
        base_atual
        .groupby(
            col_player,
            as_index=False
        )[col_share]
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

        maior_ganho = comparacao_share.loc[
            comparacao_share["variacao_pp"].idxmax()
        ]

        maior_perda = comparacao_share.loc[
            comparacao_share["variacao_pp"].idxmin()
        ]

        maior_ganho_nome = maior_ganho[col_player]
        maior_ganho_valor = float(
            maior_ganho["variacao_pp"]
        )

        maior_perda_nome = maior_perda[col_player]
        maior_perda_valor = float(
            maior_perda["variacao_pp"]
        )

# ============================================================
# CABEÇALHO
# ============================================================

st.markdown(
    """
    <div class="conecta-brand">
        CONECTA
    </div>

    <div class="conecta-title">
        INTELIGÊNC<span>.IA</span>
    </div>

    <div class="conecta-subtitle">
        Inteligência de Mercado & Estratégia potencializada por IA
    </div>

    <div class="conecta-tag">
        Market Intelligence Platform
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# ============================================================
# STATUS / ÚLTIMA ATUALIZAÇÃO
# ============================================================

c1, c2 = st.columns([3, 1])

with c1:

    st.caption(
        f"● Monitoramento ativo  |  "
        f"{len(base_atual):,.0f} registros analisados"
        .replace(",", ".")
    )

with c2:

    if periodo_atual:
        st.caption(
            f"Última atualização: {periodo_atual}"
        )

# ============================================================
# GIRO DE INTELIGÊNCIA
# ============================================================

sinais_giro = []

if churn > LIMITE_CHURN + TOLERANCIA:
    sinais_giro.append(
        f"churn está {churn - LIMITE_CHURN:.1f} p.p. acima do limite"
    )

if nps < META_NPS - TOLERANCIA:
    sinais_giro.append(
        f"NPS está {META_NPS - nps:.0f} pontos abaixo da meta"
    )

if crescimento < META_CRESCIMENTO - TOLERANCIA:
    sinais_giro.append(
        f"crescimento está {META_CRESCIMENTO - crescimento:.1f} p.p. abaixo da meta"
    )

if maior_perda_nome and maior_perda_valor <= -0.1:
    sinais_giro.append(
        f"{maior_perda_nome} perdeu {abs(maior_perda_valor):.1f} p.p. de share"
    )

if maior_ganho_nome and maior_ganho_valor >= 0.1:
    sinais_giro.append(
        f"{maior_ganho_nome} avançou {maior_ganho_valor:.1f} p.p. em share"
    )

quantidade_sinais = len(sinais_giro)

if quantidade_sinais > 0:

    destaque_giro = (
        f"{quantidade_sinais} movimentos merecem atenção "
        f"no período monitorado."
    )

    texto_giro = " • ".join(
        sinais_giro[:4]
    )

else:

    destaque_giro = (
        "Indicadores seguem sem movimentos críticos "
        "no período monitorado."
    )

    texto_giro = (
        "O radar continua acompanhando alterações "
        "de mercado, experiência e retenção."
    )

st.markdown(
    f"""
    <div class="giro-box">

        <div class="giro-title">
            ◉ GIRO DE INTELIGÊNCIA
        </div>

        <div class="giro-main">
            {destaque_giro}
        </div>

        <div class="giro-text">
            {texto_giro}
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# FUNÇÃO PARA CARD KPI
# ============================================================


def card_kpi(
    nome,
    valor,
    variacao_periodo=None,
    variacao_aa=None,
    unidade_periodo="",
    unidade_aa="",
    inverso=False,
    status="",
    status_tipo="warning"
):

    if variacao_periodo is None:

        linha_periodo = (
            '<span class="neutral">'
            '● Comparação anterior indisponível'
            '</span>'
        )

    else:

        classe = classe_variacao(
            variacao_periodo,
            inverso
        )

        linha_periodo = (
            f'<span class="{classe}">'
            f'{seta(variacao_periodo)} '
            f'{variacao_periodo:+.1f}{unidade_periodo}'
            f'</span> vs. período anterior'
        )

    if variacao_aa is None:

        linha_aa = (
            '<span class="neutral">'
            '● Comparação AA indisponível'
            '</span>'
        )

    else:

        classe_aa = classe_variacao(
            variacao_aa,
            inverso
        )

        linha_aa = (
            f'<span class="{classe_aa}">'
            f'{seta(variacao_aa)} '
            f'{variacao_aa:+.1f}{unidade_aa}'
            f'</span> vs. mesmo período AA'
        )

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-name">
                {nome}
            </div>

            <div class="kpi-value">
                {valor}
            </div>

            <div class="kpi-line">
                {linha_periodo}
            </div>

            <div class="kpi-line">
                {linha_aa}
            </div>

            <div class="status-{status_tipo}">
                {status}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# VISÃO EXECUTIVA
# ============================================================

st.markdown(
    '<div class="section-label">VISÃO EXECUTIVA</div>',
    unsafe_allow_html=True
)

st.markdown("## Indicadores de Mercado")

k1, k2, k3, k4, k5 = st.columns(5)

# ASSINANTES
with k1:

    status_assinantes = (
        "Base em expansão"
        if crescimento >= 0
        else "Base em retração"
    )

    tipo_assinantes = (
        "good"
        if crescimento >= 0
        else "warning"
    )

    card_kpi(
        "Base monitorada",
        formatar_milhoes(assinantes),
        var_assinantes_periodo,
        var_assinantes_aa,
        "%",
        "%",
        False,
        status_assinantes,
        tipo_assinantes
    )

# CHURN
with k2:

    if churn <= LIMITE_CHURN + TOLERANCIA:
        status_churn = "Dentro do limite"
        tipo_churn = "good"
    else:
        status_churn = "Acima do limite"
        tipo_churn = "critical"

    card_kpi(
        "Churn médio",
        f"{churn:.1f}%",
        var_churn_periodo,
        var_churn_aa,
        " p.p.",
        " p.p.",
        True,
        status_churn,
        tipo_churn
    )

# NPS
with k3:

    if nps >= META_NPS - TOLERANCIA:
        status_nps = "Meta atingida"
        tipo_nps = "good"
    else:
        status_nps = "Abaixo da meta"
        tipo_nps = "warning"

    card_kpi(
        "NPS",
        f"{nps:.0f}",
        var_nps_periodo,
        var_nps_aa,
        " pts",
        " pts",
        False,
        status_nps,
        tipo_nps
    )

# SATISFAÇÃO
with k4:

    if satisfacao >= META_SATISFACAO - TOLERANCIA:
        status_sat = "Meta atingida"
        tipo_sat = "good"
    else:
        status_sat = "Abaixo da meta"
        tipo_sat = "warning"

    card_kpi(
        "Satisfação",
        f"{satisfacao:.1f}/10",
        var_satisfacao_periodo,
        var_satisfacao_aa,
        " pts",
        " pts",
        False,
        status_sat,
        tipo_sat
    )

# CRESCIMENTO
with k5:

    if crescimento >= META_CRESCIMENTO - TOLERANCIA:
        status_cresc = "Meta atingida"
        tipo_cresc = "good"
    elif crescimento >= 0:
        status_cresc = "Abaixo da meta"
        tipo_cresc = "warning"
    else:
        status_cresc = "Retração da base"
        tipo_cresc = "critical"

    card_kpi(
        "Crescimento",
        f"{crescimento:+.1f}%",
        None,
        None,
        "",
        "",
        False,
        status_cresc,
        tipo_cresc
    )

# ============================================================
# MINI KPIs DE MERCADO
# ============================================================

st.write("")

m1, m2, m3 = st.columns(3)

with m1:

    st.markdown(
        f"""
        <div class="mini-card">

            <div class="mini-name">
                Líder de mercado
            </div>

            <div class="mini-value">
                {lider_share if lider_share else "—"}
            </div>

            <div class="mini-text">
                {lider_share_valor:.1f}% de Market Share
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with m2:

    st.markdown(
        f"""
        <div class="mini-card">

            <div class="mini-name">
                Concentração Top 2
            </div>

            <div class="mini-value">
                {concentracao_top2:.1f}%
            </div>

            <div class="mini-text">
                Participação combinada dos dois líderes
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with m3:

    st.markdown(
        f"""
        <div class="mini-card">

            <div class="mini-name">
                Players monitorados
            </div>

            <div class="mini-value">
                {players_monitorados}
            </div>

            <div class="mini-text">
                Players presentes no período
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# ============================================================
# PERFORMANCE VS META
# ============================================================

st.markdown(
    '<div class="section-label">PERFORMANCE</div>',
    unsafe_allow_html=True
)

st.markdown("## Performance vs. Meta")

dif_nps = nps - META_NPS
dif_satisfacao = satisfacao - META_SATISFACAO
dif_churn = churn - LIMITE_CHURN
dif_crescimento = crescimento - META_CRESCIMENTO

p1, p2, p3, p4 = st.columns(4)

with p1:

    st.metric(
        "NPS",
        f"{nps:.0f}",
        f"{dif_nps:+.1f} pts vs. meta"
    )

    if nps >= META_NPS - TOLERANCIA:
        st.success("Meta atingida")
    else:
        st.warning("Abaixo da meta")


with p2:

    st.metric(
        "Satisfação",
        f"{satisfacao:.1f}",
        f"{dif_satisfacao:+.1f} pt vs. meta"
    )

    if satisfacao >= META_SATISFACAO - TOLERANCIA:
        st.success("Meta atingida")
    else:
        st.warning("Abaixo da meta")


with p3:

    st.metric(
        "Churn",
        f"{churn:.1f}%",
        f"{dif_churn:+.1f} p.p. vs. limite",
        delta_color="inverse"
    )

    if churn <= LIMITE_CHURN + TOLERANCIA:
        st.success("Dentro do limite")
    else:
        st.error("Acima do limite")


with p4:

    st.metric(
        "Crescimento",
        f"{crescimento:+.1f}%",
        f"{dif_crescimento:+.1f} p.p. vs. meta"
    )

    if crescimento >= META_CRESCIMENTO - TOLERANCIA:
        st.success("Meta atingida")
    else:
        st.warning("Abaixo da meta")

st.divider()

# ============================================================
# MONITORAMENTO COMPETITIVO
# ============================================================

st.markdown(
    '<div class="section-label">MERCADO & CONCORRÊNCIA</div>',
    unsafe_allow_html=True
)

st.markdown("## Monitoramento Competitivo")

# ============================================================
# MARKET SHARE POR PLAYER
# ============================================================

if col_player and col_share and not share_player.empty:

    st.markdown("### Market Share por Player")

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
# EVOLUÇÃO MARKET SHARE
# ============================================================

if col_player and col_periodo and col_share:

    st.markdown("### Evolução de Market Share")

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
# RADAR CONECTA
# ============================================================

st.markdown(
    '<div class="section-label">RADAR CONECTA</div>',
    unsafe_allow_html=True
)

st.markdown("## Radar Inteligente")

alertas = []
oportunidades = []
alta_prioridade = 0

# CHURN
if churn > LIMITE_CHURN + TOLERANCIA:

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

# NPS
if nps < META_NPS - TOLERANCIA:

    diferenca = META_NPS - nps

    alertas.append({
        "nivel": "🟡",
        "titulo": "Experiência abaixo da meta",
        "texto":
            f"NPS em {nps:.0f}, "
            f"{diferenca:.0f} pontos abaixo "
            f"da meta de {META_NPS:.0f}."
    })

else:

    oportunidades.append(
        f"NPS em {nps:.0f} está dentro "
        "ou acima da meta."
    )

# SATISFAÇÃO
if satisfacao < META_SATISFACAO - TOLERANCIA:

    alertas.append({
        "nivel": "🟡",
        "titulo": "Satisfação abaixo da meta",
        "texto":
            f"Satisfação em {satisfacao:.1f}, "
            f"{META_SATISFACAO - satisfacao:.1f} "
            "ponto abaixo da meta."
    })

elif satisfacao > META_SATISFACAO + TOLERANCIA:

    oportunidades.append(
        f"Satisfação em {satisfacao:.1f}, "
        f"{satisfacao - META_SATISFACAO:.1f} "
        "ponto acima da meta."
    )

# CRESCIMENTO
if crescimento < META_CRESCIMENTO - TOLERANCIA:

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
        f"Crescimento de {crescimento:.1f}% "
        "atingiu ou superou a referência."
    )

# CONCENTRAÇÃO
if concentracao_top2 >= 60:

    alertas.append({
        "nivel": "🔵",
        "titulo": "Concentração competitiva",
        "texto":
            f"Os dois maiores players concentram "
            f"{concentracao_top2:.1f}% do "
            "Market Share monitorado."
    })

else:

    oportunidades.append(
        f"Top 2 representam {concentracao_top2:.1f}% "
        "do share, indicando menor concentração."
    )

# NPS + CHURN
if (
    nps < META_NPS - TOLERANCIA
    and churn > LIMITE_CHURN + TOLERANCIA
):

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

# CRESCIMENTO + CHURN
if (
    crescimento < META_CRESCIMENTO - TOLERANCIA
    and churn > LIMITE_CHURN + TOLERANCIA
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

# MOVIMENTO COMPETITIVO
if maior_ganho_nome and maior_ganho_valor >= 0.2:

    oportunidades.append(
        f"{maior_ganho_nome} ganhou "
        f"{maior_ganho_valor:.1f} p.p. de Market Share "
        "no período mais recente."
    )

if maior_perda_nome and maior_perda_valor <= -0.2:

    alertas.append({
        "nivel": "🟡",
        "titulo": "Perda recente de Market Share",
        "texto":
            f"{maior_perda_nome} perdeu "
            f"{abs(maior_perda_valor):.1f} p.p. "
            "de share no último período."
    })

# ============================================================
# KPIs RADAR
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

if alertas:

    st.warning(
        f"⚠️ {len(alertas)} sinal(is) "
        "identificado(s) pelo Radar CONECTA."
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

if oportunidades:

    st.markdown("### 🟢 Oportunidades identificadas")

    for oportunidade in oportunidades:

        st.success(
            f"💡 {oportunidade}"
        )

# ============================================================
# CONECTA IA
# ============================================================

st.divider()

st.markdown(
    '<div class="section-label">INTELIGÊNCIA ARTIFICIAL</div>',
    unsafe_allow_html=True
)

st.markdown("## ✦ CONECTA IA")

st.caption(
    "A camada de inteligência transforma sinais do radar "
    "em hipóteses de investigação e possíveis caminhos de ação. "
    "As recomendações devem ser validadas com dados de negócio."
)

if st.button(
    "✦ Investigar movimentos com CONECTA IA",
    use_container_width=True
):

    st.markdown(
        "### Leitura estratégica dos movimentos"
    )

    if churn > LIMITE_CHURN + TOLERANCIA:

        st.info(
            "**Retenção** — Segmentar churn por player, "
            "região e período para identificar onde a "
            "perda de clientes está mais concentrada."
        )

    if nps < META_NPS - TOLERANCIA:

        st.info(
            "**Experiência** — Cruzar NPS e churn para "
            "investigar se grupos com pior experiência "
            "também apresentam maior saída de clientes."
        )

    if crescimento < META_CRESCIMENTO - TOLERANCIA:

        st.info(
            "**Crescimento** — Separar aquisição e perda "
            "de base para investigar se o resultado está "
            "sendo pressionado por menor entrada ou "
            "maior cancelamento."
        )

    if concentracao_top2 >= 60:

        st.info(
            "**Concorrência** — Monitorar os movimentos "
            "dos líderes e identificar players menores "
            "com ganho consistente de participação."
        )

    if maior_perda_nome and maior_perda_valor < 0:

        st.info(
            f"**Movimento competitivo** — Investigar a "
            f"perda recente de share de {maior_perda_nome} "
            "e cruzar o movimento com churn, NPS e "
            "crescimento da base."
        )

    if maior_ganho_nome and maior_ganho_valor > 0:

        st.success(
            f"**Oportunidade** — {maior_ganho_nome} apresentou "
            f"ganho recente de {maior_ganho_valor:.1f} p.p. "
            "de share. Vale investigar quais indicadores "
            "acompanharam esse avanço."
        )

# ============================================================
# SOBRE
# ============================================================

st.divider()

with st.expander("ℹ️ Sobre o CONECTA INTELIGÊNC.IA"):

    st.write(
        """
        **CONECTA INTELIGÊNC.IA** é um protótipo de solução
        de Inteligência de Mercado & Estratégia potencializada
        por Inteligência Artificial.

        A plataforma conecta indicadores de mercado,
        concorrência, experiência e performance para
        identificar movimentos, riscos e oportunidades.

        O Radar CONECTA monitora alterações relevantes,
        enquanto a camada CONECTA IA transforma sinais
        em hipóteses de investigação e possíveis caminhos
        de ação.

        Os dados utilizados neste protótipo são sintéticos
        e não representam informações reais das empresas
        exibidas.
        """
    )

st.caption(
    "CONECTA INTELIGÊNC.IA • Protótipo desenvolvido por Fernanda Barbosa"
)
