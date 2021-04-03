import pyo
from mido import MidiFile
import random


def main():
    s = pyo.Server().boot().start()

    # A little audio synth to play the MIDI events.
    mid = pyo.Notein()
    amp = pyo.MidiAdsr(mid["velocity"])
    pit = pyo.MToF(mid["pitch"])
    osc = pyo.Osc(pyo.SquareTable(), freq=pit, mul=amp).mix(1)
    rev = pyo.STRev(osc, revtime=1, cutoff=4000, bal=0.2).out()

    # Opening the MIDI file...
    mid = MidiFile("/Users/lucabutera/Downloads/Titantic.mid")

    # ... and reading its content.
    for i, message in enumerate(mid.play()):
        # For each message, we convert it to integer data with the bytes()
        # method and send the values to pyo's Server with the addMidiEvent()
        # method. This method programmatically adds a MIDI message to the
        # server's internal MIDI event buffer.
        if i % 100 == 0 or i == 0:
            playing = random.sample([0, 1, 2, 3], random.randint(1, 4))
            print(playing)
        if message.channel in playing or not message.type == 'note_on':
            s.addMidiEvent(*message.bytes())


if __name__ == '__main__':
    main()
