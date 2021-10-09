from setuptools import setup

setup(
    name="Moire",
    version="0.1",
    packages=["moire"],
    url="https://github.com/enzet/Moire",
    license="",
    author="Sergey Vartanov",
    author_email="me@enzet.ru",
    description="Simple extendable markup",
    entry_points={
        "console_scripts": ["moire=moire.main:main"],
    },
)
