# 🔍 Troubleshooting - Nomadix

## 🚨 Problemas Mais Comuns e Soluções

### 1. Erro: "ModuleNotFoundError: No module named 'streamlit'"

**Causa:** Streamlit não instalado ou ambiente virtual não ativado.

**Soluções:**
```bash
# Verificar se ambiente virtual está ativo
# Deve aparecer (nomadix_env) no prompt

# Windows
.\nomadix_env\Scripts\Activate.ps1

# macOS/Linux
source nomadix_env/bin/activate

# Reinstalar Streamlit
pip install streamlit
```

### 2. Erro: "No module named 'pyarrow'"

**Causa:** PyArrow não instalado (dependência do Streamlit para dataframes).

**Soluções:**
```bash
# Solução 1: Usar versão sem PyArrow (RECOMENDADA)
streamlit run nomadix_no_pyarrow.py

# Solução 2: Tentar instalar PyArrow
pip install pyarrow

# Solução 3: Instalar versão específica
pip install pyarrow==10.0.0
```

### 3. Erro: "streamlit: command not found"

**Causa:** Streamlit não está no PATH do sistema.

**Soluções:**
```bash
# Solução 1: Executar com Python
python -m streamlit run run_simple.py

# Solução 2: Adicionar ao PATH (Windows)
$env:PATH += ";C:\Users\[USUARIO]\AppData\Roaming\Python\Python311\Scripts"

# Solução 3: Instalar para usuário
pip install --user streamlit
```

### 4. Erro de Compilação (Windows)

**Erro típico:** "error: Microsoft Visual C++ 14.0 is required"

**Soluções:**
```bash
# Solução 1: Usar binários pré-compilados
pip install --only-binary=all pandas numpy scikit-learn

# Solução 2: Instalar Visual C++ Build Tools
# Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Solução 3: Usar conda
conda install pandas numpy scikit-learn streamlit
```

### 5. Aplicação Não Abre no Navegador

**Sintomas:** Streamlit inicia mas navegador não abre.

**Soluções:**
```bash
# 1. Acessar manualmente
# Abra: http://localhost:8501

# 2. Verificar porta em uso
netstat -an | findstr :8501  # Windows
lsof -i :8501               # macOS/Linux

# 3. Usar porta diferente
streamlit run run_simple.py --server.port 8080

# 4. Desabilitar auto-abertura do navegador
streamlit run run_simple.py --server.headless true
```

### 6. Erro: "Address already in use"

**Causa:** Porta 8501 já está sendo usada.

**Soluções:**
```bash
# Usar porta diferente
streamlit run run_simple.py --server.port 8502

# Encontrar e finalizar processo usando a porta
# Windows
netstat -ano | findstr :8501
taskkill /PID [NUMERO_PID] /F

# Linux/macOS
lsof -ti:8501 | xargs kill -9
```

### 7. Tabela HTML Não Renderiza

**Sintomas:** Código HTML aparece como texto.

**Solução:**
```bash
# Use a versão corrigida
streamlit run run_simple.py
# Esta versão usa componentes nativos do Streamlit
```

### 8. Gráficos Plotly Não Aparecem

**Causa:** Plotly não instalado ou versão incompatível.

**Soluções:**
```bash
# Reinstalar Plotly
pip uninstall plotly
pip install plotly

# Verificar versão
python -c "import plotly; print(plotly.__version__)"

# Usar versão específica
pip install plotly==5.18.0
```

### 9. Erro de Permissão (Linux/macOS)

**Erro:** "Permission denied" ao instalar pacotes.

**Soluções:**
```bash
# Usar --user (preferível)
pip install --user streamlit pandas plotly

# Usar sudo (cuidado!)
sudo pip3 install streamlit pandas plotly

# Verificar permissões da pasta
ls -la nomadix_env/
chmod +x nomadix_env/bin/activate
```

### 10. Ambiente Virtual Não Ativa (Windows)

**Erro:** "execution of scripts is disabled on this system"

**Solução:**
```powershell
# Alterar política de execução
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Ou executar diretamente
.\nomadix_env\Scripts\python.exe -m streamlit run run_simple.py
```

---

## 🔍 Diagnósticos Úteis

### Verificar Sistema
```bash
# Informações do sistema
python -c "import platform; print(platform.platform())"

# Versão Python
python --version

# Localização do Python
which python     # Linux/macOS
where python     # Windows
```

### Verificar Dependências
```bash
# Listar pacotes instalados
pip list

# Verificar pacotes específicos
pip show streamlit
pip show pandas
pip show plotly

# Testar importações
python -c "
try:
    import streamlit
    print('Streamlit: OK')
except:
    print('Streamlit: ERRO')

try:
    import pandas
    print('Pandas: OK')
except:
    print('Pandas: ERRO')

try:
    import plotly
    print('Plotly: OK')
except:
    print('Plotly: ERRO')
"
```

### Verificar Streamlit
```bash
# Informações do Streamlit
streamlit --version
streamlit config show

# Diagnóstico completo
python -m streamlit doctor

# Teste do Streamlit
streamlit hello
```

---

## 📝 Log de Erros Comuns

### Registro de Problemas e Soluções

| Erro | Causa | Solução Aplicada |
|------|-------|------------------|
| PyArrow missing | Dependência complexa | Usar `nomadix_no_pyarrow.py` |
| Command not found | PATH incorreto | `python -m streamlit run` |
| Compilation error | Falta Visual C++ | `--only-binary=all` |
| Port in use | Streamlit já rodando | `--server.port 8502` |
| Permission denied | Usuário sem privilégios | `pip install --user` |

---

## 💡 Dicas de Prevenção

1. **Sempre use ambiente virtual** - Evita conflitos de dependências
2. **Mantenha backup do requirements.txt** - Para reinstalação rápida
3. **Documente versões funcionais** - Para referência futura
4. **Teste em ambiente limpo** - Antes de deploy em produção
5. **Mantenha logs de instalação** - Para diagnóstico posterior

---

## 🆘 Quando Pedir Ajuda

Se nenhuma solução funcionou, inclua estas informações:

```bash
# Sistema
python -c "import platform; print('Sistema:', platform.platform())"
python --version

# Ambiente
echo "Ambiente ativo: $VIRTUAL_ENV"

# Dependências
pip list | grep -E "streamlit|pandas|plotly"

# Erro completo
# Cole aqui a mensagem de erro completa
```

**Canais de suporte:**
- Documentação Streamlit: https://docs.streamlit.io/
- GitHub Issues: [link do repositório]
- Stack Overflow: tag `streamlit`