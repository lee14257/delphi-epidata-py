from delphi_epidata.model import EpiRange
from delphi_epidata._utils import format_item, format_list


def test_format_item() -> None:
    assert format_item("a") == "a"
    assert format_item(1) == "1"
    assert format_item({"from": 1, "to": 3}) == "1-3"
    assert format_item(EpiRange(3, 5)) == "3-5"


def test_format_list() -> None:
    assert format_list("a") == "a"
    assert format_list(1) == "1"
    assert format_list({"from": 1, "to": 3}) == "1-3"
    assert format_list(EpiRange(3, 5)) == "3-5"

    assert format_list(["a", "b"]) == "a,b"
    assert format_list(("a", "b")) == "a,b"
    assert format_list({"a", "b"}) == "b,a"
    assert format_list(["a", 1]) == "a,1"
