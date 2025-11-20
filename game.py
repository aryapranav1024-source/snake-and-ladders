import random

class SnakeAndLadderGame:
    def __init__(self, player_names):
        self.player_positions = {name: 0 for name in player_names}
        self.winner = None

        # Snakes and ladders mapping
        self.snakes = {
            99: 5,
            95: 75,
            92: 88,
            89: 68,
            74: 53,
            64: 60,
            62: 19
        }

        self.ladders = {
            3: 22,
            5: 8,
            11: 26,
            20: 29,
            27: 56,
            36: 55,
            50: 91,
        }

    def roll_dice(self):
        return random.randint(1, 6)

    def move_player(self, player):
        dice_value = self.roll_dice()
        current_position = self.player_positions[player]

        new_position = current_position + dice_value

        if new_position > 100:
            return dice_value, current_position  # can't move beyond 100

        # Check for snake or ladder
        final_position = self.snakes.get(new_position, self.ladders.get(new_position, new_position))

        self.player_positions[player] = final_position

        if final_position == 100:
            self.winner = player

        return dice_value, final_position
