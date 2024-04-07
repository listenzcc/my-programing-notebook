"""
File: files.py
Author: Chuncheng Zhang
Date: 2024-04-05
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Find all the blog files in the article_root

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2024-04-05 ------------------------
# Requirements and constants
import shutil
import pandas as pd
from pathlib import Path
from datetime import datetime
from . import logger, article_root, post_root, full_content_root


# %% ---- 2024-04-05 ------------------------
# Function and class
def find_files(root: Path = article_root) -> pd.DataFrame:
    months = [e for e in root.iterdir() if e.is_dir()]
    files = []
    for month in months:
        for sub in month.iterdir():
            files.append(dict(
                name=sub.name,
                suffix=sub.suffix,
                full_path=sub,
                path_type='file' if sub.is_file() else 'directory'
            ))
    return pd.DataFrame(files)


class MyArticle(object):
    title = 'Default title'
    date = ''
    layout = 'post'
    categories = 'default'

    def __init__(self):
        self.date = datetime.strftime(datetime.now(), '%Y-%m-%d')
        pass

    def update(self, line: str):
        line = line.strip()

        if line.startswith('Title:'):
            self.title = line.replace('Title:', '').strip()

        if line.startswith('Date:'):
            self.date = line.replace('Date:', '').strip()

        if line.startswith('Keywords:'):
            line = ' '.join([e.strip() for e in line.split(',')])
            self.categories = line.replace('Keywords:', '').strip()

        if line.startswith('Layout:'):
            self.layout = line.replace('Layout:', '').strip()

    def convert_to_text(self):
        return str(dict(
            title=self.title,
            date=self.date,
            layout=self.layout,
            categories=self.categories
        ))


# def legal_title(title: str):
#     '''Convert any title to Jekyll's :title'''
#     title = title.replace('：', '-')
#     return title


def parse_md_file(path: Path, df: pd.DataFrame):
    assert path.suffix == '.md', f'Invalid md file: {path}'

    # Read the lines of the path
    lines = open(path, 'r', encoding='utf-8').readlines()

    # --------------------
    # Create and update the article's head options
    article = MyArticle()
    for line in lines:
        if line.startswith('---'):
            break
        article.update(line)
    logger.debug(f'Parsed article: {article.convert_to_text()}')

    # --------------------
    # Find its paired folder(s)
    found = df.query(f'name=="{path.name[:-3]}" & path_type=="directory"')
    if not found.empty:
        for p in found['full_path'].to_list():
            # full_content_folder = full_content_root.joinpath(
            #     article.title, p.name)

            full_content_folder = full_content_root.joinpath(p.name)
            shutil.copytree(p, full_content_folder, dirs_exist_ok=True)

        logger.debug(f'Found folders: n={len(found)}')

    # --------------------
    # Make the post
    header = []
    header.extend([
        '---\n',
        f'layout: {article.layout}\n',
        f'title: "{article.title}"\n',
        f'date: {article.date}\n',
        f'categories: {article.categories}\n',
        '---\n\n',
    ])
    logger.debug(f'Generate header:{header}')

    # --------------------
    # Write the article to the post
    new_path = post_root.joinpath(
        f'{article.date[:10]}-{article.title}.markdown')
    new_lines = header + lines
    with open(new_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    logger.debug(f'Wrote {new_path} with {len(new_lines)} lines')

    return article


# %% ---- 2024-04-05 ------------------------
# Play ground


# %% ---- 2024-04-05 ------------------------
# Pending


# %% ---- 2024-04-05 ------------------------
# Pending
