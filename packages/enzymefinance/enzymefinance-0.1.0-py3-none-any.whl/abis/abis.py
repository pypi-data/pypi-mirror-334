import json
from pathlib import Path
from typing import Any

_abis: dict[str, Any] = {}

base_path = Path(__file__).parent
abis_path = base_path / "abis"

def __getattr__(name: str) -> Any:
    if name in _abis:
        return _abis[name]

    json_file = abis_path / f"{name}.abi.json"
    if json_file.is_file():
        try:
            with open(json_file, "r") as f:
                _abis[name] = json.load(f)
            return _abis[name]
        except json.JSONDecodeError:
            raise ImportError(f"Invalid JSON in {json_file}")
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = [f.stem.split(".abi")[0] for f in abis_path.glob("*.abi.json")]