#!/usr/bin/env python
# fileencoding=utf-8

# Written by python 3.6.1

import os
import sys
import random
import auto
import hantei


# ゲーム本体クラス
# 基本的にこいつに色々聞いていくことでゲームを進行したい
class Game:
    def __init__(self):
        self.mode = -1
        self.turn = -1
        self.oya = -1
        self.ba = -1
        self.kyoku = 0
        self.honba = -1

    def init(self, *players):
        self.mode = 1
        self.yama = hantei.rndlst(hantei.lst * 4)
        self.turn = random.randint(0, 3) # random.randintは "a以上b以下の数値"
        self.oya = self.turn
        self.ba = 0
        self.kyoku = 1
        self.honba = 0
        self.players = players
        for pl in players:
            pl.tehai = hantei.Tehai(sorted(self.yama[:13]))
            del self.yama[:13]

    # 誰が何を送ったかを受け取って、対応した正しい処理を行う
    def post(self, plid, order):
        if plid is not self.turn:
            return -1
        if self.mode is 1 and order in range(14):
            pop = self.players[plid].tehai.pop(order)
            self.players[plid].ho.append(pop)
            # ここで副露とか和了判定する
            agari = 0
            for pl in (x for x in self.players if x is not self.players[plid]):
                agari ^= pl.tehai.hantei(True, pop)
            if agari:
                self.mode = 3
            else:
                self.mode = 99
            return 0
        else:
            return -2

    # 手番プレイヤーが変わった時用
    # 主にポンに使うと思う
    def set(self, plid):
        self.turn = plid

    # 次のプレイヤーに手番を回す
    # ということはツモもするということ
    def next(self):
        if self.mode is not 99:
            return -1
        self.turn = (self.turn + 1) % 4
        self.players[self.turn].tehai.set(self.yama.pop(0))
        self.mode = 1
        return 0

    def scene_game(self):
        if sys.platform == 'win32':
            os.system('cls')
        else:
            os.system('clear')

        print(f"{hantei.dic[self.ba+41]}{self.kyoku}局 {self.honba}本場")
        print(f"山残り : {len(self.yama)-14}")
        for i in range(14):
            print(f"{i:02}", end=" ")
        print('\n')
        for i in range(4):
            print(*self.players[i].tehai.conv())
            print()
        print()

        print(" players - points : ho")
        for p0 in self.players:
            print(f"{p0.name:8s} - {p0.point:6d} : ",
                  *(hantei.dic[x] for x in p0.ho))


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
                if game.oya == 0:
                    hantei.oya = True
                    hantei.isTsumo = True
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
                    for player in players[1:]:
                        player.tehai.set(pop)
                        if player.tehai.hantei(False, False):
                            scene_game(players)
                            if players[game.oya] == player:
                                hantei.oya = True
                            else:
                                hantei.oya = False
                            hantei.isTsumo = False
                            player.tehai.hantei(True, True)
                            print("お前が放銃！")
                            exit()
                        player.tehai.pop(13)
            else:
                pop = players[game.turn].tehai.pop(13)
                players[game.turn].ho.append(pop)

                players[0].tehai.set(pop)
                if players[0].tehai.hantei(False, False):
                    scene_game(players)
                    hantei.oya = True if game.oya == 0 else False
                    hantei.isTsumo = False
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
