from setuptools import setup, find_packages

setup(
    name="physics-formulas-pawel",
    version="1.0.0",  # Wersja pakietu
    author="Dominik Pelc",
    author_email="twojemail@example.com",
    description="A package for physics formulas",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/twoj_github/physics-formulas",  # Twój repozytorium GitHub
    packages=find_packages(),  # Automatyczne znajdowanie pakietów
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],  # Tutaj możesz dodać zależności, np. ['numpy']
    python_requires=">=3.6",
)
