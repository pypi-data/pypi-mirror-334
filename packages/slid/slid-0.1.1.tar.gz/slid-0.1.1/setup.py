from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="slid",
    version="0.1.1",
    author="Ismael Faro",
    author_email="ismael.faro.sertage@gmail.com",
    description="A terminal-based markdown slide presentation tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ismaelfaro/slid.py",
    py_modules=["slid"],  # Just specify the module
    package_dir={"": "src"},  # Tell setuptools where to find the module
    python_requires=">=3.7",
    install_requires=[
        "rich",
        "readchar",
        "pyperclip",
    ],
    entry_points={
        "console_scripts": [
            "slid=slid:main",
        ],
    },
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
)
