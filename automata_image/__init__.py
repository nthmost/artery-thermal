"""
Automata Image - Generate cellular automata patterns for receipt printing.

Generates various cellular automata patterns that look great when converted to
inverted glitch art (white on black).
"""

from .automata import (
    generate_game_of_life,
    generate_rule_30,
    generate_rule_110,
    generate_rule_90,
    generate_random_automaton,
    AutomataConfig
)

__all__ = [
    'generate_game_of_life',
    'generate_rule_30',
    'generate_rule_110',
    'generate_rule_90',
    'generate_random_automaton',
    'AutomataConfig'
]
