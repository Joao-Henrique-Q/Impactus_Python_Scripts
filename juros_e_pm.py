import pandas as pd
from fredapi import Fred
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import matplotlib.ticker as mtick

fred = Fred(api_key="672d5598c8a41df9397cc5eb92c02d5e")

def plot_juros(df, titulo="Título aqui em"):
    plt.close("all")
    #vai me mandar algum dado pra eu só voltar o gráfico dele mom%
    df = df.dropna()
    df = df.tail(30000)

    fig, ax = plt.subplots(figsize=(12, 5))

    linhas = ax.plot(df.index, df["Juros"], lw=2, color="#082631")

    fig.suptitle(titulo, fontsize=15, fontweight='bold')
    

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color('#d9d9d9')
    ax.spines["bottom"].set_color('#d9d9d9')

    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15)
    
    ultimo_valor = df["Juros"].iloc[-1]
    ultimo_indice = df.index[-1]
    ax.text(ultimo_indice, ultimo_valor,
            f'{ultimo_valor:.2%}',
            fontsize=10, fontweight='bold',
            color='#082631', ha='left', va='center')
    plt.tight_layout()


    return fig

r3m = fred.get_series("DGS3MO")
yield3m = pd.DataFrame()
yield3m["Juros"] = pd.DataFrame(r3m/100)
graf_3m = plot_juros(yield3m, "3 months Treasury Rate")


r10 = fred.get_series("DGS10")
yield10 = pd.DataFrame()
yield10["Juros"] = pd.DataFrame(r10/100)
graf_10yr = plot_juros(yield10, "10 Year Treasury Rate")



r7 = fred.get_series("DGS7")
yield7 = pd.DataFrame()
yield7["Juros"] = pd.DataFrame(r7/100)
graf_7yr = plot_juros(yield7, "7 Year Treasury Rate")


r20 = fred.get_series("DGS20")
yield20 = pd.DataFrame()
yield20["Juros"] = pd.DataFrame(r20/100)
graf_20yr = plot_juros(yield20, "20 Year Treasury Rate")


r30 = fred.get_series("DGS30")
yield30 = pd.DataFrame()
yield30["Juros"] = pd.DataFrame(r30/100)
graf_30yr = plot_juros(yield30, "30 Year Treasury Rate")