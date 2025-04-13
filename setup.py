from setuptools import setup, find_packages

setup(
    name="vectorial_economics",
    version="0.1.0",
    description="Modelo de análise econômica vetorial para avaliação de carteiras em DeFi",
    author="Thiago Martins",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "networkx>=2.6.0",
        "jupyter>=1.0.0",
        "notebook>=6.4.0"
    ],
    python_requires=">=3.8",
) 