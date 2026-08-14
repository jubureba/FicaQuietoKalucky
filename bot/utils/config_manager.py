import json
import os
from pathlib import Path
from typing import Optional

CONFIG_FILE = Path(__file__).parent.parent / "data" / "config.json"


class ConfigManager:
    """Gerencia configurações do bot por servidor"""

    @staticmethod
    def ensure_file():
        """Garante que o arquivo de config existe"""
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        if not CONFIG_FILE.exists():
            CONFIG_FILE.write_text(json.dumps({}))

    @staticmethod
    def load_config(guild_id: int) -> dict:
        """Carrega config de um servidor"""
        ConfigManager.ensure_file()
        default_dict = {
            "default_group": None,
            "default_channel": None,
            "officers_role": None,
            "officers_channel": None,
            "panel_message_id": None
        }
        try:
            data = json.loads(CONFIG_FILE.read_text())
            loaded = data.get(str(guild_id), {})
            default_dict.update(loaded)
            return default_dict
        except:
            return default_dict

    @staticmethod
    def save_config(guild_id: int, config: dict):
        """Salva config de um servidor"""
        ConfigManager.ensure_file()
        try:
            data = json.loads(CONFIG_FILE.read_text())
            data[str(guild_id)] = config
            CONFIG_FILE.write_text(json.dumps(data, indent=2))
        except Exception as e:
            print(f"Erro ao salvar config: {e}")

    @staticmethod
    def set_default_group(guild_id: int, group_name: str):
        """Define o grupo padrão"""
        config = ConfigManager.load_config(guild_id)
        config["default_group"] = group_name
        ConfigManager.save_config(guild_id, config)

    @staticmethod
    def set_default_channel(guild_id: int, channel_name: str):
        """Define o canal padrão"""
        config = ConfigManager.load_config(guild_id)
        config["default_channel"] = channel_name
        ConfigManager.save_config(guild_id, config)

    @staticmethod
    def set_officers_role(guild_id: int, role_name: str):
        """Define o cargo de officers"""
        config = ConfigManager.load_config(guild_id)
        config["officers_role"] = role_name
        ConfigManager.save_config(guild_id, config)

    @staticmethod
    def set_officers_channel(guild_id: int, channel_name: str):
        """Define o canal de officers"""
        config = ConfigManager.load_config(guild_id)
        config["officers_channel"] = channel_name
        ConfigManager.save_config(guild_id, config)

    @staticmethod
    def set_panel_message_id(guild_id: int, message_id: Optional[int]):
        """Define o ID da mensagem do painel"""
        config = ConfigManager.load_config(guild_id)
        config["panel_message_id"] = message_id
        ConfigManager.save_config(guild_id, config)

    @staticmethod
    def get_default_group(guild_id: int) -> Optional[str]:
        """Obtém o grupo padrão"""
        return ConfigManager.load_config(guild_id).get("default_group")

    @staticmethod
    def get_default_channel(guild_id: int) -> Optional[str]:
        """Obtém o canal padrão"""
        return ConfigManager.load_config(guild_id).get("default_channel")

    @staticmethod
    def get_officers_role(guild_id: int) -> Optional[str]:
        """Obtém o cargo de officers"""
        return ConfigManager.load_config(guild_id).get("officers_role")

    @staticmethod
    def get_officers_channel(guild_id: int) -> Optional[str]:
        """Obtém o canal de officers"""
        return ConfigManager.load_config(guild_id).get("officers_channel")

    @staticmethod
    def get_panel_message_id(guild_id: int) -> Optional[int]:
        """Obtém o ID da mensagem do painel"""
        return ConfigManager.load_config(guild_id).get("panel_message_id")
