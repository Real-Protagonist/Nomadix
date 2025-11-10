"""
Nomadix - Versão Sem PyArrow
Sistema de Insights para Planejamento Turístico em Angola
"""

import sys
import os

try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False
    print("Streamlit não disponível")

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("Pandas não disponível")

try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    print("Plotly não disponível")

def generate_simple_data():
    """Gera dados simples sem pandas"""
    return {
        'provincias': ['Luanda', 'Benguela', 'Huíla', 'Namibe', 'Kwanza Sul'],
        'visitantes_2024': [520000, 135000, 92000, 78000, 52000],
        'receita_aoa': [10312500000, 2640000000, 1732500000, 1485000000, 990000000],
        'satisfacao': [4.2, 4.5, 4.7, 4.3, 4.1]
    }

def main():
    """Função principal"""
    if not STREAMLIT_AVAILABLE:
        print("Por favor instale streamlit: pip install streamlit")
        return
    
    # Configuração da página
    st.set_page_config(
        page_title="Nomadix - Dashboard Turístico",
        page_icon="🌍",
        layout="wide"
    )
    
    # CSS para cards e perfil de usuário
    st.markdown("""
    <style>
    .metric-card {
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .card-visitors { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    .card-revenue { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
    .card-satisfaction { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
    .card-growth { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
    .metric-title { font-size: 0.9rem; font-weight: 600; margin-bottom: 0.5rem; }
    .metric-value { font-size: 2rem; font-weight: bold; }
    .metric-delta { font-size: 0.8rem; margin-top: 0.5rem; }
    
    /* Perfil de usuário */
    .user-profile {
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 1000;
        background: white;
        border-radius: 50px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        padding: 0.5rem;
        display: flex;
        align-items: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .user-profile:hover {
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
        transform: translateY(-2px);
    }
    
    .profile-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Perfil de usuário
    st.markdown("""
        <div class="user-profile" title="Perfil do Usuário">
            <div class="profile-avatar">AD</div>
            <span style="margin-left: 0.5rem; font-weight: 500; color: #333;">Admin</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Título
    st.markdown("<h1 style='text-align: center; color: #FF6B35;'>🌍 NOMADIX</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Dashboard de Insights Turísticos - Angola</h3>", unsafe_allow_html=True)
    
    # Dados
    data = generate_simple_data()
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    total_visitantes = sum(data['visitantes_2024'])
    receita_total = sum(data['receita_aoa'])
    satisfacao_media = sum(data['satisfacao']) / len(data['satisfacao'])
    
    with col1:
        st.markdown(f"""
        <div class="metric-card card-visitors">
            <div class="metric-title">👥 Total de Visitantes 2024</div>
            <div class="metric-value">{total_visitantes:,}</div>
            <div class="metric-delta">+15.2% vs 2023</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        receita_bilhoes = receita_total / 1_000_000_000
        st.markdown(f"""
        <div class="metric-card card-revenue">
            <div class="metric-title">💰 Receita Total</div>
            <div class="metric-value">{receita_bilhoes:.1f}B AOA</div>
            <div class="metric-delta">Kwanza Angolano</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card card-satisfaction">
            <div class="metric-title">⭐ Satisfação Média</div>
            <div class="metric-value">{satisfacao_media:.1f}/5.0</div>
            <div class="metric-delta">Excelente qualidade</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card card-growth">
            <div class="metric-title">📈 Crescimento Anual</div>
            <div class="metric-value">15.2%</div>
            <div class="metric-delta">Tendência positiva</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Gráficos (se plotly disponível)
    if PLOTLY_AVAILABLE:
        st.subheader("📊 Análise por Província")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.bar(
                x=data['provincias'], 
                y=data['visitantes_2024'],
                title="Visitantes por Província (2024)",
                color_discrete_sequence=['#FF6B35']
            )
            fig1.update_layout(showlegend=False)
            st.plotly_chart(fig1, width='stretch')
        
        with col2:
            fig2 = px.pie(
                names=data['provincias'],
                values=data['receita_aoa'],
                title="Distribuição de Receita (AOA)",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig2.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig2, width='stretch')
    else:
        st.warning("📊 Gráficos indisponíveis. Instale plotly: pip install plotly")
    
    # Tabela com header colorido
    st.subheader("📋 Dados por Província")
    
    # Header colorido da tabela
    st.markdown("""
    <div style="background-color: #FF6B35; padding: 12px; border-radius: 10px 10px 0 0; margin-bottom: 0;">
        <div style="display: flex; color: white; font-weight: bold;">
            <div style="flex: 2; text-align: left;">Província</div>
            <div style="flex: 2; text-align: center;">Visitantes 2024</div>
            <div style="flex: 2.5; text-align: center;">Receita (AOA)</div>
            <div style="flex: 1.5; text-align: center;">Satisfação</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Dados da tabela com espaçamento reduzido
    for i in range(len(data['provincias'])):
        bg_color = "#f9f9f9" if i % 2 == 0 else "#ffffff"
        
        st.markdown(f"""
        <div style="background-color: {bg_color}; padding: 8px 12px; margin: 0; border-bottom: 1px solid #e0e0e0;">
            <div style="display: flex; align-items: center;">
                <div style="flex: 2; font-weight: bold; color: #333;">{data['provincias'][i]}</div>
                <div style="flex: 2; text-align: center;">{data['visitantes_2024'][i]:,}</div>
                <div style="flex: 2.5; text-align: center;">{data['receita_aoa'][i]:,.0f} AOA</div>
                <div style="flex: 1.5; text-align: center;">⭐ {data['satisfacao'][i]}/5.0</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Fechamento da tabela
    st.markdown("""
    <div style="border-radius: 0 0 10px 10px; border: 1px solid #e0e0e0; height: 1px; margin-top: 0;"></div>
    """, unsafe_allow_html=True)
    
    # Insights
    st.subheader("🎯 Insights Principais")
    
    insights = [
        "🏆 Luanda mantém liderança absoluta no setor turístico nacional",
        "📈 Crescimento consistente de 15% no número de visitantes",
        "⭐ Huíla apresenta o maior índice de satisfação dos turistas",
        "🌟 Grande potencial de desenvolvimento no turismo interior",
        "💰 Receita total de 17.2 bilhões de AOA demonstra forte economia turística"
    ]
    
    for insight in insights:
        st.info(insight)
    
    # Sidebar com informações
    st.sidebar.header("🎛️ Informações do Sistema")
    st.sidebar.info(f"""
    **Status das Dependências:**
    - Streamlit: ✅
    - Pandas: {'✅' if PANDAS_AVAILABLE else '❌'}
    - Plotly: {'✅' if PLOTLY_AVAILABLE else '❌'}
    
    **Moeda:** Kwanza Angolano (AOA)
    **Última atualização:** Novembro 2025
    """)

if __name__ == "__main__":
    main()