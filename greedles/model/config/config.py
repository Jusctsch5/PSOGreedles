from enum import IntEnum, Enum
from greedles.model.config.item_codes import ItemCodes


class Config:
    def __init__(self, item_codes: ItemCodes):
        self.ITEM_CODES = item_codes.item_codes()
        self.ELEMENT_CODES = item_codes.element_codes()
        self.SRANK_ELEMENT_CODES = item_codes.srank_element_codes()
        self.FRAME_ADDITIONS = item_codes.frame_additions()
        self.BARRIER_ADDITIONS = item_codes.barrier_additions()
        self.DISK_NAME_CODES = item_codes.disk_name_codes()
        self.DISK_NAME_LANGUAGE = item_codes.disk_name_language()
        self.PBS = item_codes.pb_data_pattern()
        self.MAG_COLOR_CODES = item_codes.mag_color_codes()
        self.SRANK_WEAPON_CODES = item_codes.srank_weapon_codes()
        self.COMMON_WEAPON_CODES = item_codes.common_weapon_codes()

        # Ranges
        self.WEAPON_RANGE = (0x000000, 0x00ED00)
        self.FRAME_RANGE = (0x010100, 0x010158)
        self.BARRIER_RANGE = (0x010200, 0x0102B4)
        self.UNIT_RANGE = (0x010300, 0x010364)
        self.MAG_RANGE = (0x020000, 0x025200)
        self.TOOL_RANGE = (0x030000, 0x030900)
        self.MESETA_RANGE = (0x040000, 0x040000)
        self.DISK_RANGE = (0x050000, 0x05121D)
        self.EPHINEA_RANGE = (0x031005, 0x031810)
        self.DISK_CODE = 0x0302

        #
        self.EPISODE_1_MAX_STAGE = 9
        self.EPISODE_2_MAX_STAGE = 6

        self.CLASSES = {
            0x00: "HUmar",
            0x01: "Hunewearl",
            0x02: "HUcast",
            0x03: "RAmar",
            0x04: "RAcast",
            0x05: "RAcaseal",
            0x06: "FOmarl",
            0x07: "FOnewm",
            0x08: "FOnewearl",
            0x09: "HUcaseal",
            0x0A: "FOmar",
            0x0B: "RAmarl",
        }

        self.MODE_NAME = {0: "NORMAL", 1: "CLASSIC"}

        self.TITLES = {
            1: "Ra-GOU",
            2: "Gi-GOU",
            3: "Bu-GOU",
            4: "Ra-ZAN",
            5: "Gi-ZAN",
            6: "Bu-ZAN",
            7: "Ra-EI",
            8: "Gi-EI",
            9: "Bu-EI",
        }

        self.SECTION_IDS = {
            0x00: "VIRIDIA",
            0x01: "GREENILL",
            0x02: "SKYLY",
            0x03: "BLUEFULL",
            0x04: "PURPLENUM",
            0x05: "PINKAL",
            0x06: "REDRIA",
            0x07: "ORAN",
            0x08: "YELLOWBOZE",
            0x09: "WHITILL",
            0x0A: "VIRIDIA",
        }

    class ItemType(IntEnum):
        WEAPON = 1
        FRAME = 2
        BARRIER = 3
        UNIT = 4
        MAG = 5
        DISK = 6
        TOOL = 7
        SRANK_WEAPON = 8
        OTHER = 9
        MESETA = 10

    class AdditionType(IntEnum):
        DEF = 0
        AVOID = 1

    class Mode(IntEnum):
        NORMAL = 0
        CLASSIC = 1

    class AttributeType(IntEnum):
        NATIVE = 0x01
        A_BEAST = 0x02
        MACHINE = 0x03
        DARK = 0x04
        HIT = 0x05

    class Lang(Enum):
        EN = "EN"
        JA = "JA"
