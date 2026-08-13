# 🎯 Guia de Setup Completo - FicaQuietoKalucky

Este guia passo a passo ajudará você a configurar o bot desde zero.

## 📋 Parte 1: Preparar o Bot no Discord

### 1.1 Criar uma Aplicação Discord

1. Acesse https://discord.com/developers/applications
2. Clique em **"New Application"**
3. Digite um nome (ex: "FicaQuietoKalucky")
4. Clique em **"Create"**

### 1.2 Criar um Bot

1. Na página da aplicação, vá para **"Bot"** no menu esquerdo
2. Clique em **"Add Bot"**
3. Copie o **TOKEN** (isso é importante!)

### 1.3 Configurar Permissões

1. Vá para **"OAuth2"** → **"URL Generator"**
2. Em **"Scopes"**, marque:
   - ✅ `bot`
3. Em **"Permissions"**, marque:
   - ✅ `Send Messages`
   - ✅ `Embed Links`
   - ✅ `Read Message History`
   - ✅ `Move Members`
   - ✅ `Use Slash Commands`

4. Copie a URL gerada no final da página

### 1.4 Adicionar Bot ao Servidor

1. Cole a URL do passo anterior no navegador
2. Selecione o servidor Discord onde quer adicionar o bot
3. Autorize as permissões

### 1.5 Ativar Intents Necessários

1. Volte à página do Bot
2. Scroll down até **"Privileged Gateway Intents"**
3. Ative os seguintes intents:
   - ✅ **PRESENCE INTENT**
   - ✅ **SERVER MEMBERS INTENT**
   - ✅ **MESSAGE CONTENT INTENT**

4. Clique em **"Save Changes"**

## 📋 Parte 2: Obter ID do Servidor

1. Abra Discord e vá ao seu servidor
2. Clique no ícone do servidor no topo
3. Clique em **"Copiar ID de Servidor"** (se não vê, ative Developer Mode)
4. **Para ativar Developer Mode:**
   - Discord → Configurações Avançadas → ativar "Modo de Desenvolvedor"

## 📋 Parte 3: Configurar o Bot Localmente

### 3.1 Clonar/Baixar Projeto

```bash
cd FicaQuietoKalucky
```

### 3.2 Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3.3 Configurar Variáveis de Ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env`:

```env
DISCORD_TOKEN=seu_token_do_bot_aqui
ADMIN_GUILD_ID=id_do_seu_servidor
PREFIX=!
```

**Exemplo:**
```env
DISCORD_TOKEN=MzQ1MjM1MjMmNDUy...
ADMIN_GUILD_ID=123456789012345678
PREFIX=!
```

### 3.4 Executar o Bot

```bash
python run.py
```

Se viu:
```
✅ Bot conectado como FicaQuietoKalucky#1234
```

Parabéns! ✨ O bot está rodando!

## 📋 Parte 4: Configurar Cargos no Discord

1. Vá às configurações do servidor
2. Clique em **"Cargos"**
3. Clique em **"Criar Cargo"**

Crie os seguintes cargos:

### Cargo 1: Jogador
- Nome: `jogador`
- Cor: Azul (ou a que preferir)

### Cargo 2: Officer
- Nome: `officer`
- Cor: Verde (ou a que preferir)

### Cargo 3: Trial (opcional)
- Nome: `trial`
- Cor: Amarelo (ou a que preferir)

**Atribuindo Cargos:**
1. Clique com botão direito em um membro
2. Selecione **"Adicionar Cargo"**
3. Escolha o cargo

## ✅ Teste o Bot

No Discord, digite:

```
!ajuda
```

Você deve ver uma mensagem com todos os comandos disponíveis.

## 📝 Usando o Bot

### Comando Básico: Mover Jogadores

```
!mover "jogador" "Sala de Espera"
```

Isso move todos os membros com o cargo `jogador` para o canal `Sala de Espera`.

### Mover Officers

```
!mover_officers "Sala de Officers"
```

### Listar Membros em um Canal

```
!listar_em_voz "Sala de Espera"
```

### Listar Todos os Cargos

```
!listar_cargos
```

### Ver Status do Bot

```
!status
```

## 🎮 Exemplo Prático Completo

1. **Criar canais de voz:**
   - "Fila de Espera"
   - "Sala 1"
   - "Sala 2"

2. **Criar cargos:**
   - "jogador"
   - "officer"

3. **Atribuir cargos a membros**

4. **Comandos:**
   ```
   !mover "jogador" "Fila de Espera"
   !mover_officers "Sala de Officers"
   ```

## 🔧 Troubleshooting

### Problema: "Bot não aparece no servidor"
**Solução:**
- Verifique se a URL de invite está correta
- Certifique-se de ser administrador do servidor
- Verifique as permissões na aba "Bot"

### Problema: "Erro ao conectar"
**Solução:**
- Verifique o token no arquivo `.env`
- Verifique a conexão com a internet
- Verifique se o token não expirou

### Problema: "Erro ao mover membros"
**Solução:**
- Certifique-se de que o bot tem "Move Members" permission
- Verifique se o bot está acima do cargo na hierarquia
- Verifique se o canal existe

### Problema: "Cargo não encontrado"
**Solução:**
- Use o nome exato do cargo
- Digite `!listar_cargos` para ver nomes corretos
- Cargos são case-sensitive

## 🚀 Próximos Passos

1. Adicione mais cargos conforme necessário
2. Personalize os comandos (edite os arquivos em `bot/cogs/`)
3. Adicione novos comandos seguindo a estrutura existente
4. Considere fazer o bot rodar 24/7 (hospedagem em servidor)

## 📞 Ajuda

Para mais informações, consulte o `README.md`.

---

**Sucesso na configuração! 🎉**
