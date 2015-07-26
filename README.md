# upbeat

This is a generic role playing game. It lets multiple people participate in
text-based combat (and, eventually, non-combat encounters). The primary intent
is for a low-attention game that can be running in an IRC or Slack channel
with only occasional interaction.

The RPG loads flavor data (classes, races, spells, etc.) from a URL. For the
time being it pulls pre-generated JSON but there's no reason it couldn't be
reading data from a dynamically-generated REST API.

# cli

You can run this on a commandline using cli.py. You should have a venv set up
with requests installed (`pip install -r pip-requirements.txt``). The
brute-force input handling (stolen blatantly from a google result for "python
non blocking input") will only work on unix-ish platforms (including osx) and
won't work well from the console of an IDE.

Note 1: You can't do the private-message commands this way, just the public
ones -- they all begin with an exclamation point.

Note 2: You REALLY REALLY want to turn off DEBUG in game.py before running the
CLI mode.

# rpgbot

This a plugin for Slack's demonstration bot
(https://github.com/slackhq/python-rtmbot) that loads the RPG class and
handles input and output.

To use this interface, install and configure python-rtmbot as described in
their docs. You'll need a Slack account and the ability to create a bot user
to get very far. Stick rpgbot.py in plugins/, make sure the rpg module is in
your venv, and create a configuration file in the working directory (see
below).

(For testing, I've been doing `ln -s ../upbeat/rpg .` and `ln -s ../upbeat/plugins .`
in a clone of rtmbot repo)

The bot looks for a config file called `gameconfig.json`  that should have
the following stuff:
* RPGCHANNEL: the ugly Slack channel ID for the channel to use for the game
(e.g. C123456789)
* DEBUG: true or false as you see fit
* SLACK_KEY: a Slack API key, preferably the same one you use for the rtmbot
config
* IGNORELIST: [] of the user IDs (e.g. U123456789) you want to ignore. Sticking
the bot's user ID in there is probably a good idea.

