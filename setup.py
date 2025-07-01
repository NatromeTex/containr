import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    description = fh.read()

setuptools.setup(
    name="containr",
    version="0.0.1",
    author="Natrome Tex",
    author_email="natrometex2014@gmail.com",
    package_dir={"": "src"},
    packages=["containr"],
    description="A CLI tool that allows you to create self-contained project folders without files littering your root folders",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/NatromeTex/containr",
    license="MIT",
    python_requires=">=3.9",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "containr=containr.cli:main",
        ],
    },
)
