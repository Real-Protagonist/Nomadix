"""
Nomadix - Página de Insights Regionais
Análise detalhada por província e região
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import sys
import os

st.set_page_config(
    page_title="Insights Regionais - Nomadix",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ Insights Regionais")
st.markdown("Análise comparativa e insights específicos por província de Angola")
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
                'gasto_medio': receita / visitantes,
                'hoteis': np.random.randint(10, 50),
                'restaurantes': np.random.randint(20, 100)
            })
    
    return pd.DataFrame(data)


# Carrega dados
df = load_sample_data()

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Seleção de Província")
    
    provincia_principal = st.selectbox(
        "Província Principal",
        df['provincia'].unique()
    )
    
    provincias_comparacao = st.multiselect(
        "Comparar com",
        [p for p in df['provincia'].unique() if p != provincia_principal],
        default=[p for p in df['provincia'].unique() if p != provincia_principal][:2]
    )
    
    st.markdown("---")
    st.markdown("### 📅 Período")
    ano_selecionado = st.selectbox("Ano", [2024, 2023, 2022, 2021, 2020], index=0)

# Filtra dados
df_ano = df[df['data'].dt.year == ano_selecionado]
df_provincia = df_ano[df_ano['provincia'] == provincia_principal]

# Perfil da Província
st.markdown(f"## 🏛️ Perfil: {provincia_principal}")

# Informações básicas da província
info_provincias = {
    'Luanda': {
        'descricao': 'Capital e maior centro urbano de Angola',
        'atracoes': ['Fortaleza de São Miguel', 'Ilha do Mussulo', 'Baía de Luanda'],
        'especialidade': 'Turismo urbano e de negócios'
    },
    'Benguela': {
        'descricao': 'Conhecida pelas belas praias do litoral',
        'atracoes': ['Praia Morena', 'Baía Azul', 'Lobito'],
        'especialidade': 'Turismo de praia'
    },
    'Huíla': {
        'descricao': 'Província montanhosa com clima ameno',
        'atracoes': ['Serra da Leba', 'Fenda da Tundavala', 'Cristo Rei'],
        'especialidade': 'Turismo de natureza'
    },
    'Namibe': {
        'descricao': 'Deserto do Namibe e paisagens únicas',
        'atracoes': ['Deserto do Namibe', 'Iona National Park', 'Arco'],
        'especialidade': 'Turismo de aventura'
    },
    'Cabinda': {
        'descricao': 'Província costeira com rica biodiversidade',
        'atracoes': ['Reserva de Maiombe', 'Praias', 'Cachoeiras'],
        'especialidade': 'Ecoturismo'
    }
}

info = info_provincias.get(provincia_principal, {})

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"**Descrição:** {info.get('descricao', 'N/A')}")
    st.markdown(f"**Especialidade:** {info.get('especialidade', 'N/A')}")
    st.markdown(f"**Principais Atrações:**")
    for atracao in info.get('atracoes', []):
        st.markdown(f"- {atracao}")

with col2:
    # Estatísticas resumidas
    total_visitantes = df_provincia['visitantes'].sum()
    receita_total = df_provincia['receita'].sum()
    
    st.metric("Total de Visitantes (2024)", f"{total_visitantes:,.0f}")
    st.metric("Receita Total (USD)", f"${receita_total:,.0f}")

st.markdown("---")

# Métricas comparativas
st.markdown(f"## 📊 Indicadores - {ano_selecionado}")

# Calcula métricas agregadas
df_metricas = df_ano.groupby('provincia').agg({
    'visitantes': 'sum',
    'receita': 'sum',
    'estadia_media': 'mean',
    'satisfacao': 'mean',
    'gasto_medio': 'mean'
}).reset_index()

# Encontra posição da província
df_metricas_sorted = df_metricas.sort_values('visitantes', ascending=False)
posicao = df_metricas_sorted[df_metricas_sorted['provincia'] == provincia_principal].index[0] + 1

col1, col2, col3, col4, col5 = st.columns(5)

provincia_data = df_metricas[df_metricas['provincia'] == provincia_principal].iloc[0]

with col1:
    st.metric(
        "Ranking",
        f"#{posicao}",
        f"de {len(df_metricas)} províncias"
    )

with col2:
    st.metric(
        "Visitantes",
        f"{provincia_data['visitantes']:,.0f}",
        "Total no ano"
    )

with col3:
    st.metric(
        "Receita",
        f"${provincia_data['receita']:,.0f}",
        "Total no ano"
    )

with col4:
    st.metric(
        "Estadia Média",
        f"{provincia_data['estadia_media']:.1f} dias",
        "Média anual"
    )

with col5:
    satisfacao = provincia_data['satisfacao']
    emoji = "😊" if satisfacao >= 4.5 else "🙂" if satisfacao >= 4.0 else "😐"
    st.metric(
        "Satisfação",
        f"{satisfacao:.2f}/5.0 {emoji}",
        "Média anual"
    )

st.markdown("---")

# Comparação com outras províncias
if provincias_comparacao:
    st.markdown("## 🔄 Comparação Regional")
    
    provincias_para_comparar = [provincia_principal] + provincias_comparacao
    df_comparacao = df_ano[df_ano['provincia'].isin(provincias_para_comparar)]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Visitantes
        df_vis = df_comparacao.groupby('provincia')['visitantes'].sum().reset_index()
        fig = px.bar(
            df_vis,
            x='provincia',
            y='visitantes',
            title='Comparação de Visitantes',
            color='provincia',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(showlegend=False, xaxis_title='', yaxis_title='Visitantes')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Receita
        df_rec = df_comparacao.groupby('provincia')['receita'].sum().reset_index()
        fig = px.bar(
            df_rec,
            x='provincia',
            y='receita',
            title='Comparação de Receita',
            color='provincia',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(showlegend=False, xaxis_title='', yaxis_title='Receita (USD)')
        st.plotly_chart(fig, use_container_width=True)
    
    # Radar chart
    st.markdown("### 🎯 Perfil Multidimensional")
    
    df_radar = df_comparacao.groupby('provincia').agg({
        'visitantes': 'sum',
        'receita': 'sum',
        'estadia_media': 'mean',
        'satisfacao': 'mean',
        'gasto_medio': 'mean'
    }).reset_index()
    
    # Normaliza valores para o radar
    for col in ['visitantes', 'receita', 'estadia_media', 'satisfacao', 'gasto_medio']:
        max_val = df_radar[col].max()
        if max_val > 0:
            df_radar[f'{col}_norm'] = df_radar[col] / max_val * 100
    
    fig = go.Figure()
    
    categorias = ['Visitantes', 'Receita', 'Estadia', 'Satisfação', 'Gasto Médio']
    
    for _, row in df_radar.iterrows():
        valores = [
            row['visitantes_norm'],
            row['receita_norm'],
            row['estadia_media_norm'],
            row['satisfacao_norm'],
            row['gasto_medio_norm']
        ]
        
        fig.add_trace(go.Scatterpolar(
            r=valores,
            theta=categorias,
            fill='toself',
            name=row['provincia']
        ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        title='Comparação Multidimensional (% do máximo)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Evolução temporal
st.markdown(f"## 📈 Evolução Temporal - {provincia_principal}")

df_provincia_all = df[df['provincia'] == provincia_principal]

col1, col2 = st.columns(2)

with col1:
    # Evolução mensal
    df_mensal = df_provincia_all.groupby(df_provincia_all['data'].dt.to_period('M')).agg({
        'visitantes': 'sum'
    }).reset_index()
    df_mensal['data'] = df_mensal['data'].dt.to_timestamp()
    
    fig = px.line(
        df_mensal,
        x='data',
        y='visitantes',
        title='Evolução Mensal de Visitantes',
        markers=True
    )
    fig.update_traces(line_color='#FF6B35', line_width=2)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Sazonalidade
    df_sazonal = df_provincia_all.copy()
    df_sazonal['mes'] = df_sazonal['data'].dt.month
    df_saz_agg = df_sazonal.groupby('mes')['visitantes'].mean().reset_index()
    
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
            'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    df_saz_agg['mes_nome'] = df_saz_agg['mes'].apply(lambda x: meses[x-1])
    
    fig = px.bar(
        df_saz_agg,
        x='mes_nome',
        y='visitantes',
        title='Padrão Sazonal (Média Mensal)',
        color='visitantes',
        color_continuous_scale='Oranges'
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# Recomendações
st.markdown("---")
st.markdown(f"## 💡 Recomendações para {provincia_principal}")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background-color: #e8f4f8; padding: 1rem; border-radius: 8px;">
        <h4>🎯 Estratégia de Marketing</h4>
        <p>Focar campanhas nos meses de alta sazonalidade para maximizar ocupação</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background-color: #fff4e6; padding: 1rem; border-radius: 8px;">
        <h4>🏨 Infraestrutura</h4>
        <p>Investir em capacidade hoteleira e serviços durante períodos de pico</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background-color: #f0f9ff; padding: 1rem; border-radius: 8px;">
        <h4>📱 Experiência</h4>
        <p>Melhorar satisfação através de apps móveis e guias turísticos</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("← Voltar para o [Dashboard Principal](../app.py)")
