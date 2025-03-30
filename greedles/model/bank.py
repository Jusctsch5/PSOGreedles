from greedles.model.inventory import Inventory


class Bank:
    def __init__(self, inventory: Inventory, slot: str, mode: int):
        # Initialize class variables
        self.inventory: Inventory = inventory
        self.slot: str = slot
        self.mode: int = mode
