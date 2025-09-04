import pytest
from game import BowlingGame

# Helper to roll multiple times
def roll_many(game, rolls, pins):
    for _ in range(rolls):
        game.roll(pins)

# Helper to roll a spare
def roll_spare(game):
    game.roll(5)
    game.roll(5)

# Helper to roll a strike
def roll_strike(game):
    game.roll(10)

# -------------------------------
# TEST CASES
# -------------------------------

def test_all_gutters():
    """All rolls are 0 pins."""
    game = BowlingGame()
    roll_many(game, 20, 0)
    assert game.score() == 0

def test_all_ones():
    """All rolls are 1 pin."""
    game = BowlingGame()
    roll_many(game, 20, 1)
    assert game.score() == 20

def test_one_spare():
    """Score a spare and a following roll."""
    game = BowlingGame()
    roll_spare(game)   # 5+5
    game.roll(3)       # bonus
    roll_many(game, 17, 0)
    assert game.score() == 16

def test_one_strike():
    """Score a strike and next two rolls as bonus."""
    game = BowlingGame()
    roll_strike(game)  # 10
    game.roll(3)
    game.roll(4)
    roll_many(game, 16, 0)
    assert game.score() == 24

def test_perfect_game():
    """Perfect game: 12 strikes, 300 points."""
    game = BowlingGame()
    roll_many(game, 12, 10)
    assert game.score() == 300

def test_10th_frame_spare_bonus():
    """Spare in 10th frame allows one bonus roll."""
    game = BowlingGame()
    roll_many(game, 18, 0)  # first 9 frames zeros
    roll_spare(game)         # 10th frame spare
    game.roll(7)             # bonus
    assert game.score() == 17

def test_10th_frame_strike_bonus():
    """Strike in 10th frame allows two bonus rolls."""
    game = BowlingGame()
    roll_many(game, 18, 0)
    roll_strike(game)        # 10th frame strike
    game.roll(7)
    game.roll(2)
    assert game.score() == 19

def test_no_roll_after_finished_game():
    """Cannot roll after game is finished."""
    game = BowlingGame()
    roll_many(game, 12, 10)  # perfect game
    with pytest.raises(ValueError):
        game.roll(10)

def test_invalid_roll_negative():
    """Cannot roll negative pins."""
    game = BowlingGame()
    with pytest.raises(ValueError):
        game.roll(-1)

def test_invalid_roll_too_many_pins():
    """Cannot roll more than 10 pins."""
    game = BowlingGame()
    with pytest.raises(ValueError):
        game.roll(11)
