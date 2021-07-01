from delphi_epidata.model import EpiRange


def test_epirange() -> None:
    r = EpiRange(3, 4)
    assert r.start == 3 and r.end == 4
    assert str(r) == "3-4"


def test_epirange_wrong_order() -> None:
    r = EpiRange(4, 3)
    assert r.start == 3 and r.end == 4
