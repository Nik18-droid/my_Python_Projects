# Python Ping Pong Game

A fully functional Ping Pong (Pong) game implemented in Python using pygame. Features two paddles, a ball with realistic physics, scoring system, and AI opponent with adjustable difficulty levels.

## Features

### Core Gameplay
- **Two Paddles**: Player-controlled and AI/human opponent
- **Realistic Ball Physics**: Ball bounces with angle variation based on paddle hit position
- **Scoring System**: First to 11 points wins
- **Multiple Game Modes**: 
  - Single Player vs AI (3 difficulty levels)
  - Two Player (human vs human)

### AI Features
- **Three Difficulty Levels**:
  - **Easy**: Slower reaction, 70% accuracy
  - **Medium**: Balanced gameplay, 85% accuracy  
  - **Hard**: Fast reaction, 95% accuracy
- **Realistic AI Behavior**: Includes reaction delays and occasional mistakes
- **Predictive Movement**: AI predicts ball trajectory for more challenging gameplay

### Visual Effects
- **Ball Trail Effect**: Visual trail following the ball
- **Gradient Paddles**: Enhanced paddle appearance with highlights
- **Smooth Animations**: 60 FPS gameplay
- **Dynamic UI**: Real-time score updates and game status

### Game States
- **Main Menu**: Game mode selection and settings
- **Gameplay**: Active game with pause functionality
- **Game Over Screen**: Winner announcement and replay options
- **Pause System**: Pause/resume during gameplay

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install pygame directly:
   ```bash
   pip install pygame
   ```

2. **Run the Game**:
   ```bash
   python ping_pong_python.py
   ```

## Controls

### Menu Navigation
- **1**: Select vs Computer mode
- **2**: Select vs Human mode  
- **3**: Cycle through AI difficulty levels (Easy → Medium → Hard)
- **SPACE**: Start game
- **ESC**: Quit game or return to menu

### Gameplay Controls
- **Player 1**: 
  - **W**: Move paddle up
  - **S**: Move paddle down
- **Player 2** (Human vs Human mode only):
  - **↑ (Up Arrow)**: Move paddle up
  - **↓ (Down Arrow)**: Move paddle down
- **P**: Pause/Resume game
- **ESC**: Return to main menu

### Game Over Screen
- **SPACE**: Play again
- **ESC**: Return to main menu

## Game Rules

1. **Objective**: Score 11 points before your opponent
2. **Scoring**: Ball passes opponent's paddle and hits the wall behind them
3. **Ball Physics**: 
   - Ball speed increases slightly with each paddle hit
   - Hit angle depends on where ball contacts paddle
   - Ball bounces off top and bottom walls
4. **Winning**: First player to reach 11 points wins

## Technical Details

### Architecture
- **Object-Oriented Design**: Separate classes for Ball, Paddle, AIPlayer, and Game
- **Game Loop**: 60 FPS with proper event handling and state management
- **Collision Detection**: Precise rectangle-based collision system
- **State Management**: Clean separation of menu, gameplay, pause, and game over states

### AI Implementation
- **Difficulty-Based Behavior**: Different speed, accuracy, and reaction times
- **Predictive Algorithm**: AI calculates ball trajectory for paddle positioning
- **Realistic Mistakes**: Random errors based on difficulty level
- **Reaction Delays**: Simulated human-like response times

### Performance
- **Optimized Rendering**: Efficient drawing with pygame
- **Smooth Movement**: Consistent 60 FPS gameplay
- **Memory Management**: Proper cleanup and resource handling

## Customization

You can easily modify the game by changing constants at the top of `ping_pong_python.py`:

```python
# Game dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Paddle settings
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
PADDLE_SPEED = 8

# Ball settings
BALL_SIZE = 15
BALL_SPEED = 7

# Game rules
WINNING_SCORE = 11
```

## Troubleshooting

### Common Issues

1. **pygame not found**:
   ```bash
   pip install pygame
   ```

2. **Game runs too fast/slow**:
   - Modify the FPS in the game loop: `self.clock.tick(60)`

3. **Sound errors** (optional sounds):
   - The game will run without sound files
   - Add .wav files for enhanced audio experience

### System Requirements
- **OS**: Windows, macOS, or Linux
- **Python**: 3.7+
- **RAM**: 50MB minimum
- **Display**: Any resolution (game window is 800x600)

## Future Enhancements

Potential improvements you could add:
- Sound effects and background music
- Particle effects for paddle hits
- Power-ups and special abilities
- Tournament mode with multiple rounds
- Online multiplayer support
- Customizable themes and colors
- Statistics tracking
- Replay system

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to fork this project and submit pull requests for improvements!