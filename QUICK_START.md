# ⚡ Quick Start - FicaQuietoKalucky

Resumo super rápido para colocar o bot em funcionamento em 5 minutos!

## 🚀 Em 5 Passos

### 1️⃣ Obtenha o Token
1. Acesse https://discord.com/developers/applications
2. Create New Application
3. Vá para "Bot" → Add Bot
4. **Copie o TOKEN**

### 2️⃣ Ative os Intents
1. Em "Privileged Gateway Intents"
2. Ative:
   - ✅ MESSAGE CONTENT INTENT
   - ✅ SERVER MEMBERS INTENT
   - ✅ PRESENCE INTENT

### 3️⃣ Adicione ao Servidor
1. OAuth2 → URL Generator
2. Scopes: `bot`
3. Permissions: `Send Messages`, `Move Members`, `Embed Links`
4. Cole a URL gerada no navegador
5. Authorize

### 4️⃣ Configure o .env
```bash
cp .env.example .env
# Edite .env com seu TOKEN e GUILD_ID
```

### 5️⃣ Execute!
```bash
pip install -r requirements.txt
python run.py
```

✅ **Bot online!**

## 🎮 Primeiros Comandos

```
!ajuda              # Ver todos os comandos
!status             # Confirmar que está online
!listar_cargos      # Ver cargos do servidor
!listar_canais      # Ver canais de voz
```

## 📋 Checklist de Setup

```
DISCORD
☐ Criar aplicação em developer.discord.com
☐ Criar bot
☐ Copiar token
☐ Ativar intents necessários
☐ Gerar URL e adicionar ao servidor
☐ Configurar permissões

LOCAL
☐ Copiar .env.example para .env
☐ Adicionar DISCORD_TOKEN no .env
☐ Adicionar ADMIN_GUILD_ID no .env
☐ pip install -r requirements.txt
☐ python run.py

DISCORD (Server Setup)
☐ Criar cargo "jogador"
☐ Criar cargo "officer"
☐ Criar canais de voz para testes
☐ Testar comando !mover

VALIDAÇÃO
☐ Bot aparece online no servidor
☐ !ajuda mostra os comandos
☐ !listar_cargos lista os cargos
☐ Conseguir mover membros
```

## 🔧 Troubleshooting Rápido

| Erro | Solução |
|------|---------|
| "DISCORD_TOKEN não está configurada" | Editar `.env` com o token correto |
| "Bot não aparece no servidor" | Verificar permissões na URL de OAuth2 |
| "Erro ao mover membros" | Verificar se bot tem "Move Members" permission |
| "Cargo não encontrado" | Verificar escrita exata do nome do cargo |
| "ImportError: No module named discord" | `pip install -r requirements.txt` |

## 📚 Próximos Passos

1. **Leia** `SETUP_GUIDE.md` para detalhes completos
2. **Explore** `EXTENSOES_EXEMPLO.md` para adicionar novos comandos
3. **Siga** `BEST_PRACTICES.md` para manter código limpo

## 🎯 Uso Básico

### Mover Todos com um Cargo

```
!mover "jogador" "Sala 1"
```

**O que faz:** Move todos os membros com o cargo "jogador" para o canal "Sala 1"

### Mover Officers

```
!mover_officers "Sala de Officers"
```

### Listar Membros em um Canal

```
!listar_em_voz "Sala 1"
```

## 🎨 Criar Cargos (no Discord)

1. Configurações do servidor → Cargos
2. Novo Cargo
3. Nome: `jogador` (ou o nome que quiser)
4. Atribuir a membros

## 🚀 Próxima Etapa

Depois de tudo funcionando, você pode:

- [ ] Adicionar mais cargos (trial, premium, etc)
- [ ] Criar novos comandos (ver `EXTENSOES_EXEMPLO.md`)
- [ ] Configurar logging avançado
- [ ] Fazer o bot rodar 24/7 (hospedagem)

## 📞 Precisa de Ajuda?

1. **Leia:** `README.md` - Documentação completa
2. **Consulte:** `SETUP_GUIDE.md` - Passo a passo detalhado
3. **Explore:** `BEST_PRACTICES.md` - Soluções comuns

## 🎉 Sucesso!

Se você chegou aqui e o bot está rodando, **parabéns!** 🎊

Agora comece a customizar e adicionar funcionalidades conforme necessário!

---

**FicaQuietoKalucky - Mantendo Discord organizado! 🎮**
