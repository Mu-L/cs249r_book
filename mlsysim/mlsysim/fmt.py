"""
fmt.py
Formatting + presentation helpers for QMD output.
Keep science in core/formulas.py; keep display here.
"""

from .core.constants import ureg


class MarkdownStr(str):
    """A string that ALSO renders as raw Markdown when consumed by Quarto/Jupyter.

    Quarto's inline ``{python} x`` substitution escapes commas and decimals in
    plain ``str`` outputs (``2,039.4`` → ``2\\,039\\.4``). Outside math mode the
    escapes are harmless (``\\.`` reads as a literal period), but **inside**
    ``$...$`` math mode they become LaTeX commands — ``\\,`` is ``\\thinspace``
    and ``\\.`` is a dot accent — and the value is silently corrupted to
    ``2 0394``.

    Quarto detects ``_repr_markdown_`` and inserts the content **verbatim**
    without escaping. By subclassing ``str``, every string operation
    (``f"{x}"``, ``x + y``, ``x.replace(...)``, ``len(x)``, slicing) continues
    to work, so this drop-in replacement for plain-``str`` formatters is fully
    backward-compatible with existing call sites.
    """

    def _repr_markdown_(self):
        return str.__str__(self)


def _get_markdown():
    """Return the MarkdownStr class. Retained for backward compatibility."""
    return MarkdownStr


def fmt(quantity, unit=None, precision=1, commas=True, allow_zero=False,
        prefix="", suffix=""):
    """
    Format a Pint Quantity (or plain number) for narrative text.
    Returns a MarkdownStr so Quarto inserts the value verbatim (no escape).

    The prefix and suffix arguments collapse the old MarkdownStr(f"...")
    escape-hatch idiom into a single canonical helper. Common uses:

        fmt(price, precision=0, prefix="$")         # "$1,000"
        fmt(rate * 100, precision=1, commas=False, suffix="%")  # "12.4%"
        fmt(bw_mb_s, precision=1, commas=False, suffix=" MB/s")  # "2.4 MB/s"
        fmt(speedup, precision=0, commas=False, suffix="x")     # "8x"

    Safety: Raises ValueError if a non-zero value is formatted as "0"
    due to insufficient precision (unless allow_zero=True).
    """
    if unit:
        # If a raw number is passed, assume it is already in base units.
        if isinstance(quantity, ureg.Quantity):
            quantity = quantity.to(unit)

    if isinstance(quantity, ureg.Quantity):
        val = quantity.magnitude
    else:
        val = quantity

    # Primary formatting
    fmt_str = f",.{precision}f" if commas else f".{precision}f"
    result = f"{val:{fmt_str}}"

    # --- Precision Safety Check ---
    # Check if we accidentally rounded a non-zero value to zero
    try:
        numeric_result = float(result.replace(",", ""))
    except ValueError:
        numeric_result = None # Case for non-numeric strings if any

    if numeric_result == 0.0 and abs(val) > 1e-12 and not allow_zero:
        raise ValueError(
            f"Formatting Precision Error: Value {val} was formatted as '{result}' "
            f"with precision={precision}. This hides the actual value. "
            f"Increase precision or set allow_zero=True if this was intentional."
        )

    decorated = f"{prefix}{result}{suffix}"
    out = MarkdownStr(decorated)
    assert isinstance(out, MarkdownStr), (
        "fmt() must return MarkdownStr — this guard exists so a future refactor "
        "of this module cannot silently break Quarto's _repr_markdown_ detection. "
        "See .claude/rules/math.md."
    )
    return out


