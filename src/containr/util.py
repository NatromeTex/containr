import os
import sys
import subprocess
from rich.console import Console

console = Console()

def create_python_workspace(path, version):
    venv_path = os.path.join(path, ".venv")

    console.print(f"[yellow]Creating virtual environment with Python {version}...[/]")

    try:
        if sys.platform == "win32":
            python_executable = "py"
            command = f'{python_executable} -{version} -m venv "{venv_path}"'
            console.print(command)
            subprocess.check_call(command, shell=True)
        else:
            python_executable = f"python{version}"
            command = [python_executable, "-m", "venv", venv_path]
            subprocess.check_call(command)

        console.print(f"[green]Virtual environment created at:[/] {venv_path}")

        config_path = os.path.join(venv_path, "pip.conf" if sys.platform != "win32" else "pip.ini")
        with open(config_path, "w") as f:
            f.write("[global]\nno-cache-dir = true\n")

    except subprocess.CalledProcessError:
        console.print(f"[red]Failed to create virtual environment with {python_executable}[/]")
        return
    except FileNotFoundError:
        console.print(f"[red]{python_executable} not found. Is it installed?[/]")
        return
