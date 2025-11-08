# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Max Tron is a Tron-inspired lightcycle battle game built with Pygame. Players control lightcycles that leave permanent trails behind them, attempting to force opponents to crash into walls or trails. The game features both single-player (vs AI) and two-player modes with five difficulty levels.

## Development Commands

**Install dependencies:**
```bash
pip3 install -r requirements.txt
```

**Run the game:**
```bash
python3 max_tron.py
```

**Requirements:**
- Python 3.7 or newer
- Pygame 2.5.0 or newer

## Architecture

### Core Components

**Main Game Loop (`Game.run()`):**
- Handles input → updates game state → renders frame → caps FPS
- FPS varies by difficulty (20-40) during gameplay, fixed at 30 for menus
- State machine: `difficulty_menu` → `mode_menu` → `playing` → `game_over`

**Game States:**
- `difficulty_menu`: Initial screen where player selects difficulty (1-5)
- `mode_menu`: Choose single-player or two-player mode
- `playing`: Active gameplay with collision detection and AI updates
- `game_over`: Shows winner and offers restart or return to menu

**LightCycle Class:**
- Maintains position (x, y), direction, trail history, and alive status
- Trail is a list of (x, y) tuples representing permanent light walls
- Movement is grid-based (GRID_SIZE = 10 pixels)
- Collision detection checks: walls, self-trail, opponent trail, head-to-head
- Rendering uses multi-layered glow effect for neon tube appearance
- Supports custom sprite images or falls back to `draw_bike()` drawn graphics
- Sprite system: loads PNG images from `assets/`, auto-rotates for all directions, caches rotations

**AggressiveAI Class (now Strategic AI):**
- Adaptive AI that dynamically adjusts strategy based on game state
- Key parameters: `lookahead_depth` (8-50 steps) and `base_aggression` (0.5-0.99)
- **Dynamic Aggression System (`adjust_aggression_dynamically()`):**
  - Adjusts aggression every move based on multiple factors
  - Own survival: Reduces aggression 70% when AI has ≤1 exit, 40% when 2 exits
  - Distance to player: More defensive when close (<50px), more aggressive when far (>300px)
  - Player's situation: Increases aggression 50% when player has ≤1 exit
  - Random variation: ±15% randomness for unpredictability
- `evaluate_offensive_move()`: Scores moves based on:
  - Distance to player (closer = higher score)
  - Cutting off player's projected path
  - Reducing player's escape routes (best when player has ≤2 exits)
  - Controlling center/strategic positions
  - Predicted player position (at high aggression)
- **Strategic Decision Making:**
  - Risk assessment: Avoids moves with <3 space if safer alternatives exist
  - Tiered strategy based on current (dynamic) aggression level:
    - >0.9: Pure offense, high risk/high reward
    - >0.7: 70% aggressive, 30% considers safety
    - >0.4: Balanced with random variance
    - ≤0.4: Defensive, prioritizes space (80%) over offense (20%)
- Balances survival vs offense: `total_score = survival_score + offensive_score`

### Difficulty Configuration

Located in `DIFFICULTY_SETTINGS` dictionary (lines 18-24):
```python
{
    'easy': {'fps': 25, 'ai_lookahead': 8, 'aggression': 0.5},
    'medium': {'fps': 32, 'ai_lookahead': 15, 'aggression': 0.7},
    'hard': {'fps': 40, 'ai_lookahead': 25, 'aggression': 0.85},
    'insane': {'fps': 50, 'ai_lookahead': 35, 'aggression': 0.95},
    'hacker': {'fps': 60, 'ai_lookahead': 50, 'aggression': 0.99}
}
```

- `fps`: Game speed (frames per second) - ranges from 25 (easy) to 60 (hacker)
- `ai_lookahead`: How many grid cells ahead the AI evaluates for space - ranges from 8 to 50
- `aggression`: 0.0-1.0 scale for base aggression (dynamically adjusted during gameplay) - ranges from 0.5 to 0.99

**Note:** HACKER mode (0.99 base aggression, 60 FPS, 50 lookahead) is extremely challenging - designed to be nearly unbeatable

