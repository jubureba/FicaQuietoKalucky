# 📥 Guia de Instalação - PC Novo

Tudo que você precisa para rodar o FicaQuietoKalucky do zero.

## 📋 Pré-requisitos

### 1. Python 3.8+
[Baixe Python](https://www.python.org/downloads/)

**Windows:**
- Baixe o instalador
- ✅ Marque "Add Python to PATH"
- Instale

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**Mac:**
```bash
# Com Homebrew
brew install python3
```

### 2. Git (Opcional, mas recomendado)
[Baixe Git](https://git-scm.com/download/)

## 🚀 Instalação Rápida (5 minutos)

### Passo 1: Clone o Repositório

**Com Git:**
```bash
git clone https://github.com/seu-usuario/FicaQuietoKalucky.git
cd FicaQuietoKalucky
```

**Sem Git:**
1. Vá em: https://github.com/seu-usuario/FicaQuietoKalucky
2. Clique em "Code" → "Download ZIP"
3. Descompacte a pasta
4. Abra terminal/CMD nela

### Passo 2: Crie o Ambiente Virtual

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

✅ Se vir `(venv)` no início da linha, funcionou!

### Passo 3: Instale as Dependências

```bash
pip install -r requirements.txt
```

⏳ Aguarde ~30 segundos (primeira vez é mais lento)

### Passo 4: Configure o Discord Token

**Windows:**
1. Crie arquivo `name.txt`
2. Escreva seu TOKEN do Discord
3. Copie o conteúdo
4. Crie arquivo `.env` (sem nome, só extensão)
5. Cole: `DISCORD_TOKEN=seu_token_aqui`

**Linux/Mac:**
```bash
cp .env.example .env
nano .env  # ou vim, code, etc
# DISCORD_TOKEN=seu_token_aqui
# ADMIN_GUILD_ID=seu_guild_id
```

### Passo 5: Execute o Bot

```bash
python run.py
```

✅ Se vir `✅ Bot conectado como jubutofu#0513` - funcionou!

---

## 🎮 Onde Conseguir os Tokens?

### DISCORD_TOKEN

1. Vá em: https://discord.com/developers/applications
2. Clique em "New Application"
3. Vá para "Bot" → "Add Bot"
4. Em "TOKEN" clique em "Copy"
5. Cole no `.env`

### ADMIN_GUILD_ID

1. Abra Discord
2. Ative "Developer Mode" (Configurações → Avançadas)
3. Clique com **botão direito** no seu servidor
4. "Copiar ID de Servidor"
5. Cole no `.env`

---

## 📝 Arquivo `.env` Completo

```
DISCORD_TOKEN=seu_token_do_bot_aqui
ADMIN_GUILD_ID=seu_guild_id_aqui
PREFIX=!
LOG_LEVEL=INFO
```

---

## ⚙️ Configuração no Discord

### 1. Dar Permissões ao Bot

1. Vá em: https://discord.com/developers/applications
2. Selecione sua aplicação
3. OAuth2 → URL Generator
4. **Scopes:** `bot`
5. **Permissions:**
   - ✅ Send Messages
   - ✅ Embed Links
   - ✅ Manage Channels
   - ✅ Move Members
   - ✅ Read Message History

6. Copie a URL gerada
7. Cole no navegador
8. Autorize

### 2. Criar Cargos (Roles)

No Discord:
1. Configurações do servidor
2. Cargos
3. Novo cargo
4. Nome: `jogador` (ou o que quiser)
5. Novo cargo
6. Nome: `officer`

### 3. Atribuir Cargos

1. Clique direito em um membro
2. "Adicionar Cargo"
3. Escolha o cargo

---

## ✅ Checklist de Instalação

- [ ] Python 3.8+ instalado (`python --version`)
- [ ] Git instalado (opcional) (`git --version`)
- [ ] Repositório clonado/descompactado
- [ ] Virtual environment criado
- [ ] Venv ativado (`(venv)` aparece)
- [ ] Dependências instaladas (`pip list`)
- [ ] `.env` criado com TOKEN e GUILD_ID
- [ ] Bot autorizado no Discord
- [ ] Cargos "jogador" e "officer" criados
- [ ] Bot rodando (`python run.py`)
- [ ] Mensagem "✅ Bot conectado" aparece

---

## 🐛 Problemas Comuns

### "Python not found"

**Solução:**
- Windows: Reinstale marcando "Add Python to PATH"
- Linux: `sudo apt install python3`

### "pip: command not found"

**Solução:**
```bash
# Windows
python -m pip install -r requirements.txt

# Linux
python3 -m pip install -r requirements.txt
```

### "ModuleNotFoundError: No module named 'discord'"

**Solução:**
```bash
# Verifique se venv está ativado
pip install -r requirements.txt
```

### "Token inválido"

**Solução:**
- Regenere o token em: https://discord.com/developers/applications
- Copie novamente no `.env`

### "ADMIN_GUILD_ID inválido"

**Solução:**
- Ative Developer Mode no Discord
- Copie ID do servidor (botão direito)
- Verifique se é um número inteiro

### "Comando não encontrado"

**Solução:**
- Aguarde 30 segundos (carregamento de cogs)
- Verifique se venv está ativado
- Tente `!ajuda`

### Bot desconecta rapidinho

**Solução:**
- Verifique os logs
- Verifique permissões
- Tente `python run.py` novamente

---

## 🔧 Comandos Úteis

```bash
# Ativar venv (sempre primeiro!)
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Desativar venv
deactivate

# Ver versão do Python
python --version

# Ver pacotes instalados
pip list

# Atualizar pip
python -m pip install --upgrade pip

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall

# Rodar bot
python run.py

# Parar bot
Ctrl + C
```

---

## 📂 Estrutura de Pastas Final

```
FicaQuietoKalucky/
├── venv/                 # Virtual environment
├── bot/
│   ├── cogs/
│   ├── utils/
│   ├── data/
│   ├── main.py
│   └── config.py
├── .env                  # ⭐ IMPORTANTE: Criado por você
├── run.py
├── requirements.txt
├── README.md
└── ...
```

---

## 🚀 Próximos Passos

1. **Primeiro Launch:**
   ```bash
   python run.py
   ```

2. **Ir para #painel-controle no Discord**

3. **Clique em ⚙️ Configurações**

4. **Configure:**
   - 👥 Grupo padrão: `jogador`
   - 📍 Canal padrão: `teste-1`
   - 👑 Sala de officers: (cria automático)

5. **Pronto!** Use os botões 🎮 e 👑

---

## 💡 Dicas Extras

### Rodar em Background (Linux/Mac)
```bash
nohup python run.py > bot.log &
```

### Rodar com Screen
```bash
screen -S kalucky
python run.py
# Ctrl+A, depois D para desanexar
```

### Rodar com Systemd (Linux)
Veja [README.md](README.md) seção "Deploy"

### Rodar em Docker
```bash
docker build -t kalucky .
docker run -e DISCORD_TOKEN=seu_token kalucky
```

---

## 📞 Ajuda

- 📖 Leia [README.md](README.md)
- 🐛 Abra [issue no GitHub](https://github.com/seu-usuario/FicaQuietoKalucky/issues)
- 💬 Crie [discussion](https://github.com/seu-usuario/FicaQuietoKalucky/discussions)

---

**Pronto! Seu bot deve estar rodando agora!** 🎉

Qualquer problema, releia este guia ou abra uma issue! ✨
