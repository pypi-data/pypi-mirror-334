from setuptools import setup, find_packages

setup(
    name="observatoriofcca",
    version="0.1.17",
    packages=find_packages(),
    install_requires=["requests"],
    author="Oscar de la Torre-Torres, Rodolfo López",
    author_email="oscar.delatorre.torres@umich.mx",
    maintainer="Felipe Andoni Luna Campos",
    maintainer_email="fluna@umich.mx",
    description="API - Observatorio de gestión pública e inteligencia de mercados",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://sites.google.com/umich.mx/observatoriofcca",  # Replace with your repository URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
