# Automata Image

Generate cellular automata patterns for thermal receipt printing.

## What are Cellular Automata?

Cellular automata are mathematical models where cells in a grid evolve based on simple rules. They can create complex, beautiful patterns from simple initial conditions.

## Available Automata

### Rule 30 - Chaotic Pattern
```python
from automata_image import generate_rule_30, AutomataConfig

config = AutomataConfig(width=120, height=120)
img = generate_rule_30(config)
```

**Pattern:** Chaotic, random-looking expansion from a single point.
**Discovered by:** Stephen Wolfram
**Properties:** Despite simple rules, produces seemingly random output. Used in Mathematica's random number generator.

### Rule 90 - Sierpinski Triangle
```python
img = generate_rule_90(config)
```

**Pattern:** Creates the famous Sierpinski triangle fractal.
**Properties:** Self-similar fractal pattern. Beautiful geometric structure.

### Rule 110 - Turing Complete
```python
img = generate_rule_110(config)
```

**Pattern:** Complex structures with "gliders" and interactions.
**Properties:** Proven to be Turing complete - can theoretically compute anything.
**Note:** Looks better with random initial seed (automatically applied).

### Conway's Game of Life
```python
from automata_image import generate_game_of_life

img = generate_game_of_life(config, generations=100)
```

**Pattern:** 2D cellular automaton with emergent behavior.
**Rules:**
- Live cell with 2-3 neighbors survives
- Dead cell with 3 neighbors becomes alive
- All other cells die or stay dead

**Properties:** Creates "gliders," "blinkers," and complex interacting structures.

### Random Automaton
```python
from automata_image import generate_random_automaton

img, rule_number = generate_random_automaton(config)
print(f"Generated using rule {rule_number}")
```

**Pattern:** Randomly selects from a curated list of visually interesting rules.
**Returns:** Tuple of (image, rule_number_used)

## Configuration

```python
from automata_image import AutomataConfig

config = AutomataConfig(
    width=120,       # Image width in pixels
    height=120,      # Image height (or generations for 1D CA)
    density=0.3      # Initial random cell density (0.0 - 1.0)
)
```

## Printing on Thermal Receipt

Automata look best when inverted (white pattern on black background):

```python
from artery.glitch_art import image_to_glitch_art
from artery import ArteryPrinter

# Generate automaton
img = generate_rule_30()

# Convert to inverted glitch art
glitch = image_to_glitch_art(
    img,
    width=384,
    invert=True,  # White on black
    sparsity=0.05
)

# Print
printer = ArteryPrinter()
printer.print_image(glitch)
printer.finish()
```

## How 1D Rules Work

1D cellular automata rules are numbered 0-255 (Wolfram notation).

Each rule defines how a cell evolves based on itself and its two neighbors:
- Input: 3-bit pattern (left, center, right)
- Output: New center cell value

Rule number is 8-bit binary showing outputs for all 8 possible inputs.

Example: **Rule 30** = `00011110` in binary

```
111 → 0
110 → 0
101 → 0
100 → 1
011 → 1
010 → 1
001 → 1
000 → 0
```

## Example Gallery

Run `test_automata.py` to generate and print examples of all automata types.

## References

- [Wolfram MathWorld - Elementary Cellular Automaton](https://mathworld.wolfram.com/ElementaryCellularAutomaton.html)
- [Wolfram Atlas of Simple Programs](https://www.wolframscience.com/nks/atlas/)
- [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)
