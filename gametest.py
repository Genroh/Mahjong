#!/usr/bin/env python
# fileencoding=utf-8

# Written by python 3.6.1

import os
import sys
import auto
import hantei


class Player:
    def __init__(self, name):
        self.name = name
        self.point = 25000
        self.tehai = []
        self.ho = []


def scene_game(players):
    print(" players - points : ho")
    for p0 in players:
        print(f"{p0.name:8s} - {p0.point:6d} : ",
              *(hantei.dic[x] for x in p0.ho))


if __name__ == '__main__':
    print("Input your name.")
    players = []
    players.append(Player(input()))
    players.append(Player("CPU1"))
    players.append(Player("CPU2"))
    players.append(Player("CPU3"))

    scene_game(players)
