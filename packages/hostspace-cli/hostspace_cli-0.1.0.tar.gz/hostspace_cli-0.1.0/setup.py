from setuptools import setup, find_packages

setup(
    name="hostspace-cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "pyyaml>=6.0.0",
        "requests>=2.28.0",
        "rich>=12.0.0",
        "typer>=0.9.0",
    ],
    entry_points={
        "console_scripts": [
            "hs=hostspace.cli:main",
        ],
    },
)
