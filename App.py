import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from fredapi import Fred
from streamlit_option_menu import option_menu
from matplotlib import rcParams
from streamlit_option_menu import option_menu
from variaveis_dashboard import *
from streamlit_option_menu import option_menu  

fred = Fred(api_key="672d5598c8a41df9397cc5eb92c02d5e")

# Configuração da página
st.set_page_config(
    page_title="Central de Dados - EUA",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- SIDEBAR ----
with st.sidebar:
    st.markdown("## Central de Dados Econômicos US")
    st.markdown("""
    Este site apresenta **dados econômicos dos EUA** e análises em relação a seus impactos macroeconômicos. """)
    
    st.markdown("### 🔗 Links Úteis")
    st.markdown("- [BEA - Site Oficial](https://www.bea.gov/)")
    st.markdown("- [Federal Reserve of St. Louis](https://www.federalreserve.gov/)")
    st.markdown("- [GitHub do Projeto](https://github.com/Jaumzinho109/Impactus_Python_Scripts/blob/main/PCE_data/PCE_Headline.py)")

# ---- CABEÇALHO ----
st.title("US Data Base")

# ---- MENU PRINCIPAL ----
st.session_state["Core CPI NSA"] = core_cpi_nsa

menu = option_menu(
    menu_title=None,  
    options=[
        "Mercado de Trabalho",
        "Inflação",
        "Atividade Econômica",
        "Política Monetária"  
    ],
    icons=[
        "briefcase",       
        "graph-up",        
        "bar-chart",    
        "bank"             
    ],
    menu_icon="cast",       
    default_index=0,        
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#0e0f12"},
        "icon": {"color": "white", "font-size": "18px"},
        "nav-link": {
            "font-size": "18px",
            "text-align": "left",
            "margin": "0px",
            "--hover-color": "#2c2f36",
            "color": "white",
        },
        "nav-link-selected": {
            "background-color": "#0e0f12",
            "color": "#d02c2c",
            "border-bottom": "3px solid #d02c2c"
        },
    }
)
if menu == "Inflação":
    st.header("Inflação")

    subtema = st.selectbox(
        "Selecione o Subtema (Inflação)",
        ["PCE", "CPI", "PPI", "Inflation Breakeven"]
    )

    if subtema == "PCE":
        st.write(
        "O dado cheio do PCE avançou 0,33% m/m em janeiro, enquanto o núcleo subiu 0,25% m/m, ambas em linha com as projeções de mercado. Isso provocou a desaceleração do dado anual para 2,5%, contudo o momentum de 3 meses ainda apresenta tendência de alta, o que mantém acesa a nossa preocupação em relação à inflação.<br><br>"
        " O setor de serviços avançou 0,25% m/m, um número menor em relação à média das leituras de 2024. Esse é um bom sinal, considerando que no último ano, o setor foi a maior complicação para o avanço da inflação à meta do FED. Já a parte de bens avançou 0,6% m/m, um dado muito forte, mas que não apresenta grandes ameaças pela sua tendência historicamente mais baixa.<br><br>"
        "Por fim, os números são mistos, pois ainda que a leitura tenha sido em linha com as expectativas, uma variação mensal de 0,33% é muito acima da meta do FED. Além disso, o consumo pessoal apresentou retração de 0,2%, o que alimenta a narrativa de estagflação.",
        unsafe_allow_html=True
    )

        opcao_grafico = st.selectbox(
        "Selecione a Visualização",
        ["PCE Contributions", "Headline PCE", "Core PCE", "PCE - Goods", "PCE - Services", "PCE - Food", "PCE - Energy", "PCE - Nondurable Goods", "PCE - Durable Goods"]  
    )
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
        elif opcao_grafico == "PCE - Nondurable Goods":
            st.pyplot(pce_ndur_mom)
            st.pyplot(pce_ndur_yoy)
        elif opcao_grafico == "PCE - Durable Goods":
            st.pyplot(pce_durable_mom)
            st.pyplot(pce_durable_yoy)
        elif opcao_grafico == "PCE - Services":
            st.pyplot(pce_serv_mom)
            st.pyplot(pce_serv_ya)
        elif opcao_grafico == "PCE - Food":
            st.pyplot(pce_food_mom)
            st.pyplot(pce_food_yoy)
        elif opcao_grafico == "PCE - Energy":
            st.pyplot(pce_en_mom)
            st.pyplot(pce_food_yoy)
    if subtema == "CPI":
        opcao_grafico = st.selectbox(
            "Selecione a Visualização",
            ['Core_cpi_nsa']
        )
        if opcao_grafico == "Core_cpi_nsa":
            st.pyplot(st.session_state["Core CPI NSA"])
