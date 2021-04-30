from mido import MidiFile

from game.synth import Synth
from game.player import Player


def main():
    # Get the Synth
    synth = Synth("/Users/caterinagreco/Desktop/PROGETTO INF./soundfonts/TimGM6mb.sf2", 'portaudio')

    # Load the MIDI File
    midi = MidiFile(filename="midi/americano.mid")

    # Play the MIDI Song
    player = Player(synth, midi)
    player.play_demo()

    player.active_channels = player.get_existing_channels()
    player.play()

    print("Done!")


if __name__ == '__main__':
    main()
