from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name="pdf_statement_reader",
    version="0.1.0",
    description="PDF Statement Reader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marlanperumal/pdf_statement_reader",
    author="Marlan Perumal",
    author_email="marlan.perumal@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="bank statement pdf digitise",
    packages=find_packages(exclude=["contrib", "docs", "test"]),
    python_requires='>=3.5',
    install_requires=['pikepdf', 'tabula-py', 'pandas', 'numpy', "click"],
    extras_require={
        "dev": ["check-manifest"],
        "test": ["pytest", "coverage"]
    },
    entry_points={
        "console_scripts": [
            "psr=pdf_statement_reader:cli"
            # "decrypt=pdf_statement_reader.decrypt:decrypt_pdf_cli",
            # "pdf2csv=pdf_statement_reader.parse:pdf2csv",
            # "validate=pdf_statement_reader.validate:validate_csv",
        ]
    },
    project_urls={
        "Bug Reports": "https://github.com/marlanperumal/pdf_statement_reader/issues",
        "Source": "https://github.com/marlanperumal/pdf_statement_reader"
    }
)
