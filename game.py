"""A beginner-friendly Nibbles (Snake) game made with Pygame."""

import pygame

from game_logic import is_opposite_direction, lose_life, move_snake, place_food


CELL_SIZE = 20
GRID_COLUMNS = 32
GRID_ROWS = 24
WINDOW_WIDTH = GRID_COLUMNS * CELL_SIZE
WINDOW_HEIGHT = GRID_ROWS * CELL_SIZE
STARTING_LIVES = 3
DIFFICULTY_SETTINGS = {
    "easy": {"label": "Easy", "move_delay": 160},
    "medium": {"label": "Medium", "move_delay": 120},
    "hard": {"label": "Hard", "move_delay": 80},
}
DIFFICULTY_KEYS = {
    pygame.K_1: "easy",
    pygame.K_2: "medium",
    pygame.K_3: "hard",
}

BACKGROUND_COLOR = (24, 28, 36)
GRID_COLOR = (37, 43, 53)
SNAKE_COLOR = (57, 190, 96)
SNAKE_HEAD_COLOR = (77, 220, 112)
SNAKE_HIGHLIGHT = (166, 255, 181)
SNAKE_SHADOW = (15, 91, 43)
FOOD_COLOR = (224, 52, 52)
FOOD_HIGHLIGHT = (255, 166, 125)
FOOD_SHADOW = (119, 26, 34)
TEXT_COLOR = (240, 240, 240)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def create_starting_snake():
    """Return the snake's starting position and length."""
    return [
        (GRID_COLUMNS // 2, GRID_ROWS // 2),
        (GRID_COLUMNS // 2 - 1, GRID_ROWS // 2),
        (GRID_COLUMNS // 2 - 2, GRID_ROWS // 2),
    ]


def create_new_game(difficulty):
    """Return the starting snake, direction, food, score, and game state."""
    starting_snake = create_starting_snake()
    return {
        "snake": starting_snake,
        "direction": RIGHT,
        "next_direction": RIGHT,
        "food": place_food(starting_snake, GRID_COLUMNS, GRID_ROWS),
        "score": 0,
        "lives": STARTING_LIVES,
        "difficulty": difficulty,
        "move_delay": DIFFICULTY_SETTINGS[difficulty]["move_delay"],
        "game_over": False,
        "won": False,
    }


def draw_grid(screen):
    """Draw subtle lines to make the movement grid easy to see."""
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))


def draw_3d_block(screen, rectangle, color, highlight, shadow):
    """Draw a beveled block with a soft shadow to suggest depth."""
    pygame.draw.rect(
        screen,
        (8, 11, 16),
        rectangle.move(2, 3),
        border_radius=5,
    )
    pygame.draw.rect(screen, shadow, rectangle, border_radius=5)

    face = rectangle.inflate(-2, -2)
    pygame.draw.rect(screen, color, face, border_radius=4)
    pygame.draw.line(
        screen,
        highlight,
        (face.left + 4, face.top + 1),
        (face.right - 4, face.top + 1),
        2,
    )
    pygame.draw.line(
        screen,
        highlight,
        (face.left + 1, face.top + 4),
        (face.left + 1, face.bottom - 4),
        2,
    )
    pygame.draw.line(
        screen,
        shadow,
        (face.right - 1, face.top + 4),
        (face.right - 1, face.bottom - 4),
        2,
    )
    pygame.draw.line(
        screen,
        shadow,
        (face.left + 4, face.bottom - 1),
        (face.right - 4, face.bottom - 1),
        2,
    )


def draw_snake_eyes(screen, rectangle, direction):
    """Draw eyes on the front of the snake's head, facing its direction."""
    eye_positions = {
        RIGHT: ((0.68, 0.30), (0.68, 0.70)),
        LEFT: ((0.32, 0.30), (0.32, 0.70)),
        UP: ((0.30, 0.32), (0.70, 0.32)),
        DOWN: ((0.30, 0.68), (0.70, 0.68)),
    }
    pupil_offsets = {
        RIGHT: (1, 0),
        LEFT: (-1, 0),
        UP: (0, -1),
        DOWN: (0, 1),
    }
    pupil_offset = pupil_offsets[direction]

    for x_fraction, y_fraction in eye_positions[direction]:
        eye_center = (
            rectangle.left + int(rectangle.width * x_fraction),
            rectangle.top + int(rectangle.height * y_fraction),
        )
        pygame.draw.circle(screen, (245, 250, 245), eye_center, 2)
        pupil_center = (
            eye_center[0] + pupil_offset[0],
            eye_center[1] + pupil_offset[1],
        )
        pygame.draw.circle(screen, (18, 30, 24), pupil_center, 1)


def draw_game(screen, font, state):
    """Draw the play area, snake, food, score, and any end-of-game message."""
    screen.fill(BACKGROUND_COLOR)
    draw_grid(screen)

    for head, body_part in zip(state["snake"], state["snake"][1:]):
        head_center = (
            head[0] * CELL_SIZE + CELL_SIZE // 2,
            head[1] * CELL_SIZE + CELL_SIZE // 2,
        )
        body_center = (
            body_part[0] * CELL_SIZE + CELL_SIZE // 2,
            body_part[1] * CELL_SIZE + CELL_SIZE // 2,
        )
        pygame.draw.line(
            screen,
            (8, 11, 16),
            (head_center[0] + 2, head_center[1] + 3),
            (body_center[0] + 2, body_center[1] + 3),
            CELL_SIZE - 6,
        )
        pygame.draw.line(
            screen,
            SNAKE_COLOR,
            head_center,
            body_center,
            CELL_SIZE - 8,
        )

    for index, segment in enumerate(state["snake"]):
        rectangle = pygame.Rect(
            segment[0] * CELL_SIZE + 1,
            segment[1] * CELL_SIZE + 1,
            CELL_SIZE - 2,
            CELL_SIZE - 2,
        )
        is_head = index == 0
        draw_3d_block(
            screen,
            rectangle,
            SNAKE_HEAD_COLOR if is_head else SNAKE_COLOR,
            SNAKE_HIGHLIGHT,
            SNAKE_SHADOW,
        )
        if is_head:
            draw_snake_eyes(screen, rectangle, state["direction"])

    if state["food"] is not None:
        food_rectangle = pygame.Rect(
            state["food"][0] * CELL_SIZE + 3,
            state["food"][1] * CELL_SIZE + 3,
            CELL_SIZE - 7,
            CELL_SIZE - 7,
        )
        draw_3d_block(
            screen,
            food_rectangle,
            FOOD_COLOR,
            FOOD_HIGHLIGHT,
            FOOD_SHADOW,
        )

    score_surface = font.render(f"Score: {state['score']}", True, TEXT_COLOR)
    screen.blit(score_surface, (10, 8))
    lives_surface = font.render(f"Lives: {state['lives']}", True, TEXT_COLOR)
    screen.blit(lives_surface, (145, 8))
    difficulty_label = DIFFICULTY_SETTINGS[state["difficulty"]]["label"]
    difficulty_surface = font.render(
        f"Difficulty: {difficulty_label}", True, TEXT_COLOR
    )
    screen.blit(difficulty_surface, (265, 8))

    if state["game_over"]:
        if state["won"]:
            message = f"You win! Final score: {state['score']}"
        else:
            message = f"Game over! Final score: {state['score']}"
        message_surface = font.render(message, True, TEXT_COLOR)
        restart_surface = font.render("Press R or Enter to try again", True, TEXT_COLOR)
        menu_surface = font.render("Press M to choose a difficulty", True, TEXT_COLOR)
        message_rectangle = message_surface.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 32)
        )
        restart_rectangle = restart_surface.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 4)
        )
        menu_rectangle = menu_surface.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40)
        )
        pygame.draw.rect(
            screen,
            BACKGROUND_COLOR,
            pygame.Rect(70, WINDOW_HEIGHT // 2 - 65, WINDOW_WIDTH - 140, 130),
            border_radius=8,
        )
        screen.blit(message_surface, message_rectangle)
        screen.blit(restart_surface, restart_rectangle)
        screen.blit(menu_surface, menu_rectangle)

    pygame.display.flip()


def draw_difficulty_selection(screen, font):
    """Draw the screen where the player chooses a difficulty."""
    screen.fill(BACKGROUND_COLOR)
    title_font = pygame.font.Font(None, 56)
    title_surface = title_font.render("Nibbles - Snake", True, SNAKE_COLOR)
    title_rectangle = title_surface.get_rect(
        center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 90)
    )
    screen.blit(title_surface, title_rectangle)

    instruction_surface = font.render("Choose a difficulty:", True, TEXT_COLOR)
    instruction_rectangle = instruction_surface.get_rect(
        center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30)
    )
    screen.blit(instruction_surface, instruction_rectangle)

    choices = ("1 - Easy", "2 - Medium", "3 - Hard")
    for index, choice in enumerate(choices):
        choice_surface = font.render(choice, True, TEXT_COLOR)
        choice_rectangle = choice_surface.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10 + index * 36)
        )
        screen.blit(choice_surface, choice_rectangle)

    help_surface = font.render(
        "You have 3 lives. Each collision uses one life.", True, TEXT_COLOR
    )
    help_rectangle = help_surface.get_rect(
        center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 135)
    )
    screen.blit(help_surface, help_rectangle)
    pygame.display.flip()


