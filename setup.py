"""Setup configuration for lite package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip()]

setup(
    name="litellm-client",
    version="0.1.0",
    author="LiteLLM Contributors",
    author_email="",
    description="Unified interface for interacting with multiple LLM providers and vision models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/litellm",
    packages=find_packages(),
    package_dir={"": "."},
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "cli-litetext=app.cli.liteclient_cli:cli_interface",
        ],
    },
    py_modules=['lite'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
