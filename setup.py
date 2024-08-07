from setuptools import setup, find_packages

setup(
    name="ACALLM",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "ollama",
    ],
    entry_points={
        "console_scripts": [
            "prompt=src.prompt:prompt",
        ],
    },
)
