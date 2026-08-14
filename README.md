# 🎮 FicaQuietoKalucky

Um bot Discord **completo, profissional e escalável** para gerenciar movimentação de membros entre canais de voz com base em cargos.

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![discord.py 2.3.2](https://img.shields.io/badge/discord.py-2.3.2-blueviolet)](https://github.com/Rapptz/discord.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Características

- ✅ **Interface Intuitiva** - Painel com botões profissionais
- ✅ **Configuração Simples** - Setup em 3 cliques
- ✅ **Gerenciamento de Cargos** - Mova membros por cargo automaticamente
- ✅ **Sistema Scalável** - Arquitetura modular para extensões
- ✅ **Auditoria Completa** - Registra todas as ações
- ✅ **Proteção de Canais** - Canais de bot automáticos e protegidos
- ✅ **Zero Poluição** - Mensagens deletadas automaticamente
- ✅ **Profissional** - Deploy-ready em produção

## 📋 Funcionalidades Principais

### 🎮 Painel de Controle
- **Mover Jogadores** - Move todos do grupo padrão em 1 clique
- **Mover Officers** - Move officers para sua sala exclusiva
- **Configurações** - Personalize todos os parâmetros

### ⚙️ Configuração
- Defina o **grupo padrão** (qual cargo será movido)
- Escolha o **canal padrão** (para onde mover)
- Configure a **sala de officers** (criada automaticamente)

### 📊 Recursos Automáticos
- **Painel Auto-Atualizado** - A cada 5 minutos
- **Canal de Auditoria** - Log de todas as ações
- **Canais Protegidos** - Apenas o bot pode enviar
- **Configurações Persistentes** - Salvas em JSON

## 🚀 Quick Start

### Requisitos
- Python 3.8+
- pip ou poetry
- Token do Discord

### 1. Clone o Repositório

```bash
git clone https://github.com/seu-usuario/FicaQuietoKalucky.git
cd FicaQuietoKalucky
```

### 2. Configure o Ambiente

```bash
# Crie virtual environment
python -m venv venv

# Ative o venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale dependências
pip install -r requirements.txt
```

### 3. Configure o Discord

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite com seus dados
# .env
DISCORD_TOKEN=seu_token_aqui
ADMIN_GUILD_ID=seu_guild_id_aqui
```

### 4. Execute o Bot

```bash
python run.py
```

## 📖 Uso

### Primeira Vez
1. Bot cria **2 canais automáticos**:
   - 🔐 `auditoria-bot` - Log de ações
   - 🎮 `painel-controle` - Painel principal com botões interativos

2. Clique em **⚙️ Configurações** no painel
3. Configure:
   - 👥 Grupo padrão (ex: "jogador")
   - 📍 Canal padrão (ex: "sala-1")
   - 👑 Cargo de officers (ex: "officer" ou qualquer cargo do servidor)
   - 🔊 Canal de officers (ex: "sala-officers" ou qualquer canal de voz)

### Uso Diário
1. Vá para `#painel-controle`
2. Clique em:
   - 🎮 **Mover Jogadores** - Move para canal configurado
   - 👑 **Mover Officers** - Move para sala de officers
   - ⚙️ **Configurações** - Altere settings

## 🏗️ Arquitetura

```
FicaQuietoKalucky/
├── bot/
│   ├── cogs/              # Comandos modulares
│   │   ├── admin.py       # Comandos admin
│   │   ├── config.py      # Sistema de config
│   │   ├── interactive.py # Painel interativo
│   │   └── setup.py       # Setup automático
│   ├── utils/             # Utilitários
│   │   ├── helpers.py     # Funções auxiliares
│   │   └── config_manager.py  # Gerenciar configs
│   ├── data/              # Dados persistentes
│   ├── main.py            # Bot principal
│   ├── config.py          # Configurações
│   └── __init__.py
├── run.py                 # Inicialização
├── requirements.txt       # Dependências
├── .env.example          # Template de env
└── README.md             # Documentação
```

## 🔧 Desenvolvendo

### Adicionar um Novo Comando

Crie `bot/cogs/seu_cog.py`:

```python
import discord
from discord.ext import commands

class SeuCog(commands.Cog):
    """Seu novo cog"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="seu_comando")
    async def seu_comando(self, ctx):
        """Descrição do comando"""
        await ctx.send("Oi! 👋")

async def setup(bot):
    await bot.add_cog(SeuCog(bot))
```

O bot carregará automaticamente!

### Estrutura de um Cog

```python
from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

class MeuCog(commands.Cog):
    """Descrição clara"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="comando")
    async def comando(self, ctx):
        """O que faz"""
        pass
    
    @commands.Cog.listener()
    async def on_ready(self):
        """Listener para evento"""
        logger.info("Bot pronto!")

async def setup(bot):
    await bot.add_cog(MeuCog(bot))
```

## 📦 Dependências

```
discord.py==2.3.2      # Bot do Discord
python-dotenv==1.0.0   # Variáveis de ambiente
aiohttp==3.9.1         # Requisições async
```

## 🔐 Segurança

- ✅ Token em `.env` (nunca no código)
- ✅ Arquivo `.env` no `.gitignore`
- ✅ Validação de permissões
- ✅ Proteção de canais
- ✅ Sem armazenamento de dados sensíveis

## 📊 Monitoramento

### Logs
```bash
tail -f bot.log
```

### Auditoria
- Todas as ações registradas em `#auditoria-bot`
- Timestamp automático
- Identifica o admin que executou

## 🚀 Deploy

### Opção 1: Replit
```bash
git clone https://github.com/seu-usuario/FicaQuietoKalucky.git
# Configure .env
python run.py
```

### Opção 2: Railway
```bash
railway link
railway up
```

### Opção 3: Servidor Linux
```bash
# Setup
git clone ...
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Systemd service
sudo nano /etc/systemd/system/kalucky.service
# [Unit]
# Description=FicaQuietoKalucky
# After=network.target
#
# [Service]
# Type=simple
# User=seu-usuario
# WorkingDirectory=/home/seu-usuario/FicaQuietoKalucky
# ExecStart=/home/seu-usuario/FicaQuietoKalucky/venv/bin/python run.py
# Restart=always
#
# [Install]
# WantedBy=multi-user.target

sudo systemctl enable kalucky
sudo systemctl start kalucky
```

## 🐛 Troubleshooting

### Bot não conecta
- ✅ Verifique o token em `.env`
- ✅ Verifique a conexão com a internet
- ✅ Verifique se o token não expirou

### Sem permissão para criar canais
- ✅ Dê permission "Manage Channels" ao bot
- ✅ Verifique hierarquia de cargos

### Não consegue mover membros
- ✅ Configure o grupo e canal em ⚙️
- ✅ Verifique se o cargo existe
- ✅ Verifique se o canal de voz existe

## 📝 Licença

MIT License - Veja [LICENSE](LICENSE)

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md)

### Passos
1. Fork o repo
2. Crie uma branch (`git checkout -b feature/sua-feature`)
3. Commit (`git commit -m 'Add sua-feature'`)
4. Push (`git push origin feature/sua-feature`)
5. Abra um Pull Request

## 📞 Suporte

- 📖 Leia a [documentação completa](docs/)
- 🐛 Abra uma [issue](https://github.com/seu-usuario/FicaQuietoKalucky/issues)
- 💬 Discussões no GitHub

## 🎯 Roadmap

- [ ] Comandos slash commands
- [ ] Dashboard web
- [ ] Integração com banco de dados
- [ ] Sistema de permissões avançado
- [ ] Agendamento de movimentações
- [ ] Suporte a múltiplos idiomas

## ⭐ Agradecimentos

- [discord.py](https://github.com/Rapptz/discord.py) - Biblioteca principal
- Comunidade Discord

---

**Feito com ❤️ para Discord**

FicaQuietoKalucky v1.0.0 | 2024
