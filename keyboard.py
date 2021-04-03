from time import sleep

import pyo


def main():
    s = pyo.Server()
    s.setMidiInputDevice(0)
    s.boot().start()
    midi = pyo.Notein()
    amp = pyo.MidiAdsr(midi['velocity'])
    pitch = pyo.MToF(midi['pitch'])
    wave = pyo.SincTable()
    osc = pyo.Osc(wave, freq=pitch, mul=amp)
    verb = pyo.Freeverb(osc).out()
    osc.out()
    sleep(1000)


if __name__ == '__main__':
    main()
