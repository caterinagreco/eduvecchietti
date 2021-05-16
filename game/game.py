from typing import Dict
from random import choice

from mido import MidiFile
from gpiozero import RotaryEncoder

from game.player import Player
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

    def __get_diff_level(self) -> str:
        levels = list(self.config["songs_by_level"].keys())
        max_steps = self.config["encoder"]["max_steps"] + 1
        step = self.level_encoder.steps
        level_index = int(step * len(levels) / max_steps)
        return levels[level_index]

    def configure(self) -> None:
        self.synth = Synth(soundfont=self.config["synth"]["soundfont"], driver=self.config["synth"]["driver"])
        self.song = MidiFile(filename=choice(self.config["songs_by_level"][self.__get_diff_level()]))
        self.player = Player(synth=self.synth, song=self.song)
        self.dashboard = Dashboard(
            player=self.player,
            hall_config=self.config["hall"],
            channel_config=self.config["channel"],
            led_config=self.config["led_strip"]
        )
        self.is_configured = True

    def start(self) -> None:
        if not self.is_configured:
            self.configure()
        self.dashboard.led_strip.animation()
        self.player.play_demo()
        self.dashboard.led_strip.animation()
        self.dashboard.hook_sensors()
        self.player.play()
