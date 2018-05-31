import sys
from time import sleep

from sense_hat import SenseHat


colors = {
            'blank':   (0,   0,   0),
            'white':   (255, 255, 255),
            'red':     (255, 0,   0),
            'green':   (0,   255, 0),
            'blue':    (0,   0,   255),
            'yellow':  (255, 255, 0),
            'pink':    (255, 105, 180)
        }

s = SenseHat()
s.low_light = True


class Tile:
    def __init__(self, nb):
        x = (nb % 3) * 3
        y = (nb // 3) * 3
        self.coords = {(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)}

    def draw(self, color):
        for x, y in self.coords:
            s.set_pixel(x, y, color)


class Grid():
    def __init__(self, color):
        self.color = color

    def draw(self):
        X = self.color
        O = colors['blank']
        grid = [
            O, O, X, O, O, X, O, O,
            O, O, X, O, O, X, O, O,
            X, X, X, X, X, X, X, X,
            O, O, X, O, O, X, O, O,
            O, O, X, O, O, X, O, O,
            X, X, X, X, X, X, X, X,
            O, O, X, O, O, X, O, O,
            O, O, X, O, O, X, O, O,
        ]
        set_pixels(grid)

class Player:
    def __init__(self, color):
        self.color = color
        self.tiles = set()

    def draw(self):
        for tile in self.tiles:
            tile.draw(self.color)

    def add_tile(self, tile):
        self.tiles.add(tile)


class Game:
    def __init__(self, tile_color, selection_color):
        self.grid = Grid(colors['white'])
        self.tile_color = tile_color
        self.selection_color = selection_color
        self.tiles = [Tile(i) for i in range(9)]
        self.selection = tiles[4]
        self.players = (Player(colors['blue']), Player(colors['red']))
        
    def start(self):
        self.grid.draw()
        self.selection.draw()




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
