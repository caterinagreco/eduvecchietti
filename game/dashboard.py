from typing import Dict, Callable

from gpiozero import DigitalInputDevice

from game.player import Player
import serial

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)


class Dashboard:
    def __init__(
            self,
            player: Player,
            hall_config: Dict[str, int],
            channel_config: Dict[str, int],):
        self.player = player
        self.channel_config = channel_config
        self.hall = {k: DigitalInputDevice(pin=v, pull_up=True) for k, v in hall_config.items()}


    def __existing_hall_on(self, channel: int, instrument: str) -> Callable:
        def action():
            self.player.active_channels[channel] = True
            ser.write(f'(led,{instrument},1,verde)')
        return action

    def __existing_hall_off(self, channel: int, instrument: str) -> Callable:
        def action():
            self.player.active_channels[channel] = False
            ser.write(f'(led,{instrument},0,verde)')
        return action

    def __non_existing_hall_on(self, instrument: str) -> Callable:
        def action():
            ser.write(f'(led,{instrument},1,rosso)')
        return action

    def __non_existing_hall_off(self, instrument: str) -> Callable:
        def action():
            ser.write(f'(led,{instrument},0,rosso)')
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

