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
from chess.chess_tournament import ChessTournament
from baseball.baseball import BaseballLeague
from basketball.basketball import BasketballLeague
from hockey.hockey import HockeyLeague


def play(params):
    sport = list(params.keys())[0]

    print(f'sport: {sport}')

    {'association football': AssociationFootballLeague,
     'baseball': BaseballLeague,
     'basketball': BasketballLeague,
     'chess': ChessTournament,
     'hockey': HockeyLeague,
     }[sport.lower()](**params[sport])


if __name__ == '__main__':
    play(benedict.from_yaml(sys.argv[1]))
