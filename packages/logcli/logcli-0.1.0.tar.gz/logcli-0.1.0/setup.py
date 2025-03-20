from setuptools import setup, find_packages

setup(
    name="logcli",
    version="0.1.0",
    packages=find_packages(),  # Finds all packages inside logcli/
    install_requires=[
        "requests",
        "click",
        "rich",
        "time",
        "os",
        "sys",
        "json",
        "argparse"
    ],
    entry_points={
        "console_scripts": [
            "logcli=logcli.main:main",  # Ensure this points to main()
        ],
    },
)
