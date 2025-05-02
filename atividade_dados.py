import pandas as pd
from fredapi import Fred
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import matplotlib.ticker as mtick
import numpy as np

fred = Fred(api_key="672d5598c8a41df9397cc5eb92c02d5e")

def plot_mom(df, titulo="Título aqui em"):
    #vai me mandar algum dado pra eu só voltar o gráfico dele mom%
    plt.close("all")
    df = df.tail(36)

    fig, ax = plt.subplots(figsize=(12, 5))

    bars = ax.bar(df.index, df["Pct Change"], width=14, color="#082631")

    ax.set_title("MoM % SA", fontsize=8, style='italic', pad=10)
    fig.suptitle(titulo, fontsize=15, fontweight='bold')
    

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color('#d9d9d9')
    ax.spines["bottom"].set_color('#d9d9d9')

    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15)
    ax.axhline(0, color='black', lw=0.8)
    

    plt.tight_layout()

    plt.close(fig)
    return fig


pi = fred.get_series("RPI")
personal_income = pd.DataFrame()
personal_income["PI"] = pd.DataFrame(pi)
personal_income["Pct Change"]= personal_income["PI"].pct_change()
graf_pi = plot_mom(personal_income, "Real Personal Income")



rdpi = fred.get_series("DSPIC96")
real_disposable_income = pd.DataFrame()
real_disposable_income["RDI"] = pd.DataFrame(rdpi)
real_disposable_income["Pct Change"]= real_disposable_income["RDI"].pct_change()
graf_rdi = plot_mom(real_disposable_income, "Real Disposable Personal Income")



dividend = fred.get_series("PIROA")
dividends = pd.DataFrame()
dividends["Personal Income Receipts on Assets"] = pd.DataFrame(dividend)
dividends["Pct Change"]= dividends["Personal Income Receipts on Assets"].pct_change()
graf_dividends = plot_mom(dividends, "Personal Income Receipts on Assets")



inv = fred.get_series("A041RC1")
pi_inv_valation = pd.DataFrame()
pi_inv_valation["Proprietors' income with inventory valuation and capital consumption adjustments"] = pd.DataFrame(inv)
pi_inv_valation["Pct Change"]= pi_inv_valation["Proprietors' income with inventory valuation and capital consumption adjustments"].pct_change()
graf_pi_inv_valation = plot_mom(pi_inv_valation, "Proprietors' income with inventory valuation and capital consumption adjustments")


rent_in = fred.get_series("A048RC1")
rent_income = pd.DataFrame()
rent_income["Rental income of persons with capital consumption adjustment"] = pd.DataFrame(rent_in)
rent_income["Pct Change"]= rent_income["Rental income of persons with capital consumption adjustment"].pct_change()
graf_rent_income = plot_mom(rent_income, "Rental income of persons with capital consumption adjustment")



pii = fred.get_series("PII")
personal_income_interest = pd.DataFrame()
personal_income_interest["Personal Income Interest"] = pd.DataFrame(pii)
personal_income_interest["Pct Change"]= personal_income_interest["Personal Income Interest"].pct_change()
graf_personal_income_interest = plot_mom(personal_income_interest, "Personal Income Interest")



pdi = fred.get_series("PDI")
personal_dividend_income = pd.DataFrame()
personal_dividend_income["Personal Dividend Income"] = pd.DataFrame(pdi)
personal_dividend_income["Pct Change"]= personal_dividend_income["Personal Dividend Income"].pct_change()
graf_personal_dividend_income = plot_mom(personal_dividend_income, "Personal Dividend Income")



pctr = fred.get_series("PCTR")
personal_current_transfer = pd.DataFrame()
personal_current_transfer["Personal Current Transfer Receipts"] = pd.DataFrame(pctr)
personal_current_transfer["Pct Change"]= personal_current_transfer["Personal Current Transfer Receipts"].pct_change()
graf_personal_current_transfer = plot_mom(personal_current_transfer, "Personal Current Transfer Receipts")



