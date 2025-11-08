import pygame
import sys
from enum import Enum
import random
import os

# Initialize Pygame
pygame.init()

# Constants
DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 1024
WINDOW_WIDTH = DEFAULT_WIDTH
WINDOW_HEIGHT = DEFAULT_HEIGHT
GRID_SIZE = 10
FULLSCREEN = False  # Set to True for fullscreen mode

# Difficulty settings
DIFFICULTY_SETTINGS = {
    'easy': {'fps': 25, 'ai_lookahead': 8, 'aggression': 0.5},
    'medium': {'fps': 32, 'ai_lookahead': 15, 'aggression': 0.7},
    'hard': {'fps': 40, 'ai_lookahead': 25, 'aggression': 0.85},
    'insane': {'fps': 50, 'ai_lookahead': 35, 'aggression': 0.95},
    'hacker': {'fps': 60, 'ai_lookahead': 50, 'aggression': 0.99}
}

# Colors (bright and colorful!)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 140, 0)
YELLOW = (255, 255, 0)
PURPLE = (200, 0, 255)
WHITE = (255, 255, 255)
DARK_BLUE = (0, 20, 40)
NEON_BLUE = (0, 150, 255)
NEON_PINK = (255, 20, 147)

# Directions
class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

# Sprite loading (done after display init)
BIKE_SPRITE_CYAN = None
BIKE_SPRITE_ORANGE = None

def load_bike_sprites():
    """Load bike sprites after display is initialized"""
    global BIKE_SPRITE_CYAN, BIKE_SPRITE_ORANGE

    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    def load_sprite(color_name, target_size=40):
        sprite_path = os.path.join(script_dir, 'assets', f'bike_{color_name}.png')
        print(f"Loading sprite: {sprite_path}")

        if os.path.exists(sprite_path):
            try:
                # Load the image
                sprite = pygame.image.load(sprite_path).convert_alpha()

                # Scale to target size while maintaining aspect ratio
                sprite_rect = sprite.get_rect()
                print(f"  Original: {sprite_rect.width}x{sprite_rect.height}")

                scale_factor = target_size / max(sprite_rect.width, sprite_rect.height)
                new_width = int(sprite_rect.width * scale_factor)
                new_height = int(sprite_rect.height * scale_factor)

                scaled_sprite = pygame.transform.smoothscale(sprite, (new_width, new_height))
                print(f"  ✓ Loaded {color_name} sprite ({new_width}x{new_height})")
                return scaled_sprite

            except Exception as e:
                print(f"  ✗ Error loading {color_name}: {e}")
                return None
        else:
            print(f"  ✗ Not found: {sprite_path}")
            return None

    BIKE_SPRITE_CYAN = load_sprite('cyan')
    BIKE_SPRITE_ORANGE = load_sprite('orange')

    if BIKE_SPRITE_CYAN and BIKE_SPRITE_ORANGE:
        print("✓ Custom bike sprites loaded successfully!")
    elif BIKE_SPRITE_CYAN or BIKE_SPRITE_ORANGE:
        print("⚠ Partial sprite loading")
    else:
        print("ℹ Using built-in drawn bikes")

