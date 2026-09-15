# Instalador do FicaQuietoKalucky

Gera um único arquivo `FicaQuietoKalucky-Setup.exe` que o usuário final abre com
dois cliques. O instalador tem 4 telas e cuida de tudo automaticamente:

1. **Boas-vindas**
2. **Configuração do Discord** — Token do Bot + ID do Servidor, com painéis de
   ajuda expansíveis (**"Como pego o token?"** e **"Como pego o ID do servidor?"**)
   explicando o passo a passo e com link direto para o Portal de Desenvolvedores
3. **Instalação** — prepara ambiente, instala Python, dependências, cria a
   configuração, configura o serviço de autostart e inicia o bot
4. **Conclusão** — status ONLINE + `Abrir pasta`, `Ver logs`, `Concluir`

A interface tem barra lateral com o progresso das etapas, tema dark estilo
Discord, campos com botão de mostrar/ocultar o token e botões arredondados.

## O que o instalador faz na máquina do usuário

- Copia os arquivos do bot para `%LOCALAPPDATA%\FicaQuietoKalucky`
- Usa o Python do sistema (3.8+) se existir; caso contrário baixa o
  **Python embeddable** e instala nele
- Instala as dependências do `requirements.txt` (discord.py, python-dotenv, aiohttp)
- Cria o `.env` com o `DISCORD_TOKEN` e `ADMIN_GUILD_ID` informados
- Cria uma **tarefa agendada** (`schtasks`, gatilho ONLOGON) para o bot subir
  sozinho quando o usuário faz login
- Inicia o bot em segundo plano (sem janela de console), com logs em
  `%LOCALAPPDATA%\FicaQuietoKalucky\logs\bot.log`

> O download do Python embeddable e das dependências exige internet durante a
> instalação. Se a máquina já tiver Python, apenas as dependências são baixadas.

## Como gerar o `.exe` (quem distribui)

Precisa ser feito **no Windows** com Python 3.8+:

```bat
pip install pyinstaller
python installer\build.py
```

Saída: `installer\dist\FicaQuietoKalucky-Setup.exe`.

O `build.py` embute `bot/`, `run.py` e `requirements.txt` dentro do próprio
`.exe`, então o arquivo gerado é autossuficiente para distribuição.

Ícone opcional: coloque um `installer\icon.ico` antes do build para
personalizar o ícone do executável.

## Testar o instalador sem gerar o `.exe`

Dá para rodar a GUI direto com Python (Windows):

```bat
python installer\installer.py
```

## Estrutura

```
installer/
  installer.py   # wizard Tkinter (4 telas) + lógica de instalação
  build.py       # empacota tudo em FicaQuietoKalucky-Setup.exe (PyInstaller)
  icon.ico       # (opcional) ícone do executável
  README.md      # este arquivo
```

## Observações

- O instalador é específico para **Windows** (usa `schtasks`, `.vbs`,
  `os.startfile`, Python embeddable amd64).
- A tarefa agendada roda com privilégios do próprio usuário (`/RL LIMITED`),
  sem exigir administrador. Se a criação da tarefa falhar, o bot ainda é
  iniciado normalmente na instalação — só não sobe sozinho no próximo logon.
- Para desinstalar manualmente: remova a tarefa
  (`schtasks /Delete /TN FicaQuietoKalucky /F`) e apague a pasta
  `%LOCALAPPDATA%\FicaQuietoKalucky`.
