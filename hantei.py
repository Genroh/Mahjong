#!/usr/bin/env python
# fileencoding=utf-8

# Written By python 3.6.1

import os
import sys
import random
import math

import yaku

# 牌に使う数値と文字の対応
lst = [i for i in range(11, 48) if i % 10 != 0]
yaochu = tuple(i for i in lst if i % 10 in (1, 9) or i//10 == 4)
conv = ('一', '二', '三', '四', '五', '六', '七', '八', '九',
        '１', '２', '３', '４', '５', '６', '７', '８', '９',
        'Ⅰ', 'Ⅱ', 'Ⅲ', 'Ⅳ', 'Ⅴ', 'Ⅵ', 'Ⅶ', 'Ⅷ', 'Ⅸ',
        '東', '南', '西', '北', '白', '發', '中')
dic = dict(zip(lst, conv))
dic.update(zip([-x for x in lst],
           map(lambda x: f"\033[031m"+x+"\033[00m", conv)))

ba = 41
ji = 41

oya = True
tsumo = True

def rndlst(lst):
    random.shuffle(lst)
    return lst


def rndtsumo(tehai, ho):
    tsumo = lst*4
    for te in tehai.tehai+[x for y in tehai.furo for x in y]+ho:
        tsumo.remove(te)
    tehai.set(random.choice(tsumo))


def rmlst(lst, rem, num):
    ls = lst.copy()
    for i in range(num):
        if ls.count(rem) <= 0:
            break
        ls.remove(rem)
    return ls


def lsteq(lst1, lst2):
    for l1 in lst1:
        if l1 not in lst2 or lst1.count(l1) != lst2.count(l1):
            return False
    return True


def myceil(num, n=0):
    myceil = math.ceil(num * 10**n) / 10**n
    return myceil if n > 0 else math.floor(myceil)


class Agari:
    def __init__(self, oya, tsumo):
        self.oya = oya
        self.tsumo = tsumo

    def tannyao(self):
        for hai in (abs(x) for y in self.get_all() for x in y):
            if hai in yaochu:
                return False
        return True

    def iso(self):
        iso = {x//10 for x in (abs(x) for y in self.get_all() for x in y)}
        if iso == {4}:
            return 3
        elif len(iso) == 1:
            return 2
        elif len(iso) == 2 and iso > {4}:
            return 1
        return 0

    def ryuiso(self):
        ryuiso = (32, 33, 34, 36, 38, 46)
        for hai in (abs(x) for y in self.get_all() for x in y):
            if hai not in ryuiso:
                return False
        return True

    def kantsu(self):
        kan = len(self.kan + self.fu_kan)
        if kan == 4:
            return 2
        elif kan == 3:
            return 1
        return 0

    def yakuhai(self):
        yakuhai = []
        for p0 in (tuple(map(abs, x)) for x in self.get_all()[1:]):
            if p0.count(p0[0]) not in (3, 4):
                continue
            if p0[0] == ba:
                yakuhai.append("場風")
            if p0[0] == self.kaze:
                yakuhai.append("自風")
            if p0[0] in range(45, 48):
                yakuhai.append(dic[p0[0]])
        return yakuhai

    def chanta(self):
        chanta = 2
        for p0 in (tuple(map(abs, x)) for x in self.get_all()):
            ptuple = (p0[0], p0[-1])
            if set(map(lambda x: x//10, ptuple)) == {4}:
                chanta = 1
                continue
            if not set(map(lambda x: x % 10, ptuple)) & {1, 9}:
                return 0
        return chanta

    def sanshoku(self):
        ones, tens = [], []
        for p0 in (tuple(map(abs, x)) for x in self.get_all()[1:]):
            if p0[0]//10 == 4:
                continue
            ones.append(tuple(i % 10 for i in p0[:3]))
            tens.append(p0[0]//10)
        sames = tuple(ones.count(x) for x in ones)
        if not ({3, 4} & set(sames)):
            return 0
        if 1 in sames:
            ones.pop(sames.index(1))
            tens.pop(sames.index(1))
        if sorted(set(tens)) == [1, 2, 3]:
            if ones[0].count(ones[0][0]) == 1:
                return 1
            else:
                return 2
        return 0

    def anko(self):
        anko = len(self.ko)
        if anko == 4:
            return 2
        elif anko == 3:
            return 1
        return 0

    def peko(self):
        if self.get_furo():
            return False
        peko = tuple(tuple(map(abs, x)) for x in self.syu)
        sames = tuple(peko.count(x) for x in peko)
        if set(sames) == {2}:
            return 2
        for i in sames:
            if i >= 2:
                return 1
        return False

    def ittsu(self):
        syu = (tuple(map(abs, x)) for x in self.syu)
        for i in range(1, 4):
            ittsu = {
                tuple(range(i*10+1, i*10+4)),
                tuple(range(i*10+4, i*10+7)),
                tuple(range(i*10+7, i*10+10))
            }
            if ittsu <= set(syu):
                return True
        return False

    def toitoi(self):
        toitoi = len(self.ko + self.kan + self.fu_ko + self.fu_kan)
        if toitoi == 4:
            return True
        return False

    def sangen(self):
        sangen = [self.janto] + self.ko + self.kan + self.fu_ko + self.fu_kan
        sangen = (tuple(map(abs, x)) for x in sangen)
        sangen = (x for x in sangen if x[0] in range(45, 48))
        if len(tuple(sangen)) != 3:
            return 0
        if self.janto[0] in range(45, 48):
            return 1
        return 2

    def sushi(self):
        sushi = [self.janto] + self.ko + self.kan + self.fu_ko + self.fu_kan
        sushi = (tuple(map(abs, x)) for x in sushi)
        sushi = (x for x in sushi if x[0] in range(41, 45))
        if len(tuple(sushi)) != 4:
            return 0
        elif self.janto in range(41, 45):
            return 1
        return 2

    def pinfu(self):
        if len(self.syu) != 4 \
                or abs(self.janto[0]) in (ba, self.kaze) \
                or len(set(self.janto)) != 1:
            return False
        for p0 in self.syu:
            if p0[1] < 0 \
                    or tuple(x % 10 for x in p0 if x > 0) in ((1, 2), (8, 9)):
                return False
        return True

    def cul_point(self, oya, tsumo):
        if self.han < 5:
            fu = myceil(self.fu, -1) if self.fu != 25 else 25
            base = min(fu * (2 ** (self.han + 2)), 2000)
            point = []
            tmp = []
            tmp.append([])
            tmp[0].append((myceil(base*4, -2),))
            tmp[0].append((myceil(base*2, -2), myceil(base, -2)))
            point.append(tuple(tmp.pop(0)))
            tmp.append([])
            tmp[0].append((myceil(base*6, -2),))
            tmp[0].append((myceil(base*2, -2),))
            point.append(tuple(tmp.pop(0)))
        elif self.han >= 5:
            base = 200
            if self.han < 6:
                base *= 10
            elif self.han < 8:
                base *= 15
            elif self.han < 11:
                base *= 20
            elif self.han < 13:
                base *= 30
            elif self.han >= 13:
                base *= 40 * self.han // 13
            point = (((base*4,), (base*2, base)), ((base*6,), (base*2,)))
        if oya and tsumo:
            return (myceil(base*2, -2),)
        elif oya and not tsumo:
            return (myceil(base*6, -2),)
        elif not oya and tsumo:
            return (myceil(base, -2), myceil(base*2, -2))
        elif not oya and not tsumo:
            return (myceil(base*4, -2),)
        return tuple(point)


# アガリ形を分解して保持するクラス群
class Kokushi(Agari):
    def __init__(self, te, oya, tsumo):
        super().__init__(oya, tsumo)
        self.te = te
        self.double = False if len(set(t for t in te if t > 0)) != 13 else True
        self.han = 26 if self.double else 13
        self.point = self.cul_point(self.oya, self.tsumo)

    def get_yaku(self):
        return yaku.kokushi_d if self.double else yaku.kokushi

    def get_all(self):
        return sorted(self.te, key=lambda x: abs(x))


class Churen(Agari):
    def __init__(self, te, oya, tsumo):
        super().__init__(oya, tsumo)
        self.te = te
        perfect = (1,)*3 + tuple(range(2, 9)) + (9,)*3
        check = tuple(t % 10 for t in te if t > 0)
        self.double = True if check == perfect else False
        self.han = 26 if self.double else 13
        self.point = self.cul_point(self.oya, self.tsumo)

    def get_yaku(self):
        return yaku.churen_d if self.double else yaku.churen

    def get_all(self):
        return sorted(self.te, key=lambda x: abs(x))


class Chitoi(Agari):
    def __init__(self, te, oya, tsumo):
        super().__init__(oya, tsumo)
        self.te = te
        self.fu = 25
        self.get_yaku()
        self.point = self.cul_point(self.oya, self.tsumo)

    def get_fu(self):
        return self.fu

    def get_han(self):
        return self.han

    def get_yaku(self):
        yaku = []
        self.han = 0
        iso = self.iso()
        if iso == 3:
            yaku.append("役満 字一色")
            self.han += 13
            return yaku
        yaku.append("2翻 七対子")
        self.han += 2
        chanta = self.chanta()
        tannyao = self.tannyao()
        if iso == 2:
            yaku.append("6翻 清一色")
            self.han += 6
        elif iso == 1:
            yaku.append("3翻 混一色")
            self.han += 3
        if chanta:
            yaku.append("2翻 混老頭")
            self.han += 2
        if tannyao:
            yaku.append("1翻 たんやお")
            self.han += 1
        if self.tsumo:
            yaku.append("1翻 門前清自摸和")
            self.han += 1
        return yaku

    def get_all(self):
        return self.te


class Mentsu(Agari):
    def __init__(self, kaze, te, furo, oya, tsumo):
        super().__init__(oya, tsumo)
        self.kaze = kaze
        self.janto = te[0]
        self.syu = []
        self.ko = []
        self.kan = []
        self.fu_syu = []
        self.fu_ko = []
        self.fu_kan = []
        for men in te[1:]:
            if [abs(x) for x in men].count(abs(men[0])) == 1:
                self.syu.append(men)
            else:
                self.ko.append(men)
        fu_ap = {
                1: self.fu_syu.append,
                3: self.fu_ko.append,
                4: self.__split_kan
        }
        for fu in furo:
            fu_ap[tuple(abs(x) for x in fu).count(abs(fu[0]))](fu)
        self.fu = self.cul_fu()
        self.yaku = self.get_yaku()
        self.point = self.cul_point(self.oya, self.tsumo)

    def __split_kan(self, kan):
        furo = False
        for k in kan:
            if k < 0:
                furo = True
                break
        if furo:
            self.fu_kan.append(kan)
        else:
            self.kan.append(kan)

    def equal(self, agari):
        lst = [
                lsteq(self.janto, agari.janto),
                lsteq(self.syu, agari.syu),
                lsteq(self.ko, agari.ko),
                lsteq(self.kan, agari.kan),
                lsteq(self.fu_syu, agari.fu_syu),
                lsteq(self.fu_ko, agari.fu_ko),
                lsteq(self.fu_kan, agari.fu_kan)
        ]
        for ls in lst:
            if not ls:
                return False
        return True

    def cul_fu(self):
        fu = 20
        if len(self.syu + self.fu_syu) == 4:
            flag = True
            for to in self.janto:
                if to < 0:
                    fu += 2
                    flag = False
            for s in self.syu + self.fu_syu:
                if s[1] < 0:
                    flag = False
                    break
            if flag:
                if not self.get_furo() and self.tsumo:
                    fu = 20
                else:
                    fu = 30
                return fu
        if abs(self.janto[0]) in (ba, self.kaze, tuple(range(45, 48))):
            fu += (
                4 if abs(self.janto[0]) == ba and ba == self.kaze else 2
            )
        for po in self.fu_ko:
            fu += 4 if po[0] in yaochu else 2
        for po in self.ko:
            fu += 8 if po[0] in yaochu else 4
        for po in self.fu_kan:
            fu += 16 if po[0] in yaochu else 8
        for po in self.kan:
            fu += 32 if po[0] in yaochu else 16
        for s in self.syu:
            if s[1] < 0 or [x % 10 for x in s if x > 0] in ([1, 2], [8, 9]):
                fu += 2
        if self.tsumo:
            fu += 2
        elif not self.get_furo():
            fu += 10
        return fu

    def get_yaku(self):
        chanta = self.chanta()
        toitoi = self.toitoi()
        sanshoku = self.sanshoku()
        peko = self.peko()
        sangen = self.sangen()
        sushi = self.sushi()
        anko = self.anko()
        iso = self.iso()
        kantsu = self.kantsu()

        self.han = 0
        lst = []
        if chanta == 2 and toitoi:
            lst.append(yaku.chinroto)
            self.han += 13
        if sangen == 2:
            lst.append(yaku.daisangen)
            self.han += 13
        if sushi == 2:
            lst.append(yaku.daisushi)
            self.han += 26
        if sushi == 1:
            lst.append(yaku.shosushi)
            self.han += 13
        if anko == 2:
            lst.append(yaku.suanko)
            self.han += 13
        if kantsu == 2:
            lst.append(yaku.sukantsu)
            self.han += 13
        if iso == 3:
            lst.append(yaku.tsuiso)
            self.han += 13
        if self.ryuiso():
            lst.append(yaku.ryuiso)
            self.han += 13
        if lst:
            return lst
        if self.pinfu():
            lst.append(yaku.pinfu)
            self.han += 1
        if toitoi:
            lst.append(yaku.toitoi)
            self.han += 2
        if chanta == 2 and not toitoi:
            lst.append(yaku.junchan(self.get_furo()))
            self.han += 2 if self.get_furo() else 3
        if chanta == 1 and toitoi:
            lst.append(yaku.honroto)
            self.han += 2
        if chanta == 1 and not toitoi:
            lst.append(yaku.chanta(self.get_furo()))
            self.han += 1 if self.get_furo() else 2
        if sanshoku == 2:
            lst.append(yaku.doko)
            self.han += 2
        if sanshoku == 1:
            lst.append(yaku.doujun(self.get_furo()))
            self.han += 1 if self.get_furo() else 2
        if peko == 2:
            lst.append(yaku.peko(2))
            self.han += 3
        if peko == 1:
            lst.append(yaku.peko(1))
            self.han += 1
        if self.ittsu():
            lst.append(yaku.ittsu(self.get_furo()))
            self.han += 1 if self.get_furo() else 2
        if sangen == 1:
            lst.append(yaku.shosangen)
            self.han += 2
        if anko == 1:
            lst.append(yaku.sannanko)
            self.han += 2
        if kantsu == 1:
            lst.append(yaku.sankantsu)
            self.han += 2
        if self.tannyao():
            lst.append(yaku.tannyao)
            self.han += 1
        if iso == 2:
            lst.append(yaku.chiniso(self.get_furo()))
            self.han += 5 if self.get_furo() else 6
        if iso == 1:
            lst.append(yaku.honniso(self.get_furo()))
            self.han += 2 if self.get_furo() else 3
        if self.tsumo and not self.get_furo():
            lst.append(yaku.tsumo)
            self.han += 1
        for y in self.yakuhai():
            lst.append(y)
            self.han += 1
        return lst

    def get_point(self, oya, tsumo):
        return self.point

    def get_te(self):
        return [self.janto] + self.ko + self.syu + self.kan

    def get_furo(self):
        return self.fu_ko + self.fu_syu + self.fu_kan

    def get_all(self):
        return self.get_te() + self.get_furo()


# 手牌を管理したり上がり形判定したりするクラス
# 判定部分は後で分離した方がいい気もする
class Tehai:
    def __init__(self, te=None, furo=None):
        if not te:
            te = rndlst(lst*4)[:14]
        if not furo:
            furo = []
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
    @classmethod
    def pop_kotsu(cls, te):
        ko, t = [], te.copy()
        for s in te:
            if t.count(s) >= 3:
                ko.append([s]*3)
                del t[t.index(s):t.index(s)+3]
        return ko, t

# 順子をカウントする
    @classmethod
    def pop_shuntsu(cls, te):
        syu, t = [], te.copy()
        for s in te:
            if s//10 == 4:
                continue
            while s in te:
                if {s, s+1, s+2} <= set(t):
                    syu.append([s, s+1, s+2])
                    for i in range(s, s+3):
                        t.remove(i)
                else:
                    break
        return syu, t

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
        # tehai = sorted(self.tehai[:-1])+self.tehai[-1:]
        tehai = sorted(self.tehai)
        target = []
        agari = []
        for t in toi:
            target.append(rmlst(tehai, t, 2))
        for t, t2 in zip(target, toi):
# 含まれている対子毎にそれを雀頭として残りを解析
# 刻子優先、順子は正順
            t1 = t.copy()
            ko = []
            syu = []
            ko, t1 = Tehai.pop_kotsu(t1)
            syu, t1 = Tehai.pop_shuntsu(t1)
            if len(ko+syu+self.furo) == 4:
                tmp = [[t2]*2]+ko+syu
                for i in range(len(tmp)):
                    if self.tsumo in tmp[i]:
                        alt = tmp[i].copy()
                        alt[alt.index(self.tsumo)] *= -1
                        agari.append(Mentsu(
                            ji, tmp[:i]+[alt]+tmp[i+1:], self.furo, oya, tsumo
                        ))
#                 agari.append([[t2]*2]+ko+syu)
# 刻子優先、順子は逆順
#             t1 = t.copy()
#             ko = []
#             syu = []
#             ko, t1 = Tehai.pop_kotsu(t1)
#             syu, t1 = Tehai.pop_shuntsu(t1[::-1])
#             if len(ko+syu+self.furo) == 4:
#                 agari.append([[t2]*2]+ko+syu[::-1])
# 順子優先、順子は正順
            t1 = t.copy()
            ko = []
            syu = []
            syu, t1 = Tehai.pop_shuntsu(t1)
            ko, t1 = Tehai.pop_kotsu(t1)
            if len(ko+syu+self.furo) == 4:
                tmp = [[t2]*2]+ko+syu
                for i in range(len(tmp)):
                    if self.tsumo in tmp[i]:
                        alt = tmp[i].copy()
                        alt[alt.index(self.tsumo)] *= -1
                        agari.append(Mentsu(
                            ji, tmp[:i]+[alt]+tmp[i+1:], self.furo, oya, tsumo
                        ))
#                 agari.append([[t2]*2]+ko+syu)
# 順子優先、順子は逆順
#             t1 = t.copy()
#             ko = []
#             syu = []
#             syu, t1 = Tehai.pop_shuntsu(t1[::-1])
#             ko, t1 = Tehai.pop_kotsu(t1)
#             if len(ko+syu+self.furo) == 4:
#                 agari.append([[t2]*2]+(syu+ko)[::-1])
        agari2 = []
        for a1 in agari:
            flag = True
            for a2 in agari2:
                if a1.equal(a2):
                    flag = False
                    break
            if flag:
                agari2.append(a1)
        return agari2


# あたり牌を検索
    def atari(self):
        atari = []
        for hai in lst:
            tehai = Tehai(sorted(self.tehai+[hai]), self.furo)
            if tehai.hantei(False):
                atari.append(hai)
        return atari

# アガリ状態かどうか判定する
    def hantei(self, flag):
        if set(self.tehai) == set(yaochu):
            tmp = self.tehai.copy()
            tmp[len(tmp)-tmp[::-1].index(self.tsumo)-1] *= -1
            self.agari = [Kokushi(tmp, oya, tsumo)]
            if flag:
                print(*[dic[x] for x in self.agari[0].get_all()])
                print(" " + self.agari[0].get_yaku())
                print(f" {self.agari[0].point}")
            return True

        for i in range(1, 4):
            if set(self.tehai) != set(range(i*10+1, i*10+10)):
                continue
            if self.tehai.count(i*10+1) >= 3 \
                    and self.tehai.count(i*10+9) >= 3:
                tmp = self.tehai.copy()
                tmp[len(tmp)-tmp[::-1].index(self.tsumo)-1] *= -1
                self.agari = [Churen(tmp, oya, tsumo)]
                if flag:
                    print(*[dic[x] for x in self.agari[0].get_all()])
                    print(" " + self.agari[0].get_yaku())
                    print(f" {self.agari[0].point}")
                return True

        agari = self.analysis()
        if agari:
            if flag:
                print("雀頭1 面子4")
                self.agari = []
                for a1 in agari:
                    if a1 not in self.agari:
                        self.agari.append(a1)
                        for p in a1.get_all():
                            print("".join([dic[x] for x in p]), end=" ")
                        print()
                        for y in a1.get_yaku():
                            print(f" {y}")
                        print()
                        print(f" {a1.fu}符 {a1.han}翻")
                        print(f" {a1.point}\n")
            return True

        if len(self.count_toi()) == 7:
            tmp = [[x, x] for x in self.count_toi()]
            for t in tmp:
                if t[0] == self.tsumo:
                    t[0] *= -1
            self.agari = [Chitoi(tmp, oya, tsumo)]
            if flag:
                for p in self.agari[0].get_all():
                    print("".join([dic[x] for x in p]), end=" ")
                print()
                for y in self.agari[0].get_yaku():
                    print(f" {y}")
                print(f" {self.agari[0].fu}符 {self.agari[0].han}翻")
                print(f" {self.agari[0].point}")
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
        if hai < 0 or hai > len(self.tehai):
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
    def get_all(self):
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
            print(f"場風:{dic[ba]} 自風:{dic[ji]}")
            print(f"親:{oya}, ツモ:{tsumo}")
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
                            break
                else:
                    kiru = []
                    for i in range(len(tehai.tehai)):
                        tmp = tehai.tehai[:i] + tehai.tehai[i+1:]
                        tempai = Tehai(tmp, tehai.furo)
                        if tempai.atari() and tehai.tehai[i] not in kiru:
                            kiru.append(tehai.tehai[i])
                    print("聴牌:", *[dic[x] for x in sorted(kiru)])
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
# 'ba' で場風指定, 'ji' で自風指定
            if usrinput and usrinput.split()[0] in ['ba', 'ji']:
                if len(usrinput.split()) != 2:
                    continue
                if usrinput.split()[1].isdigit():
                    if int(usrinput.split()[1]) in [41, 42, 43, 44]:
                        if usrinput.split()[0] == 'ba':
                            ba = int(usrinput.split()[1])
                        else:
                            ji = int(usrinput.split()[1])
                continue
# 'random' でランダムツモモード
            if usrinput == 'random':
                if len(tehai.tehai)+len(tehai.furo)*3 == 13:
                    rndtsumo(tehai, ho)
                mode = 3
                continue
            if usrinput == 'debug':
                mode = 2
                continue
            if usrinput == 'oya':
                oya = False if oya else True
            if usrinput == 'tsumo':
                tsumo = False if tsumo else True
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
                    furable.append([tehai.tsumo]*2)
                if tehai.tehai.count(tehai.tsumo) == 4:
                    furable.append([tehai.tsumo]*3)
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
                if len(furable[int(usrinput)]) == 3:
                    if mode == 2:
                        mode = 1
                    elif mode == 3:
                        tehai.tsumo = rndtsumo(tehai, ho)
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
