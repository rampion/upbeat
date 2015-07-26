#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
from slackclient import SlackClient
import time
import json
import requests
import sys
import random

# global vars (shame on me)
crontable = []
outputs = []
PEOPLE = []
GAME = None

# settings
CONFIGFILE = 'gameconfig.json'
CONFIG = {}

class Person(object):
    pass


class RpgGame(object):
    RPG_URL = 'http://...../gamedata.json'
    TEXT_URL = 'http://...../gametext.json'
    ERROR_LOADING_ERRORS = '[[ Unrecoverable error trying to load language files. Aborting. ]]'
    ERROR_UNKNOWN_COMMAND = 'I do not understand what you want to do.'
    ERROR_UNDEFINED_STRING = '[[ A message goes here but it is not defined for your language. ]]'

    class Character(object):
        pass

    class CharacterClass(object):
        pass

    class CharacterRace(object):
        pass 

    class CharacterSpell(object):
        pass 

    class CharacterState(object):
        pass 

    class Encounter(object):
        pass


    def __init__(self, language='en'):
        self.disabled = False
        self.lang = language
        self.characters = []
        self.classes = []
        self.spells = []
        self.states = []
        self.texts = {}
        self.public_message_queue = []
        self.load_text()
        self.load_data()

    def load_text(self):
        r = requests.get(RpgGame.TEXT_URL)
        if r.status_code == requests.codes.ok:
            texts = r.json()
            for text in texts:
                self.texts[text] = texts[text]
        else:
            self.public_message_queue.append(RpgGame.ERROR_LOADING_ERRORS)
            self.disabled = True

    def load_data(self):
        if self.disabled:
            return
        r = requests.get(RpgGame.RPG_URL)
        if r.status_code == requests.codes.ok:
            game_data = r.json()
            for charclass in game_data['classes']:
                cc = RpgGame.CharacterClass(name=charclass['name'])
                cc.name_cap = charclass['name_cap']
                cc.name_pl = charclass['name_pl']
                self.classes.append(cc)
            for charspell in game_data['spells']:
                cs = RpgGame.CharacterSpell(name=charspell['name'])
                self.spells.append(cs)
            for charstate in game_data['states']:
                state = RpgGame.CharacterState(name=charstate['name'])
                self.states.append(state)
            for charrace in game_data['races']:
                cr = RpgGame.CharacterRace(name=charrace['name'])
                cr.name_cap = charrace['name_cap']
                cr.name_pl = charrace['name_pl']
                self.races.append(cr)
        else:
            self.public_message_queue.append(self.get_text('error-data'))
            self.disabled = True


def dprint(message):
    if not CONFIG['DEBUG']:
        return
    print(message)


def process_message(data):
    # dprint(data)
    if data['user'] in CONFIG['IGNORELIST']:
        # dprint('Speaker is on ignore list!')
        return
    name = id_to_name(data['user'])
    if name is None:
        reload_people()
        name = id_to_name(data['user'])
        if name is None:
            return
    command = data['text']
    if data['channel'].startswith('D'):
        # direct message received, respond to same channel
        message = GAME.pvt_command(name, command)
        outputs.append([data['channel'], message])
        return
    if not data['channel'] == CONFIG['RPGCHANNEL']:
        # dprint('Ignoring non-RPG public channel')
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
    # dprint('Config loaded...')
    # for item in CONFIG:
    #     dprint('%s: %s' % (item, CONFIG[item]))


def start_game():
    global GAME
    load_config()
    GAME = RpgGame()
    crontable.append([2, 'process_game'])
    dprint('rpgbot loaded')


start_game()
