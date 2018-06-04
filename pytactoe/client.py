import socket

from .core import Game


def connect(host, port=47878):
    game = Game(1)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        
        while True:
            if game.turn < 9:
                game.play(s)
                game.wait_for_play(s)
            else:
                game.draw_msg()
                break
