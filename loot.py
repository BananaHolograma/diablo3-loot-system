# Seleccion de personaje y nivel
from typing import TypeVar, List
from random import randint, choice

# CHARACTER CLASSES
BARBARIAN = 'barbarian'
WIZARD = 'wizard'
NECROMANCER = 'necromancer'
WITCH_DOCTOR = 'witch doctor'
DEMON_HUNTER = 'demon hunter'
CRUSADER = 'crusader'
MONK = 'monk'

# ORIGINS FOR POOL
CHEST = 'CHEST'
ENEMY = 'ENEMY'
MAP_EVENT = 'EVENT'

AVAILABLE_POOLS = {
    CHEST: {
        "NORMAL": {
            "rolls": {
                "min": 1, "max": 6
            },
            "entries": [{
                "quantity": 1,
                "type": "equipment:helm",
                "name": "normal helm",
                "weight": 1,
                "drop_chance": 35
            }, {
                "quantity": 1,
                "type": "equipment:one-handed-sword",
                "name": "sword of pytagoras",
                "weight": 2,
                "drop_chance": 35
            }]
        },
        "BEAMING": {
            "rolls": {
                "min": 6, "max": 12
            },
        },
        "DIABOLIC": {
            "rolls": {
                "min": 10, "max": 15
            },
        }
    }
}

LEVEL = TypeVar('LEVEL')
CHARACTER_CLASS = TypeVar('CHARACTER_CLASS')


class Character:
    def __init__(self, level: int = None, character_class: str = None) -> None:
        self.level: int = self._ensure_level_is_on_valid_range(
            level) if level is not None else randint(1, 70)

        self.character_class: str = self._ensure_character_class_is_implemented(
            character_class or choice(game_classes()))

    def _ensure_level_is_on_valid_range(self, value: LEVEL) -> LEVEL:
        if (value < 1 or value > 70):
            raise ValueError(
                f"The level {value} is not allowed, the system can handle levels between 1 and 70"
            )
        return value

    def _ensure_character_class_is_implemented(self, value: CHARACTER_CLASS) -> CHARACTER_CLASS:
        if value not in game_classes():
            raise ValueError(
                f"The character class {value} is not implemented on diablo 3")

        return value


def game_classes() -> List[str]:
    return [
        BARBARIAN, WIZARD, NECROMANCER, WITCH_DOCTOR, DEMON_HUNTER, CRUSADER,
        MONK
    ]


"""
1. Determinar el pool a utilizar segun el origen
2. Mergear objetos de conjunto y legendarios propios del personaje elegido (si corresponde)
3. Aplicar los modificadores segun condiciones (nivel pj, dificultad, tipo de origen, etc)
4. Ejecutar rolls entre el numero min y maximo que haya resultado teniendo en cuenta las drop chances y weight de cada item en entries
6. Se seleccionan las entries en base a la propiedad weight con el calculo adecuado
7. Se aplican los calculos de drop change para los elementos que han sido seleccionados de la loot table
5. Devolver una estructura json con los entries que han salido para este proceso individual de loot
"""


def start_loot(character: Character, origin: str):
    selected_pool: dict = build_pool_based_on_origin(origin)

    print(selected_pool)


def build_pool_based_on_origin(origin: str) -> dict:
    translated_origin: list[str] = origin.upper().split('.')
    pool_template: dict = AVAILABLE_POOLS.copy()

    for key in translated_origin:
        if key in pool_template:
            pool_template = pool_template[key]
        else:
            raise KeyError(
                f"The access key {key} does not exists in the available pools for the value {origin}")

    return pool_template


monk = Character(level=18, character_class=MONK)

start_loot(monk, 'chest.normal')
