from tabula import read_pdf
from pikepdf import Pdf
import pandas as pd
import numpy as np
import re
import logging


def get_raw_df(filename, num_pages, config):
    dfs = []
    _pandas_options = {"dtype": str}
    header = True
    if config["layout"].get("pandas_options"):
        _pandas_options.update(config["layout"].get("pandas_options"))
        if (
            config["layout"]["pandas_options"].get("header")
            and config["layout"]["pandas_options"].get("header") == "None"
        ):
            header = False

    for i in range(num_pages):
        if i == 0 and "first" in config["layout"]:
            area = config["layout"]["first"]["area"]
            columns = config["layout"]["first"]["columns"]
        else:
            area = config["layout"]["default"]["area"]
            columns = config["layout"]["default"]["columns"]

        df = read_pdf(
            filename,
            pages=i + 1,
            area=area,
            columns=columns,
            stream=True,
            guess=False,
            pandas_options=_pandas_options,
            java_options=[
                "-Dorg.slf4j.simpleLogger.defaultLogLevel=off",
                "-Dorg.apache.commons.logging.Log=org.apache.commons.logging.impl.NoOpLog",
            ],
        )
        if df is not None and len(df) > 0:
            dfs.extend(df)

    if not header:
        for df in dfs:
            df.columns = [config["columns"][col] for col in config["order"]]
    statement = pd.concat(dfs, sort=False).reset_index(drop=True)
    return statement


def clean_truncate(df, config):
    key = config["columns"][config["cleaning"]["truncate"][0]]
    value = config["cleaning"]["truncate"][1]
    if not df[df[key] == value].empty:
        df = df.iloc[: df[df[key] == value].index[0]]
    return df


def clean_prestrip(df, config):
    key = config["columns"][config["cleaning"]["prestrip"][0]]
    value = config["cleaning"]["prestrip"][1]
    df.dropna(subset=[key], inplace=True)
    # df.ix[:, ~df[key].str.match(value)== True]
    df = df[~df[key].str.match(value) == True]
    return df


def format_currency_number(s):
    DECIMAL_SEPARATOR = "."
    re_real = "[^\d" + DECIMAL_SEPARATOR + "]+"
    re_negative = "(?i)(^-|DR)|(-|DR$)"
    s = str(s)
    flag_negative = True if bool(re.search(re_negative, s)) else False
    s = re.sub(re_real, "", s)
    if flag_negative:
        s = "-" + s
    return s


def format_negatives(s):
    s = str(s)
    if s.endswith("-"):
        return "-" + s[:-1]
    else:
        return s


def clean_numeric(df, config):
    numeric_cols = [config["columns"][col] for col in config["cleaning"]["numeric"]]

    for col in numeric_cols:
        df[col] = df[col].apply(format_currency_number)
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def clean_trans_detail(df, config):
    trans_detail = config["columns"]["trans_detail"]
    trans_type = config["columns"]["trans_type"]
    balance = config["columns"]["balance"]

    df[trans_detail] = ""

    for i, row in df.iterrows():
        if i == 0:
            continue
        if np.isnan(row[balance]):
            df.loc[i - 1, trans_detail] = row[trans_type]
    return df


def clean_date(df, config):
    date_cols = [config["columns"][col] for col in config["cleaning"]["date"]]
    if "date_format" in config["cleaning"]:
        date_format = config["cleaning"]["date_format"]
    else:
        date_format = None
    if date_format == "%d %b":
        no_year = True
        year = df.iloc[0, 1][0:4]
        date_format += " %Y"
    else:
        no_year = False
    for col in date_cols:
        if no_year:
            df[col] += " " + year
        df[col] = pd.to_datetime(df[col], errors="coerce", format=date_format)
    return df


def clean_unwrap(df, config):
    key = config["columns"][config["cleaning"]["unwrap"][0]]
    val = config["columns"][config["cleaning"]["unwrap"][1]]
    j = 0
    for i, row in df.iterrows():
        if pd.isnull(row[key]):
            if pd.notna(df.loc[i, val]):
                df.loc[j, val] += " " + df.loc[i, val]
        else:
            j = i
    return df


def clean_case(df, config):
    cols = [config["columns"][col] for col in config["cleaning"]["case"]]
    for col in cols:
        df[col] = df[col].str.title()
    return df


def clean_dropna(df, config):
    drop_cols = [config["columns"][col] for col in config["cleaning"]["dropna"]]
    df.dropna(subset=drop_cols, inplace=True)
    return df


def reorder_columns(df, config):
    columns = [config["columns"][col] for col in config["order"]]
    return df[columns]


def parse_statement(filename, config):
    logging.basicConfig(level=logging.ERROR)
    logger = logging.getLogger()
    pdf = Pdf.open(filename)
    num_pages = len(pdf.pages)

    statement = get_raw_df(filename, num_pages, config)
    logging.debug(statement)

    if "truncate" in config["cleaning"]:
        logging.debug("**" + "truncate")
        statement = clean_truncate(statement, config)

    if "prestrip" in config["cleaning"]:
        logging.debug("**" + "prestrip")
        statement = clean_prestrip(statement, config)

    if "numeric" in config["cleaning"]:
        logging.debug("**" + "numeric")
        statement = clean_numeric(statement, config)

    if "date" in config["cleaning"]:
        logging.debug("**" + "date")
        statement = clean_date(statement, config)

    if "unwrap" in config["cleaning"]:
        logging.debug("**" + "unwrap")
        statement = clean_unwrap(statement, config)

    if "case" in config["cleaning"]:
        logging.debug("**" + "case")
        statement = clean_case(statement, config)

    if "dropna" in config["cleaning"]:
        logging.debug("**" + "dropna")
        statement = clean_dropna(statement, config)

    if "order" in config:
        logging.debug("**" + "order")
        statement = reorder_columns(statement, config)

    return statement
