# 🐟 Read–Eval–Print Loop Interpreter (REPLI)

[![repli](https://img.shields.io/badge/🐟-repli-cyan?style=flat-square)](https://github.com/luojiahai/repli)
[![package](https://img.shields.io/github/actions/workflow/status/luojiahai/repli/python-package.yml?style=flat-square&label=package&logo=githubactions&logoColor=white)](https://github.com/luojiahai/repli/actions/workflows/python-package.yml)
[![publish](https://img.shields.io/github/actions/workflow/status/luojiahai/repli/python-publish.yml?style=flat-square&label=publish&logo=githubactions&logoColor=white)](https://github.com/luojiahai/repli/actions/workflows/python-publish.yml)
[![license](https://img.shields.io/github/license/luojiahai/repli?style=flat-square&logo=github&logoColor=white)](https://github.com/luojiahai/repli/blob/main/LICENSE)
[![python](https://img.shields.io/pypi/pyversions/repli?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![pypi](https://img.shields.io/pypi/v/repli?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/repli/)

It's a Python package for building command-line terminal applications.

Don't save frequently used commands in NotePad. Don't alias a lot of complex commands. Build a Read–Eval–Print Loop (REPL) style terminal application containing pre-defined commands for easy executions from terminal.

Preview of the [example](./example/) application in terminal:

```
┌──────────────────────────────────────────────────────────────┐
│ [myapp] home                                                 │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ 1  print hello world                                         │
│ 2  do something                                              │
│ 3  nested page                                               │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│ e  exit application  |  q  quit page                         │
└──────────────────────────────────────────────────────────────┘
> 
```

## Features

- **Command**: A command is a pre-defined executable which can be one of the following:
  - Python **native function**
  - Shell command (**subprocess**)
- **Page**: A page contains multiple commands or nested pages.
- **User interface**:
  - **Header**: The header contains breadcrumbs for page navigation.
  - **Panel**: The panel contains the commands or pages for the current page.
  - **Footer**: The footer contains built-in control commands.
- **Input**: Given the commands or pages with their unique names (in the first column) in the panel, type the name and enter to execute the command or navigate to the page.

## Install

```shell
pip install repli
```

## Usage

[Example](./example/):

```python
page = Page(description="home")

@page.command(type=NativeFunction, description="print hello world")
def command_print_hello_world():
    print("hello world")

@page.command(type=Subprocess, description="do something")
def command_do_something():
    return "echo something else"

nested_page = Page(description="nested page")
page.add_page(page=nested_page)

interpreter = Interpreter(page=page, name="myapp")
interpreter.loop()
```

## Development

Requirements:

[Poetry](https://python-poetry.org/)

Setup environment:

```shell
poetry shell
poetry install
```

Run example application:

```shell
poetry run example
```

Type check:

```shell
poetry run mypy ./example ./repli ./tests
```

Format:

```shell
poetry run black ./example ./repli ./tests
```

Lint:

```shell
poetry run flake8 ./example ./repli ./tests --config ./.flake8
```

Test:

```shell
poetry run pytest
```

Coverage:

```shell
poetry run coverage run -m pytest &&
poetry run coverage report -m
```

Export `requirements.txt`:

```shell
poetry export --dev --without-hashes --format=requirements.txt > requirements.txt
```
