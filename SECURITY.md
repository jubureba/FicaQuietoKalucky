# 🔐 Política de Segurança

## Reportando Vulnerabilidades

**NÃO** abra issues públicas para vulnerabilidades de segurança!

Por favor, envie um email para: seu-email@example.com

Inclua:
- Descrição da vulnerabilidade
- Passos para reproduzir
- Impacto potencial
- Sugestões de correção (se tiver)

Responderemos em até 48 horas.

## Práticas de Segurança

### ✅ Seguro

- Token do bot em `.env` (nunca no código)
- `.env` no `.gitignore`
- Validação de permissões
- Input sanitization
- HTTPS para requisições externas
- Logs de auditoria
- Proteção de canais

### ❌ Inseguro

- Token hardcoded no código
- Commit de `.env`
- Sem validação de permissões
- Input direto sem sanitizar
- HTTP (inseguro)
- Sem auditoria
- Sem proteção de dados sensíveis

## Dependências

Mantemos as dependências atualizadas:

```bash
# Verificar vulnerabilidades
pip install safety
safety check

# Atualizar dependências
pip install --upgrade -r requirements.txt
```

## Segredos

### Como Manter Seguro

```bash
# ✅ CORRETO
export DISCORD_TOKEN="seu-token"
# ou em .env (com .env no .gitignore)

# ❌ NUNCA FAÇA ISSO
# DISCORD_TOKEN = "seu-token"  # No código!
# git add .env  # Commit de secrets!
```

### Se Exposição Acontecer

1. **Imediatamente**: Recriar o token no Discord
2. **Avisar**: Comunidade se aplicável
3. **Review**: Como vazamento aconteceu
4. **Implementar**: Proteções adicionais

## Permissões do Bot

O bot requer **MÍNIMAS** permissões:

```
✅ Send Messages
✅ Embed Links
✅ Manage Channels
✅ Move Members
✅ Read Message History

❌ Administrator (não precisa)
❌ Manage Server
❌ Ban Members
❌ Kick Members
```

### Por Quê?

- **Send Messages** - Responder ao usuário
- **Embed Links** - Formatar respostas
- **Manage Channels** - Criar canais de controle
- **Move Members** - Mover no voice
- **Read History** - Ver mensagens anteriores

## Tratamento de Erros

Nunca exponha:

```python
# ❌ Expõe traceback
except Exception as e:
    await ctx.send(f"Erro: {traceback.format_exc()}")

# ✅ Esconde detalhes
except Exception as e:
    logger.error(f"Erro ao processar: {e}")
    await ctx.send("Erro ao processar comando")
```

## Logs

Nunca registre:

- 🔐 Tokens ou senhas
- 📧 Emails privados
- 📱 Números de telefone
- 💳 Dados bancários
- 🆔 SSN/CPF/IDs confidenciais

## Rate Limiting

O bot implementa rate limiting:

```python
# Limite 1 ação a cada 5 segundos por usuário
@commands.cooldown(1, 5, commands.BucketType.user)
```

## Auditoria

Todas as ações são registradas:

- Quem: admin que executou
- O quê: ação realizada
- Quando: timestamp automático
- Onde: canal de auditoria

## Atualizações de Segurança

Verificamos regularmente:

- Atualizações do discord.py
- Vulnerabilidades do Python
- Dependências desatualizadas

```bash
# Checar vulnerabilidades
pip list --outdated
safety check
```

## Conformidade

Este projeto segue:

- ✅ OWASP Top 10
- ✅ Discord Terms of Service
- ✅ Best Practices de Segurança
- ✅ Data Protection Guidelines

## Contato de Segurança

- 📧 Email: seu-email@example.com
- 🔐 PGP Key: (opcional)
- 📋 Issues de Segurança: Email privadamente

---

**Agradecemos por ajudar a manter FicaQuietoKalucky seguro!** 🛡️
