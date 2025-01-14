import click
import os
from os import listdir, remove
from os.path import isfile, join
import json
import pandas as pd

from pdf_statement_reader.decrypt import decrypt_pdf
from pdf_statement_reader.parse import parse_statement
from pdf_statement_reader.validate import validate_statement


def load_config(config_spec):
    """Loads configuration for a template statement

    For each type of bank statement, the exact format will be different.
    A config file holds the instructions for how to process the raw pdf.
    These config files are stored in a folder structure as follows:
        config > [country code] > [bank] > [statement type].json

    So for example the default config is stored in
        config > za > absa > cheque.json

    The config spec is a code of the form
        [country code].[bank].[statement type]

    Once again for the default this will be
        za.absa.cheque

    Args:
        config_spec: Code that resolves to a json file as explained above

    Returns:
        The configuration as a python object
    """
    local_dir = os.path.dirname(__file__)
    config_dir = os.path.join(*config_spec.split(".")[:-1])
    config_file = config_spec.split(".")[-1] + ".json"
    config_path = os.path.join(local_dir, "config", config_dir, config_file)
    with open(config_path) as f:
        config = json.load(f)
    return config


@click.group()
def cli():
    """Utility for reading bank and other statements in pdf form"""
    pass


@cli.command()
@click.argument("input_filename", type=click.Path(exists=True))
@click.argument("output_filename", type=click.Path(), required=False)
@click.option(
    "--password",
    "-p",
    prompt=True,
    hide_input=True,
    help="The pdf encryption password. If not supplied, it will be requested at the prompt",
)
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
@click.option(
    "--config",
    "-c",
    "config_spec",
    default="za.absa.cheque",
    show_default=True,
    help="The configuration code defining how the file should be parsed",
)
def pdf2csv(input_filename, output_filename=None, config_spec=None):
    """Converts a pdf statement to a csv file using a given format"""

    config = load_config(config_spec)

    if output_filename is None:
        output_filename = input_filename.split(".pdf")[0] + ".csv"

    df = parse_statement(input_filename, config)
    df.to_csv(output_filename, index=False, float_format="%.2f")
    click.echo("Converted {} and saved as {}".format(input_filename, output_filename))


@cli.command()
@click.argument("input_filename", type=click.Path(exists=True))
@click.option(
    "--config",
    "-c",
    "config_spec",
    default="za.absa.cheque",
    show_default=True,
    help="The configuration code defining how the file should be parsed",
)
def validate(input_filename, output_filename=None, config_spec=None):
    """Validates the csv statement rolling balance"""

    config = load_config(config_spec)

    statement = pd.read_csv(input_filename)
    valid = validate_statement(statement, config)

    if valid:
        click.echo("Statement is valid")
    else:
        click.echo("Statement is invalid")


@cli.command()
@click.argument("folder", type=click.Path(exists=True))
@click.option(
    "--config",
    "-c",
    "config_spec",
    default="za.absa.cheque",
    show_default=True,
    help="The configuration code defining how the file should be parsed",
)
@click.option(
    "--password",
    "-p",
    prompt=True,
    hide_input=True,
    help="The pdf encryption password. If not supplied, it will be requested at the prompt",
)
@click.option(
    "--decrypt-suffix",
    "-d",
    default="_decrypted",
    show_default=True,
    help="The suffix to append to the decrypted pdf file when created",
)
@click.option(
    "--keep-decrypted",
    "-k",
    is_flag=True,
    help="Keep the a copy of the decrypted file. It is removed by default",
)
@click.option(
    "--verbose", "-v", is_flag=True, help="Print verbose output while running"
)
def bulk(
    folder, config_spec, password, decrypt_suffix, keep_decrypted=False, verbose=False
):
    """Bulk converts all files in a folder"""

    config = load_config(config_spec)

    files = [f for f in listdir(folder) if isfile(join(folder, f))]

    for file in files:
        extension = file.split(".")[-1]
        if extension.lower() == "pdf":
            base_name = ".".join(file.split(".")[:-1])
            valid = False

            try:
                if verbose:
                    click.echo(file)
                decrypted_file = base_name + decrypt_suffix + "." + extension
                if verbose:
                    click.echo("decrypting...")
                decrypt_pdf(join(folder, file), join(folder, decrypted_file), password)
                if verbose:
                    click.echo("parsing...")
                df = parse_statement(join(folder, decrypted_file), config)
                if verbose:
                    click.echo("validating...")
                valid = validate_statement(df, config)
                if verbose:
                    click.echo("writing to csv...")
                df.to_csv(
                    join(folder, base_name + ".csv"), index=False, float_format="%.2f"
                )

                if not valid:
                    click.echo(click.style("Statement not valid", fg="yellow"))
                    raise

                click.echo(click.style("Converted {}".format(file), fg="green"))

            except Exception as e:
                if verbose:
                    click.echo(click.style(str(e), fg="yellow"))
                click.echo(click.style("Error on {}".format(file), fg="red"))

            finally:
                if not keep_decrypted:
                    if verbose:
                        click.echo("removing decrypted file...")
                    remove(join(folder, decrypted_file))
