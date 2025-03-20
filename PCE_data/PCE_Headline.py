import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
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

# Função para gráficos do PCE

def mostrar_grafico_pce_headline():
    fred = Fred(api_key="672d5598c8a41df9397cc5eb92c02d5e")  # Ou usar um objeto fred global se preferir

    pce_head = fred.get_series("PCEPI")

    pce_headline = pd.DataFrame()
    pce_headline["Nível de preços"] = pd.DataFrame(pce_head)
    pce_headline["Pct Change"] = pce_headline["Nível de preços"].pct_change()
    pce_headline["Pct Change from a year ago"] = pce_headline["Nível de preços"].pct_change(periods=12)
    pce_headline["3 MMA"] = pce_headline["Pct Change"].rolling(window=3).mean()
    pce_headline["6 MMA"] = pce_headline["Pct Change"].rolling(window=6).mean()
    pce_headline["3 MMA SAAR"] = (pce_headline["3 MMA"] + 1) ** 12 - 1
    pce_headline["6 MMA SAAR"] = (pce_headline["6 MMA"] + 1) ** 12 - 1
    pce_headline.index = pd.to_datetime(pce_headline.index)
    pce_headline = pce_headline[(pce_headline.index.year >= 2015)]

    fig, ax2 = plt.subplots(figsize=(10, 4))

    ax2.plot(pce_headline.index, pce_headline["Pct Change from a year ago"], linewidth=2, color="#082631", label="YoY %")
    ax2.plot(pce_headline.index, pce_headline["6 MMA SAAR"], linewidth=2, color="#37A6D9", label="6 MMA SAAR")
    ax2.plot(pce_headline.index, pce_headline["3 MMA SAAR"], linewidth=2, color="#AFABAB", label="3 MMA SAAR")

    ax2.set_ylabel("YoY %", fontsize=8)
    ax2.set_ylim(-0.03, 0.09)

    fig.suptitle("PCE Headline", fontsize=15, fontweight='bold')
    plt.text(0.505, 0.9, "SA Pct Change %", fontsize=8, ha='center', transform=plt.gcf().transFigure)

    ax2.legend(frameon=False, fontsize=8, loc="upper left")

    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_color("#d9d9d9")
    ax2.spines["bottom"].set_color("#d9d9d9")

    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax2.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15)

    plt.tight_layout()
    st.pyplot(fig)
def mostrar_grafico_pce_nucleo():
    fred = Fred(api_key="672d5598c8a41df9397cc5eb92c02d5e")  # Pode ser global também

    # --- Coleta e preparação dos dados ---
    psa = fred.get_series("PCEPILFE")
    core_pce_sa = pd.DataFrame()
    core_pce_sa["Pct Change"] = pd.DataFrame(psa).pct_change()
    core_pce_sa["Pct Change from a year ago"] = pd.DataFrame(psa).pct_change(periods=12)

    # --- MoM - Percentis, Mediana, 2024 e 2025 ---
    pce_graph_values = core_pce_sa[(core_pce_sa.index.year >= 2010) & (core_pce_sa.index.year <= 2019)]
    percentil_10_pctchg = pce_graph_values.groupby(pce_graph_values.index.month)["Pct Change"].quantile(0.10)
    percentil_90_pctchg = pce_graph_values.groupby(pce_graph_values.index.month)["Pct Change"].quantile(0.90)
    mediana_pctchg = pce_graph_values.groupby(pce_graph_values.index.month)["Pct Change"].median()
    pce_pctchg_2024 = core_pce_sa[core_pce_sa.index.year == 2024].groupby(core_pce_sa[core_pce_sa.index.year == 2024].index.month)["Pct Change"].first()
    pce_pctchg_2025 = core_pce_sa[core_pce_sa.index.year == 2025].groupby(core_pce_sa[core_pce_sa.index.year == 2025].index.month)["Pct Change"].first()

    pce_pctchg = pd.DataFrame({
        "Percentil 10": percentil_10_pctchg,
        "Percentil 90": percentil_90_pctchg,
        "Ano de 2024": pce_pctchg_2024,
        "Ano de 2025": pce_pctchg_2025,
        "Mediana": mediana_pctchg
    })

    pce_pctchg.index = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # --- YoY - Médias móveis ---
    pce_graph_values_ya = core_pce_sa[(core_pce_sa.index.year >= 2009)]
    mma3 = pce_graph_values_ya["Pct Change from a year ago"].rolling(window=3).mean()
    mma12 = pce_graph_values_ya["Pct Change from a year ago"].rolling(window=12).mean()
    mma6 = pce_graph_values_ya["Pct Change from a year ago"].rolling(window=6).mean()
    mean_10_19 = core_pce_sa[(core_pce_sa.index.year >= 2010) & (core_pce_sa.index.year <= 2019)]["Pct Change from a year ago"].mean()

    pce_graph_values_ya["MMA3"] = mma3
    pce_graph_values_ya["MMA6"] = mma6
    pce_graph_values_ya["MMA12"] = mma12
    pce_graph_values_ya["Mean 2010-2019"] = mean_10_19

    pce_ya = pd.DataFrame({
        "MMA3": mma3,
        "MMA6": mma6,
        "MMA12": mma12,
        "Mean 2010-2019": mean_10_19
    })

    pce_ya.dropna(inplace=True)
    pce_ya = pce_ya.drop(pce_ya.index[0])

    # ============================ #
    #       PRIMEIRO GRÁFICO       #
    # ============================ #

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(pce_pctchg.index, pce_pctchg["Mediana"], linewidth=2, color="#082631", label="Median")
    ax.plot(pce_pctchg.index, pce_pctchg["Ano de 2024"], marker="o", linewidth=2, color="#166083", label="2024")
    ax.plot(pce_pctchg.index, pce_pctchg["Ano de 2025"], marker="o", linewidth=2, color="#37A6D9", label="2025")
    ax.plot(pce_pctchg.index, pce_pctchg["Percentil 10"], color="grey", ls="-.")
    ax.plot(pce_pctchg.index, pce_pctchg["Percentil 90"], color="grey", ls="-.")

    fig.suptitle("Core PCE - MoM %", fontsize=15, fontweight='bold')
    plt.text(0.505, 0.90, "Pct Change MoM %", fontsize=8, ha='center', transform=plt.gcf().transFigure)

    ax.legend(frameon=False, fontsize=8, loc="upper right")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#d9d9d9")
    ax.spines["bottom"].set_color("#d9d9d9")

    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15)

    plt.tight_layout()
    st.pyplot(fig)

    # ============================ #
    #       SEGUNDO GRÁFICO        #
    # ============================ #

    fig2, ax2 = plt.subplots(figsize=(10, 4))

    ax2.plot(pce_ya.index, pce_ya["MMA3"], linewidth=2, color="#AFABAB", label="3 MMA", ls=":")
    ax2.plot(pce_ya.index, pce_ya["MMA6"], linewidth=2, color="#37A6D9", label="6 MMA", ls="--")
    ax2.plot(pce_ya.index, pce_ya["MMA12"], linewidth=2, color="#082631", label="12 MMA")
    ax2.plot(pce_ya.index, pce_ya["Mean 2010-2019"], linewidth=2, color="#166083", label="Mean 2010-2019")

    fig2.suptitle("Core PCE - YoY %", fontsize=15, fontweight='bold')
    plt.text(0.505, 0.9, "Pct Change YoY %", fontsize=8, ha='center', transform=plt.gcf().transFigure)

    ax2.legend(frameon=False, fontsize=8, loc="upper right")

    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_color("#c0c0c0")
    ax2.spines["bottom"].set_color("#c0c0c0")

    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax2.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15)

    ax2.set_ylim(0, 0.07)

    # Anotações de valores finais no gráfico
    ax2.text(pce_ya.index[-1], pce_ya["MMA3"].iloc[-1], f'{pce_ya["MMA3"].iloc[-1]:.2%}', color="#AFABAB", fontsize=7, ha='left')
    ax2.text(pce_ya.index[-1], pce_ya["MMA6"].iloc[-1], f'{pce_ya["MMA6"].iloc[-1]:.2%}', color="#37A6D9", fontsize=7, ha='left')
    ax2.text(pce_ya.index[-1], pce_ya["MMA12"].iloc[-1], f'{pce_ya["MMA12"].iloc[-1]:.2%}', color="#082631", fontsize=7, ha='left')
    ax2.text(pce_ya.index[-1], pce_ya["Mean 2010-2019"].iloc[-1], f'{pce_ya["Mean 2010-2019"].iloc[-1]:.2%}', color="#166083", fontsize=7, ha='left')

    plt.tight_layout()
    st.pyplot(fig2)
