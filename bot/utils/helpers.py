import discord
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


class RoleManager:
    """Gerencia operações com cargos"""

    @staticmethod
    async def get_role_by_name(guild: discord.Guild, role_name: str) -> Optional[discord.Role]:
        """Obtém um cargo pelo nome"""
        return discord.utils.get(guild.roles, name=role_name)

    @staticmethod
    async def get_members_by_role(guild: discord.Guild, role: discord.Role) -> List[discord.Member]:
        """Obtém todos os membros com um cargo específico"""
        return [member for member in guild.members if role in member.roles]

    @staticmethod
    async def has_permission(member: discord.Member) -> bool:
        """Verifica se o membro é administrador"""
        return member.guild_permissions.administrator


class VoiceManager:
    """Gerencia operações com canais de voz"""

    @staticmethod
    async def move_member(member: discord.Member, destination: discord.VoiceChannel) -> bool:
        """Move um membro para um canal de voz"""
        try:
            if member.voice and member.voice.channel:
                await member.move_to(destination)
                logger.info(f"Membro {member.name} movido para {destination.name}")
                return True
            return False
        except discord.Forbidden:
            logger.error(f"Sem permissão para mover {member.name}")
            return False
        except Exception as e:
            logger.error(f"Erro ao mover {member.name}: {e}")
            return False

    @staticmethod
    async def move_members_by_role(
        guild: discord.Guild,
        role: discord.Role,
        destination: discord.VoiceChannel,
    ) -> tuple[int, int]:
        """Move todos os membros com um cargo para um canal de voz

        Returns: (sucesso, falhas)
        """
        members = await RoleManager.get_members_by_role(guild, role)
        success = 0
        failed = 0

        for member in members:
            if await VoiceManager.move_member(member, destination):
                success += 1
            else:
                failed += 1

        return success, failed

    @staticmethod
    async def get_voice_channel_by_name(guild: discord.Guild, channel_name: str) -> Optional[discord.VoiceChannel]:
        """Obtém um canal de voz pelo nome"""
        return discord.utils.get(guild.voice_channels, name=channel_name)


class CommandValidator:
    """Valida comandos e entradas"""

    @staticmethod
    async def validate_admin(member: discord.Member) -> bool:
        """Valida se o usuário é administrador"""
        return await RoleManager.has_permission(member)

    @staticmethod
    async def validate_role_exists(guild: discord.Guild, role_name: str) -> bool:
        """Valida se um cargo existe"""
        role = await RoleManager.get_role_by_name(guild, role_name)
        return role is not None

    @staticmethod
    async def validate_channel_exists(guild: discord.Guild, channel_name: str) -> bool:
        """Valida se um canal de voz existe"""
        channel = await VoiceManager.get_voice_channel_by_name(guild, channel_name)
        return channel is not None
