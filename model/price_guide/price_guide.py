from abc import ABC, abstractmethod

from typing import Dict, Any, Optional
from pathlib import Path
# import aiohttp
import asyncio
import json


class BasePriceStrategy(ABC):
    MINIMUM = 0
    AVERAGE = 1
    MAXIMUM = 2


MESESTA_PER_PD = 500000

class PriceGuideException(Exception):
    pass


class PriceGuideParseException(PriceGuideException):
    pass

class PriceGuideAbstract(ABC):
    def __init__(self):
        self.bps = BasePriceStrategy.MINIMUM
        self.srank_weapon_prices: Dict[str, Any] = {}
        self.weapon_prices: Dict[str, Any] = {}
        self.frame_prices: Dict[str, Any] = {}
        self.barrier_prices: Dict[str, Any] = {}
        self.unit_prices: Dict[str, Any] = {}
        self.mag_prices: Dict[str, Any] = {}
        self.disk_prices: Dict[str, Any] = {}
        self.tool_prices: Dict[str, Any] = {}
        self.other_prices: Dict[str, Any] = {}

    @staticmethod
    def get_price_for_item_range(price_range: Dict[str, Any], number: int, bps: BasePriceStrategy) -> float:
        # Parse out the price range value from the price range dictionary
        price_range_value:str = ""
        if "base" in price_range:
            price_range_value = price_range['base']
        elif "base-price" in price_range:
            price_range_value = price_range['base-price']
        elif "base_price" in price_range:
            price_range_value = price_range['base_price']
        else:
            raise PriceGuideParseException(f"Price range {price_range} does not contain a base price in form of 'base' or 'base-price'")
        
        # Parse the price range value from the str to float based on the BasePriceStrategy
        if '-' not in price_range_value:
            average_price = min_price = max_price = float(price_range_value)
            
        else:
            min_price, max_price = map(float, price_range_value.split('-'))
            average_price = (min_price + max_price) / 2

        # Perform the price calculation based on the BasePriceStrategy
        if bps == BasePriceStrategy.MINIMUM:
            return min_price * number
        elif bps == BasePriceStrategy.MAXIMUM:
            return max_price * number
        else:  # AVERAGE    
            return average_price * number

    @abstractmethod
    async def build_prices(self) -> None:
        """Build the price database from the source"""
        pass

    def get_price_srank_weapon(self, name: str, grinder: int, element: str, item_data: Optional[Dict] = None) -> float:
        """Get price for S-rank weapon"""

        return 0

    def get_price_weapon(self, name: str, grinder: int, element: str, item_data: Optional[Dict] = None) -> float:
        """Get price for normal weapon"""
        return 0

    def get_price_frame(self, name: str, addition: str, slot: int, item_data: Optional[Dict] = None) -> float:
        """Get price for frame"""
        return 0

    def get_price_barrier(self, name: str, addition: str, item_data: Optional[Dict] = None) -> float:
        """Get price for barrier"""
        return 0

    def get_price_unit(self, name: str, item_data: Optional[Dict] = None) -> float:
        """Get price for unit"""
        price_range = self.unit_prices[name]
        return self.get_price_for_item_range(price_range, 1, self.bps)

    def get_price_mag(self, name: str, level: int, item_data: Optional[Dict] = None) -> float:
        """Get price for mag"""
        price_range = self.mag_prices[name]
        return self.get_price_for_item_range(price_range, 1, self.bps)

    def get_price_disk(self, name: str, level: int, item_data: Optional[Dict] = None) -> float:
        price_range = self.disk_prices[name][str(level)]
        return self.get_price_for_item_range(price_range, 1, self.bps)

    def get_price_tool(self, name: str, number: int, item_data: Optional[Dict] = None) -> float:
        """Get price for tool"""

        # Check if the tool exists in the price database
        if name not in self.tool_prices:
            return 0

        # Get the price range string
        price_range = self.tool_prices[name]
        return self.get_price_for_item_range(price_range, number, self.bps)

    def get_price_other(self, name: str, number: int, item_data: Optional[Dict] = None) -> float:
        """Get price for other items"""
        return 0

class PriceGuideFixed(PriceGuideAbstract):
    def __init__(self, directory: str):
        super().__init__()
        self.directory = Path(directory)
        asyncio.run(self.build_prices())

    async def build_prices(self) -> None:
        """Build price database from local JSON files"""
        self.srank_weapon_prices = self._load_json_file("srankweapons.json")
        self.weapon_prices = self._load_json_file("weapons.json")
        self.frame_prices = self._load_json_file("frames.json")
        self.barrier_prices = self._load_json_file("barriers.json")
        self.unit_prices = self._load_json_file("units.json")
        self.mag_prices = self._load_json_file("mags.json")
        self.disk_prices = self._load_json_file("disks.json")
        self.tool_prices = self._load_json_file("tools.json")

    def _load_json_file(self, filename: str) -> Dict[str, Any]:
        """Load and parse a JSON file from the directory"""
        try:
            with open(self.directory / filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading {filename}: {e}")
            return {}

class PriceGuideDynamic(PriceGuideAbstract):
    def __init__(self, api_url: str):
        super().__init__()
        self.api_url = api_url
        asyncio.run(self.build_prices())

    async def build_prices(self) -> None:
        """Build price database from web API"""
        pass
        """
        # This is a placeholder for the actual implementation
        async with aiohttp.ClientSession() as session:
            try:
                # Example of how it might work:
                # async with session.get(f"{self.api_url}/prices") as response:
                #     data = await response.json()
                #     self.srank_weapon_prices = data.get("srankweapons", {})
                #     self.weapon_prices = data.get("weapons", {})
                #     # etc...
                pass
            except aiohttp.ClientError as e:
                print(f"Error fetching prices: {e}")
        """

# Example usage:
if __name__ == "__main__":
    # Using fixed prices from JSON files
    fixed_guide = PriceGuideFixed("resources/data/price_guide/")
    
    # Using dynamic prices from web API
    dynamic_guide = PriceGuideDynamic("https://api.pioneer2.net/prices") 

