# 📋 Guia Detalhado de Instalação - Nomadix

## 🎯 Para Executar em Nova Máquina

### 📚 Índice
1. [Preparação do Sistema](#preparação-do-sistema)
2. [Instalação do Python](#instalação-do-python)
3. [Configuração do Projeto](#configuração-do-projeto)
4. [Instalação das Dependências](#instalação-das-dependências)
5. [Execução da Aplicação](#execução-da-aplicação)
6. [Solução de Problemas](#solução-de-problemas)
7. [Verificações Finais](#verificações-finais)

---

## 🖥️ Preparação do Sistema

### Windows 10/11

1. **Abrir PowerShell como Administrador**
   - Pressione `Win + X`
   - Selecione "Windows PowerShell (Admin)" ou "Terminal (Admin)"

2. **Verificar/Instalar Chocolatey** (opcional, para facilitar instalações)
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```

### macOS

1. **Instalar Homebrew** (se não tiver)
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Instalar ferramentas básicas**
   ```bash
   brew install git
   ```

### Ubuntu/Linux

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar ferramentas necessárias
sudo apt install git curl wget python3 python3-pip python3-venv -y
```

---

## 🐍 Instalação do Python

### Windows

**Opção 1 - Download Oficial:**
1. Acesse https://python.org/downloads/
2. Baixe Python 3.9+ (recomendado: 3.11)
3. **IMPORTANTE:** Marque "Add Python to PATH" durante instalação
4. Execute o instalador como administrador

**Opção 2 - Com Chocolatey:**
```powershell
choco install python -y
```

**Verificação:**
```powershell
python --version
pip --version
```

### macOS

**Com Homebrew:**
```bash
brew install python@3.11
```

**Verificação:**
```bash
python3 --version
pip3 --version
```

### Linux

```bash
# Ubuntu/Debian
sudo apt install python3.11 python3.11-venv python3.11-pip -y

# CentOS/RHEL
sudo yum install python3.11 python3.11-venv python3.11-pip -y
```

---

## 📁 Configuração do Projeto

### 1. Obter os Arquivos do Projeto

**Se tiver acesso ao Git:**
```bash
git clone [URL-DO-REPOSITORIO]
cd Nomadix
```

**Se não tiver Git (download manual):**
1. Baixe o arquivo ZIP do projeto
2. Extraia para uma pasta (ex: `C:\Nomadix` ou `~/Nomadix`)
3. Abra terminal/prompt na pasta do projeto

### 2. Estrutura Esperada

Verifique se tem esta estrutura:
```
Nomadix/
├── run_simple.py              ← Principal
├── nomadix_no_pyarrow.py      ← Alternativo
├── requirements.txt           ← Dependências
├── README.md
├── INSTALL_GUIDE.md           ← Este arquivo
└── src/
    ├── app.py
    ├── models/
    ├── pages/
    └── utils/
```

---

## 🔧 Instalação das Dependências

### 1. Criar Ambiente Virtual

**Windows:**
```powershell
# Navegar para pasta do projeto
cd C:\Nomadix

# Criar ambiente virtual
python -m venv nomadix_env

# Ativar ambiente
.\nomadix_env\Scripts\Activate.ps1

# Se der erro de execução de script:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**macOS/Linux:**
```bash
# Navegar para pasta do projeto
cd ~/Nomadix

# Criar ambiente virtual
python3 -m venv nomadix_env

# Ativar ambiente
source nomadix_env/bin/activate
```

### 2. Verificar Ativação

O prompt deve mostrar `(nomadix_env)` no início:
```
(nomadix_env) C:\Nomadix>
```

### 3. Atualizar pip

```bash
python -m pip install --upgrade pip
```

### 4. Instalar Dependências

**Método Principal:**
```bash
pip install -r requirements.txt
```

**Se der erro, tente instalação individual:**
```bash
# Dependências core (essenciais)
pip install streamlit
pip install pandas
pip install plotly
pip install numpy

# Dependências complementares
pip install scikit-learn
pip install python-dateutil
pip install pytz
pip install tzdata

# Dependências do Streamlit
pip install altair blinker cachetools click gitpython
pip install pillow protobuf pydeck requests tenacity toml
pip install tornado typing_extensions watchdog
```

**Para problemas com compilação (Windows):**
```bash
pip install --only-binary=all pandas numpy scikit-learn
```

### 5. Verificar Instalação

```bash
# Verificar pacotes instalados
pip list

# Testar importações
python -c "import streamlit; print('Streamlit OK')"
python -c "import pandas; print('Pandas OK')"
python -c "import plotly; print('Plotly OK')"
```

---

## 🚀 Execução da Aplicação

### 1. Certificar que Ambiente está Ativo

```bash
# Windows
.\nomadix_env\Scripts\Activate.ps1

# macOS/Linux
source nomadix_env/bin/activate
```

### 2. Executar Aplicação

**Opção 1 - Versão Simplificada (Recomendada):**
```bash
streamlit run run_simple.py
```

**Opção 2 - Versão Sem PyArrow:**
```bash
streamlit run nomadix_no_pyarrow.py
```

**Opção 3 - Versão Original Completa:**
```bash
streamlit run src/app.py
```

### 3. Acessar no Navegador

A aplicação abrirá automaticamente, ou acesse manualmente:
- **Local:** http://localhost:8501
- **Rede:** http://[SEU-IP]:8501

### 4. Configurações Avançadas

**Para acesso remoto:**
```bash
streamlit run run_simple.py --server.address 0.0.0.0
```

**Para porta específica:**
```bash
streamlit run run_simple.py --server.port 8080
```

**Para modo headless (servidor):**
```bash
streamlit run run_simple.py --server.headless true
```

---

## 🚨 Solução de Problemas

### Erro: "streamlit: command not found"

**Windows:**
```powershell
# Adicionar ao PATH
$env:PATH += ";C:\Users\[SEU-USUARIO]\AppData\Roaming\Python\Python311\Scripts"

# Ou executar diretamente
python -m streamlit run run_simple.py
```

**macOS/Linux:**
```bash
# Adicionar ao PATH
export PATH="$HOME/.local/bin:$PATH"

# Ou executar diretamente
python3 -m streamlit run run_simple.py
```

### Erro: "No module named 'pyarrow'"

```bash
# Use a versão sem PyArrow
streamlit run nomadix_no_pyarrow.py

# Ou tente instalar (pode não funcionar em todos os sistemas)
pip install pyarrow
```

### Erro: "Permission denied"

**Windows:**
```powershell
# Executar como administrador ou
pip install --user streamlit pandas plotly
```

**Linux/macOS:**
```bash
# Usar sudo apenas se necessário
sudo pip3 install streamlit pandas plotly

# Preferível usar --user
pip3 install --user streamlit pandas plotly
```

### Erro de Compilação (numpy/pandas)

```bash
# Windows - usar binários pré-compilados
pip install --only-binary=all numpy pandas

# Ou usar conda
conda install numpy pandas plotly streamlit
```

### Aplicação não Abre no Navegador

1. Verificar se o Streamlit iniciou corretamente
2. Acessar manualmente: http://localhost:8501
3. Verificar firewall/antivírus
4. Tentar porta diferente: `--server.port 8080`

---

## ✅ Verificações Finais

### Checklist de Instalação

- [ ] Python 3.9+ instalado e no PATH
- [ ] Ambiente virtual criado e ativado
- [ ] Dependências instaladas sem erros
- [ ] Streamlit executa sem erros
- [ ] Aplicação abre no navegador
- [ ] Dados aparecem corretamente
- [ ] Gráficos são exibidos
- [ ] Tabela está formatada

### Comandos de Teste

```bash
# Testar Python
python --version

# Testar ambiente virtual ativo
echo $VIRTUAL_ENV  # Linux/macOS
echo $env:VIRTUAL_ENV  # Windows PowerShell

# Testar dependências
python -c "import streamlit, pandas, plotly, numpy; print('Todas dependências OK!')"

# Testar Streamlit
streamlit --version
```

### Informações do Sistema

```bash
# Ver informações detalhadas
python -m streamlit doctor

# Ver configurações
streamlit config show
```

---

## 📞 Suporte

Se ainda tiver problemas:

1. **Verificar logs:** O terminal mostra mensagens de erro detalhadas
2. **Consultar documentação:** [Streamlit Docs](https://docs.streamlit.io/)
3. **Testar versão mínima:** Use `nomadix_no_pyarrow.py` se houver muitos erros
4. **Documentar erro:** Copie a mensagem completa do erro para análise

### Informações Úteis para Suporte

```bash
# Sistema operacional
python -c "import platform; print(platform.platform())"

# Versão Python
python --version

# Versões dos pacotes
pip list | grep -E "streamlit|pandas|plotly"

# Configuração do Streamlit
streamlit --version
```

---

**🎉 Parabéns! Se chegou até aqui, sua instalação deve estar funcionando perfeitamente!**

Acesse http://localhost:8501 e aproveite o dashboard Nomadix! 🌍