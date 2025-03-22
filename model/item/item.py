from typing import List, Dict, Union

from model import common_util
from model.common_util import Config

class Item:
    pass


def weapon(self, item_code: int, item_data: List[int]) -> Dict:
    name = self.get_item_name(item_code)
    grinder = item_data[3]
    native = self.get_native(item_data)
    a_beast = self.get_a_beast(item_data)
    machine = self.get_machine(item_data)
    dark = self.get_dark(item_data)
    hit = self.get_hit(item_data)
    is_common = self.is_common_weapon(item_code)
    
    # Set element for common weapons if it exists
    element = ""
    if item_data[4] != 0x00 and item_data[4] != 0x80:
        element = f" [{self.get_element(item_data)}]"

    tekked_mode = self.is_tekked(item_data, item_code)
    tekked_text = ""
    # Add unidentified marker if not tekked
    if not tekked_mode:
        tekked_text = "? "
    if not tekked_mode and is_common:
        tekked_text = "???? "
        
    weapon_attributes = {
        "N": native,
        "AB": a_beast,
        "M": machine,
        "D": dark,
    }

    price = self.get_price_weapon(name, weapon_attributes, hit, grinder, element)

    return {
        "name": name,
        "type": 1,
        "itemdata": common_util.binary_array_to_hex(item_data),
        "element": element,
        "grinder": grinder,
        "attribute": {
            "native": native,
            "a_beast": a_beast,
            "machine": machine,
            "dark": dark,
            "hit": hit
        },
        "tekked": tekked_mode,
        "rare": not is_common,
        "display": f"{tekked_text}{name}{self.grinder_label(grinder)}{element} [{native}/{a_beast}/{machine}/{dark}|{hit}]",
        "price": price,
    }


def frame(self, item_code: int, item_data: List[int]) -> Dict:
    name = self.get_item_name(item_code)
    slot = item_data[5]
    defense = item_data[6]  # Using def_ since 'def' is a Python keyword
    defense_max_addition = self.get_addition(name, Config.FRAME_ADDITIONS, Config.AdditionType.DEF)
    avoid = item_data[8]
    avoid_max_addition = self.get_addition(name, Config.FRAME_ADDITIONS, Config.AdditionType.AVOID)
    price = self.get_price_frame(name, item_data, slot)

    return {
        "name": name,
        "type": 2,
        "itemdata": common_util.binary_array_to_hex(item_data),
        "slot": slot,
        "status": {
            "def": defense,
            "avoid": avoid,
        },
        "addition": {
            "def": defense_max_addition,
            "avoid": avoid_max_addition,
        },
        "display": f"{name} [{defense}/{defense_max_addition}|{avoid}/{avoid_max_addition}] [{slot}S]",
        "price": price,
    }

def barrier(self, item_code: int, item_data: List[int]) -> Dict:
    name = self.get_item_name(item_code)
    defense = item_data[6]
    defense_max_addition = self.get_addition(name, Config.BARRIER_ADDITIONS, Config.AdditionType.DEF)
    avoid = item_data[8]
    avoid_max_addition = self.get_addition(name, Config.BARRIER_ADDITIONS, Config.AdditionType.AVOID)
    addition = {defense: defense_max_addition, avoid: avoid_max_addition}
    price = self.get_price_barrier(name, item_data, addition) 

    return {
        "name": name,
        "type": 3,
        "itemdata": common_util.binary_array_to_hex(item_data),
        "addition": {
            "def": defense,
            "avoid": avoid,
        },
        "max_addition": {
            "def": defense_max_addition,
            "avoid": avoid_max_addition,
        },
        "display": f"{name} [{defense}/{defense_max_addition}|{avoid}/{avoid_max_addition}]",
        "price": price
    }


def unit(self, item_code: int, item_data: List[int]) -> Dict:
    name = self.get_item_name(item_code)
    price = self.get_price_unit(name, item_data)

    return {
        "name": name,
        "type": 4,
        "display": name,
        "itemdata": common_util.binary_array_to_hex(item_data),
        "price": price
    }

def disk(self, item_code: int, item_data: List[int]) -> Dict:
    name = Config.DISK_NAME_CODES[item_data[4]]
    level = item_data[2] + 1
    price = self.get_price_disk(name, item_data, level)

    display_text = f"{name} LV{level} {Config.DISK_NAME_LANGUAGE}"
    
    return {
        "name": display_text,
        "type": 6,
        "itemdata": common_util.binary_array_to_hex(item_data),
        "level": level,
        "display": display_text,
        "price": price
    }