def aba_pce_goods():
    fred = Fred(api_key="672d5598c8a41df9397cc5eb92c02d5e")
    goods = fred.get_series("DGDSRG3M086SBEA")
    core_pce_goods = pd.DataFrame()
    core_pce_goods["Pct Change"] = pd.DataFrame(goods).pct_change()
    core_pce_goods["Pct Change from a year ago"] = pd.DataFrame(goods).pct_change(periods=12)

    pce_goods = core_pce_goods[(core_pce_goods.index.year >= 2010) & (core_pce_goods.index.year <= 2019)]
    percentil_10_pctchg_goods = pce_goods.groupby(pce_goods.index.month)["Pct Change"].quantile(0.10)
    percentil_90_pctchg_goods = pce_goods.groupby(pce_goods.index.month)["Pct Change"].quantile(0.90)
    mediana_pctchg_goods = pce_goods.groupby(pce_goods.index.month)["Pct Change"].median()
    pce_pctchg_2024_goods = core_pce_goods[core_pce_goods.index.year == 2024].groupby(core_pce_goods[core_pce_goods.index.year == 2024].index.month)["Pct Change"].first()
    pce_pctchg_2025_goods = core_pce_goods[core_pce_goods.index.year == 2025].groupby(core_pce_goods[core_pce_goods.index.year == 2025].index.month)["Pct Change"].first()

    goods_graph_values = pd.DataFrame({
        "Percentil 10": percentil_10_pctchg_goods,
        "Percentil 90": percentil_90_pctchg_goods,
        "Ano de 2024": pce_pctchg_2024_goods,
        "Ano de 2025": pce_pctchg_2025_goods,
        "Mediana": mediana_pctchg_goods
    })

    goods_graph_values.index = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    fig1, ax1 = plt.subplots(figsize=(10, 4))

    ax1.plot(goods_graph_values.index, goods_graph_values["Mediana"], linewidth=2, color="#082631", label="Median (2010-2019)")
    ax1.plot(goods_graph_values.index, goods_graph_values["Ano de 2024"], marker="o", linewidth=2, color="#166083", label="2024")
    ax1.plot(goods_graph_values.index, goods_graph_values["Ano de 2025"], marker="o", linewidth=2, color="#37A6D9", label="2025")
    ax1.plot(goods_graph_values.index, goods_graph_values["Percentil 10"], color="grey", ls="-.")
    ax1.plot(goods_graph_values.index, goods_graph_values["Percentil 90"], color="grey", ls="-.")

    fig1.suptitle("PCE - Goods", fontsize=15, fontweight='bold', fontname="Arial")
    plt.text(0.505, 0.9, "SA Pct Change MoM %", fontsize=8, fontname="Arial", ha='center', transform=plt.gcf().transFigure)

    ax1.legend(frameon=False, fontsize=8, prop={"family": "Arial"}, loc="upper right")

    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_color("#d9d9d9")
    ax1.spines["bottom"].set_color("#d9d9d9")

    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax1.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15, fontname="Arial")

    plt.tight_layout()
    st.pyplot(fig1)

    goods_graph_values_ya = core_pce_goods[(core_pce_goods.index.year >= 2009)]
    mma3_goods = goods_graph_values_ya["Pct Change from a year ago"].rolling(window=3).mean()
    mma12_goods = goods_graph_values_ya["Pct Change from a year ago"].rolling(window=12).mean()
    mma6_goods = goods_graph_values_ya["Pct Change from a year ago"].rolling(window=6).mean()
    mean_10_19_goods = core_pce_goods[(core_pce_goods.index.year >= 2010) & (core_pce_goods.index.year <= 2019)]["Pct Change from a year ago"].mean()

    goods_ya = pd.DataFrame({
        "MMA3": mma3_goods,
        "MMA6": mma6_goods,
        "MMA12": mma12_goods,
        "Mean 2010-2019": mean_10_19_goods
    })

    goods_ya.dropna(inplace=True)
    goods_ya = goods_ya.drop(goods_ya.index[0])

    fig2, ax2 = plt.subplots(figsize=(10, 4))

    ax2.plot(goods_ya.index, goods_ya["MMA3"], linewidth=2, color="#AFABAB", label="3 MMA", ls=":")
    ax2.plot(goods_ya.index, goods_ya["MMA6"], linewidth=2, color="#37A6D9", label="6 MMA", ls="--")
    ax2.plot(goods_ya.index, goods_ya["MMA12"], linewidth=2, color="#082631", label="12 MMA")
    ax2.plot(goods_ya.index, goods_ya["Mean 2010-2019"], linewidth=2, color="#166083", label="Mean (2010-2019)")

    fig2.suptitle("PCE - Goods", fontsize=15, fontweight='bold', fontname="Arial")
    plt.text(0.505, 0.9, "SA Pct Change YoY %", fontsize=8, fontname="Arial", ha='center', transform=plt.gcf().transFigure)

    ax2.legend(frameon=False, fontsize=8, prop={"family": "Arial"}, loc="upper right")

    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_color("#c0c0c0")
    ax2.spines["bottom"].set_color("#c0c0c0")

    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax2.text(goods_ya.index[-1], goods_ya["MMA3"].iloc[-1], f'{goods_ya["MMA3"].iloc[-1]:.2%}', color="#AFABAB", fontsize=7, ha='left')
    ax2.text(goods_ya.index[-1], goods_ya["MMA6"].iloc[-1], f'{goods_ya["MMA6"].iloc[-1]:.2%}', color="#37A6D9", fontsize=7, ha='left')
    ax2.text(goods_ya.index[-1], goods_ya["MMA12"].iloc[-1], f'{goods_ya["MMA12"].iloc[-1]:.2%}', color="#082631", fontsize=7, ha='left')
    ax2.text(goods_ya.index[-1], goods_ya["Mean 2010-2019"].iloc[-1], f'{goods_ya["Mean 2010-2019"].iloc[-1]:.2%}', color="#166083", fontsize=7, ha='left')

    ax2.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15, fontname="Arial")

    plt.tight_layout()
    st.pyplot(fig2)
