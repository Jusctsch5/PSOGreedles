class CommonUtil:
    @staticmethod
    def binary_array_to_int(arr):
        result = 0
        for val in arr:
            result = (result << 8) | val
        return result

    @staticmethod
    def binary_array_to_hex(arr):
        return "".join(f"{x:02X}" for x in arr)

    @staticmethod
    def string_to_char_codes(string):
        char_codes = ""
        for char in string:
            code = ord(char)
            front = (code & 0xFF00) >> 8
            back = code & 0x00FF
            char_codes += f"{back:02x}{front:02x}"
        return char_codes.upper()

    @staticmethod
    def int_to_hex(value):
        return f"0x{value:06X}"


class Config:
    ITEM_CODES = None
    ELEMENT_CODES = None
    SRANK_ELEMENT_CODES = None
    FRAME_ADDITIONS = None
    BARRIER_ADDITIONS = None
    DISK_NAME_CODES = None
    DISK_NAME_LANGUAGE = None
    PBS = None
    MAG_COLOR_CODES = None

    WEAPON_RANGE = (0x000000, 0x00ED00)
    FRAME_RANGE = (0x010100, 0x010158)
    BARRIER_RANGE = (0x010200, 0x0102B4)
    UNIT_RANGE = (0x010300, 0x010364)
    MAG_RANGE = (0x020000, 0x025200)
    TOOL_RANGE = (0x030000, 0x030900)
    MESETA_RANGE = (0x040000, 0x040000)
    DISK_RANGE = (0x050000, 0x05121D)
    EPHINEA_RANGE = (0x031005, 0x031810)
    DISK_CODE = 0x0302


class ItemType:
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


class AdditionType:
    DEF = 0
    AVOID = 1


CLASSES = {
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

MODE = {0: "NORMAL", 1: "CLASSIC"}

MODE_NAME = {0: "NORMAL", 1: "CLASSIC"}

TITLES = {
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

SECTION_IDS = {
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

COMMON_WEAPONS_CODES = [
    0x000000,
    0x000100,
    0x000101,
    0x000102,
    0x000103,
    0x000104,
    0x000200,
    0x000201,
    0x000202,
    0x000203,
    0x000204,
    0x000300,
    0x000301,
    0x000302,
    0x000303,
    0x000304,
    0x000400,
    0x000401,
    0x000402,
    0x000403,
    0x000404,
    0x000500,
    0x000501,
    0x000502,
    0x000503,
    0x000504,
    0x000600,
    0x000601,
    0x000602,
    0x000603,
    0x000604,
    0x000700,
    0x000701,
    0x000702,
    0x000703,
    0x000704,
    0x000800,
    0x000801,
    0x000802,
    0x000803,
    0x000804,
    0x000900,
    0x000901,
    0x000902,
    0x000903,
    0x000904,
    0x000A00,
    0x000A01,
    0x000A02,
    0x000A03,
    0x000B00,
    0x000B01,
    0x000B02,
    0x000B03,
    0x000C00,
    0x000C01,
    0x000C02,
    0x000C03,
]

ATTRIBUTE_TYPE = {
    "native": 0x01,
    "aBeast": 0x02,
    "machine": 0x03,
    "dark": 0x04,
    "hit": 0x05,
}

MAG_COLOR_CODES = {
    0x00: "Red",
    0x01: "Blue",
    0x02: "Yellow",
    0x03: "Green",
    0x04: "Purple",
    0x05: "Black",
    0x06: "White",
    0x07: "Cyan",
    0x08: "Brown",
    0x09: "Orange",
    0x0A: "Slate Blue",
    0x0B: "Olive",
    0x0C: "Turqoise",
    0x0D: "Fuschia",
    0x0E: "Grey",
    0x0F: "Cream",
    0x10: "Pink",
    0x11: "Dark Green",
    0x12: "Chartreuse",
    0x13: "Azure",
    0x14: "Royal Purple",
    0x15: "Ruby",
    0x16: "Sapphire",
    0x17: "Emerald",
    0x18: "Gold",
    0x19: "Silver",
    0x1A: "Bronze",
    0x1B: "Plum",
    0x1C: "Violet",
    0x1D: "Goldenrod",
}

SRANK_WEAPON_CODES = {
    0x007000: "SABER",
    0x007100: "SWORD",
    0x007200: "BLADE",
    0x007300: "PARTISAN",
    0x007400: "SLICER",
    0x007500: "GUN",
    0x007600: "RIFLE",
    0x007700: "MECHGUN",
    0x007800: "SHOT",
    0x007900: "CANE",
    0x007A00: "ROD",
    0x007B00: "WAND",
    0x007C00: "TWIN",
    0x007D00: "CLAW",
    0x007E00: "BAZOOKA",
    0x007F00: "NEEDLE",
    0x008000: "SCYTHE",
    0x008100: "HAMMER",
    0x008200: "MOON",
    0x008300: "PSYCHOGUN",
    0x008400: "PUNCH",
    0x008500: "WINDMILL",
    0x008600: "HARISEN",
    0x008700: "J-BLADE",
    0x008800: "J-CUTTER",
    0x00A500: "SOWRDS",
    0x00A600: "LAUNCHER",
    0x00A700: "CARDS",
    0x00A800: "KNUCKLE",
    0x00A900: "AXE",
}
