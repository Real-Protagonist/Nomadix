"""
Nomadix - Página de Análise Detalhada
Análises aprofundadas com Machine Learning
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

from utils.data_processor import DataProcessor
from models.clustering import TouristClusteringModel

st.set_page_config(
    page_title="Análise Detalhada - Nomadix",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Análise Detalhada")
st.markdown("Análises avançadas com clustering e segmentação de dados turísticos")
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
            receita = visitantes * np.random.uniform(50, 150)
            
            data.append({
                'data': date,
                'provincia': provincia,
                'visitantes': visitantes,
                'receita': receita,
                'estadia_media': np.random.uniform(2, 7),
                'satisfacao': np.random.uniform(3.5, 5.0),
                'gasto_medio': receita / visitantes
            })
    
    return pd.DataFrame(data)


# Carrega dados
df = load_sample_data()

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Configurações de Análise")
    
    tipo_analise = st.selectbox(
        "Tipo de Análise",
        ["Clustering de Destinos", "Análise de Correlação", "Análise Temporal"]
    )
    
    if tipo_analise == "Clustering de Destinos":
        n_clusters = st.slider("Número de Clusters", 2, 7, 4)

# Análise por tipo
if tipo_analise == "Clustering de Destinos":
    st.markdown("## 🎯 Clustering de Destinos Turísticos")
    st.markdown("Segmentação de províncias baseada em características turísticas")
    
    # Prepara dados para clustering
    df_clustering = df.groupby('provincia').agg({
        'visitantes': 'mean',
        'receita': 'mean',
        'estadia_media': 'mean',
        'satisfacao': 'mean',
        'gasto_medio': 'mean'
    }).reset_index()
    
    # Aplica clustering
    model = TouristClusteringModel(n_clusters=n_clusters)
    feature_cols = ['visitantes', 'receita', 'estadia_media', 'satisfacao', 'gasto_medio']
    
    labels = model.fit_predict(df_clustering, feature_cols)
    df_clustering['cluster'] = labels
    
    # Visualização
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.scatter(
            df_clustering,
            x='visitantes',
            y='receita',
            color='cluster',
            size='satisfacao',
            hover_data=['provincia'],
            title='Clustering: Visitantes vs Receita',
            labels={'cluster': 'Cluster'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(
            df_clustering,
            x='estadia_media',
            y='gasto_medio',
            color='cluster',
            size='satisfacao',
            hover_data=['provincia'],
            title='Clustering: Estadia vs Gasto Médio',
            labels={'cluster': 'Cluster'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabela de clusters
    st.markdown("### 📊 Características dos Clusters")
    
    cluster_stats = df_clustering.groupby('cluster').agg({
        'visitantes': 'mean',
        'receita': 'mean',
        'estadia_media': 'mean',
        'satisfacao': 'mean',
        'gasto_medio': 'mean'
    }).round(2)
    
    st.dataframe(cluster_stats, use_container_width=True)
    
    # Províncias por cluster
    st.markdown("### 🗺️ Províncias por Cluster")
    for cluster_id in sorted(df_clustering['cluster'].unique()):
        provincias_cluster = df_clustering[df_clustering['cluster'] == cluster_id]['provincia'].tolist()
        st.info(f"**Cluster {cluster_id}:** {', '.join(provincias_cluster)}")

elif tipo_analise == "Análise de Correlação":
    st.markdown("## 🔗 Análise de Correlação")
    st.markdown("Correlações entre variáveis turísticas")
    
    # Matriz de correlação
    df_corr = df[['visitantes', 'receita', 'estadia_media', 'satisfacao']].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=df_corr.values,
        x=df_corr.columns,
        y=df_corr.columns,
        colorscale='RdBu',
        zmid=0,
        text=df_corr.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 12}
    ))
    
    fig.update_layout(
        title='Matriz de Correlação',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Scatter plots de correlações
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.scatter(
            df,
            x='visitantes',
            y='receita',
            color='provincia',
            trendline='ols',
            title='Visitantes vs Receita'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(
            df,
            x='estadia_media',
            y='satisfacao',
            color='provincia',
            trendline='ols',
            title='Estadia Média vs Satisfação'
        )
        st.plotly_chart(fig, use_container_width=True)

elif tipo_analise == "Análise Temporal":
    st.markdown("## ⏰ Análise Temporal")
    st.markdown("Padrões e tendências ao longo do tempo")
    
    provincia_selecionada = st.selectbox(
        "Selecione a Província",
        df['provincia'].unique()
    )
    
    df_provincia = df[df['provincia'] == provincia_selecionada].copy()
    df_provincia = df_provincia.sort_values('data')
    
    # Gráfico de série temporal
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_provincia['data'],
        y=df_provincia['visitantes'],
        mode='lines+markers',
        name='Visitantes',
        line=dict(color='#FF6B35', width=2)
    ))
    
    # Adiciona média móvel
    df_provincia['ma_3'] = df_provincia['visitantes'].rolling(window=3).mean()
    
    fig.add_trace(go.Scatter(
        x=df_provincia['data'],
        y=df_provincia['ma_3'],
        mode='lines',
        name='Média Móvel (3 meses)',
        line=dict(color='#4ECDC4', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title=f'Evolução de Visitantes - {provincia_selecionada}',
        xaxis_title='Data',
        yaxis_title='Visitantes',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Taxa de crescimento
    col1, col2 = st.columns(2)
    
    with col1:
        processor = DataProcessor()
        growth_rate = processor.calculate_growth_rate(df_provincia, 'visitantes')
        
        fig = px.bar(
            x=df_provincia['data'],
            y=growth_rate,
            title='Taxa de Crescimento (%)',
            labels={'x': 'Data', 'y': 'Crescimento (%)'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Decomposição sazonal
        df_mensal = df_provincia.copy()
        df_mensal['mes'] = df_mensal['data'].dt.month
        
        df_sazonal = df_mensal.groupby('mes')['visitantes'].mean().reset_index()
        
        meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        df_sazonal['mes_nome'] = df_sazonal['mes'].apply(lambda x: meses[x-1])
        
        fig = px.line(
            df_sazonal,
            x='mes_nome',
            y='visitantes',
            title='Padrão Sazonal',
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("← Voltar para o [Dashboard Principal](../app.py)")
