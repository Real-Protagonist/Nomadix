"""
Nomadix - Página de Previsões
Previsões de tendências turísticas com Prophet
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.forecasting import TouristForecastingModel

st.set_page_config(
    page_title="Previsões - Nomadix",
    page_icon="🔮",
    layout="wide"
)

st.title("🔮 Previsões Turísticas")
st.markdown("Previsões de tendências usando Prophet e análise de séries temporais")
st.markdown("---")


@st.cache_data
def load_sample_data():
    """Cria dados de exemplo"""
    dates = pd.date_range(start='2020-01-01', end='2024-12-31', freq='M')
    provincias = ['Luanda', 'Benguela', 'Huíla', 'Namibe', 'Cabinda']
    
    data = []
    for date in dates:
        for provincia in provincias:
            base = {'Luanda': 15000, 'Benguela': 8000, 'Huíla': 6000, 
                   'Namibe': 5000, 'Cabinda': 4000}[provincia]
            
            seasonal = base * (1 + 0.3 * np.sin(date.month * np.pi / 6))
            trend = base * 0.05 * (date.year - 2020)
            noise = np.random.normal(0, base * 0.1)
            
            visitantes = int(seasonal + trend + noise)
            
            data.append({
                'data': date,
                'provincia': provincia,
                'visitantes': visitantes
            })
    
    return pd.DataFrame(data)


# Carrega dados
df = load_sample_data()

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Configurações de Previsão")
    
    provincia_selecionada = st.selectbox(
        "Província",
        df['provincia'].unique()
    )
    
    periodos_previsao = st.slider(
        "Períodos a Prever (meses)",
        6, 24, 12
    )
    
    incluir_sazonalidade = st.checkbox("Incluir Sazonalidade Anual", value=True)
    
    st.markdown("---")
    st.info("💡 O modelo Prophet analisa padrões históricos para gerar previsões")

# Filtra dados da província
df_provincia = df[df['provincia'] == provincia_selecionada].copy()
df_provincia = df_provincia.sort_values('data')

# Preparação e treinamento do modelo
with st.spinner('Treinando modelo de previsão...'):
    model = TouristForecastingModel(yearly_seasonality=incluir_sazonalidade)
    
    # Prepara dados no formato Prophet
    prophet_df = model.prepare_data(df_provincia, 'data', 'visitantes')
    
    # Treina o modelo
    model.fit(prophet_df)
    
    # Gera previsões
    forecast = model.predict(periodos_previsao, freq='M')
    summary = model.get_forecast_summary(forecast)

st.success(f"✅ Modelo treinado! Previsões geradas para {periodos_previsao} meses")

# Visualização principal
st.markdown(f"## 📊 Previsão de Visitantes - {provincia_selecionada}")

# Separa dados históricos e previstos
dados_historicos = forecast[forecast['ds'] <= df_provincia['data'].max()]
dados_futuros = forecast[forecast['ds'] > df_provincia['data'].max()]

fig = go.Figure()

# Dados reais
fig.add_trace(go.Scatter(
    x=prophet_df['ds'],
    y=prophet_df['y'],
    mode='markers',
    name='Dados Históricos',
    marker=dict(color='#FF6B35', size=6)
))

# Previsão
fig.add_trace(go.Scatter(
    x=forecast['ds'],
    y=forecast['yhat'],
    mode='lines',
    name='Previsão',
    line=dict(color='#4ECDC4', width=3)
))

# Intervalo de confiança
fig.add_trace(go.Scatter(
    x=forecast['ds'],
    y=forecast['yhat_upper'],
    mode='lines',
    name='Limite Superior',
    line=dict(width=0),
    showlegend=False
))

fig.add_trace(go.Scatter(
    x=forecast['ds'],
    y=forecast['yhat_lower'],
    mode='lines',
    name='Intervalo de Confiança',
    line=dict(width=0),
    fillcolor='rgba(78, 205, 196, 0.2)',
    fill='tonexty'
))

fig.update_layout(
    title=f'Previsão de Visitantes - {provincia_selecionada}',
    xaxis_title='Data',
    yaxis_title='Visitantes',
    hovermode='x unified',
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# Métricas de previsão
st.markdown("### 📈 Métricas de Previsão")

col1, col2, col3, col4 = st.columns(4)

# Valores previstos
ultimo_real = prophet_df['y'].iloc[-1]
primeiro_previsto = dados_futuros['yhat'].iloc[0] if len(dados_futuros) > 0 else ultimo_real
ultimo_previsto = dados_futuros['yhat'].iloc[-1] if len(dados_futuros) > 0 else ultimo_real

with col1:
    st.metric(
        "Último Valor Real",
        f"{ultimo_real:,.0f}",
        "Dezembro 2024"
    )

with col2:
    variacao = ((primeiro_previsto - ultimo_real) / ultimo_real) * 100
    st.metric(
        "Próximo Mês Previsto",
        f"{primeiro_previsto:,.0f}",
        f"{variacao:+.1f}%"
    )

with col3:
    st.metric(
        f"Previsão ({periodos_previsao} meses)",
        f"{ultimo_previsto:,.0f}",
        f"Em {dados_futuros['ds'].iloc[-1].strftime('%b %Y') if len(dados_futuros) > 0 else 'N/A'}"
    )

with col4:
    media_prevista = dados_futuros['yhat'].mean() if len(dados_futuros) > 0 else 0
    st.metric(
        "Média Prevista",
        f"{media_prevista:,.0f}",
        "Período futuro"
    )

st.markdown("---")

# Componentes do modelo
st.markdown("### 🔍 Análise de Componentes")

components = model.get_components(forecast)

col1, col2 = st.columns(2)

with col1:
    if 'tendencia' in components:
        fig = px.line(
            components['tendencia'],
            x='ds',
            y='trend',
            title='Componente de Tendência'
        )
        fig.update_traces(line_color='#FF6B35', line_width=2)
        st.plotly_chart(fig, use_container_width=True)

with col2:
    if 'sazonalidade_anual' in components:
        fig = px.line(
            components['sazonalidade_anual'],
            x='ds',
            y='yearly',
            title='Componente de Sazonalidade Anual'
        )
        fig.update_traces(line_color='#4ECDC4', line_width=2)
        st.plotly_chart(fig, use_container_width=True)

# Tabela de previsões futuras
st.markdown("### 📅 Previsões Detalhadas")

if len(dados_futuros) > 0:
    df_previsoes = dados_futuros[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
    df_previsoes.columns = ['Data', 'Previsão', 'Limite Inferior', 'Limite Superior']
    df_previsoes['Data'] = df_previsoes['Data'].dt.strftime('%Y-%m')
    df_previsoes = df_previsoes.round(0)
    
    st.dataframe(df_previsoes, use_container_width=True, hide_index=True)
else:
    st.warning("Nenhuma previsão futura disponível")

# Insights
st.markdown("### 💡 Insights")

col1, col2 = st.columns(2)

with col1:
    tendencia_geral = (ultimo_previsto - ultimo_real) / ultimo_real * 100
    if tendencia_geral > 0:
        st.success(f"📈 **Tendência Positiva**: Crescimento esperado de {tendencia_geral:.1f}% nos próximos {periodos_previsao} meses")
    else:
        st.warning(f"📉 **Tendência Negativa**: Decrescimento esperado de {abs(tendencia_geral):.1f}% nos próximos {periodos_previsao} meses")

with col2:
    if 'sazonalidade_anual' in components:
        st.info("🌞 **Sazonalidade Detectada**: O modelo identificou padrões sazonais nos dados históricos")
    else:
        st.info("📊 **Sem Sazonalidade**: Não há padrão sazonal significativo detectado")

st.markdown("---")
st.markdown("← Voltar para o [Dashboard Principal](../app.py)")
