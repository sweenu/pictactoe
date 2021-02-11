import socket

from .core import Game


def connect(host, port=47878):
    game = Game()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        while True:
            if game.turn < 9:
                if game.play(s):
                    break
            if game.turn < 9:
                if game.wait_for_play(s):
                    break
            else:
                game.draw_msg()
                break
