from typing import Dict, Callable

from gpiozero import DigitalInputDevice

from game.player import Player


class Dashboard:

    def __init__(self, player: Player, hall_config: Dict[str, int], channel_config: Dict[str, int], neopixel: int):
        self.player = player
        self.channel_config = channel_config
        self.neopixel = neopixel
        self.hall = {k: DigitalInputDevice(pin=v, pull_up=True) for k, v in hall_config.items()}

    def __existing_hall_on(self, channel: int) -> Callable:
        def action():
            self.player.active_channels[channel] = True
            # TODO green led on
        return action

    def __existing_hall_off(self, channel: int) -> Callable:
        def action():
            self.player.active_channels[channel] = False
            # TODO green led off
        return action

    def __non_existing_hall_on(self, channel: int) -> Callable:
        def action():
            # TODO red led on
            pass
        return action

    def __non_existing_hall_off(self, channel: int) -> Callable:
        def action():
            # TODO red led off
            pass
        return action

    def hook_sensors(self) -> None:
        existing_channels = self.player.get_existing_channels()
        for k in self.hall:
            channel = self.channel_config[k]
            if existing_channels[channel]:
                self.hall[k].when_activated = self.__existing_hall_on(channel)
                self.hall[k].when_deactivated = self.__existing_hall_off(channel)
            else:
                self.hall[k].when_activated = self.__non_existing_hall_on(channel)
                self.hall[k].when_deactivated = self.__non_existing_hall_off(channel)

