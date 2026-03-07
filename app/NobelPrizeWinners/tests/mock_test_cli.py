import pytest
import argparse
from nobel_prize_cli import validate_year, validate_category

def test_validate_year_valid():
    assert validate_year("1901") == 1901
    assert validate_year("2023") == 2023

def test_validate_year_invalid():
    with pytest.raises(argparse.ArgumentTypeError):
        validate_year("1900")
    with pytest.raises(argparse.ArgumentTypeError):
        validate_year("2027")  # Future year
    with pytest.raises(argparse.ArgumentTypeError):
        validate_year("abc")

def test_validate_category_valid():
    assert validate_category("Physics") == "Physics"
    assert validate_category("physics") == "Physics"
    assert validate_category("CHEMISTRY") == "Chemistry"
    assert validate_category("Medicine") == "Medicine"
    assert validate_category("Literature") == "Literature"
    assert validate_category("Peace") == "Peace"
    assert validate_category("Economics") == "Economics"

def test_validate_category_invalid():
    with pytest.raises(argparse.ArgumentTypeError):
        validate_category("Math")
    with pytest.raises(argparse.ArgumentTypeError):
        validate_category("Invalid")
