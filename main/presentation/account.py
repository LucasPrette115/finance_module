import streamlit as st
from models.account import Account
from infrastructure.db.session import SessionLocal

def create_account(name, description):
    session = SessionLocal()
    try:
        account = Account(name=name, description=description)
        session.add(account)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        st.error(f"Erro ao cadastrar: {e}")
        return False
    finally:
        session.close()

def show():
    st.title("Cadastro de Account")

    name = st.text_input("Nome")
    description = st.text_area("Descrição")

    if st.button("Cadastrar"):
        if name.strip():
            if create_account(name, description):
                st.success("Account criada com sucesso!")
        else:
            st.warning("O nome é obrigatório.")
