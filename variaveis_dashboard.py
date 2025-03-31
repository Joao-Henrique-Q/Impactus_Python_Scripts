import pandas as pd
from fredapi import Fred
import matplotlib.pyplot as plt
from matplotlib import ticker as mtick

fred = Fred(api_key="672d5598c8a41df9397cc5eb92c02d5e")

def core_cpi_nsa():
    fred = Fred(api_key="672d5598c8a41df9397cc5eb92c02d5e")

    pc = fred.get_series("SUUR0000SA0L1E")
    core_cpi = pd.DataFrame()
    core_cpi["Nível de preços do núcleo"] = pd.DataFrame(pc)
    core_cpi["Pct Change"] = core_cpi['Nível de preços do núcleo'].pct_change()
    core_cpi.index = pd.to_datetime(core_cpi.index)

    core_cpi_24 = core_cpi[core_cpi.index.year == 2024]
    core_cpi_25 = core_cpi[core_cpi.index.year == 2025]
    core_cpi_23 = core_cpi[core_cpi.index.year == 2023]

    valores_2024 = core_cpi_24.groupby(core_cpi_24.index.month)["Pct Change"].first()
    valores_2025 = core_cpi_25.groupby(core_cpi_25.index.month)["Pct Change"].first()
    valores_2023 = core_cpi_23.groupby(core_cpi_23.index.month)["Pct Change"].first()

    core_cpi = core_cpi[(core_cpi.index.year >= 2010) & (core_cpi.index.year <= 2019)]

    percentil_10 = pd.DataFrame()
    percentil_90 = pd.DataFrame()

    for mes in range(1, 13):
        dados_mes = core_cpi[core_cpi.index.month == mes]["Pct Change"]
        percentil_10.loc[mes, "Percentil 10"] = dados_mes.quantile(0.10)
        percentil_90.loc[mes, "Percentil 90"] = dados_mes.quantile(0.90)

    valores_2024 = []
    valores_2025 = []

    for mes in range(1, 13):
        valor_24 = core_cpi_24[core_cpi_24.index.month == mes]["Pct Change"].values
        valor_25 = core_cpi_25[core_cpi_25.index.month == mes]["Pct Change"].values
        valores_2024.append(valor_24[0] if len(valor_24) > 0 else None)
        valores_2025.append(valor_25[0] if len(valor_25) > 0 else None)

    valores_dos_graficos = pd.DataFrame()
    valores_dos_graficos["Percentil 10"] = percentil_10["Percentil 10"]
    valores_dos_graficos["Percentil 90"] = percentil_90["Percentil 90"]
    valores_dos_graficos["Ano de 2024"] = valores_2024
    valores_dos_graficos["Ano de 2025"] = valores_2025
    valores_dos_graficos["Ano de 2023"] = valores_2023
    valores_dos_graficos["Mediana"] = core_cpi.groupby(core_cpi.index.month)["Pct Change"].median()
    valores_dos_graficos.index = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    core_cpi_nsa, ax = plt.subplots(figsize=(18, 10.8))
    ax.fill_between(valores_dos_graficos.index, valores_dos_graficos["Percentil 10"], valores_dos_graficos["Percentil 90"], color="grey", alpha=0.3, label="10th-90th (2010-2019)")
    ax.plot(valores_dos_graficos.index, valores_dos_graficos["Mediana"], linestyle="dotted", linewidth=2, color="#082631", label="Median")
    ax.plot(valores_dos_graficos.index, valores_dos_graficos["Ano de 2024"], marker="o", linewidth=2, color="#166083", label="2024")
    ax.plot(valores_dos_graficos.index, valores_dos_graficos["Ano de 2025"], marker="o", linewidth=2, color="#37A6D9", label="2025")
    ax.plot(valores_dos_graficos.index, valores_dos_graficos["Ano de 2023"], marker="o", linewidth=2, color="#0B4C5F", label="2023")
    ax.set_title("Core CPI", fontsize=20, fontweight='bold')
    ax.legend(frameon=False, fontsize=14, loc="upper right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#d9d9d9")
    ax.spines["bottom"].set_color("#d9d9d9")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=14, labelpad=15)
    plt.tight_layout()
    return core_cpi_nsa
