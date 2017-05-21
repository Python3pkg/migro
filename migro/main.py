#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import uuid

from . import utils
from .exceptions import (RevisionNotFound, RevisionAlreadyExists,
                         NoRevisionsFound, GoingTooFar, AlreadyHere)


def init(directory: str):
    print(('Creating directory', directory))
    os.mkdir(directory)
    print('Creating file migro.yaml')
    with open('migro.yaml', 'w') as file:
        file.write('database_url: driver://user:pass@localhost/dbname\n'
                   'script_location: %s\n' % directory)
    print('Please edit migro.yaml before proceeding.')


def current(config: dict):
    conn, curs = utils.connect(config['database_url'])
    revisions = utils.parse_dir(config['script_location'])
    if not revisions:
        raise NoRevisionsFound
    curr_rev_id = utils.get_curr_rev_id(conn)

    curr_rev = next(
        (x for x in revisions if x['revision'] == curr_rev_id), None)

    if curr_rev is None:
        raise RevisionNotFound(curr_rev_id)

    print((curr_rev['revision'], ':', curr_rev['description']))

    curs.close()
    conn.close()


def revision(config: dict, message: str):
    revisions = utils.parse_dir(config['script_location'])

    latest_rev_id = revisions[-1]['revision'] if revisions else None

    new_rev_id = str(uuid.uuid4())[-12:]
    new_rev_filename = os.path.join(
        config['script_location'], '%s_%s.yaml' % (
            new_rev_id, re.sub('\W', '_', message).lower()
        )
    )

    if os.path.isfile(new_rev_filename):
        raise RevisionAlreadyExists

    with open(new_rev_filename, 'w') as file:
        file.write(
            'description: %s\n\nrevision: %s\n'
            'down_revision: %s\n\nupgrade:\n\ndowngrade:\n' % (
                message, new_rev_id,
                latest_rev_id if latest_rev_id is not None else 'null'))

    print(('Created revision at %s' % new_rev_filename))


def checkout(config: dict, arg: str):
    conn, curs = utils.connect(config['database_url'])
    revisions = utils.parse_dir(config['script_location'])
    if not revisions:
        raise NoRevisionsFound
    curr_rev_id = utils.get_curr_rev_id(conn)

    curr_rev_index = utils.get_index(revisions, curr_rev_id)

    if curr_rev_index is None and curr_rev_id is None:
        curr_rev_index = -1
    elif curr_rev_index is None:
        raise RevisionNotFound(curr_rev_id)

    if arg == 'head':
        next_rev_index = len(revisions) - 1
    elif utils.isnum(arg):
        next_rev_index = curr_rev_index + int(arg)

        if next_rev_index > len(revisions) - 1 or next_rev_index < -1:
            raise GoingTooFar
    else:
        next_rev_index = utils.get_index(revisions, arg)
        if next_rev_index is None:
            raise RevisionNotFound(arg)

    if next_rev_index == curr_rev_index:
        AlreadyHere()

    if next_rev_index > curr_rev_index:  # Upgrading
        for rev_index in range(curr_rev_index + 1, next_rev_index + 1):
            print(('Upgrading to', revisions[rev_index]['revision'], ':',
                  revisions[rev_index]['description']))

            curs.execute(revisions[rev_index]['upgrade'])
            curs.execute(
                "TRUNCATE TABLE migro_ver; INSERT INTO migro_ver VALUES (%s);",
                (revisions[rev_index]['revision'],))
            conn.commit()
    else:  # Downgrading
        for rev_index in range(curr_rev_index, next_rev_index, -1):
            print(('Downgrading from', revisions[rev_index]['revision'], ':',
                  revisions[rev_index]['description']))

            curs.execute(revisions[rev_index]['downgrade'])
            curs.execute("TRUNCATE TABLE migro_ver;")

            if rev_index > 0:
                curs.execute("INSERT INTO migro_ver VALUES (%s);",
                             (revisions[rev_index - 1]['revision'],))
            conn.commit()

    curs.close()
    conn.close()


def reapply(config: dict):
    conn, curs = utils.connect(config['database_url'])
    revisions = utils.parse_dir(config['script_location'])
    if not revisions:
        raise NoRevisionsFound
    curr_rev_id = utils.get_curr_rev_id(conn)

    curr_rev_index = utils.get_index(revisions, curr_rev_id)

    if curr_rev_index is None:
        raise RevisionNotFound(curr_rev_id)

    print(('Reapplying', revisions[curr_rev_index]['revision'], ':',
          revisions[curr_rev_index]['description']))

    curs.execute(revisions[curr_rev_index]['downgrade'])
    curs.execute(revisions[curr_rev_index]['upgrade'])
    conn.commit()


def show(config: dict):
    conn, curs = utils.connect(config['database_url'])
    revisions = utils.parse_dir(config['script_location'])
    if not revisions:
        raise NoRevisionsFound
    curr_rev_id = utils.get_curr_rev_id(conn)

    for rev in revisions:
        print(('[%s]' % ('x' if curr_rev_id == rev['revision'] else ' '),
              rev['revision'], ':', rev['description']))

