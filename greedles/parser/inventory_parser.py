from typing import Dict, List
import logging

from greedles.model.common_util import binary_array_to_int, binary_array_to_hex
from greedles.model.config.config import Config
from greedles.model.inventory import Inventory
from greedles.parser.item_parser import ItemParser

logger = logging.getLogger(__name__)


class InventoryParser:
    def __init__(self, config: Config):
        self.config = config

    def parse(
        self,
        inventory_data: bytes,
        slot: str,
        lang: Config.Lang,
    ) -> Inventory:
        """Parse inventory data"""
        inventory_list = self._parse_inventory(inventory_data, 28, slot, lang.value)

        meseta_data = inventory_data[884:887]
        meseta = self._parse_meseta(meseta_data, inventory_list, slot, lang.value)

        inventory = Inventory(inventory_list, slot, meseta)

        return inventory

    def _parse_inventory(
        self,
        items_data: bytes,
        length: int,
        slot: str,
        lang: str,
    ) -> List[List[str]]:
        """Set inventory items from binary data"""
        logger.debug("====== itemsData ======")
        logger.debug(items_data)

        array = []
        # Loop through all item areas by item unit
        for i in range(0, len(items_data), length):
            logger.debug("============ item data start ============")
            logger.debug(
                f"item number:{i // length}, index:{i}, length:{length}, end:{i + length}"
            )
            logger.debug(f"slot: {slot}")

            item_data = items_data[i : i + length]
            logger.debug("itemData:")
            # Check if slot is empty
            if self.is_blank(item_data):
                continue
            logger.debug(item_data)

            # Get item code
            item_code = binary_array_to_int(item_data[:3])
            item_code_hex = binary_array_to_hex(item_data[:3])
            logger.debug(f"item code: {item_code_hex}")

            item_parser = ItemParser(self.config)
            item = item_parser.parse(item_data, item_code, lang)
            logger.debug(f"item name: {item['display']}")

            # Add item info to inventory list
            array.append([item_code_hex, item, slot])

        return array

    def _parse_meseta(
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
            or binary_array_to_hex(item_data)
            == "000000000000000000000000FFFFFFFF0000000000000000"
            or binary_array_to_hex(item_data).find("00FF00000000000000000000FFFFFFFF")
            != -1
        )
