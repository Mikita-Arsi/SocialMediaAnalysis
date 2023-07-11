import pandas as pd


def save_to_csv(path_to_save_file: str, comments_list: list):
    df = pd.DataFrame({'Comments': comments_list})
    df.to_csv(path_to_save_file, index=False)
    return df
