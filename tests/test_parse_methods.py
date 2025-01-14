from pdf_statement_reader.parse import format_negatives


def test_format_negatives():
    assert format_negatives(123.45) == "123.45"
    assert format_negatives(-123.45) == "-123.45"
    assert format_negatives(0) == "0"
    assert format_negatives("123.45") == "123.45"
    assert format_negatives("-123.45") == "-123.45"
    assert format_negatives("0") == "0"
    assert format_negatives("123.45-") == "-123.45"
