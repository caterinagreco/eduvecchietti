import json

from game.game import Game

if __name__ == "__main__":
    config_path = 'config.mac.json'
    with open(config_path, 'r') as f:
        config = json.load(f)
    game = Game(config=config)
    game.configure()
    game.player.active_channels = game.player.get_existing_channels()
    game.start()
