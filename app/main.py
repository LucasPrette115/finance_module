import streamlit as st
from tabs import home, dados, dashboard, docs

def main():
    st.set_page_config(page_title='Dashboard de controle Financeiro',
                    page_icon=':money_with_wings:',
                    layout='wide')
    
    st.title('Dashboard de controle Financeiro')
    tab1, tab2, tab3, tab4 = st.tabs(['Home', 'Dados', 'Dashboard', 'Documentação'])

    with st.sidebar:
        st.header('Filters')

        column_options = ['Santander', 'Sofisa', 'Caixa']
        selected_columns = st.multiselect('Selecionar contas:', column_options, default='Santander')

        view = st.radio('Selecionar visualização:', ["monthly", "weekly", "daily"], index=1, horizontal = True, key = "sidebar")

    with tab1:
        home.show()

    with tab2:
        dados.show()


if __name__ == '__main__':
    main()