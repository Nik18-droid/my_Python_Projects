"""
SIMPLE PING PONG GAME FOR BEGINNERS
====================================

This is a simplified version of Ping Pong designed to teach fundamental Python concepts:
1. Variables and Data Types
2. Functions
3. Classes and Objects
4. Loops (while, for)
5. Conditional Statements (if, elif, else)
6. Lists and Dictionaries
7. User Input
8. Basic Game Logic

The game uses simple text-based graphics that work in the terminal.
"""

import random
import time
import os

# =============================================================================
# LESSON 1: VARIABLES AND CONSTANTS
# =============================================================================
# Variables store data that can change during program execution
# Constants are variables that shouldn't change (written in UPPERCASE)

GAME_WIDTH = 60        # Width of the game field
GAME_HEIGHT = 20       # Height of the game field
PADDLE_SIZE = 3        # Size of each paddle
WINNING_SCORE = 5      # Score needed to win
BALL_SYMBOL = "●"      # Symbol representing the ball
PADDLE_SYMBOL = "█"    # Symbol representing paddles
EMPTY_SPACE = " "      # Empty space character

# =============================================================================
# LESSON 2: FUNCTIONS
# =============================================================================
# Functions are reusable blocks of code that perform specific tasks
# They help organize code and avoid repetition


