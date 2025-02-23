from typing import Dict, Any
from .abstract import Abstract
from ..config import Config

class ShareBank(Abstract):
    def __init__(self, character_data: bytes, slot: int):
        super().__init__(character_data, slot)
        
        # Initialize class variables
        self.slot: str = ""
        self.mode: int = 0
        self.bank: Dict[str, Any] = {}
        
        # Set character slot number
        self.set_slot(slot)
        # Set character mode
        self.set_mode(slot)
        # Set character inventory (English)
        self.set_inventory(character_data[8:4808], self.bank, 24, self.slot, "EN")
        # Set character inventory (Japanese)
        self.set_inventory(character_data[8:4808], self.bank, 24, self.slot, "JA")
        # Add character meseta to inventory (English)
        self.set_meseta(character_data[4:7], self.bank, self.slot, "EN")
        # Add bank meseta to bank (Japanese)
        self.set_meseta(character_data[4:7], self.bank, self.slot, "JA")

    def set_slot(self, slot: int) -> None:
        """Set the slot name based on mode"""
        self.slot = "ShareBank(Classic)" if slot != Config.Mode.NORMAL else "ShareBank"

    def set_mode(self, slot: int) -> None:
        """Set the mode value"""
        self.mode = slot 