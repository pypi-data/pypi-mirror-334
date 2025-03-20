from typing import TypedDict, Any, Literal, get_args
from web3 import Web3
from web3.types import ChecksumAddress
from web3.constants import ADDRESS_ZERO
from .contracts import Contracts, VersionContractNames


AdapterType = Literal[
    "aave_v2",
    "aave_v3",
    "alpha_homora_v1",
    "aura",
    "balancer_v2",
    "compound_v2",
    "compound_v3",
    "convex",
    "curve_exchange",
    "curve_liquidity",
    "curve_liquidity_aave",
    "curve_liquidity_eurs",
    "curve_liquidity_seth",
    "curve_liquidity_steth",
    "erc_4626",
    "idle",
    "kyber_network",
    "olympus_v2",
    "one_inch_v5",
    "paraswap_v4",
    "paraswap_v5",
    "pendle_v2",
    "pooltogether_v4",
    "swell_staking",
    "synthetix",
    "three_one_third",
    "tracked_assets",
    "uniswap_v2",
    "uniswap_v2_liquidity",
    "uniswap_v3",
    "unknown",
    "yearn_vault_v2",
    "zeroex_v2",
    "zeroex_v4",
    "zeroex_v4_pmm_kyc",
    "zero_lend_lrt_btc_aave_v3",
    "zero_lend_rwa_stablecoins_aave_v3",
]

KnownAdapterType = Literal[
    "aave_v2",
    "aave_v3",
    "alpha_homora_v1",
    "aura",
    "balancer_v2",
    "compound_v2",
    "compound_v3",
    "convex",
    "curve_exchange",
    "curve_liquidity",
    "curve_liquidity_aave",
    "curve_liquidity_eurs",
    "curve_liquidity_seth",
    "curve_liquidity_steth",
    "erc_4626",
    "idle",
    "kyber_network",
    "olympus_v2",
    "one_inch_v5",
    "paraswap_v4",
    "paraswap_v5",
    "pendle_v2",
    "pooltogether_v4",
    "swell_staking",
    "synthetix",
    "three_one_third",
    "tracked_assets",
    "uniswap_v2",
    "uniswap_v2_liquidity",
    "uniswap_v3",
    "yearn_vault_v2",
    "zeroex_v2",
    "zeroex_v4",
    "zeroex_v4_pmm_kyc",
]

UnknownAdapterType = Literal["unknown"]


class UnresolvedAdapterDefinition(TypedDict):
    contract_name: VersionContractNames | None
    name: str
    type: AdapterType


class AdapterDefinition(TypedDict):
    address: ChecksumAddress
    name: str
    type: AdapterType


def is_adapter_definition(adapter: dict[str, Any]) -> bool:
    return (
        isinstance(adapter, dict)
        and "address" in adapter
        and "name" in adapter
        and "type" in adapter
        and Web3.is_checksum_address(adapter["address"])
        and isinstance(adapter["name"], str)
        and isinstance(adapter["type"], str)
        and adapter["type"] in get_args(AdapterType)
    )


def _is_in_contracts(
    contract_name: Any,
    contracts: Contracts,
) -> bool:
    return contract_name in contracts


def get_adapters_for_release(
    contracts: Contracts,
) -> dict[ChecksumAddress, AdapterDefinition]:
    result = {}

    for adapter_def in ADAPTER_DEFINITIONS.values():
        contract_name = adapter_def.get("contract_name")
        if contract_name is not None and _is_in_contracts(contract_name, contracts):
            address = contracts[contract_name]
            if address != ADDRESS_ZERO:
                result[address] = {
                    "address": address,
                    "name": adapter_def["name"],
                    "type": adapter_def["type"],
                }

    return result


