import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="minidetector",
    version="0.0.2",
    author="Amit Itzkovitch",
    author_email="amit7itz@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        "scapy",
        "sqlalchemy>=1.3,<1.4",
        "psycopg2-binary",
        "pyfiglet",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
