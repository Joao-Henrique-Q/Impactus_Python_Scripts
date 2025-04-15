import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd
from fredapi import Fred

# Configurações iniciais
plt.style.use('ggplot')
fred = Fred(api_key="672d5598c8a41df9397cc5eb92c02d5e")

# Funções auxiliares genéricas -------------------------------------------------
def get_fred_data(series_id):
    """Obtém dados do FRED e retorna Series temporal"""
    return fred.get_series(series_id)

def create_base_dataframe(series, periods=1):
    """Cria DataFrame com variações mensais e anuais"""
    df = pd.DataFrame({'Value': series})
    df['Pct Change'] = df['Value'].pct_change(periods=periods)
    df['Pct Change from a year ago'] = df['Value'].pct_change(periods=12)
    return df.dropna()

def plot_sa_main(df, title, colors):
    """Gera gráfico de variação mensal/anual padronizado"""
    fig, ax = plt.subplots(figsize=(12, 6))
    df['Pct Change'].plot(ax=ax, color=colors[0], label='MoM')
    df['Pct Change from a year ago'].plot(ax=ax, color=colors[1], label='YoY')
    
    ax.set_title(f"PCE - {title}", fontsize=14)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.legend()
    plt.close(fig)
    return fig

# Novas funções de visualização ------------------------------------------------
def sa_main(df, titulo="Título padrão"):
    """Gráfico de análise sazonal com percentis históricos"""
    df_24 = df[df.index.year == 2024]
    df_25 = df[df.index.year == 2025]
    baseline = df[(df.index.year >= 2010) & (df.index.year <= 2019)]
    
    # Cálculo de percentis
    percentis = baseline.groupby(baseline.index.month)['Pct Change'].agg(
        [('Percentil 10', lambda x: x.quantile(0.10)),
         ('Percentil 90', lambda x: x.quantile(0.90)),
         ('Mediana', 'median')]
    )
    
    # Preparação dos dados atuais
    current_data = pd.concat([df_24, df_25]).groupby(
        [pd.Grouper(freq='M'), pd.Grouper(key='Year')]
    )['Pct Change'].first().unstack()

    # Plotagem
    fig, ax = plt.subplots(figsize=(12, 5))
    meses = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Linhas de referência
    ax.plot(meses, percentis['Percentil 10'], linestyle='dotted', 
            color='black', label='10th Percentile (2010-2019)')
    ax.plot(meses, percentis['Percentil 90'], linestyle='dotted', 
            color='black', label='90th Percentile (2010-2019)')
    ax.plot(meses, percentis['Mediana'], color='#082631', 
            linewidth=2, label='Mediana')

    # Dados atuais
    if 2024 in current_data.columns:
        ax.plot(meses[:len(current_data[2024])], current_data[2024], 
                marker='o', color='#166083', label='2024')
    if 2025 in current_data.columns:
        ax.plot(meses[:len(current_data[2025])], current_data[2025], 
                marker='o', color='#37A6D9', label='2025')

    ax.set_title(titulo, fontsize=16, pad=20)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.legend(frameon=False, loc='upper right')
    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15)
    plt.tight_layout()
    plt.close(fig)
    return fig

def anualizar(df, titulo="Título padrão", ylim=(-0.02, 0.07)):
    """Gráfico de tendências anualizadas com médias móveis"""
    df = df.copy()
    df['3 MMA'] = df['Pct Change'].rolling(3).mean()
    df['6 MMA'] = df['Pct Change'].rolling(6).mean()
    df['3 MMA SAAR'] = (1 + df['3 MMA']).pow(12) - 1
    df['6 MMA SAAR'] = (1 + df['6 MMA']).pow(12) - 1
    
    # Preparação dos dados
    df = df[df.index >= '2010-01-01']
    mean_10_19 = df.loc['2010':'2019', 'Pct Change from a year ago'].mean()
    
    # Plotagem
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df.index, df['3 MMA SAAR'], linestyle=':', 
            color='#AFABAB', label='3M MA Annualized')
    ax.plot(df.index, df['6 MMA SAAR'], linestyle='--', 
            color='#37A6D9', label='6M MA Annualized')
    ax.plot(df.index, df['Pct Change from a year ago'], 
            color='#082631', label='YoY')
    ax.axhline(mean_10_19, color='#166083', linestyle='--', 
               label='Média 2010-2019')
    
    ax.set_title(titulo, fontsize=16, pad=20)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.set_ylim(ylim)
    ax.legend(frameon=False, loc='upper left')
    ax.set_xlabel("Fonte: FRED | Impactus UFRJ", fontsize=8, labelpad=15)
    plt.tight_layout()
    plt.close(fig)
    return fig

# Módulo Principal PCE --------------------------------------------------------
class PCEAnalyzer:
    def __init__(self):
        self.series_map = {
            'core': 'PCEPILFE',
            'goods': 'DGDSRG3M086SBEA',
            'services': 'DSERRG3M086SBEA',
            'food': 'DFXARG3M086SBEA',
            'energy': 'DNRGRG3M086SBEA',
            'nondurable': 'DNDGRG3M086SBEA',
            'durable': 'DDURRG3M086SBEA'
        }
        
        self.data = {}
        self.figures = {
            'decomposition': None,
            'monthly': {},
            'annual': {},
            'seasonal': {},
            'annualized': {}
        }
        
        self.load_data()
        self.generate_all_figures()
    
    def load_data(self):
        """Carrega todos os dados necessários"""
        for key, series_id in self.series_map.items():
            raw_data = get_fred_data(series_id)
            self.data[key] = create_base_dataframe(raw_data)
    
    def generate_component_plots(self, component):
        """Gera todos os gráficos para um componente"""
        df = self.data[component]
        
        # Gráficos básicos
        self.figures['monthly'][component] = plot_sa_main(
            df, f"{component.capitalize()} - Variação Mensal", ('#1f77b4', '#ff7f0e'))
        
        # Novos gráficos
        self.figures['seasonal'][component] = sa_main(
            df, f"{component.capitalize()} - Análise Sazonal")
        
        self.figures['annualized'][component] = anualizar(
            df, f"{component.capitalize()} - Tendências Anualizadas")
    
    def generate_decomposition_plot(self):
        """Gera o gráfico de decomposição complexo"""
        # ... (mantido igual ao original)

    def generate_all_figures(self):
        """Gera todos os gráficos automaticamente"""
        for component in self.series_map.keys():
            self.generate_component_plots(component)
        self.generate_decomposition_plot()
    
    def get_all_figures(self):
        """Retorna estrutura organizada de figuras"""
        return {
            'main_decomposition': self.figures['decomposition'],
            'monthly_analysis': self.figures['monthly'],
            'seasonal_analysis': self.figures['seasonal'],
            'annualized_trends': self.figures['annualized']
        }

# Uso no Streamlit ------------------------------------------------------------
def get_pce_figures():
    analyzer = PCEAnalyzer()
    return analyzer.get_all_figures()