def aba_pce_services():
    fred = Fred(api_key="672d5598c8a41df9397cc5eb92c02d5e")
    services = fred.get_series("DSERRG3M086SBEA")
    core_pce_services = pd.DataFrame()
    core_pce_services["Pct Change"] = pd.DataFrame(services).pct_change()
    core_pce_services["Pct Change from a year ago"] = pd.DataFrame(services).pct_change(periods=12)

    pce_services = core_pce_services[(core_pce_services.index.year >= 2010) & (core_pce_services.index.year <= 2019)]
    percentil_10_pctchg_services = pce_services.groupby(pce_services.index.month)["Pct Change"].quantile(0.10)
    percentil_90_pctchg_services = pce_services.groupby(pce_services.index.month)["Pct Change"].quantile(0.90)
    mediana_pctchg_services = pce_services.groupby(pce_services.index.month)["Pct Change"].median()
    pce_pctchg_2024_services = core_pce_services[core_pce_services.index.year == 2024].groupby(core_pce_services[core_pce_services.index.year == 2024].index.month)["Pct Change"].first()
    pce_pctchg_2025_services = core_pce_services[core_pce_services.index.year == 2025].groupby(core_pce_services[core_pce_services.index.year == 2025].index.month)["Pct Change"].first()

    services_graph_values = pd.DataFrame({
        "Percentil 10": percentil_10_pctchg_services,
        "Percentil 90": percentil_90_pctchg_services,
        "Ano de 2024": pce_pctchg_2024_services,
        "Ano de 2025": pce_pctchg_2025_services,
        "Mediana": mediana_pctchg_services
    })

    services_graph_values.index = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    fig1, ax1 = plt.subplots(figsize=(10, 4))

    ax1.plot(services_graph_values.index, services_graph_values["Mediana"], linewidth=2, color="#082631", label="Median (2010-2019)")
    ax1.plot(services_graph_values.index, services_graph_values["Ano de 2024"], marker="o", linewidth=2, color="#166083", label="2024")
    ax1.plot(services_graph_values.index, services_graph_values["Ano de 2025"], marker="o", linewidth=2, color="#37A6D9", label="2025")
    ax1.plot(services_graph_values.index, services_graph_values["Percentil 10"], color="grey", ls="-.")
    ax1.plot(services_graph_values.index, services_graph_values["Percentil 90"], color="grey", ls="-.")

    fig1.suptitle("PCE - Services", fontsize=15, fontweight='bold', fontname="Arial")
    plt.text(0.505, 0.9, "SA Pct Change MoM %", fontsize=8, fontname="Arial", ha='center', transform=plt.gcf().transFigure)

    ax1.legend(frameon=False, fontsize=8, prop={"family": "Arial"}, loc="upper right")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_color("#d9d9d9")
    ax1.spines["bottom"].set_color("#d9d9d9")
    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    ax1.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15, fontname="Arial")

    plt.tight_layout()
    st.pyplot(fig1)

    services_graph_values_ya = core_pce_services[(core_pce_services.index.year >= 2009)]
    mma3_services = services_graph_values_ya["Pct Change from a year ago"].rolling(window=3).mean()
    mma6_services = services_graph_values_ya["Pct Change from a year ago"].rolling(window=6).mean()
    mma12_services = services_graph_values_ya["Pct Change from a year ago"].rolling(window=12).mean()
    mean_10_19_services = core_pce_services[(core_pce_services.index.year >= 2010) & (core_pce_services.index.year <= 2019)]["Pct Change from a year ago"].mean()

    services_ya = pd.DataFrame({
        "MMA3": mma3_services,
        "MMA6": mma6_services,
        "MMA12": mma12_services,
        "Mean 2010-2019": mean_10_19_services
    })

    services_ya.dropna(inplace=True)
    services_ya = services_ya.drop(services_ya.index[0])

    fig2, ax2 = plt.subplots(figsize=(10, 4))

    ax2.plot(services_ya.index, services_ya["MMA3"], linewidth=2, color="#AFABAB", label="3 MMA", ls=":")
    ax2.plot(services_ya.index, services_ya["MMA6"], linewidth=2, color="#37A6D9", label="6 MMA", ls="--")
    ax2.plot(services_ya.index, services_ya["MMA12"], linewidth=2, color="#082631", label="12 MMA")
    ax2.plot(services_ya.index, services_ya["Mean 2010-2019"], linewidth=2, color="#166083", label="Mean (2010-2019)")

    fig2.suptitle("PCE - Services", fontsize=15, fontweight='bold', fontname="Arial")
    plt.text(0.505, 0.9, "SA Pct Change YoY %", fontsize=8, fontname="Arial", ha='center', transform=plt.gcf().transFigure)

    ax2.legend(frameon=False, fontsize=8, prop={"family": "Arial"}, loc="upper left")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_color("#c0c0c0")
    ax2.spines["bottom"].set_color("#c0c0c0")
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    ax2.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15, fontname="Arial")

    plt.tight_layout()
    st.pyplot(fig2)
