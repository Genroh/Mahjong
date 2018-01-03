#!/usr/bin/env python
# fileencoding=utf-8

# Written By python 3.6.1

import os
import random

# 牌に使う数値と文字の対応
lst=[i for i in range(11,48) if i%10!=0]
conv=['一','二','三','四','五','六','七','八','九',
      '１','２','３','４','５','６','７','８','９',
      '①','②','③','④','⑤','⑥','⑦','⑧','⑨',
      '東','南','西','北','白','發','中']
dic=dict(zip(lst,conv))

# 手牌を管理したり上がり形判定したりするクラス
# 判定部分は後で分離した方がいい気もする
class Tehai:
    def __init__(self):
        self.tehai = lst*4
        random.shuffle(self.tehai)
        self.tehai = sorted(self.tehai[:14])

# 刻子をカウントする
    def __kotsu(self, t, tset, ko):
        for s in tset:
            if t.count(s) >=3:
                ko.append(" ".join([dic[s]]*3))
                del t[t.index(s):t.index(s)+3]

# 順子をカウントする
    def __syuntsu(self, t, tset, syu):
        for s in tset:
            if s//10 == 4:
                continue
            while s in t:
                if s in t and s+1 in t and s+2 in t:
                    syu.append(" ".join([dic[x] for x in range(s, s+3)]))
#                    syu.append(" ".join(map(str, [s,s+1,s+2])))
                    del t[t.index(s)]
                    del t[t.index(s+1)]
                    del t[t.index(s+2)]
                else:
                    break

# 対子をカウントしてそのリストを返す
    def count_toi(self):
        dic = dict(zip(lst, [0]*len(lst)))
        for x in self.tehai:
            dic[x]+=1
        cnt=[k for k,v in dic.items() if v>=2]
        return cnt

# 一般的なアガリ形かどうかを解析する
    def analysis(self):
        toi=self.count_toi()
        tehai = sorted(self.tehai)
        target=[]
        agari=[]
        for t in toi:
            target.append(tehai[:tehai.index(t)]
                    +tehai[tehai.index(t)+2:])
        for t,t2 in zip(target,toi):
# 含まれている対子毎にそれを雀頭として残りを解析
            tset=sorted(set(t), key=t.index)
            t1=t
            ko=[]
            syu=[]
            self.__kotsu(t1, tset, ko)
            self.__syuntsu(t1, tset, syu)
            if len(ko+syu) == 4:
# 刻子優先、順子は正順
                agari.append([" ".join([dic[t2]]*2)]+ko+syu)
            t1=t
            ko=[]
            syu=[]
            self.__kotsu(t1, tset[::-1], ko)
            self.__syuntsu(t1, tset[::-1], syu)
            if len(ko+syu) == 4:
# 刻子優先、順子は逆順
                agari.append([" ".join([dic[t2]]*2)]+(ko+syu)[::-1])
            t1=t
            ko=[]
            syu=[]
            self.__syuntsu(t1, tset, syu)
            self.__kotsu(t1, tset, ko)
            if len(ko+syu) == 4:
# 順子優先、順子は正順
                agari.append([" ".join([dic[t2]]*2)]+ko+syu)
            t1=t
            ko=[]
            syu=[]
            self.__syuntsu(t1, tset[::-1], syu)
            self.__kotsu(t1, tset[::-1], ko)
            if len(ko+syu) == 4:
# 順子優先、順子は逆順
                agari.append([" ".join([dic[t2]]*2)]+(ko+syu)[::-1])
        return agari

# タンヤオ
    def tanyao(self):
        for hai in self.tehai:
            if hai//10==4 or hai%10==1 or hai%10==9:
                return False
        return True

# あたり牌を検索
    def atari(self):
        atari=[]
        for hai in lst:
            tehai = Tehai()
            tehai.tehai = sorted(self.tehai+[hai])
            if tehai.hantei(False):
                atari.append(dic[hai])
        print("当たり牌:", *atari)

# アガリ状態かどうか判定する
    def hantei(self,flag):
        tmp=[]
        for t in sorted(self.tehai):
            if t not in tmp:
                tmp.append(t)
        if tmp == [11,19,21,29,31,39,41,42,43,44,45,46,47]:
            if flag:
                print("国士無双")
                print([dic[x] for x in self.tehai])
            return True

        if len(self.count_toi()) == 7:
            if flag:
                print("七対子")
                print(["%c %c"%(dic[x],dic[x]) for x in self.count_toi()])
            return True

        agari=self.analysis()
        if agari:
            if flag:
                print("雀頭1 面子4")
                l=[]
                for a in agari:
                    if a not in l:
                        l.append(a)
                        print(a)
            return True
        return False

# ツモる
    def set(self, hai):
        if hai<11 or hai>47 or hai%10==0:
            return False
        self.tehai.append(hai)
        self.tsumo = hai
        return True

# 手牌を切る
    def pop(self, hai):
        if hai<0 or hai>13:
            return False
        self.tehai.pop(hai)
        self.tsumo = None
        self.tehai.sort()
        return True

# 手牌を対応する文字に変換
    def conv(self):
        return [dic[x] for x in self.tehai]


# このファイルを実行する時の処理
if __name__ == '__main__':

    tehai = Tehai()
    mode = 2    # mode 1:ツモ 2:切る
    try:
        while True:
            os.system('cls')
# 数値と文字の対応表を表示
            print("  ", *["%2d"%i for i in range(1,10)])
            for i in range(4):
                print("%d"%((i+1)*10), *conv[i*9:(i+1)*9])
            print()
# モード表示
            print("mode =", mode)
            print()
            print(*["%02d"%x for x in range(14)])
            print(*tehai.conv())
            print()
            print("対子:",*[dic[x] for x in tehai.count_toi()])
            print()
            if mode == 1:
                tehai.atari()
            if mode == 2:
                if tehai.hantei(True):
                    if tehai.tanyao():
                        print("たんやお",end="")
                    print()
            print("\n > ", end="")
            usrinput=input()
# 'q' または ':q' で終了
            if usrinput=='q' or usrinput==':q':
                break
            if not usrinput.isdigit():
                continue
            if mode == 1:
                if tehai.set(int(usrinput)):
                    mode = 2
            elif mode == 2:
                if tehai.pop(int(usrinput)):
                    mode = 1
# Ctrl+C で終了
    except KeyboardInterrupt:
        print()

