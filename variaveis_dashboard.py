import pandas as pd
from fredapi import Fred
import matplotlib.pyplot as plt
from matplotlib import ticker as mtick
import numpy as np
import requests
from datetime import datetime
import requests
import pandas as pd

fred = Fred(api_key="672d5598c8a41df9397cc5eb92c02d5e")
api_key="672d5598c8a41df9397cc5eb92c02d5e"
#Gráficos do CPI
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

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.fill_between(valores_dos_graficos.index, valores_dos_graficos["Percentil 10"], valores_dos_graficos["Percentil 90"], color="grey", alpha=0.3, label="10th-90th (2010-2019)")
    ax.plot(valores_dos_graficos.index, valores_dos_graficos["Mediana"], linestyle="dotted", linewidth=2, color="#082631", label="Median")
    ax.plot(valores_dos_graficos.index, valores_dos_graficos["Ano de 2024"], marker="o", linewidth=2, color="#166083", label="2024")
    ax.plot(valores_dos_graficos.index, valores_dos_graficos["Ano de 2025"], marker="o", linewidth=2, color="#37A6D9", label="2025")
    

    fig.suptitle("Core CPI", fontsize=15, fontweight='bold')
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    ax.set_title("MoM % NSA", fontsize=8)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#d9d9d9")
    ax.spines["bottom"].set_color("#d9d9d9")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15)
    fig.tight_layout()

    return fig
core_cpi_nsa = core_cpi_nsa()
def headline_nsa():
    plt.close("all")
    
    cpi = fred.get_series('CPIAUCNS')
    cpi_us = pd.DataFrame()
    cpi_us["MoM %"] = pd.DataFrame(cpi).pct_change()

    cpi_23 = cpi_us.loc[cpi_us.index.to_series().dt.year == 2023].copy()
    cpi_24 = cpi_us.loc[cpi_us.index.to_series().dt.year == 2024].copy()
    cpi_25 = cpi_us.loc[cpi_us.index.to_series().dt.year == 2025].copy()

    valores_2024 = cpi_24.groupby(cpi_24.index.month)["MoM %"].first()
    valores_2025 = cpi_25.groupby(cpi_25.index.month)["MoM %"].first()
    valores_2023 = cpi_23.groupby(cpi_23.index.month)["MoM %"].first()

    cpi_us = cpi_us[(cpi_us.index.year >= 2010) & (cpi_us.index.year <= 2019)]

    percentil_10 = pd.DataFrame()
    percentil_90 = pd.DataFrame()

    for mes in range(1, 13):
        dados_mes = cpi_us[cpi_us.index.month == mes]["MoM %"]
        percentil_10.loc[mes, "Percentil 10"] = dados_mes.quantile(0.10)
        percentil_90.loc[mes, "Percentil 90"] = dados_mes.quantile(0.90)

    valores_dos_graficos = pd.DataFrame()
    valores_dos_graficos["Percentil 10"] = percentil_10["Percentil 10"]
    valores_dos_graficos["Percentil 90"] = percentil_90["Percentil 90"]
    valores_dos_graficos["Ano de 2024"] = valores_2024
    valores_dos_graficos["Ano de 2025"] = valores_2025
    valores_dos_graficos["Ano de 2023"] = valores_2023
    valores_dos_graficos["Mediana"] = cpi_us.groupby(cpi_us.index.month)["MoM %"].median()
    valores_dos_graficos.index = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


    fig, ax = plt.subplots(figsize=(10, 4))

    ax.fill_between(valores_dos_graficos.index, valores_dos_graficos["Percentil 10"], valores_dos_graficos["Percentil 90"], color="grey", alpha=0.3, label="10th-90th (2010-2019)")
    ax.plot(valores_dos_graficos.index, valores_dos_graficos["Mediana"], linestyle="dotted", linewidth=2, color="#082631", label="Median")
    ax.plot(valores_dos_graficos.index, valores_dos_graficos["Ano de 2024"], marker="o", linewidth=2, color="#166083", label="2024")
    ax.plot(valores_dos_graficos.index, valores_dos_graficos["Ano de 2025"], marker="o", linewidth=2, color="#37A6D9", label="2025")
    

    fig.suptitle("Headline CPI", fontsize=15, fontweight='bold')
    ax.set_title("MoM % NSA", fontsize=8)
    ax.legend(frameon=False, fontsize=8, loc="upper right")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#d9d9d9")
    ax.spines["bottom"].set_color("#d9d9d9")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15)
    fig.tight_layout()
    return fig
cpi_head_nsa = headline_nsa()
def core_goods_nsa():

    plt.close('all')

    cpi_core_goods = fred.get_series('CUUR0000SACL1E')
    cpi_core_goods_us = pd.DataFrame()
    cpi_core_goods_us["MoM %"] = cpi_core_goods.pct_change()

    cpi_core_goods_23 = cpi_core_goods_us.loc[cpi_core_goods_us.index.year == 2023].copy()
    cpi_core_goods_24 = cpi_core_goods_us.loc[cpi_core_goods_us.index.year == 2024].copy()
    cpi_core_goods_25 = cpi_core_goods_us.loc[cpi_core_goods_us.index.year == 2025].copy()

    valores_2024 = cpi_core_goods_24.groupby(cpi_core_goods_24.index.month)["MoM %"].first()
    valores_2025 = cpi_core_goods_25.groupby(cpi_core_goods_25.index.month)["MoM %"].first()
    valores_2023 = cpi_core_goods_23.groupby(cpi_core_goods_23.index.month)["MoM %"].first()

    cpi_core_goods_us = cpi_core_goods_us.loc[(cpi_core_goods_us.index.year >= 2010) & (cpi_core_goods_us.index.year <= 2019)]

    percentil_10 = pd.Series(dtype="float64")
    percentil_90 = pd.Series(dtype="float64")

    for mes in range(1, 13):
        dados_mes = cpi_core_goods_us.loc[cpi_core_goods_us.index.month == mes, "MoM %"]
        percentil_10.loc[mes] = dados_mes.quantile(0.10)
        percentil_90.loc[mes] = dados_mes.quantile(0.90)

    valores_dos_graficos = pd.DataFrame({
        "Percentil 10": percentil_10,
        "Percentil 90": percentil_90,
        "Ano de 2024": valores_2024,
        "Ano de 2025": valores_2025,
        "Ano de 2023": valores_2023,
        "Mediana": cpi_core_goods_us.groupby(cpi_core_goods_us.index.month)["MoM %"].median()
    })

    valores_dos_graficos.index = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.fill_between(valores_dos_graficos.index, valores_dos_graficos["Percentil 10"], valores_dos_graficos["Percentil 90"], 
                    color="grey", alpha=0.3, label="10th-90th (2010-2019)")
    ax.plot(valores_dos_graficos.index, valores_dos_graficos["Mediana"], linestyle="dotted", linewidth=2, 
            color="#082631", label="Median")
    ax.plot(valores_dos_graficos.index, valores_dos_graficos["Ano de 2024"], marker="o", linewidth=2, 
            color="#166083", label="2024")
    ax.plot(valores_dos_graficos.index, valores_dos_graficos["Ano de 2025"], marker="o", linewidth=2, 
            color="#37A6D9", label="2025")

    fig.suptitle("Core Goods CPI", fontsize=15, fontweight='bold')
    ax.set_title("MoM % NSA", fontsize=8)
    ax.legend(frameon=False, fontsize=8, loc="upper right")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#d9d9d9")
    ax.spines["bottom"].set_color("#d9d9d9")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15)
    fig.tight_layout()


    return fig
