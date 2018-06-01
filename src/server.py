import socket

from core import Game


game = Game(1)

HOST = ''
PORT = 47878
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)

    conn, _ = s.accept()
    with conn:
        while True:
            game.wait_for_play(conn)            
            if game.turn < 9:
                game.play(s)
            else:
                game.draw_msg()
                break
