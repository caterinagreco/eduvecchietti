from typing import Dict, Callable

from gpiozero import DigitalInputDevice

from game.player import Player
from game.serial_communication import SerialCommunication


class Dashboard:
    def __init__(
            self,
            player: Player,
            serial: SerialCommunication,
            hall_config: Dict[str, int],
            channel_config: Dict[str, int],):
        self.player = player
        self.channel_config = channel_config
        self.hall = {k: DigitalInputDevice(pin=v, pull_up=True) for k, v in hall_config.items()}
        self.serial = serial

    def victory(self):
        self.serial.animation_do('victory')
        self.serial.servo_do('victory')

    def __existing_hall_on(self, channel: int, instrument: str) -> Callable:
        def action():
            self.player.active_channels[channel] = True
            self.serial.led_do(instrument, True, 'green')
            self.serial.servo_do('correct')
            if self.player.active_channels == self.player.existing_channels:
                self.victory()
        return action

    def __existing_hall_off(self, channel: int, instrument: str) -> Callable:
        def action():
            self.player.active_channels[channel] = False
            self.serial.led_do(instrument, False, 'green')
        return action

    def __non_existing_hall_on(self, channel: int, instrument: str) -> Callable:
        def action():
            self.player.active_channels[channel] = True
            self.serial.led_do(instrument, True, 'red')
        return action

    def __non_existing_hall_off(self, channel: int, instrument: str) -> Callable:
        def action():
            self.player.active_channels[channel] = False
            self.serial.led_do(instrument, False, 'red')
            if self.player.active_channels == self.player.existing_channels:
                self.victory()
        return action

    def hook_sensors(self) -> None:
        for instrument in self.hall:
            channel = self.channel_config[instrument]
            if self.player.existing_channels[channel]:
                self.hall[instrument].when_activated = self.__existing_hall_on(channel, instrument)
                self.hall[instrument].when_deactivated = self.__existing_hall_off(channel, instrument)
            else:
                self.hall[instrument].when_activated = self.__non_existing_hall_on(channel, instrument)
                self.hall[instrument].when_deactivated = self.__non_existing_hall_off(channel, instrument)

