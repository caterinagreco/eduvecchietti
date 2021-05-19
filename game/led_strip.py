from time import sleep
from typing import Dict, Tuple


class LedStrip:

    _GREEN = (0, 255, 0)
    _RED = (255, 0, 0)
    _WHITE = (255, 255, 255)
    _OFF = (0, 0, 0)

    def __init__(self, led_config: Dict[str, int], channels: Dict[str, int]):
        self.led_strip = [(0, 0, 0)] * led_config["n"]
        led_per_instr = led_config["n"] // len(channels)
        self.instr_to_led = {
            k: [e for e in range(i * led_per_instr, (i + 1) * led_per_instr)]
            for i, k in enumerate(channels)
        }

    def _blink(self, color: Tuple[int, int, int], times: int = 1, duration: float = 1):
        for i in range(times):
            self.led_strip[0] = color
            sleep(duration)
            self.led_strip[0] = self._OFF
            if not i == times - 1:
                sleep(duration)

    def animation(self) -> None:
        self._blink(color=self._WHITE, times=2, duration=1)

    def _set_instrument(self, instrument: str, color: Tuple[int, int, int]):
        for pixel in self.instr_to_led[instrument]:
            self.led_strip[pixel] = color

    def positive_feedback_on(self, instrument: str) -> None:
        self._set_instrument(instrument=instrument, color=self._GREEN)

    def negative_feedback_on(self, instrument: str) -> None:
        self._set_instrument(instrument=instrument, color=self._RED)

    def feedback_off(self, instrument: str) -> None:
        self._set_instrument(instrument=instrument, color=self._OFF)
