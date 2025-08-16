import pandas as pd
import streamlit as st
from models.transaction import get_all_transactions
import plotly.express as px
import altair as alt

def show():
    df = load_data()
    df['Data'] = pd.to_datetime(df['Data'])
    
    df['Mês'] = df['Data'].dt.to_period('M')
    df['Valor Líquido'] = df['Crédito (R$)'] - df['Débito (R$)']    
    
    monthly = df.groupby('Mês').agg(
        month=('Mês', 'first'),
        total_credit=('Crédito (R$)', 'sum'),
        total_debit=("Débito (R$)", "sum"),
        total_net=("Valor Líquido", "sum"),
        tx_count=("Descrição", "count")
         ).reset_index().sort_values('Mês')
    
    monthly['Crescimento (%)'] = (monthly['total_net'].pct_change()) * 100
    monthly['Mês_ts'] = monthly['Mês'].dt.to_timestamp()
    
    current = monthly.iloc[-1]
    previous = monthly.iloc[-2] if len(monthly) >= 2 else None
    
    balance_delta = current['total_net'] - (previous['total_net'] if previous is not None else 0)
    credit_delta = current['total_credit'] - (previous['total_credit'] if previous is not None else 0)
    debit_delta = current['total_debit'] - (previous['total_debit'] if previous is not None else 0)
    
    balance_delta_pct = pct_change(current['total_net'], previous['total_net']) if previous is not None else None
    credit_delta_pct = pct_change(current['total_credit'], previous['total_credit']) if previous is not None else None
    debit_delta_pct = pct_change(current['total_debit'], previous['total_debit']) if previous is not None else None 
    
    
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Saldo (mês)", 
        f"R$ {current['total_net']:,.2f}" if current['total_net'] is not None else "—",
        delta=f"{balance_delta_pct:.2f}%" if balance_delta_pct is not None else None
    )

    col2.metric(
        "Créditos (mês)",
        f"R$ {current['total_credit'] :,.2f}" if current['total_credit'] is not None else "—",
        delta=f"{credit_delta_pct:.2f}%" if credit_delta_pct is not None else None
    )

    col3.metric(
        "Débitos (mês)",
        f"R$ {current['total_debit']:,.2f}" if current['total_debit'] is not None else "—",
        delta=f"{debit_delta_pct:.2f}%" if debit_delta_pct is not None else None,
        delta_color="inverse" 
    )
    
    st.subheader("Gráficos de Desempenho")
    display_line_chart = (
        monthly[['Mês_ts', 'total_net']]
        .rename(columns={'Mês_ts': 'Período', 'total_net': 'Valor Líquido'})
        .copy()
    )
    display_line_chart['Valor Líquido'] = (
        display_line_chart['Valor Líquido']
        .astype(float)        
    )
    
    chart = alt.Chart(display_line_chart).mark_line(color="#2bff00").encode(
        x='Período',
        y='Valor Líquido'
    )

    st.altair_chart(chart, use_container_width=True, key='display_line_chart')
    pie_data = pd.DataFrame({
        "Tipo": ["Crédito", "Débito"],
        "Valor": [current["total_credit"], current["total_debit"]]
    })

    fig_pie = px.pie(
        pie_data,
        names="Tipo",
        values="Valor",
        title="Crédito vs Débito (Mês Atual)",
        color_discrete_sequence=["#00ff99", "#ff0000"] 
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)    
    
    st.subheader("Evolução Mensal")
    display_df = monthly[['Mês_ts', 'total_credit', 'total_debit', 'total_net', 'Crescimento (%)']].copy()
    display_df.rename(columns={'Mês_ts': 'Mês', 'total_credit': 'Crédito', 'total_debit': 'Débito', 'total_net': 'Valor Líquido'}, inplace=True)
    display_df['Mês'] = display_df['Mês'].dt.strftime('%Y-%m')

    st.dataframe(display_df.style.format({
        'Crédito': 'R$ {:,.2f}',
        'Débito': 'R$ {:,.2f}',
        'Valor Líquido': 'R$ {:,.2f}',
        'Crescimento (%)': '{:.2f}%' 
    }).apply(highlight_growth, subset=['Crescimento (%)']), height=300)

def pct_change(curr, prev):
    if prev is None or prev == 0:
        return None
    return (curr - prev) / abs(prev) * 100

def highlight_growth(s):
    return ['color: green' if v > 0 else 'color: red' for v in s]

@st.cache_data
def load_data():
    return get_all_transactions()
