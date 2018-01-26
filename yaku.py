#!/usr/bin/env python
# fileencoding=utf-8

# Written By python 3.6.1

chinroto = "役満 清老頭"
honroto = "2翻 混老頭"
daisangen = "役満 大三元"
shosangen = "2翻 小三元"
daisushi = "ダブル役満 大四喜"
shosushi = "役満 小四喜"
suanko = "役満 四暗刻"
sannanko = "2翻 三暗刻"
sukantsu = "役満 四槓子"
sankantsu = "2翻 三槓子"
tsuiso = "役満 字一色"
ryuiso = "役満 緑一色"
pinfu = "1翻 平和"
toitoi = "2翻 対々和"
doko = "2翻 三色同刻"
tannyao = "1翻 たんやお"
tsumo = "1翻 門前清自摸和"
bakaze = "1翻 場風"
jikaze = "1翻 自風"
sangen = ("1翻 白", "1翻 發", "1翻 中")

def junchan(flag):
    return f"{2 if flag else 3}翻 純チャン"
def chanta(flag):
    return f"{1 if flag else 2}翻 チャンタ"
def doujun(flag):
    return f"{1 if flag else 2}翻 三色同順"
def ittsu(flag):
    return f"{1 if flag else 2}翻 一気通貫"
def chiniso(flag):
    return f"{5 if flag else 6}翻 清一色"
def honniso(flag):
    return f"{2 if flag else 3}翻 混一色"
def peko(num):
    if num == 2:
        return "3翻 二盃口"
    if num == 1:
        return "1翻 一盃口"

