import pandas as pd
from fredapi import Fred
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import matplotlib.ticker as mtick

fred = Fred(api_key="672d5598c8a41df9397cc5eb92c02d5e")

def plot_mom(df, titulo="Título aqui em"):
    #vai me mandar algum dado pra eu só voltar o gráfico dele mom%
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