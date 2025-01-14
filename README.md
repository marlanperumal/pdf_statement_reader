# PDF Statement Reader
[![PyPI version](https://badge.fury.io/py/pdf-statement-reader.svg)](https://badge.fury.io/py/pdf-statement-reader)
[![Coverage Status](https://coveralls.io/repos/github/marlanperumal/pdf_statement_reader/badge.svg)](https://coveralls.io/github/marlanperumal/pdf_statement_reader)

Python library and command line tool for parsing pdf bank statements

Inspired by https://github.com/antonburger/pdf2csv

## Objectives

Banks generally send account statements in pdf format. These pdfs are often encrypted, the pdf format is difficult to extract tables from and when you finally get the table out it's in a non tidy format. This package aims to help by providing a library of functions and a set of command line tools for converting these statements into more useful formats such as csv files and pandas dataframes.

## Installation

Python and package management have been set up with [uv](https://docs.astral.sh/uv/). With uv installed and the repo cloned run

```bash
uv sync
```

The CLI tool can then be invoked with

```bash
uv run psr
```

Alternatively you can use the `uvx` command to run the tool without installing with

```bash
uvx --from pdf-statement-reader psr
```

Or to be less verbose on each call first run

```bash
uv tool install pdf-statement-reader
```

Then you'll be able to simply run

```bash
psr
```

### Troubleshooting

This package uses [tabula-py](https://github.com/chezou/tabula-py) under the hood, which itself is a wrapper for [tabula-java](https://github.com/tabulapdf/tabula-java). You thus need to have java installed for it to work. If you have any errors complaining about java, checkout out the `tabula-py` page for troubleshooting advice.

In the future, we hope to move to a pure python implementation.

## Usage

The package provides a command line application `psr`

```
Usage: psr [OPTIONS] COMMAND [ARGS]...

  Utility for reading bank and other statements in pdf form

Options:
  --help  Show this message and exit.

Commands:
  bulk      Bulk converts all files in a folder
  decrypt   Decrypts a pdf file Uses pikepdf to open an encrypted pdf file...
  pdf2csv   Converts a pdf statement to a csv file using a given format
  validate  Validates the csv statement rolling balance
```

## Configuration

PDF files are notoriously difficult to extract data from. (Here's a nice [blog post](https://www.propublica.org/nerds/heart-of-nerd-darkness-why-dollars-for-docs-was-so-difficult) on why). For a really good semi-manual GUI solution, check out [tabula](https://tabula.technology/). In fact this package uses tabula's pdf parsing library under the hood.

Since bank statements are generally of the same (if inconvenient) format, we can set up a configuration to tell the tool how to grab the data.

For each type of bank statement, the exact format will be different. A config file holds the instructions for how to process the raw pdf. For now the only config supported is for Cheque account statements from Absa bank in South Africa. 

To set up a different statement, you can simply add a new config file and then tell the `psr` tool to use it. These config files are stored in a folder structure as follows:

    config > [country code] > [bank] > [statement type].json

So for example the default config is stored in

    config > za > absa > cheque.json

The config spec is a code of the form

    [country code].[bank].[statement type]

Once again for the default this will be

    za.absa.cheque

The configuration file itself is in JSON format. Here's the Absa cheque account one with some commentary to explain what each field does.

```json5
{
    "$schema": "https://raw.githubusercontent.com/marlanperumal/pdf_statement_reader/develop/pdf_statement_reader/config/psr_config.schema.json",
    // Describes the page layout that should be scanned
    "layout": { 
        // Default layout for all pages not otherwise defined
        "default": {
            // The page coordinates in containing the table in pts 
            // [top, left, bottom, right]
            "area": [280, 27, 763, 576],
            // The right x coordinate of each column in the table
            "columns": [83, 264, 344, 425, 485, 570]
        },
        // Layout for the first page
        "first": {
            "area": [480, 27, 763, 576],
            "columns": [83, 264, 344, 425, 485, 570]
        }
    },

    // The columns names to be used as they exactly appear
    // in the statement
    "columns": {
        "trans_date": "Date",
        "trans_type": "Transaction Description",
        "trans_detail": "Transaction Detail",
        "debit": "Debit Amount",
        "credit": "Credit Amount",
        "balance": "Balance"
    },

    // The order of the columns to be output in the csv
    "order": [
        "trans_date",
        "trans_type",
        "trans_detail",
        "debit",
        "credit",
        "balance"
    ],

    // Specifies any cleaning operations required
    "cleaning": {
        // Convert these columns to numeric
        "numeric": ["debit", "credit", "balance"],
        // Convert these columns to date
        "date": ["trans_date"],
        // Use this date format to parse any date columns
        "date_format": "%d/%m/%Y",
        // For cases where the transaction detail is stored
        // in the next line below the transaction type
        "trans_detail": "below",
        // Only keep the rows where these columns are populated
        "dropna": ["balance"]
    }
}
```

These were the configuration options that were required for the default format. It is envisaged that as more formats are added, the list of options will grow.

This format is also captured in `pdf_statement_rader/config/psr_config.schema.json` as a [json-schema](https://json-schema.org/understanding-json-schema/index.html). If you're using vscode or some other compatible text editor, you should get autocompletion hints as long as you include that `$schema` tag at the top of your json file.

A key part in setting up a new configuration is getting the page coordinates for the area and columns. The easiest way to do this is to run the [tabula GUI](https://tabula.technology/), autodetect the page areas, save the settings as a template, then download and inspect json template file. It's not a one-to-one mapping to the psr config but hopefully it will be a good starting point.

## CLI API

### decrypt

```
Usage: psr decrypt [OPTIONS] INPUT_FILENAME [OUTPUT_FILENAME]

  Decrypts a pdf file

  Uses pikepdf to open an encrypted pdf file and then save the unencrypted
  version. If no output_filename is specified then overwrites the original
  file.

Options:
  -p, --password TEXT  The pdf encryption password. If not supplied, it will
                       be requested at the prompt
  --help               Show this message and exit.
```

### pdf2csv

```
Usage: psr pdf2csv [OPTIONS] INPUT_FILENAME [OUTPUT_FILENAME]

  Converts a pdf statement to a csv file using a given format

Options:
  -c, --config TEXT  The configuration code defining how the file should be
                     parsed  [default: za.absa.cheque]
  --help             Show this message and exit.
```

### validate

```
Usage: psr validate [OPTIONS] INPUT_FILENAME

  Validates the csv statement rolling balance

Options:
  -c, --config TEXT  The configuration code defining how the file should be
                     parsed  [default: za.absa.cheque]
  --help             Show this message and exit.
```

### bulk

```
Usage: psr bulk [OPTIONS] FOLDER

  Bulk converts all files in a folder

Options:
  -c, --config TEXT          The configuration code defining how the file
                             should be parsed  [default: za.absa.cheque]
  -p, --password TEXT        The pdf encryption password. If not supplied, it
                             will be requested at the prompt
  -d, --decrypt-suffix TEXT  The suffix to append to the decrypted pdf file
                             when created  [default: _decrypted]
  -k, --keep-decrypted       Keep the a copy of the decrypted file. It is
                             removed by default
  -v, --verbose              Print verbose output while running
  --help                     Show this message and exit.
```