pct = fred.get_series("W055RC1")
personal_current_transfer = pd.DataFrame()
personal_current_transfer["Personal Current Taxes"] = pd.DataFrame(pct)
personal_current_transfer["Pct Change"]= personal_current_transfer["Personal Current Taxes"].pct_change()
graf_personal_current_taxes = plot_mom(personal_current_transfer, "Personal Current Taxes")


#AQUI COMEÇA CONSUMO 



po = fred.get_series("A068RC1")
personal_outlays = pd.DataFrame()
personal_outlays["Personal Outlays"] = pd.DataFrame(po)
personal_outlays["Pct Change"]= personal_outlays["Personal Outlays"].pct_change()
graf_personal_outlays = plot_mom(personal_outlays, "Personal Outlays")


rpce = fred.get_series("PCEC96")
real_personal_consumption_expenditures = pd.DataFrame()
real_personal_consumption_expenditures["Real Personal Consumption Expenditures"] = pd.DataFrame(rpce)
real_personal_consumption_expenditures["Pct Change"]= real_personal_consumption_expenditures["Real Personal Consumption Expenditures"].pct_change()
graf_real_personal_consumption_expenditures = plot_mom(real_personal_consumption_expenditures, "Real Personal Consumption Expenditures")


psr = fred.get_series("PSAVERT")
personal_saving_rate = pd.DataFrame()
personal_saving_rate["Pct Change"] = pd.DataFrame(psr/100)  # Ajuste o nome da coluna para "Pct Change"
graf_personal_saving_rate = plot_mom(personal_saving_rate, "Personal Saving Rate")
graf_personal_saving_rate.axes[0].set_title("Percent of disposable personal income", fontsize=8, style='italic')


rpceserv = fred.get_series("PCESC96")
real_personal_consumption_expenditures_services = pd.DataFrame()
real_personal_consumption_expenditures_services["Real Personal Consumption Expenditures: Services"] = pd.DataFrame(rpceserv)
real_personal_consumption_expenditures_services["Pct Change"]= real_personal_consumption_expenditures_services["Real Personal Consumption Expenditures: Services"].pct_change()
graf_real_personal_consumption_expenditures_services = plot_mom(real_personal_consumption_expenditures_services, "Real Personal Consumption Expenditures: Services")


rpcegoods = fred.get_series("DGDSRX1")  
real_personal_consumption_expenditures_goods = pd.DataFrame()
real_personal_consumption_expenditures_goods["Real Personal Consumption Expenditures: Goods"] = pd.DataFrame(rpcegoods)
real_personal_consumption_expenditures_goods["Pct Change"]= real_personal_consumption_expenditures_goods["Real Personal Consumption Expenditures: Goods"].pct_change()
graf_real_personal_consumption_expenditures_goods = plot_mom(real_personal_consumption_expenditures_goods, "Real Personal Consumption Expenditures: Goods")


rpcedg = fred.get_series("PCEDGC96")
real_personal_consumption_expenditures_durables_goods = pd.DataFrame()
real_personal_consumption_expenditures_durables_goods["Real Personal Consumption Expenditures: Durable Goods"] = pd.DataFrame(rpcedg)
real_personal_consumption_expenditures_durables_goods["Pct Change"]= real_personal_consumption_expenditures_durables_goods["Real Personal Consumption Expenditures: Durable Goods"].pct_change()
graf_real_personal_consumption_expenditures_durables_goods = plot_mom(real_personal_consumption_expenditures_durables_goods, "Real Personal Consumption Expenditures: Durable Goods")


rpcendg = fred.get_series("PCENDC96")
real_personal_consumption_expenditures_nondurables_goods = pd.DataFrame()
real_personal_consumption_expenditures_nondurables_goods["Real Personal Consumption Expenditures: Nondurable Goods"] = pd.DataFrame(rpcendg)
real_personal_consumption_expenditures_nondurables_goods["Pct Change"]= real_personal_consumption_expenditures_nondurables_goods["Real Personal Consumption Expenditures: Nondurable Goods"].pct_change()
graf_real_personal_consumption_expenditures_nondurables_goods = plot_mom(real_personal_consumption_expenditures_nondurables_goods, "Real Personal Consumption Expenditures: Nondurable Goods")

#Aqui devo colocar retail sales


