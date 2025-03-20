from setuptools import setup, find_packages

setup(
    name="minaki-cli",
    version="0.1.0",
    author="Andrew Polykandriotis",
    author_email="andrew@minakilabs.com",
    description="A modular and extensible CLI tool for executing commands and managing plugins.",
    long_description="Minaki CLI is a lightweight, extensible command-line tool that allows users to execute modular commands, manage plugins, and interact with system utilities. It supports dynamic plugin management and seamless shell command execution.",
    long_description_content_type="text/plain",
    url="https://github.com/minakilabs/minaki-cli",
    packages=find_packages(include=["minaki*", "commands*"]),
    install_requires=[
        "click>=8.0.3",
        "requests>=2.25.1",
        "art>=6.4",
        "gitpython>=3.1.44"
    ],
    entry_points={
        "console_scripts": [
            "minaki=minaki.cli:minaki"
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Build Tools",
        "Topic :: System :: Shells"
    ],
    python_requires=">=3.6",
    include_package_data=True,
    zip_safe=False
)
