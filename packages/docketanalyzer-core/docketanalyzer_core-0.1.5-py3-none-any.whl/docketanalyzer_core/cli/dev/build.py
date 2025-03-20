import os
import re
import shutil
from pathlib import Path

import click

from ... import env


def parse_version(version_str: str) -> tuple[int, ...]:
    """Parse a version string into a tuple of integers.

    Args:
        version_str: Version string in format "x.y.z"

    Returns:
        Tuple of integers representing the version
    """
    return tuple(map(int, version_str.split(".")))


def is_valid_increment(v1: tuple[int, ...], v2: tuple[int, ...]) -> tuple[bool, str]:
    """Check if v2 is a valid semantic version increment from v1.

    Args:
        v1: First version as a tuple of integers
        v2: Second version as a tuple of integers

    Returns:
        Tuple containing (is_valid, message)
    """
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


def compare_versions(version1: str, version2: str) -> tuple[bool, str]:
    """Validate version increment.

    Args:
        version1: First version string
        version2: Second version string

    Returns:
        Tuple containing (is_valid, message)
    """
    v1 = parse_version(version1)
    v2 = parse_version(version2)

    result, message = is_valid_increment(v1, v2)
    return result, message


def get_version_from_pyproject(pyproject_path: Path) -> str:
    """Extract version from pyproject.toml file.

    Args:
        pyproject_path: Path to pyproject.toml file

    Returns:
        Version string
    """
    import tomli

    content = pyproject_path.read_text(encoding="utf-8")
    pyproject_data = tomli.loads(content)
    return pyproject_data["project"]["version"]


def update_version_in_pyproject(pyproject_path: Path, new_version: str) -> None:
    """Update version in pyproject.toml file.

    Args:
        pyproject_path: Path to pyproject.toml file
        new_version: New version string to set
    """
    content = pyproject_path.read_text()
    updated_content = re.sub(
        r'(version\s*=\s*")[^"]+(")', r"\g<1>" + new_version + r"\g<2>", content
    )
    pyproject_path.write_text(updated_content)


def update_version(version: str) -> str:
    """Prompt user to update version and validate the input.

    Args:
        version: Current version string

    Returns:
        New version string (or unchanged if user didn't provide one)
    """
    while 1:
        new_version = input(
            f"Current version is {version}. Enter new version or leave blank to keep: "
        )
        if not new_version:
            new_version = version
        result, message = compare_versions(version, new_version)
        if result:
            break
        print("Invalid version change:", message)
    return new_version


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

    pyproject_path = package_dir / "pyproject.toml"
    if not pyproject_path.exists():
        raise FileNotFoundError(f"pyproject.toml not found in {package_dir}")

    current_version = get_version_from_pyproject(pyproject_path)
    new_version = update_version(current_version)

    if current_version != new_version:
        update_version_in_pyproject(pyproject_path, new_version)
        print(f"Updated version in pyproject.toml to {new_version}")

    cmd = f"cd {package_dir} && python -m build"
    print(f"Building package with command: {cmd}")
    os.system(cmd)

    if push:
        cmd = f"pip install -e {package_dir}"
        print(f"Installing package with command: {cmd}")
        os.system(cmd)

        cmd = f"twine upload {dist_dir}/*"
        if env.PYPI_TOKEN is not None:
            cmd += f" -u __token__ -p {env.PYPI_TOKEN}"
        print(f"Uploading to PyPI with command: {cmd}")
        os.system(cmd)

        shutil.rmtree(dist_dir)
