import discord
from discord.ext import commands
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import CommandValidator, RoleManager, VoiceManager

logger = logging.getLogger(__name__)


class AdminCog(commands.Cog):
    """Cog para gerenciar funções administrativas do bot"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="status")
    async def status_command(self, ctx):
        """Mostra o status do bot"""
        embed = discord.Embed(
            title="🤖 Status do FicaQuietoKalucky",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="Status", value="✅ Online", inline=False)
        embed.add_field(name="Versão", value="1.0.0", inline=True)
        embed.add_field(name="Servidores", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Latência", value=f"{self.bot.latency * 1000:.0f}ms", inline=True)
        await ctx.send(embed=embed)

    @commands.command(name="ajuda")
    async def help_command(self, ctx):
        """Mostra os comandos disponíveis"""
        embed = discord.Embed(
            title="📖 Comandos do FicaQuietoKalucky",
            color=discord.Color.gold(),
        )

        embed.add_field(
            name="📋 Movimentação",
            value="**!mover** <cargo> <canal>\n"
            "Move todos com um cargo para um canal\n\n"
            "**!mover_officers** <canal>\n"
            "Move todos os officers para um canal\n\n"
            "**!listar_em_voz** <canal>\n"
            "Lista membros em um canal de voz",
            inline=False,
        )

        embed.add_field(
            name="👑 Gerenciamento",
            value="**!listar_cargos**\n"
            "Lista todos os cargos do servidor\n\n"
            "**!listar_canais**\n"
            "Lista todos os canais de voz",
            inline=False,
        )

        embed.add_field(
            name="⚙️ Sistema",
            value="**!status**\n"
            "Mostra o status do bot\n\n"
            "**!ajuda**\n"
            "Mostra essa mensagem",
            inline=False,
        )

        embed.set_footer(text="Use !<comando> para mais informações")
        await ctx.send(embed=embed)

    @commands.command(name="listar_cargos")
    @commands.guild_only()
    async def list_roles(self, ctx):
        """Lista todos os cargos do servidor"""
        if not await CommandValidator.validate_admin(ctx.author):
            embed = discord.Embed(
                title="❌ Acesso Negado",
                description="Você precisa ser administrador para usar este comando.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        roles = ctx.guild.roles
        if not roles:
            embed = discord.Embed(
                title="📭 Nenhum Cargo",
                description="Não há cargos neste servidor.",
                color=discord.Color.blue(),
            )
            await ctx.send(embed=embed)
            return

        role_list = "\n".join([f"• {role.name} ({len(role.members)} membros)" for role in reversed(roles)])
        embed = discord.Embed(
            title="👑 Cargos do Servidor",
            description=role_list,
            color=discord.Color.blue(),
        )
        embed.set_footer(text=f"Total: {len(roles)} cargos")
        await ctx.send(embed=embed)

    @commands.command(name="listar_canais")
    @commands.guild_only()
    async def list_voice_channels(self, ctx):
        """Lista todos os canais de voz do servidor"""
        if not await CommandValidator.validate_admin(ctx.author):
            embed = discord.Embed(
                title="❌ Acesso Negado",
                description="Você precisa ser administrador para usar este comando.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        voice_channels = ctx.guild.voice_channels
        if not voice_channels:
            embed = discord.Embed(
                title="📭 Nenhum Canal de Voz",
                description="Não há canais de voz neste servidor.",
                color=discord.Color.blue(),
            )
            await ctx.send(embed=embed)
            return

        channel_list = "\n".join([f"• {ch.name} ({len(ch.members)} membros)" for ch in voice_channels])
        embed = discord.Embed(
            title="🔊 Canais de Voz",
            description=channel_list,
            color=discord.Color.blue(),
        )
        embed.set_footer(text=f"Total: {len(voice_channels)} canais")
        await ctx.send(embed=embed)

    @commands.command(name="membro_info")
    @commands.guild_only()
    async def member_info(self, ctx, member: discord.Member):
        """Mostra informações sobre um membro"""
        embed = discord.Embed(
            title=f"📋 Informações de {member.name}",
            color=discord.Color.green(),
        )
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="Status", value=member.status, inline=True)
        embed.add_field(
            name="Canal de Voz",
            value=member.voice.channel.name if member.voice else "❌ Offline",
            inline=True,
        )

        roles = ", ".join([role.name for role in member.roles if role.name != "@everyone"])
        embed.add_field(name="Cargos", value=roles or "Nenhum", inline=False)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(AdminCog(bot))
