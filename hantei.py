#!/usr/bin/env python
# fileencoding=utf-8

# Written By python 3.6.1

import os
import sys
import random
import pdb

# 牌に使う数値と文字の対応
lst = [i for i in range(11, 48) if i % 10 != 0]
conv = ['一', '二', '三', '四', '五', '六', '七', '八', '九',
        '１', '２', '３', '４', '５', '６', '７', '８', '９',
        'Ⅰ', 'Ⅱ', 'Ⅲ', 'Ⅳ', 'Ⅴ', 'Ⅵ', 'Ⅶ', 'Ⅷ', 'Ⅸ',
        '東', '南', '西', '北', '白', '發', '中']
dic = dict(zip(lst, conv))


def rndlst(lst):
    random.shuffle(lst)
    return lst


def rndtsumo(tehai, ho):
    tsumo = lst*4
    for te in tehai.tehai+[x for y in tehai.furo for x in y]+ho:
        tsumo.remove(te)
    tehai.set(random.choice(tsumo))


# 手牌を管理したり上がり形判定したりするクラス
# 判定部分は後で分離した方がいい気もする
class Tehai:
    def __init__(self, te=None, furo=[]):
        if not te:
            te = rndlst(lst*4)[:14]
        if len(te)+len(furo)*3 not in [13, 14]:
            print("size error")
            return None
        if len(te)+len(furo)*3 == 13:
            self.tehai = sorted(te)
            self.furo = furo
            self.tsumo = None
        if len(te)+len(furo)*3 == 14:
            self.tehai = te
            self.tehai[:-1] = sorted(self.tehai[:-1])
            self.furo = furo
            self.tsumo = self.tehai[-1]

# 刻子をカウントする
    def __kotsu(self, t, tset, ko):
        for s in tset:
            if t.count(s) >= 3:
                ko.append([s]*3)
                del t[t.index(s):t.index(s)+3]

# 順子をカウントする
    def __syuntsu(self, t, tset, syu):
        for s in tset:
            if s//10 == 4:
                continue
            while s in t:
                if s in t and s+1 in t and s+2 in t:
                    syu.append([s, s+1, s+2])
                    del t[t.index(s)]
                    del t[t.index(s+1)]
                    del t[t.index(s+2)]
                else:
                    break

# 対子をカウントしてそのリストを返す
    def count_toi(self):
        dic = dict(zip(lst, [0]*len(lst)))
        for x in self.tehai:
            dic[x] += 1
        cnt = [k for k, v in dic.items() if v >= 2]
        return cnt

# 一般的なアガリ形かどうかを解析する
    def analysis(self):
        toi = self.count_toi()
        tehai = sorted(self.tehai)
        target = []
        agari = []
        for t in toi:
            target.append(tehai[:tehai.index(t)]
                          + tehai[tehai.index(t)+2:])
        for t, t2 in zip(target, toi):
            # 含まれている対子毎にそれを雀頭として残りを解析
            tset = sorted(set(t), key=t.index)
# 刻子優先、順子は正順
            t1 = t.copy()
            ko = []
            syu = []
            self.__kotsu(t1, tset, ko)
            self.__syuntsu(t1, tset, syu)
            if len(ko+syu+self.furo) == 4:
                agari.append([[t2]*2]+ko+syu)
# 刻子優先、順子は逆順
            t1 = t.copy()
            ko = []
            syu = []
            self.__kotsu(t1, tset[::-1], ko)
            self.__syuntsu(t1, tset[::-1], syu)
            if len(ko+syu+self.furo) == 4:
                agari.append([[t2]*2]+(syu+ko)[::-1])
# 順子優先、順子は正順
            t1 = t.copy()
            ko = []
            syu = []
            self.__syuntsu(t1, tset, syu)
            self.__kotsu(t1, tset, ko)
            if len(ko+syu+self.furo) == 4:
                agari.append([[t2]*2]+ko+syu)
