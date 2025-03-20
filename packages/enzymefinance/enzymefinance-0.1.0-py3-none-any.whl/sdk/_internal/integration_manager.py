from web3 import Web3
from web3.types import ChecksumAddress, HexStr, TxParams
from eth_abi import encode, decode
from typing import Callable, Any, TypedDict
from .extensions import call_extension
from ..utils.clients import WalletClient
from ..utils.encoding import encoding_to_types


class Action(TypedDict):
    call_on_integration: int
    add_tracked_assets: int
    remove_tracked_assets: int


ACTION = {
    "call_on_integration": 0,
    "add_tracked_assets": 1,
    "remove_tracked_assets": 2,
}


class Selector(TypedDict):
    action: HexStr
    claim_rewards: HexStr
    lend: HexStr
    lend_and_stake: HexStr
    redeem: HexStr
    stake: HexStr
    take_multiple_orders: HexStr
    take_order: HexStr
    transfer: HexStr
    unstake: HexStr
    unstake_and_redeem: HexStr
    wrap: HexStr


SELECTOR = {
    "action": "0xa7a19e00",  # action(address,bytes,bytes)
    "claim_rewards": "0xb9dfbacc",  # claimRewards(address,bytes,bytes)
    "lend": "0x099f7515",  # lend(address,bytes,bytes)
    "lend_and_stake": "0x29fa046e",  # lendAndStake(address,bytes,bytes)
    "redeem": "0xc29fa9dd",  # redeem(address,bytes,bytes)
    "stake": "0xfa7dd04d",  # stake(address,bytes,bytes)
    "take_multiple_orders": "0x0e7f692d",  # takeMultipleOrders(address,bytes,bytes)
    "take_order": "0x03e38a2b",  # takeOrder(address,bytes,bytes)
    "transfer": "0x3461917c",  # transfer(address,bytes,bytes)
    "unstake": "0x68e30677",  # unstake(address,bytes,bytes)
    "unstake_and_redeem": "0x8334eb99",  # unstakeAndRedeem(address,bytes,bytes)
    "wrap": "0xa5ca2d71",  # wrap(address,bytes,bytes)
}


class UseParams(TypedDict):
    client: WalletClient
    comptroller_proxy: ChecksumAddress
    integration_manager: ChecksumAddress
    integration_adapter: ChecksumAddress
    call_args: dict[str, Any]


def make_use(selector: HexStr, encoder: Callable) -> Callable:
    async def use_integration(
        client: WalletClient,
        comptroller_proxy: ChecksumAddress,
        integration_manager: ChecksumAddress,
        integration_adapter: ChecksumAddress,
        call_args: dict[str, Any],
    ) -> TxParams:
        return await call(
            client,
            comptroller_proxy,
            integration_manager,
            integration_adapter,
            selector,
            encoder(**call_args),
        )

    return use_integration


# --------------------------------------------------------------------------------------------
# CALL ON INTEGRATION
# --------------------------------------------------------------------------------------------

CALL_ENCODING = [
    {
        "type": "address",
        "name": "adapter",
    },
    {
        "type": "bytes4",
        "name": "selector",
    },
    {
        "type": "bytes",
        "name": "integrationData",
    },
]


class CallArgs(TypedDict):
    function_selector: HexStr
    integration_adapter: ChecksumAddress
    call_args: HexStr | None


def call_encode(
    function_selector: HexStr,
    integration_adapter: ChecksumAddress,
    call_args: HexStr | None,
) -> HexStr:
    types = encoding_to_types(CALL_ENCODING)
    values = [
        integration_adapter,
        Web3.to_bytes(hexstr=function_selector),
        Web3.to_bytes(hexstr=call_args or "0x"),
    ]
    return Web3.to_hex(encode(types, values))


def call_decode(encoded: HexStr) -> dict[str, HexStr | ChecksumAddress | HexStr]:
    """
    Returns:
            {
            "function_selector": HexStr,
            "integration_adapter": ChecksumAddress,
            "call_args": HexStr,
        }
    """
    types = encoding_to_types(CALL_ENCODING)
    decoded = decode(types, Web3.to_bytes(hexstr=encoded))
    return {
        "function_selector": Web3.to_hex(decoded[0]),
        "integration_adapter": decoded[1],
        "call_args": Web3.to_hex(decoded[2]),
    }


