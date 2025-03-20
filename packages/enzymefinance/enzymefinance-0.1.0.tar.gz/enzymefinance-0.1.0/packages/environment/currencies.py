from typing import Any, Literal, TypedDict, get_args


Currency = Literal[
    "USD",
    "AUD",
    "BTC",
    "CHF",
    "ETH",
    "EUR",
    "GBP",
    "JPY",
]


CurrencySlug = Literal[
    "usd",
    "aud",
    "btc",
    "chf",
    "eth",
    "eur",
    "gbp",
    "jpy",
]


class CurrencyDefinition(TypedDict):
    id: Currency
    slug: CurrencySlug
    label: str


SLUG_BY_CURRENCY = dict(zip(get_args(Currency), get_args(CurrencySlug)))


CURRENCY_BY_SLUG = dict(zip(get_args(CurrencySlug), get_args(Currency)))


def get_currency(currency_or_slug: Currency | CurrencySlug) -> CurrencyDefinition:
    if is_supported_currency(currency_or_slug):
        return CURRENCIES[currency_or_slug]
    if is_supported_currency_slug(currency_or_slug):
        return CURRENCIES[CURRENCY_BY_SLUG[currency_or_slug]]
    raise ValueError(f"Invalid currency {currency_or_slug}")


def is_currency_identifier(value: Any) -> bool:
    return is_supported_currency(value) or is_supported_currency_slug(value)


def is_supported_currency(value: Any) -> bool:
    return isinstance(value, str) and value in get_args(Currency)


def is_supported_currency_slug(value: Any) -> bool:
    return isinstance(value, str) and value in get_args(CurrencySlug)


class ReleasesTypeVersion(TypedDict, total=False):
    sulu: str  # f"{Deployment}.{Version}"
    encore: str  # f"{Deployment}.{Version}"
    phoenix: str  # f"{Deployment}.{Version}"


class CurrenciesType(TypedDict):
    ETH: CurrencyDefinition
    BTC: CurrencyDefinition
    USD: CurrencyDefinition
    EUR: CurrencyDefinition
    CHF: CurrencyDefinition
    GBP: CurrencyDefinition
    AUD: CurrencyDefinition
    JPY: CurrencyDefinition


CURRENCIES = {
    "ETH": {
        "id": "ETH",
        "label": "Ether",
        "slug": "eth",
    },
    "BTC": {
        "id": "BTC",
        "label": "Bitcoin",
        "slug": "btc",
    },
    "USD": {
        "id": "USD",
        "label": "United States dollar",
        "slug": "usd",
    },
    "EUR": {
        "id": "EUR",
        "label": "Euro",
        "slug": "eur",
    },
    "CHF": {
        "id": "CHF",
        "label": "Swiss franc",
        "slug": "chf",
    },
    "GBP": {
        "id": "GBP",
        "label": "Pound sterling",
        "slug": "gbp",
    },
    "AUD": {
        "id": "AUD",
        "label": "Australian dollar",
        "slug": "aud",
    },
    "JPY": {
        "id": "JPY",
        "label": "Japanese yen",
        "slug": "jpy",
    },
}
