# setup.py
from setuptools import setup, find_packages

setup(
    name="code2pdf",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "code2pdf = code_to_pdf.cli:main",
        ],
    },
    install_requires=[
        "weasyprint",
        "pygments",
        "pathspec",
        "binaryornot",
    ],
)
