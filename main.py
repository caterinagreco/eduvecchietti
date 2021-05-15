import json
from argparse import ArgumentParser
import serial
from game.game import Game

if __name__ == "__main__":
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
    parser = ArgumentParser(description='Play the game with no name.')
    parser.add_argument('config', type=str, help='Path to the config file.')
    args = parser.parse_args()
    with open(args.config, 'r') as f:
        config = json.load(f)
    game = Game(config=config)
    game.configure()
    game.start()
