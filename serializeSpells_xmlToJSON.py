import os
import xml.etree.ElementTree as ET
import json

xmlFiles = ['data/CoreRulebooks.xml', 'data/XanatharsGuideToEverything.xml', ]


def convert_to_index(s):
    s = s.replace(" ", "-")
    s = s.replace("'", "")
    return s.lower()


# Doing it this way to avoid any missing tag issues... thanks
def find_element(obj, elem):
    result = None
    try:
        result = obj.find(elem).text
    except:
        pass

    return result


# def parse_item(item):
#     item_types = {
#         'A': 'Ranged Weapon',
#         'M': 'Martial Weapon',
#         'LA': 'Light Armor',
#         'MA': 'Medium Armor',
#         'HA': 'Heavy Armor',
#         'S': 'Shield',
#         'ST': 'Staff',
#         'W': 'Worn', 
#         'WD': 'Wand'
#     }

#     desc = item.findall('text')
#     desc_text = []
#     for d in desc:
#         desc_text.append(d.text)
    
#     source = desc_text.pop()
#     desc_text.pop()

#     return {
#         'name': item.find('name').text,
#         'desc': desc_text,
#         'magic': True if item.find('magic').text == '1' else False,
#         'type': item_types[item.find('type').text],
#         'weight': item.find('weight').text,
#         'damage1': item.find('dmg1').text,
#         'damage2': item.find('dmg2').text,
#         'damage_type': item.find('dmgType').text,
#         'range': item.find('range').text,
#         'properties': item.find('property').text,
#         'armor_class': item.find('ac').text,
#         'stealth': 'Disadvantage' if item.find('stealth').text == '1' else None,
#         'strength_req': item.find('strength').text,
#         'source': source
#     }


def parse_spell(spell):
    schools = {
        'A': 'Abjuration',
        'C': 'Conjuration',
        'D': 'Divination',
        'EN': 'Enchantment',
        'EV': 'Evocation',
        'I': 'Illusion',
        'N': 'Necromancy',
        'T': 'Transmutation',
        None: None
    }
    desc = spell.findall('text')
    desc_text = []
    for d in desc:
        desc_text.append(d.text)
    
    source = desc_text.pop()
    desc_filtered = list(filter(None, desc_text))

    class_elem = find_element(spell, 'classes')
    classes = class_elem.split(',')

    spell_name = find_element(spell, 'name')
    return {
        'name': spell_name,
        'index': convert_to_index(spell_name),
        'level': find_element(spell, 'level'),
        'school': schools[find_element(spell, 'school')],
        'casting_time': find_element(spell, 'time'),
        'duration': find_element(spell, 'duration'),
        'range': find_element(spell, 'range'),
        'components': [find_element(spell, 'components')],
        'ritual': False if find_element(spell, 'ritual') == 'NO' else True,
        'desc': desc_filtered,
        'classes': classes,
        'source': source
    }


# Loop through all xml files in list and start spitting out some mad fucking json files
for xmlFile in xmlFiles:
    tree = ET.parse(xmlFile)
    root = tree.getroot()

    filename = os.path.splitext(os.path.basename(xmlFile))[0]
    jsonFilename = f'data/spells_{filename}.json'

    all_spells = {}
    class_spells = {}
    for child in root.iter('spell'):
        item = parse_spell(child)

        index = item['index']
        all_spells[index] = item

        # filter into class lists by level
        for c in item['classes']:
            
            # some malformed xml strings... gotta clean up a bunch to ensure uniformity
            className = c.lstrip().lower()

            if className not in class_spells:
                class_spells[className] = {}
                class_spells[className][int(item['level'])] = []
                class_spells[className][int(item['level'])].append(index)
            else:
                if int(item['level']) not in class_spells[className]:
                    class_spells[className][int(item['level'])] = []
                    class_spells[className][int(item['level'])].append(index)
                else:
                    class_spells[className][int(item['level'])].append(index)


    all_spells['class_lists'] = class_spells

    with open(jsonFilename, 'w', encoding='utf-8') as f:
        json.dump(all_spells, f, ensure_ascii=True, indent=4)
