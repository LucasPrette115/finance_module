import streamlit as st
from app.utils.process_file import process_financial_data
from app.repositories.transaction.transaction_repository import SqlAlchemyTransactionRepo
from app.services.transaction.transaction_service import TransactionService


def __init__(self, transaction_service: SqlAlchemyTransactionRepo):
    self.transaction_repository = 


def show():
            connection_uri = "postgresql://postgres:password@postgres:5432/personal_finance_dashboard"
            file = st.file_uploader("Upload file here")

            if st.button("Generate Dashboard"):
                if file is not None:
                    raw_transactions = process_financial_data(file)
                    load(raw_transactions, "raw_transactions", connection_uri)
                    cleaned_transactions = transform(raw_transactions)
                    load(cleaned_transactions, "transactions", connection_uri)
                else:
                    st.error("Please upload a file before generating the dashboard.")
            
            if st.button("Clear Data"):
                drop("raw_transactions", connection_uri)
                drop("transactions", connection_uri) 
            
            # DataFrames
            with st.expander('Raw Transactions Data'):
                raw_transactions = query("raw_transactions")
                st.dataframe(raw_transactions, height=400, use_container_width= True)
            with st.expander('Cleaned Transactions Data'):
                cleaned_transactions = query("transactions")
                st.dataframe(cleaned_transactions, height=400, use_container_width= True)
            with st.expander('Accounts Data'):
                accounts = query("daily_amount_over_time")
                st.dataframe(accounts, height=400, use_container_width= True)

   

        