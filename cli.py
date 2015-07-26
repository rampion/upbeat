#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
from rpg.game import RpgGame
import sys
import select
import time


PLAYER = 'me'
GAME = None


def no_input():
    messages = GAME.run()
    for m in messages:
        print(m)


def handle_input(typed_command):
    message = GAME.pub_command(PLAYER, typed_command)
    print(message)


def run_game():
    while True:
        while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            command = sys.stdin.readline()
            if command:
                handle_input(command)
            else:
                print('quitting')
                exit(0)
        else:
            no_input()
        time.sleep(0.5)


def do_setup():
    global GAME
    GAME = RpgGame()
    print('^D to quit. Type stuff:')


if __name__ == '__main__':
    do_setup()
    run_game()