# 順子優先、順子は逆順
            t1 = t.copy()
            ko = []
            syu = []
            self.__syuntsu(t1, tset[::-1], syu)
            self.__kotsu(t1, tset[::-1], ko)
            if len(ko+syu+self.furo) == 4:
                agari.append([[t2]*2]+(syu+ko)[::-1])
        agari2 = []
        for a in agari:
            flag = True
            for a2 in agari2:
                if a == a2:
                    flag = False
                    break
            if flag:
                agari2.append(a)
        return agari2

# タンヤオ
    def tanyao(self):
        for hai in self.tehai + [x for inner in self.furo for x in inner]:
            if hai//10 == 4 or hai % 10 == 1 or hai % 10 == 9:
                return False
        return True

# 清一色 or 字一色
    def chinitsu(self):
        for hai in self.tehai + [x for inner in self.furo for x in inner]:
            if hai//10 != self.tehai[0]//10:
                return False
        if hai//10 == 4:
            return 2
        return True

# 緑一色
    def ryuiso(self):
        ryuiso = [32, 33, 34, 36, 38, 46]
        for hai in self.tehai:
            if hai not in ryuiso:
                return False
        return True

# チャンタ or 純チャンタ
    def chanta(self, lst):
        chanta = [True, True]   # [純チャン, チャンタ]
        for p in lst:
            if p[0] % 10 not in [1, 9] and p[-1] % 10 not in [1, 9]:
                chanta[0] = False
                if p[0]//10 != 4 and p[-1]//10 != 4:
                    chanta[1] = False
        return chanta

