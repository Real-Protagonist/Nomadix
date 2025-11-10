import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import hashlib
import io

# ==================== SISTEMA DE AUTENTICAÇÃO ====================

def hash_password(password):
    """Gera hash da senha para segurança"""
    return hashlib.sha256(str.encode(password)).hexdigest()

def init_user_system():
    """Inicializa sistema de usuários se não existir"""
    if 'users_db' not in st.session_state:
        st.session_state.users_db = {
            'admin_gov': {
                'password': hash_password('gov2024'),
                'name': 'Ministério do Turismo',
                'level': 'GOVERNO',
                'permissions': ['full_access', 'admin', 'export', 'alerts', 'chat']
            },
            'ong_user': {
                'password': hash_password('ong2024'),
                'name': 'ONG Desenvolvimento',
                'level': 'ONG', 
                'permissions': ['social_data', 'export', 'chat', 'alerts']
            },
            'community_rep': {
                'password': hash_password('comm2024'),
                'name': 'Representante Comunitário',
                'level': 'COMUNIDADE',
                'permissions': ['local_data', 'basic_export', 'chat']
            },
            'public_user': {
                'password': hash_password('public2024'),
                'name': 'Público Geral',
                'level': 'PÚBLICO',
                'permissions': ['view_only', 'basic_chat']
            }
        }
    
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None

def authenticate_user(username, password):
    """Autentica usuário"""
    users_db = st.session_state.users_db
    if username in users_db:
        if users_db[username]['password'] == hash_password(password):
            st.session_state.current_user = {
                'username': username,
                'name': users_db[username]['name'],
                'level': users_db[username]['level'],
                'permissions': users_db[username]['permissions']
            }
            return True
    return False

def check_permission(required_permission):
    """Verifica permissão"""
    if st.session_state.current_user is None:
        return False
    return required_permission in st.session_state.current_user['permissions']

def get_access_level_color(level):
    """Cor baseada no nível"""
    colors = {
        'GOVERNO': '#FF6B35',
        'ONG': '#4ECDC4',
        'COMUNIDADE': '#45B7D1',
        'PÚBLICO': '#96CEB4'
    }
    return colors.get(level, '#666666')

def login_interface():
    """Interface de login"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #002B5C 0%, #19486A 100%); padding: 2rem; border-radius: 20px; text-align: center; margin: 2rem 0;">
        <h1 style="color: white; margin-bottom: 0.5rem;">🔐 ACESSO NOMADIX</h1>
        <p style="color: #bba55b; font-size: 1.2rem;">Sistema de Monitoramento Turístico de Angola</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("### 👤 Credenciais de Acesso")
            
            username = st.selectbox(
                "Selecione seu Tipo de Usuário:",
                options=['', 'admin_gov', 'ong_user', 'community_rep', 'public_user'],
                format_func=lambda x: {
                    '': 'Selecione...',
                    'admin_gov': '🏛️ Governo - Acesso Total',
                    'ong_user': '🤝 ONG - Dados Sociais', 
                    'community_rep': '🏘️ Comunidade - Dados Locais',
                    'public_user': '👥 Público - Visualização Básica'
                }.get(x, x)
            )
            
            password = st.text_input("Senha:", type="password")
            login_button = st.form_submit_button("🚀 ENTRAR", use_container_width=True)
            
            st.markdown("""
            ---
            **🔑 Credenciais Demo:**
            - **Governo**: `gov2024`
            - **ONG**: `ong2024` 
            - **Comunidade**: `comm2024`
            - **Público**: `public2024`
            """)
    
    if login_button:
        if username and password:
            if authenticate_user(username, password):
                st.success(f"✅ Login realizado! Bem-vindo, {st.session_state.current_user['name']}")
                st.rerun()
            else:
                st.error("❌ Credenciais inválidas!")
        else:
            st.warning("⚠️ Por favor, preencha todos os campos!")

def user_header():
    """Header do usuário logado"""
    if st.session_state.current_user:
        user = st.session_state.current_user
        level_color = get_access_level_color(user['level'])
        
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {level_color} 0%, #002B5C 100%); padding: 1rem; border-radius: 12px; color: white;">
                <div style="display: flex; align-items: center;">
                    <div style="font-size: 1.5rem; margin-right: 1rem;">👤</div>
                    <div>
                        <div style="font-weight: bold; font-size: 1.1rem;">{user['name']}</div>
                        <div style="font-size: 0.9rem; opacity: 0.8;">Nível: {user['level']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            permissions_count = len(user['permissions'])
            st.markdown(f"""
            <div style="background: #bba55b; padding: 1rem; border-radius: 12px; color: white; text-align: center;">
                <div style="font-size: 1.5rem; font-weight: bold;">{permissions_count}</div>
                <div style="font-size: 0.8rem;">Permissões</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.current_user = None
                st.rerun()