core_goods_nsa = core_goods_nsa()
def core_services_nsa():
    plt.close('all')
    cpi_core_services = fred.get_series('CUUR0000SASLE')
    cpi_core_services_us = pd.DataFrame()
    cpi_core_services_us["MoM %"] = pd.DataFrame(cpi_core_services).pct_change()

    cpi_core_services_23 = cpi_core_services_us.loc[cpi_core_services_us.index.to_series().dt.year == 2023].copy()
    cpi_core_services_24 = cpi_core_services_us.loc[cpi_core_services_us.index.to_series().dt.year == 2024].copy()
    cpi_core_services_25 = cpi_core_services_us.loc[cpi_core_services_us.index.to_series().dt.year == 2025].copy()

    valores_2024 = cpi_core_services_24.groupby(cpi_core_services_24.index.month)["MoM %"].first()
    valores_2025 = cpi_core_services_25.groupby(cpi_core_services_25.index.month)["MoM %"].first()
    valores_2023 = cpi_core_services_23.groupby(cpi_core_services_23.index.month)["MoM %"].first()

    cpi_core_services_us = cpi_core_services_us[(cpi_core_services_us.index.year >= 2010) & (cpi_core_services_us.index.year <= 2019)]

    percentil_10 = pd.DataFrame()
    percentil_90 = pd.DataFrame()

    for mes in range(1, 13):
        dados_mes = cpi_core_services_us[cpi_core_services_us.index.month == mes]["MoM %"]
        percentil_10.loc[mes, "Percentil 10"] = dados_mes.quantile(0.10)
        percentil_90.loc[mes, "Percentil 90"] = dados_mes.quantile(0.90)

    valores_dos_graficos = pd.DataFrame()
    valores_dos_graficos["Percentil 10"] = percentil_10["Percentil 10"]
    valores_dos_graficos["Percentil 90"] = percentil_90["Percentil 90"]
    valores_dos_graficos["Ano de 2024"] = valores_2024
    valores_dos_graficos["Ano de 2025"] = valores_2025
    valores_dos_graficos["Ano de 2023"] = valores_2023
    valores_dos_graficos["Mediana"] = cpi_core_services_us.groupby(cpi_core_services_us.index.month)["MoM %"].median()
    valores_dos_graficos.index = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


    fig, ax = plt.subplots(figsize=(10, 4))

    ax.fill_between(valores_dos_graficos.index, valores_dos_graficos["Percentil 10"], valores_dos_graficos["Percentil 90"], color="grey", alpha=0.3, label="10th-90th (2010-2019)")
    ax.plot(valores_dos_graficos.index, valores_dos_graficos["Mediana"], linestyle="dotted", linewidth=2, color="#082631", label="Median")
    ax.plot(valores_dos_graficos.index, valores_dos_graficos["Ano de 2024"], marker="o", linewidth=2, color="#166083", label="2024")
    ax.plot(valores_dos_graficos.index, valores_dos_graficos["Ano de 2025"], marker="o", linewidth=2, color="#37A6D9", label="2025")
    

    fig.suptitle("Core Services CPI", fontsize=15, fontweight='bold')
    ax.set_title("MoM % NSA", fontsize=8)
    ax.legend(frameon=False, fontsize=8, loc="upper right")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#d9d9d9")
    ax.spines["bottom"].set_color("#d9d9d9")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15)
    fig.tight_layout()

    return fig
core_services_nsa = core_services_nsa()
def core_less_shelter_cars_trucks():
    plt.close('all')
    BLS_API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    API_KEY = "05fb5a8c0bb54ebcb518fbeb8183e758"
    series_id = "CUUR0000SA0L12E4"

    start_year = 1947
    end_year = datetime.now().year
    MAX_YEARS = 20

    all_items_data = []

    for start in range(start_year, end_year + 1, MAX_YEARS):
        stop = min(start + MAX_YEARS - 1, end_year)
        payload = {"seriesid": [series_id], "startyear": str(start), "endyear": str(stop)}
        if API_KEY:
            payload["registrationKey"] = API_KEY
        response = requests.post(BLS_API_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            if 'Results' in data and 'series' in data['Results']:
                all_items_data.extend(data['Results']['series'][0].get('data', []))

    if all_items_data:
        df = pd.DataFrame(all_items_data)
        df['year'] = df['year'].astype(int)
        df['value'] = df['value'].astype(float)
        df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['period'].str[1:] + '-01')
        df.set_index('date', inplace=True)
        df.sort_index(inplace=True)
        
        df_cpi_filtered = pd.DataFrame()
        df_cpi_filtered["MoM %"] = df["value"].pct_change()
        
        df_cpi_23 = df_cpi_filtered[df_cpi_filtered.index.year == 2023]
        df_cpi_24 = df_cpi_filtered[df_cpi_filtered.index.year == 2024]
        df_cpi_25 = df_cpi_filtered[df_cpi_filtered.index.year == 2025]
        
        valores_2024 = df_cpi_24.groupby(df_cpi_24.index.month)["MoM %"].first()
        valores_2025 = df_cpi_25.groupby(df_cpi_25.index.month)["MoM %"].first()
        valores_2023 = df_cpi_23.groupby(df_cpi_23.index.month)["MoM %"].first()
        
        df_cpi_filtered = df_cpi_filtered[(df_cpi_filtered.index.year >= 2010) & (df_cpi_filtered.index.year <= 2019)]
        percentil_10 = df_cpi_filtered.groupby(df_cpi_filtered.index.month)["MoM %"].quantile(0.10)
        percentil_90 = df_cpi_filtered.groupby(df_cpi_filtered.index.month)["MoM %"].quantile(0.90)
        mediana = df_cpi_filtered.groupby(df_cpi_filtered.index.month)["MoM %"].median()
        
        valores_graficos = pd.DataFrame({
            "Percentil 10": percentil_10,
            "Percentil 90": percentil_90,
            "Ano de 2024": valores_2024,
            "Ano de 2025": valores_2025,
            "Ano de 2023": valores_2023,
            "Mediana": mediana
        })
        valores_graficos.index = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
       

    fig, ax = plt.subplots(figsize=(10,4))

    ax.fill_between(valores_graficos.index, valores_graficos["Percentil 10"], valores_graficos["Percentil 90"], color="grey", alpha=0.3, label="10th-90th (2010-2019)")
    ax.plot(valores_graficos.index, valores_graficos["Mediana"], linestyle="dotted", linewidth=2, color="#082631", label="Median")
    ax.plot(valores_graficos.index, valores_graficos["Ano de 2024"], marker="o", linewidth=2, color="#166083", label="2024")
    ax.plot(valores_graficos.index, valores_graficos["Ano de 2025"], marker="o", linewidth=2, color="#37A6D9", label="2025")
   

    fig.suptitle("Core CPI less Shelter, Used Cars and Trucks", fontsize=15, fontweight='bold')
    ax.set_title("MoM % NSA", fontsize=8)
    ax.legend(frameon=False, fontsize=8, loc="upper right")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#d9d9d9")
    ax.spines["bottom"].set_color("#d9d9d9")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax.set_xlabel("Fonte: BLS | Impactus UFRJ", fontsize=8, labelpad=15)
    fig.tight_layout()
    return fig
