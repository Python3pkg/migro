#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from typing import Tuple, List, Union

import yaml
import psycopg2

from .exceptions import BranchingFound


def connect(url: str) -> Tuple[psycopg2.extensions.connection,
                               psycopg2.extensions.cursor]:
    con = psycopg2.connect(url)
    return con, con.cursor()


def parse_dir(path: str) -> List[dict]:
    file_re = re.compile('\w{12}_.*\.yaml')

    files = list(
        yaml.load(
            open(os.path.join(path, x))
        ) for x in os.listdir(path) if (
            os.path.isfile(os.path.join(path, x)) and
            file_re.match(x)
        )
    )

    order = list()

    rev_id = None
    while files:
        next_rev_id = tuple(x for x in files if x['down_revision'] == rev_id)

        if not next_rev_id:
            break
        if len(next_rev_id) != 1:
            raise BranchingFound('From %s to %s' % (
                rev_id, ', '.join(x['revision'] for x in next_rev_id)))

        next_rev_id = next_rev_id[0]

        files.remove(next_rev_id)
        order.append(next_rev_id)

        rev_id = next_rev_id['revision']

    return order


def get_curr_rev_id(conn: psycopg2.extensions.connection) -> Union[str, None]:
    curs = conn.cursor()
    try:
        curs.execute('SELECT ver FROM migro_ver')
        return curs.fetchone()[0]
    except psycopg2.ProgrammingError:
        conn.rollback()
        curs.execute(
            'CREATE TABLE migro_ver (ver VARCHAR(12) PRIMARY KEY)')
        conn.commit()
        return None
    except TypeError:
        return None
    finally:
        curs.close()


def get_index(d: List[dict], rev: str) -> Union[int, None]:
    try:
        return next(i for i, x in enumerate(d) if x['revision'] == rev)
    except StopIteration:
        return None


def isnum(n) -> bool:
    try:
        int(n)
        return True
    except ValueError:
        return False