rs = fred.get_series("RSAFS")
retail_sales = pd.DataFrame()
retail_sales["Retail Sales"] = pd.DataFrame(rs)
retail_sales["Pct Change"]= retail_sales["Retail Sales"].pct_change()
graf_retail_sales = plot_mom(retail_sales, "Retail Sales")


crs = fred.get_series("RSFSXMV")
retail_sales_excl_motor_vehicle = pd.DataFrame()
retail_sales_excl_motor_vehicle["Retail Sales Excl Motor Vehicle"] = pd.DataFrame(crs)
retail_sales_excl_motor_vehicle["Pct Change"]= retail_sales_excl_motor_vehicle["Retail Sales Excl Motor Vehicle"].pct_change()
graf_retail_sales_excl_motor_vehicle = plot_mom(retail_sales_excl_motor_vehicle, "Retail Sales Excl Motor Vehicle")


rrs = fred.get_series("RRSFS")
real_retail_sales = pd.DataFrame()
real_retail_sales["Real Retail Sales"] = pd.DataFrame(rrs)
real_retail_sales["Pct Change"]= real_retail_sales["Real Retail Sales"].pct_change()
graf_real_retail_sales = plot_mom(real_retail_sales, "Real Retail Sales")




retail_sales_excl_motor_vehicle["YoY %"] = retail_sales_excl_motor_vehicle["Retail Sales Excl Motor Vehicle"].pct_change(periods=12)
retail_sales["YoY %"] = retail_sales["Retail Sales"].pct_change(periods=12)
retail_sales_excl_motor_vehicle = retail_sales_excl_motor_vehicle.dropna()
retail_sales = retail_sales.dropna()
retail_sales_excl_motor_vehicle = retail_sales_excl_motor_vehicle.tail(300)
retail_sales = retail_sales.tail(300)

r = fred.get_series("USRECD")
recessions = pd.DataFrame(r, columns=["USRECD"])
recessao_mensal = recessions.resample('MS').first()
recessao_mensal = recessao_mensal.tail(300)
index2 = retail_sales.index

def graf_yoy():
    plt.close("all")
    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(retail_sales.index, retail_sales["YoY %"], color="#082631", lw=2, label="Retail Sales")
    ax.plot(retail_sales_excl_motor_vehicle.index, retail_sales_excl_motor_vehicle["YoY %"], color="#37A6D9", lw=2, label="Retail Sales Excl Motor Vehicle")
    ax.fill_between(recessao_mensal.index, 0, 1, where=recessao_mensal["USRECD"] == 1, color='gray', alpha=0.3, transform=ax.get_xaxis_transform())
    ax.set_title("YoY % SA", fontsize=8, style='italic', pad=10)
    fig.suptitle("Retail Sales", fontsize=15, fontweight='bold')
    ax.legend(loc="upper left", fontsize=8, frameon=False)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color('#d9d9d9')
    ax.spines["bottom"].set_color('#d9d9d9')
    ax.set_ylim(-0.05, 0.1)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15)
    ax.axhline(0, color='black', lw=0.8)

    plt.tight_layout()
    plt.close(fig)
    return fig


graf_retail_sales_yoy = graf_yoy()

#Gráficos de PIB


def qoq(df, titulo="Título aqui em"):
    # Anualiza o dado QoQ
    plt.close("all")
    df = df.dropna()
    df = df.tail(12)
    df["Anualized"] = df["Pct Change"].apply(lambda x: (1 + x) ** 4 - 1)
    fig, ax = plt.subplots(figsize=(12, 5))
    bars =ax.bar(df.index, df["Pct Change"], width=14, color="#082631")
    fig.suptitle(titulo, fontsize=15, fontweight='bold')
    ax.set_title("QoQ % SA", fontsize=8, style='italic', pad=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color('#d9d9d9')
    ax.spines["bottom"].set_color('#d9d9d9')

    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15)
    ax.axhline(0, color='black', lw=0.8)

    plt.tight_layout()
    plt.close(fig)
    return fig


