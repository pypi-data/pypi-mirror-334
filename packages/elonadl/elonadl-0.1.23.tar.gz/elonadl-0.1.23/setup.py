from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="elonadl",
    version="0.1.23",
    author="vichmartins",
    packages=["elonadl"],
    description="A Installer to download and setup ElonaPlusCustom-GX on Windows.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.10',
    install_requires=['pywin32', 'requests', 'winshell']
)
