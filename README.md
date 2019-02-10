# PDF Statement Reader
[![Build Status](https://travis-ci.com/marlanperumal/pdf_statement_reader.svg?branch=master)](https://travis-ci.com/marlanperumal/pdf_statement_reader)

Python library and command line tool for parsing pdf bank statements

Inspired by https://github.com/antonburger/pdf2csv

## Installation

Clone this repository

```
git@github.com:marlanperumal/pdf_statement_reader.git
```

Install it with pip (preferably in a virtual environment)

```
pip install -e pdf_statement_reader
```

## Usage

Provides a command line application `psr`

```
Usage: psr [OPTIONS] COMMAND [ARGS]...

  Utility for reading bank and other statements in pdf form

Options:
  --help  Show this message and exit.

Commands:
  decrypt   Decrypts a pdf file Uses pikepdf to open an encrypted pdf file...
  pdf2csv   Converts a pdf statement to a csv file using a given format
  validate  Validates the csv statement rolling balance
```

### decrypt

```
Usage: psr decrypt [OPTIONS] INPUT_FILENAME [OUTPUT_FILENAME]

  Decrypts a pdf file

  Uses pikepdf to open an encrypted pdf file and then save the unencrypted
  version. If no output_filename is specified then overwrites the original
  file.

Options:
  -p, --password TEXT
  --help               Show this message and exit.
```

### pdf2csv

```
Usage: psr pdf2csv [OPTIONS] INPUT_FILENAME [OUTPUT_FILENAME]

  Converts a pdf statement to a csv file using a given format

Options:
  -c, --config TEXT
  --help             Show this message and exit.
```

### validate

```
Usage: psr validate [OPTIONS] INPUT_FILENAME

  Validates the csv statement rolling balance

Options:
  -c, --config TEXT
  --help             Show this message and exit.
```
