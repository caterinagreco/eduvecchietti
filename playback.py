import fluidsynth
import random
from mido import MidiFile

def main():
    fs = fluidsynth.Synth(samplerate=48000,gain=0.8)
    fs.start("alsa")
    sfid = fs.sfload("/usr/share/sounds/sf2/FluidR3_GM.sf2", 1)
    fs.program_select(0, sfid, 0, 0)

    mid = MidiFile("midi/two_channels.mid")
    print("Midi loaded...")

    for i, message in enumerate(mid.play()):
            # For each message, we convert it to integer data with the bytes()
            # method and send the values to pyo's Server with the addMidiEvent()
            # method. This method programmatically adds a MIDI message to the
            # server's internal MIDI event buffer.
        if i % 100 == 0 or i == 0:
            playing = random.sample([0, 1], random.randint(1, 2))
            print(playing)
        if message.channel in playing or not message.type == 'note_on':
            if message.type == 'note_on':
                fs.noteon(message.channel, message.note, message.velocity)
            if message.type == 'note_off':
                fs.noteoff(message.channel, message.note)
    print("done")


if __name__ == '__main__':
    main()
