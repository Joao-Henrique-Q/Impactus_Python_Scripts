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
st.session_state["PCE Contributions"] = pce_decomposto
st.session_state["Headline PCE"] = pce_headline
st.session_state["Core PCE - MoM"] = pce_core_mom
st.session_state["Core PCE - YoY"] = pce_core_ya
st.session_state["PCE - Goods MoM"] = pce_goods_mom
st.session_state["PCE - Goods YoY"] = pce_goods_ya
st.session_state["PCE - Nondurable Goods MoM"] = pce_ndur_mom
st.session_state["PCE - Nondurable Goods YoY"] = pce_ndur_yoy
st.session_state["PCE - Durable Goods MoM"] = pce_durable_mom
st.session_state["PCE - Durable Goods YoY"] = pce_durable_yoy
st.session_state["PCE - Services MoM"] = pce_serv_mom
st.session_state["PCE - Services YoY"] = pce_serv_ya
st.session_state["PCE - Food MoM"] = pce_food_mom
st.session_state["PCE - Food YoY"] = pce_food_yoy
st.session_state["PCE - Energy MoM"] = pce_en_mom
st.session_state["PCE - Energy YoY"] = pce_en_ya

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
            st.pyplot(st.session_state["Headline PCE"])
        elif opcao_grafico == "Core PCE":
            
            st.pyplot(st.session_state["Core PCE - MoM"])
            st.pyplot(st.session_state["Core PCE - YoY"])
        elif opcao_grafico == "PCE - Goods":
            st.pyplot(st.session_state["PCE - Goods MoM"])
            st.pyplot(st.session_state["PCE - Goods YoY"])
        elif opcao_grafico == "PCE - Nondurable Goods":
            st.pyplot(st.session_state["PCE - Nondurable Goods MoM"])
            st.pyplot(st.session_state["PCE - Nondurable Goods YoY"])
        elif opcao_grafico == "PCE - Durable Goods":
            st.pyplot(st.session_state["PCE - Durable Goods MoM"])
            st.pyplot(st.session_state["PCE - Durable Goods YoY"])
        elif opcao_grafico == "PCE - Services":
            st.pyplot(st.session_state["PCE - Services MoM"])
            st.pyplot(st.session_state["PCE - Services YoY"])
        elif opcao_grafico == "PCE - Food":
            st.pyplot(st.session_state["PCE - Food MoM"])
            st.pyplot(st.session_state["PCE - Food YoY"])
        elif opcao_grafico == "PCE - Energy":
            st.pyplot(st.session_state["PCE - Energy MoM"])
            st.pyplot(st.session_state["PCE - Energy YoY"])
    if subtema == "CPI":
        opcao_grafico = st.selectbox(
            "Selecione a Visualização",
            ['Core_cpi_nsa']
        )
        if opcao_grafico == "Core_cpi_nsa":
            st.pyplot(st.session_state["Core CPI NSA"])