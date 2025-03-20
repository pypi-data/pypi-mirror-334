from typing import TypedDict, Any, Literal, get_args
from web3.types import ChecksumAddress


Version = Literal["phoenix", "encore", "sulu"]


def is_version(version: Any) -> bool:
    return isinstance(version, str) and version in get_args(Version)


class CommonContracts(TypedDict):
    ComptrollerLib: ChecksumAddress
    Dispatcher: ChecksumAddress
    FeeManager: ChecksumAddress
    FundDataProviderRouter: ChecksumAddress
    FundDeployer: ChecksumAddress
    FundValueCalculatorRouter: ChecksumAddress
    IntegrationManager: ChecksumAddress
    PolicyManager: ChecksumAddress
    VaultLib: ChecksumAddress


class SuluContracts(CommonContracts):
    AaveDebtPositionLib: ChecksumAddress
    AaveDebtPositionParser: ChecksumAddress
    AaveV3DebtPositionLib: ChecksumAddress
    AaveV3DebtPositionParser: ChecksumAddress
    AaveV3FlashLoanAssetManagerFactory: ChecksumAddress
    AaveV3FlashLoanAssetManagerLib: ChecksumAddress
    AavePriceFeed: ChecksumAddress
    AaveV2Adapter: ChecksumAddress
    AaveV2ATokenListOwner: ChecksumAddress
    AaveV3Adapter: ChecksumAddress
    AaveV3ATokenListOwner: ChecksumAddress
    AddressListRegistry: ChecksumAddress
    AlicePositionLib: ChecksumAddress
    AlicePositionParser: ChecksumAddress
    AllowedAdapterIncomingAssetsPolicy: ChecksumAddress
    AllowedAdaptersPerManagerPolicy: ChecksumAddress
    AllowedAdaptersPolicy: ChecksumAddress
    AllowedAssetsForRedemptionPolicy: ChecksumAddress
    AllowedDepositRecipientsPolicy: ChecksumAddress
    AllowedExternalPositionTypesPerManagerPolicy: ChecksumAddress
    AllowedExternalPositionTypesPolicy: ChecksumAddress
    AllowedRedeemersForSpecificAssetsPolicy: ChecksumAddress
    AllowedSharesTransferRecipientsPolicy: ChecksumAddress
    ArbitraryLoanPositionLib: ChecksumAddress
    ArbitraryLoanPositionParser: ChecksumAddress
    ArbitraryLoanTotalNominalDeltaOracleModule: ChecksumAddress
    ArrakisV2Adapter: ChecksumAddress
    ArrakisV2PriceFeed: ChecksumAddress
    AssetValueCalculator: ChecksumAddress
    BalancerV2GaugeTokenPriceFeed: ChecksumAddress
    BalancerV2LiquidityAdapter: ChecksumAddress
    BalancerV2StablePoolPriceFeed: ChecksumAddress
    BalancerV2WeightedPoolPriceFeed: ChecksumAddress
    ChainlinkLikeWstethPriceFeed: ChecksumAddress
    ChainlinkLikeYnEthPriceFeed: ChecksumAddress
    CompoundAdapter: ChecksumAddress
    CompoundDebtPositionLib: ChecksumAddress
    CompoundDebtPositionParser: ChecksumAddress
    CompoundPriceFeed: ChecksumAddress
    CompoundV3TokenListOwner: ChecksumAddress
    CompoundV3Adapter: ChecksumAddress
    ConvertedQuoteAggregatorFactory: ChecksumAddress
    ConvexVotingPositionLib: ChecksumAddress
    ConvexVotingPositionParser: ChecksumAddress
    CumulativeSlippageTolerancePolicy: ChecksumAddress
    CurveExchangeAdapter: ChecksumAddress
    CurveLiquidityAaveAdapter: ChecksumAddress
    CurveLiquidityAdapter: ChecksumAddress
    CurveLiquiditySethAdapter: ChecksumAddress
    CurveLiquidityStethAdapter: ChecksumAddress
    CurvePriceFeed: ChecksumAddress
    DepositWrapper: ChecksumAddress
    DisallowedAdapterIncomingAssetsPolicy: ChecksumAddress
    EntranceRateBurnFee: ChecksumAddress
    EntranceRateDirectFee: ChecksumAddress
    ERC4626Adapter: ChecksumAddress
    ERC4626PriceFeed: ChecksumAddress
    EtherFiEthPriceFeed: ChecksumAddress
    ExitRateBurnFee: ChecksumAddress
    ExitRateDirectFee: ChecksumAddress
    ExternalPositionFactory: ChecksumAddress
    ExternalPositionManager: ChecksumAddress
    FiduPriceFeed: ChecksumAddress
    FundValueCalculator: ChecksumAddress
    GasRelayPaymasterFactory: ChecksumAddress
    GasRelayPaymasterLib: ChecksumAddress
    GatedRedemptionQueueSharesWrapperFactory: ChecksumAddress
    GatedRedemptionQueueSharesWrapperLib: ChecksumAddress
    GenericAdapter: ChecksumAddress
    GlobalConfigLib: ChecksumAddress
    GlobalConfigProxy: ChecksumAddress
    GMXV2LeverageTradingPositionLib: ChecksumAddress
    GMXV2LeverageTradingPositionParser: ChecksumAddress
    KilnStakingPositionLib: ChecksumAddress
    KilnStakingPositionParser: ChecksumAddress
    LidoWithdrawalsPositionLib: ChecksumAddress
    LidoWithdrawalsPositionParser: ChecksumAddress
    LiquityDebtPositionLib: ChecksumAddress
    LiquityDebtPositionParser: ChecksumAddress
    ManagementFee: ChecksumAddress
    ManualValueOracleFactory: ChecksumAddress
    MapleLiquidityPositionLib: ChecksumAddress
    MapleLiquidityPositionParser: ChecksumAddress
    MinAssetBalancesPostRedemptionPolicy: ChecksumAddress
    MinMaxInvestmentPolicy: ChecksumAddress
    MinSharesSupplyFee: ChecksumAddress
    MorphoBluePositionLib: ChecksumAddress
    MorphoBluePositionParser: ChecksumAddress
    NoDepegOnRedeemSharesForSpecificAssetsPolicy: ChecksumAddress
    NotionalV2PositionLib: ChecksumAddress
    NotionalV2PositionParser: ChecksumAddress
    OneInchV5Adapter: ChecksumAddress
    OnlyRemoveDustExternalPositionPolicy: ChecksumAddress
    OnlyUntrackDustOrPricelessAssetsPolicy: ChecksumAddress
    ParaSwapV5Adapter: ChecksumAddress
    PeggedDerivativesPriceFeed: ChecksumAddress
    PendleV2Adapter: ChecksumAddress
    PendleV2PositionLib: ChecksumAddress
    PendleV2PositionParser: ChecksumAddress
    PendleMarketsRegistry: ChecksumAddress
    PerformanceFee: ChecksumAddress
    PoolTogetherV4Adapter: ChecksumAddress
    PoolTogetherV4PriceFeed: ChecksumAddress
    ProtocolFeeReserveLib: ChecksumAddress
    ProtocolFeeReserveProxy: ChecksumAddress
    ProtocolFeeTracker: ChecksumAddress
    SharePriceThrottledAssetManagerLib: ChecksumAddress
    SharePriceThrottledAssetManagerFactory: ChecksumAddress
    SharesSplitterFactory: ChecksumAddress
    SingleAssetRedemptionQueueLib: ChecksumAddress
    SingleAssetRedemptionQueueFactory: ChecksumAddress
    SolvV2BondBuyerPositionLib: ChecksumAddress
    SolvV2BondBuyerPositionParser: ChecksumAddress
    SolvV2BondIssuerPositionLib: ChecksumAddress
    SolvV2BondIssuerPositionParser: ChecksumAddress
    StaderSDPriceFeed: ChecksumAddress
    StaderStakingAdapter: ChecksumAddress
    StaderWithdrawalsPositionLib: ChecksumAddress
    StaderWithdrawalsPositionParser: ChecksumAddress
    StakeWiseV3StakingPositionLib: ChecksumAddress
    StakeWiseV3StakingPositionParser: ChecksumAddress
    SwellStakingAdapter: ChecksumAddress
    SynthetixAdapter: ChecksumAddress
    TermFinanceV1LendingPositionLib: ChecksumAddress
    TermFinanceV1LendingPositionParser: ChecksumAddress
    TheGraphDelegationPositionLib: ChecksumAddress
    TheGraphDelegationPositionParser: ChecksumAddress
    ThreeOneThirdAdapter: ChecksumAddress
    TransferAssetsAdapter: ChecksumAddress
    UintListRegistry: ChecksumAddress
    UniswapV2ExchangeAdapter: ChecksumAddress
    UniswapV2LiquidityAdapter: ChecksumAddress
    UniswapV2PoolPriceFeed: ChecksumAddress
    UniswapV3Adapter: ChecksumAddress
    UniswapV3LiquidityPositionLib: ChecksumAddress
    UniswapV3LiquidityPositionParser: ChecksumAddress
    UnpermissionedActionsWrapper: ChecksumAddress
    UsdEthSimulatedAggregator: ChecksumAddress
    ValueInterpreter: ChecksumAddress
    WstethPriceFeed: ChecksumAddress
    YearnVaultV2Adapter: ChecksumAddress
    YearnVaultV2PriceFeed: ChecksumAddress
    ZeroExV2Adapter: ChecksumAddress
    ZeroExV4Adapter: ChecksumAddress
    ZeroExV4AdapterPmm2Kyc: ChecksumAddress
    ZeroLendLRTBTCAaveV3Adapter: ChecksumAddress
    ZeroLendLRTBTCAaveV3ATokenListOwner: ChecksumAddress
    ZeroLendLRTBTCAaveV3DebtPositionLib: ChecksumAddress
    ZeroLendLRTBTCAaveV3DebtPositionParser: ChecksumAddress
    ZeroLendRWAStablecoinsAaveV3Adapter: ChecksumAddress
    ZeroLendRWAStablecoinsAaveV3ATokenListOwner: ChecksumAddress
    ZeroLendRWAStablecoinsAaveV3DebtPositionLib: ChecksumAddress
    ZeroLendRWAStablecoinsAaveV3DebtPositionParser: ChecksumAddress


