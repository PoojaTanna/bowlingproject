"""
test_game.py - Unit tests for BowlingGame class
"""

import pytest
from game import BowlingGame

# -------------------------------
# Helper Functions
# -------------------------------
def roll_multiple(game, times, pins):
    """Roll the same number of pins multiple times."""
    for _ in range(times):
        game.roll(pins)

def roll_spare(game):
    """Roll a spare (5 + 5)."""
    game.roll(5)
    game.roll(5)

def roll_strike(game):
    """Roll a strike (10)."""
    game.roll(10)

# -------------------------------
# Test Cases
# -------------------------------

def test_all_gutters():
    """All rolls knock down 0 pins."""
    game = BowlingGame()
    roll_multiple(game, 20, 0)
    assert game.score() == 0

def test_all_ones():
    """All rolls knock down 1 pin."""
    game = BowlingGame()
    roll_multiple(game, 20, 1)
    assert game.score() == 20

def test_one_spare():
    """Score a spare and the next roll counts as bonus."""
    game = BowlingGame()
    roll_spare(game)
    game.roll(3)
    roll_multiple(game, 17, 0)
    assert game.score() == 16

def test_one_strike():
    """Score a strike and the next two rolls count as bonus."""
    game = BowlingGame()
    roll_strike(game)
    game.roll(3)
    game.roll(4)
    roll_multiple(game, 16, 0)
    assert game.score() == 24

def test_perfect_game():
    """Perfect game: 12 strikes, 300 points."""
    game = BowlingGame()
    roll_multiple(game, 12, 10)
    assert game.score() == 300

def test_10th_frame_spare_bonus():
    """Spare in 10th frame allows one bonus roll."""
    game = BowlingGame()
    roll_multiple(game, 18, 0)
    roll_spare(game)
    game.roll(7)
    assert game.score() == 17

def test_10th_frame_strike_bonus():
    """Strike in 10th frame allows two bonus rolls."""
    game = BowlingGame()
    roll_multiple(game, 18, 0)
    roll_strike(game)
    game.roll(7)
    game.roll(2)
    assert game.score() == 19

def test_no_roll_after_game_finished():
    """Cannot roll after the game is completed."""
    game = BowlingGame()
    roll_multiple(game, 12, 10)
    with pytest.raises(ValueError):
        game.roll(10)

def test_invalid_roll_negative():
    """Rolling negative pins raises ValueError."""
    game = BowlingGame()
    with pytest.raises(ValueError):
        game.roll(-1)

def test_invalid_roll_too_many_pins():
    """Rolling more than 10 pins raises ValueError."""
    game = BowlingGame()
    with pytest.raises(ValueError):
        game.roll(11)
