import discord
from discord.ext import commands, tasks
import logging
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import CommandValidator

logger = logging.getLogger(__name__)

CHANNELS_CONFIG = {
    "auditoria": {
        "name": "auditoria-bot",
        "topic": "Log de ações do FicaQuietoKalucky",
        "icon_name": "🔐"
    },
    "painel": {
        "name": "painel-controle",
        "topic": "Painel de controle do FicaQuietoKalucky",
        "icon_name": "🎮"
    }
}


class SetupCog(commands.Cog):
    """Gerencia setup automático do bot"""

    def __init__(self, bot):
        self.bot = bot
        self.panel_message_id = {}  # {guild_id: message_id}
        self.setup_channels.start()

    def cog_unload(self):
        self.setup_channels.cancel()

    @tasks.loop(minutes=5)
    async def setup_channels(self):
        """Verifica e cria canais necessários a cada 5 minutos"""
        for guild in self.bot.guilds:
            await self._ensure_channels(guild)

    @setup_channels.before_loop
    async def before_setup(self):
        await self.bot.wait_until_ready()

    async def refresh_panel_for_guild(self, guild: discord.Guild):
        """Atualiza o painel de um servidor específico sob demanda"""
        channel = discord.utils.get(guild.text_channels, name=CHANNELS_CONFIG["painel"]["name"])
        if channel:
            await self._update_panel(guild, channel)

    async def _ensure_channels(self, guild: discord.Guild):
        """Garante que todos os canais necessários existem"""
        try:
            for channel_type, config in CHANNELS_CONFIG.items():
                channel = discord.utils.get(guild.text_channels, name=config["name"])

                if not channel:
                    # Cria o canal
                    channel = await self._create_channel(guild, config, channel_type)
                else:
                    # Valida permissões
                    await self._setup_permissions(guild, channel)

                # Se for painel, atualiza o painel
                if channel_type == "painel" and channel:
                    await self._update_panel(guild, channel)

        except Exception as e:
            logger.error(f"Erro ao garantir canais em {guild.name}: {e}")

    async def _create_channel(self, guild: discord.Guild, config: dict, channel_type: str = ""):
        """Cria um novo canal com permissões corretas"""
        try:
            # Permissões padrão: apenas bot pode enviar
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(send_messages=False),
                guild.me: discord.PermissionOverwrite(send_messages=True)
            }

            channel = await guild.create_text_channel(
                name=config["name"],
                topic=config["topic"],
                overwrites=overwrites
            )

            logger.info(f"✅ Canal {config['name']} criado em {guild.name}")

            # Envia mensagem inicial apenas se não for o painel (o painel é enviado em _update_panel)
            if channel_type != "painel":
                embed = discord.Embed(
                    title=f"{config['icon_name']} {config['name'].upper()}",
                    description=config["topic"],
                    color=discord.Color.blurple()
                )
                await channel.send(embed=embed)

            return channel
        except Exception as e:
            logger.error(f"Erro ao criar canal {config['name']}: {e}")
            return None

    async def _setup_permissions(self, guild: discord.Guild, channel: discord.TextChannel):
        """Configura permissões do canal"""
        try:
            overwrites = channel.overwrites

            # Garante que @everyone não pode enviar
            if guild.default_role not in overwrites:
                await channel.set_permissions(
                    guild.default_role,
                    send_messages=False
                )

            # Garante que bot pode enviar
            if guild.me not in overwrites:
                await channel.set_permissions(
                    guild.me,
                    send_messages=True
                )

        except Exception as e:
            logger.error(f"Erro ao configurar permissões: {e}")

    async def _update_panel(self, guild: discord.Guild, channel: discord.TextChannel):
        """Atualiza o painel no canal editando a mensagem existente"""
        try:
            from .interactive import PainelView
            from utils.config_manager import ConfigManager

            # Obtém configurações atuais
            config = ConfigManager.load_config(guild.id)
            default_group = config.get("default_group") or "❌ Não configurado"
            default_channel = config.get("default_channel") or "❌ Não configurado"
            officers_role = config.get("officers_role") or "❌ Não configurado"
            officers_channel = config.get("officers_channel") or "❌ Não configurado"

            # Cria painel profissional
            embed = discord.Embed(
                title="🎮 PAINEL DE CONTROLE - FicaQuietoKalucky",
                description="Sistema inteligente de gerenciamento de membros",
                color=discord.Color.blurple()
            )

            # Seção: Status Atual
            embed.add_field(
                name="📊 CONFIGURAÇÃO ATUAL",
                value="─" * 40,
                inline=False
            )
            embed.add_field(
                name="👥 Grupo Padrão",
                value=f"`{default_group}`",
                inline=True
            )
            embed.add_field(
                name="📍 Canal Padrão",
                value=f"`{default_channel}`",
                inline=True
            )
            embed.add_field(
                name="👑 Cargo Officers",
                value=f"`{officers_role}`",
                inline=True
            )
            embed.add_field(
                name="🔊 Canal Officers",
                value=f"`{officers_channel}`",
                inline=True
            )

            # Seção: Ações Disponíveis
            embed.add_field(
                name="⚡ AÇÕES RÁPIDAS",
                value="─" * 40,
                inline=False
            )
            embed.add_field(
                name="🎮 Mover Jogadores",
                value="Move todos do grupo padrão para o canal configurado\n`clique no botão abaixo`",
                inline=False
            )
            embed.add_field(
                name="👑 Mover Officers",
                value="Move todos os officers para a sala configurada\n`clique no botão abaixo`",
                inline=False
            )
            embed.add_field(
                name="⚙️ Configurações",
                value="Altere grupos, canais e cargos de officers\n`clique no botão abaixo`",
                inline=False
            )

            # Seção: Informações
            embed.add_field(
                name="ℹ️ INFORMAÇÕES",
                value=f"📊 Servidor: **{guild.name}**\n"
                      f"👥 Membros: **{guild.member_count}**\n"
                      f"🔊 Canais de Voz: **{len(guild.voice_channels)}**\n"
                      f"👑 Cargos: **{len(guild.roles) - 1}**",
                inline=False
            )

            embed.set_footer(
                text="FicaQuietoKalucky v1.0.0",
                icon_url=guild.icon.url if guild.icon else None
            )
            embed.set_thumbnail(url=guild.icon.url if guild.icon else None)

            view = PainelView(guild)

            # Procura por mensagem existente do painel
            target_message = None
            saved_id = ConfigManager.get_panel_message_id(guild.id) or self.panel_message_id.get(guild.id)
            if saved_id:
                try:
                    target_message = await channel.fetch_message(saved_id)
                except Exception:
                    target_message = None

            if not target_message:
                async for msg in channel.history(limit=20):
                    if msg.author == self.bot.user:
                        target_message = msg
                        break

            if target_message:
                await target_message.edit(embed=embed, view=view)
                panel_id = target_message.id
                logger.info(f"✅ Painel editado/atualizado em {guild.name}")
            else:
                msg = await channel.send(embed=embed, view=view)
                panel_id = msg.id
                logger.info(f"✅ Novo painel criado e enviado em {guild.name}")

            self.panel_message_id[guild.id] = panel_id
            ConfigManager.set_panel_message_id(guild.id, panel_id)

            # Limpa mensagens duplicadas extras do bot se houver
            async for extra_msg in channel.history(limit=20):
                if extra_msg.author == self.bot.user and extra_msg.id != panel_id:
                    try:
                        await extra_msg.delete()
                    except Exception:
                        pass

        except Exception as e:
            logger.error(f"Erro ao atualizar painel: {e}")

    async def log_audit(self, guild: discord.Guild, title: str, description: str, color=discord.Color.blue()):
        """Registra uma ação no canal de auditoria"""
        try:
            channel = discord.utils.get(guild.text_channels, name="auditoria-bot")
            if not channel:
                return

            embed = discord.Embed(
                title=title,
                description=description,
                color=color,
                timestamp=datetime.now()
            )

            await channel.send(embed=embed)

        except Exception as e:
            logger.error(f"Erro ao registrar auditoria: {e}")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        """Chamado quando o bot entra em um novo servidor"""
        logger.info(f"📍 Bot adicionado ao servidor: {guild.name}")
        await self._ensure_channels(guild)

        # Log de auditoria
        await self.log_audit(
            guild,
            "🤖 Bot Iniciado",
            f"FicaQuietoKalucky conectado ao servidor {guild.name}",
            discord.Color.green()
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Valida mensagens nos canais do bot"""
        # Ignora mensagens do bot
        if message.author == self.bot.user:
            return

        # Ignora DMs
        if not message.guild:
            return

        # Bloqueia mensagens em canais do bot
        for config in CHANNELS_CONFIG.values():
            if message.channel.name == config["name"]:
                try:
                    await message.delete()

                    # Manda aviso privado
                    embed = discord.Embed(
                        title="⚠️ Mensagem Deletada",
                        description=f"Você não pode enviar mensagens no canal {message.channel.mention}",
                        color=discord.Color.orange()
                    )
                    await message.author.send(embed=embed)

                except discord.Forbidden:
                    logger.warning(f"Não consegui deletar mensagem em {message.channel.name}")

                return

    @commands.command(name="setup")
    @commands.guild_only()
    async def setup_command(self, ctx):
        """Setup manual dos canais do bot

        Uso: !setup
        """
        if not await CommandValidator.validate_admin(ctx.author):
            embed = discord.Embed(
                title="❌ Acesso Negado",
                description="Você precisa ser administrador",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        # Mostra progresso
        embed = discord.Embed(
            title="⚙️ Configurando FicaQuietoKalucky",
            description="Criando canais necessários...",
            color=discord.Color.blue()
        )
        msg = await ctx.send(embed=embed)

        # Cria/verifica canais
        await self._ensure_channels(ctx.guild)

        # Atualiza mensagem
        embed = discord.Embed(
            title="✅ Setup Completo!",
            description="Todos os canais foram criados com sucesso",
            color=discord.Color.green()
        )
        embed.add_field(
            name="📋 Canais Criados",
            value="• 🔐 auditoria-bot\n• 🎮 painel-controle",
            inline=False
        )
        embed.add_field(
            name="💡 Dica",
            value="Use o painel em <#painel-controle> para mover membros facilmente!",
            inline=False
        )

        await msg.edit(embed=embed)

        # Log auditoria
        await self.log_audit(
            ctx.guild,
            "⚙️ Setup Executado",
            f"{ctx.author.mention} executou setup do bot",
            discord.Color.blue()
        )


async def setup(bot):
    await bot.add_cog(SetupCog(bot))
