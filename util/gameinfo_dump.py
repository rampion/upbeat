#!/usr/bin/env python
import json
from datetime import datetime

game_dict = {
    "version": "0.1",
    "created": datetime.now().isoformat(),
    "classes": [
        {
            "name": "warrior",
            "name_cap": "Warrior",
            "name_pl": "warriors",
            "player_valid": True,
            "npc_valid": True,
        },
        {
            "name": "thief",
            "name_cap": "Thief",
            "name_pl": "thieves",
            "player_valid": True,
            "npc_valid": True,
        },
        {
            "name": "wizard",
            "name_cap": "Wizard",
            "name_pl": "wizards",
            "player_valid": True,
            "npc_valid": False,
        },
        {
            "name": "witch doctor",
            "name_cap": "Witch Doctor",
            "name_pl": "witch doctors",
            "player_valid": False,
            "npc_valid": True,
        },
        {
            "name": "berzerker",
            "name_cap": "Berzerker",
            "name_pl": "berzerkers",
            "player_valid": True,
            "npc_valid": True,
        },
    ],
    "spells": [
        {
            "name": "attack",
            "action": "attacks the target",
            "description": "Perform a melee attack with your weapon.",
            "num_targets": 1,
            "valid_target_mood_max": 0,
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
            "valid_target_mood_max": 0,
            "hit_chance": 80,
            "hit": {
                "damage": 4,
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
            "valid_target_mood_min": 0,
            "hit_chance": 100,
            "hit": {
                "damage": -8,
            }
        },
        {
            "name": "enrage",
            "action": "goes into a berserker rage.",
            "description": "Become angry.",
            "valid_classes": [
                "berzerker",
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
                "berzerker",
            ],
            "prereq_caster_status":[
                "enraged",
            ],
            "num_targets": 1,
            "hit_chance": 80,
            "hit": {
                "damage": 8,
            }
        },
    ],
    "states": [
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
    ],
    "races": [
        {
            "name": "elf",
            "name_cap": "Elf",
            "name_pl": "elves",
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
        },
    ],
}

encounter_dict = [
    {
        "name": "monster",
        "description": "A wandering monster appears",
        "weight": 100,
        "triggers": [
            "add-monster-angry",
        ]
    },
    {
        "name": "monsters",
        "description": "Two wandering monsters appear",
        "weight": 100,
        "triggers": [
            "add-monster-angry",
            "add-monster-angry",
        ]
    },
    {
        "name": "find-object",
        "description": "The party discovers something.",
        "weight": 20,
        "triggers": [
            "add-object-random"
        ]
    }
]

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

text_help_short = '[[ I am a game bot. Message me the world "help" for details. ]]'

game_text = {
    "text_help": text_help,
    "text_help_short": text_help_short,
}

game_config = {
    'RPGCHANNEL': 'C12345',
    'IGNORELIST': ['U12345', ],
    'SLACK_KEY': 'xoxb-zzzz-zzzzzz',
    'DEBUG': True,
}


if __name__ == '__main__':
    with open('gamedata.json', 'w') as info_fh:
        json.dump(game_dict, info_fh, indent=2)
    with open('gametext.json', 'w') as text_fh:
        json.dump(game_text, text_fh, indent=2)
    with open('gameconfig.json', 'w') as config_fh:
        json.dump(game_config, config_fh, indent=2)
    with open('encounters.json', 'w') as encounter_fh:
        json.dump(encounter_dict, encounter_fh, indent=2)