core_cpi_nsa = core_cpi_nsa()


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

    fig.suptitle("Headline PCE", fontsize=15, fontweight='bold')
    plt.text(0.505, 0.9, "SA Pct Change %", fontsize=10, ha='center', transform=plt.gcf().transFigure)

    ax2.legend(frameon=False, fontsize=10, loc="upper left")

    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_color("#d9d9d9")
    ax2.spines["bottom"].set_color("#d9d9d9")

    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax2.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15)

    plt.tight_layout()
    return fig
pce_headline = mostrar_grafico_pce_headline()
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
    plt.text(0.505, 0.90, "Pct Change MoM %", fontsize=10, ha='center', transform=plt.gcf().transFigure)

    ax.legend(frameon=False, fontsize=10, loc="upper right")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#d9d9d9")
    ax.spines["bottom"].set_color("#d9d9d9")

    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15)

    plt.tight_layout()


    # ============================ #
    #       SEGUNDO GRÁFICO        #
    # ============================ #

    fig2, ax2 = plt.subplots(figsize=(10, 4))

    ax2.plot(pce_ya.index, pce_ya["MMA3"], linewidth=2, color="#AFABAB", label="3 MMA", ls=":")
    ax2.plot(pce_ya.index, pce_ya["MMA6"], linewidth=2, color="#37A6D9", label="6 MMA", ls="--")
    ax2.plot(pce_ya.index, pce_ya["MMA12"], linewidth=2, color="#082631", label="12 MMA")
    ax2.plot(pce_ya.index, pce_ya["Mean 2010-2019"], linewidth=2, color="#166083", label="Mean 2010-2019")

    fig2.suptitle("Core PCE - YoY %", fontsize=15, fontweight='bold')
    plt.text(0.505, 0.9, "Pct Change YoY %", fontsize=10, ha='center', transform=plt.gcf().transFigure)

    ax2.legend(frameon=False, fontsize=10, loc="upper right")

    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_color("#c0c0c0")
    ax2.spines["bottom"].set_color("#c0c0c0")

    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax2.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15)

    ax2.set_ylim(0, 0.07)

    # Anotações de valores finais no gráfico
    ax2.text(pce_ya.index[-1], pce_ya["MMA3"].iloc[-1], f'{pce_ya["MMA3"].iloc[-1]:.2%}', color="#AFABAB", fontsize=7, ha='left')
    ax2.text(pce_ya.index[-1], pce_ya["MMA6"].iloc[-1], f'{pce_ya["MMA6"].iloc[-1]:.2%}', color="#37A6D9", fontsize=7, ha='left')
    ax2.text(pce_ya.index[-1], pce_ya["MMA12"].iloc[-1], f'{pce_ya["MMA12"].iloc[-1]:.2%}', color="#082631", fontsize=7, ha='left')
    ax2.text(pce_ya.index[-1], pce_ya["Mean 2010-2019"].iloc[-1], f'{pce_ya["Mean 2010-2019"].iloc[-1]:.2%}', color="#166083", fontsize=7, ha='left')

    plt.tight_layout()
  
    return fig, fig2
pce_core_mom, pce_core_ya = mostrar_grafico_pce_nucleo()
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
    plt.text(0.505, 0.9, "SA Pct Change MoM %", fontsize=10, fontname="Arial", ha='center', transform=plt.gcf().transFigure)

    ax1.legend(frameon=False, fontsize=10, prop={"family": "Arial"}, loc="upper right")

    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_color("#d9d9d9")
    ax1.spines["bottom"].set_color("#d9d9d9")

    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax1.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15, fontname="Arial")

    plt.tight_layout()

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
    return fig1,fig2
pce_goods_mom, pce_goods_ya = aba_pce_goods()
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
    plt.text(0.505, 0.9, "SA Pct Change MoM %", fontsize=10, fontname="Arial", ha='center', transform=plt.gcf().transFigure)

    ax1.legend(frameon=False, fontsize=10, prop={"family": "Arial"}, loc="upper right")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_color("#d9d9d9")
    ax1.spines["bottom"].set_color("#d9d9d9")
    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    ax1.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15, fontname="Arial")

    plt.tight_layout()
   

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
    plt.text(0.505, 0.9, "SA Pct Change YoY %", fontsize=10, fontname="Arial", ha='center', transform=plt.gcf().transFigure)

    ax2.legend(frameon=False, fontsize=10, prop={"family": "Arial"}, loc="upper left")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_color("#c0c0c0")
    ax2.spines["bottom"].set_color("#c0c0c0")
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    ax2.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15, fontname="Arial")

    plt.tight_layout()
    return fig1, fig2
