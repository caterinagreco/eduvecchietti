from typing import Dict, Callable

from gpiozero import DigitalInputDevice

from game.player import Player
from game.serial_communication import SerialCommunication


class Dashboard:
    """Classe che gestisce gli elementi della plancia di gioco,
    legando le mosse del giocatore all'esecuzione della musica.
    """
    def __init__(
            self,
            player: Player,
            serial: SerialCommunication,
            hall_config: Dict[str, int],
            channel_config: Dict[str, int],):
        """Inizializza gli elementi della plancia di gioco sulla base della configurazione.

        Args:
            player: il player di cui controllare i canali attivi.
            serial: oggetto per la comunicazione seriale da utilizzare per inviare messaggi.
            hall_config: configurazione di corrispondenza tra sensori di Hall e strumenti.
            channel_config: configurazione di corrispondenza tra canali e strumenti.
        """
        self.player = player
        self.channel_config = channel_config
        self.hall = {k: DigitalInputDevice(pin=v, pull_up=True) for k, v in hall_config.items()}
        self.serial = serial

    def victory(self) -> None:
        """Esegue le azioni legate alla vittoria.

        Returns:
            None
        """
        self.serial.animation_do('victory')
        self.serial.servo_do('victory')

    def __existing_hall_on(self, channel: int, instrument: str) -> Callable:
        """Restituisce la funzione da chiamare in seguito all'attivazione di un sensore di Hall
        corrispondente ad un canale esistente nel player.

        Args:
            channel: il canale da attivare.
            instrument: stringa che identifica lo strumento corrispondente al sensore di Hall attivato.

        Returns:
            La funzione corrispondente all'attivazione di un canale esistente.
        """
        def action():
            self.player.active_channels[channel] = True
            self.serial.led_do(instrument, True, 'green')
            self.serial.servo_do('correct')
            if self.player.active_channels == self.player.existing_channels:
                self.victory()
        return action

    def __existing_hall_off(self, channel: int, instrument: str) -> Callable:
        """Restituisce la funzione da chiamare in seguito alla disattivazione di un sensore di Hall
        corrispondente ad un canale esistente nel player.

        Args:
            channel: il canale da disattivare.
            instrument: stringa che identifica lo strumento corrispondente al sensore di Hall disattivato.

        Returns:
            La funzione corrispondente alla disattivazione di un canale esistente.
        """
        def action():
            self.player.active_channels[channel] = False
            self.serial.led_do(instrument, False, 'green')
        return action

    def __non_existing_hall_on(self, channel: int, instrument: str) -> Callable:
        """Restituisce la funzione da chiamare in seguito all'attivazione di un sensore di Hall
        corrispondente ad un canale non esistente nel player.

        Args:
            channel: il canale da attivare.
            instrument: stringa che identifica lo strumento corrispondente al sensore di Hall attivato.

        Returns:
            La funzione corrispondente all'attivazione di un canale non esistente.
        """
        def action():
            self.player.active_channels[channel] = True
            self.serial.led_do(instrument, True, 'red')
        return action

    def __non_existing_hall_off(self, channel: int, instrument: str) -> Callable:
        """Restituisce la funzione da chiamare in seguito alla disattivazione di un sensore di Hall
            corrispondente ad un canale non esistente nel player.

        Args:
            channel: il canale da disattivare.
            instrument: stringa che identifica lo strumento corrispondente al sensore di Hall disattivato.

        Returns:
            La funzione corrispondente alla disattivazione di un canale non esistente.
        """
        def action():
            self.player.active_channels[channel] = False
            self.serial.led_do(instrument, False, 'red')
            if self.player.active_channels == self.player.existing_channels:
                self.victory()
        return action

    def reset(self) -> None:
        """Resetta la plancia disattivando le azioni legate all'attivazione/disattivazione dei sensori di Hall.

        Returns:
            None
        """
        for instrument in self.hall:
            self.hall[instrument].when_activated = None
            self.hall[instrument].when_deactivated = None

    def hook_sensors(self) -> None:
        """Collega ogni sensore di Hall alle azioni da eseguire per l'attivazione/disattivazione sulla base
        del canale corrispondente e della presenza/assenza di quest'ultimo nel player.

        Returns:
            None
        """
        for instrument in self.hall:
            channel = self.channel_config[instrument]
            if self.player.existing_channels[channel]:
                self.hall[instrument].when_activated = self.__existing_hall_on(channel, instrument)
                self.hall[instrument].when_deactivated = self.__existing_hall_off(channel, instrument)
            else:
                self.hall[instrument].when_activated = self.__non_existing_hall_on(channel, instrument)
                self.hall[instrument].when_deactivated = self.__non_existing_hall_off(channel, instrument)

