from web3.types import ChecksumAddress
from .utils.clients import PublicClient
from web3.exceptions import ContractLogicError
from ..abis import abis


async def get_nav(
    client: PublicClient,
    vault_proxy: ChecksumAddress,
    value_calculator: ChecksumAddress,
) -> dict[ChecksumAddress, int]:
    contract = client.contract(value_calculator, abis.IFundValueCalculatorRouter)
    function = contract.functions.calcNav(vault_proxy)
    asset, value = await function.call()
    return {"asset": asset, "value": value}


async def get_nav_in_asset(
    client: PublicClient,
    asset: ChecksumAddress,
    vault_proxy: ChecksumAddress,
    value_calculator: ChecksumAddress,
) -> int:
    contract = client.contract(value_calculator, abis.IFundValueCalculatorRouter)
    function = contract.functions.calcNavInAsset(vault_proxy, asset)
    return await function.call()


async def get_gav(
    client: PublicClient,
    vault_proxy: ChecksumAddress,
    value_calculator: ChecksumAddress,
) -> dict[ChecksumAddress, int]:
    contract = client.contract(value_calculator, abis.IFundValueCalculatorRouter)
    function = contract.functions.calcGav(vault_proxy)
    asset, value = await function.call()
    return {"asset": asset, "value": value}


async def get_gav_in_asset(
    client: PublicClient,
    asset: ChecksumAddress,
    vault_proxy: ChecksumAddress,
    value_calculator: ChecksumAddress,
) -> int:
    contract = client.contract(value_calculator, abis.IFundValueCalculatorRouter)
    function = contract.functions.calcGavInAsset(vault_proxy, asset)
    return await function.call()


async def get_share_price(
    client: PublicClient,
    vault_proxy: ChecksumAddress,
    value_calculator: ChecksumAddress,
) -> dict[ChecksumAddress, int]:
    contract = client.contract(value_calculator, abis.IFundValueCalculatorRouter)
    function = contract.functions.calcNetShareValue(vault_proxy)
    asset, value = await function.call()
    return {"asset": asset, "value": value}


async def get_share_price_in_asset(
    client: PublicClient,
    asset: ChecksumAddress,
    vault_proxy: ChecksumAddress,
    value_calculator: ChecksumAddress,
) -> int:
    contract = client.contract(value_calculator, abis.IFundValueCalculatorRouter)
    function = contract.functions.calcNetShareValueInAsset(vault_proxy, asset)
    return await function.call()


async def get_canonical_asset_value(
    client: PublicClient,
    asset: ChecksumAddress,
    value_calculator: ChecksumAddress,
) -> int:
    contract = client.contract(value_calculator, abis.IValueInterpreter)
    function = contract.functions.calcCanonicalAssetValue(asset)
    try:
        return await function.call()
    except ContractLogicError:  # TODO: More selectively catch this error here.
        return None


async def calc_canonical_assets_total_value(
    client: PublicClient,
    value_interpreter: ChecksumAddress,
    base_assets: list[ChecksumAddress],
    amounts: list[int],
    quote_asset: ChecksumAddress,
) -> int:
    contract = client.contract(value_interpreter, abis.IValueInterpreter)
    function = contract.functions.calcCanonicalAssetsTotalValue(
        base_assets, amounts, quote_asset
    )
    try:
        return await function.call()
    except ContractLogicError:  # TODO: More selectively catch this error here.
        return None
