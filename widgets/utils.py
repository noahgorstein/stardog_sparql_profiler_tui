import re

PIPELINE_BREAKERS = ["HashJoin", "Sort", "Minus", "GroupBy"]


def is_pipeline_breaker(label: str) -> bool:
    if not label:
        return False

    pattern = r"^(?:" + "|".join(PIPELINE_BREAKERS) + r")"
    match = re.match(pattern, label, re.IGNORECASE)
    return match is not None


def parse_memory_string(memory_string: str) -> int:
    """ Utility to convert a memory string (e.g. '1.5K' representing 1.5 kilobytes)
    to its bytes equivalent

    Raises ValueError if suffix representing unit of measurement not known or ommited in the input.
    """

    suffixes = {
        "K": 1024,
        "M": 1024 * 1024,
        "G": 1024 * 1024 * 1024,
        "T": 1024 * 1024 * 1024 * 1024,
    }

    try:
        numeric_value = float(memory_string[:-1])
        suffix = memory_string[-1].upper()

        if suffix in suffixes:
            bytes_value = int(numeric_value * suffixes[suffix])
            return bytes_value
        else:
            raise ValueError("Invalid memory string suffix.")
    except (ValueError, TypeError):
        raise ValueError("Invalid memory string format.")
