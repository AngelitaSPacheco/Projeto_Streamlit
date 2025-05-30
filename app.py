# Importando as bibliotecas
import streamlit as st
import pandas as pd
import plotly.express as px

# Carregando os dados
dados = pd.read_excel('Vendas_Base_de_Dados.xlsx')

# Calcula o faturamento em cada linha
dados['Faturamento'] = dados['Quantidade'] * dados['Valor Unitário']

# Inserindo os filtros na barra lateral
st.sidebar.header("Filtros")
lojas = sorted(dados['Loja'].unique())
produtos = ['Todos'] + sorted(dados['Produto'].unique())

loja_escolhida = st.sidebar.selectbox('Escolha a loja:', lojas)
produto_escolhido = st.sidebar.selectbox('Escolha o produto:', produtos)

# Aplicando os filtros
dados_filtrados = dados[dados['Loja'] == loja_escolhida]
if produto_escolhido != 'Todos':
    dados_filtrados = dados_filtrados[dados_filtrados['Produto'] == produto_escolhido]

# Exibindo o título e a tabela com os dados filtrados
st.title("Dashboard de Vendas")

if not dados_filtrados.empty:
    st.write("Tabela de vendas do mês (após filtros):")
    st.dataframe(dados_filtrados)

    # Calculando e exibindo o faturamento total com base nos filtros
    faturamento_total = dados_filtrados['Faturamento'].sum()
    st.markdown(f"### Faturamento total: **R$ {faturamento_total:,.2f}**")

else:
    st.info("Nenhum dado disponível para os filtros selecionados.")

# Gráfico de faturamento por loja (independente dos filtros)
faturamento_por_loja = (
    dados.groupby('Loja')['Faturamento']
    .sum()
    .reset_index()
    .sort_values(by='Loja')  # Ordem alfabética
)

grafico = px.bar(faturamento_por_loja, x='Loja', y='Faturamento', title='Faturamento por Loja')
st.plotly_chart(grafico)

# Gráfico de pizza com participação dos produtos (só se houver dados filtrados)
if not dados_filtrados.empty:
    faturamento_por_produto = (
        dados_filtrados.groupby('Produto')['Faturamento']
        .sum()
        .reset_index()
        .sort_values(by='Faturamento', ascending=False)
    )

    grafico_pizza = px.pie(
        faturamento_por_produto,
        names='Produto',
        values='Faturamento',
        title=f'Participação dos produtos no faturamento da loja {loja_escolhida}'
    )
    st.plotly_chart(grafico_pizza)

    # Exibindo resumo textual destacado com base nos filtros aplicados
    if produto_escolhido != 'Todos':
        texto = f'<b>Na loja {loja_escolhida}, o produto "{produto_escolhido}" teve um faturamento total de R$ {faturamento_total:,.2f}.</b>'
    else:
        texto = f'<b>Na loja {loja_escolhida}, o faturamento total considerando todos os produtos foi de R$ {faturamento_total:,.2f}.</b>'

    st.markdown(f"""
    <div style="background-color:#e6f0fa; padding:10px; border-radius:5px; color:#004080;">
        {texto}
    </div>
    """, unsafe_allow_html=True)