class LightCycle:
    def __init__(self, x, y, color, direction, sprite=None):
        self.x = x
        self.y = y
        self.color = color
        self.direction = direction
        self.trail = []
        self.alive = True
        self.sprite = sprite

        # Debug: Show what we're using
        if self.sprite:
            print(f"  LightCycle created with CUSTOM SPRITE (color: {color})")
        else:
            print(f"  LightCycle created with DRAWN BIKE (color: {color})")

        # Cache rotated sprites for each direction
        if self.sprite:
            self.rotated_sprites = {
                Direction.RIGHT: self.sprite,  # Base sprite faces right
                Direction.LEFT: pygame.transform.flip(self.sprite, True, False),
                Direction.UP: pygame.transform.rotate(self.sprite, 90),
                Direction.DOWN: pygame.transform.rotate(self.sprite, -90)
            }
            print(f"  Rotated sprites cached for all 4 directions")

    def move(self):
        if not self.alive:
            return

        # Add current position to trail
        self.trail.append((self.x, self.y))

        # Move in current direction
        dx, dy = self.direction.value
        self.x += dx * GRID_SIZE
        self.y += dy * GRID_SIZE

    def change_direction(self, new_direction):
        # Prevent reversing into own trail
        dx, dy = self.direction.value
        new_dx, new_dy = new_direction.value

        if dx + new_dx != 0 or dy + new_dy != 0:
            self.direction = new_direction

    def check_collision(self, other_cycle=None):
        # Check wall collision
        if (self.x < 0 or self.x >= WINDOW_WIDTH or
            self.y < 0 or self.y >= WINDOW_HEIGHT):
            self.alive = False
            return True

        # Check self collision
        if (self.x, self.y) in self.trail[:-1]:
            self.alive = False
            return True

        # Check collision with other cycle
        if other_cycle:
            if (self.x, self.y) in other_cycle.trail:
                self.alive = False
                return True
            if self.x == other_cycle.x and self.y == other_cycle.y:
                self.alive = False
                other_cycle.alive = False
                return True

        return False

    def draw_bike(self, screen, x, y, direction):
        """Draw a pixel-art lightcycle inspired by the provided design"""
        # Dark bike body
        dark_body = (40, 40, 40)

        if direction == Direction.RIGHT:
            # Main body (dark)
            pygame.draw.rect(screen, dark_body, (x + 1, y + 2, 7, 6))
            # Top fairing
            pygame.draw.rect(screen, self.color, (x + 3, y + 1, 5, 2))
            pygame.draw.rect(screen, WHITE, (x + 4, y + 1, 3, 1))
            # Wheels (large circles)
            pygame.draw.circle(screen, dark_body, (x + 2, y + 7), 2)
            pygame.draw.circle(screen, self.color, (x + 2, y + 7), 2, 1)
            pygame.draw.circle(screen, dark_body, (x + 7, y + 7), 2)
            pygame.draw.circle(screen, self.color, (x + 7, y + 7), 2, 1)
            # Neon accents
            pygame.draw.rect(screen, self.color, (x + 3, y + 4, 4, 1))
            # Headlight
            pygame.draw.circle(screen, WHITE, (x + 8, y + 5), 1)

        elif direction == Direction.LEFT:
            # Main body (dark)
            pygame.draw.rect(screen, dark_body, (x + 2, y + 2, 7, 6))
            # Top fairing
            pygame.draw.rect(screen, self.color, (x + 2, y + 1, 5, 2))
            pygame.draw.rect(screen, WHITE, (x + 3, y + 1, 3, 1))
            # Wheels (large circles)
            pygame.draw.circle(screen, dark_body, (x + 8, y + 7), 2)
            pygame.draw.circle(screen, self.color, (x + 8, y + 7), 2, 1)
            pygame.draw.circle(screen, dark_body, (x + 3, y + 7), 2)
            pygame.draw.circle(screen, self.color, (x + 3, y + 7), 2, 1)
            # Neon accents
            pygame.draw.rect(screen, self.color, (x + 3, y + 4, 4, 1))
            # Headlight
            pygame.draw.circle(screen, WHITE, (x + 1, y + 5), 1)

        elif direction == Direction.UP:
            # Main body (dark)
            pygame.draw.rect(screen, dark_body, (x + 2, y + 1, 6, 7))
            # Top fairing
            pygame.draw.rect(screen, self.color, (x + 1, y + 3, 2, 5))
            pygame.draw.rect(screen, WHITE, (x + 1, y + 4, 1, 3))
            # Wheels (large circles)
            pygame.draw.circle(screen, dark_body, (x + 7, y + 2), 2)
            pygame.draw.circle(screen, self.color, (x + 7, y + 2), 2, 1)
            pygame.draw.circle(screen, dark_body, (x + 7, y + 7), 2)
            pygame.draw.circle(screen, self.color, (x + 7, y + 7), 2, 1)
            # Neon accents
            pygame.draw.rect(screen, self.color, (x + 4, y + 3, 1, 4))
            # Headlight
            pygame.draw.circle(screen, WHITE, (x + 5, y + 1), 1)

        else:  # DOWN
            # Main body (dark)
            pygame.draw.rect(screen, dark_body, (x + 2, y + 2, 6, 7))
            # Top fairing
            pygame.draw.rect(screen, self.color, (x + 7, y + 2, 2, 5))
            pygame.draw.rect(screen, WHITE, (x + 8, y + 3, 1, 3))
            # Wheels (large circles)
            pygame.draw.circle(screen, dark_body, (x + 3, y + 3), 2)
            pygame.draw.circle(screen, self.color, (x + 3, y + 3), 2, 1)
            pygame.draw.circle(screen, dark_body, (x + 3, y + 8), 2)
            pygame.draw.circle(screen, self.color, (x + 3, y + 8), 2, 1)
            # Neon accents
            pygame.draw.rect(screen, self.color, (x + 5, y + 3, 1, 4))
            # Headlight
            pygame.draw.circle(screen, WHITE, (x + 5, y + 9), 1)

    def draw(self, screen):
        # Draw trail with neon tube glow effect (multi-layered)
        for i, (tx, ty) in enumerate(self.trail):
            # Outer glow (darkest)
            outer_rect = pygame.Rect(tx - 1, ty - 1, GRID_SIZE + 2, GRID_SIZE + 2)
            dark_color = tuple(c // 3 for c in self.color)
            pygame.draw.rect(screen, dark_color, outer_rect, border_radius=2)

            # Middle layer (medium glow)
            mid_color = tuple(c * 2 // 3 for c in self.color)
            mid_rect = pygame.Rect(tx, ty, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, mid_color, mid_rect, border_radius=1)

            # Inner bright neon
            inner_rect = pygame.Rect(tx + 1, ty + 1, GRID_SIZE - 2, GRID_SIZE - 2)
            pygame.draw.rect(screen, self.color, inner_rect)

            # White hot center (neon tube core)
            center_rect = pygame.Rect(tx + 3, ty + 3, GRID_SIZE - 6, GRID_SIZE - 6)
            pygame.draw.rect(screen, WHITE, center_rect)

        # Draw cycle head
        if self.alive:
            if self.sprite:
                # Use sprite image
                current_sprite = self.rotated_sprites[self.direction]
                sprite_rect = current_sprite.get_rect()

                # Draw glow behind sprite
                glow_size = max(sprite_rect.width, sprite_rect.height) + 10
                glow_rect = pygame.Rect(
                    self.x - (glow_size - GRID_SIZE) // 2,
                    self.y - (glow_size - GRID_SIZE) // 2,
                    glow_size, glow_size
                )
                dark_color = tuple(c // 3 for c in self.color)
                pygame.draw.rect(screen, dark_color, glow_rect, border_radius=5)

                # Position sprite centered on grid position
                sprite_rect.center = (self.x + GRID_SIZE // 2, self.y + GRID_SIZE // 2)
                screen.blit(current_sprite, sprite_rect)
            else:
                # Fallback to drawn bike
                # Large outer glow
                glow_rect = pygame.Rect(self.x - 3, self.y - 3, GRID_SIZE + 6, GRID_SIZE + 6)
                dark_color = tuple(c // 4 for c in self.color)
                pygame.draw.rect(screen, dark_color, glow_rect, border_radius=3)

                # Medium glow
                mid_glow = pygame.Rect(self.x - 1, self.y - 1, GRID_SIZE + 2, GRID_SIZE + 2)
                mid_color = tuple(c * 2 // 3 for c in self.color)
                pygame.draw.rect(screen, mid_color, mid_glow, border_radius=2)

                # Bright neon background
                head_rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, self.color, head_rect, border_radius=1)

                # Draw the bike on top
                self.draw_bike(screen, self.x, self.y, self.direction)

class AggressiveAI:
    """Strategic AI that adapts tactics based on game state"""
    def __init__(self, cycle, lookahead_depth=5, aggression=0.5):
        self.cycle = cycle
        self.lookahead_depth = lookahead_depth
        self.base_aggression = aggression  # Base aggression level
        self.aggression = aggression  # Current aggression (dynamically adjusted)

    def count_open_space(self, start_x, start_y, direction, player_cycle, depth=None):
        """Count available space in a direction"""
        if depth is None:
            depth = self.lookahead_depth

        dx, dy = direction.value
        count = 0

        for i in range(1, depth + 1):
            test_x = start_x + (dx * GRID_SIZE * i)
            test_y = start_y + (dy * GRID_SIZE * i)

            if (test_x < 0 or test_x >= WINDOW_WIDTH or
                test_y < 0 or test_y >= WINDOW_HEIGHT):
                break

            if ((test_x, test_y) in self.cycle.trail or
                (test_x, test_y) in player_cycle.trail):
                break

            count += 1

        return count

    def calculate_distance_to_player(self, pos_x, pos_y, player_cycle):
        """Calculate Manhattan distance to player"""
        return abs(pos_x - player_cycle.x) + abs(pos_y - player_cycle.y)

    def is_cutting_off_player(self, direction, player_cycle):
        """Check if this move cuts off player's escape routes"""
        dx, dy = direction.value
        future_x = self.cycle.x + dx * GRID_SIZE
        future_y = self.cycle.y + dy * GRID_SIZE

        # Predict where player is heading
        player_dx, player_dy = player_cycle.direction.value
        player_future_x = player_cycle.x + player_dx * GRID_SIZE * 3
        player_future_y = player_cycle.y + player_dy * GRID_SIZE * 3

        # Check if we're moving toward player's projected path
        current_dist = self.calculate_distance_to_player(self.cycle.x, self.cycle.y, player_cycle)
        future_dist_to_player = abs(future_x - player_future_x) + abs(future_y - player_future_y)

        return future_dist_to_player < current_dist

    def count_player_escape_routes(self, player_cycle):
        """Count how many safe directions the player has"""
        escape_count = 0
        for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
            dx, dy = direction.value

            # Don't count going backwards
            pdx, pdy = player_cycle.direction.value
            if dx + pdx == 0 and dy + pdy == 0:
                continue

            test_x = player_cycle.x + dx * GRID_SIZE
            test_y = player_cycle.y + dy * GRID_SIZE

            if (test_x >= 0 and test_x < WINDOW_WIDTH and
                test_y >= 0 and test_y < WINDOW_HEIGHT and
                (test_x, test_y) not in player_cycle.trail and
                (test_x, test_y) not in self.cycle.trail):

                # Count space in this direction
                space = self.count_open_space(test_x, test_y, direction, player_cycle, depth=5)
                if space > 2:
                    escape_count += 1

        return escape_count

    def count_own_escape_routes(self):
        """Count how many safe directions the AI has"""
        escape_count = 0
        current_dir = self.cycle.direction

        for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
            dx, dy = direction.value

            # Don't count going backwards
            cdx, cdy = current_dir.value
            if dx + cdx == 0 and dy + cdy == 0:
                continue

            test_x = self.cycle.x + dx * GRID_SIZE
            test_y = self.cycle.y + dy * GRID_SIZE

            if (test_x >= 0 and test_x < WINDOW_WIDTH and
                test_y >= 0 and test_y < WINDOW_HEIGHT and
                (test_x, test_y) not in self.cycle.trail):

                escape_count += 1

        return escape_count

    def adjust_aggression_dynamically(self, player_cycle):
        """Dynamically adjust aggression based on game state"""
        # Start with base aggression
        dynamic_aggression = self.base_aggression

        # Factor 1: Own survival - if we have few exits, be more defensive
        own_exits = self.count_own_escape_routes()
        if own_exits <= 1:
            dynamic_aggression *= 0.3  # Very defensive if trapped
        elif own_exits == 2:
            dynamic_aggression *= 0.6  # Moderately defensive

        # Factor 2: Distance to player - be more cautious when close
        dist = self.calculate_distance_to_player(self.cycle.x, self.cycle.y, player_cycle)
        if dist < 50:  # Very close
            dynamic_aggression *= 0.7  # More defensive to avoid collision
        elif dist > 300:  # Far away
            dynamic_aggression = min(1.0, dynamic_aggression * 1.2)  # More aggressive

        # Factor 3: Player's situation - if player is trapped, be more aggressive
        player_exits = self.count_player_escape_routes(player_cycle)
        if player_exits <= 1:
            dynamic_aggression = min(1.0, dynamic_aggression * 1.5)  # Go for the kill!
        elif player_exits == 2:
            dynamic_aggression = min(1.0, dynamic_aggression * 1.2)

        # Factor 4: Add randomness to be less predictable (±15%)
        random_factor = 1.0 + (random.random() * 0.3 - 0.15)
        dynamic_aggression *= random_factor

        # Clamp to valid range
        return max(0.1, min(0.99, dynamic_aggression))

    def evaluate_offensive_move(self, direction, player_cycle):
        """Score how good this move is offensively"""
        dx, dy = direction.value
        future_x = self.cycle.x + dx * GRID_SIZE
        future_y = self.cycle.y + dy * GRID_SIZE

        score = 0

        # Reward getting closer to player
        current_dist = self.calculate_distance_to_player(self.cycle.x, self.cycle.y, player_cycle)
        future_dist = self.calculate_distance_to_player(future_x, future_y, player_cycle)

        if future_dist < current_dist:
            score += 15 * self.aggression

        # Extra bonus for getting very close (within striking distance)
        if future_dist < 100 and self.aggression > 0.7:
            score += 25 * self.aggression

        # Big reward for cutting off player
        if self.is_cutting_off_player(direction, player_cycle):
            score += 30 * self.aggression

        # Reward reducing player's escape routes
        player_escapes = self.count_player_escape_routes(player_cycle)
        if player_escapes <= 2:
            score += 40 * self.aggression  # Player is getting boxed in!
        if player_escapes == 1:
            score += 60 * self.aggression  # Almost trapped!

        # Bonus for positioning between player and center/open space
        center_x, center_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        if abs(future_x - center_x) < abs(player_cycle.x - center_x):
            score += 8 * self.aggression

        # High aggression: predict player's next few moves and block them
        if self.aggression > 0.8:
            player_dx, player_dy = player_cycle.direction.value
            predicted_player_x = player_cycle.x + player_dx * GRID_SIZE * 2
            predicted_player_y = player_cycle.y + player_dy * GRID_SIZE * 2

            # Reward being on collision course with predicted position
            predicted_dist = abs(future_x - predicted_player_x) + abs(future_y - predicted_player_y)
            if predicted_dist < current_dist:
                score += 20 * self.aggression

        return score

    def get_next_direction(self, player_cycle):
        # Dynamically adjust aggression based on current game state
        self.aggression = self.adjust_aggression_dynamically(player_cycle)

        current_dir = self.cycle.direction
        possible_dirs = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
        safe_dirs = []

        for direction in possible_dirs:
            # Don't reverse
            dx, dy = current_dir.value
            new_dx, new_dy = direction.value
            if dx + new_dx == 0 and dy + new_dy == 0:
                continue

            # Check immediate safety
            test_x = self.cycle.x + new_dx * GRID_SIZE
            test_y = self.cycle.y + new_dy * GRID_SIZE

            if test_x < 0 or test_x >= WINDOW_WIDTH or test_y < 0 or test_y >= WINDOW_HEIGHT:
                continue

            if (test_x, test_y) in self.cycle.trail or (test_x, test_y) in player_cycle.trail:
                continue

            # Evaluate this direction
            space = self.count_open_space(self.cycle.x, self.cycle.y, direction, player_cycle)
            offensive_score = self.evaluate_offensive_move(direction, player_cycle)

            # Combined score: balance survival and offense based on aggression
            # At very high aggression, survival matters much less
            survival_weight = max(0.1, 1.0 - self.aggression * 0.7)
            survival_score = space * survival_weight
            total_score = survival_score + offensive_score

            safe_dirs.append((direction, total_score, space, offensive_score))

        if not safe_dirs:
            return current_dir

        # Sort by total score (highest first)
        safe_dirs.sort(key=lambda x: x[1], reverse=True)

        # Strategic decision making based on current aggression and risk
        best_move = safe_dirs[0]
        best_space = best_move[2]

        # Risk assessment: if best move has very little space, consider alternatives
        if best_space < 3 and len(safe_dirs) > 1:
            # Look for safer alternatives
            safer_moves = [m for m in safe_dirs if m[2] >= 5]
            if safer_moves and self.aggression < 0.8:
                # Choose safest move with decent score
                safer_moves.sort(key=lambda x: (x[2], x[1]), reverse=True)
                return safer_moves[0][0]

        # At extreme aggression (>0.9), take risks for offense
        if self.aggression > 0.9:
            # High risk, high reward - take highest scoring move
            return safe_dirs[0][0]

        # Moderate to high aggression: weighted decision
        elif self.aggression > 0.7:
            # 70% chance to take best move, 30% to consider safety
            if random.random() < 0.7:
                return safe_dirs[0][0]
            else:
                # Pick move with best space among top 3 options
                top_moves = safe_dirs[:min(3, len(safe_dirs))]
                top_moves.sort(key=lambda x: x[2], reverse=True)
                return top_moves[0][0]

        # Balanced play: consider both offense and defense
        elif self.aggression > 0.4:
            # Choose based on combined factors with variance
            if random.random() < self.aggression:
                return safe_dirs[0][0]
            else:
                # Favor survival while still being opportunistic
                safe_dirs.sort(key=lambda x: (x[2] * 0.65 + x[1] * 0.35), reverse=True)
                return safe_dirs[0][0]

        # Defensive play: prioritize survival
        else:
            # Focus on space, but don't ignore opportunities
            safe_dirs.sort(key=lambda x: (x[2] * 0.8 + x[3] * 0.2), reverse=True)
            return safe_dirs[0][0]

class Game:
    def __init__(self):
        global WINDOW_WIDTH, WINDOW_HEIGHT

        # Set up fullscreen or windowed mode
        if FULLSCREEN:
            # Use (0, 0) to automatically use desktop resolution in fullscreen
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            # Get actual screen dimensions from the surface
            WINDOW_WIDTH = self.screen.get_width()
            WINDOW_HEIGHT = self.screen.get_height()
        else:
            WINDOW_WIDTH = DEFAULT_WIDTH
            WINDOW_HEIGHT = DEFAULT_HEIGHT
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        pygame.display.set_caption("MAX TRON - Lightcycle Battle!")

        # Load sprites AFTER display is initialized
        load_bike_sprites()

        self.clock = pygame.time.Clock()
        # Use bold, futuristic-looking system fonts
        self.font_large = pygame.font.SysFont('arial', 90, bold=True)
        self.font_medium = pygame.font.SysFont('arial', 56, bold=True)
        self.font_small = pygame.font.SysFont('arial', 40, bold=True)
        self.font_tiny = pygame.font.SysFont('arial', 32, bold=False)

        self.game_mode = None  # 'single' or 'two_player'
        self.difficulty = None  # 'easy', 'medium', 'hard', 'insane'
        self.state = 'difficulty_menu'  # 'difficulty_menu', 'mode_menu', 'playing', 'game_over'
        self.fullscreen = FULLSCREEN

        self.player1 = None
        self.player2 = None
        self.ai = None

        self.winner = None

    def render_futuristic_text(self, text, font, color, outline_color=None):
        """Render text with futuristic glow and outline effects"""
        if outline_color is None:
            outline_color = tuple(c // 3 for c in color)

        # Create the main text surface
        text_surface = font.render(text, True, color)
        w, h = text_surface.get_size()

        # Create a larger surface for glow effects
        glow_surface = pygame.Surface((w + 20, h + 20), pygame.SRCALPHA)

        # Multiple glow layers (outer to inner)
        glow_layers = [
            (outline_color, 8, 128),
            (outline_color, 5, 180),
            (tuple(min(255, c * 2) for c in outline_color), 3, 220)
        ]

        for glow_color, offset, alpha in glow_layers:
            for dx in range(-offset, offset + 1):
                for dy in range(-offset, offset + 1):
                    if dx*dx + dy*dy <= offset*offset:
                        glow_text = font.render(text, True, glow_color)
                        glow_text.set_alpha(alpha)
                        glow_surface.blit(glow_text, (10 + dx, 10 + dy))

        # Add the main text on top
        glow_surface.blit(text_surface, (10, 10))

        return glow_surface

    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        global WINDOW_WIDTH, WINDOW_HEIGHT

        self.fullscreen = not self.fullscreen

        if self.fullscreen:
            # Use (0, 0) to automatically use desktop resolution
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            # Get actual screen dimensions
            WINDOW_WIDTH = self.screen.get_width()
            WINDOW_HEIGHT = self.screen.get_height()
        else:
            WINDOW_WIDTH = DEFAULT_WIDTH
            WINDOW_HEIGHT = DEFAULT_HEIGHT
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    def show_difficulty_menu(self):
        self.screen.fill(DARK_BLUE)

        # Add scanline effect
        for i in range(0, WINDOW_HEIGHT, 4):
            pygame.draw.line(self.screen, (0, 30, 50), (0, i), (WINDOW_WIDTH, i), 1)

        # Title with futuristic glow
        title = self.render_futuristic_text("MAX TRON", self.font_large, CYAN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        # Decorative line under title
        pygame.draw.line(self.screen, CYAN, (WINDOW_WIDTH // 2 - 200, 150), (WINDOW_WIDTH // 2 + 200, 150), 3)
        pygame.draw.line(self.screen, NEON_BLUE, (WINDOW_WIDTH // 2 - 200, 152), (WINDOW_WIDTH // 2 + 200, 152), 1)

        subtitle = self.render_futuristic_text("SELECT DIFFICULTY", self.font_small, ORANGE)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, 200))
        self.screen.blit(subtitle, subtitle_rect)

        # Difficulty options with brackets
        option1 = self.render_futuristic_text("[ 1 ]  EASY", self.font_medium, (100, 255, 100))
        option1_rect = option1.get_rect(center=(WINDOW_WIDTH // 2, 300))
        self.screen.blit(option1, option1_rect)

        option2 = self.render_futuristic_text("[ 2 ]  MEDIUM", self.font_medium, YELLOW)
        option2_rect = option2.get_rect(center=(WINDOW_WIDTH // 2, 380))
        self.screen.blit(option2, option2_rect)

        option3 = self.render_futuristic_text("[ 3 ]  HARD", self.font_medium, ORANGE)
        option3_rect = option3.get_rect(center=(WINDOW_WIDTH // 2, 460))
        self.screen.blit(option3, option3_rect)

        option4 = self.render_futuristic_text("[ 4 ]  INSANE", self.font_medium, (255, 50, 50))
        option4_rect = option4.get_rect(center=(WINDOW_WIDTH // 2, 540))
        self.screen.blit(option4, option4_rect)

        option5 = self.render_futuristic_text("[ 5 ]  HACKER", self.font_medium, (255, 0, 255))
        option5_rect = option5.get_rect(center=(WINDOW_WIDTH // 2, 620))
        self.screen.blit(option5, option5_rect)

        # Warning for HACKER mode with pulsing effect
        warning = self.render_futuristic_text("NEARLY IMPOSSIBLE!", self.font_small, (255, 0, 255))
        warning_rect = warning.get_rect(center=(WINDOW_WIDTH // 2, 690))
        self.screen.blit(warning, warning_rect)

        # Description
        desc = self.render_futuristic_text("AI: FASTER | SMARTER | AGGRESSIVE", self.font_tiny, WHITE)
        desc_rect = desc.get_rect(center=(WINDOW_WIDTH // 2, 780))
        self.screen.blit(desc, desc_rect)

        # Fullscreen hint
        fullscreen_text = "[ F11 ] FULLSCREEN" if not self.fullscreen else "[ F11 ] WINDOWED"
        fs_hint = self.render_futuristic_text(fullscreen_text, self.font_tiny, (150, 150, 200))
        fs_rect = fs_hint.get_rect(center=(WINDOW_WIDTH // 2, 850))
        self.screen.blit(fs_hint, fs_rect)

        pygame.display.flip()

    def show_mode_menu(self):
        self.screen.fill(DARK_BLUE)

        # Add scanline effect
        for i in range(0, WINDOW_HEIGHT, 4):
            pygame.draw.line(self.screen, (0, 30, 50), (0, i), (WINDOW_WIDTH, i), 1)

        # Title with futuristic glow
        title = self.render_futuristic_text("MAX TRON", self.font_large, CYAN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        # Decorative line under title
        pygame.draw.line(self.screen, CYAN, (WINDOW_WIDTH // 2 - 200, 150), (WINDOW_WIDTH // 2 + 200, 150), 3)
        pygame.draw.line(self.screen, NEON_BLUE, (WINDOW_WIDTH // 2 - 200, 152), (WINDOW_WIDTH // 2 + 200, 152), 1)

        subtitle = self.render_futuristic_text("LIGHTCYCLE BATTLE", self.font_small, ORANGE)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, 200))
        self.screen.blit(subtitle, subtitle_rect)

        # Show selected difficulty with tech frame
        diff_text = self.render_futuristic_text(f">> {self.difficulty.upper()} <<", self.font_small, PURPLE)
        diff_rect = diff_text.get_rect(center=(WINDOW_WIDTH // 2, 270))
        self.screen.blit(diff_text, diff_rect)

        # Menu options with tech styling
        option1 = self.render_futuristic_text("[ 1 ]  VS COMPUTER", self.font_medium, YELLOW)
        option1_rect = option1.get_rect(center=(WINDOW_WIDTH // 2, 380))
        self.screen.blit(option1, option1_rect)

        option2 = self.render_futuristic_text("[ 2 ]  TWO PLAYERS", self.font_medium, PURPLE)
        option2_rect = option2.get_rect(center=(WINDOW_WIDTH // 2, 480))
        self.screen.blit(option2, option2_rect)

        # Decorative separator
        pygame.draw.line(self.screen, (100, 100, 150), (WINDOW_WIDTH // 2 - 300, 560), (WINDOW_WIDTH // 2 + 300, 560), 2)

        # Instructions with icons
        inst1 = self.render_futuristic_text("P1: ↑ ↓ ← →", self.font_small, CYAN)
        inst1_rect = inst1.get_rect(center=(WINDOW_WIDTH // 2, 620))
        self.screen.blit(inst1, inst1_rect)

        inst2 = self.render_futuristic_text("P2: W A S D", self.font_small, ORANGE)
        inst2_rect = inst2.get_rect(center=(WINDOW_WIDTH // 2, 680))
        self.screen.blit(inst2, inst2_rect)

        # Back option
        back = self.render_futuristic_text("[ ESC ]  BACK", self.font_tiny, WHITE)
        back_rect = back.get_rect(center=(WINDOW_WIDTH // 2, 800))
        self.screen.blit(back, back_rect)

        pygame.display.flip()

    def start_game(self, mode):
        self.game_mode = mode
        self.state = 'playing'

        # Get difficulty settings
        settings = DIFFICULTY_SETTINGS[self.difficulty]

        # Create player 1 (cyan cycle on left)
        self.player1 = LightCycle(100, WINDOW_HEIGHT // 2, CYAN, Direction.RIGHT, sprite=BIKE_SPRITE_CYAN)

        if mode == 'single':
            # Create AI opponent (orange cycle on right)
            self.player2 = LightCycle(WINDOW_WIDTH - 100, WINDOW_HEIGHT // 2, ORANGE, Direction.LEFT, sprite=BIKE_SPRITE_ORANGE)
            self.ai = AggressiveAI(
                self.player2,
                lookahead_depth=settings['ai_lookahead'],
                aggression=settings['aggression']
            )
        else:
            # Create player 2 (orange cycle on right)
            self.player2 = LightCycle(WINDOW_WIDTH - 100, WINDOW_HEIGHT // 2, ORANGE, Direction.LEFT, sprite=BIKE_SPRITE_ORANGE)
            self.ai = None

        self.winner = None

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                # F11 toggles fullscreen (works in any state)
                if event.key == pygame.K_F11:
                    self.toggle_fullscreen()
                    continue

                if self.state == 'difficulty_menu':
                    if event.key == pygame.K_1:
                        self.difficulty = 'easy'
                        self.state = 'mode_menu'
                    elif event.key == pygame.K_2:
                        self.difficulty = 'medium'
                        self.state = 'mode_menu'
                    elif event.key == pygame.K_3:
                        self.difficulty = 'hard'
                        self.state = 'mode_menu'
                    elif event.key == pygame.K_4:
                        self.difficulty = 'insane'
                        self.state = 'mode_menu'
                    elif event.key == pygame.K_5:
                        self.difficulty = 'hacker'
                        self.state = 'mode_menu'

                elif self.state == 'mode_menu':
                    if event.key == pygame.K_1:
                        self.start_game('single')
                    elif event.key == pygame.K_2:
                        self.start_game('two_player')
                    elif event.key == pygame.K_ESCAPE:
                        self.state = 'difficulty_menu'

                elif self.state == 'playing':
                    # Player 1 controls (Arrow keys)
                    if event.key == pygame.K_UP:
                        self.player1.change_direction(Direction.UP)
                    elif event.key == pygame.K_DOWN:
                        self.player1.change_direction(Direction.DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.player1.change_direction(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.player1.change_direction(Direction.RIGHT)

                    # Player 2 controls (WASD) - only in two player mode
                    if self.game_mode == 'two_player':
                        if event.key == pygame.K_w:
                            self.player2.change_direction(Direction.UP)
                        elif event.key == pygame.K_s:
                            self.player2.change_direction(Direction.DOWN)
                        elif event.key == pygame.K_a:
                            self.player2.change_direction(Direction.LEFT)
                        elif event.key == pygame.K_d:
                            self.player2.change_direction(Direction.RIGHT)

                elif self.state == 'game_over':
                    if event.key == pygame.K_SPACE:
                        self.state = 'difficulty_menu'
                    elif event.key == pygame.K_r:
                        self.start_game(self.game_mode)

        return True

    def update(self):
        if self.state != 'playing':
            return

        # AI decision
        if self.ai and self.player2.alive:
            new_dir = self.ai.get_next_direction(self.player1)
            self.player2.change_direction(new_dir)

        # Move cycles
        self.player1.move()
        self.player2.move()

        # Check collisions
        p1_collision = self.player1.check_collision(self.player2)
        p2_collision = self.player2.check_collision(self.player1)

        # Determine winner
        if not self.player1.alive or not self.player2.alive:
            self.state = 'game_over'
            if not self.player1.alive and not self.player2.alive:
                self.winner = 'tie'
            elif not self.player1.alive:
                self.winner = 'player2'
            else:
                self.winner = 'player1'

    def draw(self):
        self.screen.fill(DARK_BLUE)

        if self.state == 'difficulty_menu':
            self.show_difficulty_menu()
        elif self.state == 'mode_menu':
            self.show_mode_menu()
        elif self.state == 'playing':
            # Draw grid lines (white)
            for x in range(0, WINDOW_WIDTH, GRID_SIZE * 5):
                pygame.draw.line(self.screen, WHITE, (x, 0), (x, WINDOW_HEIGHT), 1)
            for y in range(0, WINDOW_HEIGHT, GRID_SIZE * 5):
                pygame.draw.line(self.screen, WHITE, (0, y), (WINDOW_WIDTH, y), 1)

            # Draw cycles
            self.player1.draw(self.screen)
            self.player2.draw(self.screen)

            pygame.display.flip()
        elif self.state == 'game_over':
            # Draw final positions with grid lines (white)
            for x in range(0, WINDOW_WIDTH, GRID_SIZE * 5):
                pygame.draw.line(self.screen, WHITE, (x, 0), (x, WINDOW_HEIGHT), 1)
            for y in range(0, WINDOW_HEIGHT, GRID_SIZE * 5):
                pygame.draw.line(self.screen, WHITE, (0, y), (WINDOW_WIDTH, y), 1)

            self.player1.draw(self.screen)
            self.player2.draw(self.screen)

            # Semi-transparent overlay with scanline effect
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            # Add subtle scanlines on overlay
            for i in range(0, WINDOW_HEIGHT, 6):
                pygame.draw.line(self.screen, (0, 20, 30), (0, i), (WINDOW_WIDTH, i), 1)

            # Winner text with futuristic styling
            if self.winner == 'tie':
                text = self.render_futuristic_text(">> TIE! <<", self.font_large, YELLOW)
            elif self.winner == 'player1':
                if self.game_mode == 'single':
                    text = self.render_futuristic_text(">>> YOU WIN! <<<", self.font_large, CYAN)
                else:
                    text = self.render_futuristic_text("CYAN WINS!", self.font_large, CYAN)
            else:
                if self.game_mode == 'single':
                    text = self.render_futuristic_text("COMPUTER WINS", self.font_large, ORANGE)
                else:
                    text = self.render_futuristic_text("ORANGE WINS!", self.font_large, ORANGE)

            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 250))
            self.screen.blit(text, text_rect)

            # Decorative tech line
            pygame.draw.line(self.screen, CYAN, (WINDOW_WIDTH // 2 - 250, 350), (WINDOW_WIDTH // 2 + 250, 350), 2)

            # Instructions with futuristic styling
            restart = self.render_futuristic_text("[ R ]  REMATCH", self.font_small, WHITE)
            restart_rect = restart.get_rect(center=(WINDOW_WIDTH // 2, 420))
            self.screen.blit(restart, restart_rect)

            menu = self.render_futuristic_text("[ SPACE ]  MENU", self.font_small, WHITE)
            menu_rect = menu.get_rect(center=(WINDOW_WIDTH // 2, 490))
            self.screen.blit(menu, menu_rect)

            pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()

            # Use difficulty-based FPS during gameplay, lower FPS for menus
            if self.state == 'playing' and self.difficulty:
                fps = DIFFICULTY_SETTINGS[self.difficulty]['fps']
            else:
                fps = 30  # Menu FPS

            self.clock.tick(fps)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