pce_serv_mom, pce_serv_ya = aba_pce_services()
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
    plt.text(0.505, 0.9, "SA Pct Change MoM %", fontsize=10, fontname="Arial", ha='center', transform=plt.gcf().transFigure)

    ax1.legend(frameon=False, fontsize=10, prop={"family": "Arial"}, loc="upper right")

    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_color("#d9d9d9")
    ax1.spines["bottom"].set_color("#d9d9d9")

    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax1.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15, fontname="Arial")

    plt.tight_layout()

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
    return fig1, fig2
pce_food_mom, pce_food_yoy = aba_pce_comida()
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
    plt.text(0.505, 0.9, "SA Pct Change MoM %", fontsize=10, fontname="Arial", ha='center', transform=plt.gcf().transFigure)

    ax1.legend(frameon=False, fontsize=10, prop={"family": "Arial"}, loc="upper right")

    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_color("#d9d9d9")
    ax1.spines["bottom"].set_color("#d9d9d9")

    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax1.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15, fontname="Arial")

    plt.tight_layout()
    

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
    plt.text(0.505, 0.9, "SA Pct Change YoY %", fontsize=10, fontname="Arial", ha='center', transform=plt.gcf().transFigure)

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

    ax2.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15, fontname="Arial")

    plt.tight_layout()
    return fig1, fig2
pce_en_mom, pce_en_ya = aba_pce_energia()
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
    ax1.legend(frameon=False, fontsize=10, prop={"family": "Arial"}, loc="upper right")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_color("#d9d9d9")
    ax1.spines["bottom"].set_color("#d9d9d9")
    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    ax1.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15, fontname="Arial")
    plt.tight_layout()
    

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
    ax2.legend(frameon=False, fontsize=10, prop={"family": "Arial"}, loc="upper left")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_color("#c0c0c0")
    ax2.spines["bottom"].set_color("#c0c0c0")
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    ax2.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15, fontname="Arial")
    plt.tight_layout()
    return fig1, fig2
