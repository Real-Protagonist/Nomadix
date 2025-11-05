# ⚡ Comandos Rápidos - Nomadix

## 🚀 Instalação Expressa

### Windows (PowerShell)
```powershell
# 1. Clonar/baixar projeto para C:\Nomadix
cd C:\Nomadix

# 2. Criar ambiente virtual
python -m venv nomadix_env
.\nomadix_env\Scripts\Activate.ps1

# 3. Instalar dependências
pip install streamlit pandas plotly numpy
pip install altair blinker cachetools click gitpython pillow protobuf pydeck requests tenacity toml tornado typing_extensions watchdog

# 4. Executar
streamlit run run_simple.py
```

### macOS/Linux
```bash
# 1. Clonar/baixar projeto para ~/Nomadix
cd ~/Nomadix

# 2. Criar ambiente virtual
python3 -m venv nomadix_env
source nomadix_env/bin/activate

# 3. Instalar dependências
pip install streamlit pandas plotly numpy
pip install altair blinker cachetools click gitpython pillow protobuf pydeck requests tenacity toml tornado typing_extensions watchdog

# 4. Executar
streamlit run run_simple.py
```

## 🔧 Comandos Essenciais

### Ativação do Ambiente
```bash
# Windows
.\nomadix_env\Scripts\Activate.ps1

# macOS/Linux
source nomadix_env/bin/activate
```

### Execução da Aplicação
```bash
# Versão principal (recomendada)
streamlit run run_simple.py

# Versão alternativa (sem PyArrow)
streamlit run nomadix_no_pyarrow.py

# Com acesso remoto
streamlit run run_simple.py --server.address 0.0.0.0

# Porta específica
streamlit run run_simple.py --server.port 8080
```

### Verificações
```bash
# Status das dependências
python -c "import streamlit, pandas, plotly; print('OK!')"

# Versões
python --version
streamlit --version
pip list | grep streamlit

# Teste do Streamlit
streamlit hello
```

## 🚨 Resolução Rápida de Problemas

### PyArrow Error
```bash
# Use versão alternativa
streamlit run nomadix_no_pyarrow.py
```

### Command Not Found
```bash
# Execute diretamente com Python
python -m streamlit run run_simple.py
```

### Permission Error
```bash
# Windows: Execute como administrador
# Linux/macOS: Use --user
pip install --user streamlit pandas plotly
```

### Compilation Error
```bash
# Use binários pré-compilados
pip install --only-binary=all pandas numpy
```

## 📊 URLs de Acesso

- **Local:** http://localhost:8501
- **Rede local:** http://192.168.x.x:8501
- **Porta alternativa:** http://localhost:8080

## 🔄 Manutenção

### Atualizar Dependências
```bash
pip install --upgrade streamlit pandas plotly
```

### Reinstalar Ambiente
```bash
# Remover ambiente atual
rm -rf nomadix_env  # Linux/macOS
rmdir /s nomadix_env  # Windows

# Recriar
python -m venv nomadix_env
# ... ativar e reinstalar dependências
```

### Backup da Configuração
```bash
# Salvar lista de pacotes
pip freeze > requirements_backup.txt

# Restaurar de backup
pip install -r requirements_backup.txt
```

---

**💡 Dica:** Mantenha este arquivo à mão para referência rápida!