class EncoreContracts(CommonContracts):
    AaveAdapter: ChecksumAddress
    AavePriceFeed: ChecksumAddress
    AdapterBlacklist: ChecksumAddress
    AdapterWhitelist: ChecksumAddress
    AggregatedDerivativePriceFeed: ChecksumAddress
    AlphaHomoraV1Adapter: ChecksumAddress
    AlphaHomoraV1PriceFeed: ChecksumAddress
    AssetBlacklist: ChecksumAddress
    AssetValueCalculator: ChecksumAddress
    AssetWhitelist: ChecksumAddress
    BuySharesCallerWhitelist: ChecksumAddress
    ChainlinkPriceFeed: ChecksumAddress
    CompoundAdapter: ChecksumAddress
    CompoundPriceFeed: ChecksumAddress
    CurveExchangeAdapter: ChecksumAddress
    CurveLiquidityAaveAdapter: ChecksumAddress
    CurveLiquidityEursAdapter: ChecksumAddress
    CurveLiquiditySethAdapter: ChecksumAddress
    CurveLiquidityStethAdapter: ChecksumAddress
    CurvePriceFeed: ChecksumAddress
    EntranceRateBurnFee: ChecksumAddress
    EntranceRateDirectFee: ChecksumAddress
    FundActionsWrapper: ChecksumAddress
    FundValueCalculator: ChecksumAddress
    GuaranteedRedemption: ChecksumAddress
    IdleAdapter: ChecksumAddress
    IdlePriceFeed: ChecksumAddress
    InvestorWhitelist: ChecksumAddress
    KyberAdapter: ChecksumAddress
    LidoStethPriceFeed: ChecksumAddress
    ManagementFee: ChecksumAddress
    MaxConcentration: ChecksumAddress
    MinMaxInvestment: ChecksumAddress
    ParaSwapV4Adapter: ChecksumAddress
    PerformanceFee: ChecksumAddress
    StakehoundEthPriceFeed: ChecksumAddress
    SynthetixAdapter: ChecksumAddress
    SynthetixPriceFeed: ChecksumAddress
    TrackedAssetsAdapter: ChecksumAddress
    UniswapV2Adapter: ChecksumAddress
    UniswapV2PoolPriceFeed: ChecksumAddress
    ValueInterpreter: ChecksumAddress
    WdgldPriceFeed: ChecksumAddress
    YearnVaultV2Adapter: ChecksumAddress
    YearnVaultV2PriceFeed: ChecksumAddress
    ZeroExV2Adapter: ChecksumAddress


