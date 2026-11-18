"""Small, testable functions for the Nibbles game."""

import random


def is_opposite_direction(first, second):
    """Return whether two (x, y) directions point directly opposite ways."""
    return first[0] == -second[0] and first[1] == -second[1]


def lose_life(lives):
    """Return the remaining lives and whether the game should end."""
    remaining_lives = max(0, lives - 1)
    return remaining_lives, remaining_lives == 0


def move_snake(snake, direction, food, columns, rows):
    """Move the snake one grid space.

    The snake is a list of (column, row) positions, with its head first.
    Returns the new snake, whether food was eaten, and whether a collision
    occurred. A move into the old tail position is allowed if the snake is
    not growing, because that tail moves away during the same turn.
    """
    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])
    ate_food = new_head == food

    if not (0 <= new_head[0] < columns and 0 <= new_head[1] < rows):
        return snake, False, True

    body_to_check = snake if ate_food else snake[:-1]
    if new_head in body_to_check:
        return snake, False, True

    new_snake = [new_head] + snake
    if not ate_food:
        new_snake.pop()

    return new_snake, ate_food, False


def place_food(snake, columns, rows, rng=None):
    """Choose an unoccupied grid position, or return None if the board is full."""
    if rng is None:
        rng = random

    empty_positions = [
        (column, row)
        for column in range(columns)
        for row in range(rows)
        if (column, row) not in snake
    ]
    if not empty_positions:
        return None
    return rng.choice(empty_positions)
