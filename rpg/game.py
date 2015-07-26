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
    CONFIG_VERSION = '0.2'
    URL_GAMEDATA = 'http://upbeat.projectmayhem.org:21218/data/gamedata.json'
    URL_GAMETEXT = 'http://upbeat.projectmayhem.org:21218/data/gametext.json'
    URL_ENCOUNTERS = 'http://upbeat.projectmayhem.org:21218/data/encounters.json'
    ERROR_LOADING_ERRORS = '[[ Unrecoverable error trying to load language files. Aborting. ]]'
    ERROR_UNKNOWN_COMMAND = 'I do not understand what you want to do.'
    ERROR_UNDEFINED_STRING = '[[ A message goes here but it is not defined for your language. ]]'

    class CharacterStat(object):
        def __init__(self, name, base=10, maximum=20):
            self.name = name
            self.value_base = base
            self.value_max = maximum

    # class CharacterStatMod(object):
    #     def __init__(self, stat, mod_value):
    #         self.stat = stat
    #         self.mod_value = mod_value

    class CharacterClass(object):
        def __init__(self, name):
            self.name = name
            self.name_cap = name
            self.name_pl = name + 's'
            self.valid_player = True
            self.valid_npc = True
            self.stat_modifiers = []

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

    class CharacterCondition(object):
        def __init__(self, name=''):
            self.name = name
            self.name_short = name

    class GameEncounter(object):
        def __init__(self, name):
            self.name = name
            self.events = []

        def add_event(self, event):
            self.events.append(event)

    # class GameEncounterTrigger(object):
    #     def __init__(self):
    #         self.

    def __init__(self):
        self.error = False
        self.stats = []
        self.classes = []
        self.races = []
        self.spells = []
        self.conditions = []
        self.encounters = []
        self.texts = {}
        self.load_text()
        self.load_data()

    def load_text(self):
        r = requests.get(RpgGameDB.URL_GAMETEXT)
        if r.status_code == requests.codes.ok:
            text_data = r.json()
            if text_data['version'] != RpgGameDB.CONFIG_VERSION:
                dprint('config version mismatch')
                self.error = True
                return
            for text in text_data['text']:
                self.texts[text] = text_data['text'][text]
                dprint('Loaded text %s' % text)
        else:
            dprint('Error retrieving text')
            self.error = True

    def load_data(self):
        r = requests.get(RpgGameDB.URL_GAMEDATA)
        if r.status_code == requests.codes.ok:
            game_data = r.json()
            # This whole thing explodes if there's a missing section in the JSON.
            # I considered wrapping each part in try/except or whole thing
            # but TBH if we're missing data the whole thing should just crash
            if game_data['version'] != RpgGameDB.CONFIG_VERSION:
                dprint('config version mismatch')
                self.error = True
                return
            for char_stat in game_data['stats']:
                st = RpgGameDB.CharacterStat(name=char_stat['name'])
                st.value_base = char_stat['value_base']
                st.value_max = char_stat['value_max']
                dprint('Loaded stat %s' % st.name)
                self.stats.append(st)
            for char_class in game_data['classes']:
                cc = RpgGameDB.CharacterClass(name=char_class['name'])
                cc.name_cap = char_class['name_cap']
                cc.name_pl = char_class['name_pl']
                dprint('Loaded class %s' % cc.name_cap)
                self.classes.append(cc)
            for char_spell in game_data['spells']:
                sp = RpgGameDB.CharacterSpell(name=char_spell['name'])
                dprint('Loaded spell %s' % sp.name)
                self.spells.append(sp)
            for char_cond in game_data['conditions']:
                cond = RpgGameDB.CharacterCondition(name=char_cond['name'])
                cond.name_short = char_cond['name_short']
                dprint('Loaded condition %s' % cond.name)
                self.conditions.append(cond)
            for char_race in game_data['races']:
                cr = RpgGameDB.CharacterRace(name=char_race['name'])
                cr.name_cap = char_race['name_cap']
                cr.name_pl = char_race['name_pl']
                dprint('Loaded race %s' % cr.name_cap)
                self.races.append(cr)
            for char_enc in game_data['encounters']:
                e = RpgGameDB.GameEncounter(name=char_enc['name'])
                for v in char_enc['events']:
                    e.add_event(v)
                for x in range(0, char_enc['weight']):
                    self.encounters.append(e)
                dprint('Loaded encounter %s' % e.name)
        else:
            dprint('Error retrieving data')
            self.error = True

    def get_text(self, message):
        return self.texts.get(message, RpgGameDB.ERROR_UNDEFINED_STRING)

    @property
    def max_class(self):
        return len(self.classes) - 1

    @property
    def max_race(self):
        return len(self.races) - 1

    @property
    def max_encounter(self):
        return len(self.encounters) - 1

    @property
    def max_spell(self):
        return len(self.spells) - 1

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

    def list_conditions(self, newline=True):
        response = ''
        for c in self.conditions:
            response += c.name
            if newline:
                response += '\n'
        return response

    def random_class(self, npc=False):
        c = self.classes[random.randint(0, len(self.classes) - 1)]
        return c

    def random_race(self, npc=False):
        r = self.races[random.randint(0, len(self.races) - 1)]
        return r


