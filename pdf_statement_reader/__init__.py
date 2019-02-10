import click
import os
import json
import pandas as pd

from pdf_statement_reader.decrypt import decrypt_pdf
from pdf_statement_reader.parse import parse_statement
from pdf_statement_reader.validate import validate_statement


@click.group()
def cli():
    """Utility for reading bank and other statements in pdf form"""
    pass


@cli.command()
@click.argument("input_filename", type=click.Path(exists=True))
@click.argument("output_filename", type=click.Path(), required=False)
@click.option('--password', "-p", prompt=True, hide_input=True)
def decrypt(input_filename, output_filename=None, password=None):
    """Decrypts a pdf file

    Uses pikepdf to open an encrypted pdf file and then save the unencrypted version.
    If no output_filename is specified then overwrites the original file.
    """

    decrypt_pdf(input_filename, output_filename, password)
    click.echo("Decrypted {} and saved as {}".format(input_filename, output_filename))


@cli.command()
@click.argument("input_filename", type=click.Path(exists=True))
@click.argument("output_filename", type=click.Path(), required=False)
@click.option("--config", "-c", "config_spec", default="za.absa.cheque")
def pdf2csv(input_filename, output_filename=None, config_spec=None):
    """Converts a pdf statement to a csv file using a given format"""

    if output_filename is None:
        output_filename = input_filename.split(".pdf")[0] + ".csv"

    local_dir = os.path.dirname(__file__)
    config_dir = os.path.join(*config_spec.split(".")[:-1])
    config_file = config_spec.split(".")[-1] + ".json"
    config_path = os.path.join(local_dir, "config", config_dir, config_file)
    with open(config_path) as f:
        config = json.load(f)

    df = parse_statement(input_filename, config)
    df.to_csv(output_filename, index=False, float_format="%.2f")
    click.echo("Converted {} and saved as {}".format(input_filename, output_filename))


@cli.command()
@click.argument("input_filename", type=click.Path(exists=True))
@click.option("--config", "-c", "config_spec", default="za.absa.cheque")
def validate(input_filename, output_filename=None, config_spec=None):
    """Validates the csv statement rolling balance"""

    local_dir = os.path.dirname(__file__)
    config_dir = os.path.join(*config_spec.split(".")[:-1])
    config_file = config_spec.split(".")[-1] + ".json"
    config_path = os.path.join(local_dir, "config", config_dir, config_file)
    with open(config_path) as f:
        config = json.load(f)

    statement = pd.read_csv(input_filename)
    valid = validate_statement(statement, config)

    if valid:
        click.echo("Statement is valid")
    else:
        click.echo("Statement is invalid")

    return valid
