#!/usr/bin/env python
"""Start a new project in my_projects/ from the starter template.

    python scripts/new_project.py space_cat
    -> my_projects/space_cat/platformio.ini and src/main.cpp, ready to build and upload:
       pio run -d my_projects/space_cat -t upload

Names are lowercase English letters, digits and underscores (they become folder names that every tool accepts).
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "templates" / "starter"
PROJECTS = ROOT / "my_projects"
NAME = re.compile(r"[a-z][a-z0-9_]{1,39}")


def create(name, projects=PROJECTS):
    if not NAME.fullmatch(name):
        raise ValueError(
            f"'{name}' is not a usable name: use 2-40 lowercase English letters, digits or _, starting with a letter"
        )
    target = projects / name
    if target.exists():
        raise FileExistsError(f"{target} already exists: pick another name or keep working in it")
    shutil.copytree(TEMPLATE, target)
    for path in target.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            path.write_text(text.replace("{{NAME}}", name), encoding="utf-8")
    return target


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("name")
    args = parser.parse_args(argv)
    try:
        target = create(args.name)
    except (ValueError, FileExistsError) as error:
        sys.exit(str(error))
    print(f"Created {target.relative_to(ROOT)}")
    print(f"Build and upload: pio run -d {target.relative_to(ROOT).as_posix()} -t upload")
    return 0


if __name__ == "__main__":
    sys.exit(main())