def aba_pce_comida():
    #comida
    fred = Fred(api_key="672d5598c8a41df9397cc5eb92c02d5e")
    food = fred.get_series("DFXARG3M086SBEA")
    pce_food = pd.DataFrame()
    pce_food["Pct Change"] = pd.DataFrame(food).pct_change()
    pce_food["Pct Change from a year ago"] = pd.DataFrame(food).pct_change(periods=12)
    food_graph_values_ya = pce_food[(pce_food.index.year >= 2009)]
    #Vou pegar limites 90 e 10
    pce_pctchg_2024_food = pce_food[pce_food.index.year == 2024].groupby(pce_food[pce_food.index.year == 2024].index.month)["Pct Change"].first()
    pce_pctchg_2025_food = pce_food[pce_food.index.year == 2025].groupby(pce_food[pce_food.index.year == 2025].index.month)["Pct Change"].first()
    pce_food = pce_food[(pce_food.index.year >= 2010) & (pce_food.index.year <= 2019)]
    percentil_10_pctchg_food = pce_food.groupby(pce_food.index.month)["Pct Change"].quantile(0.10)
    percentil_90_pctchg_food = pce_food.groupby(pce_food.index.month)["Pct Change"].quantile(0.90)
    mediana_pctchg_food = pce_food.groupby(pce_food.index.month)["Pct Change"].median()

    food_graph_values = pd.DataFrame({
        "Percentil 10": percentil_10_pctchg_food,
        "Percentil 90": percentil_90_pctchg_food,
        "Ano de 2024": pce_pctchg_2024_food,
        "Ano de 2025": pce_pctchg_2025_food,
        "Mediana": mediana_pctchg_food
    })

    food_graph_values.index = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    fig1, ax1 = plt.subplots(figsize=(10, 4))

    ax1.plot(food_graph_values.index, food_graph_values["Mediana"], linewidth=2, color="#082631", label="Median (2010-2019)")
    ax1.plot(food_graph_values.index, food_graph_values["Ano de 2024"], marker="o", linewidth=2, color="#166083", label="2024")
    ax1.plot(food_graph_values.index, food_graph_values["Ano de 2025"], marker="o", linewidth=2, color="#37A6D9", label="2025")
    ax1.plot(food_graph_values.index, food_graph_values["Percentil 10"], color="grey", ls="-.")
    ax1.plot(food_graph_values.index, food_graph_values["Percentil 90"], color="grey", ls="-.")

    fig1.suptitle("PCE - Food", fontsize=15, fontweight='bold', fontname="Arial")
    plt.text(0.505, 0.9, "SA Pct Change MoM %", fontsize=8, fontname="Arial", ha='center', transform=plt.gcf().transFigure)

    ax1.legend(frameon=False, fontsize=8, prop={"family": "Arial"}, loc="upper right")

    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_color("#d9d9d9")
    ax1.spines["bottom"].set_color("#d9d9d9")

    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax1.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15, fontname="Arial")

    plt.tight_layout()
    st.pyplot(fig1)

    #agora comida yoy
    mma3_food = food_graph_values_ya["Pct Change from a year ago"].rolling(window=3).mean()
    mma12_food = food_graph_values_ya["Pct Change from a year ago"].rolling(window=12).mean()
    mma6_food = food_graph_values_ya["Pct Change from a year ago"].rolling(window=6).mean()
    mean_10_19_food = pce_food[(pce_food.index.year >= 2010) & (pce_food.index.year <= 2019)]["Pct Change from a year ago"].mean()

    food_ya = pd.DataFrame({
        "MMA3": mma3_food,
        "MMA6": mma6_food,
        "MMA12": mma12_food,
        "Mean 2010-2019": mean_10_19_food
    })

    food_ya.dropna(inplace=True)
    food_ya = food_ya.drop(food_ya.index[0])


    fig2, ax2 = plt.subplots(figsize=(10, 4))

    ax2.plot(food_ya.index, food_ya["MMA3"], linewidth=2, color="#AFABAB", label="3 MMA", ls=":")
    ax2.plot(food_ya.index, food_ya["MMA6"], linewidth=2, color="#37A6D9", label="6 MMA", ls="--")
    ax2.plot(food_ya.index, food_ya["MMA12"], linewidth=2, color="#082631", label="12 MMA")
    ax2.plot(food_ya.index, food_ya["Mean 2010-2019"], linewidth=2, color="#166083", label="Mean (2010-2019)")

    fig2.suptitle("PCE - Food", fontsize=15, fontweight='bold', fontname="Arial")
    plt.text(0.505, 0.9, "SA Pct Change YoY %", fontsize=8, fontname="Arial", ha='center', transform=plt.gcf().transFigure)

    ax2.legend(frameon=False, fontsize=8, prop={"family": "Arial"}, loc="upper left")

    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_color("#c0c0c0")
    ax2.spines["bottom"].set_color("#c0c0c0")

    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax2.text(food_ya.index[-1], food_ya["MMA3"].iloc[-1], f'{food_ya["MMA3"].iloc[-1]:.2%}', color="#AFABAB", fontsize=7, ha='left')
    ax2.text(food_ya.index[-1], food_ya["MMA6"].iloc[-1], f'{food_ya["MMA6"].iloc[-1]:.2%}', color="#37A6D9", fontsize=7, ha='left')
    ax2.text(food_ya.index[-1], food_ya["MMA12"].iloc[-1], f'{food_ya["MMA12"].iloc[-1]:.2%}', color="#082631", fontsize=7, ha='left')
    ax2.text(food_ya.index[-1], food_ya["Mean 2010-2019"].iloc[-1], f'{food_ya["Mean 2010-2019"].iloc[-1]:.2%}', color="#166083", fontsize=7, ha='left')

    ax2.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15, fontname="Arial")

    plt.tight_layout()
    st.pyplot(fig2)
