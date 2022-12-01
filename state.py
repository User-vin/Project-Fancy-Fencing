from enum import Enum


class State(Enum):
    """player's state"""
    REST = 0
    LEFT = 1
    RIGHT = 2
    ATTACK = 3
    BLOCK = 4
    JUMPLSTART = 5
    JUMPLMIDDLE = 6
    JUMPLEND = 7
    JUMPRSTART = 8
    JUMPRMIDDLE = 9
    JUMPREND = 10
    ATTACKEND = 11
    BLOCKEND = 12
    STOP = 13