import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from fredapi import Fred
import os

# Configuração da fonte Arial
font_prop = fm.FontProperties(fname=fm.findfont('Arial'))

# Obtenção dos dados
fred = Fred(api_key='672d5598c8a41df9397cc5eb92c02d5e')
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
contribuicao["PCE"] = inflation["Cheio"]

contribuicao = contribuicao[(contribuicao.index.year >= 2016)]

contribuicao_positive = contribuicao.clip(lower=0)
contribuicao_negative = contribuicao.clip(upper=0)

plt.figure(figsize=(18, 10.8))

# Gráfico de barras
plt.bar(contribuicao.index, contribuicao_positive["Durable Goods"], color="#AFABAB", label="Durable Goods", width=14)
plt.bar(contribuicao.index, contribuicao_negative["Durable Goods"], color="#AFABAB", width=14)

plt.bar(contribuicao.index, contribuicao_positive["Nondurable Goods"], bottom=contribuicao_positive["Durable Goods"], color="#082631", label="Nondurable Goods", width=14)
plt.bar(contribuicao.index, contribuicao_negative["Nondurable Goods"], bottom=contribuicao_negative["Durable Goods"], color="#082631", width=14)

plt.bar(contribuicao.index, contribuicao_positive["Services"], bottom=contribuicao_positive["Durable Goods"] + contribuicao_positive["Nondurable Goods"], color="#37A6D9", label="Services", width=14)
plt.bar(contribuicao.index, contribuicao_negative["Services"], bottom=contribuicao_negative["Durable Goods"] + contribuicao_negative["Nondurable Goods"], color="#37A6D9", width=14)

# Linha de inflação total
plt.plot(contribuicao.index, inflation["Cheio"], color="#166083", label="Cheio", linewidth=2)

# Título e subtítulo
plt.suptitle("PCE - Contribution to Inflation", fontsize=20, fontweight='bold', fontproperties=font_prop, y=0.98)  # Ajuste a posição vertical com `y`
plt.title("SA Pct Change %", fontsize=14, fontproperties=font_prop, pad=20)  # Adiciona um subtítulo com padding

# Legenda
plt.legend(frameon=False, fontsize=14, prop=font_prop, loc="upper right")

# Linha horizontal em y=0
plt.axhline(y=0, color='black', linewidth=0.5)

# Remover bordas desnecessárias
plt.gca().spines["top"].set_visible(False)
plt.gca().spines["right"].set_visible(False)
plt.gca().spines["left"].set_color("#d9d9d9")
plt.gca().spines["bottom"].set_color("#d9d9d9")

# Rótulo do eixo x
plt.xlabel("Fonte: FRED | Impactus UFRJ", fontsize=14, labelpad=15, fontproperties=font_prop)

# Ajustar layout
plt.tight_layout()

# Salvar o DataFrame em um arquivo Excel
caminho_arquivo = "contribuicao_inflacao.xlsx"


# Abrir o arquivo Excel automaticamente
if os.name == 'nt':  # Verifica se o sistema operacional é Windows
    os.startfile(caminho_arquivo)
elif os.name == 'posix':  # Verifica se o sistema operacional é macOS ou Linux
    os.system(f'open "{caminho_arquivo}"')
else:
    print("Sistema operacional não suportado para abrir o arquivo automaticamente.")

# Exibir o gráfico
plt.show()