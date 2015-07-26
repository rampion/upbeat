#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
import requests
import random
import time

DEBUG = True


def dprint(debug_message):
    if DEBUG:
        print(debug_message)


class RpgGameDB(object):
    URL_GAMEDATA = 'http://upbeat.projectmayhem.org:21218/data/gamedata.json'
    URL_GAMETEXT = 'http://upbeat.projectmayhem.org:21218/data/gametext.json'
    URL_ENCOUNTERS = 'http://upbeat.projectmayhem.org:21218/data/encounters.json'
    ERROR_LOADING_ERRORS = '[[ Unrecoverable error trying to load language files. Aborting. ]]'
    ERROR_UNKNOWN_COMMAND = 'I do not understand what you want to do.'
    ERROR_UNDEFINED_STRING = '[[ A message goes here but it is not defined for your language. ]]'

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

        # def is_castable(self, caster, target):
        #     return True

    class CharacterState(object):
        def __init__(self, name=''):
            self.name = name

    class GameEncounter(object):
        def __init__(self, name):
            self.name = name
            self.triggers = []

        def add_trigger(self, trigger):
            self.triggers.append(trigger)

    # class GameEncounterTrigger(object):
    #     def __init__(self):
    #         self.

    def __init__(self):
        self.error = False
        self.classes = []
        self.races = []
        self.spells = []
        self.states = []
        self.encounters = []
        self.texts = {}
        self.load_text()
        self.load_data()
        self.load_encounters()

    def load_text(self):
        r = requests.get(RpgGameDB.URL_GAMETEXT)
        if r.status_code == requests.codes.ok:
            texts = r.json()
            for text in texts:
                self.texts[text] = texts[text]
                dprint('Loaded text %s' % text)
        else:
            dprint('Error loading text')
            self.error = True

    def load_data(self):
        r = requests.get(RpgGameDB.URL_GAMEDATA)
        if r.status_code == requests.codes.ok:
            game_data = r.json()
            for charclass in game_data['classes']:
                cc = RpgGameDB.CharacterClass(name=charclass['name'])
                cc.name_cap = charclass['name_cap']
                cc.name_pl = charclass['name_pl']
                dprint('Loaded class %s' % cc.name_cap)
                self.classes.append(cc)
            for charspell in game_data['spells']:
                cs = RpgGameDB.CharacterSpell(name=charspell['name'])
                dprint('Loaded spell %s' % cs.name)
                self.spells.append(cs)
            for charstate in game_data['states']:
                state = RpgGameDB.CharacterState(name=charstate['name'])
                dprint('Loaded state %s' % state.name)
                self.states.append(state)
            for charrace in game_data['races']:
                cr = RpgGameDB.CharacterRace(name=charrace['name'])
                cr.name_cap = charrace['name_cap']
                cr.name_pl = charrace['name_pl']
                dprint('Loaded race %s' % cr.name_cap)
                self.races.append(cr)
        else:
            dprint('Error loading data')
            self.error = True

    def load_encounters(self):
        r = requests.get(RpgGameDB.URL_ENCOUNTERS)
        if r.status_code == requests.codes.ok:
            for encounter in r.json():
                e = RpgGameDB.GameEncounter(name=encounter['name'])
                for t in encounter['triggers']:
                    e.add_trigger(t)
                for x in range(0, encounter['weight']):
                    self.encounters.append(e)
                dprint('Loaded encounter %s' % e.name)
        else:
            dprint('Error loading encounters')
            self.error = True

    def get_text(self, message):
        return self.texts.get(message, RpgGameDB.ERROR_UNDEFINED_STRING)

    @property
    def max_class(self):
        return len(self.classes)-1

    @property
    def max_race(self):
        return len(self.races)-1

    @property
    def max_encounter(self):
        return len(self.encounters)-1

    @property
    def max_spell(self):
        return len(self.spells)-1

    def list_spells(self, newline=True):
        response = ''
        for s in self.spells:
            if not s.is_hidden:
                response += s.name
                if newline:
                    response += '\n'
        return response

    def list_classes(self, newline=True):
        response = ''
        for c in self.classes:
            response += c.name_cap
            if newline:
                response += '\n'
        return response

    def list_races(self, newline=True):
        response = ''
        for r in self.races:
            response += r.name_cap
            if newline:
                response += '\n'
        return response

    def list_states(self, newline=True):
        response = ''
        for s in self.states:
            response += s.name
            if newline:
                response += '\n'
        return response



