from setuptools import setup, find_packages

setup(
    name="bgm-net",  # Unique name on PyPI
    version="0.1.1",  # Version number
    author="DanXvo",
    author_email="data.com0010@gmail.com",
    description="Python library that made for Multiplayer games.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/DanXvoIsMe/BGM",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests",
    ],
    python_requires=">=3.6",
)
