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

    fig, ax = plt.subplots(figsize=(10, 4))
    ax2 = ax.twinx()

    ax.bar(pce_headline.index, pce_headline["Pct Change"], width=20, color="#166083", label="MoM %")
    ax2.plot(pce_headline.index, pce_headline["Pct Change from a year ago"], linewidth=2, color="#082631", label="YoY %")
    ax2.plot(pce_headline.index, pce_headline["6 MMA SAAR"], linewidth=2, color="#37A6D9", label="6 MMA SAAR")
    ax2.plot(pce_headline.index, pce_headline["3 MMA SAAR"], linewidth=2, color="#AFABAB", label="3 MMA SAAR")

    ax.set_ylabel("MoM %", fontsize=8)
    ax2.set_ylabel("YoY %", fontsize=8)
    ax.set_ylim(-0.003, 0.015)
    ax2.set_ylim(-0.03, 0.15)

    fig.suptitle("PCE Headline", fontsize=15, fontweight='bold')
    plt.text(0.505, 0.94, "SA Pct Change %", fontsize=8, ha='center', transform=plt.gcf().transFigure)

    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax2.legend(frameon=False, fontsize=8, loc="upper right")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#d9d9d9")
    ax.spines["bottom"].set_color("#d9d9d9")
    ax2.spines["top"].set_visible(False)

    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15)

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

    fig, ax = plt.subplots(figsize=(12, 4))

    ax.plot(pce_pctchg.index, pce_pctchg["Mediana"], linewidth=2, color="#082631", label="Median")
    ax.plot(pce_pctchg.index, pce_pctchg["Ano de 2024"], marker="o", linewidth=2, color="#166083", label="2024")
    ax.plot(pce_pctchg.index, pce_pctchg["Ano de 2025"], marker="o", linewidth=2, color="#37A6D9", label="2025")
    ax.plot(pce_pctchg.index, pce_pctchg["Percentil 10"], color="grey", ls="-.")
    ax.plot(pce_pctchg.index, pce_pctchg["Percentil 90"], color="grey", ls="-.")

    fig.suptitle("Core PCE - MoM %", fontsize=15, fontweight='bold')
    plt.text(0.505, 0.94, "Pct Change MoM %", fontsize=8, ha='center', transform=plt.gcf().transFigure)

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

    fig2, ax2 = plt.subplots(figsize=(12, 4))

    ax2.plot(pce_ya.index, pce_ya["MMA3"], linewidth=2, color="#AFABAB", label="3 MMA", ls=":")
    ax2.plot(pce_ya.index, pce_ya["MMA6"], linewidth=2, color="#37A6D9", label="6 MMA", ls="--")
    ax2.plot(pce_ya.index, pce_ya["MMA12"], linewidth=2, color="#082631", label="12 MMA")
    ax2.plot(pce_ya.index, pce_ya["Mean 2010-2019"], linewidth=2, color="#166083", label="Mean 2010-2019")

    fig2.suptitle("Core PCE - YoY %", fontsize=15, fontweight='bold')
    plt.text(0.505, 0.94, "Pct Change YoY %", fontsize=8, ha='center', transform=plt.gcf().transFigure)

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
            ["PCE Geral", "PCE Núcleo"]
        )

        if opcao_grafico == "PCE Geral":
            mostrar_grafico_pce_headline()  

        elif opcao_grafico == "PCE Núcleo":
            mostrar_grafico_pce_nucleo()     


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