rfs = fred.get_series("FINSLC1")
real_final_sales_of_domestic_product = pd.DataFrame()
real_final_sales_of_domestic_product["Real Final Sales of Domestic Product"] = pd.DataFrame(rfs)
real_final_sales_of_domestic_product["Pct Change"]= real_final_sales_of_domestic_product["Real Final Sales of Domestic Product"].pct_change()
graf_real_final_sales_of_domestic_product = qoq(real_final_sales_of_domestic_product, "Real Final Sales of Domestic Product")


rfpdp = fred.get_series("LB0000031Q020SBEA")
real_final_sales_to_private_domestic_purchasers = pd.DataFrame()
real_final_sales_to_private_domestic_purchasers["Real Final Sales to Private Domestic Purchasers"] = pd.DataFrame(rfpdp)
real_final_sales_to_private_domestic_purchasers["Pct Change"]= real_final_sales_to_private_domestic_purchasers["Real Final Sales to Private Domestic Purchasers"].pct_change()
graf_real_final_sales_to_private_domestic_purchasers = qoq(real_final_sales_to_private_domestic_purchasers, "Real Final Sales to Private Domestic Purchasers")


rgdp = fred.get_series("GDPC1")
real_gross_domestic_product = pd.DataFrame()
real_gross_domestic_product["Real Gross Domestic Product"] = pd.DataFrame(rgdp)
real_gross_domestic_product["Pct Change"]= real_gross_domestic_product["Real Gross Domestic Product"].pct_change()
graf_real_gross_domestic_product = qoq(real_gross_domestic_product, "Real Gross Domestic Product")


rgdppc = fred.get_series("A939RX0Q048SBEA")
real_gross_domestic_product_per_capita = pd.DataFrame()
real_gross_domestic_product_per_capita["Real Gross Domestic Product Per Capita"] = pd.DataFrame(rgdppc)
real_gross_domestic_product_per_capita["Pct Change"]= real_gross_domestic_product_per_capita["Real Gross Domestic Product Per Capita"].pct_change() 
graf_real_gdp_per_capita = qoq(real_gross_domestic_product_per_capita, "Real Gross Domestic Product Per Capita")


rgdi = fred.get_series("GPDIC1")
real_gross_domestic_investment = pd.DataFrame()
real_gross_domestic_investment["Real Gross Domestic Investment"] = pd.DataFrame(rgdi)
real_gross_domestic_investment["Pct Change"]= real_gross_domestic_investment["Real Gross Domestic Investment"].pct_change()
graf_real_gross_domestic_investment = qoq(real_gross_domestic_investment, "Real Gross Domestic Investment")


rpfi = fred.get_series("FPIC1")
real_private_fixed_investment = pd.DataFrame()
real_private_fixed_investment["Real Private Fixed Investment"] = pd.DataFrame(rpfi)
real_private_fixed_investment["Pct Change"]= real_private_fixed_investment["Real Private Fixed Investment"].pct_change()
graf_real_private_fixed_investment = qoq(real_private_fixed_investment, "Real Private Fixed Investment")


negs = fred.get_series("NETEXP")
net_exports = pd.DataFrame()
net_exports["Net Exports of Goods and Services"] = pd.DataFrame(negs)
net_exports["Pct Change"]= net_exports["Net Exports of Goods and Services"].pct_change()
graf_net_exports = qoq(net_exports, "Net Exports of Goods and Services")


fgce = fred.get_series("FGEXPND")
federal_government_consumption_expenditures = pd.DataFrame()
federal_government_consumption_expenditures["Federal Government Consumption Expenditures"] = pd.DataFrame(fgce)
federal_government_consumption_expenditures["Pct Change"]= federal_government_consumption_expenditures["Federal Government Consumption Expenditures"].pct_change()
graf_federal_government_consumption_expenditures = qoq(federal_government_consumption_expenditures, "Federal Government Consumption Expenditures")


fgcei = fred.get_series("A091RC1Q027SBEA")
federal_government_consumption_expenditures_interest_payments = pd.DataFrame()
federal_government_consumption_expenditures_interest_payments["Federal Government Consumption Expenditures Interest Payments"] = pd.DataFrame(fgcei)
federal_government_consumption_expenditures_interest_payments["Pct Change"]= federal_government_consumption_expenditures_interest_payments["Federal Government Consumption Expenditures Interest Payments"].pct_change()
graf_federal_government_consumption_expenditures_interest_payments = qoq(federal_government_consumption_expenditures_interest_payments, "Federal Government Consumption Expenditures Interest Payments")


