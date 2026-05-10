import pytest
from core.similarity import _is_color_compatible, _parse_price


class TestIsColorCompatible:
    def test_same_identity(self):
        assert _is_color_compatible(["G"], ["G"]) is True

    def test_candidate_subset_of_query(self):
        assert _is_color_compatible(["G"], ["G", "W"]) is True

    def test_colorless_candidate_always_compatible(self):
        assert _is_color_compatible([], ["G"]) is True

    def test_candidate_has_color_outside_query(self):
        assert _is_color_compatible(["B"], ["G"]) is False

    def test_candidate_partial_overlap_not_subset(self):
        assert _is_color_compatible(["G", "W"], ["G"]) is False

    def test_both_colorless(self):
        assert _is_color_compatible([], []) is True

    def test_multicolor_candidate_fits_multicolor_query(self):
        assert _is_color_compatible(["W", "U"], ["W", "U", "B"]) is True


class TestParsePrice:
    def test_valid_price(self):
        assert _parse_price({"usd": "1.50"}) == 1.50

    def test_zero_price(self):
        assert _parse_price({"usd": "0.00"}) == 0.00

    def test_missing_usd_key(self):
        assert _parse_price({"usd_foil": "2.00"}) == float("inf")

    def test_none_prices(self):
        assert _parse_price(None) == float("inf")

    def test_empty_dict(self):
        assert _parse_price({}) == float("inf")

    def test_usd_is_none(self):
        assert _parse_price({"usd": None}) == float("inf")