def handle_direction_key(key, state):
    """Queue a turn, ignoring a direction that would reverse into the snake."""
    key_directions = {
        pygame.K_UP: UP,
        pygame.K_DOWN: DOWN,
        pygame.K_LEFT: LEFT,
        pygame.K_RIGHT: RIGHT,
    }
    new_direction = key_directions.get(key)
    if new_direction is not None and not is_opposite_direction(
        new_direction, state["direction"]
    ):
        state["next_direction"] = new_direction


def update_game(state):
    """Advance the snake by one cell and update food, score, and end state."""
    state["direction"] = state["next_direction"]
    snake, ate_food, collided = move_snake(
        state["snake"],
        state["direction"],
        state["food"],
        GRID_COLUMNS,
        GRID_ROWS,
    )
    if collided:
        state["lives"], state["game_over"] = lose_life(state["lives"])
        if not state["game_over"]:
            # A new attempt starts with a fresh snake but keeps the score.
            state["snake"] = create_starting_snake()
            state["direction"] = RIGHT
            state["next_direction"] = RIGHT
            state["food"] = place_food(
                state["snake"], GRID_COLUMNS, GRID_ROWS
            )
        return

    state["snake"] = snake
    if ate_food:
        state["score"] += 1
        state["food"] = place_food(snake, GRID_COLUMNS, GRID_ROWS)
        if state["food"] is None:
            state["game_over"] = True
            state["won"] = True


def main():
    """Start the game window and run the event loop."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Nibbles - Snake")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)
    state = None
    time_since_move = 0
    running = True

    while running:
        elapsed_time = clock.tick(60)
        time_since_move += elapsed_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if state is None:
                    difficulty = DIFFICULTY_KEYS.get(event.key)
                    if difficulty is not None:
                        state = create_new_game(difficulty)
                        time_since_move = 0
                elif state["game_over"] and event.key in (
                    pygame.K_r,
                    pygame.K_RETURN,
                ):
                    state = create_new_game(state["difficulty"])
                    time_since_move = 0
                elif state["game_over"] and event.key == pygame.K_m:
                    state = None
                    time_since_move = 0
                elif not state["game_over"]:
                    handle_direction_key(event.key, state)

        if (
            state is not None
            and not state["game_over"]
            and time_since_move >= state["move_delay"]
        ):
            update_game(state)
            time_since_move = 0

        if state is None:
            draw_difficulty_selection(screen, font)
        else:
            draw_game(screen, font, state)

    pygame.quit()


if __name__ == "__main__":
    main()
