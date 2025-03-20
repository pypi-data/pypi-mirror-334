import math
from decimal import Decimal, ROUND_FLOOR

def floor_to_precision(num, decimals):
    """Floors a number to a specific number of decimal places accurately."""
    num = Decimal(str(num))  # Convert to Decimal from string to avoid precision loss
    factor = Decimal(10) ** decimals
    return (num * factor).to_integral_value(rounding=ROUND_FLOOR) / factor

def get_decimal_magnitude(num):
    """Extracts fractional part and calculates its magnitude."""
    abs_num = abs(num)
    fractional_part = abs_num - math.floor(abs_num)  # Extract part after decimal

    if fractional_part == 0:
        return 0  # No decimals needed

    magnitude = math.floor(math.log10(fractional_part))  # Calculate magnitude
    return abs(magnitude)

def format_with_separator(num, decimals, ignore_first):
    """Formats the number with a thousand separator and keeps necessary decimals."""
    if ignore_first and num > 10_000:
        return f"{num:,.{decimals}f}"
    return f"{num:.{decimals}f}"

def adaptive_floor(num, extra_decimals=2, ignore_first=True):
    """
    Floors a number dynamically based on its fractional part magnitude.

    Parameters:
    num (float): The number to be floored.
    extra_decimals (int, optional): Additional decimal places to consider when flooring. Default is 2.
    ignore_first (bool, optional): Whether to ignore the first separator in the formatted output. Default is True.

    Returns:
    str: The floored number formatted with separators.
    """
    if float(num).is_integer():
        return format_with_separator(num, 0, ignore_first)

    decimals = get_decimal_magnitude(num) + extra_decimals
    floored_num = floor_to_precision(num, decimals)
    return format_with_separator(floored_num, decimals, ignore_first)
