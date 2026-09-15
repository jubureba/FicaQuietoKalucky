#!/usr/bin/env python3
"""
FicaQuietoKalucky - Instalador Gráfico (Windows)

Wizard de 4 telas que instala e configura o bot automaticamente:
  Tela 1 - Boas-vindas
  Tela 2 - Configuração do Discord (Token + ID do servidor)
  Tela 3 - Instalação (Python embutido, dependências, .env, serviço, start)
  Tela 4 - Conclusão (status + abrir pasta / ver logs / finalizar)

Empacotado como FicaQuietoKalucky-Setup.exe via PyInstaller (ver build.py).
"""

import os
import sys
import queue
import shutil
import ctypes
import threading
import webbrowser
import subprocess
import urllib.request
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

# --------------------------------------------------------------------------- #
# Constantes
# --------------------------------------------------------------------------- #

APP_NAME = "FicaQuietoKalucky"
TASK_NAME = "FicaQuietoKalucky"

# Python embutido (embeddable) usado quando o usuário não tem Python instalado.
PYTHON_EMBED_VERSION = "3.11.9"
PYTHON_EMBED_URL = (
    f"https://www.python.org/ftp/python/{PYTHON_EMBED_VERSION}/"
    f"python-{PYTHON_EMBED_VERSION}-embed-amd64.zip"
)
GET_PIP_URL = "https://bootstrap.pypa.io/get-pip.py"

# Diretório de instalação padrão: %LOCALAPPDATA%\FicaQuietoKalucky
INSTALL_DIR = Path(os.environ.get("LOCALAPPDATA", Path.home())) / APP_NAME

# Paleta (dark, estilo Discord)
BG = "#1e1f22"          # fundo geral (mais escuro)
SIDEBAR = "#181920"     # barra lateral
CARD = "#2b2d31"        # painéis / inputs
CARD_HOVER = "#313338"
INPUT_BG = "#1e1f22"
BORDER = "#3f4147"
ACCENT = "#5865f2"      # blurple
ACCENT_HOVER = "#4752c4"
TEXT = "#f2f3f5"
TEXT_DIM = "#b5bac1"
TEXT_MUTED = "#80848e"
OK = "#23a55a"
WARN = "#f0b232"
LINK = "#00a8fc"

WIN_W, WIN_H = 760, 560

DISCORD_DEV_URL = "https://discord.com/developers/applications"


def resource_path(rel: str) -> Path:
    """Resolve caminho de recurso, funcionando com PyInstaller (--onefile)."""
    base = getattr(sys, "_MEIPASS", None)
    if base:
        return Path(base) / rel
    # Em desenvolvimento os arquivos do bot ficam um nível acima do installer/
    return Path(__file__).resolve().parent.parent / rel


# --------------------------------------------------------------------------- #
# Passos de instalação (rodam em thread separada)
# --------------------------------------------------------------------------- #

class InstallError(Exception):
    pass


