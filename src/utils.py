def format_compact(value):
    try:
        num = float(value)
    except (TypeError, ValueError):
        return value

    abs_num = abs(num)
    if abs_num >= 1_000_000_000_000:
        return f"{num/1_000_000_000_000:.2f}T"
    if abs_num >= 1_000_000_000:
        return f"{num/1_000_000_000:.2f}B"
    if abs_num >= 1_000_000:
        return f"{num/1_000_000:.2f}M"
    if abs_num >= 1_000:
        return f"{num/1_000:.2f}K"
    return f"{num:,.0f}" if abs_num >= 1 else f"{num:.2f}"
