from typing import List
from mido import MidiFile

from game.synth import Synth


class Player:

    def __init__(self, synth: Synth, song: MidiFile):
        self.synth = synth
        self.song = song
        self.active_channels = [False] * 16
        self.existing_channels = self.__get_existing_channels()

    def __get_existing_channels(self) -> List[bool]:
        """Computes the channels used by the player's MIDI File

        :return: The channels present in the player's MIDI File.
        """
        existing_channels = set(msg.channel for msg in self.song if not msg.is_meta)
        return [i in existing_channels for i in range(16)]

    def reset(self, new_song: MidiFile = None):
        if new_song is not None:
            self.song = new_song
            self.existing_channels = self.__get_existing_channels()
        self.active_channels = [False] * 16

    def play(self) -> None:
        print("Playing...")
        for message in self.song.play():
            if self.active_channels[message.channel] or not message.type == 'note_on':
                self.synth.play_midi_message(msg=message)

    def play_demo(self) -> None:
        print("Playing demo...")
        remaining_demo_time = 30
        for message in self.song.play():
            self.synth.play_midi_message(msg=message)
            remaining_demo_time -= message.time
            if remaining_demo_time <= 0:
                self.synth.reset()
                break
