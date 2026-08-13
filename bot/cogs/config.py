import discord
from discord.ext import commands
from discord import ui
import logging
import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import CommandValidator, RoleManager, VoiceManager
from utils.config_manager import ConfigManager

logger = logging.getLogger(__name__)
DELETE_AFTER = 5


async def delete_after(message, delay=DELETE_AFTER):
    """Deleta uma mensagem após X segundos"""
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except:
        pass


class ConfigView(ui.View):
    """View para configurar o bot"""

    def __init__(self, guild, timeout=300):
        super().__init__(timeout=timeout)
        self.guild = guild

    @ui.button(label="👥 Grupo Padrão", style=discord.ButtonStyle.blurple)
    async def set_default_group(self, interaction: discord.Interaction, button: ui.Button):
        """Define o grupo/cargo padrão"""
        if not await CommandValidator.validate_admin(interaction.user):
            await interaction.response.defer()
            embed = discord.Embed(
                title="❌ Acesso Negado",
                description="Você precisa ser administrador para fazer isso!",
                color=discord.Color.red()
            )
            msg = await interaction.followup.send(embed=embed)
            asyncio.create_task(delete_after(msg, 3))
            return

        # Cria dropdown de cargos
        roles = [r for r in self.guild.roles if r.name != "@everyone"]
        if not roles:
            await interaction.response.defer()
            embed = discord.Embed(
                title="❌ Nenhum Cargo Disponível",
                description="Crie cargos no servidor antes de configurar!",
                color=discord.Color.red()
            )
            msg = await interaction.followup.send(embed=embed)
            asyncio.create_task(delete_after(msg, 5))
            return

        select = ui.Select(
            placeholder="📋 Selecione o cargo padrão",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(
                    label=r.name,
                    value=str(r.id),
                    description=f"{len(r.members)} membros"
                )
                for r in roles
            ]
        )

        async def callback(inter: discord.Interaction):
            role_id = select.values[0]
            role = self.guild.get_role(int(role_id))
            ConfigManager.set_default_group(self.guild.id, role.name)

            await inter.response.defer()
            embed = discord.Embed(
                title="✅ Grupo Padrão Configurado",
                description=f"Grupo padrão definido para: **{role.name}**\n\n"
                            f"👥 Membros com este cargo: **{len(role.members)}**",
                color=discord.Color.green()
            )
            msg = await inter.followup.send(embed=embed)
            asyncio.create_task(delete_after(msg, 5))

        select.callback = callback

        view = ui.View()
        view.add_item(select)

        embed = discord.Embed(
            title="⚙️ Configurar Grupo Padrão",
            description="Escolha qual cargo será movido automaticamente",
            color=discord.Color.blurple()
        )
        embed.add_field(
            name="ℹ️ Informação",
            value="Este cargo será usado no botão **🎮 Mover Jogadores**",
            inline=False
        )
        await interaction.response.defer()
        msg = await interaction.followup.send(embed=embed, view=view)
        asyncio.create_task(delete_after(msg, 30))  # 30s para interagir

    @ui.button(label="📍 Canal Padrão", style=discord.ButtonStyle.blurple)
    async def set_default_channel(self, interaction: discord.Interaction, button: ui.Button):
        """Define o canal padrão"""
        if not await CommandValidator.validate_admin(interaction.user):
            await interaction.response.defer()
            embed = discord.Embed(
                title="❌ Acesso Negado",
                description="Você precisa ser administrador para fazer isso!",
                color=discord.Color.red()
            )
            msg = await interaction.followup.send(embed=embed)
            asyncio.create_task(delete_after(msg, 3))
            return

        # Cria dropdown de canais
        channels = self.guild.voice_channels
        if not channels:
            await interaction.response.defer()
            embed = discord.Embed(
                title="❌ Nenhum Canal de Voz",
                description="Crie canais de voz no servidor antes de configurar!",
                color=discord.Color.red()
            )
            msg = await interaction.followup.send(embed=embed)
            asyncio.create_task(delete_after(msg, 5))
            return

        select = ui.Select(
            placeholder="📍 Selecione o canal padrão",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(
                    label=ch.name,
                    value=str(ch.id),
                    description=f"{len(ch.members)} membros conectados"
                )
                for ch in channels
            ]
        )

        async def callback(inter: discord.Interaction):
            channel_id = select.values[0]
            channel = self.guild.get_channel(int(channel_id))
            ConfigManager.set_default_channel(self.guild.id, channel.name)

            await inter.response.defer()
            embed = discord.Embed(
                title="✅ Canal Padrão Configurado",
                description=f"Canal padrão definido para: **{channel.name}**\n\n"
                            f"👥 Membros conectados: **{len(channel.members)}**",
                color=discord.Color.green()
            )
            msg = await inter.followup.send(embed=embed)
            asyncio.create_task(delete_after(msg, 5))

        select.callback = callback

        view = ui.View()
        view.add_item(select)

        embed = discord.Embed(
            title="📍 Configurar Canal Padrão",
            description="Escolha para qual canal os jogadores serão movidos",
            color=discord.Color.blurple()
        )
        embed.add_field(
            name="ℹ️ Informação",
            value="Este canal será usado no botão **🎮 Mover Jogadores**",
            inline=False
        )
        await interaction.response.defer()
        msg = await interaction.followup.send(embed=embed, view=view)
        asyncio.create_task(delete_after(msg, 30))  # 30s para interagir

    @ui.button(label="👑 Sala de Officers", style=discord.ButtonStyle.success)
    async def set_officers_channel(self, interaction: discord.Interaction, button: ui.Button):
        """Define o canal exclusivo de officers"""
        if not await CommandValidator.validate_admin(interaction.user):
            await interaction.response.defer()
            embed = discord.Embed(
                title="❌ Acesso Negado",
                description="Você precisa ser administrador para fazer isso!",
                color=discord.Color.red()
            )
            msg = await interaction.followup.send(embed=embed)
            asyncio.create_task(delete_after(msg, 3))
            return

        await interaction.response.defer()

        # Procura ou cria canal de officers
        channel = discord.utils.get(self.guild.voice_channels, name="sala-officers")

        if not channel:
            try:
                # Cria canal de officers
                overwrites = {
                    self.guild.default_role: discord.PermissionOverwrite(connect=False),
                    self.guild.me: discord.PermissionOverwrite(connect=True, manage_channels=True)
                }

                # Encontra o cargo de officer
                officer_role = discord.utils.get(self.guild.roles, name="officer")
                if officer_role:
                    overwrites[officer_role] = discord.PermissionOverwrite(connect=True)

                channel = await self.guild.create_voice_channel(
                    name="sala-officers",
                    overwrites=overwrites
                )
                logger.info(f"✅ Canal 'sala-officers' criado em {self.guild.name}")

                embed = discord.Embed(
                    title="✅ Canal de Officers Criado",
                    description=f"Canal exclusivo criado com sucesso!\n\n"
                                f"📍 Canal: {channel.mention}\n"
                                f"🔒 Acesso: Apenas Officers\n"
                                f"👥 Membros: **0**",
                    color=discord.Color.green()
                )
            except Exception as e:
                logger.error(f"Erro ao criar canal: {e}")
                embed = discord.Embed(
                    title="❌ Erro ao Criar Canal",
                    description=f"Não foi possível criar o canal:\n\n`{e}`",
                    color=discord.Color.red()
                )
                msg = await interaction.followup.send(embed=embed)
                asyncio.create_task(delete_after(msg, 5))
                return
        else:
            embed = discord.Embed(
                title="✅ Canal de Officers Já Existe",
                description=f"Canal já configurado!\n\n"
                            f"📍 Canal: {channel.mention}\n"
                            f"👥 Membros conectados: **{len(channel.members)}**",
                color=discord.Color.blue()
            )

        ConfigManager.set_officers_channel(self.guild.id, channel.name)
        msg = await interaction.followup.send(embed=embed)
        asyncio.create_task(delete_after(msg, 5))

    @ui.button(label="📊 Ver Configuração", style=discord.ButtonStyle.secondary)
    async def view_config(self, interaction: discord.Interaction, button: ui.Button):
        """Mostra a configuração atual"""
        config = ConfigManager.load_config(self.guild.id)

        default_group = config.get("default_group")
        default_channel = config.get("default_channel")
        officers_channel = config.get("officers_channel")

        # Obter informações adicionais
        group_role = discord.utils.get(self.guild.roles, name=default_group) if default_group else None
        default_ch = discord.utils.get(self.guild.voice_channels, name=default_channel) if default_channel else None
        officers_ch = discord.utils.get(self.guild.voice_channels, name=officers_channel) if officers_channel else None

        embed = discord.Embed(
            title="📊 CONFIGURAÇÃO ATUAL",
            description="Status de todos os parâmetros",
            color=discord.Color.blue()
        )

        # Grupo Padrão
        if default_group and group_role:
            embed.add_field(
                name="👥 Grupo Padrão",
                value=f"✅ **{default_group}**\n"
                      f"Membros: **{len(group_role.members)}**",
                inline=True
            )
        else:
            embed.add_field(
                name="👥 Grupo Padrão",
                value="❌ Não configurado",
                inline=True
            )

        # Canal Padrão
        if default_channel and default_ch:
            embed.add_field(
                name="📍 Canal Padrão",
                value=f"✅ **{default_channel}**\n"
                      f"Conectados: **{len(default_ch.members)}**",
                inline=True
            )
        else:
            embed.add_field(
                name="📍 Canal Padrão",
                value="❌ Não configurado",
                inline=True
            )

        # Canal de Officers
        if officers_channel and officers_ch:
            embed.add_field(
                name="👑 Sala de Officers",
                value=f"✅ **{officers_channel}**\n"
                      f"Conectados: **{len(officers_ch.members)}**",
                inline=True
            )
        else:
            embed.add_field(
                name="👑 Sala de Officers",
                value="❌ Não configurado",
                inline=True
            )

        embed.add_field(
            name="💡 Dica",
            value="Configure todos os itens para usar os botões de movimentação",
            inline=False
        )

        await interaction.response.defer()
        msg = await interaction.followup.send(embed=embed)
        asyncio.create_task(delete_after(msg, 8))


class ConfigCog(commands.Cog):
    """Sistema de configuração do bot"""

    def __init__(self, bot):
        self.bot = bot



async def setup(bot):
    await bot.add_cog(ConfigCog(bot))
