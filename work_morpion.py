from sense_hat import *
from time import *
import sys


s = SenseHat()
s.low_light = True

green = (0, 255, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
white = (255, 255, 255)
nothing = (0, 0, 0)
pink = (255, 105, 180)


def drawGrid():
    W = white
    O = nothing
    grid = [
        O, O, W, O, O, W, O, O,
        O, O, W, O, O, W, O, O,
        W, W, W, W, W, W, W, W,
        O, O, W, O, O, W, O, O,
        O, O, W, O, O, W, O, O,
        W, W, W, W, W, W, W, W,
        O, O, W, O, O, W, O, O,
        O, O, W, O, O, W, O, O,
    ]
    return grid


def Wsquare(posx, posy):
    x = posx
    y = posy
    s.set_pixel(x, y, (255, 255, 255))
    s.set_pixel(x + 1, y, (255, 255, 255))
    s.set_pixel(x + 1, y + 1, (255, 255, 255))
    s.set_pixel(x, y + 1, (255, 255, 255))


def Bsquare(posx, posy):
    x = posx
    y = posy
    s.set_pixel(x, y, (0, 0, 255))
    s.set_pixel(x + 1, y, (0, 0, 255))
    s.set_pixel(x + 1, y + 1, (0, 0, 255))
    s.set_pixel(x, y + 1, (0, 0, 255))


def Rsquare(posx, posy):
    x = posx
    y = posy
    s.set_pixel(x, y, (255, 0, 0))
    s.set_pixel(x + 1, y, (255, 0, 0))
    s.set_pixel(x + 1, y + 1, (255, 0, 0))
    s.set_pixel(x, y + 1, (255, 0, 0))


def EmptySquare(posx, posy):
    x = posx
    y = posy
    s.set_pixel(x, y, (0, 0, 0))
    s.set_pixel(x + 1, y, (0, 0, 0))
    s.set_pixel(x + 1, y + 1, (0, 0, 0))
    s.set_pixel(x, y + 1, (0, 0, 0))


def Ysquare(posx, posy):
    x = posx
    y = posy
    s.set_pixel(x, y, (255, 255, 0))
    s.set_pixel(x + 1, y, (255, 255, 0))
    s.set_pixel(x + 1, y + 1, (255, 255, 0))
    s.set_pixel(x, y + 1, (255, 255, 0))


def ErrorCell(posx, posy):
    x = posx
    y = posy
    Ysquare(x, y)
    sleep(.1)
    Wsquare(x, y)
    sleep(.1)
    Ysquare(x, y)
    sleep(.1)
    Wsquare(x, y)
    sleep(.1)
    Ysquare(x, y)
    sleep(.1)
    Wsquare(x, y)


def has_win(player):
    w = s.get_pixels()

    if player == 2:
        # lignes
        for x in [0, 24, 48]:
            if w[x] == w[x + 3] == w[x + 6] != [0, 0, 0]:
                s.show_message(
                    "Player 2 win", text_colour=[255, 0, 0], scroll_speed=0.1
                )
                return True
        # colonnes
        for x in [0, 3, 6]:
            if w[x] == w[x + 24] == w[x + 48] != [0, 0, 0]:
                s.show_message(
                    "Player 2 win", text_colour=[255, 0, 0], scroll_speed=0.1
                )
                return True
        # diagonales
        if w[0] == w[27] == w[54] != [0, 0, 0] or w[6] == w[27] == w[48] != [0, 0, 0]:
            s.show_message("Player 2 win", text_colour=[255, 0, 0], scroll_speed=0.1)
            return True

    if player == 1:
        # lignes
        for y in [0, 24, 48]:
            if w[y] == w[y + 3] == w[y + 6] != [0, 0, 0]:
                s.show_message(
                    "Player 1 win", text_colour=[0, 0, 255], scroll_speed=0.1
                )
                return True
        # colonnes
        for y in [0, 3, 6]:
            if w[y] == w[y + 24] == w[y + 48] != [0, 0, 0]:
                s.show_message(
                    "Player 1 win", text_colour=[0, 0, 255], scroll_speed=0.1
                )
                return True
        # diagonales
        if w[0] == w[27] == w[54] != [0, 0, 0] or w[6] == w[27] == w[48] != [0, 0, 0]:
            s.show_message("Player 1 win", text_colour=[0, 0, 255], scroll_speed=0.1)
            return True


def begin():
    s.show_message(
        "Welcome to pytictactoe !!",
        text_colour=white,
        back_colour=pink,
        scroll_speed=0.1,
    )
    s.stick.wait_for_event()


def play():
    id = 1
    x, y = 3, 3
    Wsquare(x, y)
    pc = []
    pc2 = []
    tour = 1

    while tour <= 9:
        for event in s.stick.get_events():
            if event.direction == "up" and event.action == "pressed":
                if y == 0:
                    pass
                else:
                    if pc.count([x, y]) == 1:
                        Bsquare(x, y)
                        y = y - 3
                        Wsquare(x, y)
                    elif pc2.count([x, y]) == 1:
                        Rsquare(x, y)
                        y = y - 3
                        Wsquare(x, y)
                    else:
                        EmptySquare(x, y)
                        y = y - 3
                        Wsquare(x, y)

            if event.direction == "down" and event.action == "pressed":
                if y == 6:
                    pass
                else:
                    if pc.count([x, y]) == 1:
                        Bsquare(x, y)
                        y = y + 3
                        Wsquare(x, y)
                    elif pc2.count([x, y]) == 1:
                        Rsquare(x, y)
                        y = y + 3
                        Wsquare(x, y)
                    else:
                        EmptySquare(x, y)
                        y = y + 3
                        Wsquare(x, y)

            if event.direction == "left" and event.action == "pressed":
                if x == 0:
                    pass
                else:
                    if pc.count([x, y]) == 1:
                        Bsquare(x, y)
                        x = x - 3
                        Wsquare(x, y)
                    elif pc2.count([x, y]) == 1:
                        Rsquare(x, y)
                        x = x - 3
                        Wsquare(x, y)
                    else:
                        EmptySquare(x, y)
                        x = x - 3
                        Wsquare(x, y)

            if event.direction == "right" and event.action == "pressed":
                if x == 6:
                    pass
                else:
                    if pc.count([x, y]) == 1:
                        Bsquare(x, y)
                        x = x + 3
                        Wsquare(x, y)
                    elif pc2.count([x, y]) == 1:
                        Rsquare(x, y)
                        x = x + 3
                        Wsquare(x, y)
                    else:
                        EmptySquare(x, y)
                        x = x + 3
                        Wsquare(x, y)

            if event.direction == "middle" and event.action == "pressed":
                if pc.count([x, y]) == 1 or pc2.count([x, y]) == 1:
                    ErrorCell(x, y)
                else:
                    if x == 3 and y == 3:
                        if id == 1:
                            Bsquare(x, y)
                            pc.append([x, y])
                            tour = tour + 1
                        if id == 2:
                            Rsquare(x, y)
                            pc2.append([x, y])
                            tour = tour + 1
                    else:
                        if id == 1:
                            Bsquare(x, y)
                            pc.append([x, y])
                            if has_win(id):
                                sys.exit()
                            tour = tour + 1
                            x, y = 3, 3
                            Wsquare(x, y)
                        if id == 2:
                            Rsquare(x, y)
                            pc2.append([x, y])
                            if has_win(id):
                                sys.exit()
                            tour = tour + 1
                            x, y = 3, 3
                            Wsquare(x, y)
                    if id == 1:
                        id = 2
                    elif id == 2:
                        id = 1

    s.show_message("Draw game", text_colour=[255, 255, 0], scroll_speed=0.1)


begin()
s.set_pixels(drawGrid())
play()