dc = fred.get_series("A997RC1Q027SBEA")
government_national_defense_consumption = pd.DataFrame()
government_national_defense_consumption['National Defense Consumption Expenditures'] = pd.DataFrame(dc)
government_national_defense_consumption["Pct Change"] = government_national_defense_consumption["National Defense Consumption Expenditures"].pct_change()
graf_government_national_defense_consumption = qoq(government_national_defense_consumption, "National Defense Consumption Expenditures")


ndc = fred.get_series("FNDEFX")
national_non_defense_consumption = pd.DataFrame()
national_non_defense_consumption["National Nondefense Consumption Expenditures and Gross Investments"] = pd.DataFrame(ndc)
national_non_defense_consumption["Pct Change"] = national_non_defense_consumption["National Nondefense Consumption Expenditures and Gross Investments"].pct_change()
graf_national_nondefense_consumption = qoq(national_non_defense_consumption, "National Nondefense Consumption Expenditures and Gross Investments")



real_gross_domestic_investment["YoY %"] = real_gross_domestic_investment["Real Gross Domestic Investment"].pct_change(periods=12)
real_gross_domestic_investment = real_gross_domestic_investment.dropna()
federal_government_consumption_expenditures["YoY %"] = federal_government_consumption_expenditures["Federal Government Consumption Expenditures"].pct_change(periods=12)
federal_government_consumption_expenditures = federal_government_consumption_expenditures.dropna()
real_gross_domestic_investment = real_gross_domestic_investment[real_gross_domestic_investment.index.year >= 1950]

r = fred.get_series("USRECD")
recessions = pd.DataFrame(r, columns=["USRECD"])
recessao_mensal = recessions.resample('MS').first()
recessao_mensal = recessao_mensal[recessao_mensal.index.year >= 1950]

graf_yoy_gov_and_inv, ax = plt.subplots(figsize=(12, 5))
ax.plot(real_gross_domestic_investment.index, real_gross_domestic_investment["YoY %"], color="#082631", lw=2, label="Real Gross Domestic Investment")
ax.plot(federal_government_consumption_expenditures.index, federal_government_consumption_expenditures["YoY %"], color="#37A6D9", lw=2, label="Federal Government Consumption Expenditures")
ax.fill_between(recessao_mensal.index, 0, 1, where=recessao_mensal["USRECD"] == 1, color='gray', alpha=0.3, transform=ax.get_xaxis_transform())
ax.set_title("YoY % SA", fontsize=8, style='italic', pad=10)
graf_yoy_gov_and_inv.suptitle("Real Gross Domestic Investment vs Federal Government Consumption Expenditures", fontsize=15, fontweight='bold')
ax.legend(loc="upper left", fontsize=8, frameon=False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color('#d9d9d9')
ax.spines["bottom"].set_color('#d9d9d9')

ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15)
ax.axhline(0, color='black', lw=0.8)
plt.tight_layout()





real = fred.get_series("GDPC1")
pot = fred.get_series("GDPPOT")
gap = pd.DataFrame()
gap["US real GDP"] = pd.DataFrame(real)
gap["US potential GDP"] = pd.DataFrame(pot)

gap = gap[gap.index.year >= 2000]
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12,5))

above_potential = gap["US real GDP"] > gap["US potential GDP"]
below_potential = ~above_potential

ax.fill_between(gap.index, gap["US real GDP"], gap["US potential GDP"], where=above_potential, 
                interpolate=True, color='#AFABAB', alpha=0.5, label="Above Potential")
ax.fill_between(gap.index, gap["US real GDP"], gap["US potential GDP"], where=below_potential, 
                interpolate=True, color='#37A6D9', alpha=0.5, label="Below Potential")

ax.plot(gap.index, gap["US real GDP"], label="US Real GDP", linewidth=2.5, color="#166083")
ax.plot(gap.index, gap["US potential GDP"], label="US Potential GDP", linewidth=2.5, linestyle='dashed', color="#082631")

