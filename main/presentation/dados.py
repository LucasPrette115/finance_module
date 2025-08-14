import streamlit as st
from models.account import get_all_accounts
from models.transaction import Transaction, get_all_transactions, map_financial_data_to_db
from utils.process_file import process_financial_data
from infrastructure.db.session import SessionLocal

def show():    
        
            file = st.file_uploader("Selecione um arquivo")
            accounts = get_all_accounts()
                    
            account_options = {account.name: account.id for account in accounts}
                    
            selected_account_name = st.selectbox("Selecionar conta", list(account_options.keys()))
            selected_account_id = account_options[selected_account_name]
            
            if st.button("Generate Dashboard"):
                if file is not None:
                    raw_transactions = process_financial_data(file)
                    if not map_financial_data_to_db(raw_transactions, selected_account_id):
                        st.error("Falha ao inserir dados no banco.")                     
                else:
                    st.error("Selecione um arquivo antes de gerar.")
            
            # if st.button("Clear Data"):
            #     drop("raw_transactions", connection_uri)
            #     drop("transactions", connection_uri) 
            
            # DataFrames
            # with st.expander('Raw Transactions Data'):
            #     raw_transactions = process_financial_data(file)
            #     st.dataframe(raw_transactions, height=400, use_container_width= True)
            with st.expander('Dados transformados'):
                cleaned_transactions = get_all_transactions()
                st.dataframe(cleaned_transactions, height=400, use_container_width= True)
            # with st.expander('Accounts Data'):
            #     accounts = query("daily_amount_over_time")
            #     st.dataframe(accounts, height=400, use_container_width= True)

   
       