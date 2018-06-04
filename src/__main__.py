#!/usr/bin/env python
import os
import sys
from argparse import ArgumentParser

import server


def main():
    parser = ArgumentParser(description=("Tic-Tac-Toe for RaspberryPi's sense HAT, "
                                         "playable on LAN"))
    parser.add_argument('-c', '--connect',
                        help="the host's ip address")
    parser.add_argument('-H', '--host',
                        help="start a server and wait for a player to connect")
    args = parser.parse_args()

    if args.host:
        if args.connect:
            print('Cannot both host and connect to another host')
            sys.exit(1)
        if os.fork() == 0:
            Game().start()
        else:
            server.serve()        
    else:
        if args.connect:
            Game(host=args.connect)
        Game().start()


if __name__ == '__main__':
    main()
