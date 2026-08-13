import discord
from discord.ext import commands
import logging
import os
import sys
from pathlib import Path

from config import Config

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class FicaQuietoKaluckyBot(commands.Bot):
    """Bot principal do FicaQuietoKalucky"""

    def __init__(self, *args, **kwargs):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.voice_states = True

        super().__init__(
            command_prefix=Config.PREFIX,
            intents=intents,
            help_command=None,
            *args,
            **kwargs,
        )

    async def setup_hook(self):
        """Carrega todos os cogs (extensões)"""
        cogs_path = Path(__file__).parent / "cogs"

        for filename in os.listdir(cogs_path):
            if filename.endswith(".py") and not filename.startswith("_"):
                cog_name = filename[:-3]
                try:
                    await self.load_extension(f"cogs.{cog_name}")
                    logger.info(f"✅ Cog '{cog_name}' carregado com sucesso")
                except Exception as e:
                    logger.error(f"❌ Erro ao carregar cog '{cog_name}': {e}")

    async def on_ready(self):
        """Chamado quando o bot se conecta ao Discord"""
        logger.info(f"✅ Bot conectado como {self.user}")
        logger.info(f"📊 Conectado em {len(self.guilds)} servidor(es)")

        activity = discord.Activity(type=discord.ActivityType.watching, name="!ajuda")
        await self.change_presence(activity=activity)

    async def on_command_error(self, ctx, error):
        """Trata erros de comandos"""
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                title="❌ Comando não encontrado",
                description=f"Use **!ajuda** para ver os comandos disponíveis.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="❌ Argumentos faltando",
                description=f"Use **!ajuda** para ver como usar este comando.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="❌ Permissão insuficiente",
                description="Você não tem permissão para usar este comando.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
        else:
            logger.error(f"Erro em comando: {error}")
            embed = discord.Embed(
                title="❌ Erro ao executar comando",
                description="Ocorreu um erro ao executar o comando. Tente novamente.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)


def main():
    """Função principal para iniciar o bot"""
    try:
        Config.validate()
    except ValueError as e:
        logger.error(f"❌ Erro de configuração: {e}")
        sys.exit(1)

    bot = FicaQuietoKaluckyBot()

    try:
        logger.info(f"🚀 Iniciando {Config.BOT_NAME} v{Config.BOT_VERSION}")
        bot.run(Config.DISCORD_TOKEN)
    except KeyboardInterrupt:
        logger.info("⛔ Bot interrompido pelo usuário")
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
