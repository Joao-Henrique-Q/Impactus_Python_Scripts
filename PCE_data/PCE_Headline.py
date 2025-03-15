import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from fredapi import Fred

# Configuração da página
st.set_page_config(
    page_title="Central de Dados - EUA",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- SIDEBAR ----
with st.sidebar:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/US_flag_large_51_stars.png/640px-US_flag_large_51_stars.png",
        width=150
    )
    st.markdown("## Central de Dados Econômicos (beta) 🇺🇸")
    st.markdown("""
    Este dashboard apresenta **dados econômicos dos EUA**, organizados por temas e subtemas, com filtros dinâmicos e gráficos interativos.
    
    Projeto desenvolvido para análise macroeconômica.
    """)
    st.markdown("### 🕒 Última Atualização")
    st.write(datetime.today().strftime('%Y-%m-%d'))
    
    st.markdown("### 🔗 Links Úteis")
    st.markdown("- [BEA - Site Oficial](https://www.bea.gov/)")
    st.markdown("- [Relatório do FED](https://www.federalreserve.gov/)")
    st.markdown("- [GitHub do Projeto](https://github.com/)")

# ---- CABEÇALHO ----
st.title("Central de dados - Estados Unidos")

# ---- MENU PRINCIPAL ----
menu = st.selectbox(
    "Selecione o Tema",
    ["Inflação", "Atividade Econômica", "Mercado de Trabalho", "Política Monetária"]
)

# ---- FUNÇÃO PARA GRÁFICOS DE PAYROLL ----
def mostrar_graficos_payroll():
    fred = Fred(api_key="672d5598c8a41df9397cc5eb92c02d5e")

    # Coleta dos dados
    dados = fred.get_series("PAYEMS")
    df = pd.DataFrame(dados, columns=["Total"])
    df.index.name = "Date"
    df["Criação Líquida de Postos de Trabalho"] = df["Total"].diff()
    payroll_2324 = df.tail(50)
    indice = payroll_2324.index

    # Government Payroll
    government_payroll_data = fred.get_series("USGOVT")
    goverment_payroll = pd.DataFrame(government_payroll_data, columns=["Total"])
    goverment_payroll.index.name = "Date"
    goverment_payroll["Criação Líquida de Postos de Trabalho no Governo"] = goverment_payroll["Total"].diff()
    gov = goverment_payroll.tail(50)

    # Private Payroll
    private_payroll_data = fred.get_series("USPRIV")
    private_payroll = pd.DataFrame(private_payroll_data, columns=["Total"])
    private_payroll.index.name = "Date"
    private_payroll["Criação Líquida de Postos de Trabalho no Setor Privado"] = private_payroll["Total"].diff()
    priv = private_payroll.tail(50)

    # Goods Payroll
    goods_payroll_data = fred.get_series("USGOOD")
    goodp_payroll = pd.DataFrame(goods_payroll_data, columns=["Total"])
    goodp_payroll.index.name = "Date"
    goodp_payroll["Criação Líquida de Postos de Trabalho em Bens no Setor Privado"] = goodp_payroll["Total"].diff()
    good = goodp_payroll.tail(50)

    # Services Payroll
    services_payroll_data = fred.get_series("CES0800000001")
    services_private_payroll = pd.DataFrame(services_payroll_data, columns=["Total"])
    services_private_payroll.index.name = "Date"
    services_private_payroll["Criação Líquida de Postos em Serviços no Setor Privado"] = services_private_payroll["Total"].diff()
    servp = services_private_payroll.tail(50)

    # Submenu para escolher o gráfico
    opcao_grafico = st.selectbox(
        "Selecione a Visualização de Payroll",
        [
            "Private Payroll: Goods x Services",
            "Payroll: Private x Government",
            "Total Payroll: Criação Líquida de Postos"
        ]
    )

    # Gráfico 1: Private Payroll - Goods x Services
    if opcao_grafico == "Private Payroll: Goods x Services":
        servp_values = np.array(servp["Criação Líquida de Postos em Serviços no Setor Privado"])
        good_values = np.array(good["Criação Líquida de Postos de Trabalho em Bens no Setor Privado"])

        bottom_good = np.where(good_values >= 0, servp_values, 0)
        bottom_serv = np.where(good_values < 0, good_values, 0)

        fig, ax = plt.subplots(figsize=(14, 8.4))
        ax.bar(indice, servp_values, width=15, color="#082631", label="Service Providing")
        ax.bar(indice, good_values, width=15, color="#166083", label="Goods-Producing", bottom=bottom_good)
        ax.plot(indice, priv["Criação Líquida de Postos de Trabalho no Setor Privado"], color="#184253", label="Private Payroll", linewidth=2)
        ax.axhline(0, color='black', linewidth=1)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color('#d9d9d9')
        ax.set_title("Private Payroll: Goods x Services", fontsize=14, style='italic')
        fig.suptitle("US: Payroll", fontweight="bold", fontsize=25)
        ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=14, labelpad=15)
        ax.legend(frameon=False, loc='upper right', fontsize=14)
        st.pyplot(fig)

    # Gráfico 2: Payroll Private x Government
    elif opcao_grafico == "Payroll: Private x Government":
        priv_values = np.array(priv["Criação Líquida de Postos de Trabalho no Setor Privado"])
        gov_values = np.array(gov["Criação Líquida de Postos de Trabalho no Governo"])

        bottom_gov = np.where(gov_values >= 0, priv_values, 0)
        bottom_priv = np.where(gov_values < 0, gov_values, 0)

        fig, ax = plt.subplots(figsize=(14, 8.4))
        ax.bar(indice, priv_values, width=15, color="#166083", label="Private Payroll", bottom=bottom_priv)
        ax.bar(indice, gov_values, width=15, color="#082631", label="Government Payroll", bottom=bottom_gov)
        ax.plot(indice, payroll_2324["Criação Líquida de Postos de Trabalho"], color="#184253", label="Payroll", linewidth=2)
        ax.axhline(0, color='black', linewidth=1)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color('#d9d9d9')
        ax.set_title("Payroll: Private x Government", fontsize=14, style='italic')
        fig.suptitle("US: Payroll", fontweight="bold", fontsize=25)
        ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=14, labelpad=15)
        ax.legend(frameon=False, loc='upper right', fontsize=14)
        st.pyplot(fig)

    # Gráfico 3: Total Payroll
    elif opcao_grafico == "Total Payroll: Criação Líquida de Postos":
        fig, ax = plt.subplots(figsize=(14, 8.4))
        ax.bar(indice, payroll_2324["Criação Líquida de Postos de Trabalho"], width=15, color="#184253")
        ax.axhline(0, color='black', linewidth=1)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color('#d9d9d9')
        ax.set_title("Criação Líquida de Postos de Trabalho com ajuste sazonal", fontsize=14, style='italic')
        fig.suptitle("US: Payroll", fontweight="bold", fontsize=25)
        ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=14, labelpad=15)
        st.pyplot(fig)

