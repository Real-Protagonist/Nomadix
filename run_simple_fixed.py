import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

def generate_sample_data():
    """Gera dados de exemplo para Angola"""
    
    # Províncias de Angola
    provinces = [
        "Luanda", "Benguela", "Huíla", "Huambo", "Cabinda", "Cunene", 
        "Namibe", "Cuando Cubango", "Malanje", "Bié", "Cuanza Norte",
        "Cuanza Sul", "Lunda Norte", "Lunda Sul", "Bengo", "Moxico", "Uíge", "Zaire"
    ]
    
    # Gerar dados turísticos
    tourist_data = []
    for province in provinces:
        for month in range(1, 13):
            tourists = random.randint(1000, 8000)
            revenue_usd = random.randint(50000, 400000)
            revenue_aoa = revenue_usd * 825  # Conversão USD para AOA
            satisfaction = random.uniform(3.5, 5.0)
            
            tourist_data.append({
                'Província': province,
                'Mês': month,
                'Nome_Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                            'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'][month-1],
                'Visitantes': tourists,
                'Receita_USD': revenue_usd,
                'Receita_AOA': revenue_aoa,
                'Satisfação': satisfaction
            })
    
    return pd.DataFrame(tourist_data)

def format_aoa(value):
    """Formatar valores em Kwanza (AOA)"""
    if value >= 1_000_000_000:
        return f"AOA {value/1_000_000_000:.1f}B"
    elif value >= 1_000_000:
        return f"AOA {value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"AOA {value/1_000:.1f}K"
    else:
        return f"AOA {value:.0f}"

