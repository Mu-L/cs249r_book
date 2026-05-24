"""Tests for mlsysim.fmt formatting guards."""

import pytest

from mlsysim.fmt import MarkdownStr, fmt, fmt_int, fmt_percent


class TestFmtPrecisionGuards:
    def test_precision_zero_accepts_whole_numbers(self):
        assert fmt(989, precision=0, commas=False) == "989"
        assert fmt(10.0, precision=0, commas=False) == "10"
        assert fmt(175.0, precision=0, commas=False) == "175"

    def test_precision_zero_rejects_small_fractions_that_display_as_zero(self):
        with pytest.raises(ValueError, match="formatted as '0'"):
            fmt(0.1, precision=0, commas=False)
        with pytest.raises(ValueError, match="formatted as '0'"):
            fmt(0.4, precision=0, commas=False)

    def test_precision_zero_rejects_non_integer_values(self):
        with pytest.raises(ValueError, match="not integer-like"):
            fmt(10.7, precision=0, commas=False)
        with pytest.raises(ValueError, match="not integer-like"):
            fmt(84.7, precision=0, commas=False)
        with pytest.raises(ValueError, match="not integer-like"):
            fmt(4.1, precision=0, commas=False)

    def test_precision_zero_accepts_explicit_round(self):
        assert fmt(round(10.7), precision=0, commas=False) == "11"
        assert fmt(round(362507.545), precision=0, commas=True) == "362,508"

    def test_precision_one_preserves_fractions(self):
        assert fmt(10.7, precision=1, commas=False) == "10.7"
        assert fmt(8.5, precision=1, commas=False) == "8.5"

    def test_precision_one_rejects_spurious_trailing_zeros_on_integers(self):
        with pytest.raises(ValueError, match="spurious trailing zeros"):
            fmt(512.0, precision=1, commas=False)
        with pytest.raises(ValueError, match="spurious trailing zeros"):
            fmt(989, precision=1, commas=False)

    def test_returns_markdown_str(self):
        out = fmt(42, precision=0, commas=False)
        assert isinstance(out, MarkdownStr)
        assert out._repr_markdown_() == "42"


class TestFmtInt:
    def test_rounds_computed_values_explicitly(self):
        assert fmt_int(120.28, commas=False) == "120"
        assert fmt_int(10.7, commas=False) == "11"
        assert fmt_int(362507.545, commas=True) == "362,508"

    def test_accepts_prefix_and_suffix(self):
        assert fmt_int(175, commas=False, suffix=" billion") == "175 billion"


class TestFmtPercentGuards:
    def test_precision_zero_accepts_whole_percentages(self):
        assert fmt_percent(0.45, precision=0, commas=False) == "45"

    def test_precision_zero_rejects_fractional_percentages(self):
        with pytest.raises(ValueError, match="not integer-like"):
            fmt_percent(0.456, precision=0, commas=False)
