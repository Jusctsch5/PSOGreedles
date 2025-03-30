from greedles.model.common_util import binary_array_to_hex
from greedles.model.character import Character
from greedles.model.config.config import Config
from greedles.parser.bank_parser import BankParser
from greedles.parser.inventory_parser import InventoryParser


class CharacterParser:
    """
    Parse character data
    Characters have an inventory and a bank
    """

    def __init__(self, config: Config):
        self.config = config

    def _parse_name(self, array: bytes) -> str:
        name = ""
        for i in range(0, len(array), 2):
            # End if both bytes are 0
            if array[i] + array[i + 1] == 0:
                break
            name += chr((array[i + 1] << 8) | array[i])

        print(f"name: {binary_array_to_hex(array)}")
        print(f"name: {name}")

        return name

    def parse(self, character_data: bytes, slot: int) -> Character:
        mode_array = character_data[7:9]
        mode = self._parse_mode(mode_array)

        name_array = character_data[968:988]
        name = self._parse_name(name_array)

        guild_card_number_array = character_data[888:896]
        guild_card_number = self._parse_guild_card_number(guild_card_number_array)

        character_class_array = character_data[937:938]
        character_class = self._parse_character_class(character_class_array)

        section_id_array = character_data[936:937]
        section_id = self._parse_section_id(section_id_array)

        level_array = character_data[876:877]
        level = self._parse_level(level_array)

        experience_array = character_data[877:884]
        experience = self._parse_experience(experience_array)

        ep1_progress_array = character_data[11460:11461]
        ep1_progress = self._parse_ep1_progress(ep1_progress_array)

        ep2_progress_array = character_data[11496:11497]
        ep2_progress = self._parse_ep2_progress(ep2_progress_array)

        inventory_parser = InventoryParser(self.config)
        inventory = inventory_parser.parse(character_data[8:4808], slot, Config.Lang.EN)

        bank_parser = BankParser(self.config)
        bank = bank_parser.parse(character_data[1800:6600], slot, Config.Lang.EN)

        return Character(
            slot,
            name,
            mode,
            guild_card_number,
            character_class,
            section_id,
            level,
            experience,
            ep1_progress,
            ep2_progress,
            inventory,
            bank,
        )

    def _parse_mode(self, array: bytes) -> str:
        return self.config.Mode.CLASSIC if array[0] == 0x40 else self.config.Mode.NORMAL

    def _parse_guild_card_number(self, array: bytes) -> str:
        guild_card_number = ""
        for i in range(0, len(array), 2):
            # End if both bytes are 0
            if array[i] + array[i + 1] == 0:
                break
            guild_card_number += chr((array[i + 1] << 8) | array[i])

        return guild_card_number

    def _parse_character_class(self, array: bytes) -> str:
        return self.config.CLASSES[array[0]]

    def _parse_section_id(self, array: bytes) -> str:
        return self.config.SECTION_IDS[array[0]]

    def _parse_level(self, array: bytes) -> int:
        return array[0] + 1

    def _parse_experience(self, array: bytes) -> int:
        return array[0] * 10000 + array[1] * 100 + array[2]

    def _parse_ep1_progress(self, array: bytes) -> str:
        return self._progress_count(array, 11460, self.config.EPISODE_1_MAX_STAGE)

    def _parse_ep2_progress(self, array: bytes) -> str:
        return self._progress_count(array, 11496, self.config.EPISODE_2_MAX_STAGE)

    def _progress_count(self, array: bytes, index: int, max_count: int) -> str:
        count = 0
        for i in range(max_count):
            if sum(array[index : index + 4]) == 0:
                break
            count += 1
            index += 4
        return (
            f"Stage {count} Cleared! | {self.config.TITLES[count]}"
            if count > 0
            else "No Progress"
        )