elif menu == "Mercado de Trabalho":
    st.write("A criação líquida de empregos no Payroll foi de 151 mil no mês de fevereiro, abaixo das expectativas de mercado (160 mil). Seu componente cíclico apresentou desaceleração em relação ao mês anterior. Acreditamos que isso foi resultado de maiores incertezas em relação ao futuro devido, especialmente, aos ruídos de Trump em relação às tarifas e maior austeridade. Por um lado, nossas nossas preocupações em relação a uma nova aceleração do setor que pressione os preços diminuem, mas por outro, esse fator aumenta a possibilidade de recessão. <br><br>"
             "o ganho médio por hora trabalhada subiu 0,3% no último mês em linha com o esperado, a taxa de desemprego subiu para 4.1%, acima das expectativas (4,0%).<br><br>"
             "Por fim, os dados sugerem certo arrefecimento do setor, visto que o maior nível de desemprego junto à tendência de menor demanda por trabalho tendem a pressioná-lo ao equilíbrio.",
             unsafe_allow_html=True)
    subtema_trabalho = option_menu(
        menu_title=None,  
        options=["Payroll", "Emprego", "Salários"],
        default_index=0,
        orientation="horizontal"
    )
    if subtema_trabalho == "Emprego":
        unrate_graphs = st.selectbox(
            "",
            ["Unemployment Rate", "Beveridge Curve","Labor Force Participation Rate", "Employment Change", "Layoffs and Discharges", "Hires and Job Quits", "Initial Claims", "Continuing Claims"]
        )
        if unrate_graphs == "Unemployment Rate":
            st.pyplot(unrate)
        elif unrate_graphs == "Beveridge Curve":
            st.pyplot(beveridge_curve)
            st.pyplot(beveridge_ratio)
        elif unrate_graphs == "Labor Force Participation Rate":
            st.pyplot(participation_rate)
        elif unrate_graphs == "Employment Change":
            st.pyplot(employment_change)
        elif unrate_graphs == "Layoffs and Discharges":
            st.pyplot(layoffs_and_discharges)
        elif unrate_graphs == "Hires and Job Quits":
            st.pyplot(hires_and_jobquits)
        elif unrate_graphs == "Initial Claims":
            st.pyplot(initial_claims)
        elif unrate_graphs == "Continuing Claims":
            st.pyplot(continuing_claims)
    if subtema_trabalho == "Payroll":
        payroll_graphs = st.selectbox(
        "",
        ["Payroll: Criação Líquida de Postos","Payroll: Ordering", "Payroll: Cyclics x Acyclics", "Payroll: Private x Government","Private Payroll: Goods x Services",
            "Payroll: Total vs Breakdown", "Payroll: SAM Rule"])
        if payroll_graphs == "Payroll: Criação Líquida de Postos":
            st.pyplot(payroll)
        elif payroll_graphs == "Payroll: Private x Government":
            st.pyplot(private_vs_government)
        elif payroll_graphs == "Private Payroll: Goods x Services":
            st.pyplot(goods_vs_services_payroll)
        elif payroll_graphs == "Payroll: Cyclics x Acyclics":
            st.pyplot(cic_payroll)
        elif payroll_graphs == "Payroll: Total vs Breakdown":
            st.pyplot(breakdown_payroll)
        elif payroll_graphs == "Payroll: SAM Rule":
            st.pyplot(sahm_rule)
        elif payroll_graphs == "Payroll: Ordering":
            st.pyplot(ordering)