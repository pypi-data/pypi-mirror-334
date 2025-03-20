from setuptools import setup, find_packages

setup(
    name="pdf-signer",
    version="0.1.2",
    description="A customizable PDF signature box generator",
    author="Roshan Yadav",
    author_email="roshany.ir.ry@gmail.com",
    packages=find_packages(),
    install_requires=[
        "PyMuPDF",
        "reportlab",
        "PyPDF2",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)