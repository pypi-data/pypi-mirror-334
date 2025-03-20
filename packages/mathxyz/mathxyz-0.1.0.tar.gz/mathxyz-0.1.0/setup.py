from setuptools import setup, find_packages

setup(
    name="mathxyz",
    version="0.1.0",
    author="Muhammad Taha Gorji",
    author_email="MohammadTahaGorjiProfile@gmail.com",
    description="A state-of-the-art math solver library using advanced symbolic, numerical.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mr-r0ot/mathxyz",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "sympy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)