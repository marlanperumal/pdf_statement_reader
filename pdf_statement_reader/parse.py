from tabula import read_pdf
from pikepdf import Pdf
import pandas as pd
import numpy as np
import re
import logging


def get_raw_df(filename, num_pages, config):
    dfs = []

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
            pandas_options={"dtype": str, "header": None},
            java_options=[
                "-Dorg.slf4j.simpleLogger.defaultLogLevel=off",
                "-Dorg.apache.commons.logging.Log=org.apache.commons.logging.impl.NoOpLog",
            ],
        )
        if df is not None and len(df) > 0:
            dfs.extend(df)

    if config["layout"]["pandas_options"]["header"] == "None":
        for df in dfs:
            df.columns = [config["columns"][col] for col in config["order"]]
    statement = pd.concat(dfs, sort=False).reset_index(drop=True)
    return statement


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


def clean_date(df, config):
    date_cols = [config["columns"][col] for col in config["cleaning"]["date"]]
    if "date_format" in config["cleaning"]:
        date_format = config["cleaning"]["date_format"]
    else:
        date_format = None

    cba = False  # json setting needed
    if cba:
        year = df.iloc[0, 1][0:4]
        date_format += " %Y"
    for col in date_cols:
        if cba:
            df[col] += " " + year
        df[col] = pd.to_datetime(df[col], errors="coerce", format=date_format)


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


def clean_case(df, config):
    cols = [config["columns"][col] for col in config["cleaning"]["case"]]
    for col in cols:
        df[col] = df[col].str.title()
    return df


def clean_dropna(df, config):
    drop_cols = [config["columns"][col] for col in config["cleaning"]["dropna"]]
    df.dropna(subset=drop_cols, inplace=True)


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

    logging.debug("**" + "prestrip")
    if "prestrip" in config["cleaning"]:
        statement = clean_prestrip(statement, config)

    logging.debug("**" + "numeric")
    if "numeric" in config["cleaning"]:
        clean_numeric(statement, config)

    logging.debug("**" + "date")
    if "date" in config["cleaning"]:
        clean_date(statement, config)

    logging.debug("**" + "unwrap")
    if "unwrap" in config["cleaning"]:
        clean_unwrap(statement, config)

    logging.debug("**" + "case")
    if "case" in config["cleaning"]:
        statement = clean_case(statement, config)

    logging.debug("**" + "dropna")
    if "dropna" in config["cleaning"]:
        clean_dropna(statement, config)

    logging.debug("**" + "order")
    if "order" in config:
        statement = reorder_columns(statement, config)

    return statement
