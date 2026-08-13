# ⚙️ Configurações Avançadas - FicaQuietoKalucky

Guia de configurações avançadas para personalizar o bot completamente.

## 🎨 Personalizando Cores

Edite cores nos embeds para corresponder ao tema do seu servidor:

```python
# Cores disponíveis em discord.Color
discord.Color.default()      # Preto
discord.Color.white()        # Branco
discord.Color.blurple()      # Roxo Discord
discord.Color.greyple()      # Cinza
discord.Color.dark_grey()    # Cinza escuro
discord.Color.light_grey()   # Cinza claro
discord.Color.darker_grey()  # Cinza mais escuro
discord.Color.red()          # Vermelho
discord.Color.green()        # Verde
discord.Color.blue()         # Azul
discord.Color.gold()         # Ouro
discord.Color.orange()       # Laranja
discord.Color.purple()       # Roxo
discord.Color.magenta()      # Magenta
discord.Color.teal()         # Azul-verde
discord.Color.cyan()         # Ciano
discord.Color.pink()         # Rosa
```

### Exemplo: Cores Customizadas

```python
embed = discord.Embed(
    title="Título",
    color=discord.Color.from_rgb(255, 100, 50)  # RGB customizado
)
```

## 📝 Personalizando Mensagens

### Adicionar Thumbnails

```python
embed.set_thumbnail(url="https://exemplo.com/imagem.png")
```

### Adicionar Imagens

```python
embed.set_image(url="https://exemplo.com/imagem.png")
```

### Footer Customizado

```python
embed.set_footer(text="Rodapé", icon_url="https://exemplo.com/icon.png")
```

### Author Customizado

```python
embed.set_author(name="Autor", url="https://discord.com", icon_url="https://exemplo.com/icon.png")
```

## 🔐 Configuração de Roles Hierárquicas

### Sistema de Níveis Complexo

```python
ROLE_HIERARCHY = {
    "dono": 100,
    "mod": 80,
    "officer": 60,
    "premium": 40,
    "jogador": 20,
    "trial": 10
}

async def get_role_level(member):
    """Retorna o nível do membro"""
    for role in member.roles:
        if role.name in ROLE_HIERARCHY:
            return ROLE_HIERARCHY[role.name]
    return 0
```

## 🎯 Filtros Avançados

### Mover Apenas Membros Online

```python
async def move_online_members(guild, role, destination):
    members = await RoleManager.get_members_by_role(guild, role)
    online_members = [m for m in members if m.status != discord.Status.offline]
    
    for member in online_members:
        await VoiceManager.move_member(member, destination)
```

### Mover Apenas Membros em um Canal Específico

```python
async def move_from_specific_channel(guild, role, source_channel, destination):
    members = await RoleManager.get_members_by_role(guild, role)
    
    for member in members:
        if member.voice and member.voice.channel == source_channel:
            await VoiceManager.move_member(member, destination)
```

## 📊 Sistema de Eventos Customizados

### Rastrear Movimentações

```python
import json
from datetime import datetime

class MovementLogger:
    def __init__(self):
        self.movements = []
    
    def log_movement(self, member, source, destination, timestamp=None):
        self.movements.append({
            "member": str(member),
            "source": source,
            "destination": destination,
            "timestamp": timestamp or datetime.now().isoformat()
        })
        self.save()
    
    def save(self):
        with open("movements.json", "w") as f:
            json.dump(self.movements, f, indent=4)
    
    def get_today_movements(self):
        today = datetime.now().date()
        return [m for m in self.movements 
                if datetime.fromisoformat(m["timestamp"]).date() == today]
```

### Usar no Cog

```python
logger = MovementLogger()

@commands.command(name="mover")
async def move_members(self, ctx, role_name, destination_name):
    role = await RoleManager.get_role_by_name(ctx.guild, role_name)
    destination = await VoiceManager.get_voice_channel_by_name(ctx.guild, destination_name)
    
    members = await RoleManager.get_members_by_role(ctx.guild, role)
    
    for member in members:
        success = await VoiceManager.move_member(member, destination)
        if success:
            logger.log_movement(member, member.voice.channel.name if member.voice else "Desconectado", destination.name)
```

## 🔔 Notificações Avançadas

### Notificar Admins de Ações

```python
async def notify_admins(guild, title, description):
    admins = [m for m in guild.members if m.guild_permissions.administrator]
    
    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.red()
    )
    
    for admin in admins:
        try:
            await admin.send(embed=embed)
        except discord.Forbidden:
            pass
```

### Enviar Relatório Diário

