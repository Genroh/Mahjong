#!/usr/bin/env python
# fileencoding=utf-8

# Written By python 3.6.1

import os
import sys
import random
import pdb

# 牌に使う数値と文字の対応
lst = [i for i in range(11, 48) if i % 10 != 0]
conv = ('一', '二', '三', '四', '五', '六', '七', '八', '九',
        '１', '２', '３', '４', '５', '６', '７', '８', '９',
        'Ⅰ', 'Ⅱ', 'Ⅲ', 'Ⅳ', 'Ⅴ', 'Ⅵ', 'Ⅶ', 'Ⅷ', 'Ⅸ',
        '東', '南', '西', '北', '白', '發', '中')
dic = dict(zip(lst, conv))
dic.update(zip([-x for x in lst],
           map(lambda x: f"\033[031m"+x+"\033[00m", conv)))

ba = 41
ji = 41


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


# アガリ形を分解して保持するクラス
class Agari:
    def __init__(self, tsumo, kaze, janto, mentsu, furo):
        self.tsumo = tsumo
        self.kaze = kaze
        self.janto = janto
        self.syu = []
        self.ko = []
        self.kan = []
        self.fu_syu = []
        self.fu_ko = []
        self.fu_kan = []
        for men in mentsu:
            if [abs(x) for x in men].count(abs(men[0])) == 1:
                self.syu.append(men)
            else:
                self.ko.append(men)
        fu_ap = {
                1:self.fu_syu.append,
                3:self.fu_ko.append,
                4:self.__split_kan
        }
        for fu in furo:
            fu_ap[[abs(x) for x in fu].count(abs(fu[0]))](fu)

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
    def pop_kotsu(self, te):
        ko, t = [], te.copy()
        for s in te:
            if t.count(s) >= 3:
                ko.append([s]*3)
                del t[t.index(s):t.index(s)+3]
        return ko, t

# 順子をカウントする
    def pop_shuntsu(self, te):
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
            ko, t1 = self.pop_kotsu(t1)
            syu, t1 = self.pop_shuntsu(t1)
            if len(ko+syu+self.furo) == 4:
                tmp = [[t2]*2]+ko+syu
                for i in range(len(tmp)):
                    if self.tsumo in tmp[i]:
                        alt = tmp[i].copy()
                        alt[alt.index(self.tsumo)] *= -1
                        agari.append(tmp[:i] + [alt] + tmp[i+1:])
#                 agari.append([[t2]*2]+ko+syu)
# 刻子優先、順子は逆順
#             t1 = t.copy()
#             ko = []
#             syu = []
#             ko, t1 = self.pop_kotsu(t1)
#             syu, t1 = self.pop_shuntsu(t1[::-1])
#             if len(ko+syu+self.furo) == 4:
#                 agari.append([[t2]*2]+ko+syu[::-1])
# 順子優先、順子は正順
            t1 = t.copy()
            ko = []
            syu = []
            syu, t1 = self.pop_shuntsu(t1)
            ko, t1 = self.pop_kotsu(t1)
            if len(ko+syu+self.furo) == 4:
                tmp = [[t2]*2]+ko+syu
                for i in range(len(tmp)):
                    if self.tsumo in tmp[i]:
                        alt = tmp[i].copy()
                        alt[alt.index(self.tsumo)] *= -1
                        agari.append(tmp[:i] + [alt] + tmp[i+1:])
#                 agari.append([[t2]*2]+ko+syu)
# 順子優先、順子は逆順
#             t1 = t.copy()
#             ko = []
#             syu = []
#             syu, t1 = self.pop_shuntsu(t1[::-1])
#             ko, t1 = self.pop_kotsu(t1)
#             if len(ko+syu+self.furo) == 4:
#                 agari.append([[t2]*2]+(syu+ko)[::-1])
        agari2 = []
        for a1 in agari:
            flag = False
            for a2 in agari2:
                for a3 in a1:
                    if a3 not in a2 or a1.count(a3) != a2.count(a3):
                        flag = True
            if flag or not agari2:
                agari2.append(a1)
        return agari2

# タンヤオ
    def tanyao(self):
        for hai in self.tehai + [x for y in self.furo for x in y]:
            if hai//10 == 4 or hai % 10 == 1 or hai % 10 == 9:
                return False
        return True