# 三色同順 or 三色同刻
    def sansyoku(self, lst):
        sansyoku = [False, False]
        ones, tens = [], []
        for p in lst[1:]:
            if p[0]//10 == 4:
                continue
            ones.append([i % 10 for i in p])
            tens.append(p[0]//10)
        sames = [ones.count(x) for x in ones]
        if 3 not in sames and 4 not in sames:
            return sansyoku
        if 1 in sames:
            ones.pop(sames.index(1))
            tens.pop(sames.index(1))
        if sorted(set(tens)) == [1, 2, 3]:
            if ones[0].count(ones[0][0]) == 1:
                sansyoku[0] = True
            else:
                sansyoku[1] = True
        return sansyoku

# 三暗刻
    def anko(self, lst):
        count = 0
        for p in lst[1:]:
            if p.count(p[0]) == 3:
                count += 1
        if count == 3:
            return True
        elif count == 4:
            return 2
        return False

# 一盃口 or 二盃口
    def peko(self, lst):
        if self.furo:
            return False
        peko = []
        for p in lst[1:]:
            if p.count(p[0]) == 1:
                peko.append(p)
        sames = [peko.count(x) for x in peko]
        if sames == [2, 2, 2, 2]:
            return 2
        for i in sames:
            if i >= 2:
                return True
        return False

# 一気通貫
    def ittsu(self, lst):
        lst = [x for inner in lst[1:] for x in inner]
        for i in range(1, 4):
            if set(range(i*10+1, i*10+10)) <= set(lst):
                return True
        return False

# 対々和
    def toitoi(self, lst):
        for l in lst[1:]:
            if l.count(l[0]) != 3:
                return False
        return True

# 小三元 or 大三元
    def sangen(self, lst):
        count = 0
        lst = [x for inner in lst for x in inner]
        for l in range(45, 48):
            if l in lst:
                count += 1
                continue
        if count != 3:
            return False
        if lst[0] in range(45, 48):
            return True
        return 2

# 小四喜 or 大四喜
    def sushi(self, lst):
        count = 0
        lst = [x for inner in lst for x in inner]
        for l in range(41, 45):
            if l in lst:
                count += 1
                continue
        if count != 4:
            return False
        if lst[0] in range(41, 45):
            return True
        return 2

# 平和
    def pinfu(self, lst):
        if self.furo or lst[0][0] in range(45, 48):
            return False
        pinfu = False
        for p in lst[1:]:
            if p.count(p[0]) != 1:
                return False
            if self.tsumo in [p[0], p[-1]]:
                if [x % 10 for x in p if self.tsumo != x] in [[1, 2], [8, 9]]:
                    return False
                pinfu = True
        return pinfu


# あたり牌を検索
    def atari(self):
        atari = []
        for hai in lst:
            tehai = Tehai(sorted(self.tehai+[hai]))
            if tehai.hantei(False):
                atari.append(hai)
        return atari

# アガリ状態かどうか判定する
    def hantei(self, flag):
        tmp = []
        for t in sorted(self.tehai):
            if t not in tmp:
                tmp.append(t)
        if tmp == [11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 45, 46, 47]:
            if flag:
                print(*[dic[x] for x in self.tehai])
                print("国士無双")
            return True

        for i in range(1, 4):
            if set(self.tehai) != set(range(i*10+1, i*10+10)):
                continue
            if self.tehai.count(i*10+1) >= 3 \
                    and self.tehai.count(i*10+9) >= 3:
                if flag:
                    print(*[dic[x] for x in self.tehai])
                    print("九蓮宝燈")
                return True

        agari = self.analysis()
        if agari:
            if flag:
                print("雀頭1 面子4")
                self.agari = []
                for a in agari:
                    if a not in self.agari:
                        self.agari.append(a)
                        a.extend(self.furo)
                        for p in a:
                            print("".join([dic[x] for x in p]), end=" ")
                        print()
                        if self.pinfu(a):
                            print("平和", end=" ")
                        chanta = self.chanta(a)
                        toitoi = self.toitoi(a)
                        if toitoi:
                            print("対々和", end=" ")
                        if chanta[0] and toitoi:
                            print("清老頭", end=" ")
                        elif chanta[0] and not toitoi:
                            print("純チャン", end=" ")
                        elif chanta[1] and toitoi:
                            print("混老頭", end=" ")
                        elif chanta[1] and not toitoi:
                            print("チャンタ", end=" ")
                        sansyoku = self.sansyoku(a)
                        if sansyoku[0]:
                            print("三色同順", end=" ")
                        elif sansyoku[1]:
                            print("三色同刻", end=" ")
                        peko = self.peko(a)
                        if peko == 2:
                            print("二盃口", end=" ")
                        elif peko:
                            print("一盃口", end=" ")
                        if self.ittsu(a):
                            print("一気通貫", end=" ")
                        sangen = self.sangen(a)
                        if sangen == 2:
                            print("大三元", end=" ")
                        elif sangen:
                            print("小三元", end=" ")
                        sushi = self.sushi(a)
                        if sushi == 2:
                            print("大四喜", end=" ")
                        elif sushi:
                            print("小四喜", end=" ")
                        anko = self.anko([x for x in a if x not in self.furo])
                        if anko == 2:
                            print("四暗刻", end=" ")
                        elif anko:
                            print("三暗刻", end=" ")
                        if self.tanyao():
                            print("たんやお", end=" ")
                        chinitsu = self.chinitsu()
                        if chinitsu == 2:
                            print("字一色", end=" ")
                        elif chinitsu:
                            print("清一色", end=" ")
                        if self.ryuiso():
                            print("緑一色", end=" ")
                        print()
            return True

        if len(self.count_toi()) == 7:
            if flag:
                for x in self.count_toi():
                    print(dic[x]+dic[x], end=" ")
                print()
                print("七対子", end=" ")
                chanta = self.chanta([[x] for x in self.count_toi()])
                if chanta[0]:
                    print("清老頭", end=" ")
                elif chanta[1]:
                    print("混老頭", end=" ")
                if self.tanyao():
                    print("たんやお", end=" ")
                chinitsu = self.chinitsu()
                if chinitsu == 2:
                    print("字一色", end=" ")
                elif chinitsu:
                    print("清一色", end=" ")
                if self.ryuiso():
                    print("緑一色", end=" ")
                print()
            return True
        return False

# ツモる
    def set(self, hai):
        if hai < 11 or hai > 47 or hai % 10 == 0:
            return False
        self.tehai.append(hai)
        self.tsumo = hai
        return True

# 手牌を切る
    def pop(self, hai):
        if hai < 0 or hai > 13:
            return None
        pop = self.tehai.pop(hai)
        self.tsumo = None
        self.tehai.sort()
        return pop

# 手牌を対応する文字に変換
    def conv(self):
        tehai = [dic[x] for x in self.tehai]
        furo = [[dic[x] for x in f] for f in self.furo]
        allfuro = ""
        for f in furo:
            allfuro += "," + "".join(f)
        return "".join(tehai) + allfuro

# 手牌と副露牌をまとめたやーつ
    def getAll(self):
        return self.tehai + [x for inner in self.furo for x in inner]


# このファイルを実行する時の処理
if __name__ == '__main__':

    tehai = Tehai()
    ho = []
    turn = 0
    mode = 3    # mode 1:ツモ 2:切る 3:ランダムツモ
    modedic = {1: "ツモ", 2: "切る", 3: "ランダムツモ"}
    try:
        while True:
            if sys.platform == 'win32':
                os.system('cls')
            else:
                os.system('clear')
# 数値と文字の対応表を表示
            print("  ", *[f"{i:2}" for i in range(1, 10)])
            for i in range(4):
                print(f"{(i+1)*10}", *conv[i*9:(i+1)*9])
            print()
# モード表示
            print("mode =", modedic[mode])
            print("turn =", turn)
            print()
            print(*[f"{x:02}" for x in range(14)])
            print(*tehai.conv())
            print()
            # print("対子:", *[dic[x] for x in tehai.count_toi()])
            # print()
            print("河:")
            for i in range(len(ho)//6+1):
                print(*[dic[x] for x in ho[i*6:(i+1)*6]])
            print()
            if mode in [1]:
                atari = tehai.atari()
                print("当たり牌:", *[dic[x] for x in atari])
            if mode in [2, 3]:
                if tehai.hantei(True):
                    furi = Tehai(tehai.tehai[:-1], tehai.furo)
                    for f in furi.atari():
                        if f in ho:
                            print("フリテン")
                print()
            print("\n > ", end="")
            usrinput = input()
# 'q' または ':q' で終了
            if usrinput == 'q' or usrinput == ':q':
                break
# 'r' でリセット
            if usrinput == 'r':
                tehai = Tehai()
                ho = []
                turn = 0
                if mode == 1:
                    mode = 2
                continue
# 'random' でランダムツモモード
            if usrinput == 'random':
                tehai = Tehai()
                ho = []
                turn = 0
                mode = 3
                continue
            if usrinput == 'debug':
                mode = 2
                continue
# 'furo' でツモ牌で鳴く
            if usrinput == 'furo' and mode != 1:
                furable = []
                if set([tehai.tsumo-2, tehai.tsumo-1]) <= set(tehai.tehai):
                    furable.append([tehai.tsumo-2, tehai.tsumo-1])
                if set([tehai.tsumo+1, tehai.tsumo+2]) <= set(tehai.tehai):
                    furable.append([tehai.tsumo+1, tehai.tsumo+2])
                if set([tehai.tsumo-1, tehai.tsumo+1]) <= set(tehai.tehai):
                    furable.append([tehai.tsumo-1, tehai.tsumo+1])
                if tehai.tehai.count(tehai.tsumo) >= 3:
                    furable.append([tehai.tsumo, tehai.tsumo])
                for i in range(len(furable)):
                    print(i, *[dic[x] for x in furable[i]])
                flag = True
                if not furable:
                    flag = False
                while flag:
                    print(" > ", end="")
                    usrinput = input()
                    if usrinput in ['q', ':q']:
                        flag = False
                        break
                    if usrinput.isdigit():
                        if int(usrinput) in set(range(len(furable))):
                            break
                if not flag:
                    continue
                tehai.furo.append(furable[int(usrinput)]+[tehai.tsumo])
                for f in furable[int(usrinput)]+[tehai.tsumo]:
                    tehai.tehai.remove(f)
                tehai.tsumo = None
                continue
# それ以外で数値でなければ弾く
            if not usrinput.isdigit():
                continue
            if mode == 1:
                if tehai.set(int(usrinput)):
                    mode = 2
            elif mode in [2, 3]:
                pop = tehai.pop(int(usrinput))
                if not pop:
                    continue
                turn += 1
                ho.append(pop)
                if mode == 2:
                    mode = 1
                    continue
                elif mode == 3:
                    rndtsumo(tehai, ho)
# Ctrl+C で終了
    except KeyboardInterrupt:
        print()
