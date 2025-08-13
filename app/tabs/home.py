import streamlit as st
from PIL import Image

def show():
    st.subheader('Bem-vindo ao Dashboard de controle Financeiro')
    st.write('Esse dashboard permite que você visualize e analise seus dados financeiros de forma interativa, através de importações de arquivos XLSX/CSV.')
    col1, col2, col3 = st.columns(3)
    col1.metric("Saldo Atual", "R$ 12.450", "+5%")
    col2.metric("Receitas (mês)", "R$ 7.800", "+8%")
    col3.metric("Despesas (mês)", "R$ 5.200", "-3%")

    st.markdown("---")

    # try:
    #     personal_finance = Image.open('app/images/finance.jpg')
    #     st.image(personal_finance, caption='Source: The Big Short', use_container_width=True)
    # except FileNotFoundError:
    #     st.warning(f"Imagem não encontrada")

            
           