def clear_screen():
    """
    Function to clear the terminal screen
    Works on both Windows and Unix-like systems
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def create_empty_field():
    """
    Function that creates and returns an empty game field
    Returns: 2D list representing the game field
    """
    # List comprehension - creates a 2D list (list of lists)
    field = [[EMPTY_SPACE for _ in range(GAME_WIDTH)]
             for _ in range(GAME_HEIGHT)]
    return field


def draw_borders(field):
    """
    Function to draw borders around the game field
    Parameters: field - 2D list representing the game field
    """
    # Top and bottom borders
    for x in range(GAME_WIDTH):
        field[0][x] = "-"                    # Top border
        field[GAME_HEIGHT - 1][x] = "-"     # Bottom border

    # Left and right borders
    for y in range(GAME_HEIGHT):
        field[y][0] = "|"                    # Left border
        field[y][GAME_WIDTH - 1] = "|"      # Right border

    # Corner pieces
    field[0][0] = "+"
    field[0][GAME_WIDTH - 1] = "+"
    field[GAME_HEIGHT - 1][0] = "+"
    field[GAME_HEIGHT - 1][GAME_WIDTH - 1] = "+"


def display_field(field, player1_score, player2_score):
    """
    Function to display the game field and scores
    Parameters: 
        field - 2D list representing the game field
        player1_score - Player 1's current score
        player2_score - Player 2's current score
    """
    clear_screen()

    # Display title and scores
    print("=" * 60)
    print("           SIMPLE PING PONG GAME FOR BEGINNERS")
    print("=" * 60)
    print(
        f"Player 1: {player1_score}                    Player 2: {player2_score}")
    print()

    # Display the game field
    for row in field:
        print("".join(row))  # Join list elements into a string

    print()
    print("Controls: Player 1 (w/s) | Player 2 (i/k) | q to quit")

# =============================================================================
# LESSON 3: CLASSES AND OBJECTS
# =============================================================================
# Classes are blueprints for creating objects
# Objects have attributes (data) and methods (functions)


class Ball:
    """
    Ball class - represents the game ball
    Demonstrates: class definition, __init__ method, instance variables, methods
    """

    def __init__(self, x, y):
        """
        Constructor method - called when creating a new Ball object
        Parameters: x, y - starting position of the ball
        """
        self.x = x              # Ball's x position
        self.y = y              # Ball's y position
        self.direction_x = 1    # Ball's horizontal direction (1 or -1)
        self.direction_y = 1    # Ball's vertical direction (1 or -1)

    def move(self):
        """
        Method to move the ball based on its direction
        """
        self.x += self.direction_x
        self.y += self.direction_y

    def bounce_vertical(self):
        """
        Method to reverse ball's vertical direction (bounce off top/bottom)
        """
        self.direction_y = -self.direction_y

    def bounce_horizontal(self):
        """
        Method to reverse ball's horizontal direction (bounce off paddle)
        """
        self.direction_x = -self.direction_x

    def reset_position(self):
        """
        Method to reset ball to center with random direction
        """
        self.x = GAME_WIDTH // 2
        self.y = GAME_HEIGHT // 2
        # Random starting direction
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])


class Paddle:
    """
    Paddle class - represents a player's paddle
    Demonstrates: class with multiple methods, boundary checking
    """

    def __init__(self, x, y):
        """
        Constructor for Paddle
        Parameters: x, y - starting position of the paddle
        """
        self.x = x
        self.y = y
        self.size = PADDLE_SIZE

    def move_up(self):
        """
        Method to move paddle up (with boundary checking)
        """
        if self.y > 1:  # Don't go above the top border
            self.y -= 1

    def move_down(self):
        """
        Method to move paddle down (with boundary checking)
        """
        if self.y + self.size < GAME_HEIGHT - 1:  # Don't go below bottom border
            self.y += 1

    def get_positions(self):
        """
        Method that returns all positions occupied by the paddle
        Returns: list of (x, y) tuples
        """
        positions = []
        for i in range(self.size):
            positions.append((self.x, self.y + i))
        return positions


class SimpleAI:
    """
    Simple AI class - computer opponent
    Demonstrates: basic AI logic, decision making
    """

    def __init__(self, paddle):
        """
        Constructor for AI
        Parameters: paddle - the paddle object this AI controls
        """
        self.paddle = paddle
        self.reaction_delay = 0  # Simple delay mechanism

    def update(self, ball):
        """
        Method to update AI paddle position based on ball position
        Parameters: ball - the ball object
        """
        # Simple AI: move towards the ball with some delay
        self.reaction_delay += 1

        if self.reaction_delay > 2:  # React every 3 frames
            paddle_center = self.paddle.y + self.paddle.size // 2

            if ball.y < paddle_center:
                self.paddle.move_up()
            elif ball.y > paddle_center:
                self.paddle.move_down()

            self.reaction_delay = 0

# =============================================================================
# LESSON 4: MAIN GAME CLASS
# =============================================================================


class PingPongGame:
    """
    Main game class that manages the entire game
    Demonstrates: complex class, game state management, main game loop
    """

    def __init__(self):
        """
        Constructor - initialize all game objects and variables
        """
        # Game objects
        self.ball = Ball(GAME_WIDTH // 2, GAME_HEIGHT // 2)
        self.player1 = Paddle(2, GAME_HEIGHT // 2)
        self.player2 = Paddle(GAME_WIDTH - 3, GAME_HEIGHT // 2)
        self.ai = SimpleAI(self.player2)

        # Game state variables
        self.player1_score = 0
        self.player2_score = 0
        self.game_mode = "ai"  # "ai" or "human"
        self.game_running = True
        self.winner = None

    def get_user_input(self):
        """
        Method to get user input without blocking the game
        This is a simplified version - in real games, you'd use proper input handling
        """
        try:
            # This is a simple approach - in practice, you'd use threading or async input
            import select
            import sys

            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                return sys.stdin.read(1).lower()
        except:
            # Fallback for Windows or if select is not available
            pass

        return None

    def handle_input(self, key):
        """
        Method to handle user keyboard input
        Parameters: key - the pressed key
        """
        # Player 1 controls
        if key == 'w':
            self.player1.move_up()
        elif key == 's':
            self.player1.move_down()

        # Player 2 controls (only in human vs human mode)
        if self.game_mode == "human":
            if key == 'i':
                self.player2.move_up()
            elif key == 'k':
                self.player2.move_down()

        # Game controls
        if key == 'q':
            self.game_running = False

    def check_collisions(self):
        """
        Method to check for ball collisions with walls and paddles
        Demonstrates: collision detection, conditional logic
        """
        # Check collision with top and bottom walls
        if self.ball.y <= 1 or self.ball.y >= GAME_HEIGHT - 2:
            self.ball.bounce_vertical()

        # Check collision with paddles
        player1_positions = self.player1.get_positions()
        player2_positions = self.player2.get_positions()

        ball_pos = (self.ball.x, self.ball.y)

        # Collision with player 1 paddle
        if ball_pos in player1_positions and self.ball.direction_x < 0:
            self.ball.bounce_horizontal()

        # Collision with player 2 paddle
        if ball_pos in player2_positions and self.ball.direction_x > 0:
            self.ball.bounce_horizontal()

    def check_scoring(self):
        """
        Method to check if someone scored
        Demonstrates: scoring logic, game state changes
        """
        # Player 1 scores (ball goes off right side)
        if self.ball.x >= GAME_WIDTH - 1:
            self.player1_score += 1
            self.ball.reset_position()
            time.sleep(1)  # Brief pause after scoring

        # Player 2 scores (ball goes off left side)
        elif self.ball.x <= 0:
            self.player2_score += 1
            self.ball.reset_position()
            time.sleep(1)  # Brief pause after scoring

        # Check for winner
        if self.player1_score >= WINNING_SCORE:
            self.winner = "Player 1"
            self.game_running = False
        elif self.player2_score >= WINNING_SCORE:
            self.winner = "Player 2" if self.game_mode == "human" else "Computer"
            self.game_running = False

    def update_game_objects(self):
        """
        Method to update all game objects
        """
        self.ball.move()

        # Update AI if in AI mode
        if self.game_mode == "ai":
            self.ai.update(self.ball)

    def render_game(self):
        """
        Method to render/draw the current game state
        """
        # Create empty field
        field = create_empty_field()

        # Draw borders
        draw_borders(field)

        # Draw paddles
        for pos in self.player1.get_positions():
            if 0 <= pos[1] < GAME_HEIGHT and 0 <= pos[0] < GAME_WIDTH:
                field[pos[1]][pos[0]] = PADDLE_SYMBOL

        for pos in self.player2.get_positions():
            if 0 <= pos[1] < GAME_HEIGHT and 0 <= pos[0] < GAME_WIDTH:
                field[pos[1]][pos[0]] = PADDLE_SYMBOL

        # Draw ball
        if 0 <= self.ball.y < GAME_HEIGHT and 0 <= self.ball.x < GAME_WIDTH:
            field[self.ball.y][self.ball.x] = BALL_SYMBOL

        # Display everything
        display_field(field, self.player1_score, self.player2_score)

    def show_game_over(self):
        """
        Method to display game over screen
        """
        clear_screen()
        print("=" * 60)
        print("                        GAME OVER!")
        print("=" * 60)
        print(f"                    {self.winner} WINS!")
        print(
            f"              Final Score: {self.player1_score} - {self.player2_score}")
        print("=" * 60)
        print("Thanks for playing! Press Enter to exit...")
        input()

    def run(self):
        """
        Main game loop - the heart of the game
        Demonstrates: while loop, game loop pattern, program flow
        """
        print("Welcome to Simple Ping Pong!")
        print("Choose game mode:")
        print("1. vs Computer (AI)")
        print("2. vs Human")

        choice = input("Enter choice (1 or 2): ")
        if choice == "2":
            self.game_mode = "human"

        print("\nStarting game in 3 seconds...")
        time.sleep(3)

        # Main game loop
        while self.game_running:
            # Handle input (simplified)
            key = self.get_user_input()
            if key:
                self.handle_input(key)

            # Update game logic
            self.update_game_objects()
            self.check_collisions()
            self.check_scoring()

            # Render the game
            self.render_game()

            # Control game speed
            time.sleep(0.1)  # 10 FPS

        # Show game over screen
        self.show_game_over()

# =============================================================================
# LESSON 5: PROGRAM ENTRY POINT
# =============================================================================


def main():
    """
    Main function - entry point of the program
    Demonstrates: program structure, exception handling
    """
    try:
        # Create and run the game
        game = PingPongGame()
        game.run()

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n\nGame interrupted by user. Thanks for playing!")

    except Exception as e:
        # Handle any other errors
        print(f"\nAn error occurred: {e}")
        print("Please check your Python installation and try again.")

# =============================================================================
# PROGRAM EXECUTION
# =============================================================================


if __name__ == "__main__":
    """
    This block runs only when the script is executed directly
    (not when imported as a module)
    """
    main()

# =============================================================================
# LEARNING SUMMARY
# =============================================================================
"""
CONCEPTS DEMONSTRATED IN THIS CODE:

