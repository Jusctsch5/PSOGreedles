from typing import Dict, Any
from .abstract import Abstract
from ..config import Config
from ..common_util import CommonUtil

class Character(Abstract):
    def __init__(self, character_data: bytes, slot: int):
        super().__init__(character_data, slot)
        
        # Character slot number
        self.slot: int = 0
        # Character mode
        self.mode: str = ""
        # Character name
        self.name: str = ""
        # Character guild card number
        self.guild_card_number: str = ""
        # Character class
        self.character_class: str = ""
        # Character section ID
        self.section_id: str = ""
        # Character level
        self.level: int = 0
        # Character experience
        self.experience: int = 0
        # Character Ep1 challenge progress
        self.ep1_progress: str = ""
        # Character Ep2 challenge progress
        self.ep2_progress: str = ""
        # Character inventory
        self.inventory: Dict[str, Any] = {}
        # Character bank
        self.bank: Dict[str, Any] = {}

        # Set all character attributes
        self.set_slot(slot)
        self.set_mode(character_data)
        self.set_name(character_data)
        self.set_guild_card_number(character_data)
        self.set_class(character_data)
        self.set_section_id(character_data)
        self.set_level(character_data)
        self.set_experience(character_data)
        self.set_ep1_progress(character_data, 11460, 9)
        self.set_ep2_progress(character_data, 11496, 6)
        
        # Set inventory and bank items
        self.set_inventory(character_data[20:860], self.inventory, 28, slot, "EN")
        self.set_inventory(character_data[1800:6600], self.bank, 24, f"{slot} Bank", "EN")
        self.set_inventory(character_data[20:860], self.inventory, 28, slot, "JA")
        self.set_inventory(character_data[1800:6600], self.bank, 24, f"{slot} Bank", "JA")
        
        # Set meseta values
        self.set_meseta(character_data[884:887], self.inventory, slot, "EN")
        self.set_meseta(character_data[1795:1799], self.bank, f"{slot} Bank", "EN")
        self.set_meseta(character_data[884:887], self.inventory, slot, "JA")
        self.set_meseta(character_data[1795:1799], self.bank, f"{slot} Bank", "JA")

    def set_mode(self, character_data: bytes) -> None:
        """Set character mode based on data"""
        self.mode = Config.Mode.CLASSIC if character_data[7] == 0x40 else Config.Mode.NORMAL

    def set_name(self, character_data: bytes) -> None:
        """Set character name from data"""
        array = character_data[968:988]
        name = ""
        for i in range(0, len(array), 2):
            # End if both bytes are 0
            if array[i] + array[i + 1] == 0:
                break
            name += chr((array[i + 1] << 8) | array[i])

        print(f"name: {CommonUtil.binary_array_to_hex(array)}")
        print(f"name: {name}")
        self.name = name

    def set_guild_card_number(self, character_data: bytes) -> None:
        """Set guild card number from data"""
        array = character_data[888:896]
        guild_card_number = ""
        for value in array:
            guild_card_number += str(value & 0x0F)

        print(f"guildCardNumber: {CommonUtil.binary_array_to_hex(array)}")
        print(f"guildCardNumber: {guild_card_number}")
        self.guild_card_number = guild_card_number

    def set_class(self, character_data: bytes) -> None:
        """Set character class from data"""
        class_id = character_data[937]
        self.character_class = Config.Classes.get(class_id, "undefined")
        print(f"class: {class_id}")

    def set_section_id(self, character_data: bytes) -> None:
        """Set section ID from data"""
        section_id = character_data[936]
        self.section_id = Config.SectionIDs.get(section_id, "undefined")
        print(f"sectionID: {section_id}")

    def set_level(self, character_data: bytes) -> None:
        """Set character level from data"""
        print(f"level: {character_data[876] + 1}")
        self.level = character_data[876] + 1

    def set_experience(self, character_data: bytes) -> None:
        """Set character experience from data"""
        pass  # Implementation needed

    def set_ep1_progress(self, character_data: bytes, index: int, number: int) -> None:
        """Set Episode 1 progress"""
        count = self.progress_count(character_data, index, number)
        self.ep1_progress = f"Stage {count} Cleared! | {Config.Titles[count]}" if count > 0 else "No Progress"

    def set_ep2_progress(self, character_data: bytes, index: int, number: int) -> None:
        """Set Episode 2 progress"""
        count = self.progress_count(character_data, index, number)
        self.ep2_progress = f"Stage {count} Cleared!" if count > 0 else "No Progress"

    def progress_count(self, character_data: bytes, index: int, max_count: int) -> int:
        """Count progress stages"""
        count = 0
        for i in range(max_count):
            # End if 4 bytes sum to 0 (no clear record for this stage)
            if sum(character_data[index:index + 4]) == 0:
                break
            count += 1
            index += 4
        return count 