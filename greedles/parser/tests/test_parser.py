"""
Test the parser module

This module tests the parser module by loading PSO character and bank data files and testing the parser's functionality.

The parser is tested for the following:
- File loading and sorting
- Character data decoding
- Share bank decoding
- All items collection
"""

from typing import List
import pytest
from pathlib import Path
import zipfile
import io

from greedles.model.config.item_codes_en import ItemCodesEN
from greedles.parser.parser import InputHandler
from greedles.model.character import Character
from greedles.model.bank import Bank
from greedles.model.config.config import Config

TEST_DATA_PATH = Path("data/Ephinea_42085595.zip")


@pytest.fixture
def test_data_files():
    """Load test data files from zip"""
    with zipfile.ZipFile(TEST_DATA_PATH, "r") as zip_ref:
        # Convert zip contents to list of bytes objects
        files = []
        for filename in zip_ref.namelist():
            with zip_ref.open(filename) as f:
                files.append(f.read())
    return files


@pytest.fixture
def input_handler():
    item_codes = ItemCodesEN()
    config = Config(item_codes)
    return InputHandler(config)


def test_file_handling(input_handler: InputHandler, test_data_files: List[bytes]):
    """Test basic file loading and handling"""
    input_handler.handle_files(test_data_files)

    # Verify we have processed data
    assert len(input_handler.characters) > 0
    assert len(input_handler.share_banks) > 0
    assert len(input_handler.all_items) > 0


def test_file_sorting(input_handler: InputHandler, test_data_files: List[bytes]):
    """Test file sorting logic"""

    # Create mock BytesFile objects
    class BytesFile:
        def __init__(self, name: str, content: bytes):
            self.name = name
            self.content = content

    test_files = [
        BytesFile("psochar0.dat", b"test"),
        BytesFile("psoclassicbank.dat", b"test"),
        BytesFile("psobank.dat", b"test"),
    ]

    sorted_files = input_handler.sort_input_files(test_files)

    # Verify sorting order: character files first, then bank, then classic bank
    assert "psochar" in sorted_files[0].name
    assert "psobank" in sorted_files[1].name
    assert "psoclassicbank" in sorted_files[2].name


def test_character_decoding(input_handler: InputHandler, test_data_files: List[bytes]):
    """Test character data decoding"""
    input_handler.handle_files(test_data_files)

    # Test first character
    char = input_handler.characters[0]
    assert isinstance(char, Character)
    assert char.slot > 0
    assert "EN" in char.inventory
    assert "JA" in char.inventory
    assert "EN" in char.bank
    assert "JA" in char.bank


def test_share_bank_decoding(input_handler: InputHandler, test_data_files: List[bytes]):
    """Test share bank decoding"""
    input_handler.handle_files(test_data_files)

    # Test share banks
    for bank in input_handler.share_banks:
        assert isinstance(bank, Bank)
        assert bank.mode in [Config.Mode.NORMAL, Config.Mode.CLASSIC]
        assert "EN" in bank.bank
        assert "JA" in bank.bank


def test_all_items_collection(
    input_handler: InputHandler, test_data_files: List[bytes]
):
    """Test all items collection and sorting"""
    input_handler.handle_files(test_data_files)

    # Test all_items structure
    assert len(input_handler.all_items) == 2  # Normal and Classic modes

    for items in input_handler.all_items:
        assert "Slot" in items
        assert "Mode" in items
        assert "Inventory" in items
        assert "EN" in items["Inventory"]
        assert "JA" in items["Inventory"]

        # Test that items are sorted and indexed
        for lang in ["EN", "JA"]:
            for idx, item in enumerate(items["Inventory"][lang]):
                assert item[-1] == idx  # Check index is correct


def test_mode_data_separation(
    input_handler: InputHandler, test_data_files: List[bytes]
):
    """Test separation of normal and classic mode data"""
    input_handler.handle_files(test_data_files)

    assert "characters" in input_handler.normals
    assert "characters" in input_handler.classics
    assert "shareBanks" in input_handler.normals
    assert "shareBanks" in input_handler.classics
    assert "allItems" in input_handler.normals
    assert "allItems" in input_handler.classics
