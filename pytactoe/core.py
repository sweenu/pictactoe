import platform

if platform.machine() == 'x86_64':
    from sense_emu import SenseHat
else:
    from sense_hat import SenseHat


SCROLL_SPEED = 0.04
colors = {
            'blank':   (0,   0,   0),
            'white':   (255, 255, 255),
            'red':     (255, 0,   0),
            'green':   (0,   255, 0),
            'blue':    (0,   0,   255),
            'yellow':  (255, 255, 0),
            'pink':    (255, 105, 180)
        }


class Tile:
    @property
    def coords(self):
        x = (self.nb % 3) * 3
        y = (self.nb // 3) * 3
        return {(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)}


class GameTile(Tile):
    def __init__(self, nb):
        self.nb = nb
        self.color = colors['blank']


class Cursor(Tile):
    def __init__(self, color):
        self.color = color

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
        X = self.color
        O = colors['blank']
        self._grid = [
            O, O, X, O, O, X, O, O,
            O, O, X, O, O, X, O, O,
            X, X, X, X, X, X, X, X,
            O, O, X, O, O, X, O, O,
            O, O, X, O, O, X, O, O,
            X, X, X, X, X, X, X, X,
            O, O, X, O, O, X, O, O,
            O, O, X, O, O, X, O, O,
        ]

    def __iter__(self):
        for led in self._grid:
            yield led

    def __len__(self):
        return len(self._grid)


class Player:
    def __init__(self, color):
        self.color = color
        self.tiles = set()

    def _add_tile(self, tile):
        self.tiles.add(tile)

    def play(self, tile):
        tile.color = self.color
        self._add_tile(tile)

    def has_win(self):
        tile_numbers = {tile.nb for tile in self.tiles}
        win_combinations = [{0, 3, 6}, {1, 4, 7}, {2, 5, 8},  # rows
                            {0, 1, 2}, {3, 4, 5}, {6, 7, 8},  # columns
                            {0, 4, 8}, {2, 4, 6}]  # diagonales
        return any(combi.issubset(tile_numbers) for combi in win_combinations)


class Game:
    def __init__(self, player_nb):
        self.sense = SenseHat()
        self.sense.low_light = True

        self.intro_msg()

        self.grid = Grid(colors['white'])
        self.sense.set_pixels(self.grid)

        self.cursor = Cursor(colors['pink'])
        self.tiles = [GameTile(i) for i in range(9)]

        self.player_nb = player_nb

        self.players = [Player(colors['blue']), Player(colors['red'])]

    @property
    def current_player(self):
        nb = self.turn % 2
        return self.players[nb]

    @property
    def other_player(self):
        nb = self.turn % 2
        return self.players[nb^1]

    @property
    def turn(self):
        nb_used_tiles = len(self.players[0].tiles) + len(self.players[1].tiles)
        return nb_used_tiles

    def refresh(self):
        for tile in self.tiles:
            self._draw_tile(tile)

    def _draw_tile(self, tile):
        for led in tile.coords:
            self.sense.set_pixel(led[0], led[1], tile.color)

    def play(self, socket):
        self.cursor.place(4)
        self._draw_tile(self.cursor)
        while True:
            event = self.sense.stick.wait_for_event()
            if event.action == 'pressed':
                if not event.direction == 'middle':
                    self.cursor.move(event.direction)
                    self.refresh()
                    self._draw_tile(self.cursor)
                else:
                    selected_tile = self.tiles[self.cursor.nb]
                    if selected_tile.color == colors['blank']:
                        self.current_player.play(selected_tile) # the turn is incremented here
                        if self.turn > 3:
                            if self.other_player.has_win():
                                socket.sendall(bytes([9]))
                                self.win_msg()
                                return True

                        socket.sendall(bytes([self.cursor.nb]))
                        self.refresh()
                        return False

    def wait_for_play(self, socket):
        while True:
            data = socket.recv(1024)
            if data:
                tile_nb = int.from_bytes(data, 'little')
                if tile_nb == 9:
                    self.loose_msg()
                    return True
                else:
                    self.current_player.play(self.tiles[tile_nb])
                    self.refresh()
                    return False

    def intro_msg(self):
        self.sense.show_message(
                "Welcome to pytactoe!!",
                text_colour=colors['white'],
                scroll_speed=SCROLL_SPEED,
            )

    def draw_msg(self):
        self.sense.show_message(
                "Draw!",
                 text_colour=colors['white'],
                 scroll_speed=SCROLL_SPEED
            )

    def win_msg(self):
        self.sense.show_message(
                "You win!",
                 text_colour=colors['white'],
                 scroll_speed=SCROLL_SPEED
            )

    def loose_msg(self):
        self.sense.show_message(
                "You loose!",
                 text_colour=colors['white'],
                 scroll_speed=SCROLL_SPEED
            )
