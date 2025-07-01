import os
import shutil
import argparse
import subprocess
import json
import sys
import questionary
from urllib.request import urlopen
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from .util import create_python_workspace

console = Console()

BASE_DIR = os.path.abspath("containr_workspace")
os.makedirs(BASE_DIR, exist_ok=True)

def get_installed_python_versions():
  versions = set()
  if sys.platform == "win32":
    try:
      output = subprocess.check_output(["py", "-0p"], universal_newlines=True)
      for line in output.splitlines():
        if "-" in line:
          version = line.split()[0].replace("-", "").strip()
          versions.add(version)
    except Exception:
      pass
  else:
    for minor in range(6, 13):
      try:
        result = subprocess.run([f"python3.{minor}", "--version"], capture_output=True)
        if result.returncode == 0:
          versions.add(f"3.{minor}")
      except Exception:
        pass
  return sorted(list(versions), reverse=True)


def get_latest_node_versions():
  try:
    with urlopen("https://nodejs.org/dist/index.json") as response:
      data = json.load(response)
      versions = sorted({entry["version"].lstrip("v")[:2] for entry in data}, reverse=True)
      return list(versions)[:5]
  except Exception:
    return ["20", "18", "16"]


def get_latest_react_versions():
  try:
    with urlopen("https://registry.npmjs.org/react") as response:
      data = json.load(response)
      tags = data.get("dist-tags", {})
      return [tags.get("latest", "18.0.0")]
  except Exception:
    return ["18"]


def get_latest_react_native_versions():
  try:
    with urlopen("https://registry.npmjs.org/react-native") as response:
      data = json.load(response)
      versions = sorted(data["versions"].keys(), reverse=True)
      return [v for v in versions if v.startswith("0.")]
  except Exception:
    return ["0.73", "0.72"]


def interactive_create():
  console.print(Panel("[bold cyan]containr: Project Environment Creator[/]"))

  lang = questionary.select(
    "Select project type:",
    choices=["Python", "Node", "React", "React native"]
  ).ask()

  if lang == "Python":
    versions = get_installed_python_versions()
  elif lang == "Node":
    versions = get_latest_node_versions()
  elif lang == "React":
    versions = get_latest_react_versions()
  elif lang == "React native":
    versions = get_latest_react_native_versions()
  else:
    versions = ["latest"]

  version = questionary.select(
    "Select version:",
    choices=versions
  ).ask()

  name = questionary.text("Enter project name:").ask()

  path = os.path.join(BASE_DIR, name)
  if os.path.exists(path):
    console.print(f"[red]Error:[/] Project '{name}' already exists at {path}.")
    return

  os.makedirs(path)
  os.makedirs(os.path.join(path, ".cache"))

  if lang == "Python":
    console.print("calling create_py function")
    create_python_workspace(path, version)
  elif lang in ["Node", "React", "React native"]:
    os.makedirs(os.path.join(path, "cache"))

  with open(os.path.join(path, "project.meta"), "w") as f:
    f.write(f"type={lang}\nversion={version}\n")

  console.print(f"[green]Project '{name}' created at:[/] {path}")


def delete_project(name):
  path = os.path.join(BASE_DIR, name)
  if os.path.exists(path):
    shutil.rmtree(path)
    console.print(f"[green]Deleted project:[/] {name}")
  else:
    console.print(f"[red]Error:[/] Project '{name}' not found.")


def move_project(name, new_path):
  src = os.path.join(BASE_DIR, name)
  dst = os.path.abspath(new_path)
  if os.path.exists(src):
    shutil.move(src, dst)
    console.print(f"[green]Moved project '{name}' to:[/] {dst}")
  else:
    console.print(f"[red]Error:[/] Project '{name}' not found.")


def main():
  parser = argparse.ArgumentParser(description="containr: isolated dev environment CLI")
  parser.add_argument("create", nargs="?", help="Create a new project")
  parser.add_argument("-d", metavar="NAME", help="Delete a project")
  parser.add_argument("-m", nargs=2, metavar=("NAME", "NEW_PATH"), help="Move a project")
  args = parser.parse_args()

  if args.create:
    interactive_create()
  elif args.d:
    delete_project(args.d)
  elif args.m:
    move_project(args.m[0], args.m[1])
  else:
    parser.print_help()


if __name__ == "__main__":
  main()