class RpgGame(object):
    ENCOUNTER_CHANCE = 50  # chance of a random encounter happening
    ENCOUNTER_COOLDOWN = 300  # minimum seconds between encounters

    class Character(object):
        def __init__(self, owner=None):
            self.name = self.random_name()
            self.owner = owner
            self.hp_curr = 0
            self.hp_max = 20
            self.mood = 0
            self.conditions = []
            self.stats = []
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
                'Janice',
            ]
            return names[random.randint(0, len(names) - 1)]

        # def is_friendly(self):
        #     if self.owner is not None:
        #         return True
        #     if self.angry:
        #         return False

        def fullinfo(self):
            response = '*Name:* ' + self.name + '\n'
            response += '*Race:* ' + self.get_race() + '\n'
            response += '*Class:* ' + self.get_class() + '\n'
            return response

        def summary(self):
            response = '*%s* - %s %s (%d/%d) [%s]' % (
            self.name, self.get_race(), self.get_class(), self.hp_curr, self.hp_max, self.owner)
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
            self.hp_curr = self.hp_max
            self.conditions = []

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
            dprint('run - disabled')
            return messages
        # if bot can take any actions, take them
        dprint('%d messages, dequeueing' % len(self.public_message_queue))
        for m in self.public_message_queue:
            messages.append(m)
        self.public_message_queue = []
        return messages

    def start_encounter(self):
        encounter = self.db.encounters[random.randint(0, self.db.max_encounter)]
        assert isinstance(encounter, RpgGameDB.GameEncounter)
        for event in encounter.triggers:
            if event == 'add-monster-angry':
                c = RpgGame.Character()
                c.mood = -3
                # c.cc =
        self.encounter_timestamp = time.time()

    def finish_encounter(self):
        self.combat = False
        self.encounter_timestamp = time.time()
        # do looting here

    def trigger_encounter(self):
        if self.disabled:
            dprint('trigger - disabled')
            return False
        if self.combat:
            dprint('trigger - in combat')
            return False
        if self.encounter_timestamp + RpgGame.ENCOUNTER_COOLDOWN > int(time.time()):
            dprint('trigger - too soon: %d %d %d' % (
            self.encounter_timestamp, RpgGame.ENCOUNTER_COOLDOWN, int(time.time())))
            return False
        if random.randint(1, 100) > RpgGame.ENCOUNTER_CHANCE:
            dprint('trigger - JACKPOT')
            self.start_encounter()
            return True
        else:
            dprint('trigger - nothing')
            self.public_message_queue.append(self.db.get_text('party-wander'))
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
        c.cc = self.db.random_class()
        c.cr = self.db.random_race()
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
                elif things == 'conditions':
                    return self.db.list_conditions()
                else:
                    return '[[ I do not know any of those. ]]'
            except (KeyError, IndexError):
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
