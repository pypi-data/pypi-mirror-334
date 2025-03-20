import asyncio
from typing import TypedDict, Any
from web3.types import ChecksumAddress, HexStr, TxParams
from .utils.clients import PublicClient, WalletClient
from . import asset as assets
from .portfolio_lib import asset_managers
from .portfolio_lib import integrations
from ..abis import abis

from ._internal.external_position_manager import (
    ACTION as EXTERNAL_POSITION_ACTION,
    call as call_external_position,
    call_encode as call_external_position_encode,
    call_decode as call_external_position_decode,
    CallArgs as ExternalPositionCallArgs,
    create as create_external_position,
    create_encode as create_external_position_encode,
    create_decode as create_external_position_decode,
    CreateArgs as CreateExternalPositionArgs,
    remove as remove_external_position,
    remove_encode as remove_external_position_encode,
    remove_decode as remove_external_position_decode,
    RemoveArgs as RemoveExternalPositionArgs,
    reactivate as reactivate_external_position,
    reactivate_encode as reactivate_external_position_encode,
    reactivate_decode as reactivate_external_position_decode,
    ReactivateArgs as ReactivateExternalPositionArgs,
)


from ._internal.integration_manager import (
    ACTION as INTEGRATION_ADAPTER_ACTION,
    SELECTOR as INTEGRATION_ADAPTER_SELECTOR,
    call as call_integration_adapter,
    call_encode as call_integration_adapter_encode,
    call_decode as call_integration_adapter_decode,
    CallArgs as CallIntegrationAdapterArgs,
    add_tracked_assets,
    add_tracked_assets_encode,
    add_tracked_assets_decode,
    AddTrackedAssetsArgs,
    remove_tracked_assets,
    remove_tracked_assets_encode,
    remove_tracked_assets_decode,
    RemoveTrackedAssetsArgs,
)


class VaultCallOnContractParams(TypedDict):
    client: WalletClient
    comptroller_proxy: ChecksumAddress
    contract: ChecksumAddress
    selector: HexStr
    encoded_args: HexStr


async def vault_call_on_contract(
    client: WalletClient,
    comptroller_proxy: ChecksumAddress,
    contract: ChecksumAddress,
    selector: HexStr,
    encoded_args: HexStr,
) -> TxParams:
    contract = client.contract(comptroller_proxy, abis.IComptrollerLib)
    function = contract.functions.vaultCallOnContract(contract, selector, encoded_args)
    return await client.populated_transaction(function)


async def get_portfolio(
    client: PublicClient,
    vault_proxy: ChecksumAddress,
) -> dict[str, Any]:
    external_position_addresses, tracked_asset_addresses = await asyncio.gather(
        get_active_external_positions(client, vault_proxy),
        get_tracked_assets(client, vault_proxy),
    )

    external_positions_data, tracked_assets_amounts = await asyncio.gather(
        asyncio.gather(
            *[
                get_external_position_type(client, pos)
                for pos in external_position_addresses
            ],
            *[
                get_external_position_debt_assets(client, pos)
                for pos in external_position_addresses
            ],
            *[
                get_external_position_managed_assets(client, pos)
                for pos in external_position_addresses
            ],
        ),
        asyncio.gather(
            *[
                assets.get_balance_of(client, vault_proxy, asset)
                for asset in tracked_asset_addresses
            ],
        ),
    )

    pos_count = len(external_position_addresses)
    types = external_positions_data[0:pos_count]
    debts = external_positions_data[pos_count : pos_count * 2]
    managed = external_positions_data[pos_count * 2 :]

    external_positions_data = [
        {
            "external_position": pos,
            "external_position_type": typ,
            "debt_assets": debt,
            "managed_assets": mng,
        }
        for pos, typ, debt, mng in zip(
            external_position_addresses, types, debts, managed
        )
    ]

    tracked_assets_data = [
        {"asset": asset, "amount": balance}
        for asset, balance in zip(tracked_asset_addresses, tracked_assets_amounts)
    ]

    return {
        "external_positions": external_positions_data,
        "tracked_assets": tracked_assets_data,
    }


