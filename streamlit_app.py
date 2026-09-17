# ============================================================
# ESTILO
# ============================================================

st.markdown("""
<style>

/* ==========================================================
   ÁREA PRINCIPAL
   ========================================================== */

.block-container {
    padding-top: 1.7rem;
    padding-bottom: 3rem;
}

/* ==========================================================
   SIDEBAR CLARA
   ========================================================== */

[data-testid="stSidebar"] {
    background-color: #F7F8FA !important;
    border-right: 1px solid #E2E5EA !important;
}

/* Títulos e textos da sidebar */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #172033 !important;
}

/* ==========================================================
   FILTROS
   ========================================================== */

/* Fundo das caixas */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #0E1117 !important;
    border: 1px solid #1F2937 !important;
    border-radius: 8px !important;
}

/* VALOR SELECIONADO: BRANCO */
[data-testid="stSidebar"] [data-baseweb="select"] span {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

/* Texto interno do select */
[data-testid="stSidebar"] [data-baseweb="select"] div {
    color: #FFFFFF !important;
}

/* Setinha */
[data-testid="stSidebar"] [data-baseweb="select"] svg {
    fill: #FFFFFF !important;
    color: #FFFFFF !important;
}

/* Linha divisória */
[data-testid="stSidebar"] hr {
    border-color: #DDE1E7 !important;
}

/* ==========================================================
   CARDS
   ========================================================== */

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
