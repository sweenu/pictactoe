import socket

from core import Game


game = Game(0)

HOST = 'localhost'
PORT = 47878
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    while True:
        if game.turn < 9:
            game.play(s)
            game.wait_for_play(s)
        else:
            game.draw_msg()
            break
