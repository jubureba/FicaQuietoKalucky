# 🪟 Setup Completo para Windows

Guia passo a passo para instalar FicaQuietoKalucky no Windows.

## ⚠️ Erro: "Visual C++ Build Tools"

Se vir um erro como:
```
error: Microsoft Visual C++ 14.0 or greater is required
```

Não se preocupe! Vou mostrar como resolver.

---

## 🔧 Solução 1: Instalar Build Tools (Rápido - 5 min)

### Opção A: Visual C++ Build Tools (Recomendado)

1. Baixe: [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Execute o instalador
3. Selecione: **"Desktop development with C++"**
4. Clique em **"Install"**
5. Aguarde (vai levar uns 10-15 min)
6. **Reinicie o PC**
7. Tente instalar novamente: `pip install -r requirements.txt`

### Opção B: Visual Studio Community (Completo)

1. Baixe: [Visual Studio Community](https://visualstudio.microsoft.com/vs/community/)
2. Execute o instalador
3. Na primeira tela, selecione:
   - ✅ "Desktop development with C++"
4. Clique em **"Install"**
5. Aguarde (vai levar ~30 min)
6. **Reinicie o PC**
7. Tente instalar novamente

---

## ⚡ Solução 2: Instalar Binários Pré-Compilados (Mais Rápido)

Se não quer compilar, use versões pré-compiladas:

```bash
# 1. Desative o venv
deactivate

# 2. Delete a pasta venv
rmdir /s venv

# 3. Crie novamente
python -m venv venv
venv\Scripts\activate

# 4. Upgrade pip (IMPORTANTE)
python -m pip install --upgrade pip

# 5. Instale os binários
pip install discord.py python-dotenv aiohttp --only-binary :all:
```

---

## ✅ Verificar se Funcionou

```bash
# Ative o venv
venv\Scripts\activate

# Teste import
python -c "import discord; print('OK!')"

# Se vir "OK!" - funcionou!
```

---

## 📋 Instalação Completa Windows (Do Zero)

### 1. Instale Python

1. Baixe: https://www.python.org/downloads/
2. Execute: `python-3.11.x-amd64.exe`
3. **✅ MARQUE: "Add Python to PATH"**
4. Clique em "Install Now"
5. Aguarde

**Verifique:**
```cmd
python --version
```

### 2. Instale Visual C++ Build Tools

1. Baixe: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Execute: `vs_BuildTools.exe`
3. Selecione: **"Desktop development with C++"**
4. Clique em "Install"
5. Aguarde (15-20 min)
6. **Reinicie o PC** ⚠️ IMPORTANTE

### 3. Clone o Repositório

Abra **CMD** ou **PowerShell**:

```cmd
# Acesse a pasta onde quer clonar
cd Desktop

# Clone
git clone https://github.com/seu-usuario/FicaQuietoKalucky.git

# Acesse a pasta
cd FicaQuietoKalucky
```

### 4. Crie Virtual Environment

```cmd
python -m venv venv
```

### 5. Ative o Virtual Environment

**PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**CMD:**
```cmd
venv\Scripts\activate
```

✅ Viu `(venv)` no início? Ótimo!

### 6. Instale Dependências

```cmd
pip install -r requirements.txt
```

⏳ Vai levar ~1 minuto (primeira vez)

### 7. Configure .env

1. Abra a pasta do projeto no **Explorador de Arquivos**
2. Clique em **"New"** → **"Text Document"**
3. Nomeie: `.env` (SIM, com ponto!)
4. Abra com Bloco de Notas
5. Cole:
```
DISCORD_TOKEN=seu_token_aqui
ADMIN_GUILD_ID=seu_guild_id_aqui
PREFIX=!
```
6. Salve (Ctrl+S)

### 8. Execute o Bot

```cmd
python run.py
```

Se vir:
```
✅ Bot conectado como jubutofu#0513
```

**FUNCIONOU!** 🎉

---

## 🆘 Se Ainda Der Erro

### Erro: "Failed building wheel"

```bash
# 1. Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# 2. Tente novamente
pip install -r requirements.txt --no-cache-dir
```

### Erro: "Permission denied"

Abra CMD como **Administrador**:
1. Clique direito no CMD
2. "Run as administrator"
3. Tente novamente

### Erro: "module not found"

```bash
# Verifique se venv está ativado
# (deve ter (venv) no início)

# Se não, ative:
venv\Scripts\activate

# Tente novamente:
pip install -r requirements.txt
```

---

## 🎯 Passo a Passo com Print (Opcional)

Se ainda não funcionou, tente isso:

### A. Apague tudo e comece de novo

```bash
# Desative venv
deactivate

# Delete a pasta venv
rmdir /s venv

# Delete arquivo requirements.lock (se existir)
del requirements.lock
```

### B. Instale manualmente

```bash
# Crie venv novo
python -m venv venv

# Ative
venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Instale um por um
pip install discord.py==2.3.2
pip install python-dotenv==1.0.0
pip install aiohttp==3.9.1
```

Se algum falhar, você saberá qual é.

---

## 💾 Backup de Instalação Offline

Se não tiver internet depois:

```bash
# Salve os pacotes
pip download -r requirements.txt -d ./packages

# Depois instale de:
pip install --no-index --find-links ./packages -r requirements.txt
```

---

## 🚀 Teste Final

Antes de usar, verifique tudo:

```bash
# Ative venv
venv\Scripts\activate

# Verifique Python
python --version

# Verifique Discord.py
python -c "import discord; print(discord.__version__)"

# Verifique dotenv
python -c "from dotenv import load_dotenv; print('OK')"

# Execute o bot
python run.py
```

Se tudo mostrar "OK" ou a versão - **está pronto!**

---

## 📝 Arquivo .env Correto

Crie arquivo chamado: `.env` (SEM extensão)

Conteúdo:
```
DISCORD_TOKEN=MzQ1MjM1MjMmNDUy...SUA_TOKEN_AQUI
ADMIN_GUILD_ID=123456789012345678
PREFIX=!
LOG_LEVEL=INFO
```

---

## ✅ Checklist Final Windows

- [ ] Python 3.8+ instalado
- [ ] Visual C++ Build Tools instalado
- [ ] PC reiniciado
- [ ] Repositório clonado
- [ ] venv criado
- [ ] venv ativado (vê (venv) no início)
- [ ] `pip install -r requirements.txt` funcionou
- [ ] `.env` criado com TOKEN e GUILD_ID
- [ ] `python run.py` conecta o bot

---

## 🎮 Próximo: Configurar Discord

Após bot online:
1. Vá para #painel-controle
2. Clique em ⚙️ Configurações
3. Configure tudo
4. Pronto!

---

## 📞 Ajuda

Se ainda tiver problema:

1. Tire **print do erro** exato
2. Abra **issue no GitHub** com:
   - Print do erro
   - Versão do Windows
   - Versão do Python
   - O que tentou

Vamos resolver! 💪

---

**Boa sorte! Windows foi mais trabalhoso, mas agora tá pronto!** 🎉
