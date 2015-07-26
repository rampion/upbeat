#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
import requests
import random


class RpgGame(object):
    RPG_URL = 'http://upbeat.projectmayhem.org:21218/data/gamedata.json'
    TEXT_URL = 'http://upbeat.projectmayhem.org:21218/data/gametext.json'
    ERROR_LOADING_ERRORS = '[[ Unrecoverable error trying to load language files. Aborting. ]]'
    ERROR_UNKNOWN_COMMAND = 'I do not understand what you want to do.'
    ERROR_UNDEFINED_STRING = '[[ A message goes here but it is not defined for your language. ]]'

    class Character(object):
        def __init__(self, owner=None):
            self.name = self.random_name()
            self.hp_curr = 0
            self.hp_max = 0
            self.mood = 0
            self.owner = owner
            self.cc = None
            self.cr = None

        def __str__(self):
            return self.name

        @staticmethod
        def random_name():
            names = [
                'Fred',
                'Maria',
                'Cornelius',
                'Janice'
            ]
            return names[random.randint(0, len(names)-1)]

        def is_friendly(self):
            if self.owner is not None:
                return True
            if self.angry:
                return False

        def fullinfo(self):
            response = 'You control the following character:\n'
            response += '*Name:* ' + self.name + '\n'
            response += '*Race:* ' + self.get_race() + '\n'
            response += '*Class:* ' + self.get_class() + '\n'
            return response

        def get_class(self):
            if self.cc is not None:
                return self.cc.name
            else:
                return 'unknown-class'

        def get_race(self):
            if self.cr is not None:
                return self.cr.name
            else:
                return 'unknown-race'

        def get_mood(self):
            if self.owner is not None:
                return 3
            return self.mood

        def get_owner(self):
            if self.owner is None:
                return 'NPC'
            return self.owner

        def welcome(self):
            response = 'A %s %s approaches and joins the party.' % (self.get_race(), self.get_class())
            return response

        def depart(self):
            response = '%s departs the party.' % self.name
            return response

        def reset(self):
            pass

    class CharacterClass(object):
        def __init__(self, name):
            self.name = name
            self.name_cap = name
            self.name_pl = name + 's'
            self.valid_player = True
            self.valid_npc = True

    class CharacterRace(object):
        def __init__(self, name):
            self.name = name
            self.name_cap = name
            self.name_pl = name + 's'
            self.valid_player = True
            self.valid_npc = True

    class CharacterSpell(object):
        def __init__(self, name=''):
            self.name = name
            self.is_hidden = False

        def is_castable(self, caster, target):
            return True

    class CharacterState(object):
        def __init__(self, name=''):
            self.name = name

    class Encounter(object):
        TIMES = [
            'late afternoon on a Thursday',
            'the middle of the night',
            'the morning after the peace accord was signed',
            'a sunny day with a light breeze',
            'a crisp winter morning',
            'the rainiest day you have ever seen',
            'a scorching summer day',
            'sunset on the equinox',
            'just after band practice',
            'the last day of harvest festival',
        ]
        PLACES = [
            'following a shortcut through a dark swamp',
            'the abandoned castle',
            'at a crowded inn',
            ''
        ]

        def __init__(self):
            # self.when = Encounter.TIMES[random.randint(0,len(Encounter.TIMES)-1)]
            # self.where = Encounter.PLACES[random.randint(0,len(Encounter.PLACES)-1)]
            self.fighting = False
            self.participants = []

        def num_monsters_alive(self):
            alive = 0
            for character in self.participants:
                if character.is_friendly():
                    continue
                if character.hp_curr <= 0:
                    alive += 1
            return alive

    def __init__(self, language='en'):
        self.disabled = False
        self.lang = language
        self.characters = []
        self.classes = []
        self.races = []
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

    def get_text(self, message):
        return self.texts.get(message, RpgGame.ERROR_UNDEFINED_STRING)

    def is_playing(self, player):
        for c in self.characters:
            if c.owner == player:
                return True
        return False

    # NPC commands

    def run(self):
        if self.disabled:
            return
        # if bot can take any actions, take them
        messages = []
        for m in self.public_message_queue:
            messages.append(m)
        self.public_message_queue = []
        return messages

    # LIST things

    def list_spells(self):
        if len(self.spells) == 0:
            return 'No spells known'
        spell_list = ''
        for s in self.spells:
            if not s.is_hidden:
                spell_list += s.name + '\n'
        return spell_list

    def list_races(self):
        if len(self.races) == 0:
            return 'No races known'
        race_list = ''
        for r in self.races:
            if r.valid_player:
                race_list += r.name_cap + '\n'
        return race_list

    def list_classes(self):
        if len(self.classes) == 0:
            return 'No classes known'
        class_list = ''
        for c in self.classes:
            if c.valid_player:
                class_list += c.name_cap + '\n'
        return class_list

    def list_characters(self):
        if len(self.characters) == 0:
            return 'No characters present'
        char_list = ''
        for c in self.characters:
            char_list += '*%s* (%s %s) [%s]' % (c.name, c.get_race(), c.get_class(), c.get_owner())
        return char_list

    # PLAYER commands

    def player_info(self, player):
        for c in self.characters:
            if c.owner == player:
                return c.fullinfo()
        return self.get_text('not-playing')

    def add_player(self, player):
        if self.is_playing(player):
            return self.get_text('already-playing')
        c = RpgGame.Character(owner=player)
        c.cc = self.classes[random.randint(0, len(self.classes)-1)]
        c.reset()
        self.characters.append(c)
        return c.welcome()

    def remove_player(self, player):
        if not self.is_playing(player):
            return self.get_text('not-playing')
        for c in self.characters:
            if c.owner == player:
                self.characters.remove(c)
                return c.depart()

    def player_action(self, player, action):
        return '%s tried an action.' % player

    # input/output

    def pub_command(self, player, command):
        if self.disabled:
            return
        if not command.startswith('!'):
            return
        action = command.lower().split()
        if action[0] == '!join':
            return self.add_player(player)
        if action[0] == '!quit':
            return self.remove_player(player)
        if action[0] in ['!attack', '!cast', '!heal']:
            return self.player_action(player, command)
        if action[0] == '!list':
            try:
                things = action[1]
                if things == 'spells':
                    return self.list_spells()
                elif things == 'classes':
                    return self.list_classes()
                elif things == 'races':
                    return self.list_races()
                elif things == 'characters':
                    return self.list_characters()
                else:
                    return '[[ I do not know any of those. ]]'
            except KeyError:
                return '[[ List needs another parameter. ]]'
        return self.get_text('text_help_short')

    def pvt_command(self, player, command):
        if self.disabled:
            return
        action = command.lower().split()
        if action[0] == 'help':
            return self.get_text('text_help')
        if action[0] == 'status':
            return self.player_info(player)
        return self.get_text('unknown')


def run_rpg_tests():
    pass

if __name__ == '__main__':
    run_rpg_tests()

