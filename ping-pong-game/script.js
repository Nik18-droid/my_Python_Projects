// Game variables
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Game state
let gameState = {
    isRunning: false,
    isPaused: false,
    gameMode: 'ai', // 'ai' or 'human'
    difficulty: 'medium',
    player1Score: 0,
    player2Score: 0,
    maxScore: 11,
    gameOver: false,
    winner: null
};

// Game objects
const ball = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    radius: 8,
    velocityX: 5,
    velocityY: 3,
    speed: 5,
    maxSpeed: 12,
    color: '#4ecdc4'
};

const paddle1 = {
    x: 10,
    y: canvas.height / 2 - 50,
    width: 10,
    height: 100,
    speed: 8,
    color: '#ff6b6b',
    upPressed: false,
    downPressed: false
};

const paddle2 = {
    x: canvas.width - 20,
    y: canvas.height / 2 - 50,
    width: 10,
    height: 100,
    speed: 8,
    color: '#667eea',
    upPressed: false,
    downPressed: false
};

// AI settings based on difficulty
const aiSettings = {
    easy: { speed: 4, accuracy: 0.7, reactionDelay: 15 },
    medium: { speed: 6, accuracy: 0.85, reactionDelay: 10 },
    hard: { speed: 8, accuracy: 0.95, reactionDelay: 5 }
};

// Input handling
const keys = {};

// Event listeners for buttons
document.getElementById('startBtn').addEventListener('click', startGame);
document.getElementById('pauseBtn').addEventListener('click', togglePause);
document.getElementById('resetBtn').addEventListener('click', resetGame);
document.getElementById('gameMode').addEventListener('change', changeGameMode);
document.getElementById('difficulty').addEventListener('change', changeDifficulty);

// Keyboard event listeners
document.addEventListener('keydown', (e) => {
    keys[e.key.toLowerCase()] = true;
    
    // Spacebar to start/pause
    if (e.code === 'Space') {
        e.preventDefault();
        if (!gameState.isRunning) {
            startGame();
        } else {
            togglePause();
        }
    }
});

document.addEventListener('keyup', (e) => {
    keys[e.key.toLowerCase()] = false;
});

// Game functions
function startGame() {
    if (gameState.gameOver) {
        resetGame();
    }
    
    gameState.isRunning = true;
    gameState.isPaused = false;
    updateGameStatus('Game Running!');
    
    if (!gameState.gameOver) {
        gameLoop();
    }
}

function togglePause() {
    if (gameState.isRunning && !gameState.gameOver) {
        gameState.isPaused = !gameState.isPaused;
        updateGameStatus(gameState.isPaused ? 'Game Paused' : 'Game Running!');
        
        if (!gameState.isPaused) {
            gameLoop();
        }
    }
}

function resetGame() {
    gameState.isRunning = false;
    gameState.isPaused = false;
    gameState.player1Score = 0;
    gameState.player2Score = 0;
    gameState.gameOver = false;
    gameState.winner = null;
    
    // Reset ball position
    ball.x = canvas.width / 2;
    ball.y = canvas.height / 2;
    ball.velocityX = 5 * (Math.random() > 0.5 ? 1 : -1);
    ball.velocityY = 3 * (Math.random() > 0.5 ? 1 : -1);
    ball.speed = 5;
    
    // Reset paddle positions
    paddle1.y = canvas.height / 2 - 50;
    paddle2.y = canvas.height / 2 - 50;
    
    updateScore();
    updateGameStatus('Press Start to begin!');
    
    // Remove game over overlay if it exists
    const overlay = document.querySelector('.game-over-overlay');
    if (overlay) {
        overlay.remove();
    }
    
    // Redraw the game
    draw();
}

function changeGameMode() {
    gameState.gameMode = document.getElementById('gameMode').value;
    resetGame();
}

function changeDifficulty() {
    gameState.difficulty = document.getElementById('difficulty').value;
}

function updateGameStatus(message) {
    document.getElementById('gameStatus').textContent = message;
}

function updateScore() {
    document.getElementById('player1Score').textContent = gameState.player1Score;
    document.getElementById('player2Score').textContent = gameState.player2Score;
}

// Game loop
function gameLoop() {
    if (!gameState.isRunning || gameState.isPaused || gameState.gameOver) {
        return;
    }
    
    update();
    draw();
    
    requestAnimationFrame(gameLoop);
}

// Update game logic
function update() {
    // Update paddle positions based on input
    updatePaddles();
    
    // Update ball position
    updateBall();
    
    // Check for collisions
    checkCollisions();
    
    // Check for scoring
    checkScoring();
}