def aba_pce_energia():
    fred = Fred(api_key="672d5598c8a41df9397cc5eb92c02d5e")
    # Energy goods and services
    energy = fred.get_series("DNRGRG3M086SBEA")
    pce_energy = pd.DataFrame()
    pce_energy["Pct Change"] = pd.DataFrame(energy).pct_change()
    pce_energy["Pct Change from a year ago"] = pd.DataFrame(energy).pct_change(periods=12)
    energy_graph_values_ya = pce_energy[(pce_energy.index.year >= 2009)]

    # Vou pegar limites 90 e 10
    pce_pctchg_2024_energy = pce_energy[pce_energy.index.year == 2024].groupby(pce_energy[pce_energy.index.year == 2024].index.month)["Pct Change"].first()
    pce_pctchg_2025_energy = pce_energy[pce_energy.index.year == 2025].groupby(pce_energy[pce_energy.index.year == 2025].index.month)["Pct Change"].first()
    pce_energy = pce_energy[(pce_energy.index.year >= 2010) & (pce_energy.index.year <= 2019)]
    percentil_10_pctchg_energy = pce_energy.groupby(pce_energy.index.month)["Pct Change"].quantile(0.10)
    percentil_90_pctchg_energy = pce_energy.groupby(pce_energy.index.month)["Pct Change"].quantile(0.90)
    mediana_pctchg_energy = pce_energy.groupby(pce_energy.index.month)["Pct Change"].median()

    energy_graph_values = pd.DataFrame({
        "Percentil 10": percentil_10_pctchg_energy,
        "Percentil 90": percentil_90_pctchg_energy,
        "Ano de 2024": pce_pctchg_2024_energy,
        "Ano de 2025": pce_pctchg_2025_energy,
        "Mediana": mediana_pctchg_energy
    })

    energy_graph_values.index = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    fig1, ax1 = plt.subplots(figsize=(10, 4))

    ax1.plot(energy_graph_values.index, energy_graph_values["Mediana"], linewidth=2, color="#082631", label="Median (2010-2019)")
    ax1.plot(energy_graph_values.index, energy_graph_values["Ano de 2024"], marker="o", linewidth=2, color="#166083", label="2024")
    ax1.plot(energy_graph_values.index, energy_graph_values["Ano de 2025"], marker="o", linewidth=2, color="#37A6D9", label="2025")
    ax1.plot(energy_graph_values.index, energy_graph_values["Percentil 10"], color="grey", ls="-.")
    ax1.plot(energy_graph_values.index, energy_graph_values["Percentil 90"], color="grey", ls="-.")

    fig1.suptitle("PCE - Energy Goods and Services", fontsize=15, fontweight='bold', fontname="Arial")
    plt.text(0.505, 0.9, "SA Pct Change MoM %", fontsize=8, fontname="Arial", ha='center', transform=plt.gcf().transFigure)

    ax1.legend(frameon=False, fontsize=8, prop={"family": "Arial"}, loc="upper right")

    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_color("#d9d9d9")
    ax1.spines["bottom"].set_color("#d9d9d9")

    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax1.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15, fontname="Arial")

    plt.tight_layout()
    st.pyplot(fig1)

    # Agora yoy de energia
    mma3_energy = energy_graph_values_ya["Pct Change from a year ago"].rolling(window=3).mean()
    mma12_energy = energy_graph_values_ya["Pct Change from a year ago"].rolling(window=12).mean()
    mma6_energy = energy_graph_values_ya["Pct Change from a year ago"].rolling(window=6).mean()
    mean_10_19_energy = pce_energy[(pce_energy.index.year >= 2010) & (pce_energy.index.year <= 2019)]["Pct Change from a year ago"].mean()

    energy_ya = pd.DataFrame({
        "MMA3": mma3_energy,
        "MMA6": mma6_energy,
        "MMA12": mma12_energy,
        "Mean 2010-2019": mean_10_19_energy
    })

    energy_ya.dropna(inplace=True)
    energy_ya = energy_ya.drop(energy_ya.index[0])

    fig2, ax2 = plt.subplots(figsize=(10, 4))

    ax2.plot(energy_ya.index, energy_ya["MMA3"], linewidth=2, color="#AFABAB", label="3 MMA", ls=":")
    ax2.plot(energy_ya.index, energy_ya["MMA6"], linewidth=2, color="#37A6D9", label="6 MMA", ls="--")
    ax2.plot(energy_ya.index, energy_ya["MMA12"], linewidth=2, color="#082631", label="12 MMA")
    ax2.plot(energy_ya.index, energy_ya["Mean 2010-2019"], linewidth=2, color="#166083", label="Mean (2010-2019)")

    fig2.suptitle("PCE - Energy Goods and Services", fontsize=15, fontweight='bold', fontname="Arial")
    plt.text(0.505, 0.9, "SA Pct Change YoY %", fontsize=8, fontname="Arial", ha='center', transform=plt.gcf().transFigure)

    ax2.legend(frameon=False, fontsize=8, prop={"family": "Arial"}, loc="upper left")

    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_color("#c0c0c0")
    ax2.spines["bottom"].set_color("#c0c0c0")

    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax2.text(energy_ya.index[-1], energy_ya["MMA3"].iloc[-1], f'{energy_ya["MMA3"].iloc[-1]:.2%}', color="#AFABAB", fontsize=7, ha='left')
    ax2.text(energy_ya.index[-1], energy_ya["MMA6"].iloc[-1], f'{energy_ya["MMA6"].iloc[-1]:.2%}', color="#37A6D9", fontsize=7, ha='left')
    ax2.text(energy_ya.index[-1], energy_ya["MMA12"].iloc[-1], f'{energy_ya["MMA12"].iloc[-1]:.2%}', color="#082631", fontsize=7, ha='left')
    ax2.text(energy_ya.index[-1], energy_ya["Mean 2010-2019"].iloc[-1], f'{energy_ya["Mean 2010-2019"].iloc[-1]:.2%}', color="#166083", fontsize=7, ha='left')

    ax2.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15, fontname="Arial")

    plt.tight_layout()
    st.pyplot(fig2)
