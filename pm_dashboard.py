import streamlit as st
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from juros_e_pm import *

st.set_page_config(
    page_title="Central de Dados - EUA",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---- CABEÇALHO ----
st.title("US Data Base")

# ---- MENU PRINCIPAL ----
menu = option_menu(
    menu_title=None,
    options=["Juros de Títulos Públicos", "Dados de Política Monetária"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

if menu == 'Juros de Títulos Públicos':
    
    st.pyplot(graf_3m)
    st.pyplot(graf_10yr)
    st.pyplot(graf_7yr)
    st.pyplot(graf_20yr)
    st.pyplot(graf_30yr)
    plt.close("all")
elif menu == "Dados de Política Monetária":
    
    st.pyplot(graf_ffr)
    st.pyplot(graf_dif_r)
    st.pyplot(graf_ta)
    st.pyplot(graf_repo)
    st.pyplot(graf_tga)
    st.pyplot(graf_mv)
    plt.close("all")




