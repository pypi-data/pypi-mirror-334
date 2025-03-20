from web3 import Web3
from web3.types import ChecksumAddress, HexStr, TxParams
from eth_abi import encode
from ...utils.clients import PublicClient, WalletClient
from ...utils.encoding import encoding_to_types
from ....abis import abis

# --------------------------------------------------------------------------------------------
# FACTORY
# --------------------------------------------------------------------------------------------


async def deploy_proxy(
    client: WalletClient,
    share_price_throttled_asset_manager_factory: ChecksumAddress,
    owner: ChecksumAddress,
    vault_proxy_address: ChecksumAddress,
    loss_tolerance: int,
    loss_tolerance_period_duration: int,
    shutdowner: ChecksumAddress,
) -> TxParams:
    contract = client.contract(
        share_price_throttled_asset_manager_factory,
        abis.ISharePriceThrottledAssetManagerFactory,
    )
    function = contract.functions.deployProxy(
        owner,
        vault_proxy_address,
        loss_tolerance,
        loss_tolerance_period_duration,
        shutdowner,
    )
    return await client.populated_transaction(function)


# --------------------------------------------------------------------------------------------
# LIB
# --------------------------------------------------------------------------------------------


EXECUTE_CALLS_ENCODING = [
    {
        "type": "tuple[]",
        "name": "calls",
        "components": [
            {
                "name": "target",
                "type": "address",
            },
            {
                "name": "data",
                "type": "bytes",
            },
        ],
    },
]


async def execute_calls(
    client: WalletClient,
    share_price_throttled_asset_manager: ChecksumAddress,
    calls: list[ChecksumAddress, HexStr],
) -> TxParams:
    """
    Args:
        client: WalletClient
        share_price_throttled_asset_manager: ChecksumAddress
        calls: list[ChecksumAddress, HexStr]
            [
                [
                    ChecksumAddress,  # target
                    HexStr,           # data
                ],
                ...
            ]
    """
    contract = client.contract(
        share_price_throttled_asset_manager,
        abis.ISharePriceThrottledAssetManagerLib,
    )
    types = encoding_to_types(EXECUTE_CALLS_ENCODING)
    args = [[[target, Web3.to_bytes(hexstr=data)] for target, data in calls]]
    encoded_calls = Web3.to_hex(encode(types, args))
    function = contract.functions.executeCalls(encoded_calls)
    return await client.populated_transaction(function)


async def shutdown(
    client: WalletClient,
    share_price_throttled_asset_manager: ChecksumAddress,
) -> TxParams:
    contract = client.contract(
        share_price_throttled_asset_manager,
        abis.ISharePriceThrottledAssetManagerLib,
    )
    function = contract.functions.shutdown()
    return await client.populated_transaction(function)


async def get_loss_tolerance(
    client: PublicClient,
    share_price_throttled_asset_manager: ChecksumAddress,
) -> int:
    contract = client.contract(
        share_price_throttled_asset_manager,
        abis.ISharePriceThrottledAssetManagerLib,
    )
    function = contract.functions.getLossTolerance()
    return await function.call()


async def get_loss_tolerance_period_duration(
    client: PublicClient,
    share_price_throttled_asset_manager: ChecksumAddress,
) -> int:
    contract = client.contract(
        share_price_throttled_asset_manager,
        abis.ISharePriceThrottledAssetManagerLib,
    )
    function = contract.functions.getLossTolerancePeriodDuration()
    return await function.call()


async def get_shutdowner(
    client: PublicClient,
    share_price_throttled_asset_manager: ChecksumAddress,
) -> ChecksumAddress:
    contract = client.contract(
        share_price_throttled_asset_manager,
        abis.ISharePriceThrottledAssetManagerLib,
    )
    function = contract.functions.getShutdowner()
    return await function.call()


async def get_throttle(
    client: PublicClient,
    share_price_throttled_asset_manager: ChecksumAddress,
) -> int:
    contract = client.contract(
        share_price_throttled_asset_manager,
        abis.ISharePriceThrottledAssetManagerLib,
    )
    function = contract.functions.getThrottle()
    return await function.call()


async def get_vault_proxy_address(
    client: PublicClient,
    share_price_throttled_asset_manager: ChecksumAddress,
) -> ChecksumAddress:
    contract = client.contract(
        share_price_throttled_asset_manager,
        abis.ISharePriceThrottledAssetManagerLib,
    )
    function = contract.functions.getVaultProxyAddress()
    return await function.call()
