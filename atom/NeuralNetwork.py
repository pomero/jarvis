import sys

class Cell:
    def __init__(self, name, thre):
        self._fire = False
        self._name = name
        self._thre = thre
        print("Cell __init__ called")

    def pp(self):
        print("'%s'" % (self._name), "thre is", self._thre)

    def clear(self):
        self._fire = False

    @property
    def fire(self):
        return self._fire

    def inc(self):
        self._thre += 1

    def dec(self):
        if self._thre <= 0:
            return
        self._thre -= 1


class LastCell(Cell):
    def __init__(self, name, thre):
        Cell.__init__(self, name, thre)
        self._cur = 0

    def act(self, thre):
        self._cur += thre
        if self._cur < self._thre:
            return
        self._fire = True

    def clear(self):
        Cell.clear(self)
        self._cur = 0

class TopCell(Cell):
    def __init__(self, name, thre, link, price):
        Cell.__init__(self, name, thre)
        self._link = link
        self._price = price

    def act(self):
        self._fire = True
        if self._link is None:
            return
        self._link.act(self._thre)

    def getPrice(self):
        return self._price


def learn(result, lastCell, fireTopCells):
    lea = True
    res = result()
    if res and lastCell.fire:
        print("buy over but cell fire... learn!")
        for c in fireTopCells: c.dec()
        lastCell.inc()
    elif not res and not lastCell.fire:
        print("buy in but cell unfire... learn!")
        for c in fireTopCells: c.inc()
        lastCell.dec()
    elif not res and lastCell.fire:
        print("buy over and cell fire @@@OK@@@")
        lea = False
    else:
        print("buy in and cell unfire @@@OK@@@")
        lea = False
    return lea

def calc(cells):
    MONEY = 500
    total = 0
    for c in cells:
        total += c.getPrice()
    return total < MONEY

def proc(buyCells, lastCell, topCells, cells):
    f = lambda : calc(buyCells)
    for c in buyCells: c.act()
    ok = not learn(f, lastCell, buyCells)
    for c in cells:
        c.clear()
#    print("is ok?", ok)
    return ok

def main():
    cellA = LastCell("A", 6)
    cellB = TopCell("B", 1, cellA, 310)
    cellC = TopCell("C", 3, cellA, 220)
    cellD = TopCell("D", 8, cellA, 70)

    cells = [cellA, cellB, cellC, cellD]
    tops = [cellB, cellC, cellD]
    last = cellA
    f = lambda buys: proc(buys, last, tops, cells)

    while True:
        perfect = True
        print("[pat 1 : all buy]")
        perfect &= f([cellB, cellC, cellD])
        print("[pat 2 : buy B, C]")
        perfect &= f([cellB, cellC])
        print("[pat 3 : buy B, D]")
        perfect &= f([cellB, cellD])
        print("[pat 4 : buy C, D]")
        perfect &= f([cellC, cellD])
        print("[pat 5 : buy B]")
        perfect &= f([cellB])
        print("------------------------------")
        if perfect: break

    f = lambda buys: proc(buys, cellA, tops, cells)
    print("[pat 6 : buy C]")
    f([cellC])
    print("[pat 7 : buy D]")
    f([cellD])
    print("[pat 8 : no buy]")
    f([])


    # result print
    for c in cells:
        c.pp()
main()