1. VARIABLES & DATA TYPES:
   - Integers: GAME_WIDTH, player scores
   - Strings: BALL_SYMBOL, player names
   - Booleans: game_running, direction flags
   - Lists: 2D field array, paddle positions

2. FUNCTIONS:
   - Function definition with def
   - Parameters and return values
   - Function documentation with docstrings

3. CLASSES & OBJECTS:
   - Class definition with class keyword
   - Constructor method (__init__)
   - Instance variables (self.x, self.y)
   - Methods (functions inside classes)

4. CONTROL STRUCTURES:
   - if/elif/else statements
   - while loops (main game loop)
   - for loops (drawing borders, paddle positions)

5. DATA STRUCTURES:
   - Lists and list comprehensions
   - 2D arrays (list of lists)
   - Tuples for coordinates

6. INPUT/OUTPUT:
   - print() for output
   - input() for user input
   - String formatting with f-strings

7. MODULES & IMPORTS:
   - Importing standard library modules
   - Using functions from imported modules

8. ERROR HANDLING:
   - try/except blocks
   - Handling specific exceptions

9. GAME PROGRAMMING CONCEPTS:
   - Game loop pattern
   - Object-oriented game design
   - Collision detection
   - State management

This simplified version teaches core programming concepts while creating
a functional game that runs in the terminal!
"""