if not gap.empty:
    last_date = gap.index[-1]
    last_real = gap.loc[last_date, "US real GDP"]
    last_potential = gap.loc[last_date, "US potential GDP"]
    last_pct = ((last_real - last_potential) / last_potential) * 100

    text_y = max(last_real, last_potential) + 500 
    arrow_props = dict(arrowstyle="->", color="black")

    ax.annotate(f"{last_pct:.1f}% Above potential", xy=(last_date, last_real), xytext=(last_date, text_y),
                fontsize=10, color='black', ha='center', arrowprops=arrow_props)

ax.legend(frameon=False, fontsize=10, loc="upper left")
fig.suptitle("US Real vs Potential GDP", fontsize=12, fontweight='bold')
ax.set_title("Billion of Chained 2017 Dollars SA", fontsize=10, style='italic')

ax.axhline(0, color='black', linewidth=1)

ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=10, labelpad=15)
ax.set_ylim(12000, 25000)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#d9d9d9")
ax.spines["bottom"].set_color("#d9d9d9")

fig.tight_layout()


graf_output_gap = fig

gci = fred.get_series("GCEC1")
government_consumption_expenditures_and_inv = pd.DataFrame()
government_consumption_expenditures_and_inv["Government Consumption Expenditures and Gross Investment"] = pd.DataFrame(gci)
government_consumption_expenditures_and_inv["Pct Change"]= government_consumption_expenditures_and_inv["Government Consumption Expenditures and Gross Investment"].pct_change()
graf_government_consumption_expenditures_and_inv = qoq(government_consumption_expenditures_and_inv, "Government Consumption Expenditures and Gross Investment")


rpce = fred.get_series("PCECC96")
real_personal_consumption_expenditures_qoq = pd.DataFrame()
real_personal_consumption_expenditures_qoq["Real Personal Consumption Expenditures"] = pd.DataFrame(rpce)
real_personal_consumption_expenditures_qoq["Pct Change"]= real_personal_consumption_expenditures_qoq["Real Personal Consumption Expenditures"].pct_change()
graf_real_personal_consumption_expenditures_qoq = qoq(real_personal_consumption_expenditures_qoq, "Real Personal Consumption Expenditures")


gdp = pd.DataFrame()
gdp["Real Gross Domestic Product"] = real_gross_domestic_product['Pct Change']
gdp["Gross Private Domestic Investment"] = real_gross_domestic_investment['Pct Change']
gdp["Personal Consumption Expenditures"] = real_personal_consumption_expenditures_qoq['Pct Change']
gdp["Government Consumption Expenditures"] = government_consumption_expenditures_and_inv['Pct Change']
gdp = gdp.copy().tail(12)


df = gdp.dropna().tail(12)
x = np.arange(len(df))
bar_width = 0.2

fig, ax = plt.subplots(figsize=(15,9))

ax.bar(x - bar_width, df["Personal Consumption Expenditures"], width=bar_width,
       label="Personal Consumption Expenditures", color="#0c2c36")
ax.bar(x, df["Gross Private Domestic Investment"], width=bar_width,
       label="Gross Private Domestic Investments", color="#4abff2")
ax.bar(x + bar_width, df["Government Consumption Expenditures"], width=bar_width,
       label="Government Expenditures", color="#aad8ea")
ax.plot(x, df["Real Gross Domestic Product"], label="GDP", color="#0c2c36", linewidth=2)

fig.suptitle("US GDP", fontsize=28, fontweight='bold')
ax.set_title("QoQ % SAAR", fontsize=18, style='italic', pad=10)

ax.set_xticks(x)
ax.set_xticklabels(df.index.astype(str), rotation=0, ha='center', fontsize=18)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
ax.axhline(0, color='black', lw=0.8)
ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=18, labelpad=15)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color('#d9d9d9')
ax.spines["bottom"].set_color('#d9d9d9')

ax.tick_params(axis='y', labelsize=9)
ax.tick_params(axis='x', labelsize=9)
ax.legend(fontsize=18)

plt.tight_layout()

graf_gdp = fig