# game.py

class BowlingGame:
    def __init__(self):
        self.rolls = []

    def roll(self, pins: int):
        """Record a roll. Raise ValueError if invalid pins or game finished."""
        if pins < 0 or pins > 10:
            raise ValueError("Pins must be between 0 and 10")
        if self.is_finished():
            raise ValueError("Game already finished")
        self.rolls.append(pins)

    def score(self):
        """Calculate total score for the game."""
        result = 0
        roll_index = 0
        for frame in range(10):
            if self.is_strike(roll_index):
                result += 10 + self.rolls[roll_index + 1] + self.rolls[roll_index + 2]
                roll_index += 1
            elif self.is_spare(roll_index):
                result += 10 + self.rolls[roll_index + 2]
                roll_index += 2
            else:
                result += self.rolls[roll_index] + self.rolls[roll_index + 1]
                roll_index += 2
        return result

    def is_strike(self, roll_index):
        return self.rolls[roll_index] == 10

    def is_spare(self, roll_index):
        return self.rolls[roll_index] + self.rolls[roll_index + 1] == 10

    def is_finished(self):
        """Check if the game is finished."""
        roll_index = 0
        for frame in range(9):  # first 9 frames
            if roll_index >= len(self.rolls):
                return False
            if self.rolls[roll_index] == 10:  # strike
                roll_index += 1
            else:
                roll_index += 2

        # 10th frame
        if len(self.rolls) <= roll_index:
            return False

        first = self.rolls[roll_index]
        second = self.rolls[roll_index + 1] if len(self.rolls) > roll_index + 1 else None

        # Strike in 10th frame
        if first == 10:
            return len(self.rolls) >= roll_index + 3
        # Spare in 10th frame
        if second is not None and first + second == 10:
            return len(self.rolls) >= roll_index + 3
        # Normal 10th frame
        return second is not None
