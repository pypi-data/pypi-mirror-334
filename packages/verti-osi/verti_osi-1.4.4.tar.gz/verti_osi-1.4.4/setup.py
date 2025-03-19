from setuptools import setup, find_packages

setup(
    name="verti-osi",
    version="1.4.4",
    packages=find_packages(where="src"),
    author="VTB Wanderer DG",
    author_email="vtb.wanderers63@gmail.com",
    description="A simple Python package",
    url="https://github.com/vtb-wanderers63/py-logging-module",
    package_dir={"": "src"},
    install_requires=["typer"],  # Add other dependencies as needed
    entry_points={
        "console_scripts": [
            "verti-osi=vertibit_osi_image_generator.cli:app",  # Corrected entry point
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)