def aba_pce_ndurable():
    fred = Fred(api_key="672d5598c8a41df9397cc5eb92c02d5e")
    nondurable = fred.get_series("DNDGRG3M086SBEA")
    pce_nondurable = pd.DataFrame()
    pce_nondurable["Pct Change"] = pd.DataFrame(nondurable).pct_change()
    pce_nondurable["Pct Change from a year ago"] = pd.DataFrame(nondurable).pct_change(periods=12)
    nondurable_graph_values_ya = pce_nondurable[(pce_nondurable.index.year >= 2009)]

    pce_pctchg_2024_nondurable = pce_nondurable[pce_nondurable.index.year == 2024].groupby(pce_nondurable[pce_nondurable.index.year == 2024].index.month)["Pct Change"].first()
    pce_pctchg_2025_nondurable = pce_nondurable[pce_nondurable.index.year == 2025].groupby(pce_nondurable[pce_nondurable.index.year == 2025].index.month)["Pct Change"].first()
    pce_nondurable = pce_nondurable[(pce_nondurable.index.year >= 2010) & (pce_nondurable.index.year <= 2019)]
    percentil_10_pctchg_nondurable = pce_nondurable.groupby(pce_nondurable.index.month)["Pct Change"].quantile(0.10)
    percentil_90_pctchg_nondurable = pce_nondurable.groupby(pce_nondurable.index.month)["Pct Change"].quantile(0.90)
    mediana_pctchg_nondurable = pce_nondurable.groupby(pce_nondurable.index.month)["Pct Change"].median()

    nondurable_graph_values = pd.DataFrame({
        "Percentil 10": percentil_10_pctchg_nondurable,
        "Percentil 90": percentil_90_pctchg_nondurable,
        "Ano de 2024": pce_pctchg_2024_nondurable,
        "Ano de 2025": pce_pctchg_2025_nondurable,
        "Mediana": mediana_pctchg_nondurable
    })

    nondurable_graph_values.index = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    fig1, ax1 = plt.subplots(figsize=(10, 4))
    ax1.plot(nondurable_graph_values.index, nondurable_graph_values["Mediana"], linewidth=2, color="#082631", label="Median (2010-2019)")
    ax1.plot(nondurable_graph_values.index, nondurable_graph_values["Ano de 2024"], marker="o", linewidth=2, color="#166083", label="2024")
    ax1.plot(nondurable_graph_values.index, nondurable_graph_values["Ano de 2025"], marker="o", linewidth=2, color="#37A6D9", label="2025")
    ax1.plot(nondurable_graph_values.index, nondurable_graph_values["Percentil 10"], color="grey", ls="-.")
    ax1.plot(nondurable_graph_values.index, nondurable_graph_values["Percentil 90"], color="grey", ls="-.")

    fig1.suptitle("PCE - Nondurable Goods", fontsize=15, fontweight='bold', fontname="Arial")
    ax1.legend(frameon=False, fontsize=8, prop={"family": "Arial"}, loc="upper right")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_color("#d9d9d9")
    ax1.spines["bottom"].set_color("#d9d9d9")
    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    ax1.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15, fontname="Arial")
    plt.tight_layout()
    st.pyplot(fig1)

    mma3_nondurable = nondurable_graph_values_ya["Pct Change from a year ago"].rolling(window=3).mean()
    mma12_nondurable = nondurable_graph_values_ya["Pct Change from a year ago"].rolling(window=12).mean()
    mma6_nondurable = nondurable_graph_values_ya["Pct Change from a year ago"].rolling(window=6).mean()
    mean_10_19_nondurable = pce_nondurable[(pce_nondurable.index.year >= 2010) & (pce_nondurable.index.year <= 2019)]["Pct Change from a year ago"].mean()

    nondurable_ya = pd.DataFrame({
        "MMA3": mma3_nondurable,
        "MMA6": mma6_nondurable,
        "MMA12": mma12_nondurable,
        "Mean 2010-2019": mean_10_19_nondurable
    })

    nondurable_ya.dropna(inplace=True)
    nondurable_ya = nondurable_ya.drop(nondurable_ya.index[0])

    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.plot(nondurable_ya.index, nondurable_ya["MMA3"], linewidth=2, color="#AFABAB", label="3 MMA", ls=":")
    ax2.plot(nondurable_ya.index, nondurable_ya["MMA6"], linewidth=2, color="#37A6D9", label="6 MMA", ls="--")
    ax2.plot(nondurable_ya.index, nondurable_ya["MMA12"], linewidth=2, color="#082631", label="12 MMA")
    ax2.plot(nondurable_ya.index, nondurable_ya["Mean 2010-2019"], linewidth=2, color="#166083", label="Mean (2010-2019)")

    fig2.suptitle("PCE - Nondurable Goods", fontsize=15, fontweight='bold', fontname="Arial")
    ax2.legend(frameon=False, fontsize=8, prop={"family": "Arial"}, loc="upper left")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_color("#c0c0c0")
    ax2.spines["bottom"].set_color("#c0c0c0")
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    ax2.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15, fontname="Arial")
    plt.tight_layout()
    st.pyplot(fig2)
