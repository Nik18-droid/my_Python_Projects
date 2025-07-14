import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
BALL_SIZE = 15
PADDLE_SPEED = 8
BALL_SPEED = 7
AI_SPEED = 6
WINNING_SCORE = 11

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 100, 100)
BLUE = (100, 100, 255)
GREEN = (100, 255, 100)
YELLOW = (255, 255, 100)
CYAN = (100, 255, 255)
GRAY = (128, 128, 128)


class Ball:
    """Ball class to handle ball physics and rendering"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_x = BALL_SPEED * random.choice([-1, 1])
        self.vel_y = BALL_SPEED * random.choice([-1, 1])
        self.size = BALL_SIZE
        self.color = WHITE
        self.trail = []  # For ball trail effect

    def move(self):
        """Move the ball and handle wall collisions"""
        self.x += self.vel_x
        self.y += self.vel_y

        # Add current position to trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > 10:
            self.trail.pop(0)

        # Bounce off top and bottom walls
        if self.y <= self.size // 2 or self.y >= SCREEN_HEIGHT - self.size // 2:
            self.vel_y = -self.vel_y
            self.y = max(self.size // 2,
                         min(SCREEN_HEIGHT - self.size // 2, self.y))

    def reset(self):
        """Reset ball to center with random direction"""
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.vel_x = BALL_SPEED * random.choice([-1, 1])
        self.vel_y = BALL_SPEED * random.choice([-1, 1])
        self.trail.clear()

    def draw(self, screen):
        """Draw the ball with trail effect"""
        # Draw trail
        for i, (trail_x, trail_y) in enumerate(self.trail):
            alpha = (i + 1) / len(self.trail)
            trail_size = int(self.size * alpha * 0.7)
            trail_color = tuple(int(c * alpha) for c in self.color)
            pygame.draw.circle(screen, trail_color,
                               (int(trail_x), int(trail_y)), trail_size)

        # Draw main ball
        pygame.draw.circle(screen, self.color, (int(
            self.x), int(self.y)), self.size // 2)
        # Add highlight
        pygame.draw.circle(screen, (255, 255, 255),
                           (int(self.x - 3), int(self.y - 3)), self.size // 4)


class Paddle:
    """Paddle class to handle paddle movement and rendering"""

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = PADDLE_SPEED
        self.color = color
        self.score = 0

    def move_up(self):
        """Move paddle up"""
        if self.y > 0:
            self.y -= self.speed

    def move_down(self):
        """Move paddle down"""
        if self.y < SCREEN_HEIGHT - self.height:
            self.y += self.speed

    def get_rect(self):
        """Get paddle rectangle for collision detection"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        """Draw the paddle with gradient effect"""
        # Draw main paddle
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.width, self.height))
        # Add highlight
        pygame.draw.rect(screen, WHITE, (self.x + 2,
                         self.y + 2, self.width - 4, 10))


class AIPlayer:
    """AI player class for computer opponent"""

    def __init__(self, paddle, difficulty='medium'):
        self.paddle = paddle
        self.difficulty = difficulty
        self.reaction_time = 0
        self.target_y = paddle.y + paddle.height // 2

        # AI settings based on difficulty
        self.settings = {
            'easy': {'speed': 4, 'accuracy': 0.7, 'reaction_delay': 20},
            'medium': {'speed': 6, 'accuracy': 0.85, 'reaction_delay': 15},
            'hard': {'speed': 8, 'accuracy': 0.95, 'reaction_delay': 8}
        }

    def update(self, ball):
        """Update AI paddle position based on ball position"""
        current_settings = self.settings[self.difficulty]

        # Only react when ball is moving towards AI paddle
        if ball.vel_x > 0:
            # Add some prediction based on ball trajectory
            predicted_y = ball.y + \
                (ball.vel_y * ((self.paddle.x - ball.x) / ball.vel_x))

            # Add some randomness for more realistic behavior
            if random.random() < current_settings['accuracy']:
                self.target_y = predicted_y
            else:
                # Sometimes make mistakes
                self.target_y = predicted_y + random.randint(-50, 50)

        # Move towards target with reaction delay
        paddle_center = self.paddle.y + self.paddle.height // 2
        difference = self.target_y - paddle_center

        if abs(difference) > current_settings['reaction_delay']:
            if difference > 0:
                self.paddle.y += min(current_settings['speed'], difference)
            else:
                self.paddle.y -= min(current_settings['speed'],
                                     abs(difference))

        # Keep paddle within bounds
        self.paddle.y = max(
            0, min(SCREEN_HEIGHT - self.paddle.height, self.paddle.y))


class Game:
    """Main game class"""

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Python Ping Pong Game")
        self.clock = pygame.time.Clock()

        # Game objects
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.player1 = Paddle(30, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, RED)
        self.player2 = Paddle(SCREEN_WIDTH - 30 - PADDLE_WIDTH,
                              SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, BLUE)

        # Game state
        self.game_mode = 'ai'  # 'ai' or 'human'
        self.ai_difficulty = 'medium'
        self.ai_player = AIPlayer(self.player2, self.ai_difficulty)
        self.game_state = 'menu'  # 'menu', 'playing', 'paused', 'game_over'
        self.winner = None

        # Fonts
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)

        # Sound effects (optional - requires sound files)
        self.sounds_enabled = False
        try:
            self.paddle_sound = pygame.mixer.Sound("paddle_hit.wav")
            self.wall_sound = pygame.mixer.Sound("wall_hit.wav")
            self.score_sound = pygame.mixer.Sound("score.wav")
            self.sounds_enabled = True
        except:
            pass  # Continue without sounds if files not found

    def handle_collision(self):
        """Handle ball-paddle collisions"""
        ball_rect = pygame.Rect(self.ball.x - self.ball.size // 2,
                                self.ball.y - self.ball.size // 2,
                                self.ball.size, self.ball.size)

        # Check collision with player 1 paddle
        if ball_rect.colliderect(self.player1.get_rect()) and self.ball.vel_x < 0:
            # Calculate hit position for angle variation
            hit_pos = (self.ball.y - (self.player1.y +
                       self.player1.height // 2)) / (self.player1.height // 2)
            hit_pos = max(-1, min(1, hit_pos))  # Clamp between -1 and 1

            self.ball.vel_x = abs(self.ball.vel_x)  # Reverse direction
            self.ball.vel_y = BALL_SPEED * hit_pos * 0.8  # Add angle based on hit position

            # Increase ball speed slightly
            speed_increase = 1.1
            self.ball.vel_x *= speed_increase
            self.ball.vel_y *= speed_increase

            # Ensure ball doesn't get stuck in paddle
            self.ball.x = self.player1.x + self.player1.width + self.ball.size // 2

            if self.sounds_enabled:
                self.paddle_sound.play()

        # Check collision with player 2 paddle
        elif ball_rect.colliderect(self.player2.get_rect()) and self.ball.vel_x > 0:
            # Calculate hit position for angle variation
            hit_pos = (self.ball.y - (self.player2.y +
                       self.player2.height // 2)) / (self.player2.height // 2)
            hit_pos = max(-1, min(1, hit_pos))  # Clamp between -1 and 1

            self.ball.vel_x = -abs(self.ball.vel_x)  # Reverse direction
            self.ball.vel_y = BALL_SPEED * hit_pos * 0.8  # Add angle based on hit position

            # Increase ball speed slightly
            speed_increase = 1.1
            self.ball.vel_x *= speed_increase
            self.ball.vel_y *= speed_increase

            # Ensure ball doesn't get stuck in paddle
            self.ball.x = self.player2.x - self.ball.size // 2

            if self.sounds_enabled:
                self.paddle_sound.play()

    def check_scoring(self):
        """Check if a player has scored"""
        if self.ball.x < 0:
            # Player 2 scores
            self.player2.score += 1
            if self.sounds_enabled:
                self.score_sound.play()
            self.ball.reset()

            if self.player2.score >= WINNING_SCORE:
                self.winner = "Player 2" if self.game_mode == 'human' else "Computer"
                self.game_state = 'game_over'

        elif self.ball.x > SCREEN_WIDTH:
            # Player 1 scores
            self.player1.score += 1
            if self.sounds_enabled:
                self.score_sound.play()
            self.ball.reset()

            if self.player1.score >= WINNING_SCORE:
                self.winner = "Player 1"
                self.game_state = 'game_over'

    def handle_input(self):
        """Handle keyboard input"""
        keys = pygame.key.get_pressed()

        if self.game_state == 'playing':
            # Player 1 controls (W/S keys)
            if keys[pygame.K_w]:
                self.player1.move_up()
            if keys[pygame.K_s]:
                self.player1.move_down()

            # Player 2 controls (only in human vs human mode)
            if self.game_mode == 'human':
                if keys[pygame.K_UP]:
                    self.player2.move_up()
                if keys[pygame.K_DOWN]:
                    self.player2.move_down()

    def update(self):
        """Update game logic"""
        if self.game_state == 'playing':
            self.ball.move()
            self.handle_collision()
            self.check_scoring()

            # Update AI if in AI mode
            if self.game_mode == 'ai':
                self.ai_player.update(self.ball)

    def draw_menu(self):
        """Draw the main menu"""
        self.screen.fill(BLACK)

        # Title
        title = self.font_large.render("PING PONG", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        # Menu options
        menu_items = [
            "1 - Play vs Computer",
            "2 - Play vs Human",
            "3 - Change AI Difficulty",
            "SPACE - Start Game",
            "ESC - Quit"
        ]

        for i, item in enumerate(menu_items):
            text = self.font_small.render(item, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 250 + i * 50))
            self.screen.blit(text, text_rect)

        # Current settings
        mode_text = f"Current Mode: {'vs Computer' if self.game_mode == 'ai' else 'vs Human'}"
        diff_text = f"AI Difficulty: {self.ai_difficulty.capitalize()}"

        mode_surface = self.font_small.render(mode_text, True, YELLOW)
        diff_surface = self.font_small.render(diff_text, True, YELLOW)

        self.screen.blit(mode_surface, (50, SCREEN_HEIGHT - 80))
        self.screen.blit(diff_surface, (50, SCREEN_HEIGHT - 50))

    def draw_game(self):
        """Draw the game screen"""
        self.screen.fill(BLACK)

        # Draw center line
        for i in range(0, SCREEN_HEIGHT, 20):
            pygame.draw.rect(self.screen, WHITE,
                             (SCREEN_WIDTH // 2 - 2, i, 4, 10))

        # Draw paddles
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)

        # Draw ball
        self.ball.draw(self.screen)

        # Draw scores
        score1_text = self.font_medium.render(
            str(self.player1.score), True, WHITE)
        score2_text = self.font_medium.render(
            str(self.player2.score), True, WHITE)

        self.screen.blit(score1_text, (SCREEN_WIDTH // 4, 50))
        self.screen.blit(score2_text, (3 * SCREEN_WIDTH // 4, 50))

        # Draw player labels
        p1_label = "Player 1"
        p2_label = "Player 2" if self.game_mode == 'human' else f"Computer ({self.ai_difficulty})"

        p1_text = self.font_small.render(p1_label, True, RED)
        p2_text = self.font_small.render(p2_label, True, BLUE)

        self.screen.blit(p1_text, (SCREEN_WIDTH // 4 - 50, 20))
        self.screen.blit(p2_text, (3 * SCREEN_WIDTH // 4 - 50, 20))

        # Draw controls
        controls = [
            "Player 1: W/S keys",
            "Player 2: ↑/↓ keys" if self.game_mode == 'human' else "Computer AI",
            "P - Pause | ESC - Menu"
        ]

        for i, control in enumerate(controls):
            text = pygame.font.Font(None, 24).render(control, True, GRAY)
            self.screen.blit(text, (10, SCREEN_HEIGHT - 80 + i * 25))

    def draw_pause(self):
        """Draw pause overlay"""
        self.draw_game()

        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # Pause text
        pause_text = self.font_large.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(pause_text, pause_rect)

        resume_text = self.font_small.render("Press P to resume", True, WHITE)
        resume_rect = resume_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(resume_text, resume_rect)

    def draw_game_over(self):
        """Draw game over screen"""
        self.screen.fill(BLACK)

        # Winner announcement
        winner_text = self.font_large.render(
            f"{self.winner} Wins!", True, GREEN)
        winner_rect = winner_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(winner_text, winner_rect)

        # Final score
        score_text = f"Final Score: {self.player1.score} - {self.player2.score}"
        score_surface = self.font_medium.render(score_text, True, WHITE)
        score_rect = score_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(score_surface, score_rect)

        # Options
        options = [
            "SPACE - Play Again",
            "ESC - Main Menu"
        ]

        for i, option in enumerate(options):
            text = self.font_small.render(option, True, WHITE)
            text_rect = text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60 + i * 40))
            self.screen.blit(text, text_rect)

    def reset_game(self):
        """Reset the game to initial state"""
        self.player1.score = 0
        self.player2.score = 0
        self.ball.reset()
        self.player1.y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.player2.y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.winner = None

    def run(self):
        """Main game loop"""
        running = True

        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.game_state == 'menu':
                            running = False
                        else:
                            self.game_state = 'menu'

                    elif event.key == pygame.K_SPACE:
                        if self.game_state == 'menu':
                            self.reset_game()
                            self.game_state = 'playing'
                        elif self.game_state == 'game_over':
                            self.reset_game()
                            self.game_state = 'playing'

                    elif event.key == pygame.K_p and self.game_state in ['playing', 'paused']:
                        self.game_state = 'paused' if self.game_state == 'playing' else 'playing'

                    elif self.game_state == 'menu':
                        if event.key == pygame.K_1:
                            self.game_mode = 'ai'
                        elif event.key == pygame.K_2:
                            self.game_mode = 'human'
                        elif event.key == pygame.K_3:
                            # Cycle through AI difficulties
                            difficulties = ['easy', 'medium', 'hard']
                            current_index = difficulties.index(
                                self.ai_difficulty)
                            self.ai_difficulty = difficulties[(
                                current_index + 1) % len(difficulties)]
                            self.ai_player = AIPlayer(
                                self.player2, self.ai_difficulty)

            # Handle continuous input
            self.handle_input()

            # Update game logic
            self.update()

            # Draw everything
            if self.game_state == 'menu':
                self.draw_menu()
            elif self.game_state == 'playing':
                self.draw_game()
            elif self.game_state == 'paused':
                self.draw_pause()
            elif self.game_state == 'game_over':
                self.draw_game_over()

            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    # Create and run the game
    game = Game()
    game.run()
