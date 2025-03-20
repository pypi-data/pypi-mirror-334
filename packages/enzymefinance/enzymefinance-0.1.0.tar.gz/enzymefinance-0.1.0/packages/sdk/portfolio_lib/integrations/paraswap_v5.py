from web3 import Web3
from web3.types import ChecksumAddress, HexStr, TxParams
from eth_abi import encode, decode
from ..._internal import integration_manager as integration_manager_lib
from ...utils.encoding import encoding_to_types
from typing import Any, TypedDict

# --------------------------------------------------------------------------------------------
# TAKE ORDER
# --------------------------------------------------------------------------------------------


async def take_order(*args) -> TxParams:
    """
    Args:
        client: WalletClient
        comptroller_proxy: ChecksumAddress
        integration_manager: ChecksumAddress
        integration_adapter: ChecksumAddress
        call_args: dict[str, Any]
            {
                "expected_incoming_asset_amount": int,
                "min_incoming_asset_amount": int,
                "outgoing_asset": ChecksumAddress,
                "outgoing_asset_amount": int,
                "uuid": HexStr,
                "swap_type": int,
                "swap_data": Any,
            }
    """
    _take_order = integration_manager_lib.make_use(
        integration_manager_lib.SELECTOR["take_order"], take_order_encode
    )
    return await _take_order(*args)


TAKE_ORDER_ENCODING = [
    {
        "name": "minIncomingAssetAmount",
        "type": "uint256",
    },
    {
        "name": "expectedIncomingAssetAmount",
        "type": "uint256",
    },
    {
        "name": "outgoingAsset",
        "type": "address",
    },
    {
        "name": "outgoingAssetAmount",
        "type": "uint256",
    },
    {
        "name": "uuid",
        "type": "bytes16",
    },
    {
        "name": "swapType",
        "type": "uint256",
    },
    {
        "name": "swapData",
        "type": "bytes",
    },
]

ROUTE_ENCODING = {
    "components": [
        {
            "name": "index",
            "type": "uint256",
        },
        {
            "name": "targetExchange",
            "type": "address",
        },
        {
            "name": "percent",
            "type": "uint256",
        },
        {
            "name": "payload",
            "type": "bytes",
        },
        {
            "name": "networkFee",
            "type": "uint256",
        },
    ]
}

ADAPTER_ENCODING = {
    "components": [
        {
            "name": "adapter",
            "type": "address",
        },
        {
            "name": "percent",
            "type": "uint256",
        },
        {
            "name": "networkFee",
            "type": "uint256",
        },
        {
            "name": "route",
            "type": "tuple[]",
            "components": ROUTE_ENCODING["components"],
        },
    ],
}

PATH_ENCODING = {
    "components": [
        {
            "name": "to",
            "type": "address",
        },
        {
            "name": "totalNetworkFee",
            "type": "uint256",
        },
        {
            "name": "adapters",
            "type": "tuple[]",
            "components": ADAPTER_ENCODING["components"],
        },
    ],
}

MEGA_SWAP_DATA_ENCODING = [
    {
        "components": [
            {
                "name": "fromAmountPercent",
                "type": "uint256",
            },
            {
                "name": "path",
                "type": "tuple[]",
                "components": PATH_ENCODING["components"],
            },
        ],
        "name": "megaSwapData",
        "type": "tuple[]",
    }
]

MULTI_SWAP_DATA_ENCODING = [
    {
        "name": "multiSwapPath",
        "type": "tuple[]",
        "components": PATH_ENCODING["components"],
    }
]

SIMPLE_SWAP_DATA_ENCODING = [
    {
        "components": [
            {
                "name": "incomingAsset",
                "type": "address",
            },
            {
                "name": "callees",
                "type": "address[]",
            },
            {
                "name": "exchangeData",
                "type": "bytes",
            },
            {
                "name": "startIndexes",
                "type": "uint256[]",
            },
            {
                "name": "values",
                "type": "uint256[]",
            },
        ],
        "name": "simpleSwapParams",
        "type": "tuple",
    }
]


class Route(TypedDict):
    index: int
    targetExchange: ChecksumAddress
    percent: int
    payload: HexStr
    networkFee: int


class Adapter(TypedDict):
    adapter: ChecksumAddress
    percent: int
    networkFee: int
    route: list[Route]


class Path(TypedDict):
    to: ChecksumAddress
    totalNetworkFee: int
    adapters: list[Adapter]


class MegaSwapPathData(TypedDict):
    fromAmountPercent: int
    path: list[Path]


MegaSwapData = list[MegaSwapPathData]
MultiSwapData = list[Path]


class SimpleSwapData(TypedDict):
    incomingAsset: ChecksumAddress
    callees: list[ChecksumAddress]
    exchangeData: HexStr
    startIndexes: list[int]
    values: list[int]


class SwapType(TypedDict):
    simple: int
    multi: int
    mega: int


SWAP_TYPE = {
    "simple": 0,
    "multi": 1,
    "mega": 2,
}