class Installer:
    """Executa a instalação e reporta progresso via fila de mensagens."""

    # Ordem e rótulos exibidos na Tela 3
    STEPS = [
        "Preparando ambiente",
        "Instalando Python",
        "Instalando dependências",
        "Criando configuração",
        "Configurando serviço",
        "Iniciando bot",
    ]

    def __init__(self, token: str, guild_id: str, msg_queue: "queue.Queue"):
        self.token = token.strip()
        self.guild_id = guild_id.strip()
        self.q = msg_queue
        self.python_exe: Path | None = None

    # ---- helpers de comunicação com a GUI ---- #
    def _step_done(self, index: int):
        self.q.put(("step", index))

    def _progress(self, pct: int):
        self.q.put(("progress", pct))

    def _fail(self, msg: str):
        self.q.put(("error", msg))

    def _finish(self):
        self.q.put(("done", None))

    # ---- execução ---- #
    def run(self):
        try:
            self.prepare_environment()
            self._step_done(0)
            self._progress(16)

            self.install_python()
            self._step_done(1)
            self._progress(40)

            self.install_dependencies()
            self._step_done(2)
            self._progress(64)

            self.create_config()
            self._step_done(3)
            self._progress(78)

            self.configure_service()
            self._step_done(4)
            self._progress(90)

            self.start_bot()
            self._step_done(5)
            self._progress(100)

            self._finish()
        except InstallError as e:
            self._fail(str(e))
        except Exception as e:  # noqa: BLE001 - queremos reportar qualquer falha
            self._fail(f"Erro inesperado: {e}")

    # ---- passos ---- #
    def prepare_environment(self):
        """Cria a pasta de instalação e copia os arquivos do bot."""
        INSTALL_DIR.mkdir(parents=True, exist_ok=True)

        for item in ("bot", "run.py", "requirements.txt"):
            src = resource_path(item)
            if not src.exists():
                raise InstallError(f"Arquivo do bot não encontrado no pacote: {item}")
            dst = INSTALL_DIR / item
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)

        (INSTALL_DIR / "logs").mkdir(exist_ok=True)

    def install_python(self):
        """Usa o Python do sistema se disponível; senão baixa o embeddable."""
        system_py = self._find_system_python()
        if system_py:
            self.python_exe = system_py
            return

        py_dir = INSTALL_DIR / "python"
        py_dir.mkdir(exist_ok=True)
        zip_path = INSTALL_DIR / "python-embed.zip"

        self._download(PYTHON_EMBED_URL, zip_path)

        import zipfile
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(py_dir)
        zip_path.unlink(missing_ok=True)

        # Habilita 'import site' para o pip funcionar no embeddable
        for pth in py_dir.glob("python*._pth"):
            content = pth.read_text(encoding="utf-8")
            content = content.replace("#import site", "import site")
            pth.write_text(content, encoding="utf-8")

        python_exe = py_dir / "python.exe"

        # Instala o pip
        get_pip = INSTALL_DIR / "get-pip.py"
        self._download(GET_PIP_URL, get_pip)
        self._run([str(python_exe), str(get_pip), "--no-warn-script-location"])
        get_pip.unlink(missing_ok=True)

        self.python_exe = python_exe

    def install_dependencies(self):
        req = INSTALL_DIR / "requirements.txt"
        self._run([
            str(self.python_exe), "-m", "pip", "install",
            "--no-warn-script-location", "-r", str(req),
        ])

    def create_config(self):
        """Escreve o .env na pasta de instalação com os dados informados."""
        env = INSTALL_DIR / ".env"
        env.write_text(
            "# ===== DISCORD =====\n"
            f"DISCORD_TOKEN={self.token}\n"
            f"ADMIN_GUILD_ID={self.guild_id}\n"
            "PREFIX=!\n\n"
            "# ===== LOGGING =====\n"
            "LOG_LEVEL=INFO\n",
            encoding="utf-8",
        )

    def configure_service(self):
        """Cria uma tarefa agendada para iniciar o bot no logon do usuário."""
        runner = self._write_runner_script()
        # /F sobrescreve tarefa existente; /RL LIMITED = privilégios do usuário
        try:
            self._run([
                "schtasks", "/Create", "/TN", TASK_NAME,
                "/TR", f'"{runner}"',
                "/SC", "ONLOGON", "/RL", "LIMITED", "/F",
            ])
        except InstallError:
            # Se não for possível criar a tarefa, o bot ainda inicia manualmente.
            pass

    def start_bot(self):
        runner = INSTALL_DIR / "start_bot.vbs"
        if runner.exists():
            os.startfile(str(runner))  # noqa: S606 - script local gerado por nós
        else:
            self._spawn_bot_directly()

    # ---- utilitários ---- #
    def _write_runner_script(self) -> Path:
        """
        Cria um .vbs que roda o bot sem abrir janela de console e um .bat auxiliar.
        Retorna o caminho do .vbs (usado pela tarefa agendada e pelo start).
        """
        bat = INSTALL_DIR / "run_bot.bat"
        bat.write_text(
            "@echo off\r\n"
            f'cd /d "{INSTALL_DIR}"\r\n'
            f'"{self.python_exe}" run.py >> "{INSTALL_DIR / "logs" / "bot.log"}" 2>&1\r\n',
            encoding="utf-8",
        )

        vbs = INSTALL_DIR / "start_bot.vbs"
        vbs.write_text(
            'Set WshShell = CreateObject("WScript.Shell")\r\n'
            f'WshShell.Run """{bat}""", 0, False\r\n',
            encoding="utf-8",
        )
        return vbs

    def _spawn_bot_directly(self):
        creationflags = 0
        if os.name == "nt":
            creationflags = subprocess.CREATE_NO_WINDOW  # type: ignore[attr-defined]
        log = open(INSTALL_DIR / "logs" / "bot.log", "a", encoding="utf-8")
        subprocess.Popen(
            [str(self.python_exe), "run.py"],
            cwd=str(INSTALL_DIR),
            stdout=log,
            stderr=log,
            creationflags=creationflags,
        )

    def _find_system_python(self) -> Path | None:
        """Procura um Python 3.8+ instalado no sistema."""
        for name in ("python", "python3"):
            path = shutil.which(name)
            if not path:
                continue
            try:
                out = subprocess.run(
                    [path, "-c", "import sys;print('%d.%d' % sys.version_info[:2])"],
                    capture_output=True, text=True, timeout=15,
                )
                major, minor = (int(x) for x in out.stdout.strip().split("."))
                if (major, minor) >= (3, 8):
                    return Path(path)
            except Exception:  # noqa: BLE001
                continue
        return None

    def _download(self, url: str, dest: Path):
        try:
            with urllib.request.urlopen(url, timeout=60) as resp, open(dest, "wb") as f:
                shutil.copyfileobj(resp, f)
        except Exception as e:  # noqa: BLE001
            raise InstallError(f"Falha ao baixar {url}: {e}") from e

    def _run(self, cmd: list[str]):
        creationflags = 0
        if os.name == "nt":
            creationflags = subprocess.CREATE_NO_WINDOW  # type: ignore[attr-defined]
        result = subprocess.run(
            cmd, capture_output=True, text=True, creationflags=creationflags,
        )
        if result.returncode != 0:
            raise InstallError(
                f"Comando falhou ({' '.join(cmd[:2])}): "
                f"{result.stderr.strip() or result.stdout.strip()}"
            )


