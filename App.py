import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from fredapi import Fred
from streamlit_option_menu import option_menu
from matplotlib import rcParams
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
from Codigos_p_dashboard.core_cpi_nsa import core_cpi_nsa
st.pyplot(core_cpi_nsa)