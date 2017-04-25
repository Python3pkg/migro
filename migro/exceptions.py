#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Interrupt:
    code: int = 0

    def __new__(cls, msg: str=None):
        print(cls.__name__ + (': ' + msg if msg else ''))
        exit(cls.code)


class AlreadyHere(Interrupt):
    code = 0


class RevisionNotFound(Exception):
    pass


class BranchingFound(Exception):
    pass


class RevisionAlreadyExists(Exception):
    pass


class NoRevisionsFound(Exception):
    pass


class GoingTooFar(Exception):
    pass