pce_ndur_mom, pce_ndur_yoy = aba_pce_ndurable()
def plot_pce_durable():
    # Obtenção dos dados
    fred = Fred(api_key="672d5598c8a41df9397cc5eb92c02d5e")
    font_prop = {"family": "Arial"}
    durable = fred.get_series("DDURRG3M086SBEA")
    pce_durable = pd.DataFrame()
    pce_durable["Pct Change"] = pd.DataFrame(durable).pct_change()
    pce_durable["Pct Change from a year ago"] = pd.DataFrame(durable).pct_change(periods=12)
    durable_graph_values_ya = pce_durable[(pce_durable.index.year >= 2009)]

    # Cálculo dos percentis e medianas
    pce_pctchg_2024_durable = pce_durable[pce_durable.index.year == 2024].groupby(pce_durable[pce_durable.index.year == 2024].index.month)["Pct Change"].first()
    pce_pctchg_2025_durable = pce_durable[pce_durable.index.year == 2025].groupby(pce_durable[pce_durable.index.year == 2025].index.month)["Pct Change"].first()
    pce_durable = pce_durable[(pce_durable.index.year >= 2010) & (pce_durable.index.year <= 2019)]
    percentil_10_pctchg_durable = pce_durable.groupby(pce_durable.index.month)["Pct Change"].quantile(0.10)
    percentil_90_pctchg_durable = pce_durable.groupby(pce_durable.index.month)["Pct Change"].quantile(0.90)
    mediana_pctchg_durable = pce_durable.groupby(pce_durable.index.month)["Pct Change"].median()

    # Criação do DataFrame para o gráfico
    durable_graph_values = pd.DataFrame({
        "Percentil 10": percentil_10_pctchg_durable,
        "Percentil 90": percentil_90_pctchg_durable,
        "Ano de 2024": pce_pctchg_2024_durable,
        "Ano de 2025": pce_pctchg_2025_durable,
        "Mediana": mediana_pctchg_durable
    })
    durable_graph_values.index = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # Gráfico 1: Variação Mensal (MoM)
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    ax1.plot(durable_graph_values.index, durable_graph_values["Mediana"], linewidth=2, color="#082631", label="Median (2010-2019)")
    ax1.plot(durable_graph_values.index, durable_graph_values["Ano de 2024"], marker="o", linewidth=2, color="#166083", label="2024")
    ax1.plot(durable_graph_values.index, durable_graph_values["Ano de 2025"], marker="o", linewidth=2, color="#37A6D9", label="2025")
    ax1.plot(durable_graph_values.index, durable_graph_values["Percentil 10"], color="grey", ls="-.")
    ax1.plot(durable_graph_values.index, durable_graph_values["Percentil 90"], color="grey", ls="-.")

    fig1.suptitle("PCE - Durable Goods", fontsize=15, fontweight='bold', fontproperties=font_prop)
    plt.text(0.505, 0.9, "SA Pct Change MoM %", fontsize=8, fontproperties=font_prop, ha='center', transform=plt.gcf().transFigure)
    ax1.legend(frameon=False, fontsize=8, prop=font_prop, loc="upper right")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_color("#d9d9d9")
    ax1.spines["bottom"].set_color("#d9d9d9")
    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    ax1.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15, fontproperties=font_prop)
    plt.tight_layout()
    

    # Gráfico 2: Variação Anual (YoY)
    mma3_durable = durable_graph_values_ya["Pct Change from a year ago"].rolling(window=3).mean()
    mma12_durable = durable_graph_values_ya["Pct Change from a year ago"].rolling(window=12).mean()
    mma6_durable = durable_graph_values_ya["Pct Change from a year ago"].rolling(window=6).mean()
    mean_10_19_durable = pce_durable[(pce_durable.index.year >= 2010) & (pce_durable.index.year <= 2019)]["Pct Change from a year ago"].mean()

    durable_ya = pd.DataFrame({
        "MMA3": mma3_durable,
        "MMA6": mma6_durable,
        "MMA12": mma12_durable,
        "Mean 2010-2019": mean_10_19_durable
    })
    durable_ya.dropna(inplace=True)
    durable_ya = durable_ya.drop(durable_ya.index[0])

    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.plot(durable_ya.index, durable_ya["MMA3"], linewidth=2, color="#AFABAB", label="3 MMA", ls=":")
    ax2.plot(durable_ya.index, durable_ya["MMA6"], linewidth=2, color="#37A6D9", label="6 MMA", ls="--")
    ax2.plot(durable_ya.index, durable_ya["MMA12"], linewidth=2, color="#082631", label="12 MMA")
    ax2.plot(durable_ya.index, durable_ya["Mean 2010-2019"], linewidth=2, color="#166083", label="Mean (2010-2019)")

    fig2.suptitle("PCE - Durable Goods", fontsize=15, fontweight='bold', fontproperties=font_prop)
    plt.text(0.505, 0.9, "SA Pct Change YoY %", fontsize=10, fontproperties=font_prop, ha='center', transform=plt.gcf().transFigure)
    ax2.legend(frameon=False, fontsize=10, prop=font_prop, loc="upper left")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_color("#c0c0c0")
    ax2.spines["bottom"].set_color("#c0c0c0")
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax2.text(durable_ya.index[-1], durable_ya["MMA3"].iloc[-1], f'{durable_ya["MMA3"].iloc[-1]:.2%}', color="#AFABAB", fontsize=7, ha='left')
    ax2.text(durable_ya.index[-1], durable_ya["MMA6"].iloc[-1], f'{durable_ya["MMA6"].iloc[-1]:.2%}', color="#37A6D9", fontsize=7, ha='left')
    ax2.text(durable_ya.index[-1], durable_ya["MMA12"].iloc[-1], f'{durable_ya["MMA12"].iloc[-1]:.2%}', color="#082631", fontsize=7, ha='left')
    ax2.text(durable_ya.index[-1], durable_ya["Mean 2010-2019"].iloc[-1], f'{durable_ya["Mean 2010-2019"].iloc[-1]:.2%}', color="#166083", fontsize=7, ha='left')

    ax2.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15, fontproperties=font_prop)
    plt.tight_layout()
    return fig1, fig2
