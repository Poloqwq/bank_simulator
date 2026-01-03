from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.models.utils import number_to_currency_string


def test_number_to_currency_string():
    assert number_to_currency_string(0) == "0"
    assert number_to_currency_string(1000) == "1,000"
    assert number_to_currency_string(1234567) == "1,234,567"
