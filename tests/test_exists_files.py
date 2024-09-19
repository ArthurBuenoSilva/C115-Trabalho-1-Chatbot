import os


def test_flake8_config_exists():
    assert os.path.exists(".flake8")


def test_gitignore_exists():
    assert os.path.exists(".gitignore")


def test_pyproject_toml_exists():
    assert os.path.exists("pyproject.toml")


def test_requirements_txt_exists():
    assert os.path.exists("requirements.txt")


def test_readme_exists():
    assert os.path.exists("README.md")
