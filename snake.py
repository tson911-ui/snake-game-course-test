"""
Retro Snake Game in Python
Built with Pygame.

Features:
- Smooth grid movement with input buffering (no accidental self-collisions)
- Easy / Normal / Hard difficulty selection
- Score and High Score tracking (persisted to highscore.txt)
- Animated snake eyes facing movement direction
- Normal apples + Bonus golden apples
- Pause / Resume (Space) and Quick Restart (R)
- Support for Arrow Keys and WASD
"""

import sys
import os
import random
import pygame

# -------------------------------------------------------------
# CONSTANTS & CONFIGURATION
# -------------------------------------------------------------
CELL_SIZE = 25            # Size of each grid square in pixels
GRID_WIDTH = 32           # 32 columns (32 * 25 = 800 px)
GRID_HEIGHT = 22          # 22 rows (22 * 25 = 550 px)
TOP_BAR_HEIGHT = 50       # Space for score and status header

SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH     # 800 px
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT + TOP_BAR_HEIGHT  # 600 px

# Color Palette (Modern Retro / Arcade)
COLOR_BG_DARK = (18, 22, 32)
COLOR_BG_LIGHT = (24, 30, 42)
COLOR_HEADER_BG = (12, 15, 22)
COLOR_BORDER = (45, 55, 72)

COLOR_SNAKE_HEAD = (46, 204, 113)
COLOR_SNAKE_BODY = (39, 174, 96)
COLOR_SNAKE_OUTLINE = (30, 132, 73)
COLOR_EYE_WHITE = (255, 255, 255)
COLOR_EYE_PUPIL = (20, 20, 20)

COLOR_FOOD_RED = (231, 76, 60)
COLOR_FOOD_LEAF = (46, 204, 113)
COLOR_GOLDEN_APPLE = (241, 196, 15)

COLOR_TEXT_PRIMARY = (240, 243, 246)
COLOR_TEXT_MUTED = (160, 174, 192)
COLOR_ACCENT = (241, 196, 15)
COLOR_OVERLAY = (0, 0, 0, 180)

# Difficulty settings (Frames Per Second)
DIFFICULTIES = {
    "EASY": {"speed": 8, "name": "Easy (Casual)"},
    "NORMAL": {"speed": 12, "name": "Normal (Standard)"},
    "HARD": {"speed": 18, "name": "Hard (Fast)"}
}

HIGHSCORE_FILE = os.path.join(os.path.dirname(__file__), "highscore.txt")


# -------------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------------
def load_high_score():
    """Load high score from a local text file."""
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                return int(f.read().strip())
        except (ValueError, OSError):
            return 0
    return 0


def save_high_score(score):
    """Save high score to a local text file."""
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(score))
    except OSError:
        pass


