import pandas as pd
import streamlit as st
from models.transaction import get_all_transactions
import plotly.express as px
import altair as alt
import numpy as np

def show(selected_columns, view):
    df = get_all_transactions(selected_columns)
    df['Data'] = pd.to_datetime(df['Data'])
    
    if view == "Mensal":
        df['Período'] = df['Data'].dt.to_period('M')
    if view == "Semanal":
        df['Período'] = df['Data'].dt.to_period('W')
    if view == "Diário":
        df['Período'] = df['Data'].dt.to_period('D')    
   
    df['Valor Líquido'] = df['Crédito (R$)'] - df['Débito (R$)']    
    
    period_df = df.groupby('Período').agg(
        month=('Período', 'first'),
        total_credit=('Crédito (R$)', 'sum'),
        total_debit=("Débito (R$)", "sum"),
        total_net=("Valor Líquido", "sum"),
        tx_count=("Descrição", "count")
         ).reset_index().sort_values('Período')
    
    period_df['Crescimento (%)'] = (period_df['total_net'].diff() / period_df['total_net'].abs().shift().replace(0, np.nan)) * 100
    period_df['Período_ts'] = period_df['Período'].dt.to_timestamp()
    
    current = period_df.iloc[-1]
    previous = period_df.iloc[-2] if len(period_df) >= 2 else None 
    
    balance_delta_pct = pct_change(current['total_net'], previous['total_net']) if previous is not None else None
    credit_delta_pct = pct_change(current['total_credit'], previous['total_credit']) if previous is not None else None
    debit_delta_pct = pct_change(current['total_debit'], previous['total_debit']) if previous is not None else None     
    
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Saldo", 
        f"R$ {current['total_net']:,.2f}" if current['total_net'] is not None else "—",
        delta=f"{balance_delta_pct:.2f}%" if balance_delta_pct is not None else None
    )

    col2.metric(
        "Créditos",
        f"R$ {current['total_credit'] :,.2f}" if current['total_credit'] is not None else "—",
        delta=f"{credit_delta_pct:.2f}%" if credit_delta_pct is not None else None
    )

    col3.metric(
        "Débitos",
        f"R$ {current['total_debit']:,.2f}" if current['total_debit'] is not None else "—",
        delta=f"{debit_delta_pct:.2f}%" if debit_delta_pct is not None else None,
        delta_color="inverse" 
    )
    
    st.subheader("Gráficos de Desempenho")
    display_line_chart = (
        period_df[['Período_ts', 'total_net']]
        .rename(columns={'Período_ts': 'Período', 'total_net': 'Valor Líquido'})
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
        title="Crédito vs Débito",
        color_discrete_sequence=["#2bff00", "#ff0000"] 
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)    
    
    st.subheader("Evolução Mensal")
    display_df = period_df[['Período_ts', 'total_credit', 'total_debit', 'total_net', 'Crescimento (%)']].copy()
    display_df.rename(columns={'Período_ts': 'Período', 'total_credit': 'Crédito', 'total_debit': 'Débito', 'total_net': 'Valor Líquido'}, inplace=True)
    # display_df['Período'] = display_df['Período'].dt.strftime()

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

