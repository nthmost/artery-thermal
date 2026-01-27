"""Cellular automata generators for receipt art."""

from PIL import Image
import random
from dataclasses import dataclass


@dataclass
class AutomataConfig:
    """Configuration for cellular automata generation."""
    width: int = 120
    height: int = 120
    density: float = 0.3  # Initial random density for seeds
    iterations: int = None  # Auto-calculated if None


def apply_rule(left, center, right, rule_number):
    """Apply a 1D cellular automaton rule.

    Args:
        left, center, right: Binary values (0 or 1)
        rule_number: Wolfram rule number (0-255)

    Returns:
        New center cell value (0 or 1)
    """
    # Convert rule number to 8-bit binary
    rule_binary = format(rule_number, '08b')

    # Calculate index based on neighborhood
    index = 7 - (left * 4 + center * 2 + right)

    return int(rule_binary[index])


def generate_1d_automaton(rule_number, width=120, height=120, initial_seed=None):
    """Generate a 1D cellular automaton pattern.

    Args:
        rule_number: Wolfram rule number (0-255)
        width: Width in pixels
        height: Number of generations
        initial_seed: List of initial values, or None for single center cell

    Returns:
        PIL Image
    """
    # Create blank image
    img = Image.new('L', (width, height), color=255)
    pixels = img.load()

    # Initialize first row
    if initial_seed is None:
        # Single cell in center
        current = [0] * width
        current[width // 2] = 1
    else:
        current = initial_seed[:width]

    # Draw first row
    for x in range(width):
        if current[x]:
            pixels[x, 0] = 0

    # Generate subsequent rows
    for y in range(1, height):
        next_row = []

        for x in range(width):
            # Get neighbors (with wrapping)
            left = current[(x - 1) % width]
            center = current[x]
            right = current[(x + 1) % width]

            # Apply rule
            new_cell = apply_rule(left, center, right, rule_number)
            next_row.append(new_cell)

            # Draw pixel
            if new_cell:
                pixels[x, y] = 0

        current = next_row

    return img


def generate_rule_30(config=None):
    """Generate Rule 30 cellular automaton (chaotic).

    Rule 30 is a chaotic pattern discovered by Stephen Wolfram.

    Args:
        config: AutomataConfig or None for defaults

    Returns:
        PIL Image
    """
    config = config or AutomataConfig()
    return generate_1d_automaton(30, config.width, config.height)


def generate_rule_110(config=None):
    """Generate Rule 110 cellular automaton (Turing complete).

    Rule 110 is proven to be Turing complete.

    Args:
        config: AutomataConfig or None for defaults

    Returns:
        PIL Image
    """
    config = config or AutomataConfig()

    # Rule 110 looks better with random initial seed
    seed = [random.randint(0, 1) if random.random() < config.density else 0
            for _ in range(config.width)]

    return generate_1d_automaton(110, config.width, config.height, seed)


def generate_rule_90(config=None):
    """Generate Rule 90 cellular automaton (Sierpinski triangle).

    Rule 90 produces the Sierpinski triangle pattern.

    Args:
        config: AutomataConfig or None for defaults

    Returns:
        PIL Image
    """
    config = config or AutomataConfig()
    return generate_1d_automaton(90, config.width, config.height)


def generate_game_of_life(config=None, generations=None):
    """Generate Conway's Game of Life pattern.

    Args:
        config: AutomataConfig or None for defaults
        generations: Number of generations to simulate (default: height)

    Returns:
        PIL Image (composite of all generations)
    """
    config = config or AutomataConfig()
    generations = generations or config.height

    width, height = config.width, config.height

    # Initialize grid with random cells
    grid = [[random.randint(0, 1) if random.random() < config.density else 0
             for _ in range(width)] for _ in range(height)]

    # Create image to accumulate all generations
    img = Image.new('L', (width, height), color=255)
    pixels = img.load()

    # Run simulation
    for gen in range(generations):
        # Draw current state
        for y in range(height):
            for x in range(width):
                if grid[y][x]:
                    pixels[x, y] = 0

        # Calculate next generation
        new_grid = [[0 for _ in range(width)] for _ in range(height)]

        for y in range(height):
            for x in range(width):
                # Count live neighbors
                neighbors = 0
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        ny = (y + dy) % height
                        nx = (x + dx) % width
                        neighbors += grid[ny][nx]

                # Apply Game of Life rules
                if grid[y][x]:  # Cell is alive
                    if neighbors in [2, 3]:
                        new_grid[y][x] = 1  # Survive
                else:  # Cell is dead
                    if neighbors == 3:
                        new_grid[y][x] = 1  # Birth

        grid = new_grid

    return img


def generate_random_automaton(config=None):
    """Generate a random 1D cellular automaton rule.

    Args:
        config: AutomataConfig or None for defaults

    Returns:
        PIL Image, rule_number used
    """
    config = config or AutomataConfig()

    # Pick a random rule that tends to produce interesting patterns
    # Some rules produce nothing, some produce solid blocks
    # These are curated to be visually interesting
    interesting_rules = [
        30, 45, 54, 57, 60, 62, 73, 75, 86, 89, 90, 94,
        102, 105, 106, 110, 118, 122, 124, 126, 129,
        135, 137, 146, 149, 150, 151, 153, 154, 161,
        165, 167, 169, 182, 183, 195, 225
    ]

    rule = random.choice(interesting_rules)

    # Sometimes use random seed, sometimes single center cell
    seed = None
    if random.random() < 0.5:
        seed = [random.randint(0, 1) if random.random() < config.density else 0
                for _ in range(config.width)]

    img = generate_1d_automaton(rule, config.width, config.height, seed)

    return img, rule
