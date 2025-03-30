import json
from typing import List, Dict, Any
from greedles.model.character import Character
from greedles.model.bank import Bank
from greedles.model.config.config import Config
from greedles.parser.bank_parser import BankParser
from greedles.parser.character_parser import CharacterParser
from greedles.parser.item_parser import ItemParser


class Parsers:
    """
    Parsers for different types of data
    """

    bank_parser: BankParser
    character_parser: CharacterParser
    item_parser: ItemParser

    @classmethod
    def configure(cls, config: Config):
        cls.bank_parser = BankParser(config)
        cls.character_parser = CharacterParser(config)
        cls.item_parser = ItemParser(config)


class InputHandler:
    def __init__(self, config: Config):
        self.config = config
        Parsers.configure(config)

        self.characters = []
        self.share_banks = []
        self.all_items = []
        self.normals = {}
        self.classics = {}
        self.current_data = {}

    def handle_files(self, files: List[bytes]) -> None:
        try:
            file_data = []

            # Create file-like objects from bytes for sorting
            class BytesFile:
                def __init__(self, name: str, content: bytes):
                    self.name = name
                    self.content = content

                def read(self):
                    return self.content

            byte_files = [
                BytesFile(f"psochar{i}.dat", file) for i, file in enumerate(files)
            ]
            sorted_files = self.sort_input_files(byte_files)

            for file in sorted_files:
                # Only process character data files
                if not any(
                    x in file.name.lower()
                    for x in ["psobank", "psoclassicbank", "psochar"]
                ):
                    continue

                file_data.append(
                    {
                        "filename": file.name,
                        "binary": file.read(),
                    }
                )

            if not file_data:
                return

            # Decode and display
            self.decode_and_display(file_data)

        except Exception as e:
            print(f"Error processing files: {str(e)}")
            raise

    def decode_and_display(self, file_data: List[Dict[str, Any]]) -> None:
        self.decoder(file_data)
        # self.display_pager()  # Implement display logic as needed

        # Display details
        if self.characters:
            # Prioritize character data display
            self.display_character(self.characters[0])
            self.current_data = {
                "page": "character",
                "searching": ["character", 0, self.characters[0]],
            }
            # self.pushed_page_color(f"pagecharacter0")  # Implement UI feedback as needed
        elif self.share_banks:
            if len(self.share_banks) > 1:
                share_bank = self.share_banks[1]
                index = 1
            else:
                share_bank = self.share_banks[0]
                index = 0

            self.display_share_bank(share_bank)
            self.current_data = {
                "page": "shareBank",
                "searching": ["shareBank", 0, share_bank],
            }
            # self.pushed_page_color(f"pageshareBank{index}")  # Implement UI feedback as needed

    def decoder(self, file_data: List[Dict[str, Any]]) -> None:
        if not file_data:
            return

        characters = []
        share_banks = []
        all_items = [
            {
                "Slot": "AllItems",
                "Mode": Config.Mode.NORMAL,
                "Inventory": {"JA": [], "EN": []},
            },
            {
                "Slot": "AllItems(Classic)",
                "Mode": Config.Mode.CLASSIC,
                "Inventory": {"JA": [], "EN": []},
            },
        ]

        for file_info in file_data:
            binary = file_info["binary"]
            filename = file_info["filename"]

            # Decode share bank file
            if "psobank" in filename.lower() and "classic" not in filename.lower():
                bank_parser = BankParser(self.config)
                share_bank = bank_parser.parse(binary, Config.Mode.NORMAL)
                share_banks.append(share_bank)
                all_items[share_bank.mode]["Inventory"]["EN"].extend(
                    share_bank.bank["EN"]
                )
                all_items[share_bank.mode]["Inventory"]["JA"].extend(
                    share_bank.bank["JA"]
                )
                continue

            # Decode classic bank file
            if "psoclassicbank" in filename.lower():
                bank_parser = BankParser(self.config)
                classic_bank = bank_parser.parse(binary, Config.Mode.CLASSIC)
                share_banks.append(classic_bank)
                all_items[classic_bank.mode]["Inventory"]["EN"].extend(
                    classic_bank.bank["EN"]
                )
                all_items[classic_bank.mode]["Inventory"]["JA"].extend(
                    classic_bank.bank["JA"]
                )
                continue

            # Decode character file
            if "psochar" in filename.lower():
                import re

                slot = int(re.search(r"(\d+)\.", filename).group(1))
                character_parser = CharacterParser(self.config)
                character = character_parser.parse(binary, slot + 1)
                characters.append(character)

                # Add character items to all_items
                all_items[character.mode]["Inventory"]["EN"].extend(
                    character.inventory["EN"]
                )
                all_items[character.mode]["Inventory"]["EN"].extend(
                    character.bank["EN"]
                )
                all_items[character.mode]["Inventory"]["JA"].extend(
                    character.inventory["JA"]
                )
                all_items[character.mode]["Inventory"]["JA"].extend(
                    character.bank["JA"]
                )

        # Sort items and add indices
        for items in all_items:
            for lang in ["EN", "JA"]:
                items["Inventory"][lang] = self.sort_inventory(items["Inventory"][lang])
                for idx, item in enumerate(items["Inventory"][lang]):
                    item.append(idx)

        # Set global variables
        self.set_global_variables(characters, share_banks, all_items)

    @staticmethod
    def sort_input_files(files: List[Any]) -> List[Any]:
        def sort_key(file):
            filename = file.name.lower()
            if "psoclassicbank" in filename:
                return (2, 0)  # Sort classic bank files last
            if "psobank" in filename:
                return (1, 0)  # Sort regular bank files second-to-last

            # Extract slot number for character files
            import re

            match = re.search(r"\s*(\d+)\.", filename)
            slot_num = int(match.group(1)) if match else 0
            return (0, slot_num)  # Sort character files by slot number

        return sorted(files, key=sort_key)

    def set_global_variables(self, characters, share_banks, all_items):
        if characters:
            self.characters = characters
            print("===== characters =====")
            print(characters)
            self.set_mode_data("characters", characters)

        if share_banks:
            self.share_banks = share_banks
            print("===== shareBanks =====")
            print(share_banks)
            self.set_mode_data("shareBanks", share_banks)

        if all_items:
            self.all_items = all_items
            print("===== allItems =====")
            print(all_items)
            self.set_mode_data("allItems", all_items)

    def set_mode_data(self, type_name: str, models: List[Any]) -> None:
        normals = []
        classics = []

        for model in models:
            if model is not None and model.mode == Config.Mode.NORMAL:
                normals.append(model)
            else:
                classics.append(model)

        self.normals[type_name] = [normals]
        self.classics[type_name] = [classics]