# --------------------------------------------------------------------------- #
# Widgets reutilizáveis
# --------------------------------------------------------------------------- #

class PillButton(tk.Frame):
    """Botão arredondado (usa Canvas) com estados hover, com/sem preenchimento."""

    def __init__(self, parent, text, command, primary=True, bg=BG,
                 width=150, height=42):
        super().__init__(parent, bg=bg)
        self.command = command
        self.primary = primary
        self.bg = bg
        self._enabled = True

        self.fill = ACCENT if primary else CARD
        self.fill_hover = ACCENT_HOVER if primary else CARD_HOVER
        self.fg = TEXT

        self.canvas = tk.Canvas(self, width=width, height=height, bg=bg,
                                highlightthickness=0, bd=0, cursor="hand2")
        self.canvas.pack()
        self._w, self._h, self._r = width, height, height // 2
        self._text = text
        self._draw(self.fill)

        for seq in ("<Enter>",):
            self.canvas.bind(seq, lambda e: self._enabled and self._draw(self.fill_hover))
        self.canvas.bind("<Leave>", lambda e: self._enabled and self._draw(self.fill))
        self.canvas.bind("<Button-1>", self._click)

    def _round_rect(self, x1, y1, x2, y2, r, **kw):
        pts = [
            x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2,
            x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
        ]
        return self.canvas.create_polygon(pts, smooth=True, **kw)

    def _draw(self, fill):
        self.canvas.delete("all")
        self._round_rect(1, 1, self._w - 1, self._h - 1, self._r, fill=fill)
        self.canvas.create_text(self._w // 2, self._h // 2, text=self._text,
                                fill=self.fg, font=("Segoe UI Semibold", 11))

    def _click(self, _e):
        if self._enabled and self.command:
            self.command()

    def set_enabled(self, value: bool):
        self._enabled = value
        self.canvas.configure(cursor="hand2" if value else "arrow")
        self._draw(self.fill if value else CARD)
        self.fg = TEXT if value else TEXT_MUTED
        self._draw(self.fill if value else CARD)


