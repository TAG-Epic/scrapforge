"""
Created by Epic at 7/27/20
"""
import click
from config import SCRAPMECHANIC_PATH
from pathlib import Path
import zipfile
import json
import os
from subprocess import run
from shutil import rmtree
from io import BytesIO

current_dir = os.getcwd()
applied_patch_path = Path(SCRAPMECHANIC_PATH) / "scrapforge.patch"


@click.group()
def main():
    pass


@main.command()
@click.argument("mod")
def install(mod):
    mod_file: Path = Path(mod)

    with zipfile.ZipFile(mod_file.name, "r") as zipped:
        zipped.extractall("temp/")

    extracted = Path("temp/")
    mod_config_file = extracted / "mod.info"
    patches_directory = extracted / "patches"

    if not mod_config_file.exists():
        return print("Corrupt mod! mod.info file does not exist")
    if not patches_directory.is_dir():
        return print("Corrupt mod! No patches was not found")

    with mod_config_file.open() as f:
        mod_config = json.load(f)

    if "name" not in mod_config.keys() and "banner" not in mod_config.keys():
        return print("Corrupt mod! No mod name was found")

    print(mod_config.get("banner", f"Installing {mod_config.get('name', '')}!"))

    applyPatches(patches_directory)

    rmtree(extracted)


def applyPatches(patch_dir: Path):
    for patch in patch_dir.glob("*"):
        if patch.is_dir():
            return applyPatches(patch)
        with patch.open("rb") as f:
            with applied_patch_path.open("wb+") as patch_file:
                patch_file.write(f.read())

        os.chdir(SCRAPMECHANIC_PATH)
        print(f"Installing patch {patch.name}")
        f = BytesIO()
        try:
            output = run(["git", "apply", "scrapforge.patch"], stderr=f, stdout=f)
        except:
            print(f"Mod install failed!")
            raise SystemExit()
        print("Patch installed!")
        os.chdir(current_dir)


main()
