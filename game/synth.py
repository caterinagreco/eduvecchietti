import fluidsynth
from mido import Message


class Synth:

    def __init__(self, soundfont: str = "/usr/share/sounds/sf2/TimGM6mb.sf2", driver: str = 'alsa'):
        self.fs = fluidsynth.Synth(samplerate=48000, gain=0.8)
        self.fs.start(driver)
        self.sfid = self.fs.sfload(soundfont, 1)
        self.fs.program_select(0, self.sfid, 0, 0)

    def play_midi_message(self, msg: Message) -> None:
        if msg.type == 'note_on':
            self.fs.noteon(msg.channel, msg.note, msg.velocity)
        elif msg.type == 'note_off':
            self.fs.noteoff(msg.channel, msg.note)
        elif msg.type == 'control_change':
            self.fs.cc(msg.channel, msg.control, msg.value)
        elif msg.type == 'program_change':
            self.fs.program_change(msg.channel, msg.program)
        elif msg.type == 'pitchwheel':
            self.fs.pitch_bend(msg.channel, msg.pitch)
        elif msg.type == 'aftertouch':
            # TODO: AfterTouch exists in fluidsynth as Channel Pressure but seems not implemented in pyFluidSynth
            print('AfterTouch missing!')
        else:
            print(f'Message of type {msg.type} not recognized!')

    def reset(self) -> None:
        self.fs.system_reset()
