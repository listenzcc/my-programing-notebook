"""
File: app.py
Author: Chuncheng Zhang
Date: 2024-04-05
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    The python application entrance of the project.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2024-04-05 ------------------------
# Requirements and constants
import argparse
from rich import print
from module.files import find_files, parse_md_file


# %% ---- 2024-04-05 ------------------------
# Function and class


# %% ---- 2024-04-05 ------------------------
# Play ground
if __name__ == '__main__':
    df = find_files()
    print(df)

    for path in df.query('suffix == ".md"')['full_path'].to_list():
        print(parse_md_file(path, df))

    print('Done.')


# %% ---- 2024-04-05 ------------------------
# Pending


# %% ---- 2024-04-05 ------------------------
# Pending