def plot_pce_durable():
    fred = Fred(api_key="672d5598c8a41df9397cc5eb92c02d5e")
    durable = fred.get_series("DDURRG3M086SBEA")
    
    pce_durable = pd.DataFrame()
    pce_durable["Pct Change"] = durable.pct_change()
    pce_durable["Pct Change from a year ago"] = durable.pct_change(periods=12)
    durable_graph_values_ya = pce_durable[pce_durable.index.year >= 2009]
    
    pce_pctchg_2024_durable = pce_durable[pce_durable.index.year == 2024].groupby(pce_durable.index.month)["Pct Change"].first()
    pce_pctchg_2025_durable = pce_durable[pce_durable.index.year == 2025].groupby(pce_durable.index.month)["Pct Change"].first()
    
    pce_durable = pce_durable[(pce_durable.index.year >= 2010) & (pce_durable.index.year <= 2019)]
    percentil_10_pctchg_durable = pce_durable.groupby(pce_durable.index.month)["Pct Change"].quantile(0.10)
    percentil_90_pctchg_durable = pce_durable.groupby(pce_durable.index.month)["Pct Change"].quantile(0.90)
    mediana_pctchg_durable = pce_durable.groupby(pce_durable.index.month)["Pct Change"].median()
    
    durable_graph_values = pd.DataFrame({
        "Percentil 10": percentil_10_pctchg_durable,
        "Percentil 90": percentil_90_pctchg_durable,
        "Ano de 2024": pce_pctchg_2024_durable,
        "Ano de 2025": pce_pctchg_2025_durable,
        "Mediana": mediana_pctchg_durable
    })
    
    durable_graph_values.index = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    plt.figure(figsize=(18, 10.8))
    plt.plot(durable_graph_values.index, durable_graph_values["Mediana"], linewidth=2, color="#082631", label="Median (2010-2019)")
    plt.plot(durable_graph_values.index, durable_graph_values["Ano de 2024"], marker="o", linewidth=2, color="#166083", label="2024")
    plt.plot(durable_graph_values.index, durable_graph_values["Ano de 2025"], marker="o", linewidth=2, color="#37A6D9", label="2025")
    plt.plot(durable_graph_values.index, durable_graph_values["Percentil 10"], color="grey", ls= "-.")
    plt.plot(durable_graph_values.index, durable_graph_values["Percentil 90"], color="grey", ls= "-.")
    
    plt.suptitle("PCE - Durable Goods", fontsize=20, fontweight='bold')
    plt.text(0.505, 0.94, "SA Pct Change MoM %", fontsize=14, ha='center', transform=plt.gcf().transFigure)
    plt.legend(frameon=False, fontsize=14, loc="upper right")
    
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["left"].set_color("#d9d9d9")
    plt.gca().spines["bottom"].set_color("#d9d9d9")
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    
    plt.xlabel("Fonte: FRED | Impactus UFRJ", fontsize=14, labelpad=15)
    plt.tight_layout()
    plt.show()
