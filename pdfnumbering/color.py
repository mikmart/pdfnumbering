def hex2rgb(hex: str) -> tuple[int, int, int]:
    """
    Convert hex color code to RGB tuple.
    """
    hex = hex.lstrip("#")
    r = int(hex[0:2], base=16)
    g = int(hex[2:4], base=16)
    b = int(hex[4:6], base=16)
    return r, g, b
