# Seleccion de personaje y nivel
from typing import TypeVar, List, Dict
from random import randint, choice
import json

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

with open('data/loot_table.json', 'r') as loot_table:
    AVAILABLE_POOLS = json.load(loot_table)

with open('data/equipment/legendary_equipment.json', 'r') as legendary_equipment:
    LEGENDARY_EQUIPMENT = json.load(legendary_equipment)

with open('data/equipment/rare_equipment.json', 'r') as rare_equipment:
    RARE_EQUIPMENT = json.load(rare_equipment)

with open('data/equipment/magic_equipment.json', 'r') as magic_equipment:
    MAGIC_EQUIPMENT = json.load(magic_equipment)

with open('data/equipment/normal_equipment.json', 'r') as normal_equipment:
    NORMAL_EQUIPMENT = json.load(normal_equipment)

LEVEL = TypeVar('LEVEL')
CHARACTER_CLASS = TypeVar('CHARACTER_CLASS')


def get_random_elements_from_entries(entries: List[Dict], amount: int) -> List[Dict]:
    max_entries = len(entries)
    if amount < 0:
        raise ValueError(
            "The value for parameter amount must be greater than zero")
    elif amount > max_entries:
        raise ValueError(
            f"The amount {amount} is more than the total items on the list {max_entries}")

    else:
        safe_entries = entries.copy()
        result = []

        for _ in range(0, amount + 1 if amount == 1 else amount):
            selection = choice(safe_entries)
            result.append(selection)
            safe_entries.remove(selection)

        return result


AVAILABLE_POOLS['CHEST']['NORMAL']['entries'] = NORMAL_EQUIPMENT.copy(
) + get_random_elements_from_entries(MAGIC_EQUIPMENT, randint(2, 4)) + get_random_elements_from_entries(RARE_EQUIPMENT, randint(1, 2))
AVAILABLE_POOLS['CHEST']['BEAMING']['entries'] = get_random_elements_from_entries(AVAILABLE_POOLS['CHEST']['NORMAL']['entries'], randint(1, 3)) + \
    RARE_EQUIPMENT.copy()
AVAILABLE_POOLS['CHEST']['DIABOLIC']['entries'] = get_random_elements_from_entries(RARE_EQUIPMENT, randint(2, 4)) + \
    LEGENDARY_EQUIPMENT.copy()


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
    selected_pool: dict = build_pool(character, origin)

    print(json.dumps(selected_pool, indent=4))


def build_pool(character: Character, origin: str) -> dict:
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

start_loot(monk, 'chest.beaming')
