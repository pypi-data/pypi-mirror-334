from web3.types import ChecksumAddress
from .utils.clients import PublicClient
from ..abis import abis


async def is_supported_asset(
    client: PublicClient,
    value_interpreter: ChecksumAddress,
    asset: ChecksumAddress,
) -> bool:
    contract = client.contract(value_interpreter, abis.IValueInterpreter)
    function = contract.functions.isSupportedAsset(asset)
    return await function.call()


async def is_supported_asset_for_derivative_price_feed(
    client: PublicClient,
    derivative_price_feed: ChecksumAddress,
    asset: ChecksumAddress,
) -> bool:
    contract = client.contract(derivative_price_feed, abis.IDerivativePriceFeed)
    function = contract.functions.isSupportedAsset(asset)
    return await function.call()


async def is_supported_primitive_asset(
    client: PublicClient,
    value_interpreter: ChecksumAddress,
    asset: ChecksumAddress,
) -> bool:
    contract = client.contract(value_interpreter, abis.IValueInterpreter)
    function = contract.functions.isSupportedPrimitiveAsset(asset)
    return await function.call()


async def is_supported_derivative_asset(
    client: PublicClient,
    value_interpreter: ChecksumAddress,
    asset: ChecksumAddress,
) -> bool:
    contract = client.contract(value_interpreter, abis.IValueInterpreter)
    function = contract.functions.isSupportedDerivativeAsset(asset)
    return await function.call()


async def get_aggregator_for_primitive(
    client: PublicClient,
    value_interpreter: ChecksumAddress,
    asset: ChecksumAddress,
) -> ChecksumAddress:
    contract = client.contract(value_interpreter, abis.IValueInterpreter)
    function = contract.functions.getAggregatorForPrimitive(asset)
    return await function.call()


async def get_rate_asset_for_primitive(
    client: PublicClient,
    value_interpreter: ChecksumAddress,
    asset: ChecksumAddress,
) -> ChecksumAddress:
    contract = client.contract(value_interpreter, abis.IValueInterpreter)
    function = contract.functions.getRateAssetForPrimitive(asset)
    return await function.call()


async def get_price_feed_for_derivative(
    client: PublicClient,
    value_interpreter: ChecksumAddress,
    asset: ChecksumAddress,
) -> ChecksumAddress:
    contract = client.contract(value_interpreter, abis.IValueInterpreter)
    function = contract.functions.getPriceFeedForDerivative(asset)
    return await function.call()


async def get_eth_usd_aggregator(
    client: PublicClient,
    value_interpreter: ChecksumAddress,
) -> ChecksumAddress:
    contract = client.contract(value_interpreter, abis.IValueInterpreter)
    function = contract.functions.getEthUsdAggregator()
    return await function.call()
