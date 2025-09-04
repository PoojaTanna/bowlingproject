"""
game.py - Bowling game backend implementation
"""

class BowlingGame:
    """
    A class to represent a 10-pin bowling game.

    Attributes
    ----------
    rolls : list
        Stores the number of pins knocked down in each roll.

    Methods
    -------
    roll(pins)
        Records a roll. Raises ValueError if pins are invalid or game is finished.
    score()
        Calculates the total score of the game.
    is_finished()
        Checks if the game is finished.
    """

    def __init__(self):
        """Initialize a new bowling game with an empty roll list."""
        self.rolls = []

    def roll(self, pins: int):
        """
        Record a roll.

        Parameters
        ----------
        pins : int
            Number of pins knocked down in the roll.

        Raises
        ------
        ValueError
            If pins < 0, pins > 10, or game is already finished.
        """
        if not 0 <= pins <= 10:
            raise ValueError("Pins must be between 0 and 10")
        if self.is_finished():
            raise ValueError("Game already finished")
        self.rolls.append(pins)

    def score(self):
        """
        Calculate the total score for the game.

        Returns
        -------
        int
            Total score according to standard 10-pin bowling rules.
        """
        total_score = 0
        roll_index = 0

        for frame in range(10):
            if self._is_strike(roll_index):
                total_score += 10 + self._strike_bonus(roll_index)
                roll_index += 1
            elif self._is_spare(roll_index):
                total_score += 10 + self._spare_bonus(roll_index)
                roll_index += 2
            else:
                total_score += self._frame_score(roll_index)
                roll_index += 2

        return total_score

    # -------------------------------
    # Internal Helper Methods
    # -------------------------------
    def _is_strike(self, roll_index):
        """Check if roll at index is a strike."""
        return self.rolls[roll_index] == 10

    def _is_spare(self, roll_index):
        """Check if frame at roll_index is a spare."""
        return self.rolls[roll_index] + self.rolls[roll_index + 1] == 10

    def _strike_bonus(self, roll_index):
        """Calculate strike bonus for the next two rolls."""
        return self.rolls[roll_index + 1] + self.rolls[roll_index + 2]

    def _spare_bonus(self, roll_index):
        """Calculate spare bonus for the next roll."""
        return self.rolls[roll_index + 2]

    def _frame_score(self, roll_index):
        """Return the score for a frame without spare or strike."""
        return self.rolls[roll_index] + self.rolls[roll_index + 1]

    def is_finished(self):
        """
        Check if the game is finished.

        Returns
        -------
        bool
            True if the game is finished, False otherwise.
        """
        roll_index = 0

        # First 9 frames
        for frame in range(9):
            if roll_index >= len(self.rolls):
                return False
            roll_index += 1 if self.rolls[roll_index] == 10 else 2

        # 10th frame
        if len(self.rolls) <= roll_index:
            return False

        first = self.rolls[roll_index]
        second = self.rolls[roll_index + 1] if len(self.rolls) > roll_index + 1 else None

        if first == 10:  # Strike in 10th frame
            return len(self.rolls) >= roll_index + 3
        if second is not None and first + second == 10:  # Spare in 10th frame
            return len(self.rolls) >= roll_index + 3
        return second is not None  # Normal 10th frame
