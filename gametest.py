#!/usr/bin/env python
# fileencoding=utf-8

# Written by python 3.6.1

import os
import sys
import random
import auto
import hantei


class Game:
    def __init__(self):
        self.turn = -1
        self.oya = -1
        self.ba = -1
        self.kyoku = 0
        self.honba = -1

    def init(self):
        self.turn = random.randint(0, 3)
        self.oya = self.turn
        self.ba = 0
        self.kyoku = 1
        self.honba = 0

    def next(self):
        self.turn = (self.turn + 1) % 4


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
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')

    print(f"{hantei.dic[game.ba+41]}{game.kyoku}局 {game.honba}本場")
    print(f"山残り : {len(yama)-14}")
    for i in range(14):
        print(f"{i:02}", end=" ")
    print('\n')
    for i in range(1):
        print(*players[i].tehai.conv())
        print()
    print()

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
    game = Game()

    print("Input your name.")
    player_name = input()
    players = []
    players.append(Player(player_name))
    players.append(Player("CPU1"))
    players.append(Player("CPU2"))
    players.append(Player("CPU3"))

    try:
        game.init()
        yama = hantei.rndlst(lst)
        for i in range(4):
            players[i].tehai = hantei.Tehai(sorted(yama[0:13]))
            del yama[0:13]
        while True:
            choose = random.choice(yama)
            yama.remove(choose)
            players[game.turn].tehai.set(choose)

            scene_game(players)
            if game.turn == 0:
                if players[0].tehai.hantei(True, True):
                    print("自摸和！")
                    exit()
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
            else:
                pop = players[game.turn].tehai.pop(13)
                players[game.turn].ho.append(pop)

                players[0].tehai.set(pop)
                if players[0].tehai.hantei(False, False):
                    scene_game(players)
                    players[0].tehai.hantei(True, False)
                    print("放銃！")
                    exit()
                players[0].tehai.pop(13)
            if len(yama)-14 == 0:
                print("山切れ")
                exit()
            game.next()


# Ctrl-C で終了
    except KeyboardInterrupt:
        print()
    print("See you agein!")
