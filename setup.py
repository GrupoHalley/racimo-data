from setuptools import setup, find_packages

setup(
    name="racimo-data",
    version="0.1.0",
    description="Herramientas para descargar el último dataset de DatLab (RACIMO Orquídeas)",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.5",
        "requests>=2.28",
    ],
    python_requires=">=3.9",
)
