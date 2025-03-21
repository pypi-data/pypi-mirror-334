from setuptools import setup, find_packages

# Lendo o README.md para exibir no PyPI
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="embedded_adaptive_stacking_keras",
    version="0.7",
    author="Matheus Lima Maturano Martins de Castro",
    description="Biblioteca para detecção de outliers baseada em Stacking com Keras",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Isso permite a formatação Markdown no PyPI
    packages=find_packages(),
    install_requires=[
        "tensorflow>=2.5.0",
        "numpy",
        "matplotlib"
    ],
    python_requires=">=3.7",
)
