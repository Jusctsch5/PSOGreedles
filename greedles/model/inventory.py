from typing import Dict, List


class Inventory:
    def __init__(self, inventory: Dict[str, List], slot: int, meseta: int):
        self.inventory: Dict[str, List] = inventory
        self.slot: int = slot
        self.meseta: int = meseta