KNOWN_ADAPTER_DEFINITIONS: dict[KnownAdapterType, UnresolvedAdapterDefinition] = {
    "aave_v2": {
        "contract_name": "AaveV2Adapter",
        "name": "Aave V2 Supply",
        "type": "aave_v2",  # AdapterType
    },
    "aave_v3": {
        "contract_name": "AaveV3Adapter",
        "name": "Aave V3 Supply",
        "type": "aave_v3",  # AdapterType
    },
    "alpha_homora_v1": {
        "contract_name": None,
        "name": "Alpha Homora V1",
        "type": "alpha_homora_v1",  # AdapterType
    },
    "aura": {
        "contract_name": None,
        "name": "Aura Stake",
        "type": "aura",  # AdapterType
    },
    "balancer_v2": {
        "contract_name": "BalancerV2LiquidityAdapter",
        "name": "Balancer V2",
        "type": "balancer_v2",  # AdapterType
    },
    "compound_v2": {
        "contract_name": "CompoundAdapter",
        "name": "Compound Lend",
        "type": "compound_v2",  # AdapterType
    },
    "compound_v3": {
        "contract_name": "CompoundV3Adapter",
        "name": "Compound V3 Lend",
        "type": "compound_v3",  # AdapterType
    },
    "convex": {
        "contract_name": None,
        "name": "Convex Stake",
        "type": "convex",  # AdapterType
    },
    "curve_exchange": {
        "contract_name": "CurveExchangeAdapter",
        "name": "Curve Swap",
        "type": "curve_exchange",  # AdapterType
    },
    "curve_liquidity": {
        "contract_name": "CurveLiquidityAdapter",
        "name": "Curve Provide Liquidity",
        "type": "curve_liquidity",  # AdapterType
    },
    "curve_liquidity_aave": {
        "contract_name": None,
        "name": "Curve Aave Pool",
        "type": "curve_liquidity_aave",  # AdapterType
    },
    "curve_liquidity_eurs": {
        "contract_name": None,
        "name": "Curve Eurs Pool",
        "type": "curve_liquidity_eurs",  # AdapterType
    },
    "curve_liquidity_seth": {
        "contract_name": None,
        "name": "Curve Seth Pool",
        "type": "curve_liquidity_seth",  # AdapterType
    },
    "curve_liquidity_steth": {
        "contract_name": None,
        "name": "Curve Steth Pool",
        "type": "curve_liquidity_steth",  # AdapterType
    },
    "erc_4626": {
        "contract_name": "ERC4626Adapter",
        "name": "ERC4626",
        "type": "erc_4626",  # AdapterType
    },
    "idle": {
        "contract_name": None,
        "name": "Idle",
        "type": "idle",  # AdapterType
    },
    "kyber_network": {
        "contract_name": None,
        "name": "Kyber Network",
        "type": "kyber_network",  # AdapterType
    },
    "olympus_v2": {
        "contract_name": None,
        "name": "Olympus DAO",
        "type": "olympus_v2",  # AdapterType
    },
    "one_inch_v5": {
        "contract_name": "OneInchV5Adapter",
        "name": "1inch V5",
        "type": "one_inch_v5",  # AdapterType
    },
    "paraswap_v4": {
        "contract_name": None,
        "name": "ParaSwap V4",
        "type": "paraswap_v4",  # AdapterType
    },
    "paraswap_v5": {
        "contract_name": "ParaSwapV5Adapter",
        "name": "ParaSwap V5",
        "type": "paraswap_v5",  # AdapterType
    },
    "pendle_v2": {
        "contract_name": "PendleV2Adapter",
        "name": "Pendle V2",
        "type": "pendle_v2",  # AdapterType
    },
    "pooltogether_v4": {
        "contract_name": "PoolTogetherV4Adapter",
        "name": "PoolTogether",
        "type": "pooltogether_v4",  # AdapterType
    },
    "swell_staking": {
        "contract_name": "SwellStakingAdapter",
        "name": "Swell Staking",
        "type": "swell_staking",  # AdapterType
    },
    "synthetix": {
        "contract_name": "SynthetixAdapter",
        "name": "Synthetix",
        "type": "synthetix",  # AdapterType
    },
    "three_one_third": {
        "contract_name": "ThreeOneThirdAdapter",
        "name": "31Third",
        "type": "three_one_third",  # AdapterType
    },
    "tracked_assets": {
        "contract_name": None,
        "name": "Tracked Asset",
        "type": "tracked_assets",  # AdapterType
    },
    "uniswap_v2": {
        "contract_name": "UniswapV2ExchangeAdapter",
        "name": "Uniswap V2 Swap",
        "type": "uniswap_v2",  # AdapterType
    },
    "uniswap_v2_liquidity": {
        "contract_name": "UniswapV2LiquidityAdapter",
        "name": "Uniswap V2 Provide Liquidity",
        "type": "uniswap_v2_liquidity",  # AdapterType
    },
    "uniswap_v3": {
        "contract_name": "UniswapV3Adapter",
        "name": "Uniswap V3 Swap",
        "type": "uniswap_v3",  # AdapterType
    },
    "yearn_vault_v2": {
        "contract_name": "YearnVaultV2Adapter",
        "name": "Yearn",
        "type": "yearn_vault_v2",  # AdapterType
    },
    "zeroex_v2": {
        "contract_name": "ZeroExV2Adapter",
        "name": "0x V2",
        "type": "zeroex_v2",  # AdapterType
    },
    "zeroex_v4": {
        "contract_name": "ZeroExV4Adapter",
        "name": "0x V4",
        "type": "zeroex_v4",  # AdapterType
    },
    "zeroex_v4_pmm_kyc": {
        "contract_name": "ZeroExV4AdapterPmm2Kyc",
        "name": "0x V4",
        "type": "zeroex_v4_pmm_kyc",  # AdapterType
    },
    "zero_lend_lrt_btc_aave_v3": {
        "contract_name": "ZeroLendLRTBTCAaveV3Adapter",
        "name": "Zero Lend LRT BTC Supply",
        "type": "zero_lend_lrt_btc_aave_v3",  # AdapterType
    },
    "zero_lend_rwa_stablecoins_aave_v3": {
        "contract_name": "ZeroLendRWAStablecoinsAaveV3Adapter",
        "name": "Zero Lend RWA Stablecoins Supply",
        "type": "zero_lend_rwa_stablecoins_aave_v3",  # AdapterType
    },
}

UNKNOWN_ADAPTER_DEFINITIONS: dict[UnknownAdapterType, UnresolvedAdapterDefinition] = {
    "unknown": {
        "contract_name": None,
        "name": "Unknown",
        "type": "unknown",  # AdapterType
    },
}

ADAPTER_DEFINITIONS: dict[AdapterType, UnresolvedAdapterDefinition] = {
    **KNOWN_ADAPTER_DEFINITIONS,
    **UNKNOWN_ADAPTER_DEFINITIONS,
}