core_less_shelter_cars_trucks = core_less_shelter_cars_trucks()
def services_less_shelter():
    plt.close("all")
    BLS_API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    API_KEY = "05fb5a8c0bb54ebcb518fbeb8183e758"
    series_id = "CUUR0000SASL2RS"

    start_year = 1947
    end_year = datetime.now().year
    MAX_YEARS = 20

    services_data = []

    for start in range(start_year, end_year + 1, MAX_YEARS):
        stop = min(start + MAX_YEARS - 1, end_year)
        payload = {"seriesid": [series_id], "startyear": str(start), "endyear": str(stop)}
        if API_KEY:
            payload["registrationKey"] = API_KEY
        response = requests.post(BLS_API_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            if 'Results' in data and 'series' in data['Results']:
                services_data.extend(data['Results']['series'][0].get('data', []))

    if services_data:
        df = pd.DataFrame(services_data)
        df['year'] = df['year'].astype(int)
        df['value'] = df['value'].astype(float)
        df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['period'].str[1:] + '-01')
        df.set_index('date', inplace=True)
        df.sort_index(inplace=True)
        
        df_cpi_services = pd.DataFrame()
        df_cpi_services["MoM %"] = df["value"].pct_change()
        
        df_cpi_23 = df_cpi_services[df_cpi_services.index.year == 2023]
        df_cpi_24 = df_cpi_services[df_cpi_services.index.year == 2024]
        df_cpi_25 = df_cpi_services[df_cpi_services.index.year == 2025]
        
        valores_2024 = df_cpi_24.groupby(df_cpi_24.index.month)["MoM %"].first()
        valores_2025 = df_cpi_25.groupby(df_cpi_25.index.month)["MoM %"].first()
        valores_2023 = df_cpi_23.groupby(df_cpi_23.index.month)["MoM %"].first()
        
        df_cpi_services = df_cpi_services[(df_cpi_services.index.year >= 2010) & (df_cpi_services.index.year <= 2019)]
        percentil_10 = df_cpi_services.groupby(df_cpi_services.index.month)["MoM %"].quantile(0.10)
        percentil_90 = df_cpi_services.groupby(df_cpi_services.index.month)["MoM %"].quantile(0.90)
        mediana = df_cpi_services.groupby(df_cpi_services.index.month)["MoM %"].median()
        
        valores_graficos = pd.DataFrame({
            "Percentil 10": percentil_10,
            "Percentil 90": percentil_90,
            "Ano de 2024": valores_2024,
            "Ano de 2025": valores_2025,
            "Ano de 2023": valores_2023,
            "Mediana": mediana
        })
        
        valores_graficos = valores_graficos.reindex(range(1, 13))
        valores_graficos.index = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        

    fig, ax = plt.subplots(figsize=(10,4))

    ax.fill_between(valores_graficos.index, valores_graficos["Percentil 10"], valores_graficos["Percentil 90"], color="grey", alpha=0.3, label="10th-90th (2010-2019)")
    ax.plot(valores_graficos.index, valores_graficos["Mediana"], linestyle="dotted", linewidth=2, color="#082631", label="Median")
    ax.plot(valores_graficos.index, valores_graficos["Ano de 2024"], marker="o", linewidth=2, color="#166083", label="2024")
    ax.plot(valores_graficos.index, valores_graficos["Ano de 2025"], marker="o", linewidth=2, color="#37A6D9", label="2025")
    ax.plot(valores_graficos.index, valores_graficos["Ano de 2023"], marker="o", linewidth=2, color="#0B4C5F", label="2023")

    fig.suptitle("CPI - Services Less Rent Shelter", fontsize=15, fontweight='bold')
    ax.set_title("MoM % NSA", fontsize=8)
    ax.legend(frameon=False, fontsize=8, loc="upper right")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#d9d9d9")
    ax.spines["bottom"].set_color("#d9d9d9")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax.set_xlabel("Fonte: BLS | Impactus UFRJ", fontsize=8, labelpad=15)
    fig.tight_layout()
    return fig
services_less_shelter = services_less_shelter()
def services_less_med():
    
    plt.close("all")
    BLS_API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    API_KEY = "05fb5a8c0bb54ebcb518fbeb8183e758"
    series_id = "CUUR0000SASL5"

    start_year = 1947
    end_year = datetime.now().year
    MAX_YEARS = 20

    services_data = []

    for start in range(start_year, end_year + 1, MAX_YEARS):
        stop = min(start + MAX_YEARS - 1, end_year)
        payload = {"seriesid": [series_id], "startyear": str(start), "endyear": str(stop)}
        if API_KEY:
            payload["registrationKey"] = API_KEY
        response = requests.post(BLS_API_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            if 'Results' in data and 'series' in data['Results']:
                services_data.extend(data['Results']['series'][0].get('data', []))

    if services_data:
        df = pd.DataFrame(services_data)
        df['year'] = df['year'].astype(int)
        df['value'] = df['value'].astype(float)
        df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['period'].str[1:] + '-01')
        df.set_index('date', inplace=True)
        df.sort_index(inplace=True)
        
        df_cpi_services = pd.DataFrame()
        df_cpi_services["MoM %"] = df["value"].pct_change()
        
        df_cpi_23 = df_cpi_services[df_cpi_services.index.year == 2023]
        df_cpi_24 = df_cpi_services[df_cpi_services.index.year == 2024]
        df_cpi_25 = df_cpi_services[df_cpi_services.index.year == 2025]
        
        valores_2024 = df_cpi_24.groupby(df_cpi_24.index.month)["MoM %"].first()
        valores_2025 = df_cpi_25.groupby(df_cpi_25.index.month)["MoM %"].first()
        valores_2023 = df_cpi_23.groupby(df_cpi_23.index.month)["MoM %"].first()
        
        df_cpi_services = df_cpi_services[(df_cpi_services.index.year >= 2010) & (df_cpi_services.index.year <= 2019)]
        percentil_10 = df_cpi_services.groupby(df_cpi_services.index.month)["MoM %"].quantile(0.10)
        percentil_90 = df_cpi_services.groupby(df_cpi_services.index.month)["MoM %"].quantile(0.90)
        mediana = df_cpi_services.groupby(df_cpi_services.index.month)["MoM %"].median()
        
        valores_graficos = pd.DataFrame({
            "Percentil 10": percentil_10,
            "Percentil 90": percentil_90,
            "Ano de 2024": valores_2024,
            "Ano de 2025": valores_2025,
            "Ano de 2023": valores_2023,
            "Mediana": mediana
        })
        
        valores_graficos = valores_graficos.reindex(range(1, 13))
        valores_graficos.index = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        

    fig, ax = plt.subplots(figsize=(10,4))

    ax.fill_between(valores_graficos.index, valores_graficos["Percentil 10"], valores_graficos["Percentil 90"], color="grey", alpha=0.3, label="10th-90th (2010-2019)")
    ax.plot(valores_graficos.index, valores_graficos["Mediana"], linestyle="dotted", linewidth=2, color="#082631", label="Median")
    ax.plot(valores_graficos.index, valores_graficos["Ano de 2024"], marker="o", linewidth=2, color="#166083", label="2024")
    ax.plot(valores_graficos.index, valores_graficos["Ano de 2025"], marker="o", linewidth=2, color="#37A6D9", label="2025")
    

    fig.suptitle("CPI - Services Less Medical Services", fontsize=15, fontweight='bold')
    ax.set_title("MoM % NSA", fontsize=8)
    ax.legend(frameon=False, fontsize=8, loc="upper right")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#d9d9d9")
    ax.spines["bottom"].set_color("#d9d9d9")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax.set_xlabel("Fonte: BLS | Impactus UFRJ", fontsize=8, labelpad=15)
    fig.tight_layout()
    return fig
services_less_med = services_less_med()

#Gráficos CPI SA Main
def sa_main(df,titulo="Título padrão"):
    df_24 = df[df.index.year == 2024]
    df_25 = df[df.index.year == 2025]
    df = df[(df.index.year >= 2010) & (df.index.year <= 2019)]
    percentil_10 = pd.DataFrame()
    percentil_90 = pd.DataFrame()

    for mes in range(1, 13):
        dados_mes = df[df.index.month == mes]["Pct Change"]
        percentil_10.loc[mes, "Percentil 10"] = dados_mes.quantile(0.10)
        percentil_90.loc[mes, "Percentil 90"] = dados_mes.quantile(0.90)

    valores_2024 = []
    valores_2025 = []
    
    for mes in range(1, 13):
        valor_24 = df_24[df_24.index.month == mes]["Pct Change"].values
        valor_25 = df_25[df_25.index.month == mes]["Pct Change"].values
        valores_2024.append(valor_24[0] if len(valor_24) > 0 else None)
        valores_2025.append(valor_25[0] if len(valor_25) > 0 else None)

    valores_dos_graficos = pd.DataFrame()
    valores_dos_graficos["Percentil 10"] = percentil_10["Percentil 10"]
    valores_dos_graficos["Percentil 90"] = percentil_90["Percentil 90"]
    valores_dos_graficos["Ano de 2024"] = valores_2024
    valores_dos_graficos["Ano de 2025"] = valores_2025
    valores_dos_graficos["Mediana"] = df.groupby(df.index.month)["Pct Change"].median()
    valores_dos_graficos.index = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(valores_dos_graficos.index, valores_dos_graficos["Percentil 10"], linestyle="dotted", linewidth=2, color="black", label="10th Percentile")
    ax.plot(valores_dos_graficos.index, valores_dos_graficos["Percentil 90"], linestyle="dotted", linewidth=2, color="black", label="90th Percentile")
    ax.plot(valores_dos_graficos.index, valores_dos_graficos["Mediana"],linewidth=2, color="#082631", label="Median")
    ax.plot(valores_dos_graficos.index, valores_dos_graficos["Ano de 2024"], marker="o", linewidth=2, color="#166083", label="2024")
    ax.plot(valores_dos_graficos.index, valores_dos_graficos["Ano de 2025"], marker="o", linewidth=2, color="#37A6D9", label="2025")


    fig.suptitle(titulo, fontsize=15, fontweight='bold')
    ax.legend(frameon=False, fontsize=8, loc="upper right")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#d9d9d9")
    ax.spines["bottom"].set_color("#d9d9d9")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15)
    fig.tight_layout()


    return fig  
