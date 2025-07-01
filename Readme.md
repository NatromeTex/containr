# Containr

`containr` is a command-line interface (CLI) tool designed to create fully self-contained project environments. It isolates project dependencies and cache files within the project folder, preventing clutter and pollution of system directories such as the user’s AppData or global package caches.

## Features

* Supports project scaffolding for Python, Node.js, React, and React Native.
* Automatically detects installed Python versions and fetches available Node.js, React, and React Native versions.
* Creates isolated folders for caches, virtual environments, and dependencies.
* Interactive CLI interface for selecting project type, version, and name.
* Provides commands to delete or move projects easily.
* Allows manual version input for flexibility with legacy or specific versions.
* Keeps all environment files and caches contained within the project directory.

## Installation

Clone the repository and install the package using pip:

```bash
git clone https://github.com/NatromeTex/containr.git
cd containr
pip install .
```

Alternatively, once published on PyPI, install via:

```bash
pip install containr
```

## Usage

### Create a new project environment

```bash
containr create
```

This command launches an interactive menu to select the project type, version, and name. It creates a fully self-contained project folder under the default workspace directory.

### Delete an existing project

```bash
containr -d <project_name>
```

Deletes the specified project folder and all its contents.

### Move a project to a new location

```bash
containr -m <project_name> <new_path>
```

Moves the project folder to the specified new path.

## Project Structure

The created project folder contains the following:

* `.cache/` — cache files for the project.
* `.venv/` (Python projects) — local virtual environment directory.
* `node_modules/` (Node.js, React, React Native projects) — local package directory.
* `cache/` (Node.js family) — additional cache storage.
* `project.meta` — metadata file storing project type and version information.

## Contributing

Contributions are welcome. Please open issues or submit pull requests with improvements, bug fixes, or feature suggestions.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