class Collapsible(tk.Frame):
    """Painel 'Como pego isso?' que expande/recolhe com um passo a passo."""

    def __init__(self, parent, title, steps, link=None, link_label=None, bg=BG):
        super().__init__(parent, bg=bg)
        self.bg = bg
        self._open = False
        self.link = link

        self.header = tk.Label(
            self, text=f"›  {title}", bg=bg, fg=LINK,
            font=("Segoe UI", 9, "bold"), cursor="hand2", anchor="w",
        )
        self.header.pack(anchor="w")
        self.header.bind("<Button-1>", lambda e: self.toggle())

        self.body = tk.Frame(self, bg=CARD)
        inner = tk.Frame(self.body, bg=CARD)
        inner.pack(fill="x", padx=14, pady=12)
        for i, step in enumerate(steps, 1):
            row = tk.Frame(inner, bg=CARD)
            row.pack(fill="x", anchor="w", pady=2)
            tk.Label(row, text=f"{i}.", bg=CARD, fg=ACCENT,
                     font=("Segoe UI Semibold", 9), width=2, anchor="w").pack(side="left")
            tk.Label(row, text=step, bg=CARD, fg=TEXT_DIM, justify="left",
                     font=("Segoe UI", 9), wraplength=420, anchor="w").pack(side="left")
        if link:
            lk = tk.Label(inner, text=link_label or link, bg=CARD, fg=LINK,
                          font=("Segoe UI", 9, "underline"), cursor="hand2", anchor="w")
            lk.pack(anchor="w", pady=(8, 0))
            lk.bind("<Button-1>", lambda e: webbrowser.open(link))

    def toggle(self):
        self._open = not self._open
        if self._open:
            self.header.config(text=self.header.cget("text").replace("›", "⌄", 1))
            self.body.pack(fill="x", pady=(6, 0))
        else:
            self.header.config(text=self.header.cget("text").replace("⌄", "›", 1))
            self.body.forget()


class Field(tk.Frame):
    """Input estilizado com label, borda de foco e (opcional) botão mostrar/ocultar."""

    def __init__(self, parent, label, textvar, placeholder="", secret=False, bg=BG):
        super().__init__(parent, bg=bg)
        self.secret = secret
        self._shown = not secret

        tk.Label(self, text=label, bg=bg, fg=TEXT_DIM,
                 font=("Segoe UI Semibold", 9)).pack(anchor="w", pady=(0, 5))

        self.box = tk.Frame(self, bg=INPUT_BG, highlightbackground=BORDER,
                            highlightcolor=ACCENT, highlightthickness=1, bd=0)
        self.box.pack(fill="x")

        self.entry = tk.Entry(
            self.box, textvariable=textvar, show="" if not secret else "•",
            bg=INPUT_BG, fg=TEXT, insertbackground=TEXT, relief="flat", bd=0,
            font=("Segoe UI", 11),
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(12, 6), ipady=9)
        self.entry.bind("<FocusIn>", lambda e: self.box.config(highlightbackground=ACCENT))
        self.entry.bind("<FocusOut>", lambda e: self.box.config(highlightbackground=BORDER))

        if secret:
            self.toggle_btn = tk.Label(self.box, text="👁", bg=INPUT_BG, fg=TEXT_MUTED,
                                       font=("Segoe UI", 11), cursor="hand2")
            self.toggle_btn.pack(side="right", padx=(0, 12))
            self.toggle_btn.bind("<Button-1>", lambda e: self._toggle_secret())

    def _toggle_secret(self):
        self._shown = not self._shown
        self.entry.config(show="" if self._shown else "•")
        self.toggle_btn.config(fg=TEXT if self._shown else TEXT_MUTED)

    def focus(self):
        self.entry.focus_set()


# --------------------------------------------------------------------------- #
# Interface gráfica (wizard)
# --------------------------------------------------------------------------- #

WIZARD_STEPS = ["Boas-vindas", "Configuração", "Instalação", "Concluído"]


