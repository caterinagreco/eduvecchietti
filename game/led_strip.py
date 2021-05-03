from typing import Dict

import neopixel


class LedStrip:

    def __init__(self, led_config: Dict[str, int], channels: Dict[str, int]):
        self.led_strip = neopixel.NeoPixel(
            pin=led_config["pin"],
            n=led_config["n"],
            bpp=3,
            brightness=led_config["brightness"],
            auto_write=True,
            pixel_order="RGB"
        )
        led_per_instr = led_config["n"] // len(channels)
        self.instr_to_led = {
            k: [e for e in range(i * led_per_instr, (i + 1) * led_per_instr)]
            for i, k in enumerate(channels)
        }

    def animation(self) -> None:
        pass

    def led_game_on(self) -> None:
        pass

    def positive_feedback_on(self) -> None:
        pass

    def positive_feedback_off(self) -> None:
        pass

    def negative_feedback_on(self) -> None:
        pass

    def negative_feedback_off(self) -> None:
        pass
