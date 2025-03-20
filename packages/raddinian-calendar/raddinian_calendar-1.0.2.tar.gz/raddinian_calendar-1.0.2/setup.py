from setuptools import setup, find_packages

setup(
    name="raddinian-calendar",
    version="1.0.2",
    description="A module to convert between Raddinian and Gregorian calendars.",
    author="Violet Radd",
    author_email="metatronzero199@gmail.com",
    url="https://github.com/violetradd/raddinian-calendar",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
