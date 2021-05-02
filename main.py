import json
from argparse import ArgumentParser

from game.game import Game

if __name__ == "__main__":
    parser = ArgumentParser(description='Play the game with no name.')
    parser.add_argument('config', type=str, help='Path to the config file.')
    args = parser.parse_args()
    with open(args.config, 'r') as f:
        config = json.load(f)
    game = Game(config=config)
    game.configure()
    game.start()
