import pandas as pd

def process_financial_data(file):
    df_raw = pd.read_excel(file)
    df_raw.columns = df_raw.columns.str.strip()
    expected_header = ['Data', 'Descrição', 'Docto', 'Situação', 'Crédito (R$)', 'Débito (R$)', 'Saldo (R$)']

    header_row = None
    footer_row = None
    for i, row in df_raw.iterrows():
        row_values = [str(x).strip() for x in row.values]
    
        if row_values == expected_header:        
            header_row = i
            
        if 'SALDO ANTERIOR' in row_values:
            footer_row = i  

        if footer_row and header_row:
            break
            
    df = df_raw.iloc[header_row + 1:footer_row + 1].copy()
    df.columns = expected_header
    df = df.reset_index(drop=True)

    df['Crédito (R$)'] = (
        df['Crédito (R$)']
        .fillna('0')
        .str.replace('.', '', regex=False)
        .str.replace(',', '.', regex=False)
        .str.strip()
    )

    df['Débito (R$)'] = (
        df['Débito (R$)']
        .fillna('0')
        .str.replace('.', '', regex=False)
        .str.replace(',', '.', regex=False)
        .str.strip()
    )

    df['Saldo (R$)'] = (
        df['Saldo (R$)']
        .fillna('0')
        .str.replace('.', '', regex=False)
        .str.replace(',', '.', regex=False)
        .str.strip()
    )

    df['Saldo (R$)'] = pd.to_numeric(df['Saldo (R$)'], errors='coerce').fillna(0)
    df['Crédito (R$)'] = pd.to_numeric(df['Crédito (R$)'], errors='coerce').fillna(0)
    df['Débito (R$)'] = pd.to_numeric(df['Débito (R$)'], errors='coerce').fillna(0)
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y', errors='coerce')
    df['Descrição'] = df['Descrição'].str.strip()
    df['Docto'] = df['Docto'].str.strip()
    df['Situação'] = df['Situação'].str.strip()
    
    return df       
    
