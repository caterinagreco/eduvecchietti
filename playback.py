from typing import List, Set, Callable, Tuple

import fluidsynth
import random
from mido import MidiFile
from gpiozero import Button, LED


def find_existing_channels(midi: MidiFile) -> Set[int]:
    """Computes the channels used by a MIDI File

    :param midi: the MIDI File to operate on.
    :return: The channels present in the MIDI File.
    """
    existing_channels = []
    for track in midi.tracks:
        for msg in track:
            # Meta messages do not have channels
            if not msg.is_meta:
                existing_channels.append(msg.channel)
                # Assuming all channels are the same for each track
                break
    # Converting to set in case multiple tracks play on the same channel
    return set(existing_channels)


def get_channel_switcher(container: List[int]) -> Callable:
    """Returns a function that, each time is called,
    modifies a list of playing channels IN PLACE.

    :param container: The list that must be modified to switch channels.
    :return: The function that switches channels.
    """
    def channel_switcher() -> None:
        container.clear()
        container.extend(random.sample([0, 1, 2], random.randint(1, 3)))
        print(f'Randomly playing channels {container}')
    return channel_switcher


def get_led_manager(container: List[int], reference: Set[int], led: LED) -> Callable:
    """Returns a function that, each time is called,
    switches on or off the LED based on the presence of
    elements in 'container' that are not in 'reference'.

    :param container: A reference to the selected elements.
    :param reference: A list of allowed elements.
    :param led: The LED to operate on.
    :return: The functions that operates the LED.
    """
    def led_manager():
        if all([elem in reference for elem in container]):
            led.off()
        else:
            led.on()
    return led_manager


def chain_functions(*funcs: Callable) -> Callable:
    """Concatenates multiple zero-argument functions.

    :param funcs: The functions to call.
    :return: A function that sequentially calls all given functions.
    """
    def chained():
        for func in funcs:
            func()
    return chained


def play_with_synth(midi: MidiFile, fs: fluidsynth.Synth, chosen_channels: List[int]):
    """Plays a MIDI File through FluidSynth, with the option to modify playing channels.

    :param midi: The MIDI File to play.
    :param fs: The Synth to use.
    :param chosen_channels: A reference to the channels that must be played.
    :return: None
    """
    print("Playing...")
    for message in midi.play():
        if message.channel in chosen_channels or not message.type == 'note_on':
            if message.type == 'note_on':
                fs.noteon(message.channel, message.note, message.velocity)
            if message.type == 'note_off':
                fs.noteoff(message.channel, message.note)


def get_synth() -> fluidsynth.Synth:
    """Builds a simple Synth with FluidSynth

    :return: None
    """
    fs = fluidsynth.Synth(samplerate=48000, gain=0.8)
    fs.start("alsa")
    sfid = fs.sfload("/usr/share/sounds/sf2/FluidR3_GM.sf2", 1)
    fs.program_select(0, sfid, 0, 0)
    return fs


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
    # Setup physical connections
    button = Button(12)
    # RGB Common Anode LED is on when signal is low
    led = LED(4, active_high=False)

    # Get the Synth
    fs = get_synth()

    # Load the MIDI File
    midi, existing_channels = load_midi("midi/two_channels.mid")
    # In the beginning all existing channels play
    chosen_channels = list(existing_channels)

    # Setup callbacks for button pressed
    button.when_pressed = chain_functions(
        get_channel_switcher(container=chosen_channels),
        get_led_manager(container=chosen_channels, reference=existing_channels, led=led)
    )

    # Play the MIDI Song
    play_with_synth(midi=midi, fs=fs, chosen_channels=chosen_channels)

    print("Done!")


if __name__ == '__main__':
    main()