function updatePaddles() {
    // Player 1 controls (W/S keys)
    if (keys['w'] && paddle1.y > 0) {
        paddle1.y -= paddle1.speed;
    }
    if (keys['s'] && paddle1.y < canvas.height - paddle1.height) {
        paddle1.y += paddle1.speed;
    }
    
    // Player 2 controls or AI
    if (gameState.gameMode === 'human') {
        // Human player 2 (Arrow keys)
        if (keys['arrowup'] && paddle2.y > 0) {
            paddle2.y -= paddle2.speed;
        }
        if (keys['arrowdown'] && paddle2.y < canvas.height - paddle2.height) {
            paddle2.y += paddle2.speed;
        }
    } else {
        // AI player
        updateAI();
    }
    
    // Keep paddles within bounds
    paddle1.y = Math.max(0, Math.min(canvas.height - paddle1.height, paddle1.y));
    paddle2.y = Math.max(0, Math.min(canvas.height - paddle2.height, paddle2.y));
}

function updateAI() {
    const ai = aiSettings[gameState.difficulty];
    const paddleCenter = paddle2.y + paddle2.height / 2;
    const ballCenter = ball.y;
    
    // Add some randomness and reaction delay for more realistic AI
    const shouldReact = Math.random() < ai.accuracy;
    
    if (shouldReact && ball.velocityX > 0) { // Only react when ball is coming towards AI
        const difference = ballCenter - paddleCenter;
        
        if (Math.abs(difference) > ai.reactionDelay) {
            if (difference > 0 && paddle2.y < canvas.height - paddle2.height) {
                paddle2.y += ai.speed;
            } else if (difference < 0 && paddle2.y > 0) {
                paddle2.y -= ai.speed;
            }
        }
    }
}

function updateBall() {
    ball.x += ball.velocityX;
    ball.y += ball.velocityY;
    
    // Ball collision with top and bottom walls
    if (ball.y - ball.radius <= 0 || ball.y + ball.radius >= canvas.height) {
        ball.velocityY = -ball.velocityY;
        
        // Keep ball within bounds
        if (ball.y - ball.radius <= 0) {
            ball.y = ball.radius;
        } else {
            ball.y = canvas.height - ball.radius;
        }
    }
}

function checkCollisions() {
    // Ball collision with paddle 1
    if (ball.x - ball.radius <= paddle1.x + paddle1.width &&
        ball.y >= paddle1.y &&
        ball.y <= paddle1.y + paddle1.height &&
        ball.velocityX < 0) {
        
        // Calculate hit position for angle variation
        const hitPos = (ball.y - (paddle1.y + paddle1.height / 2)) / (paddle1.height / 2);
        
        ball.velocityX = -ball.velocityX;
        ball.velocityY = hitPos * 5; // Add angle based on hit position
        
        // Increase ball speed slightly
        ball.speed = Math.min(ball.maxSpeed, ball.speed + 0.2);
        ball.velocityX = ball.velocityX > 0 ? ball.speed : -ball.speed;
        
        // Ensure ball doesn't get stuck in paddle
        ball.x = paddle1.x + paddle1.width + ball.radius;
    }
    
    // Ball collision with paddle 2
    if (ball.x + ball.radius >= paddle2.x &&
        ball.y >= paddle2.y &&
        ball.y <= paddle2.y + paddle2.height &&
        ball.velocityX > 0) {
        
        // Calculate hit position for angle variation
        const hitPos = (ball.y - (paddle2.y + paddle2.height / 2)) / (paddle2.height / 2);
        
        ball.velocityX = -ball.velocityX;
        ball.velocityY = hitPos * 5; // Add angle based on hit position
        
        // Increase ball speed slightly
        ball.speed = Math.min(ball.maxSpeed, ball.speed + 0.2);
        ball.velocityX = ball.velocityX > 0 ? ball.speed : -ball.speed;
        
        // Ensure ball doesn't get stuck in paddle
        ball.x = paddle2.x - ball.radius;
    }
}

function checkScoring() {
    // Player 1 scores (ball goes off right side)
    if (ball.x > canvas.width) {
        gameState.player1Score++;
        resetBallPosition();
        updateScore();
        
        // Add score flash animation
        document.getElementById('player1Score').classList.add('score-flash');
        setTimeout(() => {
            document.getElementById('player1Score').classList.remove('score-flash');
        }, 500);
        
        checkGameOver();
    }
    
    // Player 2 scores (ball goes off left side)
    if (ball.x < 0) {
        gameState.player2Score++;
        resetBallPosition();
        updateScore();
        
        // Add score flash animation
        document.getElementById('player2Score').classList.add('score-flash');
        setTimeout(() => {
            document.getElementById('player2Score').classList.remove('score-flash');
        }, 500);
        
        checkGameOver();
    }
}