def aba_pce_decomposto():
    fred = Fred(api_key="672d5598c8a41df9397cc5eb92c02d5e")

    data_pce = fred.get_series("PCE")
    data_ngoods = fred.get_series("PCEND")
    data_dgoods = fred.get_series("PCEDG")
    data_services = fred.get_series("PCES")

    pce = pd.DataFrame()
    pce["PCE"] = pd.DataFrame(data_pce)
    pce["Nondurable Goods"] = pd.DataFrame(data_ngoods)
    pce["Durable Goods"] = pd.DataFrame(data_dgoods)
    pce["Services"] = pd.DataFrame(data_services)

    proporcao = pd.DataFrame()
    proporcao["Nondurable Goods"] = pce["Nondurable Goods"] / pce["PCE"]
    proporcao["Durable Goods"] = pce["Durable Goods"] / pce["PCE"]
    proporcao["Services"] = pce["Services"] / pce["PCE"]
    proporcao = proporcao[(proporcao.index.year >= 2016)]

    dgood = fred.get_series("DDURRG3M086SBEA")
    ngood = fred.get_series("DNDGRG3M086SBEA")
    serv = fred.get_series("DSERRG3M086SBEA")
    cheio = fred.get_series("PCEPI")

    inflation = pd.DataFrame()
    inflation["Durable Goods"] = pd.DataFrame(dgood).pct_change(periods=12)
    inflation["Nondurable Goods"] = pd.DataFrame(ngood).pct_change(periods=12)
    inflation["Services"] = pd.DataFrame(serv).pct_change(periods=12)
    inflation["Cheio"] = pd.DataFrame(cheio).pct_change(periods=12)
    inflation = inflation[(inflation.index.year >= 2016)]

    contribuicao = pd.DataFrame()
    contribuicao["Durable Goods"] = proporcao["Durable Goods"] * inflation["Durable Goods"]
    contribuicao["Nondurable Goods"] = proporcao["Nondurable Goods"] * inflation["Nondurable Goods"]
    contribuicao["Services"] = proporcao["Services"] * inflation["Services"]
    contribuicao = contribuicao[(contribuicao.index.year >= 2016)]

    contribuicao_positive = contribuicao.clip(lower=0)
    contribuicao_negative = contribuicao.clip(upper=0)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(contribuicao.index, contribuicao_positive["Durable Goods"], color="#AFABAB", label="Durable Goods", width=14)
    ax.bar(contribuicao.index, contribuicao_negative["Durable Goods"], color="#AFABAB", width=14)
    ax.bar(contribuicao.index, contribuicao_positive["Nondurable Goods"], bottom=contribuicao_positive["Durable Goods"], color="#082631", label="Nondurable Goods", width=14)
    ax.bar(contribuicao.index, contribuicao_negative["Nondurable Goods"], bottom=contribuicao_negative["Durable Goods"], color="#082631", width=14)
    ax.bar(contribuicao.index, contribuicao_positive["Services"], bottom=contribuicao_positive["Durable Goods"] + contribuicao_positive["Nondurable Goods"], color="#37A6D9", label="Services", width=14)
    ax.bar(contribuicao.index, contribuicao_negative["Services"], bottom=contribuicao_negative["Durable Goods"] + contribuicao_negative["Nondurable Goods"], color="#37A6D9", width=14)
    ax.plot(contribuicao.index, inflation["Cheio"], color="#166083", label="Cheio", linewidth=2)

    fig.suptitle("PCE - Contribution to Inflation", fontsize=15, fontweight='bold', fontname="Arial")
    plt.text(0.505, 0.9, "SA Pct Change %", fontsize=8, fontname="Arial", ha='center', transform=plt.gcf().transFigure)
    ax.legend(frameon=False, fontsize=8, prop={"family": "Arial"}, loc="upper right")
    ax.axhline(y=0, color='black', linewidth=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#d9d9d9")
    ax.spines["bottom"].set_color("#d9d9d9")
    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15, fontname="Arial")
    plt.tight_layout()
    st.pyplot(fig)

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

        fig, ax = plt.subplots(figsize=(12, 4))
        ax.bar(indice, servp_values, width=15, color="#082631", label="Service Providing")
        ax.bar(indice, good_values, width=15, color="#166083", label="Goods-Producing", bottom=bottom_good)
        ax.plot(indice, priv["Criação Líquida de Postos de Trabalho no Setor Privado"], color="#184253", label="Private Payroll", linewidth=2)
        ax.axhline(0, color='black', linewidth=1)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color('#d9d9d9')
        ax.set_title("Private Payroll: Goods x Services", fontsize=8, style='italic')
        fig.suptitle("US: Payroll", fontweight="bold", fontsize=15)
        ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15)
        ax.legend(frameon=False, loc='upper right', fontsize=8)
        st.pyplot(fig)

    # Gráfico 2: Payroll Private x Government
    elif opcao_grafico == "Payroll: Private x Government":
        priv_values = np.array(priv["Criação Líquida de Postos de Trabalho no Setor Privado"])
        gov_values = np.array(gov["Criação Líquida de Postos de Trabalho no Governo"])

        bottom_gov = np.where(gov_values >= 0, priv_values, 0)
        bottom_priv = np.where(gov_values < 0, gov_values, 0)

        fig, ax = plt.subplots(figsize=(12, 4))
        ax.bar(indice, priv_values, width=15, color="#166083", label="Private Payroll", bottom=bottom_priv)
        ax.bar(indice, gov_values, width=15, color="#082631", label="Government Payroll", bottom=bottom_gov)
        ax.plot(indice, payroll_2324["Criação Líquida de Postos de Trabalho"], color="#184253", label="Payroll", linewidth=2)
        ax.axhline(0, color='black', linewidth=1)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color('#d9d9d9')
        ax.set_title("Payroll: Private x Government", fontsize=8, style='italic')
        fig.suptitle("US: Payroll", fontweight="bold", fontsize=15)
        ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15)
        ax.legend(frameon=False, loc='upper right', fontsize=8)
        st.pyplot(fig)

    # Gráfico 3: Total Payroll
    elif opcao_grafico == "Total Payroll: Criação Líquida de Postos":
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.bar(indice, payroll_2324["Criação Líquida de Postos de Trabalho"], width=15, color="#184253")
        ax.axhline(0, color='black', linewidth=1)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color('#d9d9d9')
        ax.set_title("Criação Líquida de Postos de Trabalho com ajuste sazonal", fontsize=8, style='italic')
        fig.suptitle("US: Payroll", fontweight="bold", fontsize=15)
        ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15)
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
            ["PCE Geral", "PCE Decomposto", "PCE Núcleo", "PCE Goods", "PCE Services", "PCE Food", "PCE Energy", "PCE Nondurable", "PCE Durable"]
        )

        if opcao_grafico == "PCE Geral":
            mostrar_grafico_pce_headline()  
        elif opcao_grafico == "PCE Núcleo":
            mostrar_grafico_pce_nucleo()   
        elif opcao_grafico == "PCE Goods":
            aba_pce_goods()  
        elif opcao_grafico == "PCE Services":
            aba_pce_services()
        elif opcao_grafico == "PCE Food":
            aba_pce_comida()
        elif opcao_grafico == "PCE Energy":
            aba_pce_energia()
        elif opcao_grafico == "PCE Nondurable":
            aba_pce_ndurable()
        elif opcao_grafico == "PCE Durable":
            plot_pce_durable()
        elif opcao_grafico == "PCE Decomposto":
            aba_pce_decomposto()


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
