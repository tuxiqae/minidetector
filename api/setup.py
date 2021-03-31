import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    print(long_description)

setuptools.setup(
    name="minidetector-api",
    version="0.0.1",
    author="Sagi Sarussi",
    author_email="sagis@sagis.dev",
    description="minidetector API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        "sqlalchemy>=1.3,<1.4",
        "psycopg2-binary",
        "fastapi",
        "uvicorn[standard]"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
