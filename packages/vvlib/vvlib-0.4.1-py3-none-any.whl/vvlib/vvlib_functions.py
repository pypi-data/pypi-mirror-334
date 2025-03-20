import random
from random import randint, choice
import turtle
from time import sleep
import os


def goofitize(text: str):
    text = list(text)
    n_text = []
    for i in text:
        goof_coeff = randint(0,1)
        if goof_coeff == 1:
            n_text.append(i.upper())
        else:
            n_text.append(i.lower())
    return "".join(n_text)

def vv_shuffle(ts : str or list):
    was = type(ts)
    ts = list(ts)
    for i in range(random.randint(len(ts), len(ts)+5)):
        fnum = random.randint(0,len(ts)-1)
        snum = random.randint(0, len(ts)-1)

        frng = ts[fnum]
        srng = ts[snum]

        ts[fnum] = srng
        ts[snum] = frng
    if was == list:
        pass
    elif was == str:
        ts = "".join(ts)

    return ts

list_of_goof = [
    "( ͡° ͜ʖ ͡°)",
    "¯\_(ツ)_/¯",
    "ʕ•ᴥ•ʔ",
    "ಠ_ಠ",
    "(͡ ͡° ͜ つ ͡͡°)",
    "(ง'̀-'́)ง",
    "(ಥ﹏ಥ)",
    "(◕‿◕✿)"
]

def vv_append(your_list: list, appendage):
    goof_coeff = random.randint(1,3)
    if goof_coeff == 1:
        your_list.append(random.choice(list_of_goof))
    else:
        your_list.append(appendage)

    return your_list

def vv_banish(offering: str):
    s = turtle.getscreen()
    t = turtle.Turtle()
    wt = turtle.Turtle()
    def tur_pent():
        #t.up()
        t.home()
        t.down()
        t.speed(0)
        t.pencolor("red")
        t.forward(150)
        t.left(180)
        t.down()
        t.forward(300)
        t.right(165)
        t.forward(250)
        t.right(130)
        t.forward(200)
        t.right(130)
        t.forward(200)
        t.right(131)
        t.forward(250)
        t.up()

    def offer(move, whw):
        wt.up()
        wt.home()
        wt.left(90)
        wt.forward(move)
        wt.pencolor("black")
        wt.write(whw, False, "center")

    tur_pent()
    offer(200, offering)
    sleep(1)
    wt.clear()
    offer(150, offering)
    sleep(1)
    wt.clear()
    offer(100, offering)
    sleep(1)
    wt.clear()
    offer(50, offering)
    sleep(1)
    wt.clear()
    offer(10, offering)
    wt.clear()
    wt.pencolor("red")
    offer(10, "Offering accepted")

    sleep(5)

#POZOR NEVOLAT POZOR NEVOLAT
def ragequit():
    os.system("shutdown /p")
#POZOR NEVOLAT POZOR NEVOLAT