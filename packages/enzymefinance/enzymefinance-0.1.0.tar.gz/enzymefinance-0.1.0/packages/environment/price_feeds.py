from enum import IntEnum
from web3.types import ChecksumAddress
from typing import Literal, TypedDict

PriceFeedType = Literal[
    "NONE",
    "WETH",
    "PRIMITIVE_CHAINLINK",
    "PRIMITIVE_CHAINLINK_LIKE_ETHX",
    "PRIMITIVE_CHAINLINK_LIKE_WSTETH",
    "PRIMITIVE_CHAINLINK_LIKE_YNETH",
    "PRIMITIVE_REDSTONE",
    "PRIMITIVE_REDSTONE_QUOTED",
    "PRIMITIVE_NON_STANDARD_PRECISION",
    "PRIMITIVE_PENDLE_V2",
    "DERIVATIVE_ARRAKIS_V2",
    "DERIVATIVE_BALANCER_V2_GAUGE_TOKEN",
    "DERIVATIVE_BALANCER_V2_STABLE_POOL",
    "DERIVATIVE_BALANCER_V2_WEIGHTED_POOL",
    "DERIVATIVE_COMPOUND",
    "DERIVATIVE_CURVE",
    "DERIVATIVE_ERC4626",
    "DERIVATIVE_ETHERFI",
    "DERIVATIVE_PEGGED_DERIVATIVES",
    "DERIVATIVE_REVERTING",
    "DERIVATIVE_STADER_SD",
    "DERIVATIVE_UNISWAP_V2_POOL",
    "DERIVATIVE_WSTETH",
    "DERIVATIVE_YEARN_VAULT_V2",
]


PRIMITIVE_PRICE_FEEDS = [
    "PRIMITIVE_CHAINLINK",
    "PRIMITIVE_CHAINLINK_LIKE_ETHX",
    "PRIMITIVE_CHAINLINK_LIKE_WSTETH",
    "PRIMITIVE_CHAINLINK_LIKE_YNETH",
    "PRIMITIVE_REDSTONE",
    "PRIMITIVE_REDSTONE_QUOTED",
    "PRIMITIVE_NON_STANDARD_PRECISION",
    "PRIMITIVE_PENDLE_V2",
]


DERIVATIVE_PRICE_FEEDS = [
    "DERIVATIVE_ARRAKIS_V2",
    "DERIVATIVE_BALANCER_V2_GAUGE_TOKEN",
    "DERIVATIVE_BALANCER_V2_STABLE_POOL",
    "DERIVATIVE_BALANCER_V2_WEIGHTED_POOL",
    "DERIVATIVE_COMPOUND",
    "DERIVATIVE_CURVE",
    "DERIVATIVE_ERC4626",
    "DERIVATIVE_ETHERFI",
    "DERIVATIVE_PEGGED_DERIVATIVES",
    "DERIVATIVE_STADER_SD",
    "DERIVATIVE_UNISWAP_V2_POOL",
    "DERIVATIVE_WSTETH",
    "DERIVATIVE_YEARN_VAULT_V2",
]


class RateAsset(IntEnum):
    ETH = 0
    USD = 1


class PriceFeedBase(TypedDict, total=False):
    non_standard: bool
    pegged_to: str
    comment: str


class NoPriceFeed(PriceFeedBase):
    type: Literal["NONE"]


class WethPriceFeed(PriceFeedBase):
    type: Literal["WETH"]


class PrimitiveChainlinkPriceFeed(PriceFeedBase):
    type: Literal["PRIMITIVE_CHAINLINK"]
    # Aggregator address
    aggregator: ChecksumAddress
    # Rate asset (ETH = 0, USD = 1)
    rate_asset: RateAsset


class PrimitiveChainlinkLikeWstEthPriceFeed(PriceFeedBase):
    type: Literal["PRIMITIVE_CHAINLINK_LIKE_WSTETH"]
    # Aggregator address
    aggregator: ChecksumAddress
    # Rate asset (ETH = 0, USD = 1)
    rate_asset: RateAsset


class PrimitiveChainlinkLikeYnEthPriceFeed(PriceFeedBase):
    type: Literal["PRIMITIVE_CHAINLINK_LIKE_YNETH"]
    # Aggregator address
    aggregator: ChecksumAddress
    # Rate asset (ETH = 0, USD = 1)
    rate_asset: RateAsset


class PrimitiveChainlinkLikeEthxPriceFeed(PriceFeedBase):
    type: Literal["PRIMITIVE_CHAINLINK_LIKE_ETHX"]
    # Aggregator address
    aggregator: ChecksumAddress
    # Rate asset (ETH = 0, USD = 1)
    rate_asset: RateAsset


class PrimitiveRedstonePriceFeed(PriceFeedBase):
    type: Literal["PRIMITIVE_REDSTONE"]
    # Aggregator address
    aggregator: ChecksumAddress
    # Rate asset (ETH = 0, USD = 1)
    rate_asset: RateAsset


