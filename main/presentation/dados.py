import streamlit as st
from models.account import get_all_accounts
from models.transaction import Transaction, get_all_transactions, map_financial_data_to_db
from utils.process_file import process_financial_data
from infrastructure.db.session import SessionLocal
import pandas as pd

def show(selected_columns, view):    
        
            file = st.file_uploader("Selecione um arquivo")
            accounts = get_all_accounts()
                    
            account_options = {account.name: account.id for account in accounts}
                    
            selected_account_name = st.selectbox("Selecionar conta", list(account_options.keys()))
            selected_account_id = account_options[selected_account_name]
            
            if st.button("Processar"):
                if file is not None:
                    raw_transactions = process_financial_data(file)
                    if not map_financial_data_to_db(raw_transactions, selected_account_id):
                        st.error("Falha ao inserir dados no banco.")                     
                else:
                    st.error("Selecione um arquivo antes de gerar.")
            
            cleaned_transactions_df = get_all_transactions(selected_columns)
            cleaned_transactions_df['Data'] = pd.to_datetime(cleaned_transactions_df['Data'])
            monthly = cleaned_transactions_df.groupby(cleaned_transactions_df['Data'].dt.to_period('M'))
            for period, df_month in monthly:                
                with st.expander(f'{period}'):
                    st.dataframe(df_month, height=400, use_container_width=True)                   

                    if st.button(f"Excluir registros de {period}", key=f"delete_{period}"):                    
                        delete_transactions_by_month(period)
                        st.rerun()
                        st.dataframe(df_month, height=400, use_container_width=True) 
                        st.success(f"Registros de {period} excluídos com sucesso!")                  
 
def delete_transactions_by_month(period):
    session = SessionLocal()
    try:        
        start = period.start_time
        end = period.end_time
        session.query(Transaction).filter(
            Transaction.date >= start,
            Transaction.date <= end
        ).delete()
        session.commit()
    finally:
        session.close()
   
       