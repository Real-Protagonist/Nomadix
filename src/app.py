"""
Nomadix - Dashboard Principal
Sistema de Insights para Planejamento Turístico em Angola
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from utils.data_loader import DataLoader
from utils.data_processor import DataProcessor
from utils.visualizer import DataVisualizer
from models.clustering import TouristClusteringModel
from models.forecasting import TouristForecastingModel


# Configuração da página
st.set_page_config(
    page_title="Nomadix - Dashboard Turístico",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #FF6B35;
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


def load_sample_data():
    """Cria dados de exemplo para demonstração"""
    # Gera dados sintéticos de turismo
    dates = pd.date_range(start='2020-01-01', end='2024-12-31', freq='M')
    
    # Dados de visitantes por província
    provincias = ['Luanda', 'Benguela', 'Huíla', 'Namibe', 'Cabinda']
    
    data = []
    for date in dates:
        for provincia in provincias:
            base = {'Luanda': 15000, 'Benguela': 8000, 'Huíla': 6000, 
                   'Namibe': 5000, 'Cabinda': 4000}[provincia]
            
            # Adiciona sazonalidade e tendência
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
                'satisfacao': np.random.uniform(3.5, 5.0)
            })
    
    return pd.DataFrame(data)


def main():
    """Função principal do dashboard"""
    
    # Header
    st.markdown('<h1 class="main-header">🌍 Nomadix</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Dashboard de Insights para Planejamento Turístico em Angola</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/200x80/FF6B35/FFFFFF?text=NOMADIX", use_container_width=True)
        st.markdown("### 🎯 Configurações")
        
        # Filtros
        st.markdown("#### Filtros de Análise")
        
        periodo = st.selectbox(
            "Período",
            ["Últimos 6 meses", "Último ano", "Últimos 2 anos", "Todos os dados"]
        )
        
        provincias_selecionadas = st.multiselect(
            "Províncias",
            ["Luanda", "Benguela", "Huíla", "Namibe", "Cabinda"],
            default=["Luanda", "Benguela", "Huíla"]
        )
        
        st.markdown("---")
        st.markdown("#### 📊 Navegação")
        st.page_link("pages/1_analise_detalhada.py", label="Análise Detalhada", icon="📈")
        st.page_link("pages/2_previsoes.py", label="Previsões", icon="🔮")
        st.page_link("pages/3_insights_regionais.py", label="Insights Regionais", icon="🗺️")
        
        st.markdown("---")
        st.info("💡 **Dica:** Use os filtros acima para personalizar sua análise")
    
    # Carrega dados
    import numpy as np
    df = load_sample_data()
    
    # Aplica filtros
    if provincias_selecionadas:
        df = df[df['provincia'].isin(provincias_selecionadas)]
    
    # Filtra por período
    hoje = df['data'].max()
    if periodo == "Últimos 6 meses":
        data_inicio = hoje - timedelta(days=180)
    elif periodo == "Último ano":
        data_inicio = hoje - timedelta(days=365)
    elif periodo == "Últimos 2 anos":
        data_inicio = hoje - timedelta(days=730)
    else:
        data_inicio = df['data'].min()
    
    df_filtrado = df[df['data'] >= data_inicio]
    
    # KPIs principais
    st.markdown("### 📊 Indicadores Principais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_visitantes = df_filtrado['visitantes'].sum()
        delta_visitantes = ((df_filtrado['visitantes'].tail(3).mean() / 
                           df_filtrado['visitantes'].head(3).mean()) - 1) * 100
        st.metric(
            "Total de Visitantes",
            f"{total_visitantes:,.0f}",
            f"{delta_visitantes:+.1f}%"
        )
    
    with col2:
        receita_total = df_filtrado['receita'].sum()
        delta_receita = ((df_filtrado['receita'].tail(3).mean() / 
                        df_filtrado['receita'].head(3).mean()) - 1) * 100
        st.metric(
            "Receita Total (USD)",
            f"${receita_total:,.0f}",
            f"{delta_receita:+.1f}%"
        )
    
    with col3:
        estadia_media = df_filtrado['estadia_media'].mean()
        st.metric(
            "Estadia Média (dias)",
            f"{estadia_media:.1f}",
            "Normal"
        )
    
    with col4:
        satisfacao_media = df_filtrado['satisfacao'].mean()
        st.metric(
            "Satisfação Média",
            f"{satisfacao_media:.2f}/5.0",
            "Bom" if satisfacao_media > 4.0 else "Regular"
        )
    
    st.markdown("---")
    
    # Gráficos principais
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Evolução de Visitantes")
        
        # Agrega por mês
        df_mensal = df_filtrado.groupby('data')['visitantes'].sum().reset_index()
        
        fig = px.line(
            df_mensal,
            x='data',
            y='visitantes',
            title='Número de Visitantes ao Longo do Tempo'
        )
        fig.update_traces(line_color='#FF6B35', line_width=3)
        fig.update_layout(
            xaxis_title='Data',
            yaxis_title='Visitantes',
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🗺️ Distribuição por Província")
        
        df_provincia = df_filtrado.groupby('provincia')['visitantes'].sum().reset_index()
        df_provincia = df_provincia.sort_values('visitantes', ascending=False)
        
        fig = px.bar(
            df_provincia,
            x='provincia',
            y='visitantes',
            title='Total de Visitantes por Província',
            color='visitantes',
            color_continuous_scale='Oranges'
        )
        fig.update_layout(
            xaxis_title='Província',
            yaxis_title='Visitantes',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Segunda linha de gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💰 Receita por Província")
        
        df_receita = df_filtrado.groupby('provincia')['receita'].sum().reset_index()
        
        fig = px.pie(
            df_receita,
            values='receita',
            names='provincia',
            title='Distribuição de Receita por Província',
            color_discrete_sequence=px.colors.sequential.Oranges
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Sazonalidade")
        
        df_sazonalidade = df_filtrado.copy()
        df_sazonalidade['mes'] = df_sazonalidade['data'].dt.month
        df_sazonal = df_sazonalidade.groupby('mes')['visitantes'].mean().reset_index()
        
        meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        df_sazonal['mes_nome'] = df_sazonal['mes'].apply(lambda x: meses[x-1])
        
        fig = px.bar(
            df_sazonal,
            x='mes_nome',
            y='visitantes',
            title='Média de Visitantes por Mês',
            color='visitantes',
            color_continuous_scale='Oranges'
        )
        fig.update_layout(
            xaxis_title='Mês',
            yaxis_title='Média de Visitantes',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Insights automáticos
    st.markdown("### 💡 Insights Automáticos")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        provincia_top = df_filtrado.groupby('provincia')['visitantes'].sum().idxmax()
        st.markdown(f"""
        <div class="insight-box">
            <h4>🏆 Destino Mais Popular</h4>
            <p><strong>{provincia_top}</strong> é a província com maior número de visitantes no período selecionado.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        crescimento = delta_visitantes
        trend = "crescimento" if crescimento > 0 else "decrescimento"
        st.markdown(f"""
        <div class="insight-box">
            <h4>📈 Tendência</h4>
            <p>O turismo está em <strong>{trend}</strong> com variação de <strong>{abs(crescimento):.1f}%</strong>.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        melhor_mes = df_sazonal.loc[df_sazonal['visitantes'].idxmax(), 'mes_nome']
        st.markdown(f"""
        <div class="insight-box">
            <h4>🌞 Melhor Época</h4>
            <p><strong>{melhor_mes}</strong> é o mês com maior fluxo turístico em média.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #666; padding: 2rem;">
            <p>Nomadix - Dashboard de Insights Turísticos | Desenvolvido para Angola 🇦🇴</p>
            <p style="font-size: 0.9rem;">Powered by Python • Streamlit • Pandas • Scikit-learn • Prophet</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
