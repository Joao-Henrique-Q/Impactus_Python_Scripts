import streamlit as st
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from variaveis_dashboard import *  
from atividade_dados import *
from ppi import *
from juros_e_pm import *

st.set_page_config(
    page_title="Central de Dados - EUA",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- SIDEBAR ----
with st.sidebar:
    st.markdown("## Central de Dados Econômicos US")
    st.markdown("""Este site apresenta **dados econômicos dos EUA** e análises em relação a seus impactos macroeconômicos.""")

    st.markdown("### 🔗 Links Úteis")
    st.markdown("- [BEA - Site Oficial](https://www.bea.gov/)")
    st.markdown("- [Federal Reserve of St. Louis](https://www.federalreserve.gov/)")
    st.markdown("- [GitHub do Projeto](https://github.com/Jaumzinho109/Impactus_Python_Scripts/blob/main/PCE_data/PCE_Headline.py)")

# ---- CABEÇALHO ----
st.title("US Data Base")

# ---- MENU PRINCIPAL ----
menu = option_menu(
    menu_title=None,
    options=["Mercado de Trabalho", "Inflação", "Atividade Econômica", "Política Monetária e Juros"],
    icons=["briefcase", "graph-up", "bar-chart", "bank"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

if menu == "Inflação":
    st.header("Inflação")

    subtema = option_menu(
        "",
        ["PCE", "CPI", "PPI"],
        orientation="horizontal"
    )

    if subtema == "PCE":
        
        st.write(
            "."
            , unsafe_allow_html=True
        )

        opcao_grafico = st.selectbox(
            "Selecione a Visualização",
            ["PCE Contributions", "SA Main MoM %", "SA Main YoY %",]
        )

       
        

        if opcao_grafico == "PCE Contributions":
            
            st.pyplot(pce_decomposto)
            plt.close("all")
        elif opcao_grafico == "SA Main MoM %":
            
            st.pyplot(pce_core_mom)
            st.pyplot(pce_serv_mom)
            st.pyplot(pce_goods_mom)
            st.pyplot(pce_durable_mom)
            st.pyplot(pce_ndur_mom)
            st.pyplot(pce_food_mom)
            st.pyplot(pce_en_mom)
            plt.close("all")
            
        elif opcao_grafico == "SA Main YoY %":
            
            st.pyplot(pce_core_ya)
            st.pyplot(pce_serv_ya)
            st.pyplot(pce_goods_ya)
            st.pyplot(pce_ndur_yoy)
            st.pyplot(pce_durable_yoy)
            st.pyplot(pce_food_yoy)
            st.pyplot(pce_en_ya)
            plt.close("all")
            
        
            
            

    elif subtema == "CPI":
        "Muitas surpresas para o dado no mês de abril, os resultados vieram muito mais fracos do que o esperado. O núcleo geral e de serviços subiram apenas 0,1%, enquanto os bens caíram 0,1%. Isso seria interpretado como um resultado há alguns meses, sinais de inflação voltando a convergir à meta do FED, mas não dessa vez. Acontece que toda incerteza sobre os impactos das tarifas nos preços faz com que seja muito difícil formar expectativa sólida sobre preços futuros. Assim, a reação do mercado ao dado foi muito menor em comparação aos últimos meses. Mercados estão 0 sensíveis a dados econômicos, agora mais importa o que Trump posta no Twitter."
        opcao_grafico = st.selectbox(
            "Selecione a Visualização",
            ["NSA - Main", "SA Main MoM %", "SA Main YoY %"]
        )
        
        if opcao_grafico == "NSA - Main":
            
            st.pyplot(core_cpi_nsa)
            st.pyplot(cpi_head_nsa)
            st.pyplot(core_goods_nsa)
            st.pyplot(core_services_nsa)
            st.pyplot(core_less_shelter_cars_trucks)
            st.pyplot(services_less_shelter)
            st.pyplot(services_less_med)
            plt.close("all")
        elif opcao_grafico == "SA Main MoM %":
            
            st.pyplot(graf_sa_core)
            st.pyplot(graf_sa_cpi)
            st.pyplot(graf_sa_core_goods)
            st.pyplot(graf_sa_core_services)
            st.pyplot(graf_sa_food)
            st.pyplot(graf_sa_energy)
            plt.close("all")
        elif opcao_grafico == "SA Main YoY %":
            
            st.pyplot(graf_sa_ya_core)
            st.pyplot(graf_sa_ya_head)
            st.pyplot(graf_sa_ya_cgoods)
            st.pyplot(graf_sa_ya_cservices)
            st.pyplot(graf_sa_ya_food)
            st.pyplot(graf_sa_ya_energy)
            plt.close("all")

    elif subtema == "PPI":
        opcao_grafico = st.selectbox(
            "Selecione a Visualização",
            ["Mom %", "YoY %"]
        )
        
        if opcao_grafico == "Mom %":
            
            st.pyplot(graf_core_ppi_mom)
            st.pyplot(graf_airline_passangers_mom)
            st.pyplot(graf_hospital_inpatient_care_mom)
            st.pyplot(graf_hospital_outpatient_care_mom)
            st.pyplot(graf_hospital_physician_care_mom)
            st.pyplot(graf_nursing_home_care_mom)
            plt.close("all")

        elif opcao_grafico == "YoY %":
            
            st.pyplot(graf_core_ppi_yoy)
            st.pyplot(graf_airline_passangers_yoy)
            st.pyplot(graf_hospital_inpatient_care_yoy)
            st.pyplot(graf_hospital_outpatient_care_yoy)
            st.pyplot(graf_hospital_physician_care_yoy)
            st.pyplot(graf_nursing_home_care_yoy)
            plt.close("all")




            

elif menu == "Mercado de Trabalho":
    st.write(
        "Apesar de toda instabilidade trazidas pelo ruídos de tarifas e seus impactos, o mercado de trabalho se mantém estável. A última leitura do Payroll indicou a criação de 228 mil vagas acima das expectativas (135 mil), enquanto a leitura anterior teve uma revisão negativa de aproximadamente 50 mil vagas.\n"
        "O desemprego subiu para 4,2% e o ganho médio se manteve estável em 0,3% m/m. Acredito que este último deve sofrer uma desaceleração no médio prazo, pois a rigidez de salários faz com que o dado ainda não reflita as condições de esfriamento do setor.\n"
        "Por fim, quase não houve reação do mercado devido às incertezas trazida pelas tarifas e seus possíveis impactos econômicos."
        , unsafe_allow_html=True
    )

    subtema_trabalho = option_menu(
        menu_title=None,
        options=["Payroll", "Emprego", "Salários"],
        default_index=0,
        orientation="horizontal"
    )

    if subtema_trabalho == "Emprego":

        
        st.pyplot(unrate)
        st.pyplot(beveridge_curve)
        st.pyplot(beveridge_ratio)
        st.pyplot(participation_rate)
        st.pyplot(employment_change)
        st.pyplot(sahm_rule)
        plt.close("all")  

    if subtema_trabalho == "Payroll":
        

         
        st.pyplot(payroll)
        st.pyplot(private_vs_government)
        st.pyplot(cic_payroll)
        st.pyplot(goods_vs_services_payroll)
        st.pyplot(ordering)
        st.pyplot(breakdown_payroll)
        plt.close("all") 


    if subtema_trabalho == "Salários":
          
        st.pyplot(average_hourly_earnings_mom)
        st.pyplot(average_hourly_earnings_yoy)
        st.pyplot(labor_cost)
        plt.close("all") 


elif menu == "Atividade Econômica":
    st.write("Aqui reside minha maior incerteza para o futuro e provavelmente para qualquer analista. A pergunta que representa tudo isso é a seguinte: o choque sobre as cadeias produtivas e expectativa dos agentes será suficiente para derrubar o excepcionalismo americano? A percepção de que o crescimento vai diminuir devido ao choque é consenso, mas acredito que muito é subestimado, o impacto das expectativa, sobretudo, no consumo. O consumo vem crescendo menos que a renda, a taxa de poupança atingiu 4,6%. Ainda assim, o efeito geral é desvalorização do dólar e venda de títulos americanos. O recente movimento deste último é explicado por uma desalavancagem de fundos hedge, os quais compravam título no mercado spot e vendiam no futuro, e a fim de se proteger do aumento da instabilidade, desfizeram suas posições.\n"
             "Acho muito interessante Trump querer muito devalorizar o dólar para que de algum modo a balança não fique tão negativa. Mas isso acontecer, necessariamente o consumo americano vai ter que cair e poupança aumentar para compensar a queda na poupança externa. Espero que não haja nenhuma surpresa sobre eventuais resultados disso aqui na atividade...\n"
             "Muitas perguntas surgem desse cenário:\n"
             "Esse movimento de venda de títulos públicos e dólar seria resultado da percepção de que não vale a pena reter a moeda devido ao posicionamento do Trump em desvalorizá-la?\n"
             "Será que esses juros de 10 anos estão realmente altos (mesmo depois do movimento de desalavancagem)? Quando comparamos com o nível de juros de curto prazo, esses juros de 10 anos estão muito baixos em termos históricos, mas ao mesmo tempo será que este último resultado é um efeito do QE?\n"
             "Dado uma piora nas expectativas e aumento de incerteza, qual vai ser o porto seguro agora que o dólar está duvidoso?"
    ,  unsafe_allow_html=True
    )
    subtema_atividade = option_menu(
        menu_title=None,
        options=["Renda", "Consumo", "V. Varejo", "PIB"],
        default_index=0,
        orientation="horizontal"
    )
    if subtema_atividade == "Renda":
        
         
        st.pyplot(graf_pi)
        st.pyplot(graf_rdi)
        st.pyplot(graf_dividends)
        st.pyplot(graf_pi_inv_valation)
        st.pyplot(graf_rent_income)
        st.pyplot(graf_personal_income_interest)
        st.pyplot(graf_personal_dividend_income)
        plt.close("all") 

    if subtema_atividade == "Consumo":
        
        st.pyplot(graf_personal_outlays)
        st.pyplot(graf_real_personal_consumption_expenditures)
        st.pyplot(graf_personal_saving_rate)
        st.pyplot(graf_real_personal_consumption_expenditures_services)
        st.pyplot(graf_real_personal_consumption_expenditures_goods)
        st.pyplot(graf_real_personal_consumption_expenditures_durables_goods)
        st.pyplot(graf_real_personal_consumption_expenditures_nondurables_goods)
        plt.close("all")

    if subtema_atividade == "Vendas no Varejo":
        
        st.pyplot(graf_retail_sales)
        st.pyplot(graf_retail_sales_excl_motor_vehicle)
        st.pyplot(graf_real_retail_sales)
        st.pyplot(graf_retail_sales_yoy)
        plt.close("all")

    if subtema_atividade == "PIB":
        
        st.pyplot(graf_output_gap)
        st.pyplot(graf_yoy_gov_and_inv)
        st.pyplot(graf_real_gross_domestic_product)
        st.pyplot(graf_real_final_sales_of_domestic_product)
        st.pyplot(graf_real_final_sales_to_private_domestic_purchasers)
        st.pyplot(graf_real_gdp_per_capita)
        st.pyplot(graf_real_gross_domestic_investment)
        st.pyplot(graf_real_private_fixed_investment)
        st.pyplot(graf_net_exports)
        st.pyplot(graf_federal_government_consumption_expenditures)
        st.pyplot(graf_federal_government_consumption_expenditures_interest_payments)
        st.pyplot(graf_government_national_defense_consumption)
        st.pyplot(graf_national_nondefense_consumption)
        plt.close("all")

elif menu == 'Política Monetária e Juros':
    st.write("Na última reunião não houve novidades quanto à operacionalidade dos juros, eles foram mantidos e continuarão até que o FED enxergue maiores sinais de enfraquecimento. Além disso, também aumentaram projeção para o PCE durante o ano (basicamente adimitiram que a inflação não deve caminhar no ano), diminuíram a perspectiva de crescimento da economia, e por fim anunciaram uma diminuição do ritmo do Quantitative Tightening.\n"
             "Muito ansioso para saber o posicionamento da próxima reunião, se já enxergam a possibilidade de um corte de juros ou QE emergencial(era uma política não convencional e já se fala sobre usar novamente, tá virando bagunça)"
        ,  unsafe_allow_html=True
    )
    subtema_pm = option_menu(
        menu_title=None,
        options=[ "Dados de Política Monetária", "Juros de Títulos Públicos"],
        default_index=0,
        orientation="horizontal"
    )
    if subtema_pm == 'Juros de Títulos Públicos':
        
        st.pyplot(graf_3m)
        st.pyplot(graf_10yr)
        st.pyplot(graf_7yr)
        st.pyplot(graf_20yr)
        st.pyplot(graf_30yr)
        plt.close("all")
    if subtema_pm == "Dados de Política Monetária":
        
        st.pyplot(graf_ffr)
        st.pyplot(graf_dif_r)
        st.pyplot(graf_ta)
        st.pyplot(graf_repo)
        st.pyplot(graf_tga)
        st.pyplot(graf_mv)
        plt.close("all")


        
        