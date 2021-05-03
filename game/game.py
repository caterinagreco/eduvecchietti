from typing import Dict
from random import choice

from mido import MidiFile

from game.player import Player
from game.synth import Synth
from game.dashboard import Dashboard


class Game:

    def __init__(self, config: Dict):
        self.config = config
        self.is_configured = False

    def __get_diff_level(self) -> str:
        return "2"

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
        self.player.play_demo()
        self.dashboard.hook_sensors()
        self.player.play()