# ==================== DADOS ====================

def generate_sample_data():
    """Gera dados de exemplo"""
    provinces = [
        "Luanda", "Benguela", "Huíla", "Huambo", "Cabinda", "Cunene", 
        "Namibe", "Cuando Cubango", "Malanje", "Bié", "Cuanza Norte",
        "Cuanza Sul", "Lunda Norte", "Lunda Sul", "Bengo", "Moxico", "Uíge", "Zaire"
    ]
    
    tourist_data = []
    for province in provinces:
        for month in range(1, 13):
            tourists = random.randint(1000, 8000)
            revenue_usd = random.randint(50000, 400000)
            revenue_aoa = revenue_usd * 825
            satisfaction = random.uniform(3.5, 5.0)
            
            tourist_data.append({
                'Província': province,
                'Mês': month,
                'Visitantes': tourists,
                'Receita_USD': revenue_usd,
                'Receita_AOA': revenue_aoa,
                'Satisfação': satisfaction
            })
    
    return pd.DataFrame(tourist_data)

def format_aoa(value):
    """Formatar valores em AOA"""
    if value >= 1e9:
        return f"{value/1e9:.1f}B AOA"
    elif value >= 1e6:
        return f"{value/1e6:.1f}M AOA"
    elif value >= 1e3:
        return f"{value/1e3:.1f}K AOA"
    else:
        return f"{value:.0f} AOA"

# ==================== EXPORTAÇÃO ====================

def export_dashboard_pdf():
    """Exporta relatório em PDF"""
    try:
        st.success("📄 Preparando relatório...")
        
        pdf_content = f"""RELATÓRIO NOMADIX - ANGOLA
        
Data: {datetime.now().strftime('%d/%m/%Y às %H:%M')}
Usuário: {st.session_state.current_user['name']}
Nível: {st.session_state.current_user['level']}

RESUMO EXECUTIVO:
✅ Sistema de monitoramento integrado
✅ Dados em tempo real de 18 províncias
✅ Análise de sustentabilidade (ODSs)
✅ Inteligência artificial aplicada

© 2025 NOMADIX - Todos os direitos reservados
"""
        
        st.download_button(
            label="📥 Baixar Relatório",
            data=pdf_content,
            file_name=f"nomadix_relatorio_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain"
        )
        
    except Exception as e:
        st.error(f"❌ Erro: {str(e)}")

