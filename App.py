import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from fredapi import Fred
from streamlit_option_menu import option_menu
from matplotlib import rcParams
from variaveis_dashboard import *  


st.set_page_config(
    page_title="Central de Dados - EUA",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- SIDEBAR ----
with st.sidebar:
    st.markdown("## Central de Dados Econômicos US")
    st.markdown("""Este site apresenta **dados econômicos dos EUA** e análises em relação a seus impactos macroeconômicos.""")

    st.markdown("### 🔗 Links Úteis")
    st.markdown("- [BEA - Site Oficial](https://www.bea.gov/)")
    st.markdown("- [Federal Reserve of St. Louis](https://www.federalreserve.gov/)")
    st.markdown("- [GitHub do Projeto](https://github.com/Jaumzinho109/Impactus_Python_Scripts/blob/main/PCE_data/PCE_Headline.py)")

# ---- CABEÇALHO ----
st.title("US Data Base")

# ---- MENU PRINCIPAL ----
if "Core CPI NSA" not in st.session_state:
    st.session_state["Core CPI NSA"] = core_cpi_nsa  # Certifique-se de que essa variável existe

menu = option_menu(
    menu_title=None,
    options=["Mercado de Trabalho", "Inflação", "Atividade Econômica", "Política Monetária"],
    icons=["briefcase", "graph-up", "bar-chart", "bank"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

if menu == "Inflação":
    st.header("Inflação")

    subtema = st.selectbox(
        "Selecione o Subtema (Inflação)",
        ["PCE", "CPI", "PPI", "Inflation Breakeven"]
    )

    if subtema == "PCE":
        st.write(
            "O dado cheio do PCE avançou 0,33% m/m em janeiro, enquanto o núcleo subiu 0,25% m/m, ambas em linha com as projeções de mercado..."
            , unsafe_allow_html=True
        )

        opcao_grafico = st.selectbox(
            "Selecione a Visualização",
            ["PCE Contributions", "Headline PCE", "Core PCE", "PCE - Goods", "PCE - Services", "PCE - Food", "PCE - Energy"]
        )

       
        plt.close("all")

        if opcao_grafico == "PCE Contributions":
            st.pyplot(pce_decomposto)
        elif opcao_grafico == "Headline PCE":
            st.pyplot(pce_headline)
        elif opcao_grafico == "Core PCE":
            st.pyplot(pce_core_mom)
            st.pyplot(pce_core_ya)
        elif opcao_grafico == "PCE - Goods":
            st.pyplot(pce_goods_mom)
            st.pyplot(pce_goods_ya)

    elif subtema == "CPI":
        opcao_grafico = st.selectbox(
            "Selecione a Visualização",
            ["Core_cpi_nsa"]
        )
        if opcao_grafico == "Core_cpi_nsa":
            st.pyplot(st.session_state["Core CPI NSA"])

elif menu == "Mercado de Trabalho":
    st.write(
        "A criação líquida de empregos no Payroll foi de 151 mil no mês de fevereiro..."
        , unsafe_allow_html=True
    )

    subtema_trabalho = option_menu(
        menu_title=None,
        options=["Payroll", "Emprego", "Salários"],
        default_index=0,
        orientation="horizontal"
    )

    if subtema_trabalho == "Emprego":
        unrate_graphs = st.selectbox(
            "",
            ["Unemployment Rate", "Beveridge Curve", "Labor Force Participation Rate", "Employment Change"]
        )

        plt.close("all")  

        if unrate_graphs == "Unemployment Rate":
            st.pyplot(unrate)
        elif unrate_graphs == "Beveridge Curve":
            st.pyplot(beveridge_curve)
            st.pyplot(beveridge_ratio)

    if subtema_trabalho == "Payroll":
        payroll_graphs = st.selectbox(
            "",
            ["Payroll: Criação Líquida de Postos", "Payroll: Private x Government", "Payroll: Cyclics x Acyclics"]
        )

        plt.close("all")  

        if payroll_graphs == "Payroll: Criação Líquida de Postos":
            st.pyplot(payroll)
        elif payroll_graphs == "Payroll: Private x Government":
            st.pyplot(private_vs_government)
        elif payroll_graphs == "Payroll: Cyclics x Acyclics":
            st.pyplot(cic_payroll)

    if subtema_trabalho == "Salários":
        salario = st.selectbox(
            "",
            ["Average Hourly Earnings", "Unit Labor Cost vs Productivity"]
        )

        plt.close("all")  

        if salario == "Average Hourly Earnings":
            st.pyplot(average_hourly_earnings)
        elif salario == "Unit Labor Cost vs Productivity":
            st.pyplot(labor_cost)
