"""Module for all methods related to numbers."""
import re
from typing import Union


def parse_numbers_from_string(input_string: str) -> list[Union[float, int]]:
    """Parses numbers from a given string, handling integers, floats, and numbers with commas as decimal points.

    This function removes non-numeric characters (except for commas, dots, and hyphens), replaces commas
    between digits with periods (to handle decimal numbers in some locales), and extracts both integers
    and floating-point numbers from the string.

    Args:
        input_string (str): The input string containing potential numbers to be parsed.

    Returns:
        List[Union[int, float]]: A list of parsed numbers (either integers or floats).

    Example:
        input_string = "The price is 10.5, and -3.2 was deducted, also 2,000 is a large number."
        parse_numbers_from_string(input_string)
        # Returns: [10.5, -3.2, 2000]
    """
    if not isinstance(input_string, str):
        raise ValueError("Given value is not string")

    # Remove all non-numeric characters (except for comma and dot)
    cleaned_string = re.sub(r"[^\d\.,\-]", " ", input_string)

    cleaned_string = re.sub(r"(?<=\d),(?=\d)", ".", cleaned_string)
    number_pattern = r"-?\d*\.\d+|-?\d+"

    # Find all matches of the pattern in the cleaned string
    numbers = re.findall(number_pattern, cleaned_string)

    parsed_numbers = []
    for num in numbers:
        if "." in num:
            parsed_numbers.append(float(num))
        else:
            parsed_numbers.append(int(num))

    return parsed_numbers
