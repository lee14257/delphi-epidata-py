from delphi_epidata.model import EpiRange, _format_item, _format_list


def test_epirange() -> None:
    r = EpiRange(3, 4)
    assert r.start == 3 and r.end == 4
    assert str(r) == "3-4"


def test_epirange_wrong_order() -> None:
    r = EpiRange(4, 3)
    assert r.start == 3 and r.end == 4


def test_format_item() -> None:
    assert _format_item("a") == "a"
    assert _format_item(1) == "1"
    assert _format_item({"from": 1, "to": 3}) == "1-3"
    assert _format_item(EpiRange(3, 5)) == "3-5"


def test_format_list() -> None:
    assert _format_list("a") == "a"
    assert _format_list(1) == "1"
    assert _format_list({"from": 1, "to": 3}) == "1-3"
    assert _format_list(EpiRange(3, 5)) == "3-5"

    assert _format_list(["a", "b"]) == "a,b"
    assert _format_list(("a", "b")) == "a,b"
    assert _format_list({"a", "b"}) == "b,a"
    assert _format_list(["a", 1]) == "a,1"
