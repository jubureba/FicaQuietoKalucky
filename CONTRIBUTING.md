# 🤝 Contribuindo para FicaQuietoKalucky

Obrigado por considerar contribuir! Aqui estão as orientações.

## 📋 Código de Conduta

Somos respeitosos e inclusivos. Comportamento abusivo não será tolerado.

## 🐛 Reportar Bugs

Abra uma [issue](https://github.com/seu-usuario/FicaQuietoKalucky/issues) com:

- Descrição clara do bug
- Passos para reproduzir
- Comportamento esperado
- Seu ambiente (Python, OS, etc)

**Exemplo:**
```
Título: Bot não move membros quando cargo tem espaço

Descrição:
Quando um cargo contém espaço no nome, o comando de movimentação falha.

Passos:
1. Criar cargo "meu cargo"
2. Clicar em "🎮 Mover Jogadores"
3. Selecionar "meu cargo"
4. Erro: cargo não encontrado

Esperado: Deve funcionar com cargos que têm espaços
```

## 🎯 Sugerir Melhorias

Abra uma [discussion](https://github.com/seu-usuario/FicaQuietoKalucky/discussions):

- Descreva o problema que você quer resolver
- Explique por que essa melhoria é importante
- Dê exemplos de como usaria

## 💻 Pull Request

### Preparação

```bash
# 1. Fork o repositório
# 2. Clone seu fork
git clone https://github.com/seu-usuario/FicaQuietoKalucky.git

# 3. Crie uma branch
git checkout -b feature/sua-feature

# 4. Crie virtual env
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows

# 5. Instale dependências
pip install -r requirements.txt
```

### Desenvolvendo

```bash
# Crie sua feature
# ... edite os arquivos ...

# Teste
python run.py

# Commit com mensagem clara
git commit -m "Adiciona feature X que resolve problema Y"

# Push
git push origin feature/sua-feature
```

### Diretrizes de Código

- ✅ Nomes descritivos de variáveis
- ✅ Sem linhas muito longas (max 100 chars)
- ✅ Funções pequenas e focadas
- ✅ Docstrings em funções públicas
- ✅ Testes para novas features

**Exemplo bom:**
```python
async def move_members_by_role(guild: discord.Guild, role: discord.Role, destination: discord.VoiceChannel) -> tuple[int, int]:
    """Move todos os membros com um cargo para um canal.
    
    Args:
        guild: O servidor Discord
        role: O cargo a mover
        destination: O canal de destino
    
    Returns:
        (sucesso, falhas)
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
```

### Commits

Siga esse padrão:

```
[tipo] Descrição curta

Descrição mais longa se necessário.

Tipo: Add, Fix, Improve, Refactor, Docs, Test, Chore
```

**Exemplos:**
- `Add comando para resetar configurações`
- `Fix bug ao mover membros com nome especial`
- `Improve mensagens de erro`
- `Docs adiciona guia de deploy`

### Mensagens de Commit

✅ Bom:
- `Add feature de agendamento`
- `Fix erro ao criar canal com espaço`
- `Improve performance de movimentação`

❌ Ruim:
- `fix`
- `atualizacao`
- `mudanças várias`

## 📁 Estrutura de Pastas

Respeite a estrutura existente:

```
bot/
├── cogs/              # Novos comandos aqui
│   └── seu_cog.py     # Seu novo cog
├── utils/             # Funções auxiliares
└── data/              # Dados (JSON, etc)
```

## ✅ Checklist antes de PR

- [ ] Testei a feature localmente
- [ ] Não há quebra de features existentes
- [ ] Código segue o estilo do projeto
- [ ] Adicionei docstrings
- [ ] Commit com mensagem clara
- [ ] Sincronizei com main/master

## 🔍 Processo de Review

1. Um maintainer revisa seu PR
2. Podem solicitar mudanças
3. Faça os ajustes necessários
4. Se aprovado, seu PR é mergeado! 🎉

## 📚 Documentação

Se adicionar features:

1. Atualize o README.md
2. Crie/atualize docs se necessário
3. Adicione exemplos de uso

## ❓ Dúvidas?

- Abra uma [discussion](https://github.com/seu-usuario/FicaQuietoKalucky/discussions)
- Verifique [issues abertas](https://github.com/seu-usuario/FicaQuietoKalucky/issues)
- Leia a documentação em `docs/`

## 🎓 Tópicos para Contribuir

Buscamos ajuda em:

- [ ] Testes automatizados
- [ ] Documentação
- [ ] Novos cogs/features
- [ ] Performance
- [ ] Suporte a múltiplos idiomas
- [ ] Dashboard web

---

**Obrigado por contribuir!** ❤️

Sua contribuição, por menor que seja, faz diferença!
