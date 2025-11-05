# 🌍 Nomadix - Dashboard de Insights Turísticos para Angola

Sistema de dashboard administrativo web que serve como motor de insights para planejamento turístico em Angola, utilizando análise de dados e machine learning.

## 📋 Sobre o Projeto

Nomadix é uma plataforma analítica desenvolvida para fornecer insights estratégicos sobre o turismo em Angola. O sistema processa dados turísticos, realiza análises preditivas e apresenta visualizações interativas para apoiar decisões de planejamento.

### 🎯 Características Principais
- **Dashboard Interativo**: Interface web moderna com Streamlit
- **Análise em Tempo Real**: Métricas atualizadas de turismo
- **Moeda Local**: Valores apresentados em Kwanza Angolano (AOA)
- **Visualizações Avançadas**: Gráficos interativos com Plotly
- **Dados Provinciais**: Análise detalhada por região de Angola

## 🚀 Tecnologias

- **Python 3.9+** - Linguagem principal
- **Streamlit** - Framework web para dashboards
- **Pandas** - Manipulação e análise de dados
- **Scikit-learn** - Machine Learning
- **Prophet** - Previsões de séries temporais
- **Plotly** - Visualizações interativas
- **NumPy** - Computação científica

## 📁 Estrutura do Projeto

```
Nomadix/
├── src/
│   ├── utils/          # Utilitários e funções auxiliares
│   ├── models/         # Modelos de ML e previsões
│   ├── pages/          # Páginas do dashboard
│   └── app.py          # Aplicação principal
├── data/
│   ├── raw/            # Dados brutos
│   └── processed/      # Dados processados
├── assets/             # Imagens e recursos
└── requirements.txt    # Dependências
```

## 🔧 Guia Completo de Instalação

### 📋 Pré-requisitos

Antes de começar, certifique-se de que você tem instalado:

