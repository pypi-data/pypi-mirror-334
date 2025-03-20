from typing import Any


def encoding_to_types(encoding: list[dict[str, Any]]) -> list[str]:
    def parse_type(item: dict[str, Any]) -> str:
        if item["type"].startswith("tuple"):
            inner_types = ",".join(parse_type(comp) for comp in item["components"])
            return f"({inner_types}){item['type'][5:]}"
        return item["type"]

    return [parse_type(item) for item in encoding]
