from typing import List
from mido import MidiFile

from game.synth import Synth


class Player:
    """Classe che si occupa di riprodurre un brano MIDI, con la possibilità di attivare o disattivare i canali.
    """

    def __init__(self, synth: Synth, song: MidiFile):
        """Inizializza il player con gli oggetti necessari alla riproduzione e tutti i canali disattivati.

        Args:
            synth: il sintetizzatore da utilizzare per suonare il brano.
            song: il brano MIDI da eseguire.
        """
        self.synth = synth
        self.song = song
        self.active_channels = [False] * 16
        self.existing_channels = self.__get_existing_channels()

    def __get_existing_channels(self) -> List[bool]:
        """Restituisce i canali utilizzati all'interno del brano MIDI.

        Returns:
            Lista di booleani in cui l'elemento alla posizione i-esima è True o False
            in base alla presenza del canale i-esimo nel brano.
        """
        existing_channels = set(msg.channel for msg in self.song if not msg.is_meta)
        return [i in existing_channels for i in range(16)]

    def reset(self, new_song: MidiFile = None) -> None:
        """Resetta il player disattivando tutti i canali ed eventualmente sostituisce il brano.

        Args:
            new_song: brano opzionale da sostutire a quello presente.

        Returns:
            None
        """
        if new_song is not None:
            self.song = new_song
            self.existing_channels = self.__get_existing_channels()
        self.active_channels = [False] * 16

    def play(self) -> None:
        """Riproduce il brano MIDI, utilizzando ad ogni passo solo i canali attivi.

        Returns:
            None
        """
        print("Playing...")
        for message in self.song.play():
            if self.active_channels[message.channel] or not message.type == 'note_on':
                self.synth.play_midi_message(msg=message)

    def play_demo(self) -> None:
        """Riproduce i primi 30 secondi del brano con tutti i canali attivi.

        Returns:
            None
        """
        print("Playing demo...")
        remaining_demo_time = 30
        for message in self.song.play():
            self.synth.play_midi_message(msg=message)
            remaining_demo_time -= message.time
            if remaining_demo_time <= 0:
                self.synth.reset()
                break
