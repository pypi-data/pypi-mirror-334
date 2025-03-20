from typing import TypedDict
from web3 import Web3
from web3.types import ChecksumAddress, HexStr, TxParams
from eth_abi import encode, decode
from ..._internal import integration_manager as integration_manager_lib
from ...utils.encoding import encoding_to_types

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
                "executor": ChecksumAddress,
                "order_description": dict[str, Any],
                "data": HexStr,
            }
    """
    _take_order = integration_manager_lib.make_use(
        integration_manager_lib.SELECTOR["take_order"], take_order_encode
    )
    return await _take_order(*args)


TAKE_ORDER_ENCODING = [
    {
        "name": "executor",
        "type": "address",
    },
    {
        "components": [
            {
                "internalType": "address",
                "name": "srcToken",
                "type": "address",
            },
            {
                "internalType": "address",
                "name": "dstToken",
                "type": "address",
            },
            {
                "internalType": "address",
                "name": "srcReceiver",
                "type": "address",
            },
            {
                "internalType": "address",
                "name": "dstReceiver",
                "type": "address",
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "minReturnAmount",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "flags",
                "type": "uint256",
            },
        ],
        "name": "orderDescription",
        "type": "tuple",
    },
    {
        "name": "data",
        "type": "bytes",
    },
]


class OrderDescription(TypedDict):
    srcToken: ChecksumAddress
    dstToken: ChecksumAddress
    srcReceiver: ChecksumAddress
    dstReceiver: ChecksumAddress
    amount: int
    minReturnAmount: int
    flags: int


class TakeOrderArgs(TypedDict):
    executor: ChecksumAddress
    order_description: OrderDescription
    data: HexStr


def take_order_encode(
    executor: ChecksumAddress,
    order_description: OrderDescription,
    data: HexStr,
) -> HexStr:
    """
    Args:
        order_description:
            {
                "srcToken": ChecksumAddress,
                "dstToken": ChecksumAddress,
                "srcReceiver": ChecksumAddress,
                "dstReceiver": ChecksumAddress,
                "amount": int,
                "minReturnAmount": int,
                "flags": int,
            }
    """
    types = encoding_to_types(TAKE_ORDER_ENCODING)
    values = [
        executor,
        (
            order_description["srcToken"],
            order_description["dstToken"],
            order_description["srcReceiver"],
            order_description["dstReceiver"],
            order_description["amount"],
            order_description["minReturnAmount"],
            order_description["flags"],
        ),
        Web3.to_bytes(hexstr=data),
    ]
    return Web3.to_hex(encode(types, values))


def take_order_decode(
    encoded: HexStr,
) -> dict[str, ChecksumAddress | dict[str, ChecksumAddress | int] | HexStr]:
    """
    Returns:
        {
            "executor": ChecksumAddress,
            "order_description": {
                "src_token": ChecksumAddress,
                "dst_token": ChecksumAddress,
                "src_receiver": ChecksumAddress,
                "dst_receiver": ChecksumAddress,
                "amount": int,
                "min_return_amount": int,
                "flags": int,
            },
            "data": HexStr,
        }
    """
    types = encoding_to_types(TAKE_ORDER_ENCODING)
    decoded = decode(types, Web3.to_bytes(hexstr=encoded))
    return {
        "executor": Web3.to_checksum_address(decoded[0]),
        "order_description": {
            "src_token": Web3.to_checksum_address(decoded[1][0]),
            "dst_token": Web3.to_checksum_address(decoded[1][1]),
            "src_receiver": Web3.to_checksum_address(decoded[1][2]),
            "dst_receiver": Web3.to_checksum_address(decoded[1][3]),
            "amount": decoded[1][4],
            "min_return_amount": decoded[1][5],
            "flags": decoded[1][6],
        },
        "data": Web3.to_hex(decoded[2]),
    }


SWAP_ARGS_ENCODING = [
    {
        "name": "executor",
        "type": "address",
    },
    {
        "components": [
            {
                "internalType": "address",
                "name": "srcToken",
                "type": "address",
            },
            {
                "internalType": "address",
                "name": "dstToken",
                "type": "address",
            },
            {
                "internalType": "address",
                "name": "srcReceiver",
                "type": "address",
            },
            {
                "internalType": "address",
                "name": "dstReceiver",
                "type": "address",
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "minReturnAmount",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "flags",
                "type": "uint256",
            },
        ],
        "name": "orderDescription",
        "type": "tuple",
    },
    {
        "name": "unknown",
        "type": "bytes",
    },
    {
        "name": "data",
        "type": "bytes",
    },
]


def decoded_swap_args(
    encoded: HexStr,
) -> dict[str, ChecksumAddress | dict[str, ChecksumAddress | int] | HexStr]:
    """
    Returns:
        {
            "executor": ChecksumAddress,
            "order_description": {
                "src_token": ChecksumAddress,
                "dst_token": ChecksumAddress,
                "src_receiver": ChecksumAddress,
                "dst_receiver": ChecksumAddress,
                "amount": int,
                "min_return_amount": int,
                "flags": int,
            },
            "data": HexStr,
        }
    """
    types = encoding_to_types(SWAP_ARGS_ENCODING)
    decoded = decode(types, Web3.to_bytes(hexstr=encoded))
    return {
        "executor": Web3.to_checksum_address(decoded[0]),
        "order_description": {
            "src_token": Web3.to_checksum_address(decoded[1][0]),
            "dst_token": Web3.to_checksum_address(decoded[1][1]),
            "src_receiver": Web3.to_checksum_address(decoded[1][2]),
            "dst_receiver": Web3.to_checksum_address(decoded[1][3]),
            "amount": decoded[1][4],
            "min_return_amount": decoded[1][5],
            "flags": decoded[1][6],
        },
        "data": Web3.to_hex(decoded[3]),
    }
