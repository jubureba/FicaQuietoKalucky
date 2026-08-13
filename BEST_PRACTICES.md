# 🏆 Melhores Práticas - FicaQuietoKalucky

Guia de melhores práticas para usar e expandir o bot de forma eficiente.

## 👥 Gerenciamento de Cargos

### ✅ Faça Isso

```
Cargos:
├── Dono
├── Officers
├── Jogadores Premium
├── Jogadores Regular
├── Trial
└── Bots
```

**Hierarquia clara**: Cargos mais importantes no topo.

### ❌ Não Faça Isso

```
Cargos desorganizados:
├── player1
├── player2
├── player3
├── random_role
└── test
```

**Problemas**: Difícil gerenciar, sem padrão consistente.

## 📝 Nomeação de Cargos

### ✅ Nomes Descritivos

```
officer            # Claro
jogador            # Descritivo
trial              # Curto e direto
premium            # Objetivo
```

### ❌ Nomes Ruins

```
a                  # Muito vago
player123          # Números desnecessários
role_with_long_name_that_is_confusing  # Muito longo
```

## 🎮 Organização de Canais de Voz

### Estrutura Recomendada

```
JOGOS
├── Fila de Espera
├── Sala 1
├── Sala 2
└── Sala 3

ADMINS
├── Sala de Officers
└── Reuniões

GERAL
├── AFK
└── Streaming
```

## 🤖 Configuração Segura do Bot

### 1️⃣ Token Seguro

```python
# ✅ Correto
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# ❌ Errado
DISCORD_TOKEN = "MzQ1MjM1MjMmNDUy..."  # Nunca coloque no código!
```

### 2️⃣ Permissões Mínimas

```
Permissões Necessárias:
✅ Send Messages
✅ Embed Links
✅ Move Members
✅ Read Message History

❌ Não conceda:
- Administrator
- Manage Server
- Ban Members
```

### 3️⃣ Proteção de Dados

```python
# ✅ Correto: Validar entrada
@commands.command(name="mover")
async def move_members(self, ctx, role_name: str):
    # Validar se role existe
    if not await CommandValidator.validate_role_exists(ctx.guild, role_name):
        await ctx.send("Erro: Cargo não existe")
        return
```

## 📊 Movimentação Eficiente

### Padrão de Fluxo

```
1. Admin executa comando
   ↓
2. Bot valida admin
   ↓
3. Bot valida cargo
   ↓
4. Bot valida canal destino
   ↓
5. Bot move membros
   ↓
6. Bot envia confirmação
```

### Exemplo com Logging

```python
@commands.command(name="mover")
async def move_members(self, ctx, role_name: str, *, destination_name: str):
    logger.info(f"Admin {ctx.author} tentou mover {role_name}")
    
    # Validações...
    
    logger.info(f"Movimentação concluída: {success} sucesso, {failed} falhas")
```

## 🔄 Expandindo o Bot

### Quando Criar um Novo Cog

```
✅ Criar novo Cog quando:
- Funcionalidade é independente
- Mais de 50 linhas de código
- Múltiplos comandos relacionados
- Lógica complexa

❌ Não criar quando:
- É apenas uma função auxiliar
- Tightly coupled com outro cog
- É uma task única simples
```

### Estrutura de Arquivo Bem Organizada

```
bot/
├── cogs/
│   ├── movements.py      # Movimentação
│   ├── admin.py          # Administração
│   ├── reminders.py      # Lembretes
│   └── welcome.py        # Boas-vindas
├── utils/
│   ├── helpers.py        # Funções auxiliares
│   └── validators.py     # Validações
└── config.py             # Configuração única
```

## 📈 Performance

### 1️⃣ Evite Loops Pesados

```python
# ❌ Ruim: API call em loop
for member in members:
    await move_member(member)  # Lento!

# ✅ Bom: Processamento paralelo
await asyncio.gather(*[move_member(m) for m in members])
```

### 2️⃣ Cache de Dados

```python
# ✅ Crie cache de roles
self.role_cache = {}

for role in guild.roles:
    self.role_cache[role.name] = role

# Lookup rápido
if role_name in self.role_cache:
    role = self.role_cache[role_name]
```

## 🐛 Debugging

### Logs Informativos

```python
logger.info(f"✅ Ação concluída: {details}")      # Info
logger.warning(f"⚠️  Atenção: {details}")         # Warning
logger.error(f"❌ Erro: {details}")               # Error
```

### Ferramentas Úteis

```bash
# Ver logs em tempo real
tail -f debug.log

# Buscar erros
grep "ERROR" debug.log

# Contar eventos
grep "moved" debug.log | wc -l
```

## 🔐 Segurança

### 1️⃣ Validar Todas as Entradas

```python
# ✅ Valide tudo
@commands.command()
async def comando(self, ctx, role_name: str):
    if not isinstance(role_name, str):
        await ctx.send("❌ Erro: Tipo inválido")
        return
    
    if len(role_name) > 100:
        await ctx.send("❌ Erro: Nome muito longo")
        return
```

### 2️⃣ Rate Limiting

```python
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.command(name="mover")
async def move_members(self, ctx, ...):
    """Limite: 1 uso a cada 5 segundos por usuário"""
    pass
```

## 📊 Monitoramento

### Verificar Status

```bash
# Ver se bot está rodando
ps aux | grep python

# Ver porta
netstat -tulpn | grep python

# Ver logs
tail -100 bot.log
```

### Métricas Importantes

```
1. Uptime do bot
2. Número de movimentações por dia
3. Erros ocorridos
4. Latência do bot
5. Membros ativos
```

## 🚀 Deployment 24/7

### Opção 1: Systemd (Linux)

```ini
# /etc/systemd/system/ficaquietokalucky.service
[Unit]
Description=FicaQuietoKalucky Bot
After=network.target

[Service]
Type=simple
User=seu_usuario
WorkingDirectory=/home/seu_usuario/FicaQuietoKalucky
ExecStart=/usr/bin/python3 /home/seu_usuario/FicaQuietoKalucky/run.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### Opção 2: Docker

```dockerfile
FROM python:3.10

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY bot/ bot/
COPY run.py .

CMD ["python", "run.py"]
```

### Opção 3: Hospedagem em Nuvem

- AWS EC2
- DigitalOcean
- Heroku
- Replit
- Railway

## ✅ Checklist de Lançamento

- [ ] Token em `.env` e não no código
- [ ] Logs configurados
- [ ] Todos os cogs carregam sem erro
- [ ] Bot testado em servidor de teste
- [ ] Permissões mínimas necessárias
- [ ] Documentação atualizada
- [ ] Versionamento iniciado (git)
- [ ] Backups configurados

## 🔄 Atualizações Seguras

```bash
# 1. Crie um branch de teste
git checkout -b update

# 2. Faça as mudanças
# ... edite os arquivos ...

# 3. Teste localmente
python run.py

# 4. Se tudo ok, faça merge
git merge update

# 5. Deploy
git pull origin main
python run.py
```

---

**Seguindo estas práticas, seu bot será robusto, seguro e escalável! 🎯**
