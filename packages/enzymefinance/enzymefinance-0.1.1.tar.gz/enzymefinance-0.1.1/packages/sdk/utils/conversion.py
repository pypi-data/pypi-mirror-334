from decimal import Decimal


def to_int(value: Decimal, decimals: int) -> int:
    return int(value * 10**decimals)


def to_bps(value: Decimal) -> int:
    return int(value * 10000)


def to_wei(value: Decimal, decimals: int = 18) -> int:
    return int(value * 10**decimals)


def from_wei(value: int, decimals: int = 18) -> Decimal:
    return Decimal(value) / Decimal(10**decimals)


def to_seconds(
    years: float = 0, weeks: float = 0, days: float = 0, hours: float = 0, minutes: float = 0
) -> int:
    return int(
        years * 31557600 + weeks * 604800 + days * 86400 + hours * 3600 + minutes * 60
    )
