from serial import Serial
from serial.serialutil import SerialException


class SerialCommunication:
    """Classe che si occupa di inviare comandi tramite comunicazione seriale.
    """

    def __init__(self):
        """Inizializza la comunicazione sulla prima porta seriale disponibile.
        """
        port = 0
        ser = None
        while ser is None:
            try:
                ser = Serial(f'/dev/ttyACM{port}', 9600, timeout=1)
            except (FileNotFoundError, SerialException) as e:
                if port < 10:
                    port += 1
                else:
                    raise e
        self.ser = ser
        self.ser.flush()

    def led_do(self, instrument: str, state: bool, color: str) -> None:
        """Invia un messaggio per l'esecuzione di un'azione dei led. 
        
        Args:
            instrument: stringa che rappresenta lo strumento selezionato.
            state: booleano che indica lo stato dei led (on/off).
            color: stringa che rappresenta il colore di accensione dei led.

        Returns:
            None
        """""
        self.ser.write(f'(led,{instrument},{int(state)},{color})'.encode())

    def animation_do(self, name: str) -> None:
        """Invia un messaggio per l'esecuzione di un'animazione.

        Args:
            name: stringa che identifica l'animazione.

        Returns:
            None
        """
        self.ser.write(f'(animation,{name})'.encode())

    def servo_do(self, name: str) -> None:
        """Invia un messaggio per l'esecuzione di un movimento del servomotore.

        Args:
            name: stringa che identifica il movimento.

        Returns:
            None
        """
        self.ser.write(f'(servo,{name})'.encode())
