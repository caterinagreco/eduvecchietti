from typing import List

import fluidsynth
import random
from mido import MidiFile
from gpiozero import Button, LED


def find_existing_channels(m: MidiFile) -> List[int]:
    return [track[0].channel for track in m.tracks]


def get_playing_channels() -> List[int]:
    return random.sample([0, 1, 2], random.randint(1, 3))


def main():
    # Setup physical connections
    button = Button(12)
    led = LED(4)
    led.on()

    fs = fluidsynth.Synth(samplerate=48000,gain=0.8)
    fs.start("alsa")
    sfid = fs.sfload("/usr/share/sounds/sf2/FluidR3_GM.sf2", 1)
    fs.program_select(0, sfid, 0, 0)

    midi = MidiFile("midi/two_channels.mid")
    existing_channels = find_existing_channels(m=midi)
    playing = [0, 1]
    print("Midi loaded...")

    print("Playing...")
    for i, message in enumerate(midi.play()):
        if button.is_pressed:
            playing = get_playing_channels()
            if playing not in existing_channels:
                led.off()
            else:
                led.on()
            print(f'Randomly playing channels {playing}')
        if message.channel in playing or not message.type == 'note_on':
            if message.type == 'note_on':
                fs.noteon(message.channel, message.note, message.velocity)
            if message.type == 'note_off':
                fs.noteoff(message.channel, message.note)
    print("done")


if __name__ == '__main__':
    main()
