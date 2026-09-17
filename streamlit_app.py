import streamlit as st
import pandas as pd
import altair as alt
import os

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="CONECTA INTELIGÊNC.IA",
    page_icon="◉",
    layout="wide"
)

# ============================================================
# ESTILO
# ============================================================

st.markdown("""
<style>
.block-container {
    padding-top: 1.8rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    border-right: 1px solid rgba(120,120,120,0.20);
}

[data-testid="stMetric"] {
    border: 1px solid rgba(120,120,120,0.22);
    border-radius: 14px;
    padding: 16px 16px 13px 16px;
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
# CONVERTER PARA NÚMERO
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
# FILTROS
# ============================================================

st.sidebar.title("CONECTA")
st.sidebar.caption("Inteligência de Mercado & Estratégia")

st.sidebar.divider()

st.sidebar.subheader("🔎 Filtros")

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
# BASE HISTÓRICA
# Mantém Player e Região, mas ignora filtro de período
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

def media(coluna, base):
    if coluna and coluna in base.columns:
        valor = pd.to_numeric(
            base[coluna],
            errors="coerce"
        ).mean()

        if pd.notna(valor):
            return float(valor)

    return 0.0


def soma(coluna, base):
    if coluna and coluna in base.columns:
        valor = pd.to_numeric(
            base[coluna],
            errors="coerce"
        ).sum()

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
    periodos_disponiveis = lista_periodos()

    if not periodos_disponiveis:
        return None

    if periodo_selecionado != "Todos":
        return periodo_selecionado

    return periodos_disponiveis[-1]


def encontrar_periodo_anterior(periodo_atual):
    periodos_disponiveis = lista_periodos()

    if periodo_atual not in periodos_disponiveis:
        return None

    indice = periodos_disponiveis.index(periodo_atual)

    if indice == 0:
        return None

    return periodos_disponiveis[indice - 1]


def encontrar_periodo_aa(periodo_atual):
    if periodo_atual is None:
        return None

    texto = str(periodo_atual)

    try:
        if len(texto) >= 7:
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
        base_historica[col_periodo].astype(str)
        == str(periodo)
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

assinantes_anterior = (
    soma(col_assinantes, base_anterior)
    if periodo_anterior
    else None
)

assinantes_aa = (
    soma(col_assinantes, base_aa)
    if periodo_aa
    else None
)

churn_anterior = (
    media(col_churn, base_anterior)
    if periodo_anterior
    else None
)

churn_aa = (
    media(col_churn, base_aa)
    if periodo_aa
    else None
)

nps_anterior = (
    media(col_nps, base_anterior)
    if periodo_anterior
    else None
)

nps_aa = (
    media(col_nps, base_aa)
    if periodo_aa
    else None
)

satisfacao_anterior = (
    media(col_satisfacao, base_anterior)
    if periodo_anterior
    else None
)

satisfacao_aa = (
    media(col_satisfacao, base_aa)
    if periodo_aa
    else None
)

# ============================================================
# CRESCIMENTO
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

lider_share = "—"
lider_share_valor = 0.0

if not share_player.empty:
    lider_share = str(
        share_player.iloc[0][col_player]
    )

    lider_share_valor = float(
        share_player.iloc[0][col_share]
    )

players_monitorados = (
    base_atual[col_player].nunique()
    if col_player
    else 0
)

# ============================================================
# CONCENTRAÇÃO TOP 2
# ============================================================

concentracao_top2 = 0.0

if len(share_player) >= 2:
    concentracao_top2 = float(
        share_player.iloc[0][col_share]
        + share_player.iloc[1][col_share]
    )

# ============================================================
# MOVIMENTOS RECENTES
# ============================================================

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
        base_anterior
        .groupby(
            col_player,
            as_index=False
        )[col_share]
        .mean()
    )

    share_atual_comparacao = (
        base_atual
        .groupby(
            col_player,
            as_index=False
        )[col_share]
        .mean()
    )

    comparacao_share = share_atual_comparacao.merge(
        share_anterior,
        on=col_player,
        suffixes=("_atual", "_anterior")
    )

    if not comparacao_share.empty:
        comparacao_share["variacao_pp"] = (
            comparacao_share[f"{col_share}_atual"]
            - comparacao_share[f"{col_share}_anterior"]
        )

        linha_ganho = comparacao_share.loc[
            comparacao_share["variacao_pp"].idxmax()
        ]

        linha_perda = comparacao_share.loc[
            comparacao_share["variacao_pp"].idxmin()
        ]

        maior_ganho_nome = str(
            linha_ganho[col_player]
        )

        maior_ganho_valor = float(
            linha_ganho["variacao_pp"]
        )

        maior_perda_nome = str(
            linha_perda[col_player]
        )

        maior_perda_valor = float(
            linha_perda["variacao_pp"]
        )

# ============================================================
# CABEÇALHO
# ============================================================

st.caption("CONECTA")

st.title("INTELIGÊNC.IA")

st.markdown(
    "**Inteligência de Mercado & Estratégia potencializada por IA**"
)

st.caption(
    "Monitoramento competitivo • Performance • "
    "Experiência • Sinais de mercado"
)

status1, status2 = st.columns([3, 1])

with status1:
    st.success(
        f"● Monitoramento ativo • "
        f"{len(base_atual):,.0f} registros analisados"
        .replace(",", ".")
    )

with status2:
    if periodo_atual:
        st.info(
            f"Atualização: {periodo_atual}"
        )

# ============================================================
# GIRO DE INTELIGÊNCIA
# ============================================================

st.divider()

st.caption("GIRO DE INTELIGÊNCIA")

st.subheader("O que está movimentando o mercado?")

sinais_giro = []

if churn > LIMITE_CHURN + TOLERANCIA:
    sinais_giro.append(
        f"Churn está {churn - LIMITE_CHURN:.1f} p.p. acima do limite."
    )

if nps < META_NPS - TOLERANCIA:
    sinais_giro.append(
        f"NPS está {META_NPS - nps:.0f} pontos abaixo da meta."
    )

if crescimento < META_CRESCIMENTO - TOLERANCIA:
    sinais_giro.append(
        f"Crescimento está "
        f"{META_CRESCIMENTO - crescimento:.1f} p.p. abaixo da meta."
    )

if (
    maior_ganho_nome
    and maior_ganho_valor >= 0.1
):
    sinais_giro.append(
        f"{maior_ganho_nome} avançou "
        f"{maior_ganho_valor:.1f} p.p. em Market Share."
    )

if (
    maior_perda_nome
    and maior_perda_valor <= -0.1
):
    sinais_giro.append(
        f"{maior_perda_nome} perdeu "
        f"{abs(maior_perda_valor):.1f} p.p. de Market Share."
    )

if sinais_giro:
    st.info(
        f"◉ **{len(sinais_giro)} movimentos relevantes identificados.**"
    )

    for sinal in sinais_giro:
        st.write("• " + sinal)

else:
    st.success(
        "Nenhum movimento crítico identificado "
        "no período monitorado."
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
        texto_delta(
            var_base_periodo,
            "%"
        )
    )

    if var_base_aa is not None:
        st.caption(
            f"{var_base_aa:+.1f}% vs. mesmo período AA"
        )
    else:
        st.caption("Comparação AA indisponível")

with k2:
    st.metric(
        "Churn médio",
        f"{churn:.1f}%",
        texto_delta(
            var_churn_periodo,
            " p.p."
        ),
        delta_color="inverse"
    )

    if var_churn_aa is not None:
        st.caption(
            f"{var_churn_aa:+.1f} p.p. vs. mesmo período AA"
        )
    else:
        st.caption("Comparação AA indisponível")

with k3:
    st.metric(
        "NPS",
        f"{nps:.0f}",
        texto_delta(
            var_nps_periodo,
            " pts"
        )
    )

    if var_nps_aa is not None:
        st.caption(
            f"{var_nps_aa:+.1f} pts vs. mesmo período AA"
        )
    else:
        st.caption("Comparação AA indisponível")

with k4:
    st.metric(
        "Satisfação",
        f"{satisfacao:.1f}/10",
        texto_delta(
            var_sat_periodo,
            " pts"
        )
    )

    if var_sat_aa is not None:
        st.caption(
            f"{var_sat_aa:+.1f} pts vs. mesmo período AA"
        )
    else:
        st.caption("Comparação AA indisponível")

with k5:
    st.metric(
        "Crescimento",
        f"{crescimento:+.1f}%",
        f"{crescimento - META_CRESCIMENTO:+.1f} p.p. vs. meta"
    )

    if crescimento >= META_CRESCIMENTO - TOLERANCIA:
        st.caption("✓ Meta atingida")
    elif crescimento >= 0:
        st.caption("⚠ Abaixo da meta")
    else:
        st.caption("▼ Retração da base")

# ============================================================
# KPIs COMPETITIVOS
# ============================================================

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
# PERFORMANCE VS META
# ============================================================

st.divider()

st.caption("PERFORMANCE")

st.header("Performance vs. Meta")

p1, p2, p3, p4 = st.columns(4)

dif_nps = nps - META_NPS
dif_satisfacao = satisfacao - META_SATISFACAO
dif_churn = churn - LIMITE_CHURN
dif_crescimento = crescimento - META_CRESCIMENTO

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
# EVOLUÇÃO DE MARKET SHARE
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

# ============================================================
# RADAR CONECTA
# ============================================================

st.divider()

st.caption("RADAR CONECTA")

st.header("Radar Inteligente")

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
            f"{diferenca:.1f} p.p. acima do limite "
            f"de {LIMITE_CHURN:.1f}%."
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

    alertas.append({
        "nivel": "🟡",
        "titulo": "Experiência abaixo da meta",
        "texto":
            f"NPS em {nps:.0f}, "
            f"{META_NPS - nps:.0f} pontos abaixo "
            f"da meta de {META_NPS:.0f}."
    })

else:

    oportunidades.append(
        f"NPS em {nps:.0f} atingiu "
        "ou superou a meta."
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
        f"Satisfação em {satisfacao:.1f} está "
        "acima da meta."
    )

# CRESCIMENTO
if crescimento < META_CRESCIMENTO - TOLERANCIA:

    alertas.append({
        "nivel": "🟡",
        "titulo": "Crescimento abaixo do esperado",
        "texto":
            f"Crescimento de {crescimento:.1f}%, "
            f"{META_CRESCIMENTO - crescimento:.1f} "
            "p.p. abaixo da meta."
    })

else:

    oportunidades.append(
        f"Crescimento de {crescimento:.1f}% "
        "atingiu ou superou a meta."
    )

# CONCENTRAÇÃO
if concentracao_top2 >= 60:

    alertas.append({
        "nivel": "🔵",
        "titulo": "Concentração competitiva",
        "texto":
            f"Os dois maiores players concentram "
            f"{concentracao_top2:.1f}% do Market Share."
    })

else:

    oportunidades.append(
        f"Top 2 concentram {concentracao_top2:.1f}% "
        "do mercado monitorado."
    )

# EXPERIÊNCIA + RETENÇÃO
if (
    nps < META_NPS - TOLERANCIA
    and churn > LIMITE_CHURN + TOLERANCIA
):

    alertas.append({
        "nivel": "🔴",
        "titulo": "Experiência + retenção",
        "texto":
            "NPS abaixo da meta ocorre junto de churn "
            "acima do limite. O cruzamento merece "
            "investigação."
    })

    alta_prioridade += 1

# CRESCIMENTO + CHURN
if (
    crescimento < META_CRESCIMENTO - TOLERANCIA
    and churn > LIMITE_CHURN + TOLERANCIA
):

    alertas.append({
        "nivel": "🔴",
        "titulo": "Pressão sobre crescimento",
        "texto":
            "Crescimento abaixo da meta ocorre junto "
            "de churn acima do limite."
    })

    alta_prioridade += 1

# MARKET SHARE
if (
    maior_ganho_nome
    and maior_ganho_valor >= 0.2
):

    oportunidades.append(
        f"{maior_ganho_nome} ganhou "
        f"{maior_ganho_valor:.1f} p.p. de Market Share "
        "no período mais recente."
    )

if (
    maior_perda_nome
    and maior_perda_valor <= -0.2
):

    alertas.append({
        "nivel": "🟡",
        "titulo": "Perda recente de Market Share",
        "texto":
            f"{maior_perda_nome} perdeu "
            f"{abs(maior_perda_valor):.1f} p.p. "
            "de participação no último período."
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

if alertas:

    st.warning(
        f"⚠️ {len(alertas)} sinais identificados "
        "pelo Radar CONECTA."
    )

    for alerta in alertas:

        st.subheader(
            f"{alerta['nivel']} {alerta['titulo']}"
        )

        st.write(
            alerta["texto"]
        )

else:

    st.success(
        "Nenhum sinal crítico identificado."
    )

# ============================================================
# OPORTUNIDADES
# ============================================================

if oportunidades:

    st.subheader("🟢 Oportunidades identificadas")

    for oportunidade in oportunidades:

        st.success(
            f"💡 {oportunidade}"
        )

# ============================================================
# CONECTA IA
# ============================================================

st.divider()

st.caption("INTELIGÊNCIA ARTIFICIAL")

st.header("✦ CONECTA IA")

st.write(
    "Transforme os sinais identificados pelo Radar CONECTA "
    "em hipóteses de investigação e possíveis caminhos de ação."
)

st.caption(
    "As recomendações são hipóteses analíticas e devem ser "
    "validadas com dados de negócio antes da implementação."
)

if st.button(
    "✦ Investigar movimentos com CONECTA IA",
    use_container_width=True
):

    st.subheader(
        "Leitura estratégica dos movimentos"
    )

    if churn > LIMITE_CHURN + TOLERANCIA:

        st.info(
            "🔎 **RETENÇÃO**\n\n"
            "Segmentar churn por player, região e período "
            "para localizar onde a perda de clientes está "
            "mais concentrada."
        )

    if nps < META_NPS - TOLERANCIA:

        st.info(
            "🔎 **EXPERIÊNCIA**\n\n"
            "Cruzar NPS com churn para investigar se "
            "grupos com pior experiência apresentam "
            "maior saída de clientes."
        )

    if crescimento < META_CRESCIMENTO - TOLERANCIA:

        st.info(
            "🔎 **CRESCIMENTO**\n\n"
            "Separar aquisição e perda de base para "
            "entender se o resultado está sendo pressionado "
            "por menor entrada ou maior cancelamento."
        )

    if concentracao_top2 >= 60:

        st.info(
            "🔎 **CONCORRÊNCIA**\n\n"
            "Acompanhar os movimentos dos líderes e "
            "identificar players menores com ganho "
            "consistente de participação."
        )

    if (
        maior_perda_nome
        and maior_perda_valor < 0
    ):

        st.info(
            f"🔎 **MOVIMENTO COMPETITIVO**\n\n"
            f"Investigar a perda de share de "
            f"{maior_perda_nome} e cruzar o movimento "
            "com churn, NPS e crescimento."
        )

    if (
        maior_ganho_nome
        and maior_ganho_valor > 0
    ):

        st.success(
            f"💡 **OPORTUNIDADE**\n\n"
            f"{maior_ganho_nome} apresentou ganho de "
            f"{maior_ganho_valor:.1f} p.p. de share. "
            "Investigar quais indicadores acompanharam "
            "esse avanço."
        )

# ============================================================
# SOBRE
# ============================================================

st.divider()

with st.expander(
    "ℹ️ Sobre o CONECTA INTELIGÊNC.IA"
):

    st.write(
        """
**CONECTA INTELIGÊNC.IA** é um protótipo de solução de
Inteligência de Mercado & Estratégia potencializada por
Inteligência Artificial.

A plataforma conecta indicadores de mercado, concorrência,
experiência e performance para identificar movimentos,
riscos e oportunidades.

O **Radar CONECTA** monitora alterações relevantes enquanto
a camada **CONECTA IA** transforma os sinais em hipóteses
de investigação e possíveis caminhos de ação.

Os dados utilizados neste protótipo são sintéticos e não
representam informações reais das empresas exibidas.
        """
    )

st.caption(
    "CONECTA INTELIGÊNC.IA • Desenvolvido por Fernanda Barbosa"
)