class CallParams(TypedDict):
    client: WalletClient
    comptroller_proxy: ChecksumAddress
    integration_manager: ChecksumAddress
    integration_adapter: ChecksumAddress
    function_selector: HexStr
    call_args: HexStr | None


async def call(
    client: WalletClient,
    comptroller_proxy: ChecksumAddress,
    integration_manager: ChecksumAddress,
    integration_adapter: ChecksumAddress,
    function_selector: HexStr,
    call_args: HexStr | None,
) -> TxParams:
    return await call_extension(
        client,
        comptroller_proxy,
        integration_manager,
        ACTION["call_on_integration"],
        call_encode(function_selector, integration_adapter, call_args or "0x"),
    )


# --------------------------------------------------------------------------------------------
# ADD TRACKED ASSET
# --------------------------------------------------------------------------------------------

ADD_TRACKED_ASSETS_ENCODING = [
    {
        "type": "address[]",
        "name": "assets",
    },
]


class AddTrackedAssetsArgs(TypedDict):
    add_assets: list[ChecksumAddress]


def add_tracked_assets_encode(add_assets: list[ChecksumAddress]) -> HexStr:
    types = encoding_to_types(ADD_TRACKED_ASSETS_ENCODING)
    values = [add_assets]
    return Web3.to_hex(encode(types, values))


def add_tracked_assets_decode(encoded: HexStr) -> dict[str, list[ChecksumAddress]]:
    """
    Returns:
        {
            "assets": list[ChecksumAddress],
        }
    """
    types = encoding_to_types(ADD_TRACKED_ASSETS_ENCODING)
    decoded = decode(types, Web3.to_bytes(hexstr=encoded))
    return {
        "assets": decoded[0],
    }


class AddTrackedAssetsParams(TypedDict):
    client: WalletClient
    comptroller_proxy: ChecksumAddress
    integration_manager: ChecksumAddress
    add_assets: list[ChecksumAddress]


async def add_tracked_assets(
    client: WalletClient,
    comptroller_proxy: ChecksumAddress,
    integration_manager: ChecksumAddress,
    add_assets: list[ChecksumAddress],
) -> TxParams:
    return await call_extension(
        client,
        comptroller_proxy,
        integration_manager,
        ACTION["add_tracked_assets"],
        add_tracked_assets_encode(add_assets),
    )


# --------------------------------------------------------------------------------------------
# REMOVE TRACKED ASSET
# --------------------------------------------------------------------------------------------

REMOVE_TRACKED_ASSETS_ENCODING = [
    {
        "type": "address[]",
        "name": "assets",
    },
]


class RemoveTrackedAssetsArgs(TypedDict):
    remove_assets: list[ChecksumAddress]


def remove_tracked_assets_encode(remove_assets: list[ChecksumAddress]) -> HexStr:
    types = encoding_to_types(REMOVE_TRACKED_ASSETS_ENCODING)
    values = [remove_assets]
    return Web3.to_hex(encode(types, values))


def remove_tracked_assets_decode(encoded: HexStr) -> dict[str, list[ChecksumAddress]]:
    """
    Returns:
        {
            "assets": list[ChecksumAddress],
        }
    """
    types = encoding_to_types(REMOVE_TRACKED_ASSETS_ENCODING)
    decoded = decode(types, Web3.to_bytes(hexstr=encoded))
    return {
        "assets": decoded[0],
    }


class RemoveTrackedAssetsParams(TypedDict):
    client: WalletClient
    comptroller_proxy: ChecksumAddress
    integration_manager: ChecksumAddress
    remove_assets: list[ChecksumAddress]


async def remove_tracked_assets(
    client: WalletClient,
    comptroller_proxy: ChecksumAddress,
    integration_manager: ChecksumAddress,
    remove_assets: list[ChecksumAddress],
) -> TxParams:
    return await call_extension(
        client,
        comptroller_proxy,
        integration_manager,
        ACTION["remove_tracked_assets"],
        remove_tracked_assets_encode(remove_assets),
    )
