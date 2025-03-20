from setuptools import setup, find_packages
from pathlib import Path

setup(
    name="tranci",
    version="1.0.0",
    description="Tranci: a no-dependencies, lightweight, easy-to-use ANSI library",
    long_description=(Path(__file__).parent / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author="Butterroach",
    author_email="butterroach@outlook.com",
    url="https://github.com/Butterroach/tranci",
    license="LGPLv3+",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    project_urls={
        "Source": "https://github.com/Butterroach/tranci",
        "Bug Tracker": "https://github.com/Butterroach/tranci/issues",
    },
)
