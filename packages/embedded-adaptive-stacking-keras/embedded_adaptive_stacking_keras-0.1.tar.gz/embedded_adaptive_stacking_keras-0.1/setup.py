from setuptools import setup, find_packages

setup(
    name="embedded_adaptive_stacking_keras",
    version="0.1",
    author="Matheus Lima Maturano Martins de Castro",
    description="Biblioteca para detecção de outliers baseada em Stacking com Keras",
    packages=find_packages(),
    install_requires=[
        "tensorflow>=2.5.0",
        "numpy",
        "matplotlib"
    ],
    python_requires=">=3.7",
)
