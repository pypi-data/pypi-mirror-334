from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="slid",
    version="0.1.0",
    author="Ismael Faro",
    author_email="ismael.faro.sertage@gmail.com",
    description="A terminal-based markdown slide presentation tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ismaelfaro/slid.py",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    py_modules=["slid"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
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
)
