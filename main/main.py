import streamlit as st
from models.account import get__all_accounts
from presentation import home, dados, account, dashboard, docs
from infrastructure.db.session import SessionLocal

def main():
    st.set_page_config(page_title='Dashboard de controle Financeiro',
                    page_icon=':money_with_wings:',
                    layout='wide')
    
    st.title('Dashboard de controle Financeiro')
    tab1, tab2, tab3, tab4, tab5 = st.tabs(['Home', 'Dados', 'Dashboard', 'Contas', 'Documentação'])

    with st.sidebar:
        st.header('Filters')

        column_options = [x.name for x in get__all_accounts()]
        selected_columns = st.multiselect('Selecionar contas:', column_options)

        view = st.radio('Selecionar visualização:', ["Monthly", "Weekly", "Daily"], index=1, horizontal = True, key = "sidebar")

    with tab1:
        home.show()

    with tab2:
        dados.show()

    with tab4:
        account.show()        


if __name__ == '__main__':
    main()