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
    lst = hantei.lst * 4

    print("Input your name.")
    players = []
    players.append(Player(input()))
    players.append(Player("CPU1"))
    players.append(Player("CPU2"))
    players.append(Player("CPU3"))

    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')

    for i in range(14):
        print(f"{i:02}", end=" ")
    print('\n')
    yama = hantei.rndlst(lst)
    for i in range(4):
        players[i].tehai.extend(sorted(yama[0:13]))
        del yama[0:13]
        print(*[hantei.dic[x] for x in players[i].tehai])
        print()
    print()

    scene_game(players)