### Controls

- Player 1 (Cyan): Arrow keys
- Player 2 (Orange): WASD keys
- Menu navigation: Number keys (1-5) for selections, ESC to go back
- Game over: R to restart, SPACE to return to difficulty menu
- F11: Toggle fullscreen mode (works in any state)

### Visual Rendering

**Neon Glow Effect (trails):**
- Outer dark glow layer (1/3 color intensity)
- Middle glow layer (2/3 intensity)
- Inner bright neon (full color)
- White hot center core

**Color Scheme:**
- Player 1: Cyan (#00FFFF)
- Player 2/AI: Orange (#FF8C00)
- Background: Dark blue (#001428)
- Grid lines: Subtle darker blue (#001E32)

### Grid System

- Default window: 1280x1024 pixels (DEFAULT_WIDTH x DEFAULT_HEIGHT)
- Fullscreen mode: Uses actual screen resolution (detected at runtime)
- Grid cell: 10x10 pixels (GRID_SIZE constant)
- Cycles move exactly one grid cell per frame
- Trail positions stored as (x, y) pixel coordinates aligned to grid
- Collision detection compares exact grid positions
- `WINDOW_WIDTH` and `WINDOW_HEIGHT` are global variables updated when toggling fullscreen

### Fullscreen Mode

- Controlled by `FULLSCREEN` constant (line 16) - set at startup
- Uses `pygame.display.set_mode((0, 0), pygame.FULLSCREEN)` to auto-detect native resolution
- Screen dimensions retrieved via `self.screen.get_width()` and `get_height()` after creation
- `toggle_fullscreen()` method switches between modes at runtime (F11 key)
- When toggling, `WINDOW_WIDTH` and `WINDOW_HEIGHT` globals are updated dynamically
- Display surface is recreated with new dimensions
- Works in any game state (menu, playing, game over)
- Fullscreen uses maximum available resolution; windowed uses DEFAULT_WIDTH x DEFAULT_HEIGHT (1280x1024)

### Custom Sprite System

**Location:** `assets/` directory
**Sprite Files:**
- `assets/bike_cyan.png` - Player 1 sprite
- `assets/bike_orange.png` - Player 2/AI sprite

**Implementation:**
- `load_bike_sprite()` function loads and scales sprites to ~40 pixels (configurable)
- Sprites must face RIGHT as base orientation
- Auto-rotation: RIGHT (base), LEFT (flipped), UP (90° CW), DOWN (90° CCW)
- Rotations are cached in `LightCycle.rotated_sprites` dictionary for performance
- Graceful fallback to `draw_bike()` method if sprites not found
- PNG format with alpha channel recommended for transparency
- Sprites loaded at startup into globals `BIKE_SPRITE_CYAN` and `BIKE_SPRITE_ORANGE`

**Rendering:**
- Sprite centered on grid position (`self.x + GRID_SIZE // 2, self.y + GRID_SIZE // 2`)
- Neon glow effect drawn behind sprite based on color
- Glow size calculated from sprite dimensions

## AI Behavior Notes

The AI uses **dynamic strategy** that adapts to the game state in real-time:

**Adaptive Behavior:**
1. **Self-Preservation:** When cornered (1-2 exits), AI reduces aggression by 30-70% to focus on survival
2. **Distance-Based Tactics:** Plays defensively when close to player (<50px), aggressively when far (>300px)
3. **Opportunistic Finishing:** Increases aggression by 50% when player is trapped (≤2 exits)
4. **Unpredictability:** Adds ±15% random variation to prevent predictable patterns
5. **Risk Assessment:** Evaluates each move's risk (available space) vs reward (offensive score)

**Strategic Depth:**
- Not purely aggressive—balances offense and defense based on context
- Looks ahead to predict player moves (especially at high aggression)
- Evaluates multiple factors: distance, escape routes, space availability, positioning
- Uses tiered decision-making based on current aggression level
- Avoids obvious traps when not in "kamikaze" mode (aggression <0.9)

This creates an AI opponent that feels intelligent and adaptive rather than just fast and aggressive.
