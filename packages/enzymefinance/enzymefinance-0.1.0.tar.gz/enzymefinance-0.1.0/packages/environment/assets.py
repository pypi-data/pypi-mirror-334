from typing import Literal, TypedDict
from web3.types import ChecksumAddress, HexStr
from .price_feeds import PriceFeed
from .types import Network, Release


AssetType = Literal[
    "aave-v2"
    "aave-v3"
    "balancer-pool"
    "balancer-pool-gauge"
    "compound-v2"
    "compound-v3"
    "curve-pool-lp"
    "curve-pool-gauge"
    "idle"
    "pendle-v2-lp"
    "pendle-v2-pt"
    "primitive"
    "stader"
    "synthetix"
    "uniswap-v2-pool"
    "yearn-vault-v2"
    "maple-v1"
    "maple-v2"
    "erc-4626"
    "zero-lend-lrt-btc-aave-v3"
    "zero-lend-rwa-stablecoins-aave-v3"
]


class AssetDefinitionInput(TypedDict):
    # The asset address
    id: ChecksumAddress
    # The asset name
    name: str
    # The asset symbol
    symbol: str
    # Number of decimal places
    decimals: int
    # The asset type
    type: AssetType
    # List of release slugs the asset is registered on
    releases: list[Release]
    # Price feed used for the asset
    price_feed: PriceFeed


class AssetBase(AssetDefinitionInput):
    # The network the asset is deployed on
    network: Network
    # Whether the asset is registered on the current release
    registered: bool


class StaderAsset(AssetBase):
    type: Literal["stader"]


class SynthetixAsset(AssetBase):
    type: Literal["synthetix"]


class PrimitiveAsset(AssetBase):
    type: Literal["primitive"]


class AaveV2Asset(AssetBase):
    type: Literal["aave-v2"]
    # Underlying Asset
    underlying: ChecksumAddress


class AaveV3Asset(AssetBase):
    type: Literal["aave-v3"]
    # Underlying Asset
    underlying: ChecksumAddress


class ZeroLendLRTBTCAaveV3Asset(AssetBase):
    type: Literal["zero-lend-lrt-btc-aave-v3"]
    # Underlying Asset
    underlying: ChecksumAddress


class ZeroLendRWAStablecoinsAaveV3Asset(AssetBase):
    type: Literal["zero-lend-rwa-stablecoins-aave-v3"]
    # Underlying Asset
    underlying: ChecksumAddress


class CompoundV2Asset(AssetBase):
    type: Literal["compound-v2"]
    # Underlying Asset
    underlying: ChecksumAddress


class CompoundV3Asset(AssetBase):
    type: Literal["compound-v3"]
    # Underlying Asset
    underlying: ChecksumAddress


class IdleAsset(AssetBase):
    type: Literal["idle"]
    # Underlying Asset
    underlying: ChecksumAddress


class YearnVaultV2Asset(AssetBase):
    type: Literal["yearn-vault-v2"]
    # Underlying Asset
    underlying: ChecksumAddress


class UniswapV2PoolAsset(AssetBase):
    type: Literal["uniswap-v2-pool"]
    # Underlying Asset Pair
    underlyings: list[ChecksumAddress]


class MapleV1Asset(AssetBase):
    type: Literal["maple-v1"]
    # Underlying Asset
    underlying: ChecksumAddress
    rewards_contract: ChecksumAddress


class MapleV2Asset(AssetBase):
    type: Literal["maple-v2"]
    # Underlying Asset
    underlying: ChecksumAddress
    pool_manager: ChecksumAddress


Erc4626Protocol = Literal["angle", "morpho", "sky", "spark", "vaultcraft"]


class ERC4626Asset(AssetBase):
    type: Literal["erc-4626"]
    # The protocol of the ERC4626 asset (since there are multiple protocols that implement ERC4626 assets)
    protocol: Erc4626Protocol
    # Underlying Asset
    underlying: ChecksumAddress


BalancerStakingType = Literal["none", "gauge"]


class BalancerStaking(TypedDict):
    token: ChecksumAddress
    type: BalancerStakingType


BalancerPoolType = Literal["meta-stable", "stable", "weighted", "composable-stable-v5"]


class BalancerPoolAsset(AssetBase):
    type: Literal["balancer-pool"]
    # Balancer pool factory
    pool_factory: ChecksumAddress
    # Staking options
    staking: list[BalancerStaking]
    # Balancer pool type
    pool_type: BalancerPoolType
    # Underlying Assets
    underlyings: list[ChecksumAddress]
    # Pool id
    pool_id: HexStr


class BalancerPoolGaugeAsset(AssetBase):
    type: Literal["balancer-pool-gauge"]
    # Balancer Pool
    pool: ChecksumAddress
    # Balancer gauge factory
    gauge_factory: ChecksumAddress
    # Balancer pool template
    pool_type: BalancerPoolType
    # Underlying Assets
    underlyings: list[ChecksumAddress]


CurvePoolTemplate = Literal["aave", "base", "eth", "meta", "yearn"]


CurveStakingType = Literal["none", "gauge"]


class CurveStaking(TypedDict):
    token: ChecksumAddress
    type: CurveStakingType


class CurvePoolLpAsset(AssetBase):
    type: Literal["curve-pool-lp"]
    # Curve Pool
    pool: ChecksumAddress
    # Staking options
    staking: list[CurveStaking]
    # Curve pool template. See: https://github.com/curvefi/curve-contract/tree/master/contracts/pool-templates
    template: CurvePoolTemplate
    # Underlying Assets
    underlyings: list[ChecksumAddress]


class CurvePoolGaugeAsset(AssetBase):
    type: Literal["curve-pool-gauge"]
    # Curve LP Token
    lp: ChecksumAddress
    # Curve Pool
    pool: ChecksumAddress
    # Curve pool template. See: https://github.com/curvefi/curve-contract/tree/master/contracts/pool-templates
    template: CurvePoolTemplate
    # Underlying Assets
    underlyings: list[ChecksumAddress]


class PendleV2LPAsset(AssetBase):
    type: Literal["pendle-v2-lp"]
    # Underlying Asset
    underlying: ChecksumAddress


class PendleV2PTAsset(AssetBase):
    type: Literal["pendle-v2-pt"]
    # Underlying Asset
    underlying: ChecksumAddress
    # Markets
    markets: list[ChecksumAddress]


Asset = (
    AaveV2Asset
    | AaveV3Asset
    | BalancerPoolAsset
    | BalancerPoolGaugeAsset
    | CompoundV2Asset
    | CompoundV3Asset
    | CurvePoolGaugeAsset
    | CurvePoolLpAsset
    | ERC4626Asset
    | IdleAsset
    | MapleV1Asset
    | MapleV2Asset
    | PendleV2PTAsset
    | PendleV2LPAsset
    | PrimitiveAsset
    | StaderAsset
    | SynthetixAsset
    | UniswapV2PoolAsset
    | YearnVaultV2Asset
    | ZeroLendLRTBTCAaveV3Asset
    | ZeroLendRWAStablecoinsAaveV3Asset
)


def define_asset_list(
    network: Network, assets: list[AssetDefinitionInput]
) -> list[AssetBase]:
    return [asset | {"network": network, "registered": False} for asset in assets]
