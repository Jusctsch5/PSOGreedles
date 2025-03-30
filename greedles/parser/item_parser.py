from typing import Dict, List, Union
from pytest import Item
from greedles.model.config.config import Config
from greedles.model.common_util import binary_array_to_hex, int_to_hex
from greedles.price_guide.price_guide import PriceGuideAbstract


class ItemParser:
    def __init__(self, config: Config, price_guide: PriceGuideAbstract):
        self.config = config
        self.price_guide = price_guide

    def parse(self, item_data: bytes, item_code: int, lang: str) -> Item:
        item_type = self.get_item_type(item_code)
        return self._parse_item(item_data, item_code, item_type, lang)

    def get_item_type(self, item_code: int) -> int:
        if self.is_s_rank_weapon(item_code):
            return self.config.ItemType.SRANK_WEAPON
        elif self.is_weapon(item_code):
            return self.config.ItemType.WEAPON
        elif self.is_frame(item_code):
            return self.config.ItemType.FRAME
        elif self.is_barrier(item_code):
            return self.config.ItemType.BARRIER
        elif self.is_unit(item_code):
            return self.config.ItemType.UNIT
        elif self.is_mag(item_code):
            return self.config.ItemType.MAG
        elif self.is_disk(item_code):
            return self.config.ItemType.DISK
        elif self.is_tool(item_code):
            return self.config.ItemType.TOOL
        else:
            return self.config.ItemType.OTHER

    def is_s_rank_weapon(self, item_code: int) -> bool:
        return item_code & 0xFFF0 in self.config.SRANK_WEAPON_CODES

    def is_weapon(self, item_code: int) -> bool:
        return (
            self.config.WEAPON_RANGE[0] <= item_code
            and item_code <= self.config.WEAPON_RANGE[1]
        )

    def is_common_weapon(self, item_code: int) -> bool:
        return (
            self.config.WEAPON_RANGE[0] <= item_code
            and item_code <= self.config.WEAPON_RANGE[1]
        )

    def is_frame(self, item_code: int) -> bool:
        return (
            self.config.FRAME_RANGE[0] <= item_code
            and item_code <= self.config.FRAME_RANGE[1]
        )

    def is_barrier(self, item_code: int) -> bool:
        return (
            self.config.BARRIER_RANGE[0] <= item_code
            and item_code <= self.config.BARRIER_RANGE[1]
        )

    def is_unit(self, item_code: int) -> bool:
        return (
            self.config.UNIT_RANGE[0] <= item_code
            and item_code <= self.config.UNIT_RANGE[1]
        )

    def is_mag(self, item_code: int) -> bool:
        return (
            self.config.MAG_RANGE[0] <= item_code
            and item_code <= self.config.MAG_RANGE[1]
        )

    def is_disk(self, item_code: int) -> bool:
        return item_code >> 8 == self.config.DISK_CODE

    def is_tool(self, item_code: int) -> bool:
        return (
            self.config.TOOL_RANGE[0] <= item_code
            and item_code <= self.config.TOOL_RANGE[1]
        )

    def _parse_item(
        self, item_data: bytes, item_code: int, item_type: int, lang: str
    ) -> Item:
        if item_type == self.config.ItemType.SRANK_WEAPON:
            return self.s_rank_weapon(item_code, item_data)
        elif item_type == self.config.ItemType.WEAPON:
            return self.weapon(item_code, item_data)
        elif item_type == self.config.ItemType.FRAME:
            return self.frame(item_code, item_data)
        elif item_type == self.config.ItemType.BARRIER:
            return self.barrier(item_code, item_data)
        elif item_type == self.config.ItemType.UNIT:
            return self.unit(item_code, item_data)
        elif item_type == self.config.ItemType.MAG:
            return self.mag(item_code, item_data)
        elif item_type == self.config.ItemType.DISK:
            return self.disk(item_code, item_data)
        elif item_type == self.config.ItemType.TOOL:
            return self.tool(item_code, item_data)
        elif item_type == self.config.ItemType.OTHER:
            return self.other(item_code, item_data)
        else:
            return f"unknown. ({int_to_hex(item_code)}). There's a possibility that New Ephinea Item"

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

        price = self.price_guide.get_price_weapon(
            name, weapon_attributes, hit, grinder, element
        )

        return {
            "name": name,
            "type": 1,
            "itemdata": binary_array_to_hex(item_data),
            "element": element,
            "grinder": grinder,
            "attribute": {
                "native": native,
                "a_beast": a_beast,
                "machine": machine,
                "dark": dark,
                "hit": hit,
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
        defense_max_addition = self.get_addition(
            name, self.config.FRAME_ADDITIONS, self.config.AdditionType.DEF
        )
        avoid = item_data[8]
        avoid_max_addition = self.get_addition(
            name, self.config.FRAME_ADDITIONS, self.config.AdditionType.AVOID
        )

        addition = {defense: defense, avoid: avoid}
        max_addition = {defense: defense_max_addition, avoid: avoid_max_addition}
        price = self.price_guide.get_price_frame(name, addition, max_addition, slot)

        return {
            "name": name,
            "type": 2,
            "itemdata": binary_array_to_hex(item_data),
            "slot": slot,
            "status": {
                "def": defense,
                "avoid": avoid,
            },
            "addition": addition,
            "max_addition": max_addition,
            "display": f"{name} [{defense}/{defense_max_addition}|{avoid}/{avoid_max_addition}] [{slot}S]",
            "price": price,
        }

    def barrier(self, item_code: int, item_data: List[int]) -> Dict:
        name = self.get_item_name(item_code)
        defense = item_data[6]
        defense_max_addition = self.get_addition(
            name, self.config.BARRIER_ADDITIONS, self.config.AdditionType.DEF
        )
        avoid = item_data[8]
        avoid_max_addition = self.get_addition(
            name, self.config.BARRIER_ADDITIONS, self.config.AdditionType.AVOID
        )
        addition = {defense: defense_max_addition, avoid: avoid_max_addition}
        max_addition = {defense: defense_max_addition, avoid: avoid_max_addition}

        price = self.price_guide.get_price_barrier(name, addition, max_addition)

        return {
            "name": name,
            "type": 3,
            "itemdata": binary_array_to_hex(item_data),
            "addition": addition,
            "max_addition": max_addition,
            "display": f"{name} [{defense}/{defense_max_addition}|{avoid}/{avoid_max_addition}]",
            "price": price,
        }

    def unit(self, item_code: int, item_data: List[int]) -> Dict:
        name = self.get_item_name(item_code)
        price = self.price_guide.get_price_unit(name, item_data)

        return {
            "name": name,
            "type": 4,
            "display": name,
            "itemdata": binary_array_to_hex(item_data),
            "price": price,
        }

    def mag(self, item_code: int, item_data: List[int]) -> Dict:
        name = self.get_item_name(item_code & 0xFFFF00)
        level = item_data[2]
        sync = item_data[16]
        iq = item_data[17]
        color = self.config.MAG_COLOR_CODES[item_data[19]]
        defense = (item_data[5] << 8 | item_data[4]) / 100
        pow = (item_data[7] << 8 | item_data[6]) / 100
        dex = (item_data[9] << 8 | item_data[8]) / 100
        mind = (item_data[11] << 8 | item_data[10]) / 100
        # pbsの要素は0=center, 1=right、2=left
        pbs = self.get_pbs(binary_array_to_hex([item_data[3], item_data[18]]))
        price = self.price_guide.get_price_mag(name, item_data, level)

        return {
            "name": f"{name} LV{level} [{color[1]}]",
            "type": 5,
            "itemdata": binary_array_to_hex(item_data),
            "level": level,
            "sync": sync,
            "iq": iq,
            "color": color[1],
            "rgb": color[0],
            "status": {
                "def": defense,
                "pow": pow,
                "dex": dex,
                "mind": mind,
            },
            "pbs": [
                pbs[0],
                pbs[1],
                pbs[2],
            ],
            "display": f"{name} LV{level} [{color[1]}] [{defense}/{pow}/{dex}/{mind}] [{pbs[2]}|{pbs[0]}|{pbs[1]}]",
            "display_front": f"{name} LV{level} [{color[1]}]",
            "display_end": f"] [{defense}/{pow}/{dex}/{mind}] [{pbs[2]}|{pbs[0]}|{pbs[1]}]",
            "price": price,
        }

    def disk(self, item_code: int, item_data: List[int]) -> Dict:
        name = self.config.DISK_NAME_CODES[item_data[4]]
        level = item_data[2] + 1
        price = self.price_guide.get_price_disk(name, item_data, level)

        display_text = f"{name} LV{level} {self.config.DISK_NAME_LANGUAGE}"

        return {
            "name": display_text,
            "type": 6,
            "itemdata": binary_array_to_hex(item_data),
            "level": level,
            "display": display_text,
            "price": price,
        }

    def s_rank_weapon(self, item_code: int, item_data: List[int]) -> Dict:
        custom_name = self.get_custom_name(item_data[6:12])
        name = f"S-RANK {custom_name} {self.config.S_RANK_WEAPON_CODES[item_code & 0xFFFF00]}"
        grinder = item_data[3]
        element = self.get_srank_element(item_data)
        price = self.price_guide.get_price_s_rank_weapon(
            name, item_data, grinder, element
        )

        return {
            "name": name,
            "type": 8,
            "itemdata": binary_array_to_hex(item_data),
            "grinder": grinder,
            "element": element,
            "display": f"{name} {self.grinder_label(grinder)} [{element}]",
            "price": price,
        }

    def tool(self, item_code: int, item_data: List[int]) -> Dict:
        name = self.get_item_name(item_code)

        # Set number based on data length (28 for inventory, otherwise storage)
        number = item_data[5] if len(item_data) == 28 else item_data[20]

        price = self.price_guide.get_price_tool(name, item_data, number)

        return {
            "name": name,
            "type": 7,
            "itemdata": binary_array_to_hex(item_data),
            "number": number,
            "display": f"{name}{self.number_label(number)}",
            "price": price,
        }

    def other(self, item_code: int, item_data: List[int]) -> Dict:
        name = self.get_item_name(item_code)

        # Set number based on data length (28 for inventory, otherwise storage)
        number = item_data[5] if len(item_data) == 28 else item_data[20]

        price = self.price_guide.get_price_other(name, item_data, number)

        return {
            "name": name,
            "type": 9,
            "itemdata": binary_array_to_hex(item_data),
            "number": number,
            "display": f"{name}{self.number_label(number)}",
            "price": price,
        }

    def get_item_name(self, item_code: int) -> str:
        if item_code in self.config.ITEM_CODES:
            return self.config.ITEM_CODES[item_code]
        return f"undefined. ({int_to_hex(item_code)})"

    def get_element(self, item_data: List[int]) -> str:
        code = item_data[4]
        if code in self.config.ELEMENT_CODES:
            return self.config.ELEMENT_CODES[code]
        return "undefined"

    def get_srank_element(self, item_data: List[int]) -> str:
        element_code = item_data[2]
        if element_code in self.config.SRANK_ELEMENT_CODES:
            return self.config.SRANK_ELEMENT_CODES[element_code]
        return "undefined"

    def get_native(self, item_data: List[int]) -> int:
        return self.get_attribute(self.config.AttributeType.NATIVE, item_data)

    def get_a_beast(self, item_data: List[int]) -> int:
        return self.get_attribute(self.config.AttributeType.A_BEAST, item_data)

    def get_machine(self, item_data: List[int]) -> int:
        return self.get_attribute(self.config.AttributeType.MACHINE, item_data)

    def get_dark(self, item_data: List[int]) -> int:
        return self.get_attribute(self.config.AttributeType.DARK, item_data)

    def get_hit(self, item_data: List[int]) -> int:
        return self.get_attribute(self.config.AttributeType.HIT, item_data)

    def get_attribute(self, attribute_type: int, item_data: List[int]) -> int:
        attributes = [
            item_data[6:8],  # First attribute value
            item_data[8:10],  # Second attribute value
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
        if pbs_code in self.config.PBS:
            return self.config.PBS[pbs_code]
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

        return [first, second, third]
