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
        "Selecione o Subtema (Inflação)",
        ["PCE", "CPI", "PPI"]
    )

    if subtema == "PCE":
        st.write(
            "O dado cheio do PCE avançou 0,33% m/m em janeiro, enquanto o núcleo subiu 0,25% m/m, ambas em linha com as projeções de mercado..."
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
        "A criação líquida de empregos no Payroll foi de 151 mil no mês de fevereiro..."
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

elif menu == 'Política Monetária e Juros':
    subtema_pm = option_menu(
        menu_title=None,
        options=[ "Dados de Política Monetária"],
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

elif menu == "Atividade Econômica":
    subtema_atividade = option_menu(
        menu_title=None,
        options=["Renda", "Consumo", "Vendas no Varejo", "PIB"],
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




        
        