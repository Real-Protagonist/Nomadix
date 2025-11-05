# Nomadix - Guia de Início Rápido

## 🚀 Como Iniciar o Projeto

### 1. Instalação das Dependências

Primeiro, crie e ative um ambiente virtual:

```powershell
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
.\venv\Scripts\activate
```

Instale as dependências:

```powershell
pip install -r requirements.txt
```

### 2. Gerar Dados de Exemplo

Execute o script de geração de dados:

```powershell
python generate_sample_data.py
```

### 3. Executar o Dashboard

Inicie o Streamlit:

```powershell
streamlit run src/app.py
```

O dashboard abrirá automaticamente em `http://localhost:8501`

## 📂 Estrutura do Projeto

```
Nomadix/
├── src/
│   ├── app.py                      # Dashboard principal
│   ├── models/
│   │   ├── clustering.py           # Modelo de clustering (Scikit-learn)
│   │   └── forecasting.py          # Modelo de previsão (Prophet)
│   ├── utils/
│   │   ├── data_loader.py          # Carregamento de dados
│   │   ├── data_processor.py       # Processamento com Pandas
│   │   └── visualizer.py           # Visualizações
│   └── pages/
│       ├── 1_analise_detalhada.py  # Análises com ML
│       ├── 2_previsoes.py          # Previsões temporais
│       └── 3_insights_regionais.py # Análises regionais
├── data/
│   ├── raw/                        # Dados brutos
│   └── processed/                  # Dados processados
├── requirements.txt                # Dependências
└── README.md                      # Documentação

```

## 🎯 Funcionalidades

1. **Dashboard Principal** (`src/app.py`)
   - KPIs em tempo real
   - Gráficos interativos
   - Análise de sazonalidade

2. **Análise Detalhada** (Página 1)
   - Clustering de destinos com Scikit-learn
   - Análise de correlação
   - Análise temporal

3. **Previsões** (Página 2)
   - Previsões com Prophet
   - Análise de tendências
   - Intervalos de confiança

4. **Insights Regionais** (Página 3)
   - Comparação entre províncias
   - Perfis regionais
   - Recomendações estratégicas

## 🔧 Tecnologias Utilizadas

- **Python 3.9+**
- **Streamlit** - Interface web
- **Pandas** - Processamento de dados
- **Scikit-learn** - Machine Learning
- **Prophet** - Previsões temporais
- **Plotly** - Visualizações interativas

## 📝 Notas

- Os dados de exemplo são gerados automaticamente
- O sistema usa dados sintéticos para demonstração
- Personalize os dados em `generate_sample_data.py`

## 🆘 Solução de Problemas

Se encontrar erros durante a instalação:

```powershell
# Atualizar pip
python -m pip install --upgrade pip

# Reinstalar dependências
pip install -r requirements.txt --upgrade
```

## 📧 Suporte

Para questões ou sugestões, consulte a documentação completa no README.md
