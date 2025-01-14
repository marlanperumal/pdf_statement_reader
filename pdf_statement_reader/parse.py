from tabula import read_pdf
from pikepdf import Pdf
import pandas as pd
import numpy as np


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
            pandas_options={"dtype": str},
            java_options=[
                "-Dorg.slf4j.simpleLogger.defaultLogLevel=off",
                "-Dorg.apache.commons.logging.Log=org.apache.commons.logging.impl.NoOpLog",
            ],
        )
        if df is not None and len(df) > 0:
            dfs.extend(df)
    statement = pd.concat(dfs, sort=False).reset_index(drop=True)
    return statement


def format_negatives(s):
    s = str(s)
    if s.endswith("-"):
        return "-" + s[:-1]
    else:
        return s


def clean_numeric(df, config):
    numeric_cols = [config["columns"][col] for col in config["cleaning"]["numeric"]]

    for col in numeric_cols:
        df[col] = df[col].apply(format_negatives)
        df[col] = df[col].str.replace(" ", "")
        df[col] = pd.to_numeric(df[col], errors="coerce")


def clean_date(df, config):
    date_cols = [config["columns"][col] for col in config["cleaning"]["date"]]
    if "date_format" in config["cleaning"]:
        date_format = config["cleaning"]["date_format"]
    else:
        date_format = None

    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce", format=date_format)


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


def clean_dropna(df, config):
    drop_cols = [config["columns"][col] for col in config["cleaning"]["dropna"]]
    df.dropna(subset=drop_cols, inplace=True)


def reorder_columns(df, config):
    columns = [config["columns"][col] for col in config["order"]]
    return df[columns]


def parse_statement(filename, config):
    pdf = Pdf.open(filename)
    num_pages = len(pdf.pages)

    statement = get_raw_df(filename, num_pages, config)

    if "numeric" in config["cleaning"]:
        clean_numeric(statement, config)

    if "trans_detail" in config["cleaning"]:
        clean_trans_detail(statement, config)

    if "date" in config["cleaning"]:
        clean_date(statement, config)

    if "dropna" in config["cleaning"]:
        clean_dropna(statement, config)

    if "order" in config:
        statement = reorder_columns(statement, config)

    return statement
