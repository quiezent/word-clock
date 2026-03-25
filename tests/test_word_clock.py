import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from word_clock import WordClock


def get_representation(hour, minute):
    wc = WordClock.__new__(WordClock)
    return wc.get_time_representation(hour, minute)


def test_three_oclock():
    assert get_representation(3, 0) == ["IT", "IS", "OCLOCK", "THREE"]


def test_fourteen_twentyfive():
    assert get_representation(14, 25) == ["TWENTY", "FIVE", "PAST", "TWO"]


def test_twenty_three_fifty_nine():
    assert get_representation(23, 59) == ["FIVE", "TO", "TWELVE"]


def test_24_hour_conversion():
    # 15:00 should be represented as three o'clock
    assert get_representation(15, 0) == ["IT", "IS", "OCLOCK", "THREE"]


def test_seventeen_fiftyfive():
    # 5:55 PM should highlight FIVE TO SIX
    assert get_representation(17, 55) == ["FIVE", "TO", "SIX"]


def test_four_fiftyfive():
    # 4:55 should highlight FIVE TO FIVE with both FIVEs at different positions
    assert get_representation(4, 55) == ["FIVE", "TO", "FIVE"]


def test_parse_specified_time_accepts_24_hour_boundaries():
    assert WordClock.parse_specified_time("00:00") == (0, 0)
    assert WordClock.parse_specified_time("23:59") == (23, 59)


def test_parse_specified_time_rejects_invalid_values():
    with pytest.raises(ValueError):
        WordClock.parse_specified_time("24:00")
    with pytest.raises(ValueError):
        WordClock.parse_specified_time("13:99")
    with pytest.raises(ValueError):
        WordClock.parse_specified_time("bad-input")
