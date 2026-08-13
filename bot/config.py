import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configurações centralizadas do bot"""

    # Discord
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    ADMIN_GUILD_ID = int(os.getenv("ADMIN_GUILD_ID", 0))
    PREFIX = os.getenv("PREFIX", "!")

    # Logs
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Status
    BOT_VERSION = "1.0.0"
    BOT_NAME = "FicaQuietoKalucky"

    # Validações
    @staticmethod
    def validate():
        """Valida se as configurações necessárias estão presentes"""
        if not Config.DISCORD_TOKEN:
            raise ValueError("DISCORD_TOKEN não está configurada no arquivo .env")
        if Config.ADMIN_GUILD_ID == 0:
            raise ValueError("ADMIN_GUILD_ID não está configurada no arquivo .env")
