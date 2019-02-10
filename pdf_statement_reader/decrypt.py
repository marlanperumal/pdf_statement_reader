from pikepdf import Pdf
import click


def decrypt_pdf(input_filename, output_filename=None, password=None):
    """Decrypts a pdf file

    Uses pikepdf to open an encrypted pdf file and then save the unencrypted version.
    If no output_filename is specified then overwrites the original file.
    If no password is supplied then checks if file is already unencrypted

    Args:
        input_filename: The source encrypted pdf file
        output_filename: The filename to write the decrypted file to
        password: The password on the encrypted pdf file

    Returns:
        True if decryption succeeded, False if the file was already unencrypted.
        If decryption fails, an error is raised

    Raises:
        FileNotFoundError: if output cannot be written
        PdfError: if the file is not a valid pdf
        PasswordError: if incorrect password supplied
    """
    if password is None:
        pdf = Pdf.open(input_filename)
        click.echo("{} was already unencrypted")
        return False

    if output_filename is None:
        output_filename = input_filename

    pdf = Pdf.open(input_filename, password)
    pdf.save(output_filename)