def anualizar(df, titulo="Título padrão", ylim=(-0.02, 0.07)):
    # você tem que me entregar um data frame com a série SA com '"Pct Change from a year ago"', em que eu preciso dos dados desde 2010 até hoje
    df["3 MMA"] = df["Pct Change"].rolling(window=3).mean()
    df["6 MMA"] = df["Pct Change"].rolling(window=6).mean()
    df["3 MMA SAAR"] = (df["3 MMA"] + 1) ** 12 - 1
    df["6 MMA SAAR"] = (df["6 MMA"] + 1) ** 12 - 1  
    # agora dados from a year ago
    goods_graph_values_ya = df[(df.index.year >= 2009)]
    mma3_goods = df["3 MMA SAAR"]
    mma6_goods = df["6 MMA SAAR"]
    mma12_goods = goods_graph_values_ya["Pct Change from a year ago"]
    mean_10_19_goods = df[(df.index.year >= 2010) & (df.index.year <= 2019)]["Pct Change from a year ago"].mean()

    goods_ya = pd.DataFrame({
        "MMA3": mma3_goods,
        "MMA6": mma6_goods,
        "MMA12": mma12_goods,
        "Mean 2010-2019": mean_10_19_goods
    })

    goods_ya.dropna(inplace=True)
    goods_ya = goods_ya.drop(goods_ya.index[0])

    fig, ax = plt.subplots(figsize=(12,5))

    ax.plot(goods_ya.index, goods_ya["MMA3"], linewidth=2, color="#AFABAB", label="3 MMA SAAR", ls=":")
    ax.plot(goods_ya.index, goods_ya["MMA6"], linewidth=2, color="#37A6D9", label="6 MMA SAAR", ls="--")
    ax.plot(goods_ya.index, goods_ya["MMA12"], linewidth=2, color="#082631", label="YoY %")
    ax.plot(goods_ya.index, goods_ya["Mean 2010-2019"], linewidth=2, color="#166083", label="Mean (2010-2019)")

    fig.suptitle(titulo, fontsize=16, fontweight='bold')
    fig.text(0.505, 0.9, "SA Pct Change YoY %", fontsize=9, ha='center', transform=fig.transFigure)

    ax.legend(frameon=False, fontsize=9, loc="upper right")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#c0c0c0")
    ax.spines["bottom"].set_color("#c0c0c0")

    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax.text(goods_ya.index[-1], goods_ya["MMA3"].iloc[-1], f'{goods_ya["MMA3"].iloc[-1]:.2%}', color="#AFABAB", fontsize=7, ha='left')
    ax.text(goods_ya.index[-1], goods_ya["MMA6"].iloc[-1], f'{goods_ya["MMA6"].iloc[-1]:.2%}', color="#37A6D9", fontsize=7, ha='left')
    ax.text(goods_ya.index[-1], goods_ya["MMA12"].iloc[-1], f'{goods_ya["MMA12"].iloc[-1]:.2%}', color="#082631", fontsize=7, ha='left')
    ax.text(goods_ya.index[-1], goods_ya["Mean 2010-2019"].iloc[-1], f'{goods_ya["Mean 2010-2019"].iloc[-1]:.2%}', color="#166083", fontsize=7, ha='left')
    ax.set_ylim(ylim)
    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=9, labelpad=15)

    fig.tight_layout()

    return fig


#cpi headline
pc = fred.get_series("CPIAUCSL")
cpi = pd.DataFrame()
cpi["Nível de preços"] = pd.DataFrame(pc)
cpi["Pct Change"] = cpi['Nível de preços'].pct_change()
cpi["Pct Change from a year ago"] = cpi['Nível de preços'].pct_change(periods=12)
graf_sa_cpi = sa_main(cpi,titulo="CPI - Headline")
graf_sa_ya_head = anualizar(cpi,titulo="CPI - Headline", ylim=(-0.02, 0.07))

#cpi core
pc = fred.get_series("CPILFESL")
cpi_core = pd.DataFrame()
cpi_core["Nível de preços do núcleo"] = pd.DataFrame(pc)
cpi_core["Pct Change"] = cpi_core['Nível de preços do núcleo'].pct_change()
cpi_core["Pct Change from a year ago"] = cpi_core['Nível de preços do núcleo'].pct_change(periods=12)
graf_sa_core = sa_main(cpi_core, titulo="Core CPI")
graf_sa_ya_core = anualizar(cpi_core, titulo= "Core CPI", ylim=(0, 0.07))

# core goods
pc = fred.get_series("CUSR0000SACL1E")
cpi_core_goods = pd.DataFrame()
cpi_core_goods["Nível de preços"] = pd.DataFrame(pc)
cpi_core_goods["Pct Change"] = cpi_core_goods['Nível de preços'].pct_change()
cpi_core_goods["Pct Change from a year ago"] = cpi_core_goods['Nível de preços'].pct_change(periods=12)
graf_sa_core_goods = sa_main(cpi_core_goods, titulo= "CPI - Core Goods")
graf_sa_ya_cgoods = anualizar(cpi_core_goods, titulo= "CPI - Core Goods", ylim=(-0.02, 0.06))


#core services
pc = fred.get_series("CUSR0000SASLE")
cpi_core_services = pd.DataFrame()
cpi_core_services["Nível de preços"] = pd.DataFrame(pc)
cpi_core_services["Pct Change"] = cpi_core_services['Nível de preços'].pct_change()
cpi_core_services["Pct Change from a year ago"] = cpi_core_services['Nível de preços'].pct_change(periods=12)
graf_sa_core_services = sa_main(cpi_core_services, titulo= "CPI - Core Services")
graf_sa_ya_cservices = anualizar(cpi_core_services, titulo= "CPI - Core Services", ylim=(0, 0.07))

#food and beverages
pc = fred.get_series("CPIFABSL")
cpi_food = pd.DataFrame()
cpi_food["Nível de preços"] = pd.DataFrame(pc)
cpi_food["Pct Change"] = cpi_food['Nível de preços'].pct_change()
cpi_food["Pct Change from a year ago"] = cpi_food['Nível de preços'].pct_change(periods=12)
graf_sa_food = sa_main(cpi_food, titulo= "CPI - Food and Beverages")
graf_sa_ya_food = anualizar(cpi_food, titulo= "CPI - Food and Beverages", ylim=(-0.01, 0.08))

#energy
pc = fred.get_series("CPIENGSL")
cpi_energy = pd.DataFrame()
cpi_energy["Nível de preços"] = pd.DataFrame(pc)
cpi_energy["Pct Change"] = cpi_energy['Nível de preços'].pct_change()
cpi_energy["Pct Change from a year ago"] = cpi_energy['Nível de preços'].pct_change(periods=12)
graf_sa_energy = sa_main(cpi_energy, titulo= "CPI - Energy")
graf_sa_ya_energy = anualizar(cpi_energy, titulo= "CPI - Energy", ylim=(-0.4, 0.6))

            




