import pytest
from pathlib import Path

from model.price_guide.price_guide import PriceGuideFixed, BasePriceStrategy

PRICE_DATA_DIR = Path("resources/data/price_guide")

@pytest.fixture
def fixed_price_guide():
    return PriceGuideFixed(PRICE_DATA_DIR)

def test_weapon_pricing_basic(fixed_price_guide: PriceGuideFixed):
    """Test weapons with simple base prices"""
    # Test fixed base price
    assert fixed_price_guide.get_price_weapon("DB's Saber 3064", {}, 0, "") == 10 * 500000
    # Test range base price
    assert 9*500000 <= fixed_price_guide.get_price_weapon("EXCALIBUR", {}, 0, "") <= 12*500000
    # Test item with only hit values
    assert fixed_price_guide.get_price_weapon("HANDGUN:GULD", {}, 0, "") == 0  # No base price

def test_weapon_hit_adjustments(fixed_price_guide: PriceGuideFixed):
    """Test weapons with hit value modifications"""
    # Test valid hit value
    item_data = {'attribute': {'hit': 30}}  # Simulate item data with 30% hit
    price = fixed_price_guide.get_price_weapon("EXCALIBUR", item_data, 0, "")
    assert 400*500000 <= price <= 650*500000
    
    # Test hit value not in data falls back to base
    item_data = {'attribute': {'hit': 10}}  # Hit value not in JSON
    price = fixed_price_guide.get_price_weapon("EXCALIBUR", item_data, 0, "")
    assert 9*500000 <= price <= 12*500000

def test_pricing_strategies(fixed_price_guide: PriceGuideFixed):
    """Test different base price strategies"""
    # Test MINIMUM strategy
    fixed_price_guide.bps = BasePriceStrategy.MINIMUM
    assert fixed_price_guide.get_price_weapon("EXCALIBUR", {}, 0, "") == 9 * 500000
    
    # Test MAXIMUM strategy
    fixed_price_guide.bps = BasePriceStrategy.MAXIMUM
    assert fixed_price_guide.get_price_weapon("EXCALIBUR", {}, 0, "") == 12 * 500000
    
    # Test AVERAGE strategy
    fixed_price_guide.bps = BasePriceStrategy.AVERAGE
    assert fixed_price_guide.get_price_weapon("EXCALIBUR", {}, 0, "") == 10.5 * 500000

def test_special_weapons(fixed_price_guide: PriceGuideFixed):
    """Test weapons with unique pricing structures"""
    # Test weapon with both base and hit values
    item_data = {'attribute': {'hit': 35}}
    price = fixed_price_guide.get_price_weapon("VJAYA", item_data, 0, "")
    assert price == 1 * 500000  # Base is 0 + hit value 1
    
    # Test weapon with only hit values
    item_data = {'attribute': {'hit': 45}}
    price = fixed_price_guide.get_price_weapon("HEAVEN STRIKER", item_data, 0, "")
    assert 2500*500000 <= price <= 3000*500000

def test_edge_cases(fixed_price_guide: PriceGuideFixed):
    """Test boundary conditions and special cases"""
    # Test weapon with invalid price format
    price = fixed_price_guide.get_price_weapon("M&A60 VISE", {}, 0, "")
    assert price == 0  # No base price and hit 0 is 0
    
    # Test weapon with N/A values
    item_data = {'attribute': {'hit': 15}}
    price = fixed_price_guide.get_price_weapon("Snow Queen", item_data, 0, "")
    assert price == 0  # N/A should be treated as 0

def test_grinder_and_element_adjustments(fixed_price_guide: PriceGuideFixed):
    """Test weapons with grinder and element modifications (if implemented)"""
    # This would need implementation details to test properly
    item_data = {'grinder': 10, 'element': 'Fire'}
    price = fixed_price_guide.get_price_weapon("EXCALIBUR", item_data, 10, "Fire")
    assert price
    # Add appropriate assertions based on your implementation


def test_price_guide_units(fixed_price_guide: PriceGuideFixed):
    """Test units with simple base prices"""
    assert fixed_price_guide.get_price_unit("Adept") == 38
    assert fixed_price_guide.get_price_unit("Centurion/Ability") == 7

