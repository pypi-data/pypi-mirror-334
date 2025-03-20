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
                "path_addresses": list[ChecksumAddress],
                "path_fees": list[int],
                "outgoing_asset_amount": int,
                "min_incoming_asset_amount": int,
            }
    """
    _take_order = integration_manager_lib.make_use(
        integration_manager_lib.SELECTOR["take_order"],
        take_order_encode,
    )
    return await _take_order(*args)


TAKE_ORDER_ENCODING = [
    {
        "name": "pathAddresses",
        "type": "address[]",
    },
    {
        "name": "pathFees",
        "type": "uint24[]",
    },
    {
        "name": "outgoingAssetAmount",
        "type": "uint256",
    },
    {
        "name": "minIncomingAssetAmount",
        "type": "uint256",
    },
]


class TakeOrderArgs(TypedDict):
    path_addresses: list[ChecksumAddress]
    path_fees: list[int]
    outgoing_asset_amount: int
    min_incoming_asset_amount: int


def take_order_encode(
    path_addresses: list[ChecksumAddress],
    path_fees: list[int],
    outgoing_asset_amount: int,
    min_incoming_asset_amount: int,
) -> HexStr:
    types = encoding_to_types(TAKE_ORDER_ENCODING)
    values = [
        path_addresses,
        path_fees,
        outgoing_asset_amount,
        min_incoming_asset_amount,
    ]
    return Web3.to_hex(encode(types, values))


def take_order_decode(encoded: HexStr) -> dict[str, Any]:
    """
    Returns:
        dict[str, Any]
            {
                "path_addresses": list[ChecksumAddress],
                "path_fees": list[int],
                "outgoing_asset_amount": int,
                "min_incoming_asset_amount": int,
            }
    """
    types = encoding_to_types(TAKE_ORDER_ENCODING)
    decoded = decode(types, Web3.to_bytes(hexstr=encoded))
    return {
        "path_addresses": [Web3.to_checksum_address(address) for address in decoded[0]],
        "path_fees": decoded[1],
        "outgoing_asset_amount": decoded[2],
        "min_incoming_asset_amount": decoded[3],
    }
