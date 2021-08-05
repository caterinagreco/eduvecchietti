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
    """Classe che gestisce lo svolgimento di una o più partite.
    """
    def __init__(self, config: Dict):
        """Inizializza il gioco e alcuni degli elementi di base indipendenti dall'azione del giocatore.

        Args:
            config: dizionario che contiene la configurazione da usare per la partita.
        """
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
        """Restiutisce il livello di difficoltà selezionato sulla base della posizione del rotary encoder.

        Returns:
            Stringa che rappresenta il livello di difficoltà.
        """
        levels = list(self.config["songs_by_level"].keys())
        max_steps = self.config["encoder"]["max_steps"] + 1
        step = self.level_encoder.steps
        level_index = int(step * len(levels) / max_steps)
        return levels[level_index]

    def configure(self) -> None:
        """Inizializza e configura tutti gli elementi necessari allo svolgimento della partita
        sulla base della configurazione e del livello di difficoltà scelto. Qualora la configurazione
        fosse già avvenuta resetta gli elementi già presenti.

        Returns:
            None
        """
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
        """Prepara e avvia la partita.

        Returns:
            None
        """
        if not self.is_configured:
            self.configure()
        self.player.play_demo()
        self.dashboard.hook_sensors()
        self.serial.animation_do('start')
        self.player.play()
        self.serial.animation_do('end')

