from serial import Serial


class SerialCommunication:

    def __init__(self):
        self.ser = Serial('/dev/ttyACM0', 9600, timeout=1)
        self.ser.flush()

    def led_do(self, instrument: str, state: bool, color: str):
        self.ser.write(f'(led,{instrument},{int(state)},{color})'.encode())

    def animation_do(self, name: str):
        self.ser.write(f'(animation,{name})'.encode())

    def servo_do(self, name: str):
        self.ser.write(f'servo,{name}'.encode())
