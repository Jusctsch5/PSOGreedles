from dataclasses import dataclass
from enum import Enum


@dataclass
class ColorInfo:
    hex_code: str
    name: str

class MagColor(Enum):
    RED = ColorInfo("#FF3319", "Red")
    BLUE = ColorInfo("#3333FF", "Blue")
    YELLOW = ColorInfo("#FFE619", "Yellow")
    GREEN = ColorInfo("#19FF19", "Green")
    PURPLE = ColorInfo("#CC19FF", "Purple")
    BLACK = ColorInfo("#191933", "Black")
    WHITE = ColorInfo("#E6FFFF", "White")
    CYAN = ColorInfo("#19E6FF", "Cyan")
    BROWN = ColorInfo("#804C33", "Brown")
    ORANGE = ColorInfo("#FF6600", "Orange")
    SLATE_BLUE = ColorInfo("#808BF9", "Slate Blue")
    OLIVE = ColorInfo("#808000", "Olive")
    TURQUOISE = ColorInfo("#00F0B6", "Turquoise")
    FUSCHIA = ColorInfo("#CC1964", "Fuschia")
    GRAY = ColorInfo("#7F7F7F", "Gray")
    CREAM = ColorInfo("#FEFED5", "Cream")
    PINK = ColorInfo("#FE7FC8", "Pink")
    DARK_GREEN = ColorInfo("#007F52", "Dark Green")
    CHARTREUSE = ColorInfo("#7FFF00", "Chartreuse")
    AZURE = ColorInfo("#007FFF", "Azure")
    ROYAL_PURPLE = ColorInfo("#660066", "Royal Purple")
    RUBY = ColorInfo("#F90505", "Ruby")
    SAPPHIRE = ColorInfo("#0A0AF2", "Sapphire")
    EMERALD = ColorInfo("#007F00", "Emerald")
    GOLD = ColorInfo("#9F7E3A", "Gold")
    SILVER = ColorInfo("#8D9BA6", "Silver")
    BRONZE = ColorInfo("#A0654E", "Bronze")
    PLUM = ColorInfo("#7F337F", "Plum")
    VIOLET = ColorInfo("#2B0757", "Violet")
    GOLDENROD = ColorInfo("#F2A400", "Goldenrod")

    @property
    def hex_code(self) -> str:
        return self.value.hex_code
        
    @property
    def color_name(self) -> str:
        return self.value.name

    @classmethod
    def from_code(cls, code: int):
        """Get color by its hex code value"""
        try:
            return list(cls)[code]
        except IndexError:
            raise ValueError(f"No color found for code: {code}")