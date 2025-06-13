#!/usr/bin/env python3
"""Build and install mt7902 kernel modules with minimal user interaction.

This script compiles the driver modules contained in this repository,
installs them under ``/lib/modules/$(uname -r)/extra`` and loads the
required modules using ``modprobe``.

Run it with root privileges so it can copy files and load modules.
"""

import os
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
KERNEL_RELEASE = os.uname().release
MODULE_DEST = Path("/lib/modules") / KERNEL_RELEASE / "extra"


def run(cmd):
    """Run a shell command and raise ``CalledProcessError`` on failure."""
    print(f"$ {cmd}")
    subprocess.run(cmd, shell=True, check=True)


def build_modules():
    """Compile kernel modules using the repository Makefile."""
    run("make -C " + str(REPO_ROOT))


def find_built_modules():
    """Return a list of paths to built ``.ko`` files."""
    return [p for p in REPO_ROOT.rglob("*.ko")]


def install_modules(modules):
    """Copy compiled modules to the system module directory."""
    MODULE_DEST.mkdir(parents=True, exist_ok=True)
    for module in modules:
        target = MODULE_DEST / module.name
        run(f"cp {module} {target}")


def update_module_dependencies():
    """Run ``depmod`` so ``modprobe`` sees newly installed modules."""
    run("depmod -a")


def load_modules(modules):
    """Load modules using ``modprobe`` in the order provided."""
    for module in modules:
        name = module.stem
        run(f"modprobe {name}")


def main():
    build_modules()
    modules = find_built_modules()
    if not modules:
        print("No modules were built. Aborting.")
        return
    install_modules(modules)
    update_module_dependencies()
    load_modules(modules)
    print("Driver modules installed and loaded successfully.")


if __name__ == "__main__":
    main()
