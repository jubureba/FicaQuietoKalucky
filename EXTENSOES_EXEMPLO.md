# 🚀 Guia de Extensões - FicaQuietoKalucky

Este guia mostra como adicionar novas funcionalidades ao bot.

## 📐 Estrutura de um Cog

Um Cog é um módulo que contém comandos relacionados. Aqui está a estrutura básica:

```python
import discord
from discord.ext import commands
import logging

logger = logging.getLogger(__name__)


class MeuCog(commands.Cog):
    """Descrição do meu cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="meu_comando")
    async def meu_comando(self, ctx):
        """Descrição do comando"""
        await ctx.send("Mensagem de resposta")


async def setup(bot):
    await bot.add_cog(MeuCog(bot))
```

## 📚 Exemplos de Extensões

### Exemplo 1: Sistema de Lembretes

Crie `bot/cogs/reminders.py`:

```python
import discord
from discord.ext import commands, tasks
from datetime import timedelta
import asyncio

class RemindersCog(commands.Cog):
    """Sistema de lembretes para o servidor"""

    def __init__(self, bot):
        self.bot = bot
        self.reminders = {}

    @commands.command(name="lembrete")
    async def set_reminder(self, ctx, minutos: int, *, mensagem: str):
        """Define um lembrete
        
        Uso: !lembrete 5 Reunião em 5 minutos
        """
        reminder_id = len(self.reminders) + 1
        self.reminders[reminder_id] = {
            "user": ctx.author,
            "message": mensagem,
            "time": minutos
        }

        embed = discord.Embed(
            title="⏰ Lembrete Definido",
            description=f"Você receberá um lembrete em {minutos} minuto(s)",
            color=discord.Color.blue()
        )
        embed.add_field(name="Mensagem", value=mensagem)
        await ctx.send(embed=embed)

        # Aguarda e envia o lembrete
        await asyncio.sleep(minutos * 60)
        
        reminder = self.reminders[reminder_id]
        embed = discord.Embed(
            title="🔔 Seu Lembrete!",
            description=reminder["message"],
            color=discord.Color.gold()
        )
        await reminder["user"].send(embed=embed)

async def setup(bot):
    await bot.add_cog(RemindersCog(bot))
```

### Exemplo 2: Sistema de Estatísticas

Crie `bot/cogs/stats.py`:

```python
import discord
from discord.ext import commands

class StatsCog(commands.Cog):
    """Estatísticas do servidor"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="stats")
    @commands.guild_only()
    async def server_stats(self, ctx):
        """Mostra estatísticas do servidor"""
        guild = ctx.guild
        
        embed = discord.Embed(
            title=f"📊 Estatísticas - {guild.name}",
            color=discord.Color.purple()
        )
        embed.add_field(name="Total de Membros", value=guild.member_count)
        embed.add_field(name="Canais de Texto", value=len(guild.text_channels))
        embed.add_field(name="Canais de Voz", value=len(guild.voice_channels))
        embed.add_field(name="Cargos", value=len(guild.roles))
        embed.add_field(name="Criado em", value=guild.created_at.strftime("%d/%m/%Y"))
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(StatsCog(bot))
```

### Exemplo 3: Sistema de Bem-vindo

Crie `bot/cogs/welcome.py`:

```python
import discord
from discord.ext import commands

class WelcomeCog(commands.Cog):
    """Sistema de boas-vindas"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Chamado quando um novo membro entra"""
        embed = discord.Embed(
            title=f"👋 Bem-vindo(a), {member.name}!",
            description="Leia as regras e se divirta!",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=member.avatar.url)
        
        # Envia para um canal específico (ajuste o ID)
        channel = member.guild.system_channel
        if channel:
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Chamado quando um membro sai"""
        embed = discord.Embed(
            title=f"👋 {member.name} saiu do servidor",
            color=discord.Color.red()
        )
        
        channel = member.guild.system_channel
        if channel:
            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(WelcomeCog(bot))
```

### Exemplo 4: Sistema de Votação

Crie `bot/cogs/voting.py`:

