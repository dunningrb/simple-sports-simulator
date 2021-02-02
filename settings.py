# -*- coding: utf-8 -*-

"""
settings.py

Rodney Dunning

Define global settings.

"""

import os
from pathlib import Path

ROOT_PATH = Path(os.path.dirname(os.path.realpath(__file__))).parent

LOG_CONFIG = f'{ROOT_PATH}/settings/logging.ini'  # Config file for log files.
LOG_PATH = f'{ROOT_PATH}/logs/'  # Path for log files.
LOG_FILEPATH = f'{LOG_PATH}/log.log'
LOG_DEFAULT = {'logfilepath': LOG_FILEPATH}  # defaults dict for logging.config.fileConfig().

SCHEDULE_TABLES = {
    (3, 4):
        {1: 'A-D,B-C',
         2: 'D-C,A-B',
         3: 'B-D,C-A'},
    (5, 6):
        {1: 'A-F,B-E,C-D',
         2: 'F-D,E-C,A-B',
         3: 'B-F,C-A,D-E',
         4: 'F-E,A-D,B-C',
         5: 'C-F,D-B,E-A'},
    (7, 8):
        {1: 'A-H,B-G,C-F,D-E',
         2: 'H-E,F-D,G-C,A-B',
         3: 'B-H,C-A,D-G,E-F',
         4: 'H-F,G-E,A-D,B-C',
         5: 'C-H,D-B,E-A,F-G',
         6: 'H-G,A-F,B-E,C-D',
         7: 'D-H,E-C,F-B,G-A'},
    (9, 10):
        {1: 'A-J,B-I,C-H,D-G,E-F',
         2: 'J-F,G-E,H-D,I-C,A-B',
         3: 'B-J,C-A,D-I,E-H,F-G',
         4: 'J-G,H-F,I-E,A-D,B-C',
         5: 'C-J,D-B,E-A,F-I,G-H',
         6: 'J-H,I-G,A-F,B-E,C-D',
         7: 'D-J,E-C,F-B,G-A,H-I',
         8: 'J-I,A-H,B-G,C-F,D-E',
         9: 'E-J,F-D,G-C,H-B,I-A'},
    (11, 12):
        {1: 'A-L,B-K,C-J,D-I,E-H,F-G',
         2: 'L-G,H-F,I-E,J-D,K-C,A-B',
         3: 'B-L,C-A,D-K,E-J,F-I,G-H',
         4: 'L-H,I-G,J-F,K-E,A-D,B-C',
         5: 'C-L,D-B,E-A,F-K,G-J,H-I',
         6: 'L-I,J-H,K-G,A-F,B-E,C-D',
         7: 'D-L,E-C,F-B,G-A,H-K,I-J',
         8: 'L-J,K-I,A-H,B-G,C-F,D-E',
         9: 'E-L,F-D,G-C,H-B,I-A,J-K',
         10: 'L-K,A-J,B-I,C-H,D-G,E-F',
         11: 'F-L,G-E,H-D,I-C,J-B,K-A'},
    (13, 14):
        {1: 'A-N,B-M,C-L,D-K,E-J,F-I,G-H',
         2: 'N-H,I-G,J-F,K-E,L-D,M-C,A-B',
         3: 'B-N,C-A,D-M,E-L,F-K,G-J,H-I',
         4: 'N-I,J-H,K-G,L-F,M-E,A-D,B-C',
         5: 'C-N,D-B,E-A,F-M,G-L,H-K,I-J',
         6: 'N-J,K-I,L-H,M-G,A-F,B-E,C-D',
         7: 'D-N,E-C,F-B,G-A,H-M,I-L,J-K',
         8: 'N-K,L-J,M-I,A-H,B-G,C-F,D-E',
         9: 'E-N,F-D,G-C,H-B,I-A,J-M,K-L',
         10: 'N-L,M-K,A-J,B-I C-H,D-G,E-F',
         11: 'F-N,G-E,H-D,I-C,J-B,K-A,L-M',
         12: 'N-M,A-L,B-K,C-J,D-I,E-H,F-G',
         13: 'G-N,H-F,I-E,J-D,K-C,L-B,M-A'},
    (15, 16):
        {1: 'A-P,B-O,C-N,D-M,E-L,F-K,G-J,H-I',
         2: 'P-I,J-H,K-G,L-F,M-E,N-D,O-C,A-B',
         3: 'B-P,C-A,D-O,E-N,F-M,G-L,H-K,I-J',
         4: 'P-J,K-I,L-H,M-G,N-F,O-E,A-D,B-C',
         5: 'C-P,D-B,E-A,F-O,G-N,H-M,I-L,J-K',
         6: 'P-K,L-J,M-I,N-H,O-G,A-F,B-E,C-D',
         7: 'D-P,E-C,F-B,G-A,H-O,I-N,J-M,K-L',
         8: 'P-L,M-K,N-J,O-I,A-H,B-G,C-F,D-E',
         9: 'E-P,F-D,G-C,H-B,I-A,J-O,K-N,L-M',
         10: 'P-M,N-L,O-K,A-J,B-I,C-H,D-G,E-F',
         11: 'F-P,G-E,H-D,I-C,J-B,K-A,L-O,M-N',
         12: 'P-N,O-M,A-L,B-K,C-J,D-I,E-H,F-G',
         13: 'G-P,H-F,I-E,J-D,K-C,L-B,M-A,N-O',
         14: 'P-O,A-N,B-M,C-L,D-K,E-J,F-I,G-H',
         15: 'H-P,I-G,J-F,K-E,L-D,M-C,N-B,O-A'},
    (19, 20):
        {1: 'A-T,S-B,R-C,Q-D,P-E,O-F,N-G,M-H,L-I,K-J',
         2: 'T-K,J-L,I-M,H-N,G-O,F-P,E-Q,D-R,C-S,B-A',
         3: 'B-T,A-C,S-D,R-E,Q-F,P-G,O-H,N-I,M-J,L-K',
         4: 'T-L,K-M,J-N,I-O,H-P,G-Q,F-R,E-S,D-A,C-B',
         5: 'C-T,B-D,A-E,S-F,R-G,Q-H,P-I,O-J,N-K,M-L',
         6: 'T-M,L-N,K-O,J-P,I-Q,H-R,G-S,F-A,E-B,D-C',
         7: 'D-T,C-E,B-F,A-G,S-H,R-I,Q-J,P-K,O-L,N-M',
         8: 'T-N,M-O,L-P,K-Q,J-R,I-S,H-A,G-B,F-C,E-D',
         9: 'E-T,D-F,C-G,B-H,A-I,S-J,R-K,Q-L,P-M,O-N',
         10: 'T-O,N-P,M-Q,L-R,K-S,J-A,I-B,H-C,G-D,F-E',
         11: 'F-T,E-G,D-H,C-I,B-J,A-K,S-L,R-M,Q-N,P-O',
         12: 'T-P,O-Q,N-R,M-S,L-A,K-B,J-C,I-D,H-E,G-F',
         13: 'G-T,F-H,E-I,D-J,C-K,B-L,A-M,S-N,R-O,Q-P',
         14: 'T-Q,P-R,O-S,N-A,M-B,L-C,K-D,J-E,I-F,H-G',
         15: 'H-T,G-I,F-J,E-K,D-L,C-M,B-N,A-O,S-P,R-Q',
         16: 'T-R,Q-S,P-A,O-B,N-C,M-D,L-E,K-F,J-G,I-H',
         17: 'I-T,H-J,G-K,F-L,E-M,D-N,C-O,B-P,A-Q,S-R',
         18: 'T-S,R-A,Q-B,P-C,O-D,N-E,M-F,L-G,K-H,J-I',
         19: 'J-T,I-K,H-L,G-M,F-N,E-O,D-P,C-Q,B-R,A-S'}
}
