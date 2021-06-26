import unittest
import pandas as pd
from pandas._testing import assert_frame_equal

from pdf_statement_reader.parse import format_negatives
from pdf_statement_reader.parse import format_currency_number
from pdf_statement_reader.parse import clean_prestrip
# from pdf_statement_reader.parse import clean_numeric
# from pdf_statement_reader.parse import clean_trans_detail
from pdf_statement_reader.parse import clean_unwrap
# from pdf_statement_reader.parse import clean_date
from pdf_statement_reader.parse import clean_case
# from pdf_statement_reader.parse import clean_dropna
# from pdf_statement_reader.parse import reorder_columns


def test_format_negatives():
    assert format_negatives(123.45) == "123.45"
    assert format_negatives(-123.45) == "-123.45"
    assert format_negatives(0) == "0"
    assert format_negatives("123.45") == "123.45"
    assert format_negatives("-123.45") == "-123.45"
    assert format_negatives("0") == "0"
    assert format_negatives("123.45-") == "-123.45"


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


def test_clean_prestrip():
 
    _df = pd.DataFrame([['Field1':["",""],
                         'Faction':["Test String", "Another test"]])
    _config = {'$schema': '',
               'columns': {'F1': 'Field1', 'Key': 'Faction'},
               'cleaning': {'prestrip': ['Key', 'test']}
              }

    df = _df
    config = _config
    assert clean_prestrip(df, config) == [['Field1':["","Test String"]]

    df = _df
    config = _config
    assert clean_prestrip(df, config) == []


def test_clean_unwrap():
    _df = pd.DataFrame({['Date':["01/01/2020","","","26/05/2020"],
                         'Faction':["Test String", "Another test","Short", "Last bit."]})
    _config = {'$schema': '',
               'columns': {'Key': 'Date', 'F2': 'Faction'},
               'cleaning': {'unwrap': ['Key', 'F2']}
              }

    df = _df
    config = _config
    assert clean_unwrap(df, config) == [['Date':["01/01/2020","","","26/05/2020"],
                         'Faction':["Test String Another test Short", "Another test","Short", "Last bit."]]


def test_clean_case():
    df1 = pd.DataFrame({'Faction':["test string", "ANOTHER TEst","shORT", "last Bit."]})
    df2 = pd.DataFrame({'Faction':["Test String", "Another Test","Short", "Last Bit."]})
    config = {'$schema': '',
               'cleaning': {'case': ['F1']},
               'columns': {'F1': 'Faction'}
              }

    assert_frame_equal(clean_case(df1, config), df2)
