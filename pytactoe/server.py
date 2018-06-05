import socket

from .core import Game


def serve(host='', port=47878):
    game = Game(0)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)

        conn, _ = s.accept()
        with conn:
            while True:
                if game.turn < 9:
                    if game.wait_for_play(conn):
                        break
                if game.turn < 9:
                    if game.play(conn):
                        break
                else:
                    game.draw_msg()
                    break