def main():
    st.set_page_config(
        page_title="NOMADIX - Dashboard Angola",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Verificar se os dados estão no cache
    if 'tourist_data' not in st.session_state:
        with st.spinner('Carregando dados turísticos de Angola...'):
            st.session_state.tourist_data = generate_sample_data()
    
    df = st.session_state.tourist_data
    
    # Verificar se o DataFrame está vazio
    if df.empty:
        st.error("❌ Erro ao carregar os dados. Tente recarregar a página.")
        return
    
    # CSS customizado para os cards
    st.markdown("""
        <style>
        /* Cards de métricas */
        .metric-card {
            padding: 1.5rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(4px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            margin-bottom: 1rem;
        }
        .metric-card-visitors {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .metric-card-revenue {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }
        .metric-card-satisfaction {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }
        .metric-card-growth {
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        }
        .metric-title {
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            opacity: 0.9;
        }
        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            margin: 0;
        }
        .metric-delta {
            font-size: 0.8rem;
            margin-top: 0.5rem;
        }
        
        /* Perfil de usuário simples */
        .user-profile {
            position: fixed;
            top: 1rem;
            right: 1rem;
            z-index: 1000;
            background: white;
            border-radius: 25px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            padding: 0.5rem 1rem;
            display: flex;
            align-items: center;
            border: 2px solid #FF6B35;
        }
        
        .profile-avatar {
            width: 35px;
            height: 35px;
            border-radius: 50%;
            background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 14px;
            margin-right: 0.5rem;
        }
        
        .profile-info {
            color: #333;
            font-size: 14px;
            font-weight: 500;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Perfil de usuário no canto superior direito (versão simples)
    current_hour = datetime.now().hour
    greeting = "🌅 Bom dia" if current_hour < 12 else "☀️ Boa tarde" if current_hour < 18 else "🌙 Boa noite"
    
    st.markdown(f"""
        <div class="user-profile">
            <div class="profile-avatar">AD</div>
            <div class="profile-info">{greeting}, Admin</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Título principal
    st.markdown("<h1 style='text-align: center; color: #FF6B35;'>🌍 NOMADIX</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Dashboard de Insights Turísticos - Angola</h3>", unsafe_allow_html=True)
    
    # Sidebar com menu
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%); border-radius: 10px; margin-bottom: 1rem;">
            <div style="width: 60px; height: 60px; background: white; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold; color: #FF6B35; margin-bottom: 0.5rem;">
                AD
            </div>
            <div style="color: white; font-weight: bold; font-size: 16px;">Admin Dashboard</div>
            <div style="color: rgba(255,255,255,0.8); font-size: 12px;">Administrador do Sistema</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.header("🎛️ Menu Principal")
        menu_option = st.selectbox(
            "Navegação:",
            ["🏠 Dashboard Principal", "👤 Meu Perfil", "📊 Relatórios", "⚙️ Configurações", "💬 Suporte"]
        )
        
        st.header("⚙️ Configurações")
        dark_mode = st.checkbox("🌙 Modo Escuro")
        notifications = st.checkbox("🔔 Notificações", value=True)
        
        st.header("📋 Status do Sistema")
        st.success("✅ Sistema Online")
        st.info(f"👤 **Admin** conectado")
        st.info(f"🕒 {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        
        if st.button("🚪 Logout", type="secondary"):
            st.success("👋 Logout realizado!")
    
    # Métricas principais
    total_visitors = df['Visitantes'].sum()
    total_revenue = df['Receita_AOA'].sum()
    avg_satisfaction = df['Satisfação'].mean()
    growth_rate = 15.3  # Simulado
    
    # Cards de métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card metric-card-visitors">
                <div class="metric-title">Total de Visitantes</div>
                <div class="metric-value">{total_visitors:,}</div>
                <div class="metric-delta">+12.5% vs mês anterior</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card metric-card-revenue">
                <div class="metric-title">Receita Total</div>
                <div class="metric-value">{format_aoa(total_revenue)}</div>
                <div class="metric-delta">+8.3% vs mês anterior</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card metric-card-satisfaction">
                <div class="metric-title">Satisfação Média</div>
                <div class="metric-value">{avg_satisfaction:.1f}/5.0</div>
                <div class="metric-delta">+0.2 vs mês anterior</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="metric-card metric-card-growth">
                <div class="metric-title">Taxa de Crescimento</div>
                <div class="metric-value">{growth_rate}%</div>
                <div class="metric-delta">+2.1% vs mês anterior</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Gráficos principais
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Visitantes por Província")
        province_data = df.groupby('Província')['Visitantes'].sum().sort_values(ascending=False).head(10)
        
        fig_bar = px.bar(
            x=province_data.values,
            y=province_data.index,
            orientation='h',
            title="Top 10 Províncias por Visitantes",
            color=province_data.values,
            color_continuous_scale=['#FF6B35', '#F7931E']
        )
        fig_bar.update_layout(
            height=400,
            showlegend=False,
            xaxis_title="Número de Visitantes",
            yaxis_title="Província"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.subheader("💰 Receita por Mês (AOA)")
        monthly_revenue = df.groupby('Nome_Mês')['Receita_AOA'].sum()
        months_order = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        monthly_revenue = monthly_revenue.reindex(months_order)
        
        fig_line = px.line(
            x=monthly_revenue.index,
            y=monthly_revenue.values,
            title="Evolução da Receita Mensal",
            markers=True
        )
        fig_line.update_traces(
            line_color='#FF6B35',
            marker_color='#F7931E',
            marker_size=8
        )
        fig_line.update_layout(
            height=400,
            xaxis_title="Mês",
            yaxis_title="Receita (AOA)"
        )
        st.plotly_chart(fig_line, use_container_width=True)
    
    # Mapa de calor da satisfação
    st.subheader("🌡️ Mapa de Satisfação por Província e Mês")
    
    # Preparar dados para o mapa de calor
    satisfaction_matrix = df.pivot_table(
        values='Satisfação',
        index='Província',
        columns='Nome_Mês',
        aggfunc='mean'
    )
    
    # Reordenar colunas por mês
    months_order = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    satisfaction_matrix = satisfaction_matrix.reindex(columns=months_order)
    
    fig_heatmap = px.imshow(
        satisfaction_matrix,
        title="Satisfação dos Turistas (1-5)",
        color_continuous_scale=['#FF6B35', '#F7931E', '#FFD700'],
        aspect='auto'
    )
    fig_heatmap.update_layout(height=500)
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Tabela de dados detalhados
    st.subheader("📋 Dados Detalhados por Província")
    
    # Criar resumo por província
    province_summary = df.groupby('Província').agg({
        'Visitantes': 'sum',
        'Receita_AOA': 'sum',
        'Satisfação': 'mean'
    }).round(2)
    
    province_summary['Receita_Formatada'] = province_summary['Receita_AOA'].apply(format_aoa)
    province_summary = province_summary.sort_values('Visitantes', ascending=False)
    
    # Mostrar tabela formatada
    st.dataframe(
        province_summary[['Visitantes', 'Receita_Formatada', 'Satisfação']].rename(columns={
            'Visitantes': 'Total Visitantes',
            'Receita_Formatada': 'Receita Total (AOA)',
            'Satisfação': 'Satisfação Média'
        }),
        use_container_width=True
    )
    
    # Insights e recomendações
    st.subheader("💡 Insights Automáticos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top província
        top_province = province_summary.index[0]
        top_visitors = province_summary.iloc[0]['Visitantes']
        
        st.info(f"""
        🏆 **Melhor Desempenho:**
        
        **{top_province}** lidera com **{top_visitors:,} visitantes**
        
        Esta província representa {(top_visitors/total_visitors)*100:.1f}% do turismo total.
        """)
    
    with col2:
        # Melhor satisfação
        best_satisfaction_province = province_summary.loc[province_summary['Satisfação'].idxmax()]
        
        st.success(f"""
        ⭐ **Maior Satisfação:**
        
        **{best_satisfaction_province.name}** com **{best_satisfaction_province['Satisfação']:.2f}/5.0**
        
        Excelente qualidade de experiência turística.
        """)
    
    # Rodapé
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>🌍 <strong>NOMADIX</strong> - Sistema de Análise Turística para Angola</p>
        <p>Desenvolvido para otimizar o planejamento estratégico do setor turístico</p>
        <p style='font-size: 0.8rem;'>© 2025 - Todos os direitos reservados</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()