class PhoenixContracts(CommonContracts):
    AaveAdapter: ChecksumAddress
    AavePriceFeed: ChecksumAddress
    AdapterBlacklist: ChecksumAddress
    AdapterWhitelist: ChecksumAddress
    AggregatedDerivativePriceFeed: ChecksumAddress
    AlphaHomoraV1Adapter: ChecksumAddress
    AlphaHomoraV1PriceFeed: ChecksumAddress
    AssetBlacklist: ChecksumAddress
    AssetValueCalculator: ChecksumAddress
    AssetWhitelist: ChecksumAddress
    BuySharesCallerWhitelist: ChecksumAddress
    ChaiAdapter: ChecksumAddress
    ChainlinkPriceFeed: ChecksumAddress
    ChaiPriceFeed: ChecksumAddress
    CompoundAdapter: ChecksumAddress
    CompoundPriceFeed: ChecksumAddress
    CurveExchangeAdapter: ChecksumAddress
    CurveLiquidityAaveAdapter: ChecksumAddress
    CurveLiquiditySethAdapter: ChecksumAddress
    CurveLiquidityStethAdapter: ChecksumAddress
    CurvePriceFeed: ChecksumAddress
    EntranceRateBurnFee: ChecksumAddress
    EntranceRateDirectFee: ChecksumAddress
    FundActionsWrapper: ChecksumAddress
    FundValueCalculator: ChecksumAddress
    GuaranteedRedemption: ChecksumAddress
    IdleAdapter: ChecksumAddress
    IdlePriceFeed: ChecksumAddress
    InvestorWhitelist: ChecksumAddress
    KyberAdapter: ChecksumAddress
    LidoStethPriceFeed: ChecksumAddress
    ManagementFee: ChecksumAddress
    MaxConcentration: ChecksumAddress
    MinMaxInvestment: ChecksumAddress
    ParaSwapV4Adapter: ChecksumAddress
    PerformanceFee: ChecksumAddress
    StakehoundEthPriceFeed: ChecksumAddress
    SynthetixAdapter: ChecksumAddress
    SynthetixPriceFeed: ChecksumAddress
    TrackedAssetsAdapter: ChecksumAddress
    UniswapV2Adapter: ChecksumAddress
    UniswapV2PoolPriceFeed: ChecksumAddress
    ValueInterpreter: ChecksumAddress
    WdgldPriceFeed: ChecksumAddress
    ZeroExV2Adapter: ChecksumAddress