def fmt_val(quantity, default="-"):
    """
    Format the magnitude of a Pint Quantity (or a plain scalar) using Python's
    ``:g`` general format — compact, no trailing zeros, variable precision.

    Returns a MarkdownStr. Pairs with ``fmt_unit()`` for side-by-side
    value/unit table columns where ``fmt()``'s fixed-precision output is
    too rigid (e.g., a column that mixes ``2``, ``2.5``, ``80``, ``9.5e10``).

    >>> fmt_val(2.0)        # "2"
    >>> fmt_val(2.5)        # "2.5"
    >>> fmt_val(quantity)   # "80" for 80 GB; "9.5e+10" for 95 GFLOPS as TFLOPS
    """
    if isinstance(quantity, ureg.Quantity):
        val = quantity.magnitude
    else:
        val = quantity
    if val is None:
        return MarkdownStr(default)
    out = MarkdownStr(f"{val:g}")
    assert isinstance(out, MarkdownStr), "fmt_val() must return MarkdownStr"
    return out


def fmt_unit(quantity, default="-"):
    """
    Extract the unit string of a Pint Quantity. Returns a MarkdownStr.
    For non-Pint values, returns ``default`` wrapped in MarkdownStr.

    Pairs with ``fmt_val()`` for value/unit table columns.

    >>> fmt_unit(80 * GB)        # "gigabyte"
    >>> fmt_unit(80)             # "-"
    """
    if isinstance(quantity, ureg.Quantity):
        out = MarkdownStr(f"{quantity.units}")
    else:
        out = MarkdownStr(default)
    assert isinstance(out, MarkdownStr), "fmt_unit() must return MarkdownStr"
    return out


def fmt_percent(ratio, precision=1, commas=False):
    """
    Format a ratio (0.0 to 1.0) as a percentage string for display.
    Use this for compound fractions (e.g. effective utilization) to avoid
    display bugs from Quantity or wrong scaling.
    Accepts Pint Quantity (uses magnitude) or plain float.
    """
    if isinstance(ratio, ureg.Quantity):
        # Crucial: convert to dimensionless first so units like flop/TFLOP cancel out!
        ratio = float(ratio.m_as(''))
    else:
        ratio = float(ratio)
    return fmt(ratio * 100, precision=precision, commas=commas)


def fmt_sci(val, precision=2):
    """
    Formats a number or Pint Quantity into scientific notation using Unicode.
    Example: 4.1e9 -> "4.10 × 10⁹"
    """
    # Unicode superscript digits
    superscripts = {
        "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
        "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹", "-": "⁻",
    }

    if isinstance(val, ureg.Quantity):
        val = val.magnitude
    s = f"{val:.{precision}e}"
    base, exp = s.split("e")
    exp_int = int(exp)
    exp_str = "".join(superscripts.get(c, c) for c in str(exp_int))
    return MarkdownStr(f"{float(base):.{precision}f} × 10{exp_str}")


def sci_latex(val, precision=2):
    """
    Formats a number or Pint Quantity into LaTeX scientific notation.
    Example: 4.1e9 -> "4.10 \\times 10^{9}"
    """
    if isinstance(val, ureg.Quantity):
        val = val.magnitude
    s = f"{val:.{precision}e}"
    base, exp = s.split('e')
    exp_int = int(exp)
    return f"{float(base):.{precision}f} \\times 10^{{{exp_int}}}"


def fmt_frac(numerator, denominator, result=None, unit=None):
    """
    Create a LaTeX fraction with optional result and unit.
    Returns: $\\frac{num}{denom}$ or $\\frac{num}{denom} = result$ unit
    """
    latex = f'$\\frac{{{numerator}}}{{{denominator}}}$'
    if result is not None:
        latex += f' = {result}'
    if unit is not None:
        latex += f' {unit}'
    out = MarkdownStr(latex)
    assert isinstance(out, MarkdownStr), "fmt_frac() must return MarkdownStr"
    return out


def check(condition, message):
    """
    Invariant guard for narrative logic.
    Ensures that the calculated values support the textbook's claims.
    """
    if not condition:
        raise ValueError(f"Narrative broken: {message}")


def fmt_math(expression):
    """
    Wrap a LaTeX math expression in `$...$` so Quarto renders it as inline math.
    Returns a MarkdownStr.
    """
    out = MarkdownStr(f"${expression}$")
    assert isinstance(out, MarkdownStr), "fmt_math() must return MarkdownStr"
    return out