function resetBallPosition() {
    ball.x = canvas.width / 2;
    ball.y = canvas.height / 2;
    ball.velocityX = 5 * (Math.random() > 0.5 ? 1 : -1);
    ball.velocityY = 3 * (Math.random() > 0.5 ? 1 : -1);
    ball.speed = 5;
}

function checkGameOver() {
    if (gameState.player1Score >= gameState.maxScore || gameState.player2Score >= gameState.maxScore) {
        gameState.gameOver = true;
        gameState.isRunning = false;
        gameState.winner = gameState.player1Score >= gameState.maxScore ? 'Player 1' : 'Player 2';
        
        showGameOverScreen();
    }
}

function showGameOverScreen() {
    const overlay = document.createElement('div');
    overlay.className = 'game-over-overlay';
    
    const content = document.createElement('div');
    content.className = 'game-over-content';
    
    const title = document.createElement('h2');
    title.textContent = `${gameState.winner} Wins!`;
    
    const score = document.createElement('p');
    score.textContent = `Final Score: ${gameState.player1Score} - ${gameState.player2Score}`;
    score.style.fontSize = '1.2em';
    score.style.marginBottom = '20px';
    
    const playAgainBtn = document.createElement('button');
    playAgainBtn.textContent = 'Play Again';
    playAgainBtn.addEventListener('click', () => {
        overlay.remove();
        resetGame();
    });
    
    content.appendChild(title);
    content.appendChild(score);
    content.appendChild(playAgainBtn);
    overlay.appendChild(content);
    document.body.appendChild(overlay);
}

// Drawing functions
function draw() {
    // Clear canvas
    ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw center line
    drawCenterLine();
    
    // Draw paddles
    drawPaddle(paddle1);
    drawPaddle(paddle2);
    
    // Draw ball
    drawBall();
    
    // Draw particle effects for ball trail
    drawBallTrail();
}

function drawCenterLine() {
    ctx.setLineDash([5, 15]);
    ctx.beginPath();
    ctx.moveTo(canvas.width / 2, 0);
    ctx.lineTo(canvas.width / 2, canvas.height);
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.setLineDash([]);
}

function drawPaddle(paddle) {
    // Add gradient effect to paddles
    const gradient = ctx.createLinearGradient(paddle.x, paddle.y, paddle.x + paddle.width, paddle.y + paddle.height);
    gradient.addColorStop(0, paddle.color);
    gradient.addColorStop(1, paddle.color + '80');
    
    ctx.fillStyle = gradient;
    ctx.fillRect(paddle.x, paddle.y, paddle.width, paddle.height);
    
    // Add glow effect
    ctx.shadowColor = paddle.color;
    ctx.shadowBlur = 10;
    ctx.fillRect(paddle.x, paddle.y, paddle.width, paddle.height);
    ctx.shadowBlur = 0;
}

function drawBall() {
    // Add glow effect to ball
    ctx.shadowColor = ball.color;
    ctx.shadowBlur = 15;
    
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fillStyle = ball.color;
    ctx.fill();
    
    // Add inner highlight
    ctx.shadowBlur = 0;
    ctx.beginPath();
    ctx.arc(ball.x - 2, ball.y - 2, ball.radius / 3, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
    ctx.fill();
}

function drawBallTrail() {
    // Simple trail effect - you could enhance this with a proper particle system
    ctx.globalAlpha = 0.3;
    ctx.beginPath();
    ctx.arc(ball.x - ball.velocityX, ball.y - ball.velocityY, ball.radius * 0.8, 0, Math.PI * 2);
    ctx.fillStyle = ball.color;
    ctx.fill();
    
    ctx.globalAlpha = 0.1;
    ctx.beginPath();
    ctx.arc(ball.x - ball.velocityX * 2, ball.y - ball.velocityY * 2, ball.radius * 0.6, 0, Math.PI * 2);
    ctx.fillStyle = ball.color;
    ctx.fill();
    
    ctx.globalAlpha = 1;
}

// Initialize the game
function init() {
    updateScore();
    updateGameStatus('Press Start to begin!');
    draw();
}

// Start the game when page loads
window.addEventListener('load', init);

// Handle window resize
window.addEventListener('resize', () => {
    // You could add responsive canvas resizing here if needed
});