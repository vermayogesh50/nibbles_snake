"""Basic tests for game rules that do not need a Pygame window."""

import random
import unittest

from game_logic import is_opposite_direction, lose_life, move_snake, place_food


class GameLogicTests(unittest.TestCase):
    def test_move_forward_keeps_snake_length(self):
        snake = [(2, 2), (1, 2), (0, 2)]

        moved_snake, ate_food, collided = move_snake(
            snake, (1, 0), (5, 5), 8, 8
        )

        self.assertEqual(moved_snake, [(3, 2), (2, 2), (1, 2)])
        self.assertFalse(ate_food)
        self.assertFalse(collided)

    def test_eating_food_grows_snake(self):
        snake = [(2, 2), (1, 2)]

        moved_snake, ate_food, collided = move_snake(
            snake, (1, 0), (3, 2), 8, 8
        )

        self.assertEqual(moved_snake, [(3, 2), (2, 2), (1, 2)])
        self.assertTrue(ate_food)
        self.assertFalse(collided)

    def test_wall_and_body_collisions(self):
        snake = [(0, 2), (1, 2)]
        _, _, wall_collision = move_snake(snake, (-1, 0), None, 8, 8)
        self.assertTrue(wall_collision)

        turning_snake = [(2, 2), (2, 3), (1, 3), (1, 2), (0, 2)]
        _, _, body_collision = move_snake(
            turning_snake, (-1, 0), None, 8, 8
        )
        self.assertTrue(body_collision)

    def test_moving_into_vacating_tail_is_allowed(self):
        snake = [(2, 2), (2, 3), (1, 3), (1, 2)]

        moved_snake, ate_food, collided = move_snake(
            snake, (-1, 0), None, 8, 8
        )

        self.assertEqual(moved_snake[0], (1, 2))
        self.assertFalse(ate_food)
        self.assertFalse(collided)

    def test_opposite_directions(self):
        self.assertTrue(is_opposite_direction((1, 0), (-1, 0)))
        self.assertFalse(is_opposite_direction((1, 0), (0, -1)))

    def test_three_lives_are_used_before_game_over(self):
        lives = 3

        lives, game_over = lose_life(lives)
        self.assertEqual(lives, 2)
        self.assertFalse(game_over)

        lives, game_over = lose_life(lives)
        self.assertEqual(lives, 1)
        self.assertFalse(game_over)

        lives, game_over = lose_life(lives)
        self.assertEqual(lives, 0)
        self.assertTrue(game_over)

    def test_food_is_empty_and_none_when_board_is_full(self):
        snake = [(0, 0), (1, 0), (0, 1)]
        food = place_food(snake, 2, 2, random.Random(1))
        self.assertNotIn(food, snake)
        self.assertIsNone(place_food([(0, 0), (1, 0)], 2, 1))


if __name__ == "__main__":
    unittest.main()
