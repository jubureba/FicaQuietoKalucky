import discord
from discord.ext import commands
from discord import ui
import logging
import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import RoleManager, VoiceManager, CommandValidator
from utils.config_manager import ConfigManager

logger = logging.getLogger(__name__)
DELETE_AFTER = 5  # Segundos para deletar mensagens


async def delete_after(message, delay=DELETE_AFTER):
    """Deleta uma mensagem após X segundos"""
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except:
        pass


class PainelView(ui.View):
    """Painel simplificado com apenas 3 botões"""

    def __init__(self, guild, timeout=300):
        super().__init__(timeout=timeout)
        self.guild = guild

    @ui.button(label="🎮 Mover Jogadores", style=discord.ButtonStyle.blurple)
    async def mover_jogadores(self, interaction: discord.Interaction, button: ui.Button):
        """Move jogadores para o canal configurado"""
        if not await CommandValidator.validate_admin(interaction.user):
            await interaction.response.defer()
            embed = discord.Embed(
                title="❌ Acesso Negado",
                description="Você precisa ser administrador!",
                color=discord.Color.red()
            )
            msg = await interaction.followup.send(embed=embed)
            asyncio.create_task(delete_after(msg, 3))
            return

        # Obtém configurações
        default_group = ConfigManager.get_default_group(self.guild.id)
        default_channel = ConfigManager.get_default_channel(self.guild.id)

        if not default_group or not default_channel:
            await interaction.response.defer()
            embed = discord.Embed(
                title="⚠️ Configure Primeiro",
                description="Clique em **⚙️ Configurações**",
                color=discord.Color.orange()
            )
            msg = await interaction.followup.send(embed=embed)
            asyncio.create_task(delete_after(msg, 5))
            return

        # Obtém role e channel
        role = await RoleManager.get_role_by_name(self.guild, default_group)
        channel = await VoiceManager.get_voice_channel_by_name(self.guild, default_channel)

        if not role or not channel:
            await interaction.response.defer()
            embed = discord.Embed(
                title="❌ Erro na Configuração",
                description="Reconfigure em **⚙️ Configurações**",
                color=discord.Color.red()
            )
            msg = await interaction.followup.send(embed=embed)
            asyncio.create_task(delete_after(msg, 5))
            return

        # Executa movimentação
        await interaction.response.defer()
        success, failed = await VoiceManager.move_members_by_role(self.guild, role, channel)

        embed = discord.Embed(
            title="✅ Movimentação Concluída",
            description=f"{success} jogadores movidos para **{default_channel}**",
            color=discord.Color.green()
        )

        msg = await interaction.followup.send(embed=embed)
        asyncio.create_task(delete_after(msg, 5))

        # Log em auditoria
        await self._log_audit(
            "🎮 Jogadores Movidos",
            f"**Admin:** {interaction.user.mention}\n"
            f"**Cargo:** {default_group}\n"
            f"**Destino:** {default_channel}\n"
            f"**Movidos:** {success} | **Falharam:** {failed}",
            discord.Color.blue()
        )

    @ui.button(label="👑 Mover Officers", style=discord.ButtonStyle.success)
    async def mover_officers(self, interaction: discord.Interaction, button: ui.Button):
        """Move officers para o canal específico"""
        if not await CommandValidator.validate_admin(interaction.user):
            await interaction.response.defer()
            embed = discord.Embed(
                title="❌ Acesso Negado",
                description="Você precisa ser administrador!",
                color=discord.Color.red()
            )
            msg = await interaction.followup.send(embed=embed)
            asyncio.create_task(delete_after(msg, 3))
            return

        # Obtém canal de officers
        officers_channel_name = ConfigManager.get_officers_channel(self.guild.id)

        if not officers_channel_name:
            embed = discord.Embed(
                title="⚠️ Configure Officers",
                description="Clique em **⚙️ Configurações**",
                color=discord.Color.orange()
            )
            msg = await interaction.response.send_message(embed=embed)
            asyncio.create_task(delete_after(msg, 5))
            return

        officers_channel = await VoiceManager.get_voice_channel_by_name(
            self.guild, officers_channel_name
        )

        if not officers_channel:
            embed = discord.Embed(
                title="❌ Canal Não Encontrado",
                description="Reconfigure em **⚙️ Configurações**",
                color=discord.Color.red()
            )
            msg = await interaction.response.send_message(embed=embed)
            asyncio.create_task(delete_after(msg, 5))
            return

        # Executa movimentação
        await interaction.response.defer()
        role = discord.utils.get(self.guild.roles, name="officer")

        if not role:
            embed = discord.Embed(
                title="❌ Cargo 'officer' Não Encontrado",
                description="Crie um cargo chamado 'officer'",
                color=discord.Color.red()
            )
            msg = await interaction.followup.send(embed=embed)
            asyncio.create_task(delete_after(msg, 5))
            return

        success, failed = await VoiceManager.move_members_by_role(
            self.guild, role, officers_channel
        )

        embed = discord.Embed(
            title="✅ Officers Movidos",
            description=f"{success} officers movidos para **{officers_channel_name}**",
            color=discord.Color.green()
        )

        msg = await interaction.followup.send(embed=embed)
        asyncio.create_task(delete_after(msg, 5))

        # Log em auditoria
        await self._log_audit(
            "👑 Officers Movidos",
            f"**Admin:** {interaction.user.mention}\n"
            f"**Destino:** {officers_channel_name}\n"
            f"**Movidos:** {success} | **Falharam:** {failed}",
            discord.Color.green()
        )

    @ui.button(label="⚙️ Configurações", style=discord.ButtonStyle.grey)
    async def configuracoes(self, interaction: discord.Interaction, button: ui.Button):
        """Abre o painel completo de configurações"""
        if not await CommandValidator.validate_admin(interaction.user):
            await interaction.response.defer()
            embed = discord.Embed(
                title="❌ Acesso Negado",
                description="Você precisa ser administrador!",
                color=discord.Color.red()
            )
            msg = await interaction.followup.send(embed=embed)
            asyncio.create_task(delete_after(msg, 3))
            return

        from .config import ConfigView

        embed = discord.Embed(
            title="⚙️ Configurações - FicaQuietoKalucky",
            description="Configure tudo aqui",
            color=discord.Color.gold()
        )

        view = ConfigView(self.guild)
        await interaction.response.defer()
        msg = await interaction.followup.send(embed=embed, view=view)
        asyncio.create_task(delete_after(msg, 30))  # 30s para interagir

    async def _log_audit(self, title: str, description: str, color):
        """Registra ação em auditoria"""
        try:
            audit_channel = discord.utils.get(self.guild.text_channels, name="auditoria-bot")
            if audit_channel:
                embed = discord.Embed(
                    title=title,
                    description=description,
                    color=color
                )
                await audit_channel.send(embed=embed)
        except Exception as e:
            logger.error(f"Erro ao registrar auditoria: {e}")


class InteractiveCog(commands.Cog):
    """Sistema interativo com botões"""

    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(InteractiveCog(bot))
