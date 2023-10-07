def hex2rgb(hex: str) -> tuple[int, int, int]:
    """
    Convert hex color code string to RGB tuple.
    """
    hex = hex.lstrip("#")
    try:
        r = int(hex[0:2], base=16)
        g = int(hex[2:4], base=16)
        b = int(hex[4:6], base=16)
    except ValueError:
        raise ValueError(f"Invalid hex color code: #{hex}")
    return r, g, b
