#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
from slackclient import SlackClient
from rpg.game import RpgGame
import json
import sys


# global vars (shame on me)
crontable = []
outputs = []
PEOPLE = []
GAME = None

# settings
CONFIGFILE = 'gameconfig.json'
CONFIG = {}


class Person(object):
    def __init__(self, uid=None, name=None):
        self.uid = uid
        self.name = name


def dprint(message):
    if not CONFIG['DEBUG']:
        return
    print(message)


def process_message(data):
    if data['user'] in CONFIG['IGNORELIST']:
        return
    name = id_to_name(data['user'])
    if name is None:
        reload_people()
        name = id_to_name(data['user'])
        if name is None:
            return
    command = data['text']
    if data['channel'].startswith('D'):
        message = GAME.pvt_command(name, command)
        outputs.append([data['channel'], message])
        return
    if not data['channel'] == CONFIG['RPGCHANNEL']:
        return
    message = GAME.pub_command(name, command)
    outputs.append([data['channel'], message])


def reload_people():
    global PEOPLE
    PEOPLE = []
    client = SlackClient(CONFIG['SLACK_KEY'])
    user_json = client.api_call('users.list')
    users = json.loads(user_json)
    if users['ok']:
        for u in users['members']:
            if u['deleted']:
                continue
            uid = u['id']
            name = u['name']
            p = Person(uid=uid, name=name)
            PEOPLE.append(p)
    else:
        dprint('Error loading users.')


def id_to_name(uid):
    for p in PEOPLE:
        if p.uid == uid:
            return p.name
    return None


def process_game():
    messages = GAME.run()
    for m in messages:
        outputs.append([CONFIG['RPGCHANNEL'], m])


def load_config():
    global CONFIG
    try:
        with open(CONFIGFILE, 'r') as conf_fh:
            CONFIG = json.load(conf_fh)
    except IOError:
        print('Error loading config file. Make sure it exists and is readable.')
        sys.exit(1)


def start_game():
    global GAME
    load_config()
    GAME = RpgGame()
    crontable.append([2, 'process_game'])
    dprint('rpgbot loaded')


start_game()

