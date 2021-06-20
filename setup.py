from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name="pdf_statement_reader",
    version="0.2.3",
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
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="bank statement pdf digitise",
    packages=find_packages(exclude=["contrib", "docs", "test"]),
    python_requires='>=3.6',
    install_requires=['pikepdf', 'tabula-py', 'pandas', 'numpy', "click"],
    include_package_data=True,
    extras_require={
        "dev": ["check-manifest"],
        "test": ["pytest", "coverage"]
    },
    entry_points={
        "console_scripts": [
            "psr=pdf_statement_reader:cli",
            "pdfsr=pdf_statement_reader:cli"
        ]
    },
    project_urls={
        "Bug Reports": "https://github.com/marlanperumal/pdf_statement_reader/issues",
        "Source": "https://github.com/marlanperumal/pdf_statement_reader"
    }
)
