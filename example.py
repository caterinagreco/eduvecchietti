import pyo
from mido import MidiFile
import random
import platform


def main():
    audio = 'coreaudio' if platform.system() == 'Darwin' else 'portaudio'
    s = pyo.Server(audio=audio, duplex=0).boot().start()

    # A little audio synth to play the MIDI events.
    mid = pyo.Notein()
    amp = pyo.MidiAdsr(mid["velocity"])
    pit = pyo.MToF(mid["pitch"])
    osc = pyo.Osc(pyo.ParaTable(), freq=pit, mul=amp).mix(1)
    rev = pyo.STRev(osc, revtime=1, cutoff=4000, bal=0.2).out()

    # Opening the MIDI file...
    mid = MidiFile("midi/two_channels.mid")

    # ... and reading its content.
    for i, message in enumerate(mid.play()):
        # For each message, we convert it to integer data with the bytes()
        # method and send the values to pyo's Server with the addMidiEvent()
        # method. This method programmatically adds a MIDI message to the
        # server's internal MIDI event buffer.
        if i % 100 == 0 or i == 0:
            playing = random.sample([0, 1], random.randint(1, 2))
            print(playing)
        if message.channel in playing or not message.type == 'note_on':
            s.addMidiEvent(*message.bytes())


if __name__ == '__main__':
    main()
