#!/usr/bin/env python
import json
from datetime import datetime

version = '0.2'

stats = [
    {
        "name": "strength",
        "value_base": 5,
        "value_max": 20,
    },
    {
        "name": "agility",
        "value_base": 5,
        "value_max": 20,
    },
    {
        "name": "intelligence",
        "value_base": 5,
        "value_max": 20,
    },
    {
        "name": "health",
        "value_base": 5,
        "value_max": 20,
    },
    {
        "name": "hit",
        "value_base": 80,
        "value_max": 100,
    }
]

classes = [
    {
        "name": "warrior",
        "name_cap": "Warrior",
        "name_pl": "warriors",
        "valid_player": True,
        "valid_npc": True,
        "stats": {
            "health": "+2",
        }
    },
    {
        "name": "thief",
        "name_cap": "Thief",
        "name_pl": "thieves",
        "valid_player": True,
        "valid_npc": True,
        "stats": {
            "agility": "+2",
        }
    },
    {
        "name": "wizard",
        "name_cap": "Wizard",
        "name_pl": "wizards",
        "valid_player": True,
        "valid_npc": False,
        "stats": {
            "intelligence": "+2",
        }
    },
    {
        "name": "witch doctor",
        "name_cap": "Witch Doctor",
        "name_pl": "witch doctors",
        "valid_player": False,
        "valid_npc": True,
    },
    {
        "name": "berserker",
        "name_cap": "Berserker",
        "name_pl": "berserker",
        "valid_player": True,
        "valid_npc": True,
        "stats": {
            "hit": "-10",
        }
    },
]

races = [
    {
        "name": "elf",
        "name_cap": "Elf",
        "name_pl": "elves",
        "stats": {
            "hit": "+10",
        }
    },
    {
        "name": "human",
        "name_cap": "Human",
        "name_pl": "humans",
    },
    {
        "name": "fish",
        "name_cap": "Fish",
        "name_pl": "fish",
        "stats": {
            "max_hp": "-5",
        }

    },
]

spells = [
    {
        "name": "attack",
        "action": "attacks the target",
        "description": "Perform a melee attack with your weapon.",
        "num_targets": 1,
        "valid_target": {
            "mood_max": 0,
        },
        "hit_chance": 80,
        "hit": {
            "damage": 2,
        }
    },
    {
        "name": "fireball",
        "action": "launches a ball of fire at the target.",
        "description": "Summon a ball of fire from the ether and hurl it at an enemy.",
        "valid_classes": [
            "wizard",
        ],
        "num_targets": 2,
        "valid_target": {
            "mood_max": 0,
        },
        "hit_chance": 80,
        "hit": {
            "damage": 4,
            "add_status": "burning",
        }
    },
    {
        "name": "heal",
        "action": "prays to their deity for aid helping the target.",
        "description": "Call on your deity's grace to restore an ally's health.",
        "valid_classes": [
            "cleric",
        ],
        "num_targets": 1,
        "valid_target": {
            "mood_min": 0,
        },
        "hit_chance": 100,
        "hit": {
            "damage": -8,
        }
    },
    {
        "name": "sap",
        "action": "deftly smacks their target on the head with something heavy.",
        "description": "Whack them on the head.",
        "valid_classes": [
            "thief"
        ],
        "num_targets": 1,
        "valid_target": {
            "mood_max": 0,
        },
        "hit": {
            "add_status": "stunned"
        }

    },
    {
        "name": "enrage",
        "action": "goes into a berserker rage.",
        "description": "Become angry.",
        "valid_classes": [
            "berserker",
        ],
        "num_targets": 0,
        "hit_chance": 100,
        "hit": {
            "add_status": "enraged",
        }
    },
    {
        "name": "frenzied attack",
        "action": "unleashes their fury on a target.",
        "description": "HULK SMASH.",
        "valid_classes": [
            "berserker",
        ],
        "prereq_caster_status": [
            "enraged",
        ],
        "num_targets": 1,
        "hit_chance": 80,
        "hit": {
            "damage": 8,
        }
    },
]

conditions = [
    {
        "name": "stunned",
        "name_short": "STN",
    },
    {
        "name": "unconscious",
        "name_short": "UNC",
    },
    {
        "name": "burning",
        "name_short": "BRN",
    },
    {
        "name": "enraged",
        "name_short": "ENR",
    },
]

effects = [

]

events = [

]

encounters = [
    {
        "name": "monster",
        "description": "A wandering monster appears",
        "weight": 100,
        "events": [
            "add-monster-angry",
        ]
    },
    {
        "name": "monsters",
        "description": "Two wandering monsters appear",
        "weight": 100,
        "events": [
            "add-monster-angry",
            "add-monster-angry",
        ]
    },
    {
        "name": "find-object",
        "description": "The party discovers something.",
        "weight": 20,
        "events": [
            "add-object-random"
        ]
    }
]

game_data_dict = {
    "version": version,
    "created": datetime.now().isoformat(),
    "stats": stats,
    "classes": classes,
    "races": races,
    "spells": spells,
    "conditions": conditions,
    "effects": effects,
    "events": events,
    "encounters": encounters,
}

text_help = 'Welcome to ROLE PLAYING GAME.\n\n' \
            'This is a simple cooperative game where players' \
            'take part in a fantasy adventure. This chat bot "manages" the game' \
            'and anyone in the channel is welcome' \
            'to join the team (or just watch).\n\n' \
            'All commands start with an exclamation point:\n' \
            '- *!join* - The bot will create a character for you (not available during combat)\n' \
            '- *!quit* - Your character will leave the party\n' \
            '- *!attack* - Your character will fight a monster during combat\n' \
            '- *!spell* - Your character will cast a spell, if able to do so\n' \
            '- *!heal* - Your character will attempt to heal an ally, if able to do so\n' \
            '- *!run* - Your character will attempt to run away from combat\n' \
            '(These are not all the commands.)'

game_text = {
    "text_help": text_help,
    "text_help_short": "[[ I am a game bot. Message me the world \"help\" for details. ]]",
    "not-playing": "No character was found for you. Have you tried joining the game with `!join` in the game channel?",
    "unknown": "I do not understand what you want me to do!",
    "no-races": "No races known.",
    "no-classes": "No classes known.",
    "no-characters": "No characters are present.",
    "no-spells": "No spells known.",
    "your-char": "You control the following character:\n",
    "party-quit": " departs the party.",
    "party-join": " joins the party.",
    "party-wander": "The party continues to wander without incident.",
}

game_text_dict = {
    "version": version,
    "created": datetime.now().isoformat(),
    "text": game_text
}

game_config_dict = {
    'RPGCHANNEL': 'C12345',
    'IGNORELIST': ['U12345', ],
    'SLACK_KEY': 'xoxb-zzzz-zzzzzz',
    'DEBUG': True,
}

if __name__ == '__main__':
    with open('gamedata.json', 'w') as info_fh:
        json.dump(game_data_dict, info_fh, indent=2)
    with open('gametext.json', 'w') as text_fh:
        json.dump(game_text_dict, text_fh, indent=2)
    with open('gameconfig.json', 'w') as config_fh:
        json.dump(game_config_dict, config_fh, indent=2)
