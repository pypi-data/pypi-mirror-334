from setuptools import setup, find_packages

def get_version():
    version = {}
    with open("fmeta/version.py") as f:
        exec(f.read(), version)
    return version["__version__"]

setup(
    name="fmeta",
    version=get_version(),
    description="A small package to scan directories and list file metadata in a tabular format.",
    long_description=open("readme.md").read(),
    long_description_content_type="text/markdown",
    author="Benevant Mathew",
    author_email="benevantmathewv@gmail.com",
    license="MIT",
    packages=find_packages(include=["fmeta"]),
    install_requires=[
        "pandas",
        "tkinter",  # Required for GUI
    ],
    entry_points={
        "console_scripts": [
            "fmeta = fmeta.main:main",  # Entry point calls `main`
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Topic :: System :: Filesystems",
    ],
    python_requires=">=3.7",
)
