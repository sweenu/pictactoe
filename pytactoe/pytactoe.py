from sense_hat import SenseHat


SCROLL_SPEED = 0.1
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
        self.nb = nb

    @property
    def coords(self):
        x = (self.nb % 3) * 3
        y = (self.nb // 3) * 3
        return {(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)}

    @staticmethod
    def _draw(coords, color):
        for x, y in coords:
            s.set_pixel(x, y, color)

    def draw(self, color):
        self._draw(self.coords, color)


class Cursor(Tile):
    def __init__(self, color):
        self.color = color

    def draw(self):
        self._draw(self.coords, self.color)

    def place(self, nb):
        self.nb = nb

    def move(self, direction):
        if direction == 'up':
            nb = self.nb - 3
            if not nb < 0:
                self.nb = nb
        elif direction == 'down':
            nb = self.nb + 3
            if not nb > 8:
                self.nb = nb
        elif direction == 'left':
            nb = self.nb - 1
            if nb not in {-1, 2, 5}:
                self.nb = nb
        elif direction == 'right':
            nb = self.nb + 1
            if nb not in {3, 6, 9}:
                self.nb = nb
            

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
        s.set_pixels(grid)


class Player:
    def __init__(self, color):
        self.color = color
        self.tiles = set()

    def draw(self):
        for tile in self.tiles:
            tile.draw(self.color)

    def add_tile(self, tile):
        self.tiles.add(tile)

    def has_win(self):
        tile_numbers = {tile.nb for tile in self.tiles}
        win_combinations = [{0, 3, 6}, {1, 4, 7}, {2, 5, 8}, # lines
                            {0, 1, 2}, {3, 4 ,5}, {6, 7 ,8}, # columns
                            {0, 4, 8}, {2, 4, 6}] # diagonales
        return any(combi.issubset(tile_numbers) for combi in win_combinations)


class Game:
    def __init__(self, cursor_color):
        self.grid = Grid(colors['white'])
        self.cursor = Cursor(cursor_color)
        self.tiles = [Tile(i) for i in range(9)]
        self.players = (Player(colors['blue']), Player(colors['red']))

    @property
    def used_tiles(self):
        return self.players[0].tiles.union(self.players[1].tiles)

    def _refresh(self):
        for player in self.players:
            player.draw()

        for unused_tile in set(self.tiles).difference(self.used_tiles):
            unused_tile.draw(colors['blank'])

        self.cursor.draw()

    def start(self):
        s.show_message(
            "Welcome to pytactoe !!",
            text_colour=colors['white'],
            scroll_speed=SCROLL_SPEED,
        )
        self.grid.draw()
        self.cursor.place(4)
        self.cursor.draw()

        turn = 0
        while turn < 9:
            player = self.players[turn % 2]

            played = False
            while not played:
                event = s.stick.wait_for_event()
                if event.action == 'pressed':
                    if not event.direction == 'middle':
                        self.cursor.move(event.direction)
                        self._refresh()
                        self.cursor.draw()
                    else:
                        if not self.cursor.nb in self.used_tiles:
                            player.add_tile(self.tiles[self.cursor.nb])
                            self.cursor.place(4)
                            self._refresh()
                            played = True

            if turn > 2:
                if player.has_win():
                    s.show_message("You win!",
                                   text_colour=player.color,
                                   scroll_speed=SCROLL_SPEED)
                    return

            turn += 1

        s.show_message("Draw!",
                       text_colour=colors['white'],
                       scroll_speed=SCROLL_SPEED)
