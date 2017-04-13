#!/usr/bin/env python3
# -*- coding: utf-8 -*-


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


class AlreadyHere(Exception):
    pass