# -------------------------------------------------------------
# MAIN GAME CLASS
# -------------------------------------------------------------
class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Classic Snake Game")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        # Fonts
        self.font_title = pygame.font.SysFont("arial", 32, bold=True)
        self.font_ui = pygame.font.SysFont("arial", 20, bold=True)
        self.font_sub = pygame.font.SysFont("arial", 16)

        self.difficulty_key = "NORMAL"
        self.high_score = load_high_score()
        self.state = "MENU"   # "MENU", "PLAYING", "PAUSED", "GAMEOVER"

        self.reset_game()

    def reset_game(self):
        """Initialize or reset snake and food positions."""
        mid_x = GRID_WIDTH // 2
        mid_y = GRID_HEIGHT // 2

        # Snake body represented as list of (grid_x, grid_y)
        self.snake = [
            (mid_x, mid_y),
            (mid_x - 1, mid_y),
            (mid_x - 2, mid_y)
        ]
        self.direction = (1, 0)       # Moving right initially
        self.input_queue = []          # Buffer keypresses to prevent self-collision on fast input
        self.score = 0
        self.is_new_high_score = False

        # Food state
        self.golden_food = None
        self.golden_timer = 0          # Frames remaining for golden apple
        self.apples_eaten = 0
        self.food = self.spawn_food()

    def spawn_food(self):
        """Generate a random food position not occupied by the snake."""
        empty_cells = [
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x, y) not in self.snake and (self.golden_food is None or (x, y) != self.golden_food)
        ]
        return random.choice(empty_cells) if empty_cells else (0, 0)

    def maybe_spawn_golden_apple(self):
        """Occasionally spawn a bonus golden apple."""
        if self.golden_food is None and self.apples_eaten > 0 and self.apples_eaten % 5 == 0:
            if random.random() < 0.6:  # 60% chance every 5 apples
                empty_cells = [
                    (x, y)
                    for x in range(GRID_WIDTH)
                    for y in range(GRID_HEIGHT)
                    if (x, y) not in self.snake and (x, y) != self.food
                ]
                if empty_cells:
                    self.golden_food = random.choice(empty_cells)
                    # Timer lasts for ~70 ticks
                    self.golden_timer = 70

    def handle_input(self):
        """Process keyboard events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state in ("PLAYING", "PAUSED", "GAMEOVER"):
                        self.state = "MENU"
                    else:
                        return False

                # Menu state controls
                if self.state == "MENU":
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.reset_game()
                        self.state = "PLAYING"
                    elif event.key == pygame.K_1:
                        self.difficulty_key = "EASY"
                    elif event.key == pygame.K_2:
                        self.difficulty_key = "NORMAL"
                    elif event.key == pygame.K_3:
                        self.difficulty_key = "HARD"

                # Playing state controls
                elif self.state == "PLAYING":
                    if event.key == pygame.K_SPACE:
                        self.state = "PAUSED"
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        self.queue_direction((0, -1))
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.queue_direction((0, 1))
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        self.queue_direction((-1, 0))
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.queue_direction((1, 0))

                # Paused state controls
                elif self.state == "PAUSED":
                    if event.key == pygame.K_SPACE:
                        self.state = "PLAYING"
                    elif event.key == pygame.K_r:
                        self.reset_game()
                        self.state = "PLAYING"

                # Game Over controls
                elif self.state == "GAMEOVER":
                    if event.key in (pygame.K_r, pygame.K_SPACE, pygame.K_RETURN):
                        self.reset_game()
                        self.state = "PLAYING"

        return True

    def queue_direction(self, new_dir):
        """Queue up a direction change if it's not a 180-degree reverse."""
        current = self.input_queue[-1] if self.input_queue else self.direction
        # Check that new_dir is not directly opposite to current
        if (new_dir[0] + current[0] != 0) or (new_dir[1] + current[1] != 0):
            # Limit queue size to 2 to keep gameplay crisp
            if len(self.input_queue) < 2:
                self.input_queue.append(new_dir)

    def update(self):
        """Advance game state by one frame."""
        if self.state != "PLAYING":
            return

        # Handle queued direction changes
        if self.input_queue:
            self.direction = self.input_queue.pop(0)

        # Calculate new head position
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Check collision with walls
        if (
            new_head[0] < 0
            or new_head[0] >= GRID_WIDTH
            or new_head[1] < 0
            or new_head[1] >= GRID_HEIGHT
        ):
            self.game_over()
            return

        # Check collision with self
        if new_head in self.snake:
            self.game_over()
            return

        # Move snake
        self.snake.insert(0, new_head)

        # Check apple collision
        if new_head == self.food:
            self.score += 10
            self.apples_eaten += 1
            if self.score > self.high_score:
                self.high_score = self.score
                self.is_new_high_score = True
                save_high_score(self.high_score)
            self.food = self.spawn_food()
            self.maybe_spawn_golden_apple()
        elif self.golden_food and new_head == self.golden_food:
            self.score += 30
            if self.score > self.high_score:
                self.high_score = self.score
                self.is_new_high_score = True
                save_high_score(self.high_score)
            self.golden_food = None
            self.golden_timer = 0
        else:
            # Normal movement: remove tail
            self.snake.pop()

        # Update golden apple timer
        if self.golden_food:
            self.golden_timer -= 1
            if self.golden_timer <= 0:
                self.golden_food = None

    def game_over(self):
        """Trigger game over state."""
        self.state = "GAMEOVER"

    # -------------------------------------------------------------
    # DRAWING ROUTINES
    # -------------------------------------------------------------
    def draw_grid(self):
        """Draw a clean subtle checkerboard grid."""
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = COLOR_BG_DARK if (x + y) % 2 == 0 else COLOR_BG_LIGHT
                rect = pygame.Rect(
                    x * CELL_SIZE,
                    TOP_BAR_HEIGHT + y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )
                pygame.draw.rect(self.screen, color, rect)

    def draw_header(self):
        """Draw top banner with score, high score, and difficulty."""
        # Top banner background
        header_rect = pygame.Rect(0, 0, SCREEN_WIDTH, TOP_BAR_HEIGHT)
        pygame.draw.rect(self.screen, COLOR_HEADER_BG, header_rect)
        pygame.draw.line(self.screen, COLOR_BORDER, (0, TOP_BAR_HEIGHT - 1), (SCREEN_WIDTH, TOP_BAR_HEIGHT - 1), 2)

        # Current Score
        score_surface = self.font_ui.render(f"SCORE: {self.score}", True, COLOR_TEXT_PRIMARY)
        self.screen.blit(score_surface, (20, 13))

        # High Score
        high_surface = self.font_ui.render(f"HIGH: {self.high_score}", True, COLOR_ACCENT)
        self.screen.blit(high_surface, (180, 13))

        # Difficulty indicator
        diff_text = f"MODE: {self.difficulty_key}"
        diff_surface = self.font_sub.render(diff_text, True, COLOR_TEXT_MUTED)
        self.screen.blit(diff_surface, (SCREEN_WIDTH - diff_surface.get_width() - 20, 16))

    def draw_food(self):
        """Draw food item (red apple with leaf, or golden apple)."""
        # Normal Apple
        fx, fy = self.food
        rect = pygame.Rect(
            fx * CELL_SIZE + 2,
            TOP_BAR_HEIGHT + fy * CELL_SIZE + 2,
            CELL_SIZE - 4,
            CELL_SIZE - 4
        )
        pygame.draw.ellipse(self.screen, COLOR_FOOD_RED, rect)

        # Little green leaf
        leaf_rect = pygame.Rect(
            fx * CELL_SIZE + CELL_SIZE // 2,
            TOP_BAR_HEIGHT + fy * CELL_SIZE + 2,
            4,
            4
        )
        pygame.draw.ellipse(self.screen, COLOR_FOOD_LEAF, leaf_rect)

        # Golden Apple (if active)
        if self.golden_food:
            gx, gy = self.golden_food
            g_rect = pygame.Rect(
                gx * CELL_SIZE + 2,
                TOP_BAR_HEIGHT + gy * CELL_SIZE + 2,
                CELL_SIZE - 4,
                CELL_SIZE - 4
            )
            # Pulsing effect based on timer
            pulse_color = COLOR_GOLDEN_APPLE if (self.golden_timer % 6 > 2) else (255, 235, 120)
            pygame.draw.ellipse(self.screen, pulse_color, g_rect)

    def draw_snake(self):
        """Draw snake body and head with cute eyes."""
        for i, (x, y) in enumerate(self.snake):
            rect = pygame.Rect(
                x * CELL_SIZE + 1,
                TOP_BAR_HEIGHT + y * CELL_SIZE + 1,
                CELL_SIZE - 2,
                CELL_SIZE - 2
            )

            if i == 0:
                # Snake Head
                pygame.draw.rect(self.screen, COLOR_SNAKE_HEAD, rect, border_radius=6)

                # Draw eyes facing current direction
                dx, dy = self.direction
                eye_radius = 3
                pupil_radius = 1

                # Calculate eye offsets based on movement direction
                if dx == 1:    # Right
                    e1 = (rect.right - 6, rect.top + 6)
                    e2 = (rect.right - 6, rect.bottom - 6)
                elif dx == -1:  # Left
                    e1 = (rect.left + 6, rect.top + 6)
                    e2 = (rect.left + 6, rect.bottom - 6)
                elif dy == -1:  # Up
                    e1 = (rect.left + 6, rect.top + 6)
                    e2 = (rect.right - 6, rect.top + 6)
                else:          # Down
                    e1 = (rect.left + 6, rect.bottom - 6)
                    e2 = (rect.right - 6, rect.bottom - 6)

                # Draw white sclera and black pupil
                for ex, ey in (e1, e2):
                    pygame.draw.circle(self.screen, COLOR_EYE_WHITE, (ex, ey), eye_radius)
                    pygame.draw.circle(self.screen, COLOR_EYE_PUPIL, (ex + dx, ey + dy), pupil_radius)
            else:
                # Snake Body segment
                pygame.draw.rect(self.screen, COLOR_SNAKE_BODY, rect, border_radius=4)
                pygame.draw.rect(self.screen, COLOR_SNAKE_OUTLINE, rect, width=1, border_radius=4)

    def draw_overlay_menu(self):
        """Draw start menu screen."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 15, 25, 220))
        self.screen.blit(overlay, (0, 0))

        title = self.font_title.render("S N A K E", True, COLOR_SNAKE_HEAD)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 120))

        sub = self.font_sub.render("Classic Arcade Game", True, COLOR_TEXT_MUTED)
        self.screen.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, 165))

        prompt = self.font_ui.render("Press [SPACE] or [ENTER] to Play", True, COLOR_ACCENT)
        self.screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 235))

        diff_title = self.font_sub.render("Select Difficulty:", True, COLOR_TEXT_PRIMARY)
        self.screen.blit(diff_title, (SCREEN_WIDTH // 2 - diff_title.get_width() // 2, 305))

        diff_1 = self.font_sub.render("[1] Easy    [2] Normal    [3] Hard", True, COLOR_TEXT_MUTED)
        self.screen.blit(diff_1, (SCREEN_WIDTH // 2 - diff_1.get_width() // 2, 335))

        current_info = self.font_sub.render(
            f"Current Mode: {DIFFICULTIES[self.difficulty_key]['name']}", True, (120, 200, 255)
        )
        self.screen.blit(current_info, (SCREEN_WIDTH // 2 - current_info.get_width() // 2, 365))

        controls_1 = self.font_sub.render("Controls: Arrow Keys or W/A/S/D to Move", True, COLOR_TEXT_MUTED)
        self.screen.blit(controls_1, (SCREEN_WIDTH // 2 - controls_1.get_width() // 2, 440))

        controls_2 = self.font_sub.render("Space = Pause  |  Esc = Quit", True, COLOR_TEXT_MUTED)
        self.screen.blit(controls_2, (SCREEN_WIDTH // 2 - controls_2.get_width() // 2, 470))

    def draw_overlay_pause(self):
        """Draw pause overlay."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        paused_text = self.font_title.render("PAUSED", True, COLOR_ACCENT)
        self.screen.blit(paused_text, (SCREEN_WIDTH // 2 - paused_text.get_width() // 2, 250))

        help_text = self.font_ui.render("Press [SPACE] to Resume", True, COLOR_TEXT_PRIMARY)
        self.screen.blit(help_text, (SCREEN_WIDTH // 2 - help_text.get_width() // 2, 310))

        restart_text = self.font_sub.render("Press [R] to Restart  |  [ESC] for Menu", True, COLOR_TEXT_MUTED)
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 350))

    def draw_overlay_gameover(self):
        """Draw game over overlay."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((20, 10, 10, 200))
        self.screen.blit(overlay, (0, 0))

        go_text = self.font_title.render("GAME OVER", True, COLOR_FOOD_RED)
        self.screen.blit(go_text, (SCREEN_WIDTH // 2 - go_text.get_width() // 2, 200))

        score_text = self.font_ui.render(f"Final Score: {self.score}", True, COLOR_TEXT_PRIMARY)
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 260))

        if self.is_new_high_score and self.score > 0:
            nh_text = self.font_ui.render("★ NEW HIGH SCORE! ★", True, COLOR_ACCENT)
            self.screen.blit(nh_text, (SCREEN_WIDTH // 2 - nh_text.get_width() // 2, 300))
        else:
            hs_text = self.font_sub.render(f"Best Score: {self.high_score}", True, COLOR_TEXT_MUTED)
            self.screen.blit(hs_text, (SCREEN_WIDTH // 2 - hs_text.get_width() // 2, 300))

        play_again = self.font_ui.render("Press [R] or [SPACE] to Play Again", True, COLOR_SNAKE_HEAD)
        self.screen.blit(play_again, (SCREEN_WIDTH // 2 - play_again.get_width() // 2, 370))

        esc_text = self.font_sub.render("Press [ESC] to return to Menu", True, COLOR_TEXT_MUTED)
        self.screen.blit(esc_text, (SCREEN_WIDTH // 2 - esc_text.get_width() // 2, 410))

    def render(self):
        """Render all visual elements."""
        self.draw_grid()
        self.draw_food()
        self.draw_snake()
        self.draw_header()

        if self.state == "MENU":
            self.draw_overlay_menu()
        elif self.state == "PAUSED":
            self.draw_overlay_pause()
        elif self.state == "GAMEOVER":
            self.draw_overlay_gameover()

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.render()

            # Tick speed based on difficulty
            speed = DIFFICULTIES[self.difficulty_key]["speed"]
            self.clock.tick(speed)

        pygame.quit()
        sys.exit()


# -------------------------------------------------------------
# ENTRY POINT
# -------------------------------------------------------------
if __name__ == "__main__":
    game = SnakeGame()
    game.run()
