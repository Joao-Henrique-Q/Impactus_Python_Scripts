import streamlit as st
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from variaveis_dashboard import get_pce_figures, get_cpi_figures, get_ppi_figures
from atividade_dados import get_economic_activity_figures
from ppi import get_employment_figures
from juros_e_pm import get_interest_figures, get_monetary_policy_figures

# Configuração inicial da página
st.set_page_config(
    page_title="Central de Dados - EUA",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- SIDEBAR ----
with st.sidebar:
    st.markdown("## Central de Dados Econômicos US")
    st.markdown("Este site apresenta dados econômicos dos EUA e análises em relação a seus impactos macroeconômicos.")
    
    st.markdown("### 🔗 Links Úteis")
    st.markdown("- [BEA - Site Oficial](https://www.bea.gov/)")
    st.markdown("- [Federal Reserve of St. Louis](https://www.federalreserve.gov/)")
    st.markdown("- [GitHub do Projeto](https://github.com/Jaumzinho109/Impactus_Python_Scripts/blob/main/PCE_data/PCE_Headline.py)")

# ---- CABEÇALHO ----
st.title("US Data Base")

# ---- MENU PRINCIPAL ----
menu = option_menu(
    menu_title=None,
    options=["Mercado de Trabalho", "Inflação", "Atividade Econômica", "Política Monetária e Juros"],
    icons=["briefcase", "graph-up", "bar-chart", "bank"],
    default_index=0,
    orientation="horizontal",
)

# Função auxiliar para exibir gráficos
def display_figures(figures, cols_per_row=2):
    cols = st.columns(cols_per_row)
    for i, fig in enumerate(figures):
        with cols[i % cols_per_row]:
            st.pyplot(fig)
            plt.close(fig)

# ---- SEÇÃO DE INFLAÇÃO ----
if menu == "Inflação":
    st.header("Inflação")
    
    subtema = option_menu(
        "Selecione o Subtema (Inflação)",
        ["PCE", "CPI", "PPI"],
        default_index=0
    )

    if subtema == "PCE":
        st.write("O dado cheio do PCE avançou 0,33% m/m em janeiro...")
        pce_figures = get_pce_figures()
        display_figures(pce_figures)

    elif subtema == "CPI":
        cpi_figures = get_cpi_figures()
        display_figures(cpi_figures)

    elif subtema == "PPI":
        ppi_figures = get_ppi_figures()
        display_figures(ppi_figures)

# ---- SEÇÃO DE MERCADO DE TRABALHO ----
elif menu == "Mercado de Trabalho":
    st.write("A criação líquida de empregos no Payroll foi de 151 mil...")
    
    subtema_trabalho = option_menu(
        menu_title=None,
        options=["Payroll", "Emprego", "Salários"],
        default_index=0,
        orientation="horizontal"
    )
    
    employment_figures = get_employment_figures(subtema_trabalho)
    display_figures(employment_figures)

# ---- SEÇÃO DE POLÍTICA MONETÁRIA ----
elif menu == 'Política Monetária e Juros':
    subtema_pm = option_menu(
        menu_title=None,
        options=["Juros de Títulos Públicos", "Dados de Política Monetária"],
        default_index=0,
        orientation="horizontal"
    )
    
    if subtema_pm == 'Juros de Títulos Públicos':
        interest_figures = get_interest_figures()
        display_figures(interest_figures)
    else:
        policy_figures = get_monetary_policy_figures()
        display_figures(policy_figures)

# ---- SEÇÃO DE ATIVIDADE ECONÔMICA ----
elif menu == "Atividade Econômica":
    subtema_atividade = option_menu(
        menu_title=None,
        options=["Renda", "Consumo", "Vendas no Varejo", "PIB"],
        default_index=0,
        orientation="horizontal"
    )
    
    economic_figures = get_economic_activity_figures(subtema_atividade)
    display_figures(economic_figures)