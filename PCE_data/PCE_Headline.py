import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from fredapi import Fred

# Configurar API do FRED (substitua 'YOUR_API_KEY' pela sua chave real)
API_KEY = "672d5598c8a41df9397cc5eb92c02d5e"
fred = Fred(api_key=API_KEY)

# Obter dados do FRED
pce_head = fred.get_series("PCEPI")

# Criar DataFrame
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

# Criar gráfico
fig, ax = plt.subplots(figsize=(18, 10.8))
ax2 = ax.twinx()

ax.bar(pce_headline.index, pce_headline["Pct Change"], width=20, color="#166083", label="MoM %")
ax2.plot(pce_headline.index, pce_headline["Pct Change from a year ago"], linewidth=2, color="#082631", label="YoY %")
ax2.plot(pce_headline.index, pce_headline["6 MMA SAAR"], linewidth=2, color="#37A6D9", label="6 MMA SAAR")
ax2.plot(pce_headline.index, pce_headline["3 MMA SAAR"], linewidth=2, color="#AFABAB", label="3 MMA SAAR")

ax.set_ylabel("MoM %", fontsize=14)
ax2.set_ylabel("YoY %", fontsize=14)
ax.set_ylim(-0.003, 0.015)
ax2.set_ylim(-0.03, 0.15)

plt.suptitle("PCE Headline", fontsize=20, fontweight='bold')
plt.text(0.505, 0.94, "SA Pct Change %", fontsize=14, ha='center', transform=plt.gcf().transFigure)

ax.legend(frameon=False, fontsize=14, loc="upper left")
ax2.legend(frameon=False, fontsize=14, loc="upper right")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#d9d9d9")
ax.spines["bottom"].set_color("#d9d9d9")
ax2.spines["top"].set_visible(False)

ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
ax2.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

plt.xlabel("Fonte: FRED | Impactus UFRJ", fontsize=14, labelpad=15)
plt.tight_layout()

# Streamlit
st.title("PCE Headline - Análise de Inflação")
st.pyplot(fig)
