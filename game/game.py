from time import sleep
from typing import Dict
from random import choice

from mido import MidiFile
from gpiozero import RotaryEncoder

from game.player import Player
from game.serial_communication import SerialCommunication
from game.synth import Synth
from game.dashboard import Dashboard


class Game:

    def __init__(self, config: Dict):
        self.config = config
        self.is_configured = False
        self.level_encoder = RotaryEncoder(
            a=config["encoder"]["clk"],
            b=config["encoder"]["dt"],
            max_steps=config["encoder"]["max_steps"],
        )
        self.serial = SerialCommunication()
        sleep(2)
        self.serial.animation_do('gameon')

    def __get_diff_level(self) -> str:
        levels = list(self.config["songs_by_level"].keys())
        max_steps = self.config["encoder"]["max_steps"] + 1
        step = self.level_encoder.steps
        level_index = int(step * len(levels) / max_steps)
        return levels[level_index]

    def configure(self) -> None:
        if self.is_configured:
            self.synth.reset()
            self.song = MidiFile(filename=choice(self.config["songs_by_level"][self.__get_diff_level()]))
            self.dashboard.reset()
            self.player.reset(new_song=self.song)
        else:
            self.synth = Synth(soundfont=self.config["synth"]["soundfont"], driver=self.config["synth"]["driver"])
            self.song = MidiFile(filename=choice(self.config["songs_by_level"][self.__get_diff_level()]))
            self.player = Player(synth=self.synth, song=self.song)
            self.dashboard = Dashboard(
                player=self.player,
                hall_config=self.config["hall"],
                channel_config=self.config["channel"],
                serial=self.serial,
            )
            self.is_configured = True

    def start(self) -> None:
        if not self.is_configured:
            self.configure()
        self.player.play_demo()
        self.dashboard.hook_sensors()
        self.serial.animation_do('start')
        self.player.play()
        self.serial.animation_do('end')

