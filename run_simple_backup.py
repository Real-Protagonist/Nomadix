import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import hashlib
import base64
import io
import json

# ==================== SISTEMA DE AUTENTICAÇÃO ====================

def hash_password(password):
    """Gera hash da senha para segurança"""
    return hashlib.sha256(str.encode(password)).hexdigest()

def init_user_system():
    """Inicializa sistema de usuários se não existir"""
    if 'users_db' not in st.session_state:
        # Base de usuários pré-definidos (em produção seria um banco de dados)
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
    
    if 'user_permissions' not in st.session_state:
        st.session_state.user_permissions = []

def authenticate_user(username, password):
    """Autentica usuário e define permissões"""
    users_db = st.session_state.users_db
    
    if username in users_db:
        if users_db[username]['password'] == hash_password(password):
            st.session_state.current_user = {
                'username': username,
                'name': users_db[username]['name'],
                'level': users_db[username]['level'],
                'permissions': users_db[username]['permissions']
            }
            st.session_state.user_permissions = users_db[username]['permissions']
            return True
    return False

def check_permission(required_permission):
    """Verifica se o usuário tem permissão específica"""
    if st.session_state.current_user is None:
        return False
    return required_permission in st.session_state.user_permissions

def get_access_level_color(level):
    """Retorna cor baseada no nível de acesso"""
    colors = {
        'GOVERNO': '#FF6B35',      # Laranja (máximo acesso)
        'ONG': '#4ECDC4',          # Teal (acesso social)
        'COMUNIDADE': '#45B7D1',   # Azul claro (acesso local)
        'PÚBLICO': '#96CEB4'       # Verde claro (acesso básico)
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
    
    # Formulário de login
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
            
            # Informações de demo
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
    """Header com informações do usuário logado"""
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
                st.session_state.user_permissions = []
                st.rerun()

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

def generate_advanced_kpis():
    """Gera KPIs avançados para o painel geral"""
    return {
        'total_visitors': random.randint(850000, 1200000),
        'monthly_variation': random.uniform(-5.2, 15.8),
        'total_revenue_aoa': random.randint(400000000000, 800000000000),  # Bilhões AOA
        'revenue_per_capita': random.randint(180000, 350000),  # AOA per capita
        'sustainability_index': random.uniform(6.2, 8.9),  # Índice 0-10
        'hotel_occupancy': random.uniform(65.5, 85.2),  # Percentual
        'jobs_created': random.randint(45000, 78000),  # Empregos
        'environmental_pressure': random.uniform(3.2, 7.8),  # Índice 0-10
        'investment_potential': random.uniform(7.1, 9.4)  # Índice 0-10
    }

def generate_tourism_flows():
    """Gera dados de fluxos turísticos por província"""
    provinces = [
        "Luanda", "Benguela", "Huíla", "Huambo", "Cabinda", "Cunene", 
        "Namibe", "Cuando Cubango", "Malanje", "Bié", "Cuanza Norte",
        "Cuanza Sul", "Lunda Norte", "Lunda Sul", "Bengo", "Moxico", "Uíge", "Zaire"
    ]
    
    flows_data = []
    for province in provinces:
        flows_data.append({
            'Província': province,
            'Fluxo_Turístico': random.randint(5000, 45000),
            'Pressão_Ambiental': random.uniform(1.0, 10.0),
            'Potencial_Investimento': random.uniform(1.0, 10.0),
            'Lat': random.uniform(-18.0, -4.0),  # Coordenadas aproximadas de Angola
            'Lon': random.uniform(11.0, 24.0)
        })
    
    return pd.DataFrame(flows_data)

def generate_tourist_origins():
    """Gera dados de origem dos turistas"""
    return {
        'Brasil': 28.5,
        'Portugal': 22.3,
        'África do Sul': 18.7,
        'França': 12.1,
        'Alemanha': 8.2,
        'Reino Unido': 5.8,
        'Outros': 4.4
    }

def generate_sdg_data():
    """Gera dados dos ODSs relacionados ao turismo"""
    return {
        'ods_1': {  # Erradicação da Pobreza
            'nome': 'ODS 1 - Erradicação da Pobreza',
            'meta_atual': random.uniform(68.5, 85.2),
            'meta_2030': 90.0,
            'indicadores': {
                'Empregos turísticos criados': random.randint(45000, 78000),
                'Renda média familiar (AOA)': random.randint(180000, 350000),
                'Redução da pobreza extrema (%)': random.uniform(15.2, 28.7)
            },
            'cor': '#E5243B'
        },
        'ods_5': {  # Igualdade de Gênero
            'nome': 'ODS 5 - Igualdade de Gênero',
            'meta_atual': random.uniform(72.3, 88.9),
            'meta_2030': 85.0,
            'indicadores': {
                'Mulheres em cargos de liderança (%)': random.uniform(35.2, 48.6),
                'Empresárias no turismo (%)': random.uniform(42.8, 56.3),
                'Igualdade salarial atingida (%)': random.uniform(78.1, 89.4)
            },
            'cor': '#FF3A21'
        },
        'ods_8': {  # Trabalho Decente e Crescimento Econômico
            'nome': 'ODS 8 - Trabalho Decente',
            'meta_atual': random.uniform(79.4, 92.1),
            'meta_2030': 88.0,
            'indicadores': {
                'PIB turístico (Bilhões AOA)': random.uniform(580, 920),
                'Produtividade do trabalho': random.uniform(85.3, 96.7),
                'Trabalho informal reduzido (%)': random.uniform(25.8, 39.2)
            },
            'cor': '#A21942'
        },
        'ods_11': {  # Cidades e Comunidades Sustentáveis
            'nome': 'ODS 11 - Cidades Sustentáveis',
            'meta_atual': random.uniform(71.8, 86.4),
            'meta_2030': 82.0,
            'indicadores': {
                'Infraestrutura turística sustentável (%)': random.uniform(68.2, 81.7),
                'Transporte público melhorado (%)': random.uniform(54.3, 72.9),
                'Gestão de resíduos eficiente (%)': random.uniform(61.8, 78.5)
            },
            'cor': '#FD6925'
        },
        'ods_12': {  # Consumo e Produção Responsáveis
            'nome': 'ODS 12 - Produção Responsável',
            'meta_atual': random.uniform(64.7, 79.3),
            'meta_2030': 75.0,
            'indicadores': {
                'Turismo de baixo carbono (%)': random.uniform(58.4, 73.2),
                'Desperdício reduzido (%)': random.uniform(67.1, 82.8),
                'Certificações sustentáveis': random.randint(128, 245)
            },
            'cor': '#BF8B2E'
        },
        'ods_14': {  # Vida na Água
            'nome': 'ODS 14 - Vida na Água',
            'meta_atual': random.uniform(69.5, 84.1),
            'meta_2030': 78.0,
            'indicadores': {
                'Áreas marinhas protegidas (%)': random.uniform(42.7, 58.9),
                'Qualidade da água costeira': random.uniform(76.3, 91.2),
                'Turismo marinho sustentável (%)': random.uniform(63.8, 79.4)
            },
            'cor': '#14A085'
        },
        'ods_15': {  # Vida Terrestre
            'nome': 'ODS 15 - Vida Terrestre',
            'meta_atual': random.uniform(73.2, 87.6),
            'meta_2030': 80.0,
            'indicadores': {
                'Áreas protegidas (% território)': random.uniform(18.4, 26.7),
                'Biodiversidade conservada (%)': random.uniform(71.8, 86.3),
                'Ecoturismo desenvolvido (%)': random.uniform(55.2, 74.9)
            },
            'cor': '#56C02B'
        },
        'ods_17': {  # Parcerias para as Metas
            'nome': 'ODS 17 - Parcerias Globais',
            'meta_atual': random.uniform(76.8, 91.4),
            'meta_2030': 85.0,
            'indicadores': {
                'Parcerias internacionais ativas': random.randint(23, 47),
                'Investimento estrangeiro (Milhões USD)': random.uniform(150, 380),
                'Cooperação técnica (projetos)': random.randint(15, 32)
            },
            'cor': '#19486A'
        }
    }

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
    
    # Inicializar sistema de usuários
    init_user_system()
    
    # Verificar se usuário está logado
    if st.session_state.current_user is None:
        login_interface()
        return
    
    # Header do usuário logado
    user_header()
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Verificar se os dados estão no cache
    if 'tourist_data' not in st.session_state:
        with st.spinner('Carregando dados turísticos de Angola...'):
            st.session_state.tourist_data = generate_sample_data()
    
    df = st.session_state.tourist_data
    
    # Verificar se o DataFrame está vazio
    if df.empty:
        st.error("❌ Erro ao carregar os dados. Tente recarregar a página.")
        return
    
    # Definir saudação baseada na hora atual
    current_hour = datetime.now().hour
    greeting = "🌅 Bom dia" if current_hour < 12 else "☀️ Boa tarde" if current_hour < 18 else "🌙 Boa noite"
    
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
            background: linear-gradient(135deg, #002B5C 0%, #003d7a 100%);
            border: 2px solid #bba55b;
        }
        .metric-card-revenue {
            background: linear-gradient(135deg, #1a4c7a 0%, #2563eb 100%);
            border: 2px solid #bba55b;
        }
        .metric-card-satisfaction {
            background: linear-gradient(135deg, #0f3460 0%, #1e5a8a 100%);
            border: 2px solid #bba55b;
        }
        .metric-card-growth {
            background: linear-gradient(135deg, #bba55b 0%, #d4c875 100%);
            border: 2px solid #002B5C;
            color: #002B5C;
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
        
        /* Menu horizontal superior */
        .top-menu-container {
            background: linear-gradient(135deg, #002B5C 0%, #003d7a 100%);
            padding: 0.75rem 2rem;
            box-shadow: 0 2px 10px rgba(0, 43, 92, 0.3);
            border-bottom: 3px solid #bba55b;
            margin-bottom: 1.5rem;
        }
        
        .top-menu {
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .menu-left {
            display: flex;
            align-items: center;
            gap: 2rem;
        }
        
        .menu-right {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .menu-item {
            background: transparent;
            border: 2px solid #bba55b;
            border-radius: 25px;
            padding: 0.5rem 1.5rem;
            color: white;
            text-decoration: none;
            font-weight: 500;
            font-size: 14px;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .menu-item:hover {
            background: #bba55b;
            color: #002B5C;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(187, 165, 91, 0.3);
        }
        
        .profile-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: linear-gradient(135deg, #002B5C 0%, #bba55b 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 16px;
            margin-right: 0.5rem;
            border: 2px solid #bba55b;
        }
        
        .profile-info {
            color: white;
            font-size: 14px;
            font-weight: 500;
            margin-right: 1rem;
        }
        
        .system-status {
            color: #bba55b;
            font-size: 12px;
            font-weight: 500;
        }
        
        .brand-title {
            color: white;
            font-size: 24px;
            font-weight: bold;
            margin: 0;
        }
        
        .brand-subtitle {
            color: #bba55b;
            font-size: 12px;
            margin: 0;
        }
        
        .user-profile:hover .dropdown-arrow {
            transform: rotate(180deg);
        }
        
        /* Dropdown Menu */
        .profile-dropdown {
            position: absolute;
            top: 100%;
            right: 0;
            margin-top: 0.5rem;
            background: white;
            border-radius: 10px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
            min-width: 220px;
            padding: 0;
            display: none;
            z-index: 1001;
            border: 1px solid rgba(255, 107, 53, 0.2);
            overflow: hidden;
            animation: slideDown 0.3s ease-out;
        }
        
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .user-profile-container:hover .profile-dropdown {
            display: block;
        }
        
        .dropdown-header {
            padding: 1rem;
            text-align: center;
            background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
            color: white;
            border-radius: 10px 10px 0 0;
        }
        
        .dropdown-header-title {
            font-weight: bold;
            font-size: 16px;
        }
        
        .dropdown-header-email {
            font-size: 12px;
            opacity: 0.9;
            margin-top: 0.25rem;
        }
        
        .dropdown-header-time {
            font-size: 11px;
            opacity: 0.8;
            margin-top: 0.25rem;
        }
        
        .dropdown-item {
            padding: 0.75rem 1rem;
            color: #333;
            text-decoration: none;
            display: flex;
            align-items: center;
            transition: all 0.2s ease;
            cursor: pointer;
            border: none;
            background: none;
            width: 100%;
            font-size: 14px;
        }
        
        .dropdown-item:hover {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            color: #FF6B35;
            transform: translateX(5px);
        }
        
        .dropdown-icon {
            margin-right: 0.75rem;
            font-size: 16px;
            width: 16px;
        }
        
        .dropdown-divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, #e0e0e0, transparent);
            margin: 0.5rem 0;
        }
        
        .dropdown-item-danger {
            color: #dc3545;
        }
        
        .dropdown-item-danger:hover {
            background: linear-gradient(135deg, #f8d7da 0%, #f1aeb5 100%);
            color: #721c24;
        }
        
        /* Responsividade para mobile */
        @media (max-width: 768px) {
            .user-profile-container {
                position: relative;
                top: auto;
                right: auto;
                margin-bottom: 1rem;
            }
            
            .profile-dropdown {
                position: relative;
                margin-top: 0.5rem;
                right: auto;
                left: 0;
                width: 100%;
            }
        }
        </style>
        
        <script>
        // Adicionar interatividade ao dropdown
        document.addEventListener('DOMContentLoaded', function() {
            // Função para mostrar notificações
            function showNotification(message, type = 'info') {
                // Simular uma notificação
                const notification = document.createElement('div');
                notification.style.cssText = `
                    position: fixed;
                    top: 70px;
                    right: 20px;
                    background: ${type === 'success' ? '#d4edda' : type === 'warning' ? '#fff3cd' : '#d1ecf1'};
                    color: ${type === 'success' ? '#155724' : type === 'warning' ? '#856404' : '#0c5460'};
                    padding: 12px 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                    z-index: 10000;
                    font-size: 14px;
                    min-width: 250px;
                    animation: slideInRight 0.3s ease-out;
                `;
                notification.textContent = message;
                document.body.appendChild(notification);
                
                setTimeout(() => {
                    notification.style.animation = 'slideOutRight 0.3s ease-in';
                    setTimeout(() => {
                        if (notification.parentNode) {
                            notification.parentNode.removeChild(notification);
                        }
                    }, 300);
                }, 3000);
            }
            
            // Adicionar event listeners aos itens do dropdown
            const dropdownItems = document.querySelectorAll('.dropdown-item');
            
            dropdownItems.forEach(item => {
                item.addEventListener('click', function(e) {
                    e.preventDefault();
                    const text = this.textContent.trim();
                    
                    switch(text) {
                        case 'Meu Perfil':
                            showNotification('👤 Abrindo perfil do usuário...', 'info');
                            break;
                        case 'Relatórios Avançados':
                            showNotification('📊 Carregando relatórios avançados...', 'info');
                            break;
                        case 'Analytics & Insights':
                            showNotification('📈 Abrindo analytics e insights...', 'info');
                            break;
                        case 'Configurações':
                            showNotification('⚙️ Abrindo configurações do sistema...', 'info');
                            break;
                        case 'Notificações':
                            showNotification('🔔 Central de notificações ativada!', 'success');
                            break;
                        case 'Modo Escuro':
                            showNotification('🌙 Modo escuro será implementado em breve!', 'warning');
                            break;
                        case 'Idioma: Português':
                            showNotification('🌍 Configurações de idioma disponíveis!', 'info');
                            break;
                        case 'Suporte & Ajuda':
                            showNotification('💬 Conectando com suporte técnico...', 'info');
                            break;
                        case 'Documentação':
                            showNotification('📋 Abrindo documentação completa...', 'info');
                            break;
                        case 'Sair do Sistema':
                            if (confirm('🚪 Tem certeza que deseja sair do sistema?')) {
                                showNotification('👋 Logout realizado com sucesso!', 'success');
                                setTimeout(() => {
                                    showNotification('🔒 Redirecionando para login...', 'info');
                                }, 1500);
                            }
                            break;
                    }
                });
            });
        });
        
        // CSS para animações das notificações
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideInRight {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            
            @keyframes slideOutRight {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(100%);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
        </script>
    """, unsafe_allow_html=True)
    
    # Menu horizontal superior
    # Header com título principal (versão simplificada)
    st.markdown("""
    <div style="background: linear-gradient(135deg, #002B5C 0%, #003d7a 100%); padding: 1.5rem; margin: -1rem -1rem 2rem -1rem; border-bottom: 3px solid #bba55b; text-align: center;">
        <h1 style="color: white; margin: 0; font-size: 2.5rem;">🌍 NOMADIX</h1>
        <p style="color: #bba55b; margin: 0.5rem 0 0 0; font-size: 1.2rem;">Dashboard Turístico - Angola</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Menu horizontal baseado em permissões
    user = st.session_state.current_user
    level_color = get_access_level_color(user['level'])
    
    # Definir opções de menu baseadas no nível de acesso
    menu_options = {
        'GOVERNO': [
            ("📊 Dashboard Geral", "dashboard"),
            ("🏛️ Painel Governamental", "gov_panel"), 
            ("📈 Analytics Avançadas", "analytics"),
            ("📋 Relatórios Executivos", "reports"),
            ("👥 Gestão Usuários", "admin"),
            ("⚙️ Configurações", "config")
        ],
        'ONG': [
            ("📊 Dashboard", "dashboard"),
            ("🤝 Dados Sociais", "social_data"),
            ("🎯 ODSs", "sdgs"),
            ("📋 Relatórios ONG", "ngo_reports"),
            ("💬 Suporte", "support")
        ],
        'COMUNIDADE': [
            ("📊 Dashboard", "dashboard"), 
            ("🏘️ Dados Locais", "local_data"),
            ("📈 Tendências Locais", "local_trends"),
            ("💬 Chat Comunitário", "community_chat")
        ],
        'PÚBLICO': [
            ("📊 Visão Geral", "overview"),
            ("📈 Estatísticas Básicas", "basic_stats"),
            ("💬 Assistente", "chat")
        ]
    }
    
    current_options = menu_options.get(user['level'], menu_options['PÚBLICO'])
    cols = st.columns([2] + [1.2] * len(current_options) + [1])
    
    with cols[0]:
        st.markdown(f"""
        <div style="background: {level_color}; padding: 0.7rem; border-radius: 15px; text-align: center; border: 2px solid #002B5C; margin-bottom: 1rem;">
            <span style="color: white; font-weight: bold;">👤 {greeting}, {user['name'][:20]}...</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Inicializar página ativa se não existir
    if 'active_page' not in st.session_state:
        st.session_state.active_page = 'dashboard'
    
    # Botões do menu
    for i, (label, page_id) in enumerate(current_options):
        with cols[i + 1]:
            if st.button(label, key=f"menu_{page_id}"):
                st.session_state.active_page = page_id
    
    with cols[-1]:
        st.markdown("""
        <div style="text-align: right; padding: 0.7rem;">
            <div style="color: #28a745; font-weight: bold;">🟢 Online</div>
            <div style="color: #666; font-size: 12px;">Nomadix v2.0</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==================== ROTEAMENTO DE PÁGINAS ====================
    active_page = st.session_state.active_page
    
    # Verificar permissões para a página solicitada
    if active_page == 'gov_panel' and not check_permission('admin'):
        st.error("❌ Acesso negado. Esta página é restrita ao nível Governamental.")
        active_page = 'dashboard'
    elif active_page == 'admin' and not check_permission('admin'):
        st.error("❌ Acesso negado. Página administrativa restrita.")
        active_page = 'dashboard'
    elif active_page in ['social_data', 'sdgs'] and user['level'] not in ['GOVERNO', 'ONG']:
        st.error("❌ Acesso negado. Conteúdo restrito para ONGs e Governo.")
        active_page = 'dashboard'
    
    # ==================== RENDERIZAÇÃO DE PÁGINAS ====================
    
    if active_page == 'dashboard':
        render_dashboard_content(df, user)
    elif active_page == 'gov_panel':
        render_government_panel(df)
    elif active_page == 'analytics':
        render_analytics_panel(df)
    elif active_page == 'reports':
        render_reports_panel(df, user)
    elif active_page == 'admin':
        render_admin_panel()
    elif active_page == 'social_data':
        render_social_data_panel(df)
    elif active_page == 'sdgs':
        render_sdgs_panel()
    elif active_page == 'local_data':
        render_local_data_panel(df, user)
    elif active_page == 'overview':
        render_public_overview(df)
    elif active_page == 'basic_stats':
        render_basic_stats(df)
    elif active_page == 'chat':
        render_chat_interface(user)
    else:
        render_dashboard_content(df, user)

def render_dashboard_content(df, user):
    """Renderiza o conteúdo principal do dashboard baseado nas permissões"""
    
    # Sidebar personalizada para o usuário
    with st.sidebar:
        render_user_sidebar(user)
    
    # Verificar nível de acesso para conteúdo
    if user['level'] == 'PÚBLICO':
        render_public_dashboard(df)
    elif user['level'] == 'COMUNIDADE':
        render_community_dashboard(df)  
    elif user['level'] == 'ONG':
        render_ngo_dashboard(df)
    else:  # GOVERNO
        render_full_dashboard(df)

def render_user_sidebar(user):
    """Renderiza sidebar personalizada baseada no usuário"""
    level_color = get_access_level_color(user['level'])
    greeting = get_greeting()
    
    # Perfil do usuário - HEADER PRINCIPAL
    st.markdown(f"""
    <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, {level_color} 0%, #002B5C 100%); border-radius: 15px; margin-bottom: 1.5rem; box-shadow: 0 4px 12px rgba(0, 43, 92, 0.3); border: 2px solid #bba55b;">
        <div style="width: 80px; height: 80px; background: white; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 32px; font-weight: bold; color: #002B5C; margin-bottom: 1rem; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border: 2px solid #bba55b;">
            👤
        </div>
        <div style="color: white; font-weight: bold; font-size: 18px; margin-bottom: 0.25rem;">{user['name']}</div>
        <div style="color: #bba55b; font-size: 14px; margin-bottom: 0.5rem;">Nível: {user['level']}</div>
        <div style="color: rgba(255,255,255,0.8); font-size: 12px;">{greeting} • Sistema Online 🟢</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Menu de permissões
    st.markdown("### 🔐 Suas Permissões")
    permissions_icons = {
        'full_access': '🔓 Acesso Total',
        'admin': '👑 Administrador', 
        'export': '📤 Exportação',
        'alerts': '🚨 Alertas',
        'chat': '💬 Assistente IA',
        'social_data': '🤝 Dados Sociais',
        'local_data': '🏘️ Dados Locais',
        'view_only': '👁️ Visualização',
        'basic_chat': '💬 Chat Básico',
        'basic_export': '📋 Exportação Básica'
    }
    
    for permission in user['permissions']:
        if permission in permissions_icons:
            st.success(permissions_icons[permission])
    
    # Funcionalidades baseadas em permissões
    if check_permission('export'):
        st.markdown("---")
        st.markdown("### 📤 Exportação Rápida")
        if st.button("📊 Exportar Dashboard", use_container_width=True):
            export_dashboard_pdf()
        if st.button("📋 Exportar Dados CSV", use_container_width=True):
            export_data_csv(df)
    
    if check_permission('alerts'):
        st.markdown("---")
        st.markdown("### 🚨 Alertas Ativos") 
        render_alerts_sidebar()
    
    # Status do sistema
    st.markdown("---")
    st.markdown("### 📋 Status")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🟢", "Online", delta="99.9%")
    with col2:
        st.metric("👥", "1,247", delta="+12")

def get_greeting():
    """Retorna saudação baseada na hora"""
    hour = datetime.now().hour
    return "🌅 Bom dia" if hour < 12 else "☀️ Boa tarde" if hour < 18 else "🌙 Boa noite"

def render_full_dashboard(df):
    """Dashboard completo para usuários GOVERNO"""
    st.info("📊 Dashboard completo carregado com sucesso!")
    
    # Conteúdo do dashboard principal (será implementado)
    st.subheader("🎯 Painel Governamental Completo")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Visitantes", f"{df['Visitantes'].sum():,}")
    with col2:
        st.metric("Receita Total", f"{format_aoa(df['Receita_AOA'].sum())}")
    with col3:
        st.metric("Satisfação", f"{df['Satisfação'].mean():.1f}/5.0")

def render_public_dashboard(df):
    """Dashboard público simplificado"""
    st.info("👥 Acesso público ativo - dados básicos")
    render_public_overview(df)

def render_community_dashboard(df):
    """Dashboard para comunidades"""
    st.info("🏘️ Dashboard comunitário ativo")
    render_local_data_panel(df, st.session_state.current_user)

def render_ngo_dashboard(df):
    """Dashboard para ONGs"""
    st.info("🤝 Dashboard ONG ativo - foco em dados sociais")
    render_social_data_panel(df)

def render_local_data_panel(df, user):
    """Painel de dados locais para comunidades"""
    st.subheader("🏘️ Dados da Sua Região")
    
    # Simulação de dados locais
    local_provinces = ['Luanda', 'Benguela', 'Huíla']  # Exemplo
    
    for province in local_provinces:
        province_data = df[df['Província'] == province]
        if not province_data.empty:
            st.markdown(f"### 📍 {province}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Visitantes Locais", f"{province_data['Visitantes'].sum():,}")
            with col2:
                st.metric("Satisfação Local", f"{province_data['Satisfação'].mean():.1f}/5.0")

def render_social_data_panel(df):
    """Painel de dados sociais para ONGs"""
    st.subheader("🤝 Impacto Social do Turismo")
    
    # Métricas sociais simuladas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Empregos Gerados", "12,450", delta="850")
    with col2:
        st.metric("Comunidades Beneficiadas", "89", delta="12")
    with col3:
        st.metric("Projetos Sociais", "34", delta="5")
    
    st.info("📈 Dados sociais específicos para análise de ONGs")

def render_sdgs_panel():
    """Renderiza painel completo de ODSs"""
    st.info("🎯 Carregando painel completo de ODSs...")
    
    # Aqui seria carregado o painel completo de ODSs que já foi implementado
    # Por agora, uma versão simplificada
    sdg_data = generate_sdg_data()
    
    st.subheader("🌍 Progresso dos ODSs")
    
    for ods_key, ods_info in list(sdg_data.items())[:3]:  # Mostrar apenas 3 para exemplo
        col1, col2 = st.columns([1, 2])
        
        with col1:
            progress = (ods_info['meta_atual'] / ods_info['meta_2030']) * 100
            st.markdown(f"""
            <div style="background: {ods_info['cor']}; padding: 1rem; border-radius: 10px; color: white; text-align: center;">
                <h4 style="margin: 0;">{ods_info['nome']}</h4>
                <div style="font-size: 1.5rem; font-weight: bold;">{ods_info['meta_atual']:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            for indicator, value in list(ods_info['indicadores'].items())[:2]:
                st.write(f"**{indicator}**: {value}")

def render_public_overview(df):
    """Visão pública do dashboard"""
    st.subheader("🌍 Angola - Destino Turístico")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🌍 Visitantes", f"{df['Visitantes'].sum():,}")
    with col2:
        st.metric("😊 Satisfação", f"{df['Satisfação'].mean():.1f}/5")
    with col3:
        st.metric("🏛️ Províncias", "18")
    
    # Gráfico público básico
    monthly_visitors = df.groupby('Mês')['Visitantes'].sum()
    
    fig = px.line(
        x=monthly_visitors.index,
        y=monthly_visitors.values,
        title="Visitantes por Mês - Angola 2024",
        markers=True
    )
    
    fig.update_traces(line_color='#96CEB4', marker_color='#96CEB4')
    fig.update_layout(
        xaxis_title="Mês",
        yaxis_title="Visitantes",
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_chat_interface(user):
    """Interface do chatbot"""
    st.subheader("💬 Assistente IA NOMADIX")
    
    # Perguntas sugeridas
    suggestions = [
        "Quais os destinos mais populares?",
        "Como está a satisfação dos turistas?", 
        "Qual a melhor época para visitar Angola?"
    ]
    
    for suggestion in suggestions:
        if st.button(f"❓ {suggestion}"):
            simulate_ai_response(suggestion, user)
        
        # MENU PRINCIPAL COM DROPDOWN FUNCIONAL
        st.markdown("### 🎛️ Menu Principal")
        
        # Usando expander para simular dropdown
        with st.expander("👤 Perfil de Usuário", expanded=False):
            if st.button("📝 Editar Perfil"):
                st.success("✏️ Funcionalidade em desenvolvimento!")
            if st.button("🔑 Alterar Senha"):
                st.info("🔒 Redirecionando para alteração de senha...")
            if st.button("� Alterar Foto"):
                st.info("📸 Upload de foto em desenvolvimento!")
        
        with st.expander("📊 Relatórios & Analytics", expanded=False):
            if st.button("📈 Relatórios Avançados"):
                st.success("📊 Carregando relatórios detalhados...")
            if st.button("� Exportar Dados"):
                st.info("💾 Preparando exportação em Excel/PDF...")
            if st.button("🔍 Analytics Customizados"):
                st.success("🎯 Abrindo ferramentas de análise...")
        
        with st.expander("⚙️ Configurações do Sistema", expanded=False):
            dark_mode = st.checkbox("🌙 Modo Escuro", value=False)
            if dark_mode:
                st.success("🌙 Modo escuro ativado!")
            
            notifications = st.checkbox("🔔 Notificações Push", value=True)
            if notifications:
                st.info("🔔 Notificações ativas")
            
            language = st.selectbox("🌍 Idioma", ["🇵🇹 Português", "🇬🇧 English", "🇫🇷 Français"])
            
        with st.expander("� Suporte & Ajuda", expanded=False):
            if st.button("📞 Contatar Suporte"):
                st.success("📱 Conectando com suporte técnico...")
            if st.button("📋 Documentação"):
                st.info("📖 Abrindo guia de usuário...")
            if st.button("🐛 Reportar Bug"):
                st.warning("� Formulário de bug report em desenvolvimento!")
        
        # STATUS DO SISTEMA
        st.markdown("---")
        st.markdown("### 📋 Status do Sistema")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🟢 Status", "Online", delta="99.9%")
        with col2:
            st.metric("👥 Usuários", "1,247", delta="+12")
            
        st.success("✅ Todos os serviços operacionais")
        st.info(f"🕒 Último acesso: **{datetime.now().strftime('%d/%m/%Y às %H:%M')}**")
        
        # LOGOUT
        st.markdown("---")
        logout_col1, logout_col2, logout_col3 = st.columns([1, 2, 1])
        with logout_col2:
            if st.button("🚪 Sair do Sistema", type="primary"):
                st.balloons()
                st.success("👋 Logout realizado com sucesso!")
                st.info("🔒 Redirecionando para tela de login...")
    
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
    
    # ==================== PAINEL GERAL - VISÃO GLOBAL ====================
    st.markdown("""
    <div style="background: linear-gradient(135deg, #002B5C 0%, #003d7a 100%); padding: 1.5rem; border-radius: 15px; margin: 2rem 0; border: 3px solid #bba55b;">
        <h2 style="color: white; text-align: center; margin: 0; font-size: 2rem;">🌍 PAINEL GERAL - VISÃO GLOBAL</h2>
        <p style="color: #bba55b; text-align: center; margin: 0.5rem 0 0 0; font-size: 1.1rem;">Estado Geral do Turismo e Sustentabilidade em Angola</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Gerar dados avançados
    kpis = generate_advanced_kpis()
    flows_data = generate_tourism_flows()
    origins_data = generate_tourist_origins()
    
    # ===== INDICADORES-CHAVE (KPIs AVANÇADOS) =====
    st.subheader("📈 Indicadores-Chave de Performance (KPIs)")
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)
    
    with kpi_col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #002B5C 0%, #005C9C 100%); padding: 1.2rem; border-radius: 12px; text-align: center; border: 2px solid #bba55b; color: white;">
            <div style="font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem;">👥</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: #bba55b;">{kpis['total_visitors']:,}</div>
            <div style="font-size: 0.9rem; margin: 0.5rem 0;">Total de Visitantes</div>
            <div style="font-size: 0.8rem; color: {'#90EE90' if kpis['monthly_variation'] > 0 else '#FFB6C1'};">
                {'▲' if kpis['monthly_variation'] > 0 else '▼'} {kpis['monthly_variation']:.1f}% vs mês anterior
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #005C9C 0%, #002B5C 100%); padding: 1.2rem; border-radius: 12px; text-align: center; border: 2px solid #bba55b; color: white;">
            <div style="font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem;">💰</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: #bba55b;">{format_aoa(kpis['total_revenue_aoa'])}</div>
            <div style="font-size: 0.9rem; margin: 0.5rem 0;">Receita Total</div>
            <div style="font-size: 0.8rem; color: #90EE90;">Per Capita: {format_aoa(kpis['revenue_per_capita'])}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col3:
        sustainability_color = "#90EE90" if kpis['sustainability_index'] >= 7.0 else "#FFD700" if kpis['sustainability_index'] >= 5.0 else "#FFB6C1"
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #bba55b 0%, #d4c875 100%); padding: 1.2rem; border-radius: 12px; text-align: center; border: 2px solid #002B5C; color: #002B5C;">
            <div style="font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem;">🌱</div>
            <div style="font-size: 1.8rem; font-weight: bold;">{kpis['sustainability_index']:.1f}/10</div>
            <div style="font-size: 0.9rem; margin: 0.5rem 0;">Índice Sustentabilidade</div>
            <div style="font-size: 0.8rem; font-weight: bold;">
                {'🟢 Excelente' if kpis['sustainability_index'] >= 8 else '🟡 Bom' if kpis['sustainability_index'] >= 6 else '🔴 Atenção'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col4:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #002B5C 0%, #005C9C 100%); padding: 1.2rem; border-radius: 12px; text-align: center; border: 2px solid #bba55b; color: white;">
            <div style="font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem;">🏨</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: #bba55b;">{kpis['hotel_occupancy']:.1f}%</div>
            <div style="font-size: 0.9rem; margin: 0.5rem 0;">Taxa Ocupação Hoteleira</div>
            <div style="font-size: 0.8rem; color: {'#90EE90' if kpis['hotel_occupancy'] >= 75 else '#FFD700'};">
                {'🟢 Alta' if kpis['hotel_occupancy'] >= 75 else '🟡 Média'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col5:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #005C9C 0%, #002B5C 100%); padding: 1.2rem; border-radius: 12px; text-align: center; border: 2px solid #bba55b; color: white;">
            <div style="font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem;">👷</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: #bba55b;">{kpis['jobs_created']:,}</div>
            <div style="font-size: 0.9rem; margin: 0.5rem 0;">Empregos Gerados</div>
            <div style="font-size: 0.8rem; color: #90EE90;">No setor turístico</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ===== MAPA INTERATIVO E ANÁLISES =====
    st.subheader("🗺️ Mapa Interativo - Fluxos e Sustentabilidade")
    
    map_col1, map_col2 = st.columns([2, 1])
    
    with map_col1:
        # Mapa de dispersão representando as 18 províncias
        fig_map = px.scatter(
            flows_data,
            x='Lon',
            y='Lat',
            size='Fluxo_Turístico',
            color='Pressão_Ambiental',
            hover_name='Província',
            hover_data={
                'Fluxo_Turístico': ':,',
                'Pressão_Ambiental': ':.1f',
                'Potencial_Investimento': ':.1f'
            },
            color_continuous_scale=['#005C9C', '#F4F5F7', '#002B5C'],
            size_max=30,
            title="Províncias de Angola - Fluxos Turísticos e Pressão Ambiental"
        )
        fig_map.update_layout(
            height=400,
            showlegend=False,
            title_font_size=16,
            title_font_color='#002B5C',
            font_color='#002B5C',
            plot_bgcolor='#F4F5F7',
            paper_bgcolor='white',
            xaxis_title="Longitude",
            yaxis_title="Latitude"
        )
        st.plotly_chart(fig_map, width='stretch')
    
    with map_col2:
        # Top províncias por critérios
        st.markdown("**🏆 Top Províncias por Fluxo Turístico**")
        top_flow = flows_data.nlargest(5, 'Fluxo_Turístico')[['Província', 'Fluxo_Turístico']]
        for idx, row in top_flow.iterrows():
            st.markdown(f"**{row['Província']}**: {row['Fluxo_Turístico']:,} visitantes")
        
        st.markdown("<br>**⚠️ Maior Pressão Ambiental**", unsafe_allow_html=True)
        top_pressure = flows_data.nlargest(3, 'Pressão_Ambiental')[['Província', 'Pressão_Ambiental']]
        for idx, row in top_pressure.iterrows():
            color = "🔴" if row['Pressão_Ambiental'] >= 7 else "🟡"
            st.markdown(f"{color} **{row['Província']}**: {row['Pressão_Ambiental']:.1f}/10")
        
        st.markdown("<br>**💎 Potencial de Investimento**", unsafe_allow_html=True)
        top_investment = flows_data.nlargest(3, 'Potencial_Investimento')[['Província', 'Potencial_Investimento']]
        for idx, row in top_investment.iterrows():
            st.markdown(f"🟢 **{row['Província']}**: {row['Potencial_Investimento']:.1f}/10")
    
    # ===== RESUMO DE TENDÊNCIAS =====
    st.subheader("📊 Resumo de Tendências (Últimos 12 Meses)")
    
    trend_col1, trend_col2, trend_col3 = st.columns(3)
    
    with trend_col1:
        # Crescimento de visitantes
        months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        growth_data = [random.uniform(-5, 20) for _ in months]
        
        fig_growth = px.line(
            x=months,
            y=growth_data,
            title="Crescimento Mensal de Visitantes (%)",
            markers=True
        )
        fig_growth.update_traces(
            line_color='#002B5C',
            marker_color='#bba55b',
            marker_size=8
        )
        fig_growth.update_layout(
            height=300,
            title_font_size=14,
            title_font_color='#002B5C',
            font_color='#002B5C',
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis_title="Mês",
            yaxis_title="Crescimento (%)"
        )
        st.plotly_chart(fig_growth, width='stretch')
    
    with trend_col2:
        # Origem dos turistas
        fig_origins = px.pie(
            values=list(origins_data.values()),
            names=list(origins_data.keys()),
            title="Origem dos Turistas",
            color_discrete_sequence=['#002B5C', '#005C9C', '#bba55b', '#F4F5F7', '#003d7a', '#d4c875', '#1e5a8a']
        )
        fig_origins.update_layout(
            height=300,
            title_font_size=14,
            title_font_color='#002B5C',
            font_color='#002B5C',
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        st.plotly_chart(fig_origins, width='stretch')
    
    with trend_col3:
        # Evolução dos gastos
        spending_months = months
        avg_spending = [random.uniform(1500, 3500) for _ in months]
        
        fig_spending = px.bar(
            x=spending_months,
            y=avg_spending,
            title="Gasto Médio por Turista (USD)",
            color=avg_spending,
            color_continuous_scale=['#002B5C', '#bba55b']
        )
        fig_spending.update_layout(
            height=300,
            title_font_size=14,
            title_font_color='#002B5C',
            font_color='#002B5C',
            plot_bgcolor='white',
            paper_bgcolor='white',
            showlegend=False,
            xaxis_title="Mês",
            yaxis_title="Gasto Médio (USD)"
        )
        st.plotly_chart(fig_spending, width='stretch')
    
    # Separador visual
    st.markdown("---")
    
    # ==================== PAINEL ODSs - OBJETIVOS DE DESENVOLVIMENTO SUSTENTÁVEL ====================
    st.markdown("""
    <div style="background: linear-gradient(135deg, #002B5C 0%, #19486A 100%); padding: 1.5rem; border-radius: 15px; margin: 2rem 0; border: 3px solid #bba55b;">
        <h2 style="color: white; text-align: center; margin: 0; font-size: 2rem;">🎯 PAINEL ODSs - OBJETIVOS DE DESENVOLVIMENTO SUSTENTÁVEL</h2>
        <p style="color: #bba55b; text-align: center; margin: 0.5rem 0 0 0; font-size: 1.1rem;">Monitoramento das Metas Globais de Sustentabilidade no Turismo Angolano</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Gerar dados dos ODSs
    sdg_data = generate_sdg_data()
    
    # ===== VISÃO GERAL DOS ODSs =====
    st.subheader("🌍 Visão Geral do Progresso dos ODSs")
    
    # Métricas gerais dos ODSs
    progress_col1, progress_col2, progress_col3, progress_col4 = st.columns(4)
    
    total_progress = sum([ods['meta_atual'] for ods in sdg_data.values()]) / len(sdg_data)
    ods_on_track = sum([1 for ods in sdg_data.values() if ods['meta_atual'] >= ods['meta_2030'] * 0.85])
    ods_critical = sum([1 for ods in sdg_data.values() if ods['meta_atual'] < ods['meta_2030'] * 0.70])
    
    with progress_col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #19486A 0%, #002B5C 100%); padding: 1.2rem; border-radius: 12px; text-align: center; border: 2px solid #bba55b; color: white;">
            <div style="font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem;">🎯</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: #bba55b;">{total_progress:.1f}%</div>
            <div style="font-size: 0.9rem; margin: 0.5rem 0;">Progresso Médio ODSs</div>
            <div style="font-size: 0.8rem; color: {'#90EE90' if total_progress >= 80 else '#FFD700' if total_progress >= 70 else '#FFB6C1'};">
                {'🟢 No caminho certo' if total_progress >= 80 else '🟡 Atenção necessária' if total_progress >= 70 else '🔴 Ação urgente'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with progress_col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #56C02B 0%, #14A085 100%); padding: 1.2rem; border-radius: 12px; text-align: center; border: 2px solid #bba55b; color: white;">
            <div style="font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem;">✅</div>
            <div style="font-size: 1.8rem; font-weight: bold;">{ods_on_track}</div>
            <div style="font-size: 0.9rem; margin: 0.5rem 0;">ODSs no Caminho Certo</div>
            <div style="font-size: 0.8rem;">De {len(sdg_data)} ODSs monitorados</div>
        </div>
        """, unsafe_allow_html=True)
    
    with progress_col3:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #E5243B 0%, #FF3A21 100%); padding: 1.2rem; border-radius: 12px; text-align: center; border: 2px solid #bba55b; color: white;">
            <div style="font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem;">⚠️</div>
            <div style="font-size: 1.8rem; font-weight: bold;">{ods_critical}</div>
            <div style="font-size: 0.9rem; margin: 0.5rem 0;">ODSs Críticos</div>
            <div style="font-size: 0.8rem;">Necessitam ação urgente</div>
        </div>
        """, unsafe_allow_html=True)
    
    with progress_col4:
        years_remaining = 2030 - datetime.now().year
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FD6925 0%, #BF8B2E 100%); padding: 1.2rem; border-radius: 12px; text-align: center; border: 2px solid #002B5C; color: white;">
            <div style="font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem;">⏰</div>
            <div style="font-size: 1.8rem; font-weight: bold;">{years_remaining}</div>
            <div style="font-size: 0.9rem; margin: 0.5rem 0;">Anos até 2030</div>
            <div style="font-size: 0.8rem;">Prazo para as metas</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ===== PAINÉIS ESPECÍFICOS POR ODS =====
    st.subheader("📊 Monitoramento Detalhado por ODS")
    
    # Criar abas para cada ODS
    tab_names = [f"{ods_key.upper().replace('_', ' ')}" for ods_key in sdg_data.keys()]
    tabs = st.tabs(tab_names)
    
    for i, (ods_key, ods_info) in enumerate(sdg_data.items()):
        with tabs[i]:
            ods_col1, ods_col2 = st.columns([1, 2])
            
            with ods_col1:
                # Card principal do ODS
                progress_percent = (ods_info['meta_atual'] / ods_info['meta_2030']) * 100
                status_color = "#90EE90" if progress_percent >= 85 else "#FFD700" if progress_percent >= 70 else "#FFB6C1"
                status_text = "🟢 No Caminho" if progress_percent >= 85 else "🟡 Atenção" if progress_percent >= 70 else "🔴 Crítico"
                
                st.markdown(f"""
                <div style="background: {ods_info['cor']}; padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 1rem;">
                    <h3 style="margin: 0 0 1rem 0; font-size: 1.3rem;">{ods_info['nome']}</h3>
                    <div style="font-size: 2.5rem; font-weight: bold; margin: 1rem 0;">{ods_info['meta_atual']:.1f}%</div>
                    <div style="background: rgba(255,255,255,0.2); border-radius: 10px; padding: 0.5rem; margin: 1rem 0;">
                        Meta 2030: {ods_info['meta_2030']}%
                    </div>
                    <div style="font-size: 1.1rem; font-weight: bold;">{status_text}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Barra de progresso
                st.markdown(f"""
                <div style="background: #f0f0f0; border-radius: 10px; padding: 0.5rem; margin-bottom: 1rem;">
                    <div style="background: {ods_info['cor']}; height: 20px; border-radius: 8px; width: {min(progress_percent, 100):.1f}%;"></div>
                    <div style="text-align: center; margin-top: 0.5rem; color: #666; font-size: 0.9rem;">
                        Progresso: {progress_percent:.1f}% da meta 2030
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with ods_col2:
                # Indicadores específicos
                st.markdown("**📈 Indicadores-Chave:**")
                
                for indicator, value in ods_info['indicadores'].items():
                    if isinstance(value, float):
                        if '%' in indicator:
                            display_value = f"{value:.1f}%"
                            color = "#90EE90" if value >= 75 else "#FFD700" if value >= 50 else "#FFB6C1"
                        else:
                            display_value = f"{value:.1f}"
                            color = "#90EE90"
                    else:
                        display_value = f"{value:,}"
                        color = "#90EE90"
                    
                    st.markdown(f"""
                    <div style="background: white; border-left: 4px solid {ods_info['cor']}; padding: 1rem; margin: 0.5rem 0; border-radius: 0 8px 8px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <div style="font-weight: bold; color: #333; margin-bottom: 0.3rem;">{indicator}</div>
                        <div style="font-size: 1.5rem; font-weight: bold; color: {color};">{display_value}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Gráfico de tendência simulado para cada ODS
                months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
                base_value = ods_info['meta_atual']
                trend_data = [base_value + random.uniform(-5, 3) for _ in months]
                
                fig_ods_trend = px.line(
                    x=months,
                    y=trend_data,
                    title=f"Tendência {ods_info['nome']} (2024)",
                    markers=True
                )
                fig_ods_trend.update_traces(
                    line_color=ods_info['cor'],
                    marker_color=ods_info['cor'],
                    marker_size=6
                )
                fig_ods_trend.update_layout(
                    height=250,
                    title_font_size=12,
                    title_font_color='#002B5C',
                    font_color='#002B5C',
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    xaxis_title="Mês",
                    yaxis_title="Progresso (%)"
                )
                fig_ods_trend.add_hline(y=ods_info['meta_2030'], 
                                       line_dash="dash", 
                                       line_color="red", 
                                       annotation_text="Meta 2030")
                st.plotly_chart(fig_ods_trend, width='stretch')
    
    # ===== DASHBOARD COMPARATIVO ODSs =====
    st.subheader("📊 Dashboard Comparativo - Todos os ODSs")
    
    comp_col1, comp_col2 = st.columns(2)
    
    with comp_col1:
        # Gráfico de barras comparativo
        ods_names = [ods['nome'].replace('ODS ', '').replace(' -', '\n') for ods in sdg_data.values()]
        ods_values = [ods['meta_atual'] for ods in sdg_data.values()]
        ods_colors = [ods['cor'] for ods in sdg_data.values()]
        
        fig_comp = px.bar(
            x=ods_names,
            y=ods_values,
            title="Progresso Atual de Todos os ODSs (%)",
            color=ods_values,
            color_continuous_scale='Viridis'
        )
        fig_comp.update_layout(
            height=400,
            title_font_size=14,
            title_font_color='#002B5C',
            font_color='#002B5C',
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis_title="ODSs",
            yaxis_title="Progresso Atual (%)",
            showlegend=False
        )
        fig_comp.add_hline(y=75, line_dash="dash", line_color="orange", annotation_text="Meta Mínima")
        st.plotly_chart(fig_comp, width='stretch')
    
    with comp_col2:
        # Radar chart dos ODSs
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=ods_values,
            theta=ods_names,
            fill='toself',
            name='Progresso Atual',
            line_color='#002B5C',
            fillcolor='rgba(0, 43, 92, 0.3)'
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=[ods['meta_2030'] for ods in sdg_data.values()],
            theta=ods_names,
            fill='toself',
            name='Meta 2030',
            line_color='#bba55b',
            fillcolor='rgba(187, 165, 91, 0.2)',
            line_dash='dash'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont_size=10
                )
            ),
            showlegend=True,
            title="Radar ODSs - Atual vs Meta 2030",
            title_font_size=14,
            title_font_color='#002B5C',
            font_color='#002B5C',
            height=400
        )
        st.plotly_chart(fig_radar, width='stretch')
    
    # Separador visual
    st.markdown("---")
    
    # Gráficos principais (seção existente)
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
            color_continuous_scale=['#002B5C', '#bba55b']
        )
        fig_bar.update_layout(
            height=400,
            showlegend=False,
            xaxis_title="Número de Visitantes",
            yaxis_title="Província"
        )
        st.plotly_chart(fig_bar, width='stretch')
    
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
            line_color='#002B5C',
            marker_color='#bba55b',
            marker_size=8
        )
        fig_line.update_layout(
            height=400,
            xaxis_title="Mês",
            yaxis_title="Receita (AOA)"
        )
        st.plotly_chart(fig_line, width='stretch')
    
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
        color_continuous_scale=['#002B5C', '#F4F5F7', '#005C9C'],
        aspect='auto'
    )
    fig_heatmap.update_layout(
        height=500,
        title_font_size=18,
        title_font_color='#002B5C',
        font_color='#002B5C',
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    st.plotly_chart(fig_heatmap, width='stretch')
    
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
    
    # Mostrar tabela formatada usando HTML
    table_data = province_summary[['Visitantes', 'Receita_Formatada', 'Satisfação']].rename(columns={
        'Visitantes': 'Total Visitantes',
        'Receita_Formatada': 'Receita Total (AOA)',
        'Satisfação': 'Satisfação Média'
    })
    
    # Criar tabela HTML
    html_table = "<table style='width:100%; border-collapse: collapse;'>"
    html_table += "<tr style='background: linear-gradient(135deg, #002B5C 0%, #003d7a 100%); color: white;'>"
    html_table += "<th style='padding: 10px; border: 2px solid #bba55b;'>Província</th>"
    for col in table_data.columns:
        html_table += f"<th style='padding: 10px; border: 2px solid #bba55b;'>{col}</th>"
    html_table += "</tr>"
    
    for idx, row in table_data.iterrows():
        html_table += "<tr style='background-color: #f8f9fa;'>"
        html_table += f"<td style='padding: 10px; border: 1px solid #bba55b; font-weight: bold; color: #002B5C;'>{idx}</td>"
        for val in row:
            html_table += f"<td style='padding: 10px; border: 1px solid #bba55b; text-align: center; color: #002B5C;'>{val}</td>"
        html_table += "</tr>"
    html_table += "</table>"
    
    st.markdown(html_table, unsafe_allow_html=True)
    
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

# ==================== FUNCIONALIDADES DE EXPORTAÇÃO ====================

def export_dashboard_pdf():
    """Exporta o dashboard atual em PDF"""
    try:
        st.success("📄 Preparando relatório em PDF...")
        
        pdf_content = f"""RELATÓRIO NOMADIX - DASHBOARD TURÍSTICO ANGOLA
        
Data de Geração: {datetime.now().strftime('%d/%m/%Y às %H:%M')}
Usuário: {st.session_state.current_user['name']}
Nível de Acesso: {st.session_state.current_user['level']}

RESUMO EXECUTIVO:
- Sistema de monitoramento turístico integrado
- Dados em tempo real de todas as províncias
- Análise de ODSs e sustentabilidade
- Inteligência artificial aplicada

Este relatório contém dados confidenciais do sistema NOMADIX.
Distribuição restrita conforme nível de acesso do usuário.
"""
        
        st.download_button(
            label="📥 Baixar Relatório PDF",
            data=pdf_content,
            file_name=f"nomadix_relatorio_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain"
        )
        
        st.info("✅ Relatório gerado com sucesso!")
        
    except Exception as e:
        st.error(f"❌ Erro ao gerar PDF: {str(e)}")

def export_data_csv(df):
    """Exporta dados em formato CSV"""
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
            label="📥 Baixar Dados CSV",
            data=csv_data,
            file_name=f"nomadix_dados_{user_level.lower()}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )
        
        st.success(f"✅ Arquivo CSV preparado com {len(export_df)} registros!")
        
    except Exception as e:
        st.error(f"❌ Erro ao exportar CSV: {str(e)}")

def render_alerts_sidebar():
    """Renderiza alertas na sidebar"""
    alerts = [
        {'type': 'critical', 'message': 'ODS 14 abaixo de 70% da meta'},
        {'type': 'warning', 'message': 'Queda de turismo em Benguela'}, 
        {'type': 'info', 'message': 'Nova campanha ativa'}
    ]
    
    for alert in alerts[:3]:
        if alert['type'] == 'critical':
            st.error(f"🚨 {alert['message']}")
        elif alert['type'] == 'warning':
            st.warning(f"⚠️ {alert['message']}")
        else:
            st.info(f"ℹ️ {alert['message']}")

# ==================== SIMULAÇÃO DE CHATBOT IA ====================

def simulate_ai_response(question, user):
    """Simula resposta do assistente IA"""
    responses = {
        'roi': f"📊 ROI médio das campanhas: 312%. Luanda lidera com 425%.",
        'ods': "🎯 ODS 8: 78%, ODS 14: 65%. Foco recomendado no ODS 14.",
        'investimento': "💰 Cunene, Cuando Cubango e Moxico precisam de investimento prioritário.",
        'destinos': "🏆 Top 3: Luanda (32%), Benguela (18%), Huíla (12%)."
    }
    
    response = "🤖 Analisando dados disponíveis para sua pergunta..."
    
    for key, value in responses.items():
        if key in question.lower():
            response = value
            break
    
    st.success(f"🤖 **Assistente NOMADIX**: {response}")
    st.info("💡 Posso gerar relatórios específicos ou análises complementares!")

if __name__ == "__main__":
    main()