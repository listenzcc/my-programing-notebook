"""
File: __init__.py
Author: Chuncheng Zhang
Date: 2024-04-05
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Amazing things

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2024-04-05 ------------------------
# Requirements and constants
from loguru import logger
from pathlib import Path


# %% ---- 2024-04-05 ------------------------
# Function and class


# %% ---- 2024-04-05 ------------------------
# Play ground
logger.add('log/my-parttime-writing.log', rotation='5 MB')

root = Path(__file__).parent.parent.parent
article_root = root.joinpath('article')

post_root = root.joinpath('myblog/_posts')
full_content_root = post_root.parent.joinpath('full-content')


# %% ---- 2024-04-05 ------------------------
# Pending


# %% ---- 2024-04-05 ------------------------
# Pending