class Wizard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} - Instalador")
        self.configure(bg=BG)
        self.resizable(False, False)
        self._center(WIN_W, WIN_H)

        self.token_var = tk.StringVar()
        self.guild_var = tk.StringVar()
        self.msg_queue: "queue.Queue" = queue.Queue()
        self.install_ok = False
        self.current_step = 0

        self._step_widgets: list[dict] = []

        # Layout: sidebar (esquerda) + área de conteúdo (direita)
        root = tk.Frame(self, bg=BG)
        root.pack(fill="both", expand=True)

        self.sidebar = tk.Frame(root, bg=SIDEBAR, width=210)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        self._build_sidebar()

        self.content = tk.Frame(root, bg=BG)
        self.content.pack(side="left", fill="both", expand=True)

        self.show_welcome()

    # ---- sidebar ---- #
    def _build_sidebar(self):
        tk.Label(self.sidebar, text=APP_NAME, bg=SIDEBAR, fg=TEXT,
                 font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=24, pady=(30, 4))
        tk.Label(self.sidebar, text="Assistente de instalação", bg=SIDEBAR,
                 fg=TEXT_MUTED, font=("Segoe UI", 9)).pack(anchor="w", padx=24)

        steps_wrap = tk.Frame(self.sidebar, bg=SIDEBAR)
        steps_wrap.pack(anchor="w", padx=20, pady=(36, 0), fill="x")

        self._sidebar_items = []
        for i, name in enumerate(WIZARD_STEPS):
            row = tk.Frame(steps_wrap, bg=SIDEBAR)
            row.pack(anchor="w", fill="x", pady=7)
            dot = tk.Label(row, text="●", bg=SIDEBAR, fg=TEXT_MUTED,
                           font=("Segoe UI", 11))
            dot.pack(side="left", padx=(0, 10))
            lbl = tk.Label(row, text=name, bg=SIDEBAR, fg=TEXT_MUTED,
                           font=("Segoe UI", 10))
            lbl.pack(side="left")
            self._sidebar_items.append((dot, lbl))

        tk.Label(self.sidebar, text="v1.1.0", bg=SIDEBAR, fg=TEXT_MUTED,
                 font=("Segoe UI", 8)).pack(side="bottom", anchor="w", padx=24, pady=18)

    def _set_step(self, index: int):
        self.current_step = index
        for i, (dot, lbl) in enumerate(self._sidebar_items):
            if i < index:
                dot.config(text="✓", fg=OK)
                lbl.config(fg=TEXT_DIM)
            elif i == index:
                dot.config(text="●", fg=ACCENT)
                lbl.config(fg=TEXT, font=("Segoe UI", 10, "bold"))
            else:
                dot.config(text="●", fg=TEXT_MUTED)
                lbl.config(fg=TEXT_MUTED, font=("Segoe UI", 10))

    # ---- helpers ---- #
    def _center(self, w: int, h: int):
        self.update_idletasks()
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _clear(self):
        for child in self.content.winfo_children():
            child.destroy()

    def _page(self, pad_x=44, pad_y=40):
        f = tk.Frame(self.content, bg=BG)
        f.pack(fill="both", expand=True, padx=pad_x, pady=pad_y)
        return f

    def _heading(self, parent, title, subtitle=None):
        tk.Label(parent, text=title, bg=BG, fg=TEXT,
                 font=("Segoe UI", 20, "bold")).pack(anchor="w")
        if subtitle:
            tk.Label(parent, text=subtitle, bg=BG, fg=TEXT_MUTED,
                     font=("Segoe UI", 11), justify="left").pack(anchor="w", pady=(6, 0))

    # ---- Tela 1: boas-vindas ---- #
    def show_welcome(self):
        self._clear()
        self._set_step(0)
        f = self._page()

        tk.Label(f, text="👋", bg=BG, font=("Segoe UI Emoji", 40)).pack(anchor="w")
        self._heading(
            f, f"Bem-vindo ao\n{APP_NAME}",
        )
        tk.Label(
            f,
            text="Este assistente instala e configura o bot automaticamente.\n"
                 "Você só precisa informar o token e o ID do servidor — o resto\n"
                 "é por nossa conta.",
            bg=BG, fg=TEXT_DIM, font=("Segoe UI", 11), justify="left",
        ).pack(anchor="w", pady=(18, 0))

        feats = tk.Frame(f, bg=BG)
        feats.pack(anchor="w", pady=(24, 0))
        for txt in (
            "Instala o Python e as dependências pra você",
            "Configura o bot pra iniciar sozinho com o Windows",
            "Deixa tudo pronto e rodando em segundos",
        ):
            row = tk.Frame(feats, bg=BG)
            row.pack(anchor="w", pady=3)
            tk.Label(row, text="✓", bg=BG, fg=OK,
                     font=("Segoe UI", 11, "bold")).pack(side="left", padx=(0, 10))
            tk.Label(row, text=txt, bg=BG, fg=TEXT_DIM,
                     font=("Segoe UI", 10)).pack(side="left")

        bar = tk.Frame(f, bg=BG)
        bar.pack(side="bottom", fill="x")
        PillButton(bar, "Começar  →", self.show_config, bg=BG).pack(side="right")

    # ---- Tela 2: configuração do Discord ---- #
    def show_config(self):
        self._clear()
        self._set_step(1)
        f = self._page(pad_y=34)

        self._heading(f, "Configuração do Discord",
                      "Cole abaixo as credenciais do seu bot.")

        # Token
        token_field = Field(f, "TOKEN DO BOT", self.token_var, secret=True)
        token_field.pack(fill="x", pady=(24, 6))
        Collapsible(
            f, "Como pego o token?",
            steps=[
                "Acesse o Portal de Desenvolvedores do Discord e abra a sua aplicação (ou crie uma nova).",
                "No menu lateral, clique em \"Bot\".",
                "Em \"Token\", clique em \"Reset Token\" e confirme.",
                "Clique em \"Copy\" para copiar o token e cole aqui.",
                "Guarde o token com segurança — ele dá controle total do bot.",
            ],
            link=DISCORD_DEV_URL,
            link_label="Abrir o Portal de Desenvolvedores →",
        ).pack(fill="x", pady=(0, 8))

        # Guild ID
        guild_field = Field(f, "ID DO SERVIDOR", self.guild_var)
        guild_field.pack(fill="x", pady=(14, 6))
        Collapsible(
            f, "Como pego o ID do servidor?",
            steps=[
                "No Discord, abra Configurações do Usuário › Avançado e ative o \"Modo Desenvolvedor\".",
                "Volte à lista de servidores, clique com o botão direito no ícone do seu servidor.",
                "Escolha \"Copiar ID do servidor\".",
                "Cole aqui — o ID é uma sequência só de números.",
            ],
        ).pack(fill="x", pady=(0, 8))

        bar = tk.Frame(f, bg=BG)
        bar.pack(side="bottom", fill="x")
        PillButton(bar, "←  Voltar", self.show_welcome, primary=False,
                   bg=BG, width=120).pack(side="left")
        PillButton(bar, "Instalar  →", self._validate_and_install, bg=BG).pack(side="right")

        token_field.focus()

    def _validate_and_install(self):
        token = self.token_var.get().strip()
        guild = self.guild_var.get().strip()
        if not token:
            messagebox.showwarning(APP_NAME, "Informe o Token do Bot.")
            return
        if not guild.isdigit():
            messagebox.showwarning(APP_NAME, "O ID do Servidor deve conter apenas números.")
            return
        self.show_install()

    # ---- Tela 3: instalação ---- #
    def show_install(self):
        self._clear()
        self._set_step(2)
        f = self._page()

        self._heading(f, "Instalando…",
                      "Isso leva alguns segundos. Pode deixar rodando.")

        steps_frame = tk.Frame(f, bg=BG)
        steps_frame.pack(anchor="w", fill="x", pady=(26, 20))
        self._step_widgets = []
        for step in Installer.STEPS:
            row = tk.Frame(steps_frame, bg=BG)
            row.pack(anchor="w", fill="x", pady=5)
            icon = tk.Label(row, text="○", bg=BG, fg=TEXT_MUTED,
                            font=("Segoe UI", 12), width=2)
            icon.pack(side="left")
            lbl = tk.Label(row, text=step, bg=BG, fg=TEXT_MUTED,
                           font=("Segoe UI", 11), anchor="w")
            lbl.pack(side="left")
            self._step_widgets.append({"icon": icon, "label": lbl})

        style = ttk.Style(self)
        style.theme_use("default")
        style.configure(
            "Fica.Horizontal.TProgressbar",
            troughcolor=CARD, background=ACCENT, bordercolor=BG,
            lightcolor=ACCENT, darkcolor=ACCENT, thickness=10,
        )
        bottom = tk.Frame(f, bg=BG)
        bottom.pack(side="bottom", fill="x")
        self.pct_label = tk.Label(bottom, text="0%", bg=BG, fg=TEXT_DIM,
                                  font=("Segoe UI Semibold", 10))
        self.pct_label.pack(anchor="w", pady=(0, 6))
        self.progress = ttk.Progressbar(
            bottom, style="Fica.Horizontal.TProgressbar",
            mode="determinate", maximum=100,
        )
        self.progress.pack(fill="x")

        self._mark_active(0)

        installer = Installer(self.token_var.get(), self.guild_var.get(), self.msg_queue)
        threading.Thread(target=installer.run, daemon=True).start()
        self.after(100, self._poll_queue)

    def _mark_active(self, index: int):
        if 0 <= index < len(self._step_widgets):
            w = self._step_widgets[index]
            w["icon"].config(text="◐", fg=ACCENT)
            w["label"].config(fg=TEXT, font=("Segoe UI Semibold", 11))

    def _poll_queue(self):
        try:
            while True:
                kind, payload = self.msg_queue.get_nowait()
                if kind == "step":
                    w = self._step_widgets[payload]
                    w["icon"].config(text="✓", fg=OK)
                    w["label"].config(fg=TEXT_DIM, font=("Segoe UI", 11))
                    self._mark_active(payload + 1)
                elif kind == "progress":
                    self.progress["value"] = payload
                    self.pct_label.config(text=f"{payload}%")
                elif kind == "done":
                    self.install_ok = True
                    self.after(400, self.show_done)
                    return
                elif kind == "error":
                    messagebox.showerror(
                        APP_NAME,
                        f"A instalação falhou:\n\n{payload}\n\n"
                        f"Verifique os logs em:\n{INSTALL_DIR / 'logs'}",
                    )
                    self.show_config()
                    return
        except queue.Empty:
            pass
        self.after(100, self._poll_queue)

    # ---- Tela 4: conclusão ---- #
    def show_done(self):
        self._clear()
        self._set_step(3)
        f = self._page()

        tk.Label(f, text="🎉", bg=BG, font=("Segoe UI Emoji", 44)).pack(anchor="w")
        self._heading(f, "Tudo pronto!",
                      f"O {APP_NAME} foi instalado e já está rodando.")

        status = tk.Frame(f, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        status.pack(fill="x", pady=(24, 0))
        inner = tk.Frame(status, bg=CARD)
        inner.pack(fill="x", padx=18, pady=16)
        tk.Label(inner, text="🟢", bg=CARD, font=("Segoe UI Emoji", 13)).pack(side="left")
        tk.Label(inner, text="Status:  ONLINE", bg=CARD, fg=OK,
                 font=("Segoe UI Semibold", 12)).pack(side="left", padx=(10, 0))
        tk.Label(f, text="O bot inicia sozinho toda vez que você ligar o computador.",
                 bg=BG, fg=TEXT_MUTED, font=("Segoe UI", 10)).pack(anchor="w", pady=(14, 0))

        bar = tk.Frame(f, bg=BG)
        bar.pack(side="bottom", fill="x")
        PillButton(bar, "Concluir", self.destroy, bg=BG, width=130).pack(side="right")
        PillButton(bar, "Ver logs", self._open_logs, primary=False,
                   bg=BG, width=120).pack(side="left")
        PillButton(bar, "Abrir pasta", self._open_folder, primary=False,
                   bg=BG, width=130).pack(side="left", padx=(0, 10))

    def _open_folder(self):
        os.startfile(str(INSTALL_DIR))  # noqa: S606

    def _open_logs(self):
        log = INSTALL_DIR / "logs" / "bot.log"
        target = log if log.exists() else (INSTALL_DIR / "logs")
        os.startfile(str(target))  # noqa: S606


def main():
    # Melhora nitidez em telas HiDPI no Windows
    if os.name == "nt":
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:  # noqa: BLE001
            pass
    Wizard().mainloop()


if __name__ == "__main__":
    main()
