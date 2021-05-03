from typing import Dict, Callable, List

from gpiozero import DigitalInputDevice, RGBLED

from game.player import Player


class Dashboard:

    def __init__(
            self,
            player: Player,
            hall_config: Dict[str, int],
            channel_config: Dict[str, int],
            led_config: Dict[str, List[int]]):
        self.player = player
        self.channel_config = channel_config
        self.hall = {k: DigitalInputDevice(pin=v, pull_up=True) for k, v in hall_config.items()}
        self.led = {
            k: RGBLED(red=v[0], green=v[1], blue=4, active_high=False, pwm=False)
            for k, v in led_config.items()
        }

    def __existing_hall_on(self, channel: int, instrument: str) -> Callable:
        def action():
            self.player.active_channels[channel] = True
            self.led[instrument].value = (0, 1, 0)
        return action

    def __existing_hall_off(self, channel: int, instrument: str) -> Callable:
        def action():
            self.player.active_channels[channel] = False
            self.led[instrument].off()
        return action

    def __non_existing_hall_on(self, instrument: str) -> Callable:
        def action():
            self.led[instrument].value = (1, 0, 0)
            pass
        return action

    def __non_existing_hall_off(self, instrument: str) -> Callable:
        def action():
            self.led[instrument].off()
            pass
        return action

    def hook_sensors(self) -> None:
        existing_channels = self.player.get_existing_channels()
        for inst in self.hall:
            channel = self.channel_config[inst]
            if existing_channels[channel]:
                self.hall[inst].when_activated = self.__existing_hall_on(channel, inst)
                self.hall[inst].when_deactivated = self.__existing_hall_off(channel, inst)
            else:
                self.hall[inst].when_activated = self.__non_existing_hall_on(inst)
                self.hall[inst].when_deactivated = self.__non_existing_hall_off(inst)

