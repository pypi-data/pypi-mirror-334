import os
import shutil
from pathlib import Path
from typing import Any

import click
import requests
import tomli
import tomli_w

from ... import EXTENSIONS, env


def get_pyproject_shared_config(module_name: str) -> dict[str, Any]:
    """Get the shared configuration that should be in all DA projects."""
    extension_modules = [f"docketanalyzer_{ext}" for ext in EXTENSIONS]
    return {
        "tool": {
            "ruff": {
                "lint": {
                    "select": [
                        "E",
                        "F",
                        "I",
                        "B",
                        "UP",
                        "N",
                        "SIM",
                        "PD",
                        "NPY",
                        "PTH",
                        "RUF",
                        "D",
                    ],
                    "ignore": ["D100", "D104", "N801"],
                    "isort": {
                        "known-first-party": ["docketanalyzer", *extension_modules],
                        "section-order": [
                            "future",
                            "standard-library",
                            "third-party",
                            "first-party",
                            "local-folder",
                        ],
                    },
                    "per-file-ignores": {"__init__.py": ["I001", "I002"]},
                    "pydocstyle": {"convention": "google"},
                },
            },
            "pytest": {
                "ini_options": {
                    "log_cli": True,
                    "log_cli_level": "INFO",
                    "addopts": f"-ra -q --cov={module_name} -m 'not cost'",
                    "testpaths": ["tests"],
                    "pythonpath": ".",
                    "markers": [
                        "cost: tests that incur real costs when run",
                        "local: requires credentials only available locally",
                    ],
                }
            },
        }
    }


def is_valid_increment(v1: tuple[int, ...], v2: tuple[int, ...]) -> tuple[bool, str]:
    """Check if v2 is a valid semantic version increment from v1."""
    if v1 == v2:
        return True, "Versions are identical"

    for i in range(3):
        if v2[i] > v1[i]:
            if v2[i] == v1[i] + 1 and v2[i + 1 :] == (0,) * (2 - i):
                level = "major" if i == 0 else "minor" if i == 1 else "patch"
                return (True, f"Valid increment at {level} level")
            else:
                return False, "Invalid increment"
        elif v2[i] < v1[i]:
            return False, "Second version is lower"

    return False, "Other issue"


def update_version(version: str) -> str:
    """Prompt user to update version and validate the input."""
    while 1:
        new_version = input(
            f"Current version is {version}. Enter new version or leave blank to keep: "
        )
        if not new_version:
            new_version = version

        version = tuple(map(int, version.split(".")))
        new_version = tuple(map(int, new_version.split(".")))
        result, message = is_valid_increment(version, new_version)
        if result:
            break
        print("Invalid version change:", message)
    return ".".join(map(str, new_version))


def update_dependency_version(dependency: str) -> str:
    """Update the version of a dependency if it is a docketanalyzer package."""
    if dependency.startswith("docketanalyzer"):
        package_with_extra = dependency.split(">=")[0]
        package_name = package_with_extra.split("[")[0]
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
        latest_version = response.json()["info"]["version"]
        return f"{package_with_extra}>={latest_version}"
    return dependency


def update_pyproject(package_dir: Path) -> str:
    """Update the pyproject.toml file with shared config and version info."""
    pyproject_path = package_dir / "pyproject.toml"
    config = tomli.loads(pyproject_path.read_text())
    module_name = config["project"]["name"].replace("-", "_")
    current_version = config["project"]["version"]

    new_version = update_version(current_version)

    if current_version != new_version:
        config["project"]["version"] = new_version
        print(f"Updating version in pyproject.toml to {new_version}")

    shared_config = get_pyproject_shared_config(module_name)
    config = {**config, **shared_config}

    config["project"]["dependencies"] = [
        update_dependency_version(dep) for dep in config["project"]["dependencies"]
    ]
    for extra in config["project"]["optional-dependencies"]:
        config["project"]["optional-dependencies"][extra] = [
            update_dependency_version(dep)
            for dep in config["project"]["optional-dependencies"][extra]
        ]

    pyproject_path.write_text(tomli_w.dumps(config))
    return module_name


@click.command()
@click.option("--push", is_flag=True, help="Push to PyPI after building")
def build(push):
    """Build the package in the current directory.

    Args:
        push (bool): Whether to push the package to PyPI after building
    Raises:
        FileNotFoundError: If pyproject.toml is not found in the current directory
        ValueError: If the version change is not valid
        Exception: If the build or upload process fails
    """
    package_dir = Path.cwd()
    dist_dir = package_dir / "dist"
    if dist_dir.exists():
        shutil.rmtree(dist_dir)

    module_name = update_pyproject(package_dir)

    cmd = f"cd {package_dir} && python -m build"
    print(f"Building package with command: {cmd}")
    os.system(cmd)

    if push:
        if "dev" in module_name:
            raise ValueError("You may not push dev to PyPi.")
        cmd = f"pip install -e {package_dir}"
        print(f"Installing package with command: {cmd}")
        os.system(cmd)

        cmd = f"twine upload {dist_dir}/*"
        if env.PYPI_TOKEN is not None:
            cmd += f" -u __token__ -p {env.PYPI_TOKEN}"
        print(f"Uploading to PyPI with command: {cmd}")
        os.system(cmd)

        shutil.rmtree(dist_dir)