Contracts = EncoreContracts | PhoenixContracts | SuluContracts


SuluContractNames = Literal[
    "ComptrollerLib",
    "Dispatcher",
    "FeeManager",
    "FundDataProviderRouter",
    "FundDeployer",
    "FundValueCalculatorRouter",
    "IntegrationManager",
    "PolicyManager",
    "VaultLib",
    "AaveDebtPositionLib",
    "AaveDebtPositionParser",
    "AaveV3DebtPositionLib",
    "AaveV3DebtPositionParser",
    "AaveV3FlashLoanAssetManagerFactory",
    "AaveV3FlashLoanAssetManagerLib",
    "AavePriceFeed",
    "AaveV2Adapter",
    "AaveV2ATokenListOwner",
    "AaveV3Adapter",
    "AaveV3ATokenListOwner",
    "AddressListRegistry",
    "AlicePositionLib",
    "AlicePositionParser",
    "AllowedAdapterIncomingAssetsPolicy",
    "AllowedAdaptersPerManagerPolicy",
    "AllowedAdaptersPolicy",
    "AllowedAssetsForRedemptionPolicy",
    "AllowedDepositRecipientsPolicy",
    "AllowedExternalPositionTypesPerManagerPolicy",
    "AllowedExternalPositionTypesPolicy",
    "AllowedRedeemersForSpecificAssetsPolicy",
    "AllowedSharesTransferRecipientsPolicy",
    "ArbitraryLoanPositionLib",
    "ArbitraryLoanPositionParser",
    "ArbitraryLoanTotalNominalDeltaOracleModule",
    "ArrakisV2Adapter",
    "ArrakisV2PriceFeed",
    "AssetValueCalculator",
    "BalancerV2GaugeTokenPriceFeed",
    "BalancerV2LiquidityAdapter",
    "BalancerV2StablePoolPriceFeed",
    "BalancerV2WeightedPoolPriceFeed",
    "ChainlinkLikeWstethPriceFeed",
    "ChainlinkLikeYnEthPriceFeed",
    "CompoundAdapter",
    "CompoundDebtPositionLib",
    "CompoundDebtPositionParser",
    "CompoundPriceFeed",
    "CompoundV3TokenListOwner",
    "CompoundV3Adapter",
    "ConvexVotingPositionLib",
    "ConvexVotingPositionParser",
    "CumulativeSlippageTolerancePolicy",
    "CurveExchangeAdapter",
    "CurveLiquidityAaveAdapter",
    "CurveLiquidityAdapter",
    "CurveLiquiditySethAdapter",
    "CurveLiquidityStethAdapter",
    "CurvePriceFeed",
    "DepositWrapper",
    "DisallowedAdapterIncomingAssetsPolicy",
    "EntranceRateBurnFee",
    "EntranceRateDirectFee",
    "ERC4626Adapter",
    "ERC4626PriceFeed",
    "EtherFiEthPriceFeed",
    "ExitRateBurnFee",
    "ExitRateDirectFee",
    "ExternalPositionFactory",
    "ExternalPositionManager",
    "FiduPriceFeed",
    "FundValueCalculator",
    "GasRelayPaymasterFactory",
    "GasRelayPaymasterLib",
    "GatedRedemptionQueueSharesWrapperFactory",
    "GatedRedemptionQueueSharesWrapperLib",
    "GenericAdapter",
    "GlobalConfigLib",
    "GlobalConfigProxy",
    "GMXV2LeverageTradingPositionLib",
    "GMXV2LeverageTradingPositionParser",
    "KilnStakingPositionLib",
    "KilnStakingPositionParser",
    "LidoWithdrawalsPositionLib",
    "LidoWithdrawalsPositionParser",
    "LiquityDebtPositionLib",
    "LiquityDebtPositionParser",
    "ManagementFee",
    "ManualValueOracleFactory",
    "MapleLiquidityPositionLib",
    "MapleLiquidityPositionParser",
    "MinAssetBalancesPostRedemptionPolicy",
    "MinMaxInvestmentPolicy",
    "MinSharesSupplyFee",
    "MorphoBluePositionLib",
    "MorphoBluePositionParser",
    "NoDepegOnRedeemSharesForSpecificAssetsPolicy",
    "NotionalV2PositionLib",
    "NotionalV2PositionParser",
    "OneInchV5Adapter",
    "OnlyRemoveDustExternalPositionPolicy",
    "OnlyUntrackDustOrPricelessAssetsPolicy",
    "ParaSwapV5Adapter",
    "PeggedDerivativesPriceFeed",
    "PendleV2Adapter",
    "PendleV2PositionLib",
    "PendleV2PositionParser",
    "PendleMarketsRegistry",
    "PerformanceFee",
    "PoolTogetherV4Adapter",
    "PoolTogetherV4PriceFeed",
    "ProtocolFeeReserveLib",
    "ProtocolFeeReserveProxy",
    "ProtocolFeeTracker",
    "SharePriceThrottledAssetManagerLib",
    "SharePriceThrottledAssetManagerFactory",
    "SharesSplitterFactory",
    "SingleAssetRedemptionQueueLib",
    "SingleAssetRedemptionQueueFactory",
    "SolvV2BondBuyerPositionLib",
    "SolvV2BondBuyerPositionParser",
    "SolvV2BondIssuerPositionLib",
    "SolvV2BondIssuerPositionParser",
    "StaderSDPriceFeed",
    "StaderStakingAdapter",
    "StaderWithdrawalsPositionLib",
    "StaderWithdrawalsPositionParser",
    "StakeWiseV3StakingPositionLib",
    "StakeWiseV3StakingPositionParser",
    "SwellStakingAdapter",
    "SynthetixAdapter",
    "TermFinanceV1LendingPositionLib",
    "TermFinanceV1LendingPositionParser",
    "TheGraphDelegationPositionLib",
    "TheGraphDelegationPositionParser",
    "ThreeOneThirdAdapter",
    "TransferAssetsAdapter",
    "UintListRegistry",
    "UniswapV2ExchangeAdapter",
    "UniswapV2LiquidityAdapter",
    "UniswapV2PoolPriceFeed",
    "UniswapV3Adapter",
    "UniswapV3LiquidityPositionLib",
    "UniswapV3LiquidityPositionParser",
    "UnpermissionedActionsWrapper",
    "UsdEthSimulatedAggregator",
    "ValueInterpreter",
    "WstethPriceFeed",
    "YearnVaultV2Adapter",
    "YearnVaultV2PriceFeed",
    "ZeroExV2Adapter",
    "ZeroExV4Adapter",
    "ZeroExV4AdapterPmm2Kyc",
]