pce_durable_mom, pce_durable_yoy = plot_pce_durable()
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
    ax.plot(contribuicao.index, inflation["Cheio"], color="#166083", label="Headline", linewidth=2)

    fig.suptitle("PCE - Contribution to Inflation", fontsize=15, fontweight='bold', fontname="Arial")
    plt.text(0.505, 0.9, "SA Pct Change %", fontsize=10, fontname="Arial", ha='center', transform=plt.gcf().transFigure)
    ax.legend(frameon=False, fontsize=10, prop={"family": "Arial"}, loc="upper right")
    ax.axhline(y=0, color='black', linewidth=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#d9d9d9")
    ax.spines["bottom"].set_color("#d9d9d9")
    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15, fontname="Arial")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    plt.tight_layout()
    return fig
pce_decomposto = aba_pce_decomposto()


#Gráficos Emprego
def unrate():
    u = fred.get_series("UNRATE")
    unrate = pd.DataFrame()
    unrate["UnRate"] = pd.DataFrame(u)
    unrate["3 MAA"] = unrate["UnRate"].rolling(window=3).mean()
    unrate["Min 12 m"]= unrate["UnRate"].rolling(window=12,min_periods=1).min()
    unrate["Sahm Rule"] = unrate["3 MAA"] - unrate["Min 12 m"]
    unrate = unrate.dropna()
    unrate = unrate.tail(450)
    index2 = unrate.index
    
    unr = unrate.tail(200).copy()
    unr["UnRate"] = unr["UnRate"] / 100
    unr["Média de 12 meses"] = unr["UnRate"].rolling(window=12).mean()
    index3 = unr.index

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(index3, unr["UnRate"], label="Unemployment Rate", linewidth=2.5, color="#37A6D9")
    ax.plot(index3, unr["Média de 12 meses"], label="12 MMA", linewidth=2.5, color="#082631")

    fig.suptitle("US: Unemployment Rate", fontsize=15, fontweight='bold')
    ax.set_title("Pct SA", fontsize=10, style='italic', pad=10)

    ax.legend(frameon=False, fontsize=10, loc="upper right")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color('#d9d9d9')

    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15)

    fig.tight_layout()

    return fig
unrate = unrate()
def participation_rate():
    cvp = fred.get_series("CIVPART")
    labor_participation_rate = pd.DataFrame()
    labor_participation_rate["Labor Force Participation Rate"] = pd.DataFrame(cvp)
    labor_participation_rate["Labor Force Participation Rate"] = labor_participation_rate["Labor Force Participation Rate"] / 100
    index = labor_participation_rate.index

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(index, labor_participation_rate["Labor Force Participation Rate"], linewidth=2.5, color="#082631")

    fig.suptitle("Labor Force Participation Rate", fontsize=15, fontweight='bold')
    ax.set_title("Pct SA", fontsize=10, style='italic')

    ax.axhline(0, color='black', linewidth=1)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15)

    ax.set_ylim(0.57, 0.68)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color('#d9d9d9')

    fig.tight_layout()

    return fig
participation_rate = participation_rate()
def employment_change():
    eml = fred.get_series("CE16OV")
    pa = fred.get_series("PAYEMS")
    employment_level = pd.DataFrame()
    payems = pd.DataFrame()
    employment_level["Employment Level"] = pd.DataFrame(eml)
    employment_level["Pct change"] = employment_level["Employment Level"].pct_change()
    payems["Payroll"] = pd.DataFrame(pa)
    payems["Pct change"] = payems["Payroll"].pct_change()
    payems = payems.tail(48)
    employment_level = employment_level.tail(48)
    index = employment_level.index

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(index, payems["Pct change"], linewidth=2.5, color="#082631", label="Payroll - Pct Change")
    ax.plot(index, employment_level["Pct change"], linewidth=2.5, color="#166083", label="Employment Level - Pct Change")

    fig.suptitle("Employment Change", fontsize=15, fontweight='bold')
    ax.set_title("MoM % SA", fontsize=10, style='italic')

    ax.axhline(0, color='black', linewidth=1)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15)

    ax.legend(frameon=False, fontsize=10, loc="upper right")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color('#d9d9d9')

    fig.tight_layout()

    return fig