class RpgGame(object):
    ENCOUNTER_CHANCE = 50       # chance of a random encounter happening
    ENCOUNTER_COOLDOWN = 300    # minimum seconds between encounters

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

        # def is_friendly(self):
        #     if self.owner is not None:
        #         return True
        #     if self.angry:
        #         return False

        def fullinfo(self):
            response = 'You control the following character:\n'
            response += '*Name:* ' + self.name + '\n'
            response += '*Race:* ' + self.get_race() + '\n'
            response += '*Class:* ' + self.get_class() + '\n'
            return response

        def summary(self):
            response = '*%s* - %s %s (%d/%d) [%s]' % (self.name, self.get_race(), self.get_class(), self.hp_curr, self.hp_max, self.owner)
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

    def __init__(self, language='en'):
        self.public_message_queue = []
        self.encounter_timestamp = 0
        self.disabled = False
        self.combat = False
        self.lang = language
        self.characters = []
        self.db = RpgGameDB()
        if self.db.error:
            self.disabled = True
            self.public_message_queue.append(self.db.get_text('error-data'))

    def is_playing(self, player):
        for c in self.characters:
            if c.owner == player:
                return True
        return False

    # NPC commands

    def run(self):
        messages = []
        if self.disabled:
            return messages
        # if bot can take any actions, take them
        for m in self.public_message_queue:
            messages.append(m)
        self.public_message_queue = []
        return messages

    def start_encounter(self):
        e = self.db.encounters[random.randint(0, self.db.max_encounter)]
        assert isinstance(e, RpgGameDB.GameEncounter)
        for trigger in e.triggers:
            print(trigger)  # DELETE ME

    def finish_encounter(self):
        self.combat = False
        self.encounter_timestamp = time.time()
        # do looting here

    def trigger_encounter(self):
        if self.disabled:
            return False
        if self.combat:
            return False
        if self.encounter_timestamp + RpgGame.ENCOUNTER_COOLDOWN < int(time.time()):
            return False
        if random.randint(1, 100) > RpgGame.ENCOUNTER_CHANCE:
            self.start_encounter()
        else:
            return False

    # PLAYER commands

    def player_info(self, player):
        for c in self.characters:
            if c.owner == player:
                return self.db.get_text('your-char') + c.fullinfo()
        return self.db.get_text('not-playing')

    def add_player(self, player):
        if self.is_playing(player):
            return self.db.get_text('already-playing')
        c = RpgGame.Character(owner=player)
        c.cc = self.db.classes[random.randint(0, len(self.db.classes)-1)]
        c.cr = self.db.races[random.randint(0, len(self.db.races)-1)]
        c.reset()
        self.characters.append(c)
        return c.name + self.db.get_text('party-join')

    def remove_player(self, player):
        if not self.is_playing(player):
            return self.db.get_text('not-playing')
        for c in self.characters:
            if c.owner == player:
                self.characters.remove(c)
                return c.name + self.db.get_text('party-quit')

    def player_action(self, player, action):
        return '%s tried an action.' % player

    def list_characters(self, newline=True):
        response = ''
        for c in self.characters:
            response += c.summary()
            if newline:
                response += '\n'
        return response

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
                    return self.db.list_spells()
                elif things == 'classes':
                    return self.db.list_classes()
                elif things == 'races':
                    return self.db.list_races()
                elif things == 'characters':
                    return self.list_characters()
                elif things == 'states':
                    return self.db.list_states()
                else:
                    return '[[ I do not know any of those. ]]'
            except KeyError:
                return '[[ List needs another parameter. ]]'
        return self.db.get_text('text_help_short')

    def pvt_command(self, player, command):
        if self.disabled:
            return
        action = command.lower().split()
        if action[0] == 'help':
            return self.db.get_text('text_help')
        if action[0] == 'status':
            return self.player_info(player)
        if action[0] == 'encounter-new':
            if self.trigger_encounter():
                return 'OK'
            else:
                return 'Tried'
        return self.db.get_text('unknown')


def run_rpg_tests():
    pass

if __name__ == '__main__':
    run_rpg_tests()