EncoreContractNames = Literal[
    "ComptrollerLib",
    "Dispatcher",
    "FeeManager",
    "FundDataProviderRouter",
    "FundDeployer",
    "FundValueCalculatorRouter",
    "IntegrationManager",
    "PolicyManager",
    "VaultLib",
    "AaveAdapter",
    "AavePriceFeed",
    "AdapterBlacklist",
    "AdapterWhitelist",
    "AggregatedDerivativePriceFeed",
    "AlphaHomoraV1Adapter",
    "AlphaHomoraV1PriceFeed",
    "AssetBlacklist",
    "AssetValueCalculator",
    "AssetWhitelist",
    "BuySharesCallerWhitelist",
    "ChainlinkPriceFeed",
    "CompoundAdapter",
    "CompoundPriceFeed",
    "CurveExchangeAdapter",
    "CurveLiquidityAaveAdapter",
    "CurveLiquidityEursAdapter",
    "CurveLiquiditySethAdapter",
    "CurveLiquidityStethAdapter",
    "CurvePriceFeed",
    "EntranceRateBurnFee",
    "EntranceRateDirectFee",
    "FundActionsWrapper",
    "FundValueCalculator",
    "GuaranteedRedemption",
    "IdleAdapter",
    "IdlePriceFeed",
    "InvestorWhitelist",
    "KyberAdapter",
    "LidoStethPriceFeed",
    "ManagementFee",
    "MaxConcentration",
    "MinMaxInvestment",
    "ParaSwapV4Adapter",
    "PerformanceFee",
    "StakehoundEthPriceFeed",
    "SynthetixAdapter",
    "SynthetixPriceFeed",
    "TrackedAssetsAdapter",
    "UniswapV2Adapter",
    "UniswapV2PoolPriceFeed",
    "ValueInterpreter",
    "WdgldPriceFeed",
    "YearnVaultV2Adapter",
    "YearnVaultV2PriceFeed",
    "ZeroExV2Adapter",
]