# Função para gráficos do PCE
def mostrar_grafico_pce_headline():
    plt.close("all")
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
    plt.close("all")
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
    plt.close("all")
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
    plt.close("all")
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
    plt.close("all")
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
    plt.close("all")
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
    plt.close("all")
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
    plt.close("all")
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
    plt.close("all")
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
    plt.close("all")
    u = fred.get_series("UNRATE")
    unrate = pd.DataFrame()
    unrate["UnRate"] = pd.DataFrame(u)
    unrate["3 MAA"] = unrate["UnRate"].rolling(window=3).mean()
    unrate["Min 12 m"]= unrate["UnRate"].rolling(window=12,min_periods=1).min()
    unrate["Sahm Rule"] = unrate["3 MAA"] - unrate["Min 12 m"]
    unrate = unrate.dropna()
    unrate = unrate.tail(450)
    unr = unrate.tail(200).copy()
    unr["UnRate"] = unr["UnRate"] / 100
    unr["Média de 12 meses"] = unr["UnRate"].rolling(window=12).mean()
    unr = unr.tail(24)

    fig, ax = plt.subplots(figsize=(12, 5))

    bars = ax.bar(unr.index, unr["UnRate"], label="Unemployment Rate", width=14, color="#082631")

    ax.set_title("Pct SA", fontsize=8, style='italic', pad=10)
    fig.suptitle("US: Unemployment Rate", fontsize=15, fontweight='bold')
    ax.legend(frameon=False, fontsize=8, loc="upper right")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color('#d9d9d9')

    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
    ax.set_ylim(0.03, 0.045)
    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.0003,
                f'{height:.1%}', ha='center', va='bottom', fontsize=8, color="#082631")

    plt.tight_layout()


    return fig
unrate = unrate()
def participation_rate():
    plt.close("all")
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
    plt.close("all")
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
    plt.close('all')
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
    plt.close('all')
    from matplotlib.ticker import FuncFormatter
    fred = Fred(api_key="672d5598c8a41df9397cc5eb92c02d5e")

    jr = fred.get_series("JTSJOR")
    ur = fred.get_series("UNRATE")

    beveridge_data = pd.DataFrame(index=jr.index)
    beveridge_data["Vacancy rate"] = jr / 100
    beveridge_data["Unemployment rate"] = ur / 100
    beveridge_data = beveridge_data[beveridge_data.index.year >= 2000]

    beveridge_data["Beveridge curve"] = beveridge_data["Vacancy rate"] / beveridge_data["Unemployment rate"]

    wage_growth = pd.DataFrame()
    wage_growth["AVG Hourly Earnings"] = fred.get_series("CES0500000003")
    wage_growth["YoY %"] = wage_growth["AVG Hourly Earnings"].pct_change(periods=12)

    beveridge_data = beveridge_data[beveridge_data.index >= "2008-01-01"]
    wage_growth = wage_growth[wage_growth.index >= "2008-01-01"]

    fig, ax1 = plt.subplots(figsize=(12,5))

    ax1.plot(beveridge_data.index, beveridge_data["Beveridge curve"], label="Beveridge curve", linewidth=2.5, color="#166083")
    ax1.set_ylabel("Vacancy Rate / Unemployment Rate", fontsize=8, labelpad=15)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_color("#d9d9d9")
    ax1.spines["bottom"].set_color("#d9d9d9")
    ax1.set_ylim(0, 2)

    # Anotação último valor Beveridge Curve
    last_date_b = beveridge_data.index[-1]
    last_value_b = beveridge_data["Beveridge curve"].iloc[-1]
    ax1.annotate(f'{last_value_b:.2f}', 
                xy=(last_date_b, last_value_b), 
                xytext=(10, 0), 
                textcoords='offset points',
                va='center',
                fontsize=8,
                color="#166083")

    ax2 = ax1.twinx()
    ax2.plot(wage_growth.index, wage_growth["YoY %"], label="Wage growth", linewidth=2.5, color="#082631")
    ax2.set_ylabel("Wage growth YoY %", fontsize=8, labelpad=15)
    ax2.spines["top"].set_visible(False)
    ax2.spines["left"].set_visible(False)
    ax2.spines["right"].set_color("#d9d9d9")
    ax2.spines["bottom"].set_color("#d9d9d9")
    ax2.set_ylim(0, 0.1)
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y)))

    # Anotação último valor Wage Growth
    last_date_w = wage_growth.index[-1]
    last_value_w = wage_growth["YoY %"].iloc[-1]
    ax2.annotate(f'{last_value_w:.1%}', 
                xy=(last_date_w, last_value_w), 
                xytext=(10, 0), 
                textcoords='offset points',
                va='center',
                fontsize=8,
                color="#082631")

    plt.suptitle("Beveridge curve vs Wage Tracker", fontsize=15, fontweight='bold')
    ax1.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15)

    plt.tight_layout()

    return fig
beveridge_curve = plot_beveridge_curve()
beveridge_ratio = plot_beveridge_ratio()
def layoffs_and_discharges():
    plt.close('all')
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
    plt.close('all')
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
    plt.close('all')
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
    plt.close('all')
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


# Gráficos Payroll
def plot_total_payroll():
    plt.close('all')
    dados = fred.get_series("PAYEMS")
    
    df = pd.DataFrame(dados, columns=["Total"])
    df.index.name = "Date"
    df["Criação Líquida de Postos de Trabalho"] = df["Total"].diff()
    payroll_2324 = df.tail(50)
    indice = payroll_2324.index

    fig, ax = plt.subplots(figsize=(12,5))
    ax.bar(indice, payroll_2324["Criação Líquida de Postos de Trabalho"], width=15, color="#184253")
    ax.axhline(0, color='black', linewidth=1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#d9d9d9')
    ax.set_title("Net Changes (Thousands) SA", fontsize=8, style='italic')
    fig.suptitle("US Payroll", fontweight="bold", fontsize=15)
    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15)
    plt.tight_layout()
    return fig
payroll = plot_total_payroll()
def plot_private_vs_government_payroll():
    plt.close('all')
    dados = fred.get_series("PAYEMS")
    df = pd.DataFrame(dados, columns=["Total"])
    df.index.name = "Date"
    df["Criação Líquida de Postos de Trabalho"] = df["Total"].diff()
    payroll_2324 = df.tail(50)
    indice = payroll_2324.index

    government_payroll_data = fred.get_series("USGOVT")
    goverment_payroll = pd.DataFrame(government_payroll_data, columns=["Total"])
    goverment_payroll.index.name = "Date"
    goverment_payroll["Criação Líquida de Postos de Trabalho no Governo"] = goverment_payroll["Total"].diff()
    gov = goverment_payroll.tail(50)

    private_payroll_data = fred.get_series("USPRIV")
    private_payroll = pd.DataFrame(private_payroll_data, columns=["Total"])
    private_payroll.index.name = "Date"
    private_payroll["Criação Líquida de Postos de Trabalho no Setor Privado"] = private_payroll["Total"].diff()
    priv = private_payroll.tail(50)

    priv_values = np.array(priv["Criação Líquida de Postos de Trabalho no Setor Privado"])
    gov_values = np.array(gov["Criação Líquida de Postos de Trabalho no Governo"])

    bottom_gov = np.where(gov_values >= 0, priv_values, 0)
    bottom_priv = np.where(gov_values < 0, gov_values, 0)

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(indice, priv_values, width=15, color="#166083", label="Private Payroll", bottom=bottom_priv)
    ax.bar(indice, gov_values, width=15, color="#082631", label="Government Payroll", bottom=bottom_gov)
    ax.plot(indice, payroll_2324["Criação Líquida de Postos de Trabalho"], color="#184253", label="Payroll", linewidth=2)
    ax.axhline(0, color='black', linewidth=1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#d9d9d9')
    ax.set_title("Net Changes (Thousands) SA and Contributions", fontsize=10, style='italic')
    fig.suptitle("US Payroll: Government x Private", fontweight="bold", fontsize=15)
    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15)
    ax.legend(frameon=False, loc='upper right', fontsize=10)
    plt.tight_layout()
    return fig
