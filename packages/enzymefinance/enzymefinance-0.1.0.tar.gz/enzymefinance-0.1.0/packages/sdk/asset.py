import asyncio
from typing import TypedDict
from web3.types import ChecksumAddress, TxParams
from .utils.clients import WalletClient, PublicClient
from ..abis import abis


# --------------------------------------------------------------------------------------------
# TRANSACTIONS
# --------------------------------------------------------------------------------------------


class ApproveParams(TypedDict):
    client: WalletClient
    asset: ChecksumAddress
    spender: ChecksumAddress
    amount: int


async def approve(
    client: WalletClient,
    asset: ChecksumAddress,
    spender: ChecksumAddress,
    amount: int,
) -> TxParams:
    contract = client.contract(asset, abis.IERC20)
    function = contract.functions.approve(spender, amount)
    return await function.call()


# --------------------------------------------------------------------------------------------
# READ FUNCTIONS
# --------------------------------------------------------------------------------------------


async def get_info(
    client: PublicClient,
    asset: ChecksumAddress,
) -> dict[str, str | int]:
    """
    Returns:
        {
            "name": str,
            "symbol": str,
            "decimals": int,
        }
    """
    info = await asyncio.gather(
        get_name(client, asset),
        get_symbol(client, asset),
        get_decimals(client, asset),
    )
    return {
        "name": info[0],
        "symbol": info[1],
        "decimals": info[2],
    }


async def get_name(
    client: PublicClient,
    asset: ChecksumAddress,
) -> str:
    # TODO: Handle case where name is a bytes32
    contract = client.contract(asset, abis.IERC20)
    function = contract.functions.name()
    return await function.call()


async def get_symbol(
    client: PublicClient,
    asset: ChecksumAddress,
) -> str:
    # TODO: Handle case where symbol is a bytes32
    contract = client.contract(asset, abis.IERC20)
    function = contract.functions.symbol()
    return await function.call()


async def get_balance_of(
    client: PublicClient,
    owner: ChecksumAddress,
    asset: ChecksumAddress,
) -> int:
    contract = client.contract(asset, abis.IERC20)
    function = contract.functions.balanceOf(owner)
    return await function.call()


async def get_balances_of(
    client: PublicClient,
    owner: ChecksumAddress,
    assets: list[ChecksumAddress],
) -> list[dict[ChecksumAddress, int]]:
    """
    Returns:
        [
            {
                "asset": ChecksumAddress,
                "balance": int,
            },
            ...
        ]
    """
    balances = await asyncio.gather(
        *[get_balance_of(client, owner, asset) for asset in assets],
    )
    return [
        {
            "asset": assets[i],
            "balance": balances[i],
        }
        for i in range(len(assets))
    ]


async def get_allowance(
    client: PublicClient,
    asset: ChecksumAddress,
    owner: ChecksumAddress,
    spender: ChecksumAddress,
) -> int:
    contract = client.contract(asset, abis.IERC20)
    function = contract.functions.allowance(owner, spender)
    return await function.call()


async def get_decimals(
    client: PublicClient,
    asset: ChecksumAddress,
) -> int:
    contract = client.contract(asset, abis.IERC20)
    function = contract.functions.decimals()
    return await function.call()


async def get_total_supply(
    client: PublicClient,
    asset: ChecksumAddress,
) -> int:
    contract = client.contract(asset, abis.IERC20)
    function = contract.functions.totalSupply()
    return await function.call()


async def get_canonical_value(
    client: PublicClient,
    value_interpreter: ChecksumAddress,
    base_asset: ChecksumAddress,
    quote_asset: ChecksumAddress,
    amount: int,
) -> int:
    contract = client.contract(value_interpreter, abis.IValueInterpreter)
    function = contract.functions.calcCanonicalAssetValue(
        base_asset, amount, quote_asset
    )
    return await function.call()
