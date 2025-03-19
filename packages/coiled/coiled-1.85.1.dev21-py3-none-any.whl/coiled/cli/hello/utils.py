from __future__ import annotations

import asyncio
import contextlib
import functools
import os
import pathlib
import subprocess
import sys
import time

import importlib_metadata
import rich
import rich.panel
from rich import box
from rich.console import Console, Group
from rich.live import Live
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.rule import Rule
from rich.syntax import Syntax

import coiled
from coiled.pypi_conda_map import PYPI_TO_CONDA
from coiled.scan import scan_prefix
from coiled.utils import error_info_for_tracking

PRIMARY_COLOR = "rgb(0,95,255)"
console = Console(width=80)


class Panel(rich.panel.Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "padding" not in kwargs:
            self.padding = (1, 2)


@contextlib.contextmanager
def log_interactions(action):
    success = True
    exception = None
    try:
        yield
    except (Exception, KeyboardInterrupt) as e:
        # TODO: Better error when something goes wrong in example
        success = False
        exception = e
        raise e
    finally:
        coiled.add_interaction(
            f"cli-hello:{action}",
            success=success,
            **error_info_for_tracking(exception),
        )


def live_panel_print(*renderables, delay=0.5, panel_kwargs=None):
    panel_kwargs = panel_kwargs or {}
    renderables = [r for r in renderables if r is not None]
    with Live(Panel(renderables[0], **panel_kwargs), console=console, auto_refresh=False) as live:
        for idx in range(len(renderables)):
            time.sleep(delay)
            live.update(Panel(Group(*renderables[: idx + 1]), **panel_kwargs), refresh=True)


@functools.cache
def cached_scan():
    return asyncio.run(scan_prefix())


def has_mixed_conda_channels():
    scan = cached_scan()
    channels = {pkg["channel"] for pkg in scan if pkg["source"] == "conda"}
    non_conda_forge_channels = channels - {"conda-forge"}
    mixed_channels = bool(non_conda_forge_channels)
    packages = []
    if mixed_channels:
        # Only log full package / channel info when there are mixed channels
        packages = [(pkg["name"], pkg["channel"]) for pkg in scan if pkg["source"] == "conda"]
    coiled.add_interaction(
        "cli-hello:mixed-conda-channels",
        success=True,
        mixed_channels=mixed_channels,
        channels=tuple(channels),
        packages=tuple(packages),
    )
    return mixed_channels


def has_macos_system_python():
    system_python_mac = sys.platform == "darwin" and "Python3.framework" in sys.exec_prefix
    coiled.add_interaction("cli-hello:system-python-mac", success=True, system_python_mac=system_python_mac)
    return system_python_mac


def missing_dependencies_message(dependencies):
    missing = []
    for dep in dependencies:
        try:
            importlib_metadata.distribution(dep)
        except ModuleNotFoundError:
            missing.append(dep)
    coiled.add_interaction("cli-hello:missing-deps", success=True, missing=missing)

    msg = ""
    if missing:
        if len(missing) == 1:
            missing_formatted = f"`{missing[0]}`"
        elif len(missing) == 2:
            missing_formatted = f"`{missing[0]}` and `{missing[1]}`"
        else:
            missing_formatted = ", ".join([f"`{p}`" for p in missing[:-1]])
            missing_formatted += f", and `{missing[-1]}`"

        plural = len(missing) > 1
        msg = Markdown(
            f"""
I noticed you're missing the {"libraries" if plural else "library"} {missing_formatted}
which {"are" if plural else "is"} needed for this example.
We'll install {"them" if plural else "it"} for you with `pip` before
running the example.  

<br>
"""  # noqa
        )
    return msg, missing


def ask_and_run_example(name, missing, filename) -> bool | None:
    if missing:
        prompt = "Install packages and run example?"
    else:
        prompt = "Run example?"

    try:
        choice = Prompt.ask(
            prompt,
            choices=["y", "n"],
            default="y",
            show_choices=True,
        )
    except KeyboardInterrupt:
        coiled.add_interaction(action="cli-hello:KeyboardInterrupt", success=False)
        return False

    coiled.add_interaction("cli-hello:install-and-run", success=True, choice=choice)
    if choice == "y":
        if missing:
            with log_interactions("install-missing-deps"):
                with console.status(f"Installing {', '.join(missing)}"):
                    subprocess.run(
                        [sys.executable or "python", "-m", "pip", "install", *missing], capture_output=True, check=True
                    )
        # Run example
        with log_interactions(f"example-{name}"):
            fill = pathlib.Path(__file__).parent / "scripts" / "fill_ipython.py"
            ipython = "ipython"
            if sys.executable:
                ipython = pathlib.Path(sys.executable).parent / "ipython"
            subprocess.run(
                [ipython, "-i", fill, str(filename)],
                env={**os.environ, **{"DASK_COILED__TAGS": f'{{"coiled-hello": "{name}"}}'}},
                check=True,
            )
    else:
        return None

    return True


def render_example(name: str, dependencies, msg_start) -> bool | None:
    script_path = pathlib.Path(__file__).parent / "scripts" / f"{name.replace('-', '_')}.py"
    msg_code = Syntax.from_path(str(script_path))
    msg_ipython = """
Next we'll drop you into an IPython terminal to run this code yourself.
When you're done type "exit" to come back here
""".strip()

    msg_messy = messy_software_message(dependencies)
    msg_missing, missing = missing_dependencies_message(dependencies)
    if msg_messy:
        msg_end = """
I recommend quitting this wizard (Ctrl-C) and running the commands above.
    """.strip()

        live_panel_print(msg_start, Rule(style="grey"), msg_code, Rule(style="grey"), msg_messy, msg_end)
        try:
            choice = Prompt.ask(
                "Proceed anyway?",
                choices=["y", "n"],
                default="n",
                show_choices=True,
            )
        except KeyboardInterrupt:
            coiled.add_interaction(action="cli-hello:KeyboardInterrupt", success=False)
            return False

        coiled.add_interaction("cli-hello:messy-software-continue", success=True, choice=choice)
        if choice == "y":
            if msg_missing:
                live_panel_print(msg_missing, msg_ipython, panel_kwargs={"box": box.SIMPLE})
            else:
                live_panel_print(msg_ipython)
            result = ask_and_run_example(name=name, missing=missing, filename=script_path)
            return result
        else:
            console.print("See you in a minute with that new software environment :wave:")
            return True
    else:
        live_panel_print(msg_start, Rule(style="grey"), msg_code, Rule(style="grey"), msg_missing, msg_ipython)
        result = ask_and_run_example(name=name, missing=missing, filename=script_path)

    return result


def get_conda_dependencies(deps):
    if "dask" in deps:
        # These are included with `dask` on conda-forge
        deps = [d for d in deps if d not in ("pandas", "bokeh", "pyarrow")]
    deps = [PYPI_TO_CONDA.get(p, p) if p not in ("dask", "matplotlib") else p for p in deps]
    return deps


def messy_software_message(dependencies):
    msg_mixed_channels = ""
    if has_mixed_conda_channels():
        msg_mixed_channels = "has packages from multiple conda channels"

    msg_system_macos = ""
    if has_macos_system_python():
        msg_system_macos = "is using the macOS system Python"

    msg = ""
    recommendation = ""
    if msg_mixed_channels or msg_system_macos:
        formatted_dependencies = " \\\n\t".join(get_conda_dependencies(dependencies))
        if msg_mixed_channels:
            recommendation = f"""I notice you have conda installed. Making a new environment is easy.

```bash
conda create -n coiled -c conda-forge -y {formatted_dependencies}
conda activate coiled
coiled hello
```
"""
        else:
            recommendation = f"""Making a new environment with conda is easy.

```bash
curl -L -O \\
    "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
conda create -n coiled -c conda-forge -y {formatted_dependencies}
conda activate coiled
coiled hello
```
"""

        msg = Panel(
            Group(
                Markdown(
                    f"""
We're about to run a fun Python example on the cloud.  
But, this Python environment {msg_mixed_channels or msg_system_macos},
which makes it kinda messy.

Normally, Coiled copies your local environment to the cloud machines (no Docker!)
I'm not confident we'll be able to copy an environment this messy though.

You have some options:
-  Make a fresh and clean virtual environment (recommended!)
-  Use your own Docker image (but only if you love docker)
-  Try anyway!

{recommendation}

""".strip()  # noqa
                ),
            ),
            title=f"[{PRIMARY_COLOR}]Whoa! Messy Python environment[/{PRIMARY_COLOR}]",
        )

    return msg