private_vs_government = plot_private_vs_government_payroll()
def plot_goods_vs_services_payroll():
    plt.close('all')
    dados = fred.get_series("PAYEMS")
    df = pd.DataFrame(dados, columns=["Total"])
    df.index.name = "Date"
    df["Criação Líquida de Postos de Trabalho"] = df["Total"].diff()
    payroll_2324 = df.tail(50)
    indice = payroll_2324.index

    private_payroll_data = fred.get_series("USPRIV")
    private_payroll = pd.DataFrame(private_payroll_data, columns=["Total"])
    private_payroll.index.name = "Date"
    private_payroll["Criação Líquida de Postos de Trabalho no Setor Privado"] = private_payroll["Total"].diff()
    priv = private_payroll.tail(50)

    goods_payroll_data = fred.get_series("USGOOD")
    goodp_payroll = pd.DataFrame(goods_payroll_data, columns=["Total"])
    goodp_payroll.index.name = "Date"
    goodp_payroll["Criação Líquida de Postos de Trabalho em Bens no Setor Privado"] = goodp_payroll["Total"].diff()
    good = goodp_payroll.tail(50)

    services_payroll_data = fred.get_series("CES0800000001")
    services_private_payroll = pd.DataFrame(services_payroll_data, columns=["Total"])
    services_private_payroll.index.name = "Date"
    services_private_payroll["Criação Líquida de Postos em Serviços no Setor Privado"] = services_private_payroll["Total"].diff()
    servp = services_private_payroll.tail(50)

    servp_values = np.array(servp["Criação Líquida de Postos em Serviços no Setor Privado"])
    good_values = np.array(good["Criação Líquida de Postos de Trabalho em Bens no Setor Privado"])

    bottom_good = np.where(good_values >= 0, servp_values, 0)
    bottom_serv = np.where(good_values < 0, good_values, 0)

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(indice, servp_values, width=15, color="#082631", label="Service Providing")
    ax.bar(indice, good_values, width=15, color="#166083", label="Goods-Producing", bottom=bottom_good)
    ax.plot(indice, priv["Criação Líquida de Postos de Trabalho no Setor Privado"], color="#184253", label="Private Payroll", linewidth=2)
    ax.axhline(0, color='black', linewidth=1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#d9d9d9')
    ax.set_title("Net Changes (Thousands) SA and Contributions", fontsize=10, style='italic')
    fig.suptitle("US Private Payroll: Goods x Services", fontweight="bold", fontsize=15)
    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15)
    ax.legend(frameon=False, loc='upper right', fontsize=10)
    plt.tight_layout()
    return fig
goods_vs_services_payroll = plot_goods_vs_services_payroll()
def plot_cic_payroll():
    plt.close('all')
    dados = fred.get_series("PAYEMS")
    df = pd.DataFrame(dados, columns=["Total"])
    df.index.name = "Date"
    df["Criação Líquida de Postos de Trabalho"] = df["Total"].diff()
    payroll_2324 = df.tail(50)
    indice = payroll_2324.index

    government_payroll_data = fred.get_series("USGOVT")
    goverment_payroll = pd.DataFrame(government_payroll_data, columns=["Total"])
    goverment_payroll.index.name = "Date"
    goverment_payroll["Criação Líquida de Postos de Trabalho no Governo"] = goverment_payroll["Total"].diff()
    gov = goverment_payroll.tail(50)

    private_payroll_data = fred.get_series("USPRIV")
    private_payroll = pd.DataFrame(private_payroll_data, columns=["Total"])
    private_payroll.index.name = "Date"
    private_payroll["Criação Líquida de Postos de Trabalho no Setor Privado"] = private_payroll["Total"].diff()
    priv = private_payroll.tail(50)

    goods_payroll_data = fred.get_series("USGOOD")
    goodp_payroll = pd.DataFrame(goods_payroll_data, columns=["Total"])
    goodp_payroll.index.name = "Date"
    goodp_payroll["Criação Líquida de Postos de Trabalho em Bens no Setor Privado"] = goodp_payroll["Total"].diff()
    good = goodp_payroll.tail(50)

    services_payroll_data = fred.get_series("CES0800000001")
    services_private_payroll = pd.DataFrame(services_payroll_data, columns=["Total"])
    services_private_payroll.index.name = "Date"
    services_private_payroll["Criação Líquida de Postos em Serviços no Setor Privado"] = services_private_payroll["Total"].diff()
    servp = services_private_payroll.tail(50)

    #Pegando dados de acíclicos
    dados_private_ed_health = fred.get_series("USEHS")
    private_ed_health = pd.DataFrame(dados_private_ed_health, columns= ["Total"])
    private_ed_health["Criação líquida em acíclicos"] = private_ed_health["Total"].diff()
    acyclic = private_ed_health.tail(50).copy()
    acyclic["Private ex education and Health care and Social Ass."] = priv["Criação Líquida de Postos de Trabalho no Setor Privado"] - acyclic["Criação líquida em acíclicos"]
    acyclic["Government + Health Care + Education"] = gov["Criação Líquida de Postos de Trabalho no Governo"] + acyclic["Criação líquida em acíclicos"]
    acyclic["P1"] = payroll_2324["Criação Líquida de Postos de Trabalho"]
    acyclic["P2"] = acyclic["Private ex education and Health care and Social Ass."] + acyclic["Government + Health Care + Education"]
    
    #colocar os acíclicos em média de 3 meses
    maa = pd.DataFrame()
    maa["3 MAA Private ex education and Health care and Social Ass."] = acyclic["Private ex education and Health care and Social Ass."].rolling(window=3).mean()
    maa["3 MAA Government + Health Care + Education"] = acyclic["Government + Health Care + Education"].rolling(window=3).mean()
    maa["3 MAA Payroll"] = payroll_2324["Criação Líquida de Postos de Trabalho"].rolling(window=3).mean(3)
    maa = maa.dropna()
    ind = maa.index

    cic_values = np.array(maa["3 MAA Private ex education and Health care and Social Ass."])
    acic_values = np.array(maa["3 MAA Government + Health Care + Education"])

    cic_positive = np.where(cic_values > 0, cic_values, 0)
    cic_negative = np.where(cic_values < 0, cic_values, 0)

    acic_positive = np.where(acic_values > 0, acic_values, 0)
    acic_negative = np.where(acic_values < 0, acic_values, 0)

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.bar(ind, cic_positive, width=15, color="#082631", label="Private ex education and Health care and Social Ass.")
    ax.bar(ind, cic_negative, width=15, color="#082631")
    ax.bar(ind, acic_positive, width=15, color="#37A6D9", label="Government + Health Care + Education", bottom=cic_positive)
    ax.bar(ind, acic_negative, width=15, color="#37A6D9", bottom=cic_negative)
    ax.plot(ind, maa["3 MAA Payroll"], linewidth=2, label="Payroll", color="#166083")

    ax.axhline(0, color='black', linewidth=1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#d9d9d9')
    ax.xaxis.grid(False)

    ax.set_title("Net Changes (Thousands) 3 MMA SA and Contributions", fontsize=10, style='italic', pad=10)
    fig.suptitle("US: Payroll", fontweight="bold", fontsize=15)
    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15)
    ax.legend(frameon=False, loc='upper right', fontsize=10)

    plt.tight_layout()
    return fig
cic_payroll = plot_cic_payroll()
def plot_breakdown_payroll():
    plt.close('all')
    p2 = fred.get_series("USPRIV")
    ac = fred.get_series("USEHS")
    pl = fred.get_series("PAYEMS")
    breakdown = pd.DataFrame()
    breakdown_change = pd.DataFrame()
    breakdown["Total Payroll"] = pd.DataFrame(pl)
    breakdown["Total Private"] = pd.DataFrame(p2)
    breakdown["Total private acyclicals"] = pd.DataFrame(ac)
    breakdown_change["Criação líquida de empregos"] = breakdown["Total Payroll"].diff()
    breakdown_change["Criação líquida de empregos no setor privado"] = breakdown["Total Private"].diff()
    breakdown_change["Criação líquida em acyclicals"] = breakdown["Total private acyclicals"].diff()
    breakdown_change["Private ex acyclicals"] = breakdown_change["Criação líquida de empregos no setor privado"] - breakdown_change["Criação líquida em acyclicals"]
    breakdown_change = breakdown_change.dropna()
    breakdown_f = breakdown_change.rolling(window=3).mean().tail(150)
    indc = breakdown_f.index    

    plt.rcParams['font.family'] = 'Arial'
    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(indc, breakdown_f["Criação líquida de empregos"], linewidth=2, color="#082631", label="Payroll")
    ax.plot(indc, breakdown_f["Criação líquida de empregos no setor privado"], linewidth=2, color="#166083", label="Private Payroll")
    ax.plot(indc, breakdown_f["Private ex acyclicals"], linewidth=2, color="#37A6D9", label="Private ex acyclicals")

    for column, color in zip(["Criação líquida de empregos", "Criação líquida de empregos no setor privado", "Private ex acyclicals"],
                            ["#082631", "#166083", "#37A6D9"]):
        ax.text(indc[-1], breakdown_f[column].iloc[-1], f"{breakdown_f[column].iloc[-1]:,.0f}",
                fontsize=10, color=color, verticalalignment='bottom', horizontalalignment='left')

    ax.axhline(0, color='black', linewidth=1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#d9d9d9')
    ax.xaxis.grid(False)
    ax.set_ylim(0, 400)

    ax.set_title("Thousands SA (3 MAA)", fontsize=10, style='italic', pad=10)
    fig.suptitle("US: Payroll - Total Payroll vs Breakdown", fontweight="bold", fontsize=15)
    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15)
    ax.legend(frameon=False, loc='upper right', fontsize=10)

    plt.tight_layout()
    return fig
