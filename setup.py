from setuptools import setup

with open("README.md") as input_file:
    long_description = input_file.read()

setup(
    name="Moire",
    version="0.1",
    packages=["moire"],
    url="https://github.com/enzet/Moire",
    license="MIT",
    author="Sergey Vartanov",
    author_email="me@enzet.ru",
    description="Simple extendable markup",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": ["moire=moire.main:main"],
    },
    install_requires=[],
)
