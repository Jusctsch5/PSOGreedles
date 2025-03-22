from typing import Dict, Any, List
from ..config import Config
from ..common_util import CommonUtil
from model.item import Item


class Abstract:
    def __init__(self, character_data: bytes, slot: int):
        Config.init()
        print("====== characterData ======")
        print(character_data)

    def set_inventory(
        self,
        items_data: bytes,
        inventory: Dict[str, List],
        length: int,
        slot: str,
        lang: str,
    ) -> None:
        """Set inventory items from binary data"""
        print("====== itemsData ======")
        print(items_data)

        array = []
        # Loop through all item areas by item unit
        for i in range(0, len(items_data), length):
            print("============ item data start ============")
            print(
                f"item number:{i // length}, index:{i}, length:{length}, end:{i + length}"
            )
            print(f"slot: {slot}")

            item_data = items_data[i : i + length]
            print("itemData:")
            # Check if slot is empty
            if self.is_blank(item_data):
                continue
            print(item_data)

            # Get item code
            item_code = CommonUtil.binary_array_to_int(item_data[:3])
            item_code_hex = CommonUtil.binary_array_to_hex(item_data[:3])
            print(f"item code: {item_code_hex}")

            item = Item(item_data, item_code, lang).item
            print(f"item name: {item['display']}")

            # Add item info to inventory list
            array.append([item_code_hex, item, slot])

        inventory[lang] = array

    def set_slot(self, slot: int) -> None:
        """Set the slot number"""
        self.slot = slot

    def set_meseta(
        self, meseta_data: bytes, inventory: Dict[str, List], slot: str, lang: str
    ) -> None:
        """Set meseta (currency) amount"""
        name = "MESETA" if lang == "EN" else "メセタ"
        meseta = (meseta_data[2] << 8 | meseta_data[1]) << 8 | meseta_data[0]
        item = {
            "type": 10,
            "name": name,
            "value": meseta,
            "display": f"{meseta} {name}",
        }
        inventory[lang].append(
            [
                "09"
                + str(meseta).zfill(7),  # Add prefix to make meseta maximum item code
                item,
                slot,
            ]
        )

    def is_blank(self, item_data: bytes) -> bool:
        """Check if item slot is empty"""
        return (
            sum(item_data[:20]) == 0
            or CommonUtil.binary_array_to_hex(item_data)
            == "000000000000000000000000FFFFFFFF0000000000000000"
            or CommonUtil.binary_array_to_hex(item_data).find(
                "00FF00000000000000000000FFFFFFFF"
            )
            != -1
        )
