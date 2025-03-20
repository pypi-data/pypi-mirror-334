from typing import TypedDict
from web3.types import ChecksumAddress, TxParams
from .utils.clients import PublicClient, WalletClient
from ..abis import abis


# --------------------------------------------------------------------------------------------
# TRANSACTIONS
# --------------------------------------------------------------------------------------------


class SetFreelyTransferableSharesParams(TypedDict):
    client: WalletClient
    vault_proxy: ChecksumAddress


async def set_freely_transferable_shares(
    client: WalletClient,
    vault_proxy: ChecksumAddress,
) -> TxParams:
    contract = client.contract(vault_proxy, abis.IVaultLib)
    function = contract.functions.setFreelyTransferableShares()
    return await client.populated_transaction(function)


class SetNominatedOwnerParams(TypedDict):
    client: WalletClient
    vault_proxy: ChecksumAddress
    next_nominated_owner: ChecksumAddress


async def set_nominated_owner(
    client: WalletClient,
    vault_proxy: ChecksumAddress,
    next_nominated_owner: ChecksumAddress,
) -> TxParams:
    contract = client.contract(vault_proxy, abis.IVaultLib)
    function = contract.functions.setNominatedOwner(next_nominated_owner)
    return await client.populated_transaction(function)


class RemoveNominatedOwnerParams(TypedDict):
    client: WalletClient
    vault_proxy: ChecksumAddress


async def remove_nominated_owner(
    client: WalletClient,
    vault_proxy: ChecksumAddress,
) -> TxParams:
    contract = client.contract(vault_proxy, abis.IVaultLib)
    function = contract.functions.removeNominatedOwner()
    return await client.populated_transaction(function)


class ClaimOwnershipParams(TypedDict):
    client: WalletClient
    vault_proxy: ChecksumAddress


async def claim_ownership(
    client: WalletClient,
    vault_proxy: ChecksumAddress,
) -> TxParams:
    contract = client.contract(vault_proxy, abis.IVaultLib)
    function = contract.functions.claimOwnership()
    return await client.populated_transaction(function)


class SetNameParams(TypedDict):
    client: WalletClient
    vault_proxy: ChecksumAddress
    name: str


async def set_name(
    client: WalletClient,
    vault_proxy: ChecksumAddress,
    name: str,
) -> TxParams:
    contract = client.contract(vault_proxy, abis.IVaultLib)
    function = contract.functions.setName(name)
    return await client.populated_transaction(function)


class SetSymbolParams(TypedDict):
    client: WalletClient
    vault_proxy: ChecksumAddress
    symbol: str


async def set_symbol(
    client: WalletClient,
    vault_proxy: ChecksumAddress,
    symbol: str,
) -> TxParams:
    contract = client.contract(vault_proxy, abis.IVaultLib)
    function = contract.functions.setSymbol(symbol)
    return await client.populated_transaction(function)


async def add_asset_managers(
    client: WalletClient,
    vault_proxy: ChecksumAddress,
    managers: list[ChecksumAddress],
) -> TxParams:
    contract = client.contract(vault_proxy, abis.IVaultLib)
    function = contract.functions.addAssetManagers(managers)
    return await client.populated_transaction(function)


async def remove_asset_managers(
    client: WalletClient,
    vault_proxy: ChecksumAddress,
    managers: list[ChecksumAddress],
) -> TxParams:
    contract = client.contract(vault_proxy, abis.IVaultLib)
    function = contract.functions.removeAssetManagers(managers)
    return await client.populated_transaction(function)


# --------------------------------------------------------------------------------------------
# READ FUNCTIONS
# --------------------------------------------------------------------------------------------


async def get_name(
    client: PublicClient,
    vault_proxy: ChecksumAddress,
) -> str:
    contract = client.contract(vault_proxy, abis.IVaultLib)
    function = contract.functions.name()
    return await function.call()


async def get_symbol(
    client: PublicClient,
    vault_proxy: ChecksumAddress,
) -> str:
    contract = client.contract(vault_proxy, abis.IVaultLib)
    function = contract.functions.symbol()
    return await function.call()


async def get_owner(
    client: PublicClient,
    vault_proxy: ChecksumAddress,
) -> ChecksumAddress:
    contract = client.contract(vault_proxy, abis.IVaultLib)
    function = contract.functions.getOwner()
    return await function.call()


async def get_nominated_owner(
    client: PublicClient,
    vault: ChecksumAddress,
) -> ChecksumAddress:
    contract = client.contract(vault, abis.IVaultLib)
    function = contract.functions.getNominatedOwner()
    return await function.call()


async def get_denomination_asset(
    client: PublicClient,
    comptroller_proxy: ChecksumAddress,
) -> ChecksumAddress:
    contract = client.contract(comptroller_proxy, abis.IComptrollerLib)
    function = contract.functions.getDenominationAsset()
    return await function.call()


async def get_comptroller_proxy(
    client: PublicClient,
    vault_proxy: ChecksumAddress,
) -> ChecksumAddress:
    contract = client.contract(vault_proxy, abis.IVaultLib)
    function = contract.functions.getAccessor()
    return await function.call()


async def get_policy_manager(
    client: PublicClient,
    comptroller_proxy: ChecksumAddress,
) -> ChecksumAddress:
    contract = client.contract(comptroller_proxy, abis.IComptrollerLib)
    function = contract.functions.getPolicyManager()
    return await function.call()


async def get_fee_manager(
    client: PublicClient,
    comptroller_proxy: ChecksumAddress,
) -> ChecksumAddress:
    contract = client.contract(comptroller_proxy, abis.IComptrollerLib)
    function = contract.functions.getFeeManager()
    return await function.call()


async def shares_are_freely_transferable(
    client: PublicClient,
    vault_proxy: ChecksumAddress,
) -> bool:
    contract = client.contract(vault_proxy, abis.IVaultLib)
    function = contract.functions.sharesAreFreelyTransferable()
    return await function.call()


async def get_fund_deployer(
    client: PublicClient,
    vault_proxy: ChecksumAddress,
) -> ChecksumAddress:
    contract = client.contract(vault_proxy, abis.IVaultLib)
    function = contract.functions.getFundDeployer()
    return await function.call()
