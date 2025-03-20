from setuptools import setup, find_packages
from pathlib import Path

setup(
    name="kiwi-di",
    version="0.1.1",
    packages=find_packages(),
    description="A decorator-based dependency injection tool.",
    long_description_content_type="text/markdown",
    long_description=(Path(__file__).parent / "README.md").read_text(),
    python_requires=">=3.11, <=3.13",
)