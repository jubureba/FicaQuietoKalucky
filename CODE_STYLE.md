# 📐 Guia de Estilo de Código

Padrões de código para FicaQuietoKalucky.

## Python

### Formatação

- **Indentação**: 4 espaços (não tabs)
- **Comprimento máximo de linha**: 100 caracteres
- **Encoding**: UTF-8

### Convenções de Nomes

```python
# Classes: PascalCase
class MyClass:
    pass

# Funções/métodos: snake_case
def my_function():
    pass

# Constantes: UPPER_CASE
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# Variáveis privadas: _leading_underscore
_private_var = None

# Variáveis "magic": __double_underscore (evite)
__magic__ = None  # Evite isso
```

### Imports

```python
# 1. Imports do stdlib
import asyncio
import logging
from pathlib import Path
from typing import Optional

# 2. Imports de bibliotecas de terceiros
import discord
from discord.ext import commands

# 3. Imports locais
from utils import RoleManager
from utils.config_manager import ConfigManager
```

### Docstrings

Use docstrings em **toda** função pública:

```python
async def move_members(guild: discord.Guild, role: discord.Role, destination: discord.VoiceChannel) -> tuple[int, int]:
    """Move todos os membros com um cargo para um canal.
    
    Args:
        guild: O servidor Discord
        role: O cargo a mover
        destination: O canal de destino
    
    Returns:
        Tupla (sucesso, falhas)
    
    Raises:
        discord.Forbidden: Se sem permissão
    """
    pass
```

### Type Hints

Use type hints em **toda** função:

```python
# ✅ Bom
async def process_data(data: list[str]) -> dict[str, int]:
    result: dict[str, int] = {}
    return result

# ❌ Ruim
async def process_data(data):
    result = {}
    return result
```

### Comprimento de Linhas

```python
# ✅ Bom - quebra em múltiplas linhas
embed = discord.Embed(
    title="Título Longo que Não Cabe em uma Linha",
    description="Descrição também longa",
    color=discord.Color.blurple()
)

# ❌ Ruim
embed = discord.Embed(title="Título Longo que Não Cabe em uma Linha", description="Descrição também longa", color=discord.Color.blurple())
```

### Async/Await

```python
# ✅ Correto
async def setup(bot):
    await bot.add_cog(MyC og(bot))

# ❌ Incorreto
def setup(bot):
    asyncio.run(bot.add_cog(MyCog(bot)))
```

## Estrutura de Cogs

```python
import discord
from discord.ext import commands
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class MyCog(commands.Cog):
    """Descrição clara do cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="comando")
    async def comando(self, ctx):
        """Descrição do comando"""
        pass

    @commands.Cog.listener()
    async def on_ready(self):
        """Listener para evento"""
        logger.info("Bot pronto!")


async def setup(bot):
    await bot.add_cog(MyCog(bot))
```

## Tratamento de Erros

```python
# ✅ Correto
try:
    await guild.create_text_channel("canal")
except discord.Forbidden:
    logger.error("Sem permissão para criar canal")
except discord.HTTPException as e:
    logger.error(f"Erro HTTP: {e}")

# ❌ Incorreto
try:
    await guild.create_text_channel("canal")
except Exception:
    pass  # Nunca use bare except!
```

## Logging

```python
import logging

logger = logging.getLogger(__name__)

# Use níveis apropriados
logger.debug("Informação de debug")      # Detalhes internos
logger.info("✅ Ação concluída")         # Eventos importantes
logger.warning("⚠️ Aviso importante")    # Algo inesperado
logger.error("❌ Erro ao fazer algo")    # Erro que precisa atenção
logger.critical("🔥 Sistema indisponível") # Falha crítica
```

## Constantes

```python
# bot/config.py
class Config:
    """Configurações centralizadas"""
    
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    ADMIN_GUILD_ID = int(os.getenv("ADMIN_GUILD_ID", 0))
    PREFIX = os.getenv("PREFIX", "!")
    
    # Timeouts
    DELETE_MESSAGE_AFTER = 5  # segundos
    WEBHOOK_TIMEOUT = 30  # segundos
```

## Comments

Use comments **apenas** para explicar **POR QUÊ**, não **O QUÊ**:

```python
# ✅ Correto - explica o porquê
# Aguardamos 5 segundos porque o Discord precisa processar a criação do canal
await asyncio.sleep(5)

# ❌ Incorreto - óbvio pelo código
# Aguardar 5 segundos
await asyncio.sleep(5)
```

## Métodos Privados vs Públicos

```python
class MyClass:
    # Público - para usar fora da classe
    async def process(self):
        """Processa dados publicamente"""
        return await self._validate()
    
    # Privado - só para uso interno
    async def _validate(self):
        """Validação interna"""
        pass
```

## Formato de Strings

```python
# ✅ Correto - f-strings
name = "Alice"
message = f"Olá {name}!"

# ⚠️ Aceitável em alguns casos
message = "Olá {0}!".format(name)

# ❌ Evite
message = "Olá " + name + "!"
```

## Tests (Recomendado)

```python
# tests/test_helpers.py
import pytest
from bot.utils import RoleManager


@pytest.mark.asyncio
async def test_get_role_by_name(mock_guild):
    """Testa obtenção de cargo pelo nome"""
    role = await RoleManager.get_role_by_name(mock_guild, "admin")
    assert role.name == "admin"
    assert role.id == 123456


@pytest.mark.asyncio
async def test_get_role_not_found(mock_guild):
    """Testa quando cargo não existe"""
    role = await RoleManager.get_role_by_name(mock_guild, "inexistente")
    assert role is None
```

## Checklist de Qualidade

Antes de fazer PR:

- [ ] Código segue este guia
- [ ] Type hints em todas as funções
- [ ] Docstrings em públicas
- [ ] Imports organizados
- [ ] Sem comentários desnecessários
- [ ] Nomes descritivos
- [ ] Max 100 caracteres por linha
- [ ] Sem código comentado
- [ ] Logger usado para debug/erros
- [ ] Erros tratados apropriadamente

## Ferramentas Recomendadas

```bash
# Formatação automática
pip install black isort
black bot --line-length=100
isort bot

# Linting
pip install flake8 pylint
flake8 bot
pylint bot

# Type checking
pip install mypy
mypy bot
```

## Referências

- [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [PEP 257](https://www.python.org/dev/peps/pep-0257/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [discord.py Documentation](https://discordpy.readthedocs.io/)

---

**Dúvidas?** Abra uma [discussion](https://github.com/seu-usuario/FicaQuietoKalucky/discussions)!
