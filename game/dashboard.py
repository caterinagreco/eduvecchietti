from typing import Dict, Callable

from gpiozero import DigitalInputDevice

from game.led_strip import LedStrip
from game.player import Player


class Dashboard:

    def __init__(
            self,
            player: Player,
            hall_config: Dict[str, int],
            channel_config: Dict[str, int],
            led_config: Dict[str, int]):
        self.player = player
        self.channel_config = channel_config
        self.led_strip = LedStrip(led_config=led_config, channels=channel_config)
        self.hall = {k: DigitalInputDevice(pin=v, pull_up=True) for k, v in hall_config.items()}

    def __existing_hall_on(self, channel: int, instrument: str) -> Callable:
        def action():
            self.player.active_channels[channel] = True
            self.led_strip.positive_feedback_on(instrument=instrument)
        return action

    def __existing_hall_off(self, channel: int, instrument: str) -> Callable:
        def action():
            self.player.active_channels[channel] = False
            self.led_strip.feedback_off(instrument=instrument)
        return action

    def __non_existing_hall_on(self, instrument: str) -> Callable:
        def action():
            self.led_strip.negative_feedback_on(instrument=instrument)
        return action

    def __non_existing_hall_off(self, instrument: str) -> Callable:
        def action():
            self.led_strip.feedback_off(instrument=instrument)
        return action

    def hook_sensors(self) -> None:
        existing_channels = self.player.get_existing_channels()
        for instrument in self.hall:
            channel = self.channel_config[instrument]
            if existing_channels[channel]:
                self.hall[instrument].when_activated = self.__existing_hall_on(channel, instrument)
                self.hall[instrument].when_deactivated = self.__existing_hall_off(channel, instrument)
            else:
                self.hall[instrument].when_activated = self.__non_existing_hall_on(instrument)
                self.hall[instrument].when_deactivated = self.__non_existing_hall_off(instrument)

