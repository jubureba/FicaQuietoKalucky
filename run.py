#!/usr/bin/env python3
"""Arquivo de inicialização do FicaQuietoKalucky"""

import sys
import os
from pathlib import Path

# Adiciona diretórios ao path
bot_dir = Path(__file__).parent / "bot"
sys.path.insert(0, str(bot_dir))
sys.path.insert(0, str(bot_dir.parent))

# Muda para diretório do bot
os.chdir(bot_dir)

from main import main

if __name__ == "__main__":
    main()
