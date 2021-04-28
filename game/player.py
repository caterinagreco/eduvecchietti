from typing import Set

from mido import MidiFile

from game.synth import Synth


class Player:

    def __init__(self, synth: Synth, song: MidiFile):
        self.synth = synth
        self.song = song
        self.active_channels = set()

    def get_existing_channels(self) -> Set[int]:
        """Computes the channels used by the player's MIDI File

        :return: The channels present in the player's MIDI File.
        """
        return set(msg.channel for msg in self.song if not msg.is_meta)

    def activate_channel(self, channel: int) -> None:
        self.active_channels.add(channel)

    def deactivate_channel(self, channel: int) -> None:
        self.active_channels.remove(channel)

    def play(self) -> None:
        print("Playing...")
        for message in self.song.play():
            if message.channel in self.active_channels or not message.type == 'note_on':
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
