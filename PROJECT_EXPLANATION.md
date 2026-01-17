# Senet Game Project - Comprehensive Explanation

## Project Overview
This is a complete implementation of the ancient Egyptian board game "Senet" (also known as "Senat" or "Senet-taui"). The game features a player-vs-computer setup where players compete to move all their pieces off the board first according to specific rules.

## Game Rules & Mechanics

### Board Structure
- **Board Size**: 3 rows × 10 columns (30 positions total)
- **Piece Movement Path**: 
  - Row 1: Positions 1-10 (left to right)
  - Row 2: Positions 11-20 (right to left)  
  - Row 3: Positions 21-30 (left to right)

### Players & Pieces
- **Players**: White (human player) and Black (computer/AI)
- **Pieces per player**: 7 pieces each
- **Starting positions**: 
  - White: [2, 4, 6, 8, 10, 12, 14]
  - Black: [1, 3, 5, 7, 9, 11, 13]

### Dice System
- Uses 4 sticks instead of traditional dice
- Each stick has two sides: light (1) and dark (0)
- Rolling mechanism:
  - Sum all sticks (0-4)
  - If sum = 0, result is 5
  - Possible outcomes: 1, 2, 3, 4, 5
- Probabilities: {1: 25%, 2: 37.5%, 3: 25%, 4: 6.25%, 5: 6.25%}

### Special Houses/Rules

#### House of Rebirth (Position 15)
- Symbol: Two concentric circles
- Normal movement house - no special rules

#### House of Happiness (Position 26)  
- Symbol: Green checkmark (✔)
- Cannot jump over this house - pieces must land on it or stop before it

#### House of Water (Position 27)
- Symbol: Blue waves
- Penalty house: Any piece landing here must return to the nearest empty position ≤ 15

#### House of Three Truths (Position 28)
- Symbol: Three red triangles (▲▲▲)
- Must roll exactly 3 to exit
- If different roll: piece returns to nearest empty position ≤ 15

#### House of Re-Atoum (Position 29)
- Symbol: Two red triangles (▲▲)
- Must roll exactly 2 to exit
- If different roll: piece returns to nearest empty position ≤ 15

#### House of Horus (Position 30)
- Symbol: Black arrow pointing right
- Exit house: Can choose to exit the board or return to play
- No mandatory roll requirement

## Core Components

### 1. Constants (`constants.py`)
Defines all game constants:
- Board dimensions and layout
- Special house positions
- Player identifiers (WHITE, BLACK)
- UI colors and sizes
- Window dimensions

### 2. Board (`board.py`)
Manages the game board state:
- Piece placement and movement
- Occupancy checks
- Special house rule enforcement (except House of Water which is handled in Game class)
- Board visualization

### 3. Game State (`state.py`)
Represents the complete game state:
- Current board configuration
- Player piece positions
- Exited pieces tracking
- Turn management
- Terminal state detection (win/lose conditions)
- Exit condition validation for special houses

### 4. Dice (`dice.py`)
Handles dice rolling mechanics:
- Stick rolling simulation
- Probability calculations for Expectiminimax algorithm
- Result normalization (0-sum becomes 5)

### 5. Move Logic (`move.py`)
Core game mechanics:
- Legal move generation based on current roll
- Move application with all rule enforcement
- Piece swapping when landing on opponent's piece
- Special house handling (28, 29, 30)
- House of Water penalty processing

### 6. Heuristic Evaluation (`heuristic.py`)
AI evaluation function:
- Piece position scoring system
- Higher scores for advanced positions
- Bonus for pieces approaching exit (positions ≥ 28)
- Difference-based scoring (white_score - black_score)

### 7. Expectiminimax AI (`expectiminimax.py`)
Game AI implementation:
- Minimax algorithm adapted for chance nodes (dice rolls)
- Uses probability-weighted decision making
- Depth-limited search with configurable search depth
- Node counting for performance monitoring

### 8. Game Controller (`game.py`)
Main game orchestration:
- Turn management (player vs computer)
- Input processing and move execution
- Penalty application for special houses
- Win condition checking
- Game loop coordination

### 9. Renderer (`renderer.py`)
Pygame-based graphics system:
- Board drawing and piece rendering
- Special house symbol visualization
- Legal move highlighting
- Toss button and game info display
- Exited pieces visualization
- Game over screen

### 10. Input Handler (`input_handler.py`)
Mouse input processing:
- Cell coordinate conversion
- Position mapping according to Senet movement path
- Click detection and validation

### 11. Main Entry Point (`main.py`)
Application startup:
- Initializes game with configurable AI depth
- Starts the main game loop

## Key Algorithms & Design Patterns

### Expectiminimax Algorithm
Used for AI decision making:
- MAX nodes: Computer's turn (maximizing score)
- MIN nodes: Player's turn (minimizing computer's advantage)
- CHANCE nodes: Dice roll outcomes with probabilities
- Evaluates all possible moves weighted by dice probabilities

### State Pattern
Game state is immutable during AI calculation:
- `clone()` method creates copies for simulation
- Original state remains unchanged during search
- Thread-safe approach for future multiplayer expansion

### Observer Pattern (Implicit)
Renderer observes game state changes:
- Redraws board after each move
- Updates UI elements dynamically
- Real-time feedback to players

## Game Flow

1. **Initialization**: Set up board with pieces in starting positions
2. **Player Turn**: 
   - Click "TOSS" button to roll sticks
   - Select piece to move from highlighted legal moves
   - Apply move with all rule enforcement
3. **Computer Turn**:
   - AI calculates best move using Expectiminimax
   - Execute chosen move
   - Apply penalties for special houses
4. **Win Condition**: First player to remove all pieces wins

## Technical Features

### Error Handling
- Invalid move prevention
- Boundary checking
- Piece collision detection
- Special house rule enforcement

### Performance Optimization
- Efficient board representation (dictionary)
- Pruned search space in Expectiminimax
- Configurable search depth
- Lazy evaluation where possible

### Extensibility Points
- Easy AI difficulty adjustment (depth parameter)
- Modular component design
- Clear separation of concerns
- Well-defined interfaces between components

## Dependencies
- Python 3.x
- Pygame library for graphics
- Standard library modules (random, math)

## Running the Game
```bash
python main.py
```

## Configuration Options
- AI search depth can be modified in `main.py`
- Board colors and sizes adjustable in `constants.py`
- Starting positions modifiable in `state.py`

This comprehensive implementation provides a solid foundation for the ancient Senet game with modern AI capabilities and clean, maintainable code structure.