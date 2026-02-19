import os
import tomllib
from os.path import join as pjoin

def load_toml(f_path: str, f_name: str = "") -> dict[str, any]:
    if not f_name == "":
        f_path = pjoin(f_path, f_name)

    if not f_path.endswith(".toml"):
        f_path += ".toml"

    if not os.path.exists(f_path):
        print(f'No existe el archivo {f_path}.')
        return {}
    with open(f_path, 'r') as toml_file:
        return tomllib.loads(toml_file.read())