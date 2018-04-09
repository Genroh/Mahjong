#!/usr/bin/env python
# fileencoding=utf-8

# Written by python 3.6.1

import os
import sys
import random
import auto
import hantei


class Player:
    def __init__(self, name):
        self.name = name
        self.point = 25000
        self.tehai = []
        self.furo = []
        self.ho = []


def used_hai(players):
    hai = []
    for player in players[1:]:
        hai.extend(player.tehai)
        hai.extend(player.ho)
    return hai


def scene_game(players):
    print(" players - points : ho")
    for p0 in players:
        print(f"{p0.name:8s} - {p0.point:6d} : ",
              *(hantei.dic[x] for x in p0.ho))


if __name__ == '__main__':

    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')

    lst = hantei.lst * 4

    print("Input your name.")
    players = []
    players.append(Player(input()))
    players.append(Player("CPU1"))
    players.append(Player("CPU2"))
    players.append(Player("CPU3"))

    try:
        yama = hantei.rndlst(lst)
        for i in range(4):
            players[i].tehai = hantei.Tehai(sorted(yama[0:13]))
            del yama[0:13]
        choose = random.choice(yama)
        yama.remove(choose)
        players[0].tehai.set(choose)
        while True:
            if sys.platform == 'win32':
                os.system('cls')
            else:
                os.system('clear')

            print(f"山残り : {len(yama)}")
            for i in range(14):
                print(f"{i:02}", end=" ")
            print('\n')
            for i in range(4):
#                 print(*[hantei.dic[x] for x in players[i].tehai])
                print(*players[i].tehai.conv())
                print()
            print()

            scene_game(players)
            print("\n > ", end="")
            usrinput = input()
# 'q' または ':q' で終了
            if usrinput == 'q' or usrinput == ':q':
                break
            if usrinput.isdigit():
                pop = players[0].tehai.pop(int(usrinput))
                if not pop:
                    continue
                players[0].ho.append(pop)
                for AI in players[1:]:
                    if not yama:
                        print("山切れ")
                        break
                    choose = random.choice(yama)
                    yama.remove(choose)
                    AI.ho.append(choose)
                    players[0].tehai.set(choose)
                    if players[0].tehai.hantei(True):
                        print("correct")
                        exit()
                    players[0].tehai.pop(13)

            else:
                continue
            if not yama:
                print("山切れ")
                break
            choose = random.choice(yama)
            yama.remove(choose)
            players[0].tehai.set(choose)
            if players[0].tehai.hantei(True):
                print("correct")
                exit()


# Ctrl-C で終了
    except KeyboardInterrupt:
        print()
    print("See you agein!")
