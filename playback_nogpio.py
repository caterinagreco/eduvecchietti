import random
from typing import List, Set, Tuple
from mido import MidiFile

from game.synth import Synth


def find_existing_channels(midi: MidiFile) -> Set[int]:
    """Computes the channels used by a MIDI File

    :param midi: the MIDI File to operate on.
    :return: The channels present in the MIDI File.
    """
    return set(msg.channel for msg in midi if not msg.is_meta)


def play_with_synth(midi: MidiFile, fs: Synth, chosen_channels: List[int]):
    """Plays a MIDI File through FluidSynth, with the option to modify playing channels.

    :param midi: The MIDI File to play.
    :param fs: The Synth to use.
    :param chosen_channels: A reference to the channels that must be played.
    :return: None
    """
    print("Playing...")
    for i, message in enumerate(midi.play()):
        if message.channel in chosen_channels or not message.type == 'note_on':
            fs.play_midi_message(msg=message)
        #if i > 0 and i % 100 == 0:
        #    chosen_channels = random.sample([0, 1, 2, 3, 4, 5], random.randint(1, 6))


def load_midi(filename: str) -> Tuple[MidiFile, Set[int]]:
    """Load a MIDI File and checks the channels that it uses.

    :param filename: The path to the MIDI File.
    :return: The loaded MIDI File and the channels it uses.
    """
    midi = MidiFile(filename=filename)
    existing_channels = find_existing_channels(midi=midi)
    print("Midi loaded...")
    return midi, existing_channels


def main():
    # Get the Synth
    fs = Synth("/Users/caterinagreco/Desktop/PROGETTO INF./soundfonts/TimGM6mb.sf2", 'portaudio')

    # Load the MIDI File
    midi, existing_channels = load_midi("midi/azzurro.mid")
    # In the beginning all existing channels play
    chosen_channels = list(existing_channels)

    # Play the MIDI Song
    play_with_synth(midi=midi, fs=fs, chosen_channels=chosen_channels)

    print("Done!")


if __name__ == '__main__':
    main()
