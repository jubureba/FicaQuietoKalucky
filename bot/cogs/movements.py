import discord
from discord.ext import commands
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import RoleManager, VoiceManager, CommandValidator
from utils.config_manager import ConfigManager

logger = logging.getLogger(__name__)


class MovementsCog(commands.Cog):
    """Cog para gerenciar movimentação de membros entre canais de voz"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mover")
    @commands.guild_only()
    async def move_members(self, ctx, role_name: str, *, destination_name: str):
        """Move todos os membros com um cargo para um canal de voz específico

        Uso: !mover "jogador" "Fila de Espera"
        """
        # Valida permissão de administrador
        if not await CommandValidator.validate_admin(ctx.author):
            embed = discord.Embed(
                title="❌ Acesso Negado",
                description="Você precisa ser administrador para usar este comando.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        # Obtém o cargo
        role = await RoleManager.get_role_by_name(ctx.guild, role_name)
        if not role:
            embed = discord.Embed(
                title="❌ Cargo não encontrado",
                description=f"O cargo '{role_name}' não existe no servidor.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        # Obtém o canal de destino
        destination = await VoiceManager.get_voice_channel_by_name(ctx.guild, destination_name)
        if not destination:
            embed = discord.Embed(
                title="❌ Canal não encontrado",
                description=f"O canal de voz '{destination_name}' não existe no servidor.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        # Executa a movimentação
        success, failed = await VoiceManager.move_members_by_role(ctx.guild, role, destination)

        # Envia resultado
        embed = discord.Embed(
            title="✅ Movimentação Concluída",
            color=discord.Color.green(),
        )
        embed.add_field(name="Cargo", value=role_name, inline=False)
        embed.add_field(name="Destino", value=destination_name, inline=False)
        embed.add_field(name="✅ Movidos com sucesso", value=success, inline=True)
        embed.add_field(name="❌ Falharam", value=failed, inline=True)

        await ctx.send(embed=embed)

    @commands.command(name="mover_officers")
    @commands.guild_only()
    async def move_officers(self, ctx, *, destination_name: str = None):
        """Move todos os officers para um canal de voz específico

        Uso: !mover_officers "Sala de Officers" (ou apenas !mover_officers se configurado)
        """
        if not await CommandValidator.validate_admin(ctx.author):
            embed = discord.Embed(
                title="❌ Acesso Negado",
                description="Você precisa ser administrador para usar este comando.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        role_name = ConfigManager.get_officers_role(ctx.guild.id) or "officer"
        role = await RoleManager.get_role_by_name(ctx.guild, role_name)
        if not role:
            embed = discord.Embed(
                title="❌ Cargo não encontrado",
                description=f"O cargo '{role_name}' não existe no servidor. Configure pelo painel.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        dest_name = destination_name or ConfigManager.get_officers_channel(ctx.guild.id)
        if not dest_name:
            embed = discord.Embed(
                title="❌ Canal de destino não informado",
                description="Informe o canal de destino ou configure no painel.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        destination = await VoiceManager.get_voice_channel_by_name(ctx.guild, dest_name)
        if not destination:
            embed = discord.Embed(
                title="❌ Canal não encontrado",
                description=f"O canal de voz '{dest_name}' não existe no servidor.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        success, failed = await VoiceManager.move_members_by_role(ctx.guild, role, destination)

        embed = discord.Embed(
            title="✅ Officers Movidos",
            color=discord.Color.green(),
        )
        embed.add_field(name="Cargo", value=role_name, inline=False)
        embed.add_field(name="Destino", value=dest_name, inline=False)
        embed.add_field(name="✅ Movidos", value=success, inline=True)
        embed.add_field(name="❌ Falharam", value=failed, inline=True)

        await ctx.send(embed=embed)

    @commands.command(name="listar_em_voz")
    @commands.guild_only()
    async def list_voice_members(self, ctx, *, channel_name: str):
        """Lista todos os membros em um canal de voz

        Uso: !listar_em_voz "Fila de Espera"
        """
        channel = await VoiceManager.get_voice_channel_by_name(ctx.guild, channel_name)
        if not channel:
            embed = discord.Embed(
                title="❌ Canal não encontrado",
                description=f"O canal de voz '{channel_name}' não existe.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        members = channel.members
        if not members:
            embed = discord.Embed(
                title="📭 Canal Vazio",
                description=f"Nenhum membro em '{channel_name}'.",
                color=discord.Color.blue(),
            )
            await ctx.send(embed=embed)
            return

        member_list = "\n".join([f"• {member.name}" for member in members])
        embed = discord.Embed(
            title=f"👥 Membros em {channel_name}",
            description=member_list,
            color=discord.Color.blue(),
        )
        embed.set_footer(text=f"Total: {len(members)} membros")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(MovementsCog(bot))