def s_rank_weapon(self, item_code: int, item_data: List[int]) -> Dict:
    custom_name = self.get_custom_name(item_data[6:12])
    name = f"S-RANK {custom_name} {Config.S_RANK_WEAPON_CODES[item_code & 0xFFFF00]}"
    grinder = item_data[3]
    element = self.get_srank_element(item_data)
    price = self.get_price_s_rank_weapon(name, item_data, grinder, element)

    return {
        "name": name,
        "type": 8,
        "itemdata": common_util.binary_array_to_hex(item_data),
        "grinder": grinder,
        "element": element,
        "display": f"{name} {self.grinder_label(grinder)} [{element}]",
        "price": price,
    }

def tool(self, item_code: int, item_data: List[int]) -> Dict:
    name = self.get_item_name(item_code)
    
    # Set number based on data length (28 for inventory, otherwise storage)
    number = item_data[5] if len(item_data) == 28 else item_data[20]
    
    price = self.get_price_tool(name, item_data, number)

    return {
        "name": name,
        "type": 7,
        "itemdata": common_util.binary_array_to_hex(item_data),
        "number": number,
        "display": f"{name}{self.number_label(number)}",
        "price": price,
    }


def other(self, item_code: int, item_data: List[int]) -> Dict:
    name = self.get_item_name(item_code)
    
    # Set number based on data length (28 for inventory, otherwise storage)
    number = item_data[5] if len(item_data) == 28 else item_data[20]
    
    price = self.get_price_other(name, item_data, number)
    
    return {
        "name": name,
        "type": 9,
        "itemdata": common_util.binary_array_to_hex(item_data),
        "number": number,
        "display": f"{name}{self.number_label(number)}",
        "price": price
    }


def get_item_name(self, item_code: int) -> str:
    if item_code in Config.ITEM_CODES:
        return Config.ITEM_CODES[item_code]
    return f"undefined. ({common_util.int_to_hex(item_code)})"

def get_element(self, item_data: List[int]) -> str:
    code = item_data[4]
    if code in Config.ELEMENT_CODES:
        return Config.ELEMENT_CODES[code]
    return "undefined"

def get_srank_element(self, item_data: List[int]) -> str:
    element_code = item_data[2]
    if element_code in Config.SRANK_ELEMENT_CODES:
        return Config.SRANK_ELEMENT_CODES[element_code]
    return "undefined"

def get_native(self, item_data: List[int]) -> int:
    return self.get_attribute(Config.AttributeType.NATIVE, item_data)

def get_a_beast(self, item_data: List[int]) -> int:
    return self.get_attribute(Config.AttributeType.A_BEAST, item_data)

def get_machine(self, item_data: List[int]) -> int:
    return self.get_attribute(Config.AttributeType.MACHINE, item_data)

def get_dark(self, item_data: List[int]) -> int:
    return self.get_attribute(Config.AttributeType.DARK, item_data)

def get_hit(self, item_data: List[int]) -> int:
    return self.get_attribute(Config.AttributeType.HIT, item_data)

def get_attribute(self, attribute_type: int, item_data: List[int]) -> int:
    attributes = [
        item_data[6:8],    # First attribute value
        item_data[8:10],   # Second attribute value
        item_data[10:12],  # Third attribute value
    ]
    
    for attribute in attributes:
        if attribute[0] == attribute_type:
            # Just return the second byte directly instead of using Int8Array
            return attribute[1]
            
    return 0

def get_addition(self, name: str, additions: Dict, type_: int) -> Union[int, str]:
    if name in additions:
        return additions[name][type_]
    return "undefined"

def is_tekked(self, item_data: List[int], item_code: int) -> bool:
    # Returns True if common weapon has element set
    return item_data[4] < 0x80

def get_pbs(self, pbs_code: int) -> List[str]:
    if pbs_code in Config.PBS:
        return Config.PBS[pbs_code]
    return ["undefined", "undefined", "undefined"]


def number_label(self, number):
    if number == 1:
        return ""
    if number > 0:
        return f" x{number}"
    return ""

def grinder_label(self, number):
    if number > 0:
        return f" +{number}"
    return ""

def get_custom_name(self, custom_name_data):
    # Create temp array for name storage
    temp = []

    # Second character (effectively first) is lowercase data, convert to uppercase
    custom_name_data[0] -= 0x04
    
    # Get 3 letters * 3 times, but first character is empty so effectively 8 characters
    temp.extend(self.three_letters(custom_name_data[0:2]))
    temp.extend(self.three_letters(custom_name_data[2:4]))
    temp.extend(self.three_letters(custom_name_data[4:6]))

    # Convert each number to corresponding letter
    # 1 -> A, 26 -> Z, 0 is skipped
    custom_name = ""
    for value in temp:
        if value != 0:
            custom_name += chr(value + 64)

    return custom_name

def three_letters(self, array):
    # Remove initial data not related to calculation
    array[0] = array[0] - 0x80
    first = array[0] // 0x04
    second = ((array[0] % 0x04) << 8 | array[1]) // 0x20
    third = array[1] % 0x20
    
    return [
        first,
        second,
        third
    ] 

