import streamlit as st
from models.account import get_all_accounts
from presentation import home, dados, account, docs
from infrastructure.db.session import SessionLocal

def main():
    st.set_page_config(page_title='Dashboard de controle Financeiro',
                    page_icon=':money_with_wings:',
                    layout='wide')
    
    st.title('Dashboard de controle Financeiro')
    tab1, tab2, tab3, tab5 = st.tabs(['Home', 'Dados', 'Contas', 'Documentação'])

    with st.sidebar:
        st.header('Filters')

        column_options = {x.id: x.name for x in get_all_accounts()}      
            
        selected_names = st.multiselect("Selecionar contas:", column_options.values(), default=next(iter(column_options.values()))) 
 
        selected_columns = [id for id, name in column_options.items() if name in selected_names]

        view = st.radio('Selecionar visualização:', ["Mensal", "Semanal", "Diário"], index=0, horizontal = True, key = "sidebar")

    with tab1:
        home.show(selected_columns, view)

    with tab2:
        dados.show(selected_columns, view)

    with tab3:
        account.show()        


if __name__ == '__main__':
    main()