breakdown_payroll = plot_breakdown_payroll()
def plot_sam_rule():
    # Obtenção e processamento dos dados
    plt.close('all')
    p = fred.get_series("USPRIV")
    privado = pd.DataFrame()
    privado["Private"] = pd.DataFrame(p)
    privado["Private pct change"] = privado["Private"].pct_change().rolling(window=3).mean()
    privado["Private pct change from a year ago"] = (1 + privado["Private pct change"]).rolling(window=12).apply(np.prod, raw=True) - 1
    privado = privado.dropna()
    privado = privado.tail(450)
    index1 = privado.index

    u = fred.get_series("UNRATE")
    unrate = pd.DataFrame()
    unrate["UnRate"] = pd.DataFrame(u)
    unrate["3 MAA"] = unrate["UnRate"].rolling(window=3).mean()
    unrate["Min 12 m"] = unrate["UnRate"].rolling(window=12, min_periods=1).min()
    unrate["Sahm Rule"] = unrate["3 MAA"] - unrate["Min 12 m"]
    unrate = unrate.dropna()
    unrate = unrate.tail(450)

    r = fred.get_series("USRECD")
    recessions = pd.DataFrame(r, columns=["USRECD"])
    recessao_mensal = recessions.resample('MS').first()
    recessao_mensal = recessao_mensal.tail(450)
    index2 = unrate.index

    # Plotagem
    plt.rcParams['font.family'] = 'Arial'
    fig, ax1 = plt.subplots(figsize=(12, 5))

    # Plotando a variação percentual do payroll privado
    ax1.plot(index1, privado["Private pct change from a year ago"], label="Private YoY %", color="#082631", linewidth=2)
    ax1.set_ylim(-0.03, 0.06)
    ax1.tick_params(axis='y', labelcolor="#082631")
    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    # Plotando a regra de Sahm
    ax2 = ax1.twinx()
    ax2.plot(index1, unrate["Sahm Rule"], label="Sahm Rule", color="#37A6D9", linewidth=2)
    ax2.set_ylim(-0.5, 1)
    ax2.tick_params(axis='y', labelcolor="#37A6D9")
    ax2.axhline(y=0.5, linestyle="--", color="#37A6D9", linewidth=1)

    # Adicionando áreas de recessão
    ax1.fill_between(recessao_mensal.index, 0, 1, where=recessao_mensal["USRECD"] == 1, color='gray', alpha=0.3, transform=ax1.get_xaxis_transform())

    # Legendas e formatação
    ax1.legend(frameon=False, loc="upper right", bbox_to_anchor=(1, 1), fontsize=10)
    ax2.legend(frameon=False, loc="upper right", bbox_to_anchor=(1, 0.95), fontsize=10)

    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ax1.spines['bottom'].set_color('#d9d9d9')
    ax1.xaxis.grid(False)

    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.spines['bottom'].set_color('#d9d9d9')

    plt.suptitle("US: Private Payroll vs Sahm Rule", fontsize=15, fontweight='bold')
    plt.title("3 MMA SAAR %", fontsize=10, style='italic', pad=10)
    ax1.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15)
    plt.axhline(0, color='black', linewidth=1)
    plt.tight_layout()
    return fig
