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
        "psycopg2",
        "fastapi",
        "uvicorn[standard]"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6, <3.8.8',
    # Due to issues with `scapy` v2.4.4, minidetector doesn't work with newer versions of Python such as Python 3.8.8, 3.9
)