# 混一色 or 清一色 or 字一色
    def iso(self):
        iso = self.tehai + [x for y in self.furo for x in y]
        iso = {x//10 for x in iso}
        if len(iso) == 1 and 4 in iso:
            return 3
        elif len(iso) == 1:
            return 2
        elif len(iso) == 2 and 4 in iso:
            return 1
        return 0

# 緑一色
    def ryuiso(self):
        ryuiso = [32, 33, 34, 36, 38, 46]
        for hai in self.tehai:
            if hai not in ryuiso:
                return False
        return True

# 槓子
    def kantsu(self, furo):
        kantsu = 0
        for f in furo:
            if len(f) == 4:
                kantsu += 1
        if kantsu == 4:
            return 2
        elif kantsu == 3:
            return 1
        return 0

# 役牌
    def yakuhai(self, lst):
        yakuhai = []
        for p in lst[1:]:
            if [abs(x) for x in p].count(p[0]) not in [3, 4]:
                continue
            if p[0] == ba:
                yakuhai.append(p[0])
            if p[0] == ji:
                yakuhai.append(p[0])
            if p[0] in range(45, 48) and p[0] not in yakuhai:
                yakuhai.append(p[0])
        return yakuhai

# チャンタ or 純チャンタ
    def chanta(self, lst):
        chanta = 2   # [純チャン, チャンタ]
        for p in lst:
            if abs(p[0]) % 10 not in [1, 9] and abs(p[-1]) % 10 not in [1, 9]:
                chanta = 1
                if abs(p[0])//10 != 4 and abs(p[-1])//10 != 4:
                    return 0
        return chanta

# 三色同順 or 三色同刻
    def sansyoku(self, lst):
        ones, tens = [], []
        for p in lst[1:]:
            if abs(p[0])//10 == 4:
                continue
            ones.append([i % 10 for i in p][:3])
            tens.append(p[0]//10)
        sames = [ones.count(x) for x in ones]
        if not {3, 4} & set(sames):
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

# 三暗刻 or 四暗刻
    def anko(self, lst):
        count = 0
        for p in [list(map(abs, x)) for x in lst[1:]]:
            if p.count(p[0]) in [3, 4]:
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
        for p in [list(map(abs, x)) for x in lst[1:]]:
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
        lst = [abs(x) for inner in lst[1:] for x in inner]
        for i in range(1, 4):
            if set(range(i*10+1, i*10+10)) <= set(lst):
                return True
        return False

# 対々和
    def toitoi(self, lst):
        for l in [list(map(abs, x)) for x in lst[1:]]:
            if l.count(l[0]) != 3:
                return False
        return True

# 小三元 or 大三元
    def sangen(self, lst):
        count = 0
        lst = [abs(x) for inner in lst for x in inner]
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
        lst = [abs(x) for inner in lst for x in inner]
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
        if self.furo or lst[0][0] in [ba, ji] + list(range(45, 48)):
            return False
        pinfu = False
        for p0 in lst[1:]:
            if [abs(x) for x in p0].count(abs(p0[0])) != 1:
                return False
            if p0[0] * p0[-1] < 0:
                if [x % 10 for x in p0 if self.tsumo != x] in [[1, 2], [8, 9]]:
                    return False
                pinfu = True
        return pinfu


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
        tmp = []
        for t in sorted(self.tehai):
            if t not in tmp:
                tmp.append(t)
        if tmp == [11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 45, 46, 47]:
            if flag:
                print(*[dic[x] for x in self.tehai])
                print(" 役満 国士無双")
            return True

        for i in range(1, 4):
            if set(self.tehai) != set(range(i*10+1, i*10+10)):
                continue
            if self.tehai.count(i*10+1) >= 3 \
                    and self.tehai.count(i*10+9) >= 3:
                if flag:
                    print(*[dic[x] for x in self.tehai])
                    print(" 役満 九蓮宝燈")
                return True

        agari = self.analysis()
        if agari:
            if flag:
                print("雀頭1 面子4")
                self.agari = []
                for a1 in agari:
                    if a1 not in self.agari:
                        self.agari.append(a1)
                        a1.extend(self.furo)
                        for p in a1:
                            print("".join([dic[x] for x in p]), end=" ")
                        print()
                        chanta = self.chanta(a1)
                        toitoi = self.toitoi(a1)
                        sansyoku = self.sansyoku(a1)
                        peko = self.peko(a1)
                        sangen = self.sangen(a1)
                        sushi = self.sushi(a1)
                        anko = self.anko([x for x in a1 if x not in self.furo])
                        iso = self.iso()
                        kantsu = self.kantsu(self.furo)
                        yaku = ""
                        if chanta == 2 and toitoi:
                            yaku += " 役満 清老頭\n"
                        if sangen == 2:
                            yaku += " 役満 大三元\n"
                        if sushi == 2:
                            yaku += " ダブル役満 大四喜\n"
                        if sushi == 1:
                            yaku += " 役満 小四喜\n"
                        if anko == 2:
                            yaku += " 役満 四暗刻\n"
                        if kantsu == 2:
                            yaku += " 役満 四槓子\n"
                        if iso == 3:
                            yaku += " 役満 字一色\n"
                        if self.ryuiso():
                            yaku += " 役満 緑一色\n"
                        if yaku:
                            print(yaku)
                            return True
                        han = 0
                        if self.pinfu(a1):
                            yaku += " 1翻 平和\n"
                            han += 1
                        if toitoi:
                            yaku += " 2翻 対々和\n"
                            han += 2
                        if chanta == 2 and not toitoi:
                            yaku += f" {2 if self.furo else 3}翻 純チャン\n"
                            han += 2 if self.furo else 3
                        if chanta == 1 and toitoi:
                            yaku += " 2翻 混老頭\n"
                            han += 2
                        if chanta == 1 and not toitoi:
                            yaku += f" {1 if self.furo else 2}翻 チャンタ\n"
                            han += 1 if self.furo else 2
                        if sansyoku == 2:
                            yaku += " 2翻 三色同刻\n"
                            han += 2
                        if sansyoku == 1:
                            yaku += f" {1 if self.furo else 2}翻 三色同順\n"
                            han += 1 if self.furo else 2
                        if peko == 2:
                            yaku += " 3翻 二盃口\n"
                            han += 3
                        if peko == 1:
                            yaku += " 1翻 一盃口\n"
                            han += 1
                        if self.ittsu(a1):
                            yaku += f" {1 if self.furo else 2}翻 一気通貫\n"
                            han += 1 if self.furo else 2
                        if sangen == 1:
                            yaku += " 2翻 小三元\n"
                            han += 2
                        if anko == 1:
                            yaku += " 2翻 三暗刻\n"
                            han += 2
                        if kantsu == 1:
                            yaku += " 2翻 三槓子\n"
                            han += 2
                        if self.tanyao():
                            yaku += " 1翻 たんやお\n"
                            han += 1
                        if iso == 2:
                            yaku += f" {5 if self.furo else 6}翻 清一色\n"
                            han += 5 if self.furo else 6
                        if iso == 1:
                            yaku += f" {2 if self.furo else 3}翻 混一色\n"
                            han += 2 if self.furo else 3
                        if not self.furo:
                            yaku += " 1翻 門前清自摸和\n"
                            han += 1
                        yakuhai = self.yakuhai(a1)
                        for y in yakuhai:
                            yaku += f" 1翻 {dic[y]}\n"
                            han += 1
                        if yaku:
                            print(yaku)
                            print(f" {han}翻\n")
            return True

        if len(self.count_toi()) == 7:
            if flag:
                for x in self.count_toi():
                    print(dic[x]+dic[x], end=" ")
                print()
                yaku = ""
                han = 0
                chanta = self.chanta([[x] for x in self.count_toi()])
                iso = self.iso()
                if iso == 3:
                    print(" 役満 字一色")
                    return True
                yaku = yaku + " 2翻 七対子\n"
                han += 2
                if chanta == 1:
                    yaku += " 2翻 混老頭\n"
                    han += 2
                if self.tanyao():
                    yaku += " 1翻 たんやお\n"
                    han += 1
                if iso == 2:
                    yaku += " 6翻 清一色\n"
                    han += 6
                print(yaku)
                print(f" {han}翻\n")
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
            print("場風:", dic[ba], "自風:", dic[ji])
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
