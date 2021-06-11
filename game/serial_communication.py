from serial import Serial
from serial.serialutil import SerialException


class SerialCommunication:

    def __init__(self):
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

    def led_do(self, instrument: str, state: bool, color: str):
        self.ser.write(f'(led,{instrument},{int(state)},{color})'.encode())

    def animation_do(self, name: str):
        self.ser.write(f'(animation,{name})'.encode())

    def servo_do(self, name: str):
        self.ser.write(f'(servo,{name})'.encode())