PhoenixContractNames = Literal[
    "ComptrollerLib",
    "Dispatcher",
    "FeeManager",
    "FundDataProviderRouter",
    "FundDeployer",
    "FundValueCalculatorRouter",
    "IntegrationManager",
    "PolicyManager",
    "VaultLib",
    "AaveAdapter",
    "AavePriceFeed",
    "AdapterBlacklist",
    "AdapterWhitelist",
    "AggregatedDerivativePriceFeed",
    "AlphaHomoraV1Adapter",
    "AlphaHomoraV1PriceFeed",
    "AssetBlacklist",
    "AssetValueCalculator",
    "AssetWhitelist",
    "BuySharesCallerWhitelist",
    "ChaiAdapter",
    "ChainlinkPriceFeed",
    "ChaiPriceFeed",
    "CompoundAdapter",
    "CompoundPriceFeed",
    "CurveExchangeAdapter",
    "CurveLiquidityAaveAdapter",
    "CurveLiquiditySethAdapter",
    "CurveLiquidityStethAdapter",
    "CurvePriceFeed",
    "EntranceRateBurnFee",
    "EntranceRateDirectFee",
    "FundActionsWrapper",
    "FundValueCalculator",
    "GuaranteedRedemption",
    "IdleAdapter",
    "IdlePriceFeed",
    "InvestorWhitelist",
    "KyberAdapter",
    "LidoStethPriceFeed",
    "ManagementFee",
    "MaxConcentration",
    "MinMaxInvestment",
    "ParaSwapV4Adapter",
    "PerformanceFee",
    "StakehoundEthPriceFeed",
    "SynthetixAdapter",
    "SynthetixPriceFeed",
    "TrackedAssetsAdapter",
    "UniswapV2Adapter",
    "UniswapV2PoolPriceFeed",
    "ValueInterpreter",
    "WdgldPriceFeed",
    "ZeroExV2Adapter",
]


VersionContractNames = EncoreContractNames | PhoenixContractNames | SuluContractNames
