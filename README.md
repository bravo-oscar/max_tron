# MAX TRON - Lightcycle Battle!

A fun and colorful Tron-inspired lightcycle game for kids! Race your lightcycle, leave trails of light, and try to make your opponent crash!

## How to Install

### Step 1: Make sure Python is installed
You need Python 3.7 or newer. Check if you have it by opening Terminal and typing:
```bash
python3 --version
```

### Step 2: Install the game
Open Terminal and go to the game folder:
```bash
cd /*download-location*/max_tron
```

Install the required game library (Pygame):
```bash
pip3 install -r requirements.txt
```

## How to Play

### Starting the Game
In Terminal, type:
```bash
python3 max_tron.py
```

### Fullscreen Mode (Maximum Grid Size!)
- Press **F11** at any time to toggle fullscreen mode
- Fullscreen automatically detects your screen resolution and uses the ENTIRE display
- Much bigger playing field - great for high-difficulty battles!
- Press **F11** again to return to windowed mode (1280x1024)

### Difficulty Selection
First, you'll choose a difficulty level:
- Press **1** for EASY (Medium speed, cautious AI)
- Press **2** for MEDIUM (Fast speed, balanced AI)
- Press **3** for HARD (Very fast, aggressive AI)
- Press **4** for INSANE (Blazing fast, ruthless AI!)
- Press **5** for HACKER (EXTREME speed, NEARLY IMPOSSIBLE!)

### Game Modes
After choosing difficulty, select your game mode:
- Press **1** to play against the computer
- Press **2** to play with a friend
- Press **ESC** to go back and change difficulty

### Controls

**Player 1 (Cyan/Blue Lightcycle):**
- Arrow Keys to move (Up, Down, Left, Right)

**Player 2 (Orange Lightcycle) - Two Player Mode Only:**
- W = Up
- S = Down
- A = Left
- D = Right

### Rules
- Your lightcycle leaves a trail of light behind it
- If you hit a wall, a trail, or another cycle, you crash and lose!
- Try to make your opponent crash while avoiding crashes yourself
- You can't turn backwards into your own trail

### After a Game
- Press **R** to play again with the same mode
- Press **SPACE** to go back to the menu

## Visual Features
- Beautiful neon glow trails that look like light tubes
- Custom pixel art lightcycle sprites (or fallback to built-in graphics)
- Bright headlights on each bike
- Multi-layered glow effects for an authentic Tron look
- Dark blue grid background
- Sprites automatically rotate based on direction

## Custom Bike Sprites
Want to use your own pixel art bikes? Simply add these image files:
- `assets/bike_cyan.png` - Cyan/blue player bike (facing RIGHT)
- `assets/bike_orange.png` - Orange AI/player 2 bike (facing RIGHT)

The game will automatically:
- Load and scale your sprites to ~40 pixels
- Rotate them based on direction (up, down, left, right)
- Add glowing effects behind them
- Fall back to built-in graphics if images aren't found

**Sprite Tips:**
- Draw your bike facing RIGHT (that's the base orientation)
- Use transparent backgrounds (PNG with alpha channel)
- Make it roughly square for best rotation
- Include neon accents in the colors (cyan or orange)

## Tips for Max
- **Start with EASY mode** to learn the game, then work your way up!
- **The AI is now SMART** - it adapts its strategy based on the game situation!
- Plan ahead! Look where you're going and predict where the AI will go
- The AI plays differently based on the situation:
  - When it's cornered, it becomes more defensive and focuses on survival
  - When YOU'RE cornered, it becomes more aggressive to finish you off
  - When far away, it might play more aggressively to close the gap
  - It adds randomness so you can't predict its every move
- Stay in open spaces when possible - this forces the AI to be more cautious
- Try to corner the AI while keeping multiple escape routes for yourself
- On HARD, INSANE, and HACKER modes, the AI looks much further ahead
- Watch the neon trails - they show where you can't go
- Two player mode uses the same difficulty setting for speed (no AI in 2P mode)
- **HACKER mode is extremely challenging** - 60 FPS, looks 50 steps ahead!

## For Parents
- Five difficulty levels to grow with your child's skills
  - **EASY**: 25 FPS, AI looks 8 steps ahead, 50% base aggression
  - **MEDIUM**: 32 FPS, AI looks 15 steps ahead, 70% base aggression
  - **HARD**: 40 FPS, AI looks 25 steps ahead, 85% base aggression
  - **INSANE**: 50 FPS, AI looks 35 steps ahead, 95% base aggression
  - **HACKER**: 60 FPS, AI looks 50 steps ahead, 99% base aggression (extreme challenge!)
- **Advanced AI behavior**: The computer uses dynamic strategy that adapts to the game state
  - Becomes more defensive when cornered or close to the player
  - Becomes more aggressive when the player is trapped
  - Balances offense and defense based on available space
  - Adds randomness to be less predictable
  - Evaluates risk vs reward for each move
- Bright neon colors and simple controls make it accessible
- No violence - just colorful light trails and strategic gameplay
- Great for developing planning, spatial awareness, reaction skills, and strategic thinking
- Progression system encourages mastery and builds confidence

## Customization
The difficulty levels are pre-configured in the game, but you can customize them by editing `max_tron.py`:
- Find the `DIFFICULTY_SETTINGS` dictionary (lines 17-23)
- Adjust `fps` (game speed), `ai_lookahead` (how far AI plans ahead), and `aggression` (0.0-1.0, how offensive the AI plays)
- Higher aggression makes AI prioritize trapping you over self-preservation!

**Start in Fullscreen Mode:**
- Find `FULLSCREEN = False` on line 15
- Change to `FULLSCREEN = True` to always start in fullscreen
- You can still toggle with F11 during gameplay

Have fun playing MAX TRON!