- **Python 3.9 ou superior** ([Download aqui](https://python.org/downloads/))
- **Git** ([Download aqui](https://git-scm.com/downloads))
- **Editor de código** (recomendado: VS Code)

### 🖥️ Preparação do Ambiente

#### 1️⃣ **Verificação do Python**

Abra o terminal/prompt de comando e verifique a versão do Python:

```bash
python --version
# Deve mostrar Python 3.9.x ou superior
```

Se não tiver Python instalado, baixe em: https://python.org/downloads/

#### 2️⃣ **Clone do Repositório**

```bash
# Clone o repositório (substitua pela URL real)
git clone <repository-url>

# Entre na pasta do projeto
cd Nomadix
```

#### 3️⃣ **Criação do Ambiente Virtual**

**No Windows:**
```bash
# Criar ambiente virtual
python -m venv nomadix_env

# Ativar ambiente virtual
nomadix_env\Scripts\activate

# Confirmar ativação (deve aparecer (nomadix_env) no início da linha)
```

**No macOS/Linux:**
```bash
# Criar ambiente virtual
python3 -m venv nomadix_env

# Ativar ambiente virtual
source nomadix_env/bin/activate

# Confirmar ativação (deve aparecer (nomadix_env) no início da linha)
```

#### 4️⃣ **Instalação das Dependências**

**Método 1 - Instalação Automática (Recomendado):**
```bash
pip install -r requirements.txt
```

**Método 2 - Instalação Manual (caso haja problemas):**
```bash
# Dependências essenciais
pip install streamlit pandas plotly numpy

# Dependências complementares
pip install scikit-learn python-dateutil pytz tzdata

# Dependências opcionais (para funcionalidades avançadas)
pip install seaborn matplotlib
```

### ⚠️ Solução de Problemas Comuns

#### **Problema 1: Erro do PyArrow**
Se aparecer erro "No module named 'pyarrow'":

```bash
# Instalar sem PyArrow (versão simplificada)
pip install streamlit pandas plotly --no-deps
pip install altair blinker cachetools click gitpython pillow protobuf pydeck requests tenacity toml tornado typing_extensions watchdog
```

#### **Problema 2: Erro de Compilação no Windows**
Se houver erros de compilação (especialmente com numpy/pandas):

```bash
# Usar versões pré-compiladas
pip install --only-binary=all pandas numpy plotly streamlit
```

#### **Problema 3: Permissões no Windows**
Se aparecer erro de permissão:

```bash
# Instalar para usuário atual
pip install --user streamlit pandas plotly
```

### 📁 Estrutura de Arquivos Necessária

Certifique-se de que a estrutura está assim:

```
Nomadix/
├── src/
│   ├── __init__.py
│   ├── app.py                 # Aplicação principal original
│   ├── models/
│   ├── pages/
│   └── utils/
├── run_simple.py              # Versão simplificada (funcional)
├── nomadix_no_pyarrow.py      # Versão sem PyArrow (alternativa)
├── requirements.txt
├── README.md
└── data/
```

## ▶️ Como Executar

### 🚀 **Execução Principal**

1. **Ative o ambiente virtual** (se não estiver ativo):
   ```bash
   # Windows
   nomadix_env\Scripts\activate
   
   # macOS/Linux
   source nomadix_env/bin/activate
   ```

2. **Execute a aplicação**:
   ```bash
   # Versão simplificada (recomendada)
   streamlit run run_simple.py
   
   # Ou versão sem PyArrow (alternativa)
   streamlit run nomadix_no_pyarrow.py
   
   # Ou versão original (se todas as dependências estiverem instaladas)
   streamlit run src/app.py
   ```

3. **Acesse no navegador**:
   - URL Local: `http://localhost:8501`
   - URL de Rede: `http://192.168.x.x:8501` (para acesso remoto)

### 🔄 **Comandos Úteis**

```bash
# Parar a aplicação
Ctrl + C

# Verificar dependências instaladas
pip list

# Atualizar dependências
pip install --upgrade streamlit pandas plotly

# Desativar ambiente virtual
deactivate
```

### 🌐 **Acesso Remoto**

Para acessar de outras máquinas na rede:

```bash
# Execute com configuração de rede
streamlit run run_simple.py --server.address 0.0.0.0 --server.port 8501
```

Depois acesse: `http://[IP-DA-MAQUINA]:8501`

## 📊 Funcionalidades

- **Análise de Dados Turísticos**: Processamento e visualização de dados históricos
- **Previsões com ML**: Modelos preditivos para tendências turísticas
- **Insights Regionais**: Análises por província e destino
- **Dashboard Interativo**: Interface intuitiva com métricas em tempo real
- **Análise de Sazonalidade**: Identificação de padrões temporais

## 📈 Módulos

1. **Data Processing**: Limpeza e transformação de dados
2. **ML Models**: Clustering e classificação com Scikit-learn
3. **Forecasting**: Previsões temporais com Prophet
4. **Visualizations**: Gráficos e dashboards interativos

### ===================================

## 📊 Funcionalidades 2

### 🎯 **Dashboard Principal**
- **Métricas em Tempo Real**: Visitantes, receita, satisfação e crescimento
- **Cards Interativos**: Visualização colorida com gradientes
- **Moeda Local**: Valores em Kwanza Angolano (AOA)
- **Responsividade**: Interface adaptável a diferentes dispositivos

### 📈 **Análises Disponíveis**
- **Análise Provincial**: Dados detalhados por província de Angola
- **Gráficos Interativos**: Barras e pizza com Plotly
- **Tabelas Formatadas**: Dados organizados e fáceis de ler
- **Insights Estratégicos**: Recomendações para planejamento turístico

### 🏛️ **Províncias Cobertas**
- **Luanda** - Capital e maior centro turístico
- **Benguela** - Região costeira com potencial
- **Huíla** - Interior com alta satisfação
- **Namibe** - Costa sul com crescimento
- **Kwanza Sul** - Desenvolvimento emergente

## 📈 Módulos do Sistema

### 🔧 **Arquivos Principais**

1. **`run_simple.py`** - Versão funcional principal
   - Interface completa com Streamlit
   - Cards de métricas com CSS customizado
   - Tabelas formatadas sem PyArrow
   - Gráficos interativos com Plotly

2. **`nomadix_no_pyarrow.py`** - Versão alternativa
   - Funciona sem dependências complexas
   - Interface simplificada mas completa
   - Ideal para ambientes com restrições

3. **`src/app.py`** - Versão original avançada
   - Funcionalidades completas de ML
   - Requer todas as dependências
   - Análises preditivas com Prophet

### � **Estrutura de Dados**

```python
# Exemplo de dados utilizados
data = {
    'Província': ['Luanda', 'Benguela', 'Huíla', 'Namibe', 'Kwanza Sul'],
    'Visitantes_2024': [520000, 135000, 92000, 78000, 52000],
    'Receita_AOA': [10312500000, 2640000000, 1732500000, 1485000000, 990000000],
    'Satisfação': [4.2, 4.5, 4.7, 4.3, 4.1]
}
```

## 🔍 Configurações Avançadas

### 🎨 **Personalização da Interface**

Para modificar cores e estilos, edite as seções CSS nos arquivos:

```python
# Cores dos cards de métricas
.metric-card-visitors { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.metric-card-revenue { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
.metric-card-satisfaction { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
.metric-card-growth { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
```

### 📊 **Adição de Novos Dados**

Para incluir novas províncias ou métricas, modifique a função `generate_sample_data()`:

```python
def generate_sample_data():
    data = {
        'Província': ['Nova Província'],
        'Visitantes_2024': [100000],
        'Receita_AOA': [2000000000],
        'Satisfação': [4.0]
    }
    return pd.DataFrame(data)
```

### 🌐 **Configuração de Produção**

Para deploy em servidor:

```bash
# Configuração para produção
streamlit run run_simple.py \
  --server.address 0.0.0.0 \
  --server.port 8501 \
  --server.headless true \
  --server.enableCORS false
```

## 🆘 FAQ - Perguntas Frequentes

### ❓ **Problemas Comuns**

**P: A aplicação não abre no navegador?**
R: Verifique se o Streamlit está instalado corretamente e tente acessar manualmente `http://localhost:8501`

**P: Erro "ModuleNotFoundError"?**
R: Ative o ambiente virtual e reinstale as dependências com `pip install -r requirements.txt`

**P: Tabela não aparece formatada?**
R: Use a versão `run_simple.py` que tem tabelas otimizadas sem PyArrow

**P: Gráficos não aparecem?**
R: Instale o Plotly com `pip install plotly`

### 🔧 **Comandos de Diagnóstico**

```bash
# Verificar versão do Python
python --version

# Listar pacotes instalados
pip list | grep -E "streamlit|pandas|plotly"

# Testar importação
python -c "import streamlit, pandas, plotly; print('Todas as dependências OK')"
```

## CRIADORES

    - LILIANE NETO
    - x x x x x


## 👥 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

**Desenvolvido para planejamento turístico em Angola 🇦🇴**

*Sistema criado para apoiar o desenvolvimento sustentável do turismo angolano através de análise de dados e insights estratégicos.*
