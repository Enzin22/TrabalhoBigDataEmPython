import streamlit as st
import pandas as pd
import plotly.express as px

# Configurar para usar a página toda
st.set_page_config(layout="wide")

# Carregar o arquivo
file_path = "clientes_alterados.xlsx"
df = pd.read_excel(file_path, engine='openpyxl')

# Transformar colunas de data para datetime
df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y %H:%M:%S')
df['data_pagamento'] = pd.to_datetime(df['data_pagamento'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
df['data_cancelamento'] = pd.to_datetime(df['data_cancelamento'], format='%d/%m/%Y %H:%M:%S', errors='coerce')

# Calcular lucro
df['lucro'] = df['total'] - df['total_produtos']

# Faturamento e lucro por mês
df['mes_ano'] = df['data'].dt.to_period('M')
faturamento_lucro_mensal = df.groupby('mes_ano').agg({'total': 'sum', 'lucro': 'sum'}).reset_index()

# Modelos mais vendidos
produtos_mais_vendidos = df.groupby('produto').agg({'quantidade': 'sum'}).reset_index().sort_values(by='quantidade', ascending=False).head(10)

# Tipos de pagamento mais utilizados
tipos_pagamento = df['pagamento'].value_counts().reset_index()
tipos_pagamento.columns = ['pagamento', 'frequencia']

# Definindo a divisão de tela
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

# Faturamento e lucro por mês
df['mes_ano'] = df['data'].dt.to_period('M')
faturamento_lucro_mensal = df.groupby('mes_ano').agg({'total': 'sum', 'lucro': 'sum'}).reset_index()

# Convert mes_ano to string
faturamento_lucro_mensal['mes_ano'] = faturamento_lucro_mensal['mes_ano'].astype(str)

# Faturamento e lucro mensal
fig_faturamento_lucro_mensal = px.bar(faturamento_lucro_mensal, x='mes_ano', y=['total', 'lucro'], title='Faturamento e Lucro Mensal')
col1.plotly_chart(fig_faturamento_lucro_mensal, use_container_width=True)

# Produtos mais vendidos
fig_produtos_mais_vendidos = px.bar(produtos_mais_vendidos, x='quantidade', y='produto', orientation='h', title='Produtos Mais Vendidos')
col2.plotly_chart(fig_produtos_mais_vendidos, use_container_width=True)

# Tipos de pagamento
fig_tipos_pagamento = px.pie(tipos_pagamento, names='pagamento', values='frequencia', title='Tipos de Pagamento Mais Utilizados')
col3.plotly_chart(fig_tipos_pagamento, use_container_width=True)

# Análise de cancelamentos
cancelamentos = df[df['data_cancelamento'].notna()].shape[0]
col4.metric("Número de Cancelamentos", cancelamentos)

# Exibir dataframe com as informações
st.dataframe(df)