class TakeOrderArgs(TypedDict):
    expected_incoming_asset_amount: int
    min_incoming_asset_amount: int
    outgoing_asset: ChecksumAddress
    outgoing_asset_amount: int
    uuid: HexStr
    swap_type: int
    swap_data: MegaSwapData | MultiSwapData | SimpleSwapData


def take_order_encode(
    expected_incoming_asset_amount: int,
    min_incoming_asset_amount: int,
    outgoing_asset: ChecksumAddress,
    outgoing_asset_amount: int,
    uuid: HexStr,
    swap_type: int,
    swap_data: Any,
) -> HexStr:
    """
    Args:
        if swap_type == 0 (simple):
            swap_data:
                {
                    "incomingAsset": ChecksumAddress,
                    "callees": list[ChecksumAddress],
                    "exchangeData": HexStr,
                    "startIndexes": list[int],
                    "values": list[int],
                }
        elif swap_type == 1 (multi):
            swap_data:
                [
                    {
                        "to": ChecksumAddress,
                        "totalNetworkFee": int,
                        "adapters":
                            [
                                {
                                    "adapter": ChecksumAddress,
                                    "percent": int,
                                    "networkFee": int,
                                    "route":
                                        [
                                            {
                                                "index": int,
                                                "targetExchange": ChecksumAddress,
                                                "percent": int,
                                                "payload": HexStr,
                                                "networkFee": int,
                                            }
                                        ]
                                }
                            ]
                    }
                ]
        elif swap_type == 2 (mega):
            swap_data:
                [
                    {
                        "fromAmountPercent": int,
                        "path":
                            [
                                {
                                    "to": ChecksumAddress,
                                    "totalNetworkFee": int,
                                    "adapters":
                                        [
                                            {
                                                "adapter": ChecksumAddress,
                                                "percent": int,
                                                "networkFee": int,
                                                "route":
                                                    [
                                                        {
                                                            "index": int,
                                                            "targetExchange": ChecksumAddress,
                                                            "percent": int,
                                                            "payload": HexStr,
                                                            "networkFee": int,
                                                        }
                                                    ]
                                            }
                                        ]
                                }
                            ]
                    }
                ]
    """

    def _extract_paths_values(paths):
        paths_values = []
        for path in paths:
            adapters_values = []
            for adapter in path["adapters"]:
                route_values = []
                for route in adapter["route"]:
                    route_values.append(
                        (
                            int(route["index"]),
                            Web3.to_checksum_address(route["targetExchange"]),
                            int(route["percent"]),
                            Web3.to_bytes(hexstr=route["payload"]),
                            int(route["networkFee"]),
                        )
                    )
                adapters_values.append(
                    (
                        Web3.to_checksum_address(adapter["adapter"]),
                        int(adapter["percent"]),
                        int(adapter["networkFee"]),
                        route_values,
                    )
                )
            paths_values.append(
                (
                    Web3.to_checksum_address(path["to"]),
                    int(path["totalNetworkFee"]),
                    adapters_values,
                )
            )
        return paths_values

    if swap_type == SWAP_TYPE["mega"]:
        swap_data_types = encoding_to_types(MEGA_SWAP_DATA_ENCODING)
        swap_data_values = [
            [
                (int(part["fromAmountPercent"]), _extract_paths_values(part["path"]))
                for part in swap_data
            ]
        ]
    elif swap_type == SWAP_TYPE["multi"]:
        swap_data_types = encoding_to_types(MULTI_SWAP_DATA_ENCODING)
        swap_data_values = [_extract_paths_values(swap_data)]
    elif swap_type == SWAP_TYPE["simple"]:
        swap_data_types = encoding_to_types(SIMPLE_SWAP_DATA_ENCODING)
        swap_data_values = [
            (
                swap_data["incoming_asset"],
                swap_data["callees"],
                Web3.to_bytes(hexstr=swap_data["exchange_data"]),
                swap_data["start_indexes"],
                swap_data["values"],
            ),
        ]
    else:
        raise ValueError(f"Invalid swap_type: {swap_type}")

    encoded_swap_data = encode(swap_data_types, swap_data_values)

    types = encoding_to_types(TAKE_ORDER_ENCODING)
    values = [
        min_incoming_asset_amount,
        expected_incoming_asset_amount,
        outgoing_asset,
        outgoing_asset_amount,
        Web3.to_bytes(hexstr=uuid),
        swap_type,
        encoded_swap_data,
    ]
    return Web3.to_hex(encode(types, values))


