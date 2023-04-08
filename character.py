from random import randint, choice
from typing import TypeVar, Annotated

# CHARACTER CLASSES
BARBARIAN = 'barbarian'
WIZARD = 'wizard'
NECROMANCER = 'necromancer'
WITCH_DOCTOR = 'witch doctor'
DEMON_HUNTER = 'demon hunter'
CRUSADER = 'crusader'
MONK = 'monk'

GAME_CLASSES = [
    BARBARIAN, WIZARD, NECROMANCER, WITCH_DOCTOR, DEMON_HUNTER, CRUSADER,
    MONK
]

CHARACTER_CLASS = TypeVar('CHARACTER_CLASS')


class Character:
    def __init__(self, level: int = None, character_class: str = None) -> None:
        self.level: int = self._ensure_level_is_on_valid_range(
            level) if level is not None else randint(1, 70)

        self.character_class: str = self._ensure_character_class_is_implemented(
            character_class or choice(GAME_CLASSES))

        self.gold: float = 0

    def _ensure_level_is_on_valid_range(self, value: Annotated[int, lambda x: 1 <= x <= 70]) -> int:
        if (value < 1 or value > 70):
            raise ValueError(
                f"The level {value} is not allowed, the system can handle levels between 1 and 70"
            )
        return value

    def _ensure_character_class_is_implemented(self, value: CHARACTER_CLASS) -> CHARACTER_CLASS:
        if value.lower() not in GAME_CLASSES:
            raise ValueError(
                f"The character class {value} is not implemented on diablo 3")

        return value