employment_change = employment_change()
def plot_beveridge_curve():
    fred = Fred(api_key="672d5598c8a41df9397cc5eb92c02d5e")

    jr = fred.get_series("JTSJOR")
    ur = fred.get_series("UNRATE")

    beveridge_data = pd.DataFrame(index=jr.index)
    beveridge_data["Vacancy rate"] = jr / 100
    beveridge_data["Unemployment rate"] = ur / 100
    beveridge_data = beveridge_data[beveridge_data.index.year >= 2000]

    beveridge_data["Beveridge curve"] = beveridge_data["Vacancy rate"] / beveridge_data["Unemployment rate"]

    fig, ax = plt.subplots(figsize=(12, 5))

    period1 = beveridge_data[(beveridge_data.index.year >= 2000) & (beveridge_data.index < "2020-04-01")]
    period2 = beveridge_data[(beveridge_data.index >= "2020-04-01") & (beveridge_data.index < "2022-06-01")]
    period3 = beveridge_data[(beveridge_data.index >= "2022-06-01") & (beveridge_data.index < "2025-04-01")]
    point_jan_2025 = beveridge_data[(beveridge_data.index.year == 2025) & (beveridge_data.index.month == 1)]

    ax.scatter(period1["Unemployment rate"], period1["Vacancy rate"], color='#166083', label='Dec 2000 - Mar 2020', s=100)
    ax.scatter(period2["Unemployment rate"], period2["Vacancy rate"], color='#37A6D9', label='Apr 2020 - May 2022', s=100)
    ax.scatter(period3["Unemployment rate"], period3["Vacancy rate"], color='#AFABAB', label='Jun 2022 - Mar 2025', s=100)
    ax.scatter(point_jan_2025["Unemployment rate"], point_jan_2025["Vacancy rate"], color='#81C1DB', s=200, label='Jan 2025')

    ax.set_xlabel("Unemployment Rate", fontsize=10, color='#333333')
    ax.set_ylabel("Vacancy Rate", fontsize=10, color='#333333')
    ax.set_ylim(0, 0.08)
    ax.set_xlim(0.03, 0.15)

    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))

    ax.grid(True, linestyle='--', alpha=0.6, color='#d9d9d9')
    ax.legend(frameon=False, fontsize=10, loc="upper right")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#d9d9d9")
    ax.spines["bottom"].set_color("#d9d9d9")

    fig.suptitle("Beveridge Curve", fontsize=15, fontweight='bold', color='#333333')
    ax.set_title("US Labor Market Dynamics", fontsize=10, style='italic', color='#333333')

    ax.set_xlabel("Unemployment Rate\nFonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15)

    fig.tight_layout()
    
    return fig
def plot_beveridge_ratio():
    fred = Fred(api_key="672d5598c8a41df9397cc5eb92c02d5e")

    jr = fred.get_series("JTSJOR")
    ur = fred.get_series("UNRATE")

    beveridge_data = pd.DataFrame(index=jr.index)
    beveridge_data["Vacancy rate"] = jr / 100
    beveridge_data["Unemployment rate"] = ur / 100
    beveridge_data = beveridge_data[beveridge_data.index.year >= 2000]

    beveridge_data["Beveridge curve"] = beveridge_data["Vacancy rate"] / beveridge_data["Unemployment rate"]

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(beveridge_data.index, beveridge_data["Beveridge curve"], label="Beveridge curve", linewidth=2.5, color="#166083")

    fig.suptitle("Beveridge curve", fontsize=15, fontweight='bold')
    ax.set_title("Vacancy Rate / Unemployment Rate", fontsize=10, style='italic')

    ax.axhline(1, color='black', linewidth=1)

    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#d9d9d9")
    ax.spines["bottom"].set_color("#d9d9d9")

    fig.tight_layout()

    return fig
beveridge_curve = plot_beveridge_curve()
beveridge_ratio = plot_beveridge_ratio()
def layoffs_and_discharges():
    layoffs = fred.get_series("JTSLDL")
    layoffs_and_discharges = pd.DataFrame()
    layoffs_and_discharges["Layoffs and Discharges"] = pd.DataFrame(layoffs)
    layoffs_and_discharges["Média de 12 meses"] = layoffs_and_discharges["Layoffs and Discharges"].rolling(window=12).mean()
    layoffs_and_discharges = layoffs_and_discharges.dropna()
    index = layoffs_and_discharges.index

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(index, layoffs_and_discharges["Layoffs and Discharges"], linewidth=2, color="#082631", label="Layoffs and Discharges")
    ax.plot(index, layoffs_and_discharges["Média de 12 meses"], linewidth=2, color="#166083", label='12MMA')

    fig.suptitle("US: Layoffs and Discharges", fontsize=15, fontweight='bold')
    ax.set_title("Thousand SA", fontsize=10, style='italic', pad=10)

    ax.legend(frameon=False, fontsize=10, loc="upper right")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#d9d9d9")
    ax.spines["bottom"].set_color("#d9d9d9")

    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{int(x):,}'))

    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15)

    ax.set_ylim(1000, 3000)

    fig.tight_layout()

    return fig
