#!/usr/bin/env python3
"""
Gera FicaQuietoKalucky-Setup.exe a partir de installer/installer.py.

Empacota os arquivos do bot (bot/, run.py, requirements.txt) dentro do .exe
como dados, de forma que o instalador seja um único arquivo distribuível.

Uso (no Windows, com Python 3.8+):
    pip install pyinstaller
    python installer/build.py

Saída:
    installer/dist/FicaQuietoKalucky-Setup.exe
"""

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # .../FicaQuietoKalucky/installer
PROJECT = HERE.parent                            # .../FicaQuietoKalucky

# Arquivos/pastas do bot a embutir no .exe. Formato PyInstaller: "ORIGEM;DESTINO".
# No Windows o separador de --add-data é ';'.
DATA = [
    (PROJECT / "bot", "bot"),
    (PROJECT / "run.py", "."),
    (PROJECT / "requirements.txt", "."),
]


def main() -> int:
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("PyInstaller não encontrado. Instale com:\n    pip install pyinstaller")
        return 1

    sep = ";" if sys.platform.startswith("win") else ":"
    add_data_args = []
    for src, dest in DATA:
        if not src.exists():
            print(f"AVISO: origem não encontrada, pulando: {src}")
            continue
        add_data_args += ["--add-data", f"{src}{sep}{dest}"]

    icon = HERE / "icon.ico"

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--windowed",                       # sem console (app GUI)
        "--name", "FicaQuietoKalucky-Setup",
        "--distpath", str(HERE / "dist"),
        "--workpath", str(HERE / "build"),
        "--specpath", str(HERE),
        *add_data_args,
        str(HERE / "installer.py"),
    ]
    if icon.exists():
        cmd[cmd.index("--windowed") + 1:cmd.index("--windowed") + 1] = ["--icon", str(icon)]

    print("Executando:\n  " + " ".join(cmd) + "\n")
    result = subprocess.run(cmd)
    if result.returncode == 0:
        exe = HERE / "dist" / "FicaQuietoKalucky-Setup.exe"
        print(f"\n✅ Instalador gerado: {exe}")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
