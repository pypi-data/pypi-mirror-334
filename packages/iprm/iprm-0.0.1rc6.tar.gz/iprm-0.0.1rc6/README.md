# Intermediate Project Representation Model

[![PyPI version](https://img.shields.io/pypi/v/iprm.svg)](https://pypi.org/project/iprm/)

IPRM is to C++ project models what LLVM is to CPU architectures.
The goal is not to be yet another a competitor to existing software in this space (e.g. CMake, Meson, Ninja, MSBuild,
GNU Make), just like
how LLVM is not a competitor to x86-64, Aarch64, and risc-v64. Instead, the goal is to be project
model/build system agnostic, enabling developer accessibility to a wide array of project
models/build systems via a common unified format. The actual project model or build
system used under the hood is up to the developer, allowing for ease of migration to
newer/difference backends.

Developers act as the "compiler frontend", describing their large/complex C++ software project
in the .iprm format. Where-as typically an actual program is required/desired to emit the
intermediate representation, IPRM is designed so developers can do this manually because the
IPRM file format is just a python file that exposes an API tailor-made for all the varying tools
and strategies needed to describe C++ projects. IPRM then takes those files and acts as
the "compiler backend", taking its intermediate format and emitting a specific project model or
build system that can actually do the work of configuring, building, testing, and installing
C++ based projects

## Supported Systems

### Project Models

- CMake
- Meson

### Build Systems

- **(TODO)** SCons
- **(TODO)** MSBuild

### Miscellaneous 

- **(TODO)** Graphviz

## Build Instructions
> [!NOTE]
> These instructions are for if you want to build from source and/or contribute to IPRM
> IPRM is built with [IPRM](https://pypi.org/project/iprm/), so the previously released version is required to build a future version

### Pre-requisites
- [IPRM](https://pypi.org/project/iprm/)
- C++ 20
- [Python 3.12](https://www.python.org/downloads/)
- [Rust 1.85](https://rustup.rs/)

> [!WARNING]
> It's strongly recommended to install Python packages in a virtual environment to avoid conflicts with system
packages. You can create and activate a virtual environment with:
> ```
> python -m venv .venv
> # On Windows
> .venv\Scripts\activate
> # On Unix/macOS
> source .venv/bin/activate
> ```

#### Development
```
pip install [-e] . [-v]
pytest
```

#### Packaging
> [!WARNING]
> Attempting to build with just `python -m build` will most likely fail
```
python build_iprm.py
```

## Install Instructions
> [!NOTE]
> These instructions are for if you just want to use the latest version of IPRM

```
pip install iprm
```

## Usage
### Command Line Interface
`iprm --help`

### Graphic User Interface (Studio)
`iprm-studio --help`