```python
import discord
from discord.ext import commands

class VotingCog(commands.Cog):
    """Sistema de votações"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="votacao")
    async def create_vote(self, ctx, titulo: str, *, opcoes: str):
        """Cria uma votação
        
        Uso: !votacao "Qual jogo?" "Opção 1,Opção 2,Opção 3"
        """
        opcoes_list = [op.strip() for op in opcoes.split(",")]
        
        embed = discord.Embed(
            title=f"🗳️ {titulo}",
            color=discord.Color.blue()
        )
        
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
        
        for i, opcao in enumerate(opcoes_list):
            embed.add_field(name=f"{emojis[i]} {opcao}", value="​", inline=False)
        
        mensagem = await ctx.send(embed=embed)
        
        for i in range(len(opcoes_list)):
            await mensagem.add_reaction(emojis[i])

async def setup(bot):
    await bot.add_cog(VotingCog(bot))
```

## 🔄 Ciclo de Vida dos Cogs

### Listeners (Ouvintes de Eventos)

```python
@commands.Cog.listener()
async def on_message(self, message):
    """Chamado toda vez que uma mensagem é enviada"""
    if message.author == self.bot.user:
        return
    
    if message.content.startswith("oi"):
        await message.channel.send(f"Olá, {message.author.name}!")

@commands.Cog.listener()
async def on_ready():
    """Chamado quando o bot se conecta"""
    print("Bot pronto!")

@commands.Cog.listener()
async def on_member_update(self, before, after):
    """Chamado quando um membro é atualizado"""
    if before.roles != after.roles:
        print(f"{after.name} teve seus cargos atualizados")
```

## 🎨 Decoradores Úteis

```python
# Apenas em servidores (não em DM)
@commands.guild_only()

# Apenas usuários com permissão específica
@commands.has_permissions(administrator=True)

# Apenas o dono do bot
@commands.is_owner()

# Cooldown (limite de uso)
@commands.cooldown(1, 5, commands.BucketType.user)  # 1 uso a cada 5 segundos por usuário

# Requer um cargo específico
@commands.has_role("Admin")
```

## 📦 Salvando Dados (JSON)

```python
import json
import os

class DataCog(commands.Cog):
    """Exemplo de salvamento de dados"""

    def __init__(self, bot):
        self.bot = bot
        self.data_file = "data.json"
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def save_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.data, f, indent=4)

    @commands.command(name="salvar")
    async def save_info(self, ctx, chave: str, *, valor: str):
        """Salva uma informação"""
        self.data[chave] = valor
        self.save_data()
        await ctx.send(f"✅ Salvo: {chave} = {valor}")

async def setup(bot):
    await bot.add_cog(DataCog(bot))
```

## ⏰ Tasks (Tarefas Recorrentes)

```python
from discord.ext import tasks

class TasksCog(commands.Cog):
    """Tarefas que rodamrecorrentemente"""

    def __init__(self, bot):
        self.bot = bot
        self.tarefa_recorrente.start()

    @tasks.loop(minutes=30)
    async def tarefa_recorrente(self):
        """Executa a cada 30 minutos"""
        print("Executando tarefa!")

    @tarefa_recorrente.before_loop
    async def antes_tarefa(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(TasksCog(bot))
```

## 🧪 Testando Extensões

1. Crie o arquivo em `bot/cogs/`
2. Execute `python run.py`
3. O bot carregará automaticamente
4. Teste no Discord

## 📝 Checklist para Novos Cogs

- ✅ Nome do arquivo segue padrão `lowercase_with_underscores.py`
- ✅ Classe herda de `commands.Cog`
- ✅ Função `setup(bot)` está definida
- ✅ Comandos têm descriptions (docstrings)
- ✅ Logging implementado para debug
- ✅ Tratamento de erros apropriado
- ✅ Embeds são usados para respostas visuais

## 🐛 Debug

Para ver logs detalhados, edite o arquivo principal e altere:

```python
logging.basicConfig(level=logging.DEBUG)  # Antes era INFO
```

---

**Parabéns! Agora você sabe como estender o FicaQuietoKalucky! 🎉**
