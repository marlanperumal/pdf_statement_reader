def validate_statement(df, config):
    """Checks that the dataframe statement has a valid rolling balance"""
    df = df.copy()
    debit = config["columns"]["debit"]
    credit = config["columns"]["credit"]
    balance = config["columns"]["balance"]

    df[[debit, credit, balance]] = df[[debit, credit, balance]].fillna(0)

    prev_balance = df[balance] - df[credit] + df[debit]

    invalid = (abs(prev_balance.shift(-1) - df[balance]) > 1e-6).any()

    return not invalid