```python
from discord.ext import tasks

class ReportCog(commands.Cog):
    def __init__(self, bot, movement_logger):
        self.bot = bot
        self.logger = movement_logger
        self.daily_report.start()
    
    @tasks.loop(hours=24)
    async def daily_report(self):
        movements = self.logger.get_today_movements()
        
        embed = discord.Embed(
            title="📊 Relatório Diário",
            description=f"Total de movimentações: {len(movements)}",
            color=discord.Color.blue()
        )
        
        # Enviar para um canal específico
        channel = self.bot.get_channel(CHANNEL_ID)
        await channel.send(embed=embed)
```

## 🎮 Automação de Filas

### Sistema de Fila Automática

```python
class QueueManager:
    def __init__(self):
        self.queues = {}
    
    def create_queue(self, name, max_size=10):
        self.queues[name] = {
            "members": [],
            "max_size": max_size
        }
    
    def add_to_queue(self, queue_name, member):
        if queue_name in self.queues:
            queue = self.queues[queue_name]
            if len(queue["members"]) < queue["max_size"]:
                queue["members"].append(member)
                return True
        return False
    
    def get_queue_position(self, queue_name, member):
        if queue_name in self.queues:
            try:
                return self.queues[queue_name]["members"].index(member) + 1
            except ValueError:
                return -1
        return -1
```

## 🔐 Sistema de Permissões Customizado

### Permissões por Cargo

```python
COMMAND_PERMISSIONS = {
    "mover": ["officer", "dono"],
    "listar_cargos": ["officer", "dono"],
    "status": ["dono"]
}

async def check_command_permission(member, command_name):
    if command_name not in COMMAND_PERMISSIONS:
        return True
    
    required_roles = COMMAND_PERMISSIONS[command_name]
    member_roles = [role.name for role in member.roles]
    
    return any(role in member_roles for role in required_roles)

# Usar como decorator
def require_permission(command_name):
    async def predicate(ctx):
        return await check_command_permission(ctx.author, command_name)
    return commands.check(predicate)
```

### Usar o Decorator

```python
@commands.command(name="mover")
@require_permission("mover")
async def move_members(self, ctx, ...):
    pass
```

## 📈 Dashboard Web (Opcional)

### Estrutura com Flask

```python
from flask import Flask, render_template
import json

app = Flask(__name__)

class BotDashboard:
    def __init__(self, bot, movement_logger):
        self.bot = bot
        self.logger = movement_logger
    
    @app.route('/stats')
    def get_stats(self):
        return {
            "bot_online": self.bot.is_closed() == False,
            "total_movements": len(self.logger.movements),
            "today_movements": len(self.logger.get_today_movements())
        }
    
    @app.route('/movements')
    def get_movements(self):
        return json.dumps(self.logger.movements)
```

## 🔄 Integração com Banco de Dados

### Usando SQLite

```python
import sqlite3

class BotDatabase:
    def __init__(self, db_name="bot.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS movements (
                id INTEGER PRIMARY KEY,
                member_id INTEGER,
                member_name TEXT,
                source_channel TEXT,
                destination_channel TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()
    
    def log_movement(self, member_id, member_name, source, destination):
        self.cursor.execute("""
            INSERT INTO movements (member_id, member_name, source_channel, destination_channel)
            VALUES (?, ?, ?, ?)
        """, (member_id, member_name, source, destination))
        self.conn.commit()
    
    def get_member_movements(self, member_id):
        self.cursor.execute(
            "SELECT * FROM movements WHERE member_id = ?",
            (member_id,)
        )
        return self.cursor.fetchall()
```

## 🌍 Internacionalização (i18n)

### Sistema Multi-idioma

```python
MENSAGENS = {
    "pt": {
        "bot_online": "✅ Bot conectado como {name}",
        "acesso_negado": "❌ Acesso Negado",
        "cargo_nao_encontrado": "❌ Cargo não encontrado"
    },
    "en": {
        "bot_online": "✅ Bot connected as {name}",
        "acesso_negado": "❌ Access Denied",
        "cargo_nao_encontrado": "❌ Role not found"
    }
}

def get_message(key, lang="pt", **kwargs):
    msg = MENSAGENS.get(lang, MENSAGENS["pt"]).get(key, key)
    return msg.format(**kwargs) if kwargs else msg
```

## 📦 Versionamento do Bot

### Gerenciar Versões

```python
# bot/version.py
VERSION = "1.0.0"
CHANGELOG = """
v1.0.0 - 2024-01-01
- Lançamento inicial
- Sistema de movimentação
- Comandos de administração

v0.9.0 - 2023-12-15
- Beta testing
"""

# Usar no comando
@commands.command(name="versao")
async def bot_version(self, ctx):
    from version import VERSION
    embed = discord.Embed(
        title=f"Versão: {VERSION}",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)
```

---

**Com essas configurações avançadas, seu bot se torna super poderoso! 🚀**
