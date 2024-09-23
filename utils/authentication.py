import pandas as pd

def authentication(account: str, password: str) -> bool:
    """
    check your account
    account: str
    password: str
    return: bool
    """

    account_data = pd.read_json('account/account.jsonl', lines =True)
    for _, row in account_data.iterrows():
        if row['account'] == account and row['password'] == password:
            return True

    return False
