#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
runner.py

Example:
    $ python3 runner.py filename.yaml

"""
import sys
from benedict import benedict

from association_football.association_football import AssociationFootballLeague


def play(params):
    sport = list(params.keys())[0]

    {'association football': AssociationFootballLeague}[sport.lower()](**params[sport])



if __name__ == '__main__':
    play(benedict.from_yaml(sys.argv[1]))
