from greedles.model.config.config import Config
from greedles.model.config.item_codes_en import ItemCodesEN


def test_config():
    config = Config()
    assert config is not None


def test_item_codes():
    item_codes = ItemCodesEN()
    assert item_codes is not None