class PrimitiveRedstoneQuotedPriceFeed(PriceFeedBase):
    type: Literal["PRIMITIVE_REDSTONE_QUOTED"]
    # Aggregator address
    aggregator: ChecksumAddress
    # Rate asset (ETH = 0, USD = 1)
    rate_asset: RateAsset


class PrimitiveNonStandardPrecisionPriceFeed(PriceFeedBase):
    type: Literal["PRIMITIVE_REDSTONE_NON_STANDARD_PRECISION"]
    # Aggregator address
    aggregator: ChecksumAddress
    # Rate asset (ETH = 0, USD = 1)
    rate_asset: RateAsset


class PrimitivePendleV2PriceFeed(PriceFeedBase):
    type: Literal["PRIMITIVE_PENDLE_V2"]
    # Aggregator address
    aggregator: ChecksumAddress
    # Rate asset (ETH = 0, USD = 1)
    rate_asset: RateAsset


class DerivativeArrakisV2PriceFeed(PriceFeedBase):
    type: Literal["DERIVATIVE_ARRAKIS_V2"]
    # Price feed address
    address: ChecksumAddress


class DerivativeBalancerV2GaugeTokenPriceFeed(PriceFeedBase):
    type: Literal["DERIVATIVE_BALANCER_V2_GAUGE_TOKEN"]
    # Price feed address
    address: ChecksumAddress


class DerivativeBalancerV2StablePoolPriceFeed(PriceFeedBase):
    type: Literal["DERIVATIVE_BALANCER_V2_STABLE_POOL"]
    # Price feed address
    address: ChecksumAddress
    # Invariant Proxy Asset (ipa)
    ipa: ChecksumAddress


class DerivativeBalancerV2WeightedPoolPriceFeed(PriceFeedBase):
    type: Literal["DERIVATIVE_BALANCER_V2_WEIGHTED_POOL"]
    # Price feed address
    address: ChecksumAddress


class DerivativeCompoundPriceFeed(PriceFeedBase):
    type: Literal["DERIVATIVE_COMPOUND"]
    # Price feed address
    address: ChecksumAddress


class DerivativeCurvePriceFeed(PriceFeedBase):
    type: Literal["DERIVATIVE_CURVE"]
    # Price feed address
    address: ChecksumAddress
    # Invariant Proxy Asset (ipa)
    ipa: ChecksumAddress


class DerivativeERC4626PriceFeed(PriceFeedBase):
    type: Literal["DERIVATIVE_ERC4626"]
    # Price feed address
    address: ChecksumAddress


class DerivativeEtherfiPriceFeed(PriceFeedBase):
    type: Literal["DERIVATIVE_ETHERFI"]
    # Price feed address
    address: ChecksumAddress


class DerivativePeggedDerivativesPriceFeed(PriceFeedBase):
    type: Literal["DERIVATIVE_PEGGED_DERIVATIVES"]
    # Price feed address
    address: ChecksumAddress


class DerivativeStaderSDPriceFeed(PriceFeedBase):
    type: Literal["DERIVATIVE_STADER_SD"]
    # Price feed address
    address: ChecksumAddress


class DerivativeUniswapV2PoolPriceFeed(PriceFeedBase):
    type: Literal["DERIVATIVE_UNISWAP_V2_POOL"]
    # Price feed address
    address: ChecksumAddress


class DerivativeWstethPriceFeed(PriceFeedBase):
    type: Literal["DERIVATIVE_WSTETH"]
    # Price feed address
    address: ChecksumAddress


class DerivativeYearnVaultV2PriceFeed(PriceFeedBase):
    type: Literal["DERIVATIVE_YEARN_VAULT_V2"]
    # Price feed address
    address: ChecksumAddress


PriceFeed = (
  NoPriceFeed
  | WethPriceFeed
  | PrimitiveChainlinkPriceFeed
  | PrimitiveChainlinkLikeEthxPriceFeed
  | PrimitiveChainlinkLikeWstEthPriceFeed
  | PrimitiveChainlinkLikeYnEthPriceFeed
  | PrimitiveRedstonePriceFeed
  | PrimitiveRedstoneQuotedPriceFeed
  | PrimitiveNonStandardPrecisionPriceFeed
  | PrimitivePendleV2PriceFeed
  | DerivativeArrakisV2PriceFeed
  | DerivativeBalancerV2GaugeTokenPriceFeed
  | DerivativeBalancerV2StablePoolPriceFeed
  | DerivativeBalancerV2WeightedPoolPriceFeed
  | DerivativeCompoundPriceFeed
  | DerivativeCurvePriceFeed
  | DerivativeERC4626PriceFeed
  | DerivativeEtherfiPriceFeed
  | DerivativePeggedDerivativesPriceFeed
  | DerivativeStaderSDPriceFeed
  | DerivativeUniswapV2PoolPriceFeed
  | DerivativeWstethPriceFeed
  | DerivativeYearnVaultV2PriceFeed
)