# ---- SUBMENUS E CONTEÚDO ----
if menu == "Inflação":
    st.header("Inflação")
    
    subtema = st.selectbox(
        "Selecione o Subtema (Inflação)",
        ["PCE", "CPI", "PPI", "Inflation Breakeven"]
    )
    
    if subtema == "PCE":
        st.subheader("PCE - Personal Consumption Expenditures")
        
        opcao_grafico = st.selectbox(
            "Selecione a Visualização",
            ["PCE Geral", "PCE Núcleo"]
        )
        
        if opcao_grafico == "PCE Geral":
            st.write("🔵 Gráfico do PCE Geral aqui!")
        elif opcao_grafico == "PCE Núcleo":
            st.write("🟢 Gráfico do PCE Núcleo aqui!")

elif menu == "Atividade Econômica":
    st.header("Atividade Econômica")
    st.write("📊 Gráficos de atividade econômica aqui!")

elif menu == "Mercado de Trabalho":
    st.header("Mercado de Trabalho")

    subtema_trabalho = st.selectbox(
        "Selecione o Subtema do Mercado de Trabalho",
        ["Visão Geral", "Payroll"]
    )

    if subtema_trabalho == "Visão Geral":
        st.write("📈 Gráficos de emprego, desemprego, payrolls etc.")

    elif subtema_trabalho == "Payroll":
        st.subheader("Payroll - Criação Líquida de Postos de Trabalho")
        mostrar_graficos_payroll()

elif menu == "Política Monetária":
    st.header("Política Monetária")
    st.write("📉 Gráficos e dados de juros, balanço do FED, entre outros.")

# ---- COMENTÁRIOS E ANÁLISE ----
st.markdown("---")
st.subheader("Comentários")
st.write("""
Aqui você pode adicionar comentários analíticos sobre o gráfico ou dados selecionados.  
Exemplo: Os dados mais recentes do PCE indicam uma desaceleração no crescimento de preços em janeiro de 2025, alinhada à política do FED.
""")
