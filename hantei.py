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
        self.tsumo = self.tehai[13]

# 刻子をカウントする
    def __kotsu(self, t, tset, ko):
        for s in tset:
            if t.count(s) >=3:
                ko.append([s]*3)
                del t[t.index(s):t.index(s)+3]

# 順子をカウントする
    def __syuntsu(self, t, tset, syu):
        for s in tset:
            if s//10 == 4:
                continue
            while s in t:
                if s in t and s+1 in t and s+2 in t:
                    syu.append([s,s+1,s+2])
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
# 刻子優先、順子は正順
            t1=t.copy()
            ko=[]
            syu=[]
            self.__kotsu(t1, tset, ko)
            self.__syuntsu(t1, tset, syu)
            if len(ko+syu) == 4:
                agari.append([[t2]*2]+ko+syu)
# 刻子優先、順子は逆順
            t1=t.copy()
            ko=[]
            syu=[]
            self.__kotsu(t1, tset[::-1], ko)
            self.__syuntsu(t1, tset[::-1], syu)
            if len(ko+syu) == 4:
                agari.append([[t2]*2]+(ko+syu)[::-1])
# 順子優先、順子は正順
            t1=t.copy()
            ko=[]
            syu=[]
            self.__syuntsu(t1, tset, syu)
            self.__kotsu(t1, tset, ko)
            if len(ko+syu) == 4:
                agari.append([[t2]*2]+ko+syu)
# 順子優先、順子は逆順
            t1=t.copy()
            ko=[]
            syu=[]
            self.__syuntsu(t1, tset[::-1], syu)
            self.__kotsu(t1, tset[::-1], ko)
            if len(ko+syu) == 4:
                agari.append([[t2]*2]+(ko+syu)[::-1])
        return agari

# タンヤオ
    def tanyao(self):
        for hai in self.tehai:
            if hai//10==4 or hai%10==1 or hai%10==9:
                return False
        return True

# チャンタor純チャンタ
    def chanta(self,lst):
        chanta=[True,True]  #[純チャン, チャンタ]
        for p in lst:
            if p[0]%10 not in [1,9] and p[-1]%10 not in [1,9]:
                chanta[0] = False
                if p[0]//10 != 4 and p[-1]//10 != 4:
                    chanta[1] = False
        return chanta

# 三色同順or三色同刻
    def sansyoku(self,lst):
        sansyoku=[False,False]
        ones,tens=[],[]
        for p in lst[1:]:
            if p[0]//10==4:
                continue
            ones.append([i%10 for i in p])
            tens.append(p[0]//10)
        sames=[ones.count(x) for x in ones]
        if 3 not in sames and 4 not in sames:
            return sansyoku
        if 1 in sames:
            ones.pop(sames.index(1))
            tens.pop(sames.index(1))
        if sorted(set(tens))==[1,2,3]:
            if ones[0].count(ones[0][0])==1:
                sansyoku[0]=True
            else:
                sansyoku[1]=True
        return sansyoku

# 一盃口
    def ipeko(self, lst):
        ipeko=[]
        for p in lst[1:]:
            if p.count(p[0])==1:
                ipeko.append(p)
        sames=[ipeko.count(x) for x in ipeko]
        for i in sames:
            if i>=2:
                return True
        return False

# 平和
    def pinfu(self, lst):
        for p in lst[1:]:
            if p.count(p[0]) != 1:
                return False
            if self.tsumo in [p[0],p[-1]]:
                if ((self.tsumo-3)%10)*((self.tsumo+3)%10)!=0:
                    return True
        return False


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
                self.agari=[]
                for a in agari:
                    if a not in self.agari:
                        self.agari.append(a)
                        print([" ".join([dic[x] for x in p]) for p in a])
                        if self.pinfu(a):
                            print("平和",end=" ")
                        chanta=self.chanta(a)
                        if chanta[0]:
                            print("純チャン",end=" ")
                        elif chanta[1]:
                            print("チャンタ",end=" ")
                        sansyoku=self.sansyoku(a)
                        if sansyoku[0]:
                            print("三色同順",end=" ")
                        elif sansyoku[1]:
                            print("三色同刻",end=" ")
                        if self.ipeko(a):
                            print("一盃口",end=" ")
                        print()
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
            print("  ", *[f"{i:2}" for i in range(1,10)])
            for i in range(4):
                print(f"{(i+1)*10}", *conv[i*9:(i+1)*9])
            print()
# モード表示
            print("mode =", mode)
            print()
            print(*[f"{x:02}" for x in range(14)])
            print(*tehai.conv())
            print()
            print("対子:",*[dic[x] for x in tehai.count_toi()])
            print()
            if mode == 1:
                tehai.atari()
            if mode == 2:
                if tehai.hantei(True):
                    if tehai.tanyao():
                        print("たんやお",end=" ")
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

