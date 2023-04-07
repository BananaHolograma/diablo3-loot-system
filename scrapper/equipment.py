import requests
import requests_cache
import re
from json import dump, load, JSONDecodeError
from os import makedirs, path
from bs4 import BeautifulSoup
from bs4.element import Tag

base_url: str = "https://us.diablo3.blizzard.com/en-us"

requests_cache.install_cache(
    cache_name='diablo3-cache', expire_after=3600)


def extract_items_information(base_url: str, category: str):
    item_page = base_url + f"/item/{category}/"

    try:
        response = requests.get(item_page)
        response.raise_for_status()

        scrapper = BeautifulSoup(response.text, "html.parser")

        items = scrapper.find_all(lambda tag: tag.name == 'tr' and ('row1' in tag.get('class', []) or 'row2' in tag.get(
            'class', [])))

        result = {}

        for item in items:
            name: str = extract_item_name(item)
            rarity: str = extract_item_rarity(item)
            armor_range: dict = extract_item_armor_range(item, category)

            item_build = {"quantity": 1,
                          "name": name,
                          "type": f"armor:{category}",
                          "rarity": rarity,
                          "value_range": armor_range
                          }

            if rarity in result:
                result[rarity].append(item_build)
            else:
                result[rarity] = [item_build]

        for rarity in result.keys():
            current_dir = path.dirname(path.abspath(__file__))
            data_directory = path.join(current_dir, '..', 'data', 'equipment')
            makedirs(data_directory, exist_ok=True)
            equipment_filename = f"{rarity}_equipment.json"

            if path.exists(f"{data_directory}/{equipment_filename}"):
                with open(f"{data_directory}/{equipment_filename}", 'r+') as existing_equipment_file:
                    try:
                        actual_content = load(existing_equipment_file)
                    except JSONDecodeError:
                        actual_content = []

                    # Mover el puntero al principio del archivo
                    existing_equipment_file.seek(0)
                    # Borrar todo el contenido existente del archivo
                    existing_equipment_file.truncate()

                    dump(actual_content +
                         result[rarity], existing_equipment_file)
            else:
                with open(f"{data_directory}/{equipment_filename}", 'w') as equipment_file:
                    dump(result[rarity], equipment_file)

    except requests.exceptions.HTTPError as error:
        print(f"Error HTTP: {error}")
        exit()


def extract_item_name(item: Tag) -> str:
    return item.find("h3", class_="subheader-3").find('a').text


def extract_item_rarity(item: Tag) -> str:
    colors = {
        'd3-color-orange': 'legendary',
        'd3-color-yellow': 'rare',
        'd3-color-blue': 'magic',
        'd3-color-white': 'normal',
        'd3-color-green': 'character_set'
    }

    for color, rarity in colors.items():
        if item.find('a', {'class': color}):
            return rarity

    return 'unknown'


def extract_item_armor_range(item: Tag, category: str) -> dict:
    if category not in ['amulet', 'ring']:
        armor_range = item.find(
            'ul', {"class": 'item-armor-armor'}).find('span', {"class": 'value'}).text
        match = re.search(r'(\d+)\s*-\s*(\d+)', armor_range.strip())

        if match:
            return {'min': int(match.group(1)), 'max': int(match.group(2))}

    return {"min": 0, "max": 0}


for equipment in ['helm', 'pauldrons', 'chest-armor', 'bracers', 'gloves', 'belt', 'pants', 'boots', 'amulet', 'ring']:
    print(f"Extracting data for {equipment}...")
    extract_items_information(base_url, equipment)