def export_data_csv(df):
    """Exporta dados CSV"""
    try:
        user_level = st.session_state.current_user['level']
        
        if user_level == 'PÚBLICO':
            export_df = df[['Província', 'Mês', 'Visitantes']].copy()
        elif user_level == 'COMUNIDADE':
            export_df = df[['Província', 'Mês', 'Visitantes', 'Satisfação']].copy()
        elif user_level == 'ONG':
            export_df = df[['Província', 'Mês', 'Visitantes', 'Satisfação', 'Receita_AOA']].copy()
        else:
            export_df = df.copy()
        
        csv_data = export_df.to_csv(index=False, encoding='utf-8')
        
        st.download_button(
            label="📥 Baixar CSV",
            data=csv_data,
            file_name=f"nomadix_dados_{user_level.lower()}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )
        
        st.success(f"✅ CSV preparado com {len(export_df)} registros!")
        
    except Exception as e:
        st.error(f"❌ Erro: {str(e)}")

# ==================== CHATBOT IA ====================

def render_chat_interface():
    """Interface do chatbot"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #bba55b 0%, #002B5C 100%); padding: 2rem; border-radius: 15px; margin: 1rem 0; text-align: center;">
        <h2 style="color: white; margin: 0;">💬 ASSISTENTE IA NOMADIX</h2>
        <p style="color: white; margin: 0.5rem 0 0 0;">Inteligência Artificial para Dados Turísticos</p>
    </div>
    """, unsafe_allow_html=True)
    
    user_level = st.session_state.current_user['level']
    suggestions = {
        'GOVERNO': [
            "Qual o ROI das campanhas turísticas?",
            "Como está o progresso das ODSs?",
            "Quais províncias precisam investimento?"
        ],
        'ONG': [
            "Impacto social do turismo?", 
            "Indicadores sociais atuais?",
            "Projetos de turismo sustentável?"
        ],
        'COMUNIDADE': [
            "Turismo na minha região?",
            "Oportunidades de emprego?",
            "Como participar do turismo local?"
        ],
        'PÚBLICO': [
            "Destinos mais populares?",
            "Melhor época para visitar?",
            "Satisfação dos turistas?"
        ]
    }
    
    user_suggestions = suggestions.get(user_level, suggestions['PÚBLICO'])
    
    st.markdown("**💡 Perguntas Sugeridas:**")
    for suggestion in user_suggestions:
        if st.button(f"❓ {suggestion}"):
            simulate_ai_response(suggestion)
    
    st.markdown("---")
    user_input = st.text_input("💬 Digite sua pergunta:")
    
    if st.button("📤 Enviar") and user_input:
        simulate_ai_response(user_input)

def simulate_ai_response(question):
    """Simula resposta do assistente IA"""
    responses = {
        'roi': "📊 ROI médio das campanhas: 312%. Luanda lidera com 425%.",
        'ods': "🎯 ODS 8: 78%, ODS 14: 65%. Recomendo foco no ODS 14.",
        'investimento': "💰 Cunene, Cuando Cubango e Moxico precisam de investimento prioritário.",
        'destinos': "🏆 Top 3: Luanda (32%), Benguela (18%), Huíla (12%).",
        'emprego': "💼 45.230 empregos gerados, crescimento de 23% na renda local.",
        'satisfacao': "😊 Satisfação média: 4.2/5.0, com crescimento de 0.3 pontos."
    }
    
    response = "🤖 Analisando dados disponíveis..."
    
    for key, value in responses.items():
        if key in question.lower():
            response = value
            break
    
    st.success(f"🤖 **Assistente NOMADIX**: {response}")
    st.info("💡 Posso gerar relatórios específicos ou análises complementares!")

# ==================== ALERTAS ====================

def render_alerts():
    """Sistema de alertas"""
    st.subheader("🚨 Alertas do Sistema")
    
    alerts = [
        {'type': 'critical', 'message': 'ODS 14 abaixo de 70% da meta'},
        {'type': 'warning', 'message': 'Queda de turismo em Benguela (-5%)'}, 
        {'type': 'info', 'message': 'Nova campanha promocional ativa'},
        {'type': 'success', 'message': 'Meta de Luanda superada em 15%'}
    ]
    
    for alert in alerts:
        if alert['type'] == 'critical':
            st.error(f"🚨 **CRÍTICO**: {alert['message']}")
        elif alert['type'] == 'warning':
            st.warning(f"⚠️ **ATENÇÃO**: {alert['message']}")
        elif alert['type'] == 'success':
            st.success(f"✅ **SUCESSO**: {alert['message']}")
        else:
            st.info(f"ℹ️ **INFO**: {alert['message']}")

# ==================== DASHBOARD PRINCIPAL ====================