sahm_rule = plot_sam_rule()
def ordering():
    #DF de ordering
    plt.close('all')
    ht = fred.get_series("CES6562000101")
    health_care = pd.DataFrame()
    health_care["All employees"] = pd.DataFrame(ht)
    health_care["Diff"] =health_care["All employees"].diff()
    health_care["Média de 12 meses"]= health_care["Diff"].rolling(window=12).mean()

    rt = fred.get_series("USTRADE")
    retail_trade = pd.DataFrame()
    retail_trade["All employees"] = pd.DataFrame(rt)
    retail_trade["Diff"] =retail_trade["All employees"].diff()
    retail_trade["Média de 12 meses"]= retail_trade["Diff"].rolling(window=12).mean()

    lh = fred.get_series("USLAH")
    leisure_hospitality = pd.DataFrame()
    leisure_hospitality["All employees"] = pd.DataFrame(lh)
    leisure_hospitality["Diff"] =leisure_hospitality["All employees"].diff()
    leisure_hospitality["Média de 12 meses"]= leisure_hospitality["Diff"].rolling(window=12).mean()

    pb = fred.get_series("USPBS")
    professionalb_services = pd.DataFrame()
    professionalb_services["All employees"] = pd.DataFrame(pb)
    professionalb_services["Diff"] =professionalb_services["All employees"].diff()
    professionalb_services["Média de 12 meses"]= professionalb_services["Diff"].rolling(window=12).mean()

    sa = fred.get_series("CES6562400001")
    social_assistance = pd.DataFrame()
    social_assistance["All employees"] = pd.DataFrame(sa)
    social_assistance["Diff"] =social_assistance["All employees"].diff()
    social_assistance["Média de 12 meses"]= social_assistance["Diff"].rolling(window=12).mean()

    lg = fred.get_series("CES9093000001")
    local_government = pd.DataFrame()
    local_government["All employees"] = pd.DataFrame(lg)
    local_government["Diff"] =local_government["All employees"].diff()
    local_government["Média de 12 meses"]= local_government["Diff"].rolling(window=12).mean()

    fa = fred.get_series("USFIRE")
    financial_activity = pd.DataFrame()
    financial_activity["All employees"] = pd.DataFrame(fa)
    financial_activity["Diff"] =financial_activity["All employees"].diff()
    financial_activity["Média de 12 meses"]= financial_activity["Diff"].rolling(window=12).mean()

    ped = fred.get_series("CES6561000001")
    private_education = pd.DataFrame()
    private_education["All employees"] = pd.DataFrame(ped)
    private_education["Diff"] =private_education["All employees"].diff()
    private_education["Média de 12 meses"]= private_education["Diff"].rolling(window=12).mean()

    sg = fred.get_series("CES9092000001")
    state_government = pd.DataFrame()
    state_government["All employees"] = pd.DataFrame(sg)
    state_government["Diff"] =state_government["All employees"].diff()
    state_government["Média de 12 meses"]= state_government["Diff"].rolling(window=12).mean()

    inf = fred.get_series("USINFO")
    information = pd.DataFrame()
    information["All employees"] = pd.DataFrame(inf)
    information["Diff"] =information["All employees"].diff()
    information["Média de 12 meses"]= information["Diff"].rolling(window=12).mean()

    tw = fred.get_series("CES4300000001")
    transportation_warehousing = pd.DataFrame()
    transportation_warehousing["All employees"] = pd.DataFrame(tw)
    transportation_warehousing["Diff"] =transportation_warehousing["All employees"].diff()
    transportation_warehousing["Média de 12 meses"]= transportation_warehousing["Diff"].rolling(window=12).mean()

    os = fred.get_series("USSERV")
    other_services = pd.DataFrame()
    other_services["All employees"] = pd.DataFrame(os)
    other_services["Diff"] =other_services["All employees"].diff()
    other_services["Média de 12 meses"]= other_services["Diff"].rolling(window=12).mean()

    cons = fred.get_series("USCONS")
    construction = pd.DataFrame()
    construction["All employees"] = pd.DataFrame(cons)
    construction["Diff"] =construction["All employees"].diff()
    construction["Média de 12 meses"]= construction["Diff"].rolling(window=12).mean()

    fed = fred.get_series("CES9091000001")
    federal = pd.DataFrame()
    federal["All employees"] = pd.DataFrame(fed)
    federal["Diff"] =federal["All employees"].diff()
    federal["Média de 12 meses"]= federal["Diff"].rolling(window=12).mean()

    log = fred.get_series("CES1011330001")
    logging = pd.DataFrame()
    logging["All employees"] = pd.DataFrame(log)
    logging["Diff"] =logging["All employees"].diff()
    logging["Média de 12 meses"]= logging["Diff"].rolling(window=12).mean()

    ut = fred.get_series("CES4422000001")
    utilities = pd.DataFrame()
    utilities["All employees"] = pd.DataFrame(ut)
    utilities["Diff"] =utilities["All employees"].diff()
    utilities["Média de 12 meses"]= utilities["Diff"].rolling(window=12).mean()

    mn = fred.get_series("CES1021200001")
    mining_ex_oil_gas = pd.DataFrame()
    mining_ex_oil_gas["All employees"] = pd.DataFrame(mn)
    mining_ex_oil_gas["Diff"] =mining_ex_oil_gas["All employees"].diff()
    mining_ex_oil_gas["Média de 12 meses"]= mining_ex_oil_gas["Diff"].rolling(window=12).mean()

    og = fred.get_series("CES1021100001")
    oil_gas = pd.DataFrame()
    oil_gas["All employees"] = pd.DataFrame(og)
    oil_gas["Diff"] =oil_gas["All employees"].diff()
    oil_gas["Média de 12 meses"]= oil_gas["Diff"].rolling(window=12).mean()

    wt = fred.get_series("USWTRADE")
    whole_sale_trade = pd.DataFrame()
    whole_sale_trade["All employees"] = pd.DataFrame(wt)
    whole_sale_trade["Diff"] =whole_sale_trade["All employees"].diff()
    whole_sale_trade["Média de 12 meses"]= whole_sale_trade["Diff"].rolling(window=12).mean()

    man = fred.get_series("MANEMP")
    manufacturing = pd.DataFrame()
    manufacturing["All employees"] = pd.DataFrame(man)
    manufacturing["Diff"] =manufacturing["All employees"].diff()
    manufacturing["Média de 12 meses"]= manufacturing["Diff"].rolling(window=12).mean()

    # Define Arial como a fonte padrão
   

    # Dados
    setores = {
        "Health Care": health_care,
        "Retail Trade": retail_trade,
        "Leisure & Hospitality": leisure_hospitality,
        "Professional & Business Services": professionalb_services,
        "Social Assistance": social_assistance,
        "Local Government": local_government,
        "Financial Activities": financial_activity,
        "Private Education": private_education,
        "State Government": state_government,
        "Information": information,
        "Transportation & Warehousing": transportation_warehousing,
        "Other Services": other_services,
        "Construction": construction,
        "Federal Government": federal,
        "Logging": logging,
        "Utilities": utilities,
        "Mining (Ex Oil & Gas)": mining_ex_oil_gas,
        "Oil & Gas": oil_gas,
        "Wholesale Trade": whole_sale_trade,
        "Manufacturing": manufacturing
    }

    labels = list(setores.keys())
    diff_atual = [df["Diff"].iloc[-1] for df in setores.values()]
    diff_anterior = [df["Diff"].iloc[-2] for df in setores.values()]
    media_12m = [df["Média de 12 meses"].iloc[-1] for df in setores.values()]

    # Plot
    fig, ax = plt.subplots(figsize=(12, 5))  # Igual ao figsize do outro gráfico
    y = np.arange(len(labels))
    width = 0.3

    # Barras
    ax.barh(y - width, media_12m, width, label="12MMA", color="#082631")
    ax.barh(y, diff_anterior, width, label="Previous month", color="#37A6D9")
    ax.barh(y + width, diff_atual, width, label="This month", color="#AFABAB")

    # Y ticks e labels
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=10)

    # Título e legenda
    fig.suptitle("US: Payroll - Category Breakdown", fontsize=15, fontweight='bold')
    ax.set_title("Net Thousand SA", fontsize=10, style='italic', pad=10)
    ax.legend(frameon=False, fontsize=10, loc="upper right")

    # Eixos e bordas
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#d9d9d9")
    ax.spines["bottom"].set_color("#d9d9d9")

    # Formatando os valores do eixo x com separador de milhar (pode mudar para porcentagem se preferir)
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{int(x):,}'))

    # Labels dos eixos
    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15)

    # Layout
    plt.tight_layout()
    return fig
ordering = ordering()

#Gráficos Salários
def average_hourly_earnings():
    plt.close('all')
    #Average hourly earnings
    avgh = fred.get_series("CES0500000003")
    ahe = pd.DataFrame()
    ahe["Average Hourly earnings"] = pd.DataFrame(avgh)
    ahe["Pct Change"] = ahe["Average Hourly earnings"].pct_change()
    ahe["Acumulado de 12 meses"] = (1 + ahe["Pct Change"]).rolling(window=12).apply(np.prod, raw=True) - 1
    ahe["3 MMA"] = ahe["Acumulado de 12 meses"].rolling(window=3).mean()
    ahe = ahe.dropna()
    ahe = ahe.tail(48)
    i = ahe.index

    fig, ax_avghe = plt.subplots(figsize=(12,5))

    ax_avghe.plot(i, ahe["Acumulado de 12 meses"], label="YoY %", color="#082631", linewidth=2.5)
    ax_avghe.plot(i, ahe["3 MMA"], label="3 MMA", color="#37A6D9", linewidth=2.5)

    ax_avghe.tick_params(axis='y', labelcolor="#082631")
    ax_avghe.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))


    fig.suptitle("US: Average Hourly Earnings", fontsize=15, fontweight='bold')
    ax_avghe.set_title("Pct Change SA", fontsize=10, style='italic')

    ax_avghe.legend(frameon=False, fontsize=10, loc="upper right", bbox_to_anchor=(1, 1))


    ax_avghe.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15)

    ax_avghe.axhline(0, color='black', linewidth=1)

    ax_avghe.spines["top"].set_visible(False)
    ax_avghe.spines["right"].set_visible(False)
    ax_avghe.spines["left"].set_visible(False)
    ax_avghe.spines["bottom"].set_color('#d9d9d9')


    plt.tight_layout()
    return fig
average_hourly_earnings = average_hourly_earnings()
def labor_cost():
    #Unit Labor Cost vs Productivity
    
    plt.close('all')
    pr = fred.get_series("OPHNFB")
    labor_productivity = pd.DataFrame()
    labor_productivity["Produtividade do Trabalho"] = pd.DataFrame(pr)
    labor_productivity["Pct Change from a Year Ago"] = (labor_productivity["Produtividade do Trabalho"] / labor_productivity["Produtividade do Trabalho"].shift(4)) - 1
    labor_productivity = labor_productivity.tail(100)
    lbc = fred.get_series("PRS85006112")
    average_labor_cost = pd.DataFrame()
    average_labor_cost["Unit Labor Cost pct change"] = pd.DataFrame(lbc)
    average_labor_cost["Pct Change do jeito que eu quero"] = average_labor_cost["Unit Labor Cost pct change"]/100
    average_labor_cost = average_labor_cost.tail(100)
    index = average_labor_cost.index
    index1 = labor_productivity.index

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(index, labor_productivity["Pct Change from a Year Ago"], label="Labor productivity: Change from a Year Ago", linewidth=2.5, color="#082631")
    ax.plot(index, average_labor_cost["Pct Change do jeito que eu quero"], label="Unit Labor Cost: Change at Annual Rate", linewidth=2.5, color="#166083")

    ax.legend(frameon=False, fontsize=10, loc="upper right")
    fig.suptitle("US: Unit Labor Cost vs Labor Productivity", fontsize=15, fontweight='bold')
    ax.set_title("Pct Change SA", fontsize=10, style='italic')

    ax.axhline(0, color='black', linewidth=1)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color('#d9d9d9')

    fig.tight_layout()

    return fig
labor_cost = labor_cost()



