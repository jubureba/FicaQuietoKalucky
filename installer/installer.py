#!/usr/bin/env python3
"""
FicaQuietoKalucky - Instalador Gráfico (Windows)

Wizard de 4 telas que instala e configura o bot automaticamente:
  Tela 1 - Boas-vindas
  Tela 2 - Configuração do Discord (Token + ID do servidor)
  Tela 3 - Instalação (Python embutido, dependências, .env, serviço, start)
  Tela 4 - Conclusão (status + abrir pasta / ver logs / finalizar)

Interface simples com widgets nativos do Tkinter (tk.Button/Label/Entry),
sem widgets customizados, para máxima compatibilidade.

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
APP_VERSION = "1.2.0"
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
BG = "#2b2d31"
CARD = "#1e1f22"
ACCENT = "#5865f2"
ACCENT_HOVER = "#4752c4"
TEXT = "#f2f3f5"
TEXT_DIM = "#b5bac1"
TEXT_MUTED = "#80848e"
OK = "#23a55a"
LINK = "#00a8fc"

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
        self.python_exe = None

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

    def _find_system_python(self):
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

    def _run(self, cmd):
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
# Interface gráfica (wizard) - widgets nativos, simples
# --------------------------------------------------------------------------- #

def make_button(parent, text, command, primary=True):
    """Botão nativo estilizado (sem Canvas)."""
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=ACCENT if primary else CARD,
        fg=TEXT if primary else TEXT_DIM,
        activebackground=ACCENT_HOVER if primary else CARD,
        activeforeground=TEXT,
        relief="flat",
        bd=0,
        font=("Segoe UI", 10, "bold"),
        padx=22,
        pady=10,
        cursor="hand2",
    )


class Wizard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} - Instalador")
        self.configure(bg=BG)
        self.resizable(False, False)
        self._center(600, 480)

        self.token_var = tk.StringVar()
        self.guild_var = tk.StringVar()
        self.msg_queue = queue.Queue()

        self.step_rows = []

        self.container = tk.Frame(self, bg=BG)
        self.container.pack(fill="both", expand=True)

        self.show_welcome()

    # ---- helpers ---- #
    def _center(self, w, h):
        self.update_idletasks()
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _clear(self):
        for child in self.container.winfo_children():
            child.destroy()

    def _page(self):
        f = tk.Frame(self.container, bg=BG)
        f.pack(fill="both", expand=True, padx=44, pady=36)
        return f

    def _title(self, parent, text):
        tk.Label(parent, text=text, bg=BG, fg=TEXT,
                 font=("Segoe UI", 19, "bold"), justify="left").pack(anchor="w")

    def _subtitle(self, parent, text):
        tk.Label(parent, text=text, bg=BG, fg=TEXT_MUTED,
                 font=("Segoe UI", 11), justify="left").pack(anchor="w", pady=(6, 0))

    # ---- Tela 1: boas-vindas ---- #
    def show_welcome(self):
        self._clear()
        f = self._page()

        self._title(f, f"Bem-vindo ao {APP_NAME}")
        self._subtitle(
            f,
            "Este assistente instala e configura o bot automaticamente.\n"
            "Você só informa o token e o ID do servidor.",
        )

        feats = tk.Frame(f, bg=BG)
        feats.pack(anchor="w", pady=(26, 0))
        for txt in (
            "Instala o Python e as dependências pra você",
            "Configura o bot pra iniciar junto com o Windows",
            "Deixa tudo pronto e rodando em segundos",
        ):
            row = tk.Frame(feats, bg=BG)
            row.pack(anchor="w", pady=4)
            tk.Label(row, text="✓", bg=BG, fg=OK,
                     font=("Segoe UI", 12, "bold")).pack(side="left", padx=(0, 10))
            tk.Label(row, text=txt, bg=BG, fg=TEXT_DIM,
                     font=("Segoe UI", 11)).pack(side="left")

        bar = tk.Frame(f, bg=BG)
        bar.pack(side="bottom", fill="x", pady=(20, 0))
        make_button(bar, "Avançar  →", self.show_config).pack(side="right")

    # ---- Tela 2: configuração ---- #
    def show_config(self):
        self._clear()
        f = self._page()

        self._title(f, "Configuração do Discord")
        self._subtitle(f, "Cole abaixo as credenciais do seu bot.")

        # Token
        tk.Label(f, text="Token do Bot", bg=BG, fg=TEXT_DIM,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(22, 4))
        tk.Entry(f, textvariable=self.token_var, show="•",
                 bg=CARD, fg=TEXT, insertbackground=TEXT, relief="flat",
                 font=("Segoe UI", 11)).pack(fill="x", ipady=8)
        self._help(
            f, "Como pego o token?",
            "1. Acesse o Portal de Desenvolvedores do Discord e abra sua aplicação.\n"
            "2. No menu lateral, clique em \"Bot\".\n"
            "3. Em \"Token\", clique em \"Reset Token\" e confirme.\n"
            "4. Clique em \"Copy\" e cole o token aqui.",
            link=DISCORD_DEV_URL,
        )

        # ID do servidor
        tk.Label(f, text="ID do Servidor", bg=BG, fg=TEXT_DIM,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(16, 4))
        tk.Entry(f, textvariable=self.guild_var,
                 bg=CARD, fg=TEXT, insertbackground=TEXT, relief="flat",
                 font=("Segoe UI", 11)).pack(fill="x", ipady=8)
        self._help(
            f, "Como pego o ID do servidor?",
            "1. No Discord, ative Configurações › Avançado › \"Modo Desenvolvedor\".\n"
            "2. Clique com o botão direito no ícone do seu servidor.\n"
            "3. Escolha \"Copiar ID do servidor\".\n"
            "4. Cole aqui (o ID é uma sequência só de números).",
        )

        bar = tk.Frame(f, bg=BG)
        bar.pack(side="bottom", fill="x", pady=(20, 0))
        make_button(bar, "←  Voltar", self.show_welcome, primary=False).pack(side="left")
        make_button(bar, "Instalar  →", self._validate_and_install).pack(side="right")

    def _help(self, parent, title, body, link=None):
        """Bloco de ajuda expansível simples (mostra/oculta o texto)."""
        state = {"open": False}
        header = tk.Label(parent, text="›  " + title, bg=BG, fg=LINK,
                          font=("Segoe UI", 9, "bold"), cursor="hand2")
        header.pack(anchor="w", pady=(6, 0))

        panel = tk.Frame(parent, bg=CARD)
        inner = tk.Label(panel, text=body, bg=CARD, fg=TEXT_DIM,
                         font=("Segoe UI", 9), justify="left", anchor="w")
        inner.pack(fill="x", padx=12, pady=10)
        if link:
            lk = tk.Label(panel, text="Abrir o Portal de Desenvolvedores →",
                          bg=CARD, fg=LINK, font=("Segoe UI", 9, "underline"),
                          cursor="hand2", anchor="w")
            lk.pack(anchor="w", padx=12, pady=(0, 10))
            lk.bind("<Button-1>", lambda e: webbrowser.open(link))

        def toggle(_e=None):
            state["open"] = not state["open"]
            if state["open"]:
                header.config(text="⌄  " + title)
                panel.pack(fill="x", pady=(4, 0))
            else:
                header.config(text="›  " + title)
                panel.pack_forget()

        header.bind("<Button-1>", toggle)

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
        f = self._page()

        self._title(f, "Instalando…")
        self._subtitle(f, "Isso leva alguns segundos. Pode deixar rodando.")

        steps_frame = tk.Frame(f, bg=BG)
        steps_frame.pack(anchor="w", fill="x", pady=(22, 18))
        self.step_rows = []
        for step in Installer.STEPS:
            lbl = tk.Label(steps_frame, text="○  " + step, bg=BG, fg=TEXT_MUTED,
                           font=("Segoe UI", 11), anchor="w")
            lbl.pack(anchor="w", pady=4)
            self.step_rows.append(lbl)

        style = ttk.Style(self)
        style.theme_use("default")
        style.configure(
            "Fica.Horizontal.TProgressbar",
            troughcolor=CARD, background=ACCENT, bordercolor=BG,
            lightcolor=ACCENT, darkcolor=ACCENT, thickness=12,
        )
        bottom = tk.Frame(f, bg=BG)
        bottom.pack(side="bottom", fill="x")
        self.pct_label = tk.Label(bottom, text="0%", bg=BG, fg=TEXT_DIM,
                                  font=("Segoe UI", 10, "bold"))
        self.pct_label.pack(anchor="w", pady=(0, 6))
        self.progress = ttk.Progressbar(
            bottom, style="Fica.Horizontal.TProgressbar",
            mode="determinate", maximum=100,
        )
        self.progress.pack(fill="x")

        installer = Installer(self.token_var.get(), self.guild_var.get(), self.msg_queue)
        threading.Thread(target=installer.run, daemon=True).start()
        self.after(100, self._poll_queue)

    def _poll_queue(self):
        try:
            while True:
                kind, payload = self.msg_queue.get_nowait()
                if kind == "step":
                    self.step_rows[payload].config(
                        text="✓  " + Installer.STEPS[payload], fg=OK)
                elif kind == "progress":
                    self.progress["value"] = payload
                    self.pct_label.config(text=f"{payload}%")
                elif kind == "done":
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
        f = self._page()

        self._title(f, "🎉  Instalação concluída!")
        self._subtitle(f, f"O {APP_NAME} foi instalado e já está rodando.")

        tk.Label(f, text="Status:  🟢 ONLINE", bg=BG, fg=OK,
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(22, 0))
        tk.Label(f, text="O bot inicia sozinho toda vez que você ligar o computador.",
                 bg=BG, fg=TEXT_MUTED, font=("Segoe UI", 10)).pack(anchor="w", pady=(10, 0))

        bar = tk.Frame(f, bg=BG)
        bar.pack(side="bottom", fill="x", pady=(20, 0))
        make_button(bar, "Concluir", self.destroy).pack(side="right")
        make_button(bar, "Abrir pasta", self._open_folder, primary=False).pack(side="left")
        make_button(bar, "Ver logs", self._open_logs, primary=False).pack(side="left", padx=(10, 0))

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