def render_dashboard_content(df):
    """Renderiza dashboard baseado no nível de acesso"""
    user = st.session_state.current_user
    
    # Sidebar com funcionalidades
    with st.sidebar:
        render_sidebar(df)
    
    # Header principal
    st.markdown("""
    <div style="background: linear-gradient(135deg, #002B5C 0%, #003d7a 100%); padding: 1.5rem; border-radius: 15px; text-align: center; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0;">🌍 NOMADIX DASHBOARD</h1>
        <p style="color: #bba55b; margin: 0.5rem 0 0 0;">Sistema Interativo de Turismo - Angola</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Menu de navegação
    menu_options = get_menu_options(user['level'])
    selected = st.selectbox("📋 Selecione a Seção:", menu_options)
    
    # Renderizar conteúdo baseado na seleção
    if selected == "📊 Dashboard Geral":
        render_main_dashboard(df)
    elif selected == "💬 Assistente IA":
        render_chat_interface()
    elif selected == "🚨 Alertas":
        render_alerts()
    elif selected == "👥 Admin":
        render_admin_panel()
    else:
        render_main_dashboard(df)

def get_menu_options(level):
    """Opções de menu baseadas no nível"""
    base_options = ["📊 Dashboard Geral", "💬 Assistente IA"]
    
    if level == 'GOVERNO':
        return base_options + ["🚨 Alertas", "👥 Admin", "📈 Analytics Avançadas"]
    elif level == 'ONG':
        return base_options + ["🚨 Alertas", "🤝 Dados Sociais"]
    elif level == 'COMUNIDADE':
        return base_options + ["🏘️ Dados Locais"]
    else:  # PÚBLICO
        return ["📊 Visão Pública", "💬 Assistente Básico"]

def render_sidebar(df):
    """Sidebar com funcionalidades"""
    user = st.session_state.current_user
    
    st.markdown(f"### 👤 {user['name']}")
    st.markdown(f"**Nível**: {user['level']}")
    
    # Permissões do usuário
    st.markdown("---")
    st.markdown("**🔐 Suas Permissões:**")
    for perm in user['permissions']:
        if perm == 'full_access':
            st.success("🔓 Acesso Total")
        elif perm == 'export':
            st.success("📤 Exportação")
        elif perm == 'chat':
            st.success("💬 Assistente IA")
        elif perm == 'alerts':
            st.success("🚨 Alertas")
        elif perm == 'admin':
            st.success("👑 Administrador")
    
    # Exportação (se permitida)
    if check_permission('export'):
        st.markdown("---")
        st.markdown("**📤 Exportação:**")
        if st.button("📄 Relatório PDF", use_container_width=True):
            export_dashboard_pdf()
        if st.button("📊 Dados CSV", use_container_width=True):
            export_data_csv(df)
    
    # Estatísticas rápidas
    st.markdown("---")
    st.markdown("**📈 Stats Rápidas:**")
    st.metric("Visitantes", f"{df['Visitantes'].sum():,}")
    st.metric("Satisfação", f"{df['Satisfação'].mean():.1f}/5")
    st.metric("Receita", format_aoa(df['Receita_AOA'].sum()))

def render_main_dashboard(df):
    """Dashboard principal com métricas"""
    user = st.session_state.current_user
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_visitors = df['Visitantes'].sum()
        st.metric("🌍 Total Visitantes", f"{total_visitors:,}", delta="12.5%")
    
    with col2:
        total_revenue = df['Receita_AOA'].sum()
        st.metric("💰 Receita Total", format_aoa(total_revenue), delta="8.3%")
    
    with col3:
        avg_satisfaction = df['Satisfação'].mean()
        st.metric("😊 Satisfação", f"{avg_satisfaction:.1f}/5.0", delta="0.2")
    
    with col4:
        if user['level'] == 'GOVERNO':
            growth_rate = 15.3
            st.metric("📈 Crescimento", f"{growth_rate}%", delta="2.1%")
        else:
            st.metric("🏛️ Províncias", "18", delta="0")
    
    # Gráficos
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Visitantes por Província")
        province_data = df.groupby('Província')['Visitantes'].sum().sort_values(ascending=False).head(10)
        
        fig_provinces = px.bar(
            x=province_data.values,
            y=province_data.index,
            orientation='h',
            title="Top 10 Províncias",
            color_discrete_sequence=['#002B5C']
        )
        fig_provinces.update_layout(height=400)
        st.plotly_chart(fig_provinces, use_container_width=True)
    
    with col2:
        st.subheader("📈 Tendência Mensal")
        monthly_data = df.groupby('Mês')['Visitantes'].sum()
        
        fig_monthly = px.line(
            x=monthly_data.index,
            y=monthly_data.values,
            title="Visitantes por Mês - 2024",
            markers=True,
            color_discrete_sequence=['#bba55b']
        )
        fig_monthly.update_layout(height=400)
        st.plotly_chart(fig_monthly, use_container_width=True)

def render_admin_panel():
    """Painel administrativo"""
    if not check_permission('admin'):
        st.error("❌ Acesso negado. Funcionalidade restrita ao governo.")
        return
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #96CEB4 0%, #002B5C 100%); padding: 2rem; border-radius: 15px; margin: 1rem 0; text-align: center;">
        <h2 style="color: white; margin: 0;">👥 ADMINISTRAÇÃO</h2>
        <p style="color: white; margin: 0.5rem 0 0 0;">Gestão de Usuários e Sistema</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Estatísticas de usuários
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Usuários", "1,247", delta="12")
    with col2:
        st.metric("Usuários Ativos", "892", delta="8")
    with col3:
        st.metric("Sessões Hoje", "156", delta="23")
    with col4:
        st.metric("Tempo Médio", "25min", delta="2min")
    
    # Gestão simulada
    st.subheader("👤 Usuários Ativos")
    
    users_data = {
        'Usuário': ['admin@gov.ao', 'ong@social.ao', 'community@local.ao', 'public@guest.ao'],
        'Nível': ['GOVERNO', 'ONG', 'COMUNIDADE', 'PÚBLICO'],
        'Último Acesso': ['Hoje 14:30', 'Ontem 16:45', 'Hoje 09:15', 'Hoje 11:20'],
        'Status': ['🟢 Ativo', '🟢 Ativo', '🟡 Ausente', '🟢 Ativo']
    }
    
    users_df = pd.DataFrame(users_data)
    st.dataframe(users_df, use_container_width=True)
    
    # Ações
    st.subheader("⚙️ Ações Administrativas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Adicionar Usuário", use_container_width=True):
            st.success("✅ Função de criação de usuário!")
    
    with col2:
        if st.button("🔄 Logs do Sistema", use_container_width=True):
            st.info("📋 Carregando logs de atividade...")
    
    with col3:
        if st.button("⚙️ Configurações", use_container_width=True):
            st.success("🔧 Painel de configurações!")

# ==================== FUNÇÃO PRINCIPAL ====================

def main():
    st.set_page_config(
        page_title="NOMADIX Interativo - Angola",
        page_icon="🌍",
        layout="wide"
    )
    
    # Inicializar sistema
    init_user_system()
    
    # Verificar login
    if st.session_state.current_user is None:
        login_interface()
        return
    
    # Header do usuário
    user_header()
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Carregar dados
    if 'tourist_data' not in st.session_state:
        with st.spinner('🔄 Carregando dados turísticos de Angola...'):
            st.session_state.tourist_data = generate_sample_data()
    
    df = st.session_state.tourist_data
    
    # Renderizar dashboard
    render_dashboard_content(df)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>🌍 <strong>NOMADIX INTERATIVO</strong> - Sistema Avançado de Turismo para Angola</p>
        <p>🔐 Sistema de Login Multinível | 📤 Exportação Inteligente | 🤖 IA Integrada | 🚨 Alertas Automáticos</p>
        <p style='font-size: 0.8rem;'>© 2025 - Todos os direitos reservados</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()