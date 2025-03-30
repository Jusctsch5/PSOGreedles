from greedles.model.config.config import Config
from greedles.model.bank import Bank
from greedles.parser.inventory_parser import InventoryParser


class BankParser:
    def __init__(self, config: Config):
        self.config = config

    def parse(self, bank_data: bytes, slot: int) -> Bank:
        inventory_parser = InventoryParser(self.config)
        inventory = inventory_parser.parse(bank_data)
        slot = self._parse_slot(slot)
        mode = self._parse_mode(slot)

        return Bank(inventory, slot, mode)

    def _parse_slot(self, slot: int) -> None:
        """Set the slot name based on mode"""
        self.slot = "ShareBank(Classic)" if slot != Config.Mode.NORMAL else "ShareBank"

    def _parse_mode(self, slot: int) -> None:
        """Set the mode value"""
        self.mode = slot
