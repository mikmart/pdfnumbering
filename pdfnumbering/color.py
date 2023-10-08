def hex2rgb(code: str) -> tuple[int, int, int]:
    """
    Convert hex color code string to RGB tuple.
    """
    code = code.lstrip("#")
    try:
        r = int(code[0:2], base=16)
        g = int(code[2:4], base=16)
        b = int(code[4:6], base=16)
    except ValueError:
        raise ValueError(f"invalid hexadecimal color code: '#{code}'") from None
    return r, g, b