layoffs_and_discharges = layoffs_and_discharges()
def hires_and_jobquits():
    jq = fred.get_series("JTSQUL")
    job_quits = pd.DataFrame()
    job_quits["Job Quits"] = pd.DataFrame(jq)
    job_quits["Pct Change"] = job_quits['Job Quits'].pct_change()

    hr = fred.get_series("JTSHIL")
    hires = pd.DataFrame()
    hires["Hires"] = pd.DataFrame(hr)
    hires["Pct Change"] = hires["Hires"].pct_change()

    index = hires.index

    fig, ax1 = plt.subplots(figsize=(12,5))

    ax1.set_ylabel("Hires", fontsize=10, color="#082631")
    ax1.plot(index, hires["Hires"], linewidth=2.5, color="#082631", label="Hires")
    ax1.tick_params(axis='y', labelcolor="#082631")

    ax2 = ax1.twinx()
    ax2.set_ylabel("Job Quits", fontsize=10, color="#37A6D9")
    ax2.plot(index, job_quits["Job Quits"], linewidth=2.5, color="#37A6D9", label="Job Quits")
    ax2.tick_params(axis='y', labelcolor="#37A6D9")

    fig.suptitle("US: Hires and Job Quits", fontsize=15, fontweight='bold')
    ax1.set_title("Thousand SA", fontsize=10, style='italic')

    ax1.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15)

    line1, = ax1.plot(index, hires["Hires"], linewidth=2.5, color="#082631", label="Hires")
    line2, = ax2.plot(index, job_quits["Job Quits"], linewidth=2.5, color="#37A6D9", label="Job Quits")
    lines = [line1, line2]
    labels = [line.get_label() for line in lines]
    ax1.legend(lines, labels, frameon=False, fontsize=10, loc="upper right")

    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ax1.spines['bottom'].set_color('#d9d9d9')

    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.spines['bottom'].set_color('#d9d9d9')

    plt.tight_layout()
    return fig
hires_and_jobquits = hires_and_jobquits()
def initial_claims():

    # Acesso aos dados do FRED
    ic = fred.get_series("ICSA")
    initial_claims = pd.DataFrame()
    initial_claims["Initial Claims"] = pd.DataFrame(ic)
    initial_claims["4 Week AVG"] = initial_claims["Initial Claims"].rolling(window=4).mean()
    initial_claims = initial_claims.tail(180)
    index = initial_claims.index

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(index, initial_claims["4 Week AVG"], linewidth=2.5, color="#082631", label="4 Week AVG")
    ax.plot(index, initial_claims["Initial Claims"], linewidth=2.5, color="#166083", label="Initial Claims")

    fig.suptitle("US: Initial Claims", fontsize=15, fontweight='bold')
    ax.set_title("Net Change SA", fontsize=10, style='italic', pad=10)

    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15)

    ax.set_ylim(150000, 300000)

    ax.legend(frameon=False, fontsize=10, loc="upper right")

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#d9d9d9')

    fig.tight_layout()

    return fig
initial_claims = initial_claims()
def continuing_claims():
    # Acesso aos dados do FRED
    cc = fred.get_series("CCSA")
    continuing_claims = pd.DataFrame()
    continuing_claims["Continuing Claims"] = pd.DataFrame(cc)
    index = continuing_claims.index


    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(index, continuing_claims["Continuing Claims"], linewidth=2.5, color="#082631")

    fig.suptitle("US: Continuing Claims", fontsize=15, fontweight='bold')
    ax.set_title("Units SA", fontsize=10, style='italic', pad=10)
    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15)

    ax.set_ylim(1000000, 7000000)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#d9d9d9')

    fig.tight_layout()

    return fig
continuing_claims = continuing_claims()