def take_order_decode(encoded: HexStr) -> dict[str, Any]:
    """
    Returns:
        dict[str, Any]
            {
                "min_incoming_asset_amount": int,
                "expected_incoming_asset_amount": int,
                "outgoing_asset": ChecksumAddress,
                "outgoing_asset_amount": int,
                "uuid": HexStr,
                "swap_type": int,
                "swap_data": Any,
            }
    """
    types = encoding_to_types(TAKE_ORDER_ENCODING)
    decoded = decode(types, Web3.to_bytes(hexstr=encoded))

    swap_type = decoded[5]
    swap_data_encoded = decoded[6]

    def _rebuild_paths_values(paths_values):
        paths = []
        for path in paths_values:
            adapters = []
            for adapter in path[2]:
                routes = []
                for route in adapter[3]:
                    routes.append(
                        {
                            "index": route[0],
                            "targetExchange": Web3.to_checksum_address(route[1]),
                            "percent": route[2],
                            "payload": Web3.to_hex(route[3]),
                            "networkFee": route[4],
                        }
                    )
                adapters.append(
                    {
                        "adapter": Web3.to_checksum_address(adapter[0]),
                        "percent": adapter[1],
                        "networkFee": adapter[2],
                        "route": routes,
                    }
                )
            paths.append(
                {
                    "to": Web3.to_checksum_address(path[0]),
                    "totalNetworkFee": path[1],
                    "adapters": adapters,
                }
            )
        return paths

    if swap_type == SWAP_TYPE["mega"]:
        swap_data_types = encoding_to_types(MEGA_SWAP_DATA_ENCODING)
        (swap_data_decoded,) = decode(swap_data_types, swap_data_encoded)
        swap_data = [
            {
                "fromAmountPercent": part[0],
                "path": _rebuild_paths_values(part[1]),
            }
            for part in swap_data_decoded
        ]
    elif swap_type == SWAP_TYPE["multi"]:
        swap_data_types = encoding_to_types(MULTI_SWAP_DATA_ENCODING)
        (swap_data_decoded,) = decode(swap_data_types, swap_data_encoded)
        swap_data = _rebuild_paths_values(swap_data_decoded)
    elif swap_type == SWAP_TYPE["simple"]:
        swap_data_types = encoding_to_types(SIMPLE_SWAP_DATA_ENCODING)
        (swap_data_decoded,) = decode(swap_data_types, swap_data_encoded)
        swap_data = {
            "incoming_asset": swap_data_decoded[0],
            "callees": list(swap_data_decoded[1]),
            "exchange_data": Web3.to_hex(swap_data_decoded[2]),
            "start_indexes": list(swap_data_decoded[3]),
            "values": list(swap_data_decoded[4]),
        }
    else:
        raise ValueError(f"Invalid swap_type: {swap_type}")

    return {
        "min_incoming_asset_amount": decoded[0],
        "expected_incoming_asset_amount": decoded[1],
        "outgoing_asset": decoded[2],
        "outgoing_asset_amount": decoded[3],
        "uuid": Web3.to_hex(decoded[4]),
        "swap_type": swap_type,
        "swap_data": swap_data,
    }


# --------------------------------------------------------------------------------------------
# TAKE MULTIPLE ORDERS
# --------------------------------------------------------------------------------------------


async def take_multiple_orders(*args) -> TxParams:
    """
    Args:
        client: WalletClient
        comptroller_proxy: ChecksumAddress
        integration_manager: ChecksumAddress
        integration_adapter: ChecksumAddress
        call_args: dict[str, Any]
            {
                "allow_orders_to_fail": bool,
                "orders": list[dict[str, Any]],
            }
    """
    _take_multiple_orders = integration_manager_lib.make_use(
        integration_manager_lib.SELECTOR["take_multiple_orders"],
        take_multiple_orders_encode,
    )
    return await _take_multiple_orders(*args)


TAKE_MULTIPLE_ORDERS_ENCODING = [
    {
        "name": "ordersData",
        "type": "bytes[]",
    },
    {
        "name": "allowOrdersToFail",
        "type": "bool",
    },
]


class TakeMultipleOrdersArgs(TypedDict):
    allow_orders_to_fail: bool
    orders: list[TakeOrderArgs]


def take_multiple_orders_encode(
    allow_orders_to_fail: bool,
    orders: list[TakeOrderArgs],
) -> HexStr:
    """
    Args:
        orders: list[dict[str, Any]]
            [
                {
                    "expected_incoming_asset_amount": int,
                    "min_incoming_asset_amount": int,
                    "outgoing_asset": ChecksumAddress,
                    "outgoing_asset_amount": int,
                    "uuid": HexStr,
                    "swap_type": int,
                    "swap_data": Any,
                }
            ]
    """
    orders_data = [Web3.to_bytes(hexstr=take_order_encode(**order)) for order in orders]
    types = encoding_to_types(TAKE_MULTIPLE_ORDERS_ENCODING)
    values = [orders_data, allow_orders_to_fail]
    return Web3.to_hex(encode(types, values))


def take_multiple_orders_decode(encoded: HexStr) -> dict[str, Any]:
    """
    Returns:
        dict[str, Any]
            {
                "orders": list[dict[str, Any]],
                "allow_orders_to_fail": bool,
            }
    """
    types = encoding_to_types(TAKE_MULTIPLE_ORDERS_ENCODING)
    decoded = decode(types, Web3.to_bytes(hexstr=encoded))

    return {
        "orders": [take_order_decode(Web3.to_hex(order)) for order in decoded[0]],
        "allow_orders_to_fail": decoded[1],
    }
