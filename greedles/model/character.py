from typing import Dict, Any

from greedles.model.inventory import Inventory
from greedles.model.bank import Bank


class Character:
    def __init__(
        self,
        slot: int,
        name: str,
        mode: str,
        guild_card_number: str,
        character_class: str,
        section_id: str,
        level: int,
        experience: int,
        ep1_progress: str,
        ep2_progress: str,
        inventory: Inventory,
        bank: Bank,
    ):
        # Character slot number
        self.slot: int = slot
        # Character mode
        self.mode: str = mode
        # Character name
        self.name: str = name
        # Character guild card number
        self.guild_card_number: str = guild_card_number
        # Character class
        self.character_class: str = character_class
        # Character section ID
        self.section_id: str = section_id
        # Character level
        self.level: int = level
        # Character experience
        self.experience: int = experience
        # Character Ep1 challenge progress
        self.ep1_progress: str = ep1_progress
        # Character Ep2 challenge progress
        self.ep2_progress: str = ep2_progress
        # Character inventory
        self.inventory: Dict[str, Any] = inventory
        # Character bank
        self.bank: Dict[str, Any] = bank
