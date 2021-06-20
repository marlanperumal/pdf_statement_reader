from pdf_statement_reader.parse import format_negatives


def test_format_negatives():
    assert format_negatives(123.45) == "123.45"
    assert format_negatives(-123.45) == "-123.45"
    assert format_negatives(0) == "0"
    assert format_negatives("123.45") == "123.45"
    assert format_negatives("-123.45") == "-123.45"
    assert format_negatives("0") == "0"
    assert format_negatives("123.45-") == "-123.45"


from pdf_statement_reader.parse import format_currency_number


def test_format_currency_number():
    assert format_currency_number('123.45') == "123.45"
    assert format_currency_number('$123.45') == "123.45"
    assert format_currency_number('$123.45 CR') == "123.45"
    assert format_currency_number('-1,234.56') == "-1234.56"
    assert format_currency_number('1,234.56-') == "-1234.56"
    assert format_currency_number('1,234.56 DR') == "-1234.56"
    assert format_currency_number('-$1,234.56 dr') == "-1234.56"
    assert format_currency_number('0') == "0"
    assert format_currency_number('-1') == "-1"
    assert format_currency_number('.12') == ".12"
    assert format_currency_number('“1”') == "1"
