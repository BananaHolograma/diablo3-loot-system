# Seleccion de personaje y nivel
from typing import List, Dict, Any,  Annotated, cast
from random import randint, random, randrange, shuffle, choice
from os import path
import json
from character import Character, MONK

"""
1. Determinar el pool a utilizar segun el origen
2. Mergear objetos de conjunto y legendarios propios del personaje elegido (si corresponde)
3. Aplicar los modificadores segun condiciones (nivel pj, dificultad, tipo de origen, etc)
4. Ejecutar rolls entre el numero min y maximo que haya resultado teniendo en cuenta las drop chances y weight de cada item en entries
6. Se seleccionan las entries en base a la propiedad weight con el calculo adecuado
7. Se aplican los calculos de drop change para los elementos que han sido seleccionados de la loot table
5. Devolver una estructura json con los entries que han salido para este proceso individual de loot
"""

# ORIGINS FOR POOL
CHEST = 'CHEST'
ENEMY = 'ENEMY'
MAP_EVENT = 'EVENT'

with open('data/loot_table.json', 'r') as loot_table:
    AVAILABLE_POOLS = json.load(loot_table)

GAME_ITEMS: dict = {}

with open('data/equipment/legendary_equipment.json', 'r') as legendary_equipment:
    GAME_ITEMS['LEGENDARY_EQUIPMENT'] = json.load(legendary_equipment)

with open('data/equipment/rare_equipment.json', 'r') as rare_equipment:
    GAME_ITEMS['RARE_EQUIPMENT'] = json.load(rare_equipment)

with open('data/equipment/magic_equipment.json', 'r') as magic_equipment:
    GAME_ITEMS['MAGIC_EQUIPMENT'] = json.load(magic_equipment)

with open('data/equipment/normal_equipment.json', 'r') as normal_equipment:
    GAME_ITEMS['NORMAL_EQUIPMENT'] = json.load(normal_equipment)

with open('data/equipment/character_set_equipment.json', 'r') as character_set_equipment:
    GAME_ITEMS['CHARACTER_SET_EQUIPMENT'] = json.load(character_set_equipment)

with open('data/gems/gems.json', 'r') as gems:
    GAME_ITEMS['GEMS'] = json.load(gems)


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
        shuffle(safe_entries)

        return safe_entries[:amount]


def choose_items_with_weight_calculation(pool: Dict) -> List[Dict]:
    number_of_rolls = randint(pool['rolls']['min'], pool['rolls']['max']) + 1
    total_weight = sum([entry['weight'] for entry in pool['entries']])
    result = []

    for _ in range(0, number_of_rolls):
        for item in pool['entries']:
            probability = item['weight'] / total_weight

            # ¿quitar de la lista una vez añadido para evitar duplicados, o generar duplicados a proposito?
            if random() <= probability:
                result.append(item)

    return result


def apply_drop_chance(items: List[Dict], modifier: Annotated[float, lambda x: 0.0 <= x <= 1.0] = None) -> List[Dict]:
    safe_items = items.copy()
    result = []

    for item in safe_items:
        chance = item['drop']['chance']
        max_chance = item['drop']['max_chance']
        final_chance = chance

        if modifier is not None:
            new_chance = chance + modifier
            final_chance = new_chance if new_chance < max_chance else max_chance

        if random() <= final_chance:
            result.append(item)

    return result


def loot_gems(character: Character) -> List[Dict]:
    looted_gems = []
    max_quantity = 3
    enabled_categories = ['SQUARE', 'FLAWLESS SQUARE', 'STAR']

    if character.level >= 61:
        max_quantity = 6
        enabled_categories += ['MARQUISE', 'IMPERIAL']

    for _ in range(randrange(max_quantity) + 1):
        looted_gems.append({
            "type": choice(GAME_ITEMS['GEMS']["NORMAL"]["TYPES"]),
            "category": choice(enabled_categories),
            "quantity": 1
        })

    return looted_gems


def start_loot(character: Character, origin: str) -> List[Dict]:
    selected_pool: dict = build_pool(character, origin)

    selected_items = choose_items_with_weight_calculation(selected_pool)
    dropped_items = apply_drop_chance(selected_items, 0.05)
    gold = randrange(10000) + 1
    gems = loot_gems(character)

    return {"items": dropped_items, "gold": gold, "gems": gems}


def build_pool(character: Character, origin: str) -> dict:
    pool_template: dict = AVAILABLE_POOLS.copy()
    translated_origin: list[str] = origin.upper().split('.')

    for key in translated_origin:
        if key in pool_template:
            pool_template = pool_template[key]
        else:
            raise KeyError(
                f"The access key {key} does not exists in the available pools for the value {origin}")

    return load_item_entries_based_on_pool_rules(pool_template)


def load_item_entries_based_on_pool_rules(selected_pool: dict) -> List[Dict]:
    key: str
    for key in selected_pool['rules'].keys():
        equipment_rarity = key.strip().upper()

        if equipment_rarity in GAME_ITEMS:
            items = GAME_ITEMS[equipment_rarity].copy()
            amount_rule = selected_pool['rules'][key]['amount']
            shuffle(items)

            selected_pool['entries'] += items[:amount_rule]

    return selected_pool


monk = Character(level=61, character_class=MONK)

looted = start_loot(monk, 'chest.diabolic')

print(json.dumps(looted, indent=4))
