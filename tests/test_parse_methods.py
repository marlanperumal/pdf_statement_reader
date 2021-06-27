import unittest
import pandas as pd
from pandas._testing import assert_frame_equal

from pdf_statement_reader.parse import format_negatives
from pdf_statement_reader.parse import format_currency_number
from pdf_statement_reader.parse import clean_prestrip
# from pdf_statement_reader.parse import clean_numeric
# from pdf_statement_reader.parse import clean_trans_detail
from pdf_statement_reader.parse import clean_unwrap
from pdf_statement_reader.parse import clean_date
from pdf_statement_reader.parse import clean_case
from pdf_statement_reader.parse import clean_dropna
from pdf_statement_reader.parse import reorder_columns


def test_format_negatives():
    assert format_negatives(123.45) == "123.45"
    assert format_negatives(-123.45) == "-123.45"
    assert format_negatives(0) == "0"
    assert format_negatives("123.45") == "123.45"
    assert format_negatives("-123.45") == "-123.45"
    assert format_negatives("0") == "0"
    assert format_negatives("123.45-") == "-123.45"


def test_format_currency_number():
    assert format_currency_number("123.45") == "123.45"
    assert format_currency_number("$123.45") == "123.45"
    assert format_currency_number("$123.45 CR") == "123.45"
    assert format_currency_number("-1,234.56") == "-1234.56"
    assert format_currency_number("1,234.56-") == "-1234.56"
    assert format_currency_number("1,234.56 DR") == "-1234.56"
    assert format_currency_number("-$1,234.56 dr") == "-1234.56"
    assert format_currency_number("0") == "0"
    assert format_currency_number("-1") == "-1"
    assert format_currency_number(".12") == ".12"
    assert format_currency_number("“1”") == "1"


def test_clean_prestrip():
    df1 = pd.DataFrame({"Field1": ["", ""], "Faction": ["Test String", "Another test"]})
    df2 = pd.DataFrame({"Field1": [""], "Faction": ["Another test"]})
    config = {
        "$schema": "",
        "cleaning": {"prestrip": ["Key", "Test"]},
        "columns": {"F1": "Field1", "Key": "Faction"},
    }
    assert_frame_equal(
        clean_prestrip(df1, config).reset_index(drop=True), df2.reset_index(drop=True)
    )


def test_clean_unwrap():
    df1 = pd.DataFrame(
        {
            "Date": ["01/01/2020", pd.NA, pd.NA, "26/05/2020"],
            "Faction": ["Test String", "Another test", "Short", "Last bit."],
        }
    )
    df2 = pd.DataFrame(
        {
            "Date": ["01/01/2020", pd.NA, pd.NA, "26/05/2020"],
            "Faction": [
                "Test String Another test Short",
                "Another test",
                "Short",
                "Last bit.",
            ],
        }
    )
    config = {
        "$schema": "",
        "columns": {"Key": "Date", "F2": "Faction"},
        "cleaning": {"unwrap": ["Key", "F2"]},
    }
    assert_frame_equal(clean_unwrap(df1, config), df2)


def test_clean_date():
    df1 = pd.DataFrame({"Faction": ["01/02/03"]})
    df2 = pd.DataFrame({"Faction": ["2003-02-01"]})
    df2["Faction"] = pd.to_datetime(df2["Faction"])
    config = {
        "$schema": "",
        "cleaning": {
            "date": ["F1"],
            "date_format": "%d/%m/%y",
        },
        "columns": {"F1": "Faction"},
    }
    assert_frame_equal(clean_date(df1, config), df2)


def test_clean_case():
    df1 = pd.DataFrame(
        {"Faction": ["test string", "ANOTHER TEst", "shORT", "last Bit."]}
    )
    df2 = pd.DataFrame(
        {"Faction": ["Test String", "Another Test", "Short", "Last Bit."]}
    )
    config = {"$schema": "", "cleaning": {"case": ["F1"]}, "columns": {"F1": "Faction"}}
    assert_frame_equal(clean_case(df1, config), df2)


def test_clean_dropna():
    df1 = pd.DataFrame(
        {"Field1": [pd.NA, "1.23"], "Faction": ["Test String", "Another test"]}
    )
    df2 = pd.DataFrame({"Field1": ["1.23"], "Faction": ["Another test"]})
    config = {
        "$schema": "",
        "cleaning": {"dropna": ["F1"]},
        "columns": {"F1": "Field1"},
    }
    assert_frame_equal(
        clean_dropna(df1, config).reset_index(drop=True), df2.reset_index(drop=True)
    )


def test_reorder_columns():
    df1 = pd.DataFrame({"Col1": ["", ""], "Col2": ["Aa", "bB"], "Col3": ["xx", "ZZ"]})
    df2 = pd.DataFrame({"Col1": ["", ""], "Col3": ["xx", "ZZ"], "Col2": ["Aa", "bB"]})
    config = {"$schema": "", "order": ["Col1", "Col3", "Col2"]}
    config = {
        "$schema": "",
        "order": ["F1", "F3", "F2"],
        "columns": {"F1": "Col1", "F2": "Col2", "F3": "Col3"},
    }
    assert_frame_equal(
        reorder_columns(df1, config).reset_index(drop=True), df2.reset_index(drop=True)
    )

