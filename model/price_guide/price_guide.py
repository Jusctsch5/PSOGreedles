from abc import ABC, abstractmethod
from bisect import bisect
from typing import Dict, Any, Optional
from pathlib import Path
import asyncio
import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class BasePriceStrategy(ABC):
    MINIMUM = 0
    AVERAGE = 1
    MAXIMUM = 2


MESESTA_PER_PD = 500000
HIGH_ATTRIBUTE_THRESHOLD = 50

class PriceGuideException(Exception):
    pass

class PriceGuideExceptionItemNameNotFound(PriceGuideException):
    pass

class PriceGuideExceptionAbilityNameNotFound(PriceGuideException):
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

    @staticmethod
    def get_price_from_range(price_range: str, bps: BasePriceStrategy) -> float:
        # Parse out the price range value from the price range dictionary
        price_range_value:str = ""
        if "-" in price_range:
            price_range_value = price_range
        elif price_range.isdigit():
            return float(price_range)
        else:
            raise PriceGuideParseException(f"Price range {price_range} does not contain a base price in form of 'base' or 'base-price'")
        
        # Parse the price range value from the str to float based on the BasePriceStrategy
        min_price, max_price = map(float, price_range_value.split('-'))
        average_price = (min_price + max_price) / 2

        # Perform the price calculation based on the BasePriceStrategy
        if bps == BasePriceStrategy.MINIMUM:
            return min_price
        elif bps == BasePriceStrategy.MAXIMUM:
            return max_price
        else:  # AVERAGE    
            return average_price

    @staticmethod
    def get_price_for_item_range(price_range: str, number: int, bps: BasePriceStrategy) -> float:
        return PriceGuideAbstract.get_price_from_range(price_range, bps) * number

    @abstractmethod
    async def build_prices(self) -> None:
        """Build the price database from the source"""
        pass

    def get_price_srank_weapon(self, name: str, ability: str, grinder: int, element: str, item_data: Optional[Dict] = None) -> float:
        """Get price for S-rank weapon"""

        actual_key = next(
            (key for key in self.srank_weapon_prices["weapons"].keys() if key.lower() == name.lower()),
            None
        )
        
        if actual_key is None:
            raise PriceGuideExceptionItemNameNotFound(f"Item name {name} not found in srank_weapon_prices")

        base_price = self.srank_weapon_prices["weapons"][actual_key]["base"]


        ability_price = 0
        if ability:
            actual_ability = next(
                (key for key in self.srank_weapon_prices["modifiers"].keys() if key.lower() == ability.lower()),
                None
            )

            if actual_ability is None:
                raise PriceGuideExceptionAbilityNameNotFound(f"Ability {ability} not found in srank_weapon_prices")

            ability_price = self.srank_weapon_prices["modifiers"][actual_ability]["base"]


        total_price = float(base_price) + float(ability_price)

        return total_price

    def get_price_weapon(self, name: str, weapon_attributes: Dict, hit: int, grinder: int, element: str, item_data: Optional[Dict] = None) -> float:
        """Get price for normal weapon"""
        
        actual_key = next(
            (key for key in self.weapon_prices.keys() if key.lower() == name.lower()),
            None
        )
        
        if actual_key is None:
            raise PriceGuideExceptionItemNameNotFound(f"Item name {name} not found in weapon_prices")
            
        base_price = self.get_price_from_range(self.weapon_prices[actual_key]["base"], self.bps)

        if weapon_attributes:
            for attribute, value in weapon_attributes.items():
                if value > HIGH_ATTRIBUTE_THRESHOLD:
                    ability_price = self.weapon_prices[actual_key]["modifiers"][attribute]
                    base_price += ability_price

        hit_values = self.weapon_prices[actual_key].get("hit_values", {})
        
        if hit_values and hit > 0:
            # Convert string keys to integers and sort
            sorted_thresholds = sorted(map(int, hit_values.keys()))
            
            # Find the largest threshold <= actual hit value
            index = bisect(sorted_thresholds, hit) - 1
            
            if index >= 0:
                threshold = sorted_thresholds[index]
                price_range = hit_values[str(threshold)]
                hit_price = self.get_price_from_range(price_range, self.bps)
                base_price += hit_price

        return base_price


    def get_price_frame(self, name: str, addition: str, slot: int, item_data: Optional[Dict] = None) -> float:
        """Get price for frame"""
        return 0

    def get_price_barrier(self, name: str, addition: str, item_data: Optional[Dict] = None) -> float:
        """Get price for barrier"""
        return 0

    def get_price_unit(self, name: str, item_data: Optional[Dict] = None) -> float:
        """Get price for unit"""
        price_range = self.unit_prices[name]["base_price"]
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
        logger.info(f"Building price database from {self.directory}")
        self.srank_weapon_prices = self._load_json_file("srankweapons.json")
        self.weapon_prices = self._load_json_file("weapons.json")
        self.frame_prices = self._load_json_file("frames.json")
        self.barrier_prices = self._load_json_file("barriers.json")
        self.unit_prices = self._load_json_file("units.json")
        self.mag_prices = self._load_json_file("mags.json")
        self.disk_prices = self._load_json_file("disks.json")
        self.tool_prices = self._load_json_file("tools.json")
        logger.info(f"Price database built from {self.directory}"   )

    def _load_json_file(self, filename: str) -> Dict[str, Any]:
        """Load and parse a JSON file from the directory"""
        file_path = self.directory / filename
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Error loading {filename} from {file_path}: {e}")
            raise PriceGuideException(f"Error loading {filename} from {file_path}: {e}")

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