async def get_tracked_assets(
    client: PublicClient,
    vault_proxy: ChecksumAddress,
) -> list[ChecksumAddress]:
    contract = client.contract(vault_proxy, abis.IVaultLib)
    function = contract.functions.getTrackedAssets()
    return await function.call()


# --------------------------------------------------------------------------------------------
# EXTERNAL POSITIONS
# --------------------------------------------------------------------------------------------


async def is_active_external_position(
    client: PublicClient,
    vault_proxy: ChecksumAddress,
    external_position: ChecksumAddress,
) -> bool:
    contract = client.contract(vault_proxy, abis.IVaultLib)
    function = contract.functions.isActiveExternalPosition(external_position)
    return await function.call()


async def get_total_value_for_all_external_positions(
    client: PublicClient,
    vault_proxy: ChecksumAddress,
) -> int:
    addresses = await get_active_external_positions(client, vault_proxy)
    external_position_assets = await asyncio.gather(
        *[get_external_position_assets(client, addr) for addr in addresses]
    )
    values = []
    for assets in external_position_assets:
        debt_assets = assets["debt_assets"]
        managed_assets = assets["managed_assets"]

        debt_assets_value = sum(asset["amount"] for asset in debt_assets)
        managed_assets_values = sum(asset["amount"] for asset in managed_assets)

        if managed_assets_values > debt_assets_value:
            values.append(managed_assets_values - debt_assets_value)
        else:
            values.append(0)

    return sum(values)


async def get_active_external_positions(
    client: PublicClient,
    vault_proxy: ChecksumAddress,
) -> list[ChecksumAddress]:
    contract = client.contract(vault_proxy, abis.IVaultLib)
    function = contract.functions.getActiveExternalPositions()
    return await function.call()


async def get_external_position_managed_assets(
    client: PublicClient,
    external_position: ChecksumAddress,
) -> list[dict[ChecksumAddress, int]]:
    contract = client.contract(external_position, abis.IExternalPosition)
    function = contract.functions.getManagedAssets()
    assets, amounts = await function.call()
    assert all(amount is not None for amount in amounts), "Missing managed asset amount"
    return [
        {
            "asset": asset,
            "amount": amount,
        }
        for asset, amount in zip(assets, amounts)
    ]


async def get_external_position_debt_assets(
    client: PublicClient,
    external_position: ChecksumAddress,
) -> list[dict[ChecksumAddress, int]]:
    contract = client.contract(external_position, abis.IExternalPosition)
    function = contract.functions.getDebtAssets()
    assets, amounts = await function.call()
    assert all(amount is not None for amount in amounts), "Missing debt asset amount"
    return [
        {
            "asset": asset,
            "amount": amount,
        }
        for asset, amount in zip(assets, amounts)
    ]


async def get_external_position_assets(
    client: PublicClient,
    external_position: ChecksumAddress,
) -> dict[str, list[dict[ChecksumAddress, int]]]:
    debt_assets, managed_assets = await asyncio.gather(
        get_external_position_debt_assets(client, external_position),
        get_external_position_managed_assets(client, external_position),
    )
    return {
        "debt_assets": debt_assets,
        "managed_assets": managed_assets,
    }


async def get_external_position_type(
    client: PublicClient,
    external_position: ChecksumAddress,
) -> int:
    contract = client.contract(external_position, abis.IExternalPositionProxy)
    function = contract.functions.getExternalPositionType()
    return await function.call()


async def get_type_label(
    client: PublicClient,
    external_position_factory: ChecksumAddress,
    type_id: int,
) -> str:
    contract = client.contract(external_position_factory, abis.IExternalPositionFactory)
    function = contract.functions.getTypeLabel(type_id)
    return await function.call()
