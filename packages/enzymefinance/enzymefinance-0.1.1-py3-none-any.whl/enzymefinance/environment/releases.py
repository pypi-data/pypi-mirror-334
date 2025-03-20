from typing import Any, Literal, get_args, TypedDict
from web3.types import ChecksumAddress
from .contracts import is_version, Contracts, Version
from .assets import PrimitiveAsset, CompoundV2Asset, ERC4626Asset, AssetType
from .networks import Network
from .types import Release


Status = Literal["live", "pending", "deprecated"]


Deployment = Literal["arbitrum", "base", "ethereum", "polygon", "testnet"]


def is_deployment(value: Any) -> bool:
    return isinstance(value, str) and value in get_args(Deployment)


def is_release(value: Any) -> bool:
    if isinstance(value, str) and "." in value:
        deployment, version = value.split(".")

        if is_deployment(deployment) and is_version(version):
            return version in RELEASES[deployment]

    return False


class ReleaseDefinition(TypedDict):
    # The unique release identifier.
    slug: str  # f"{Deployment}.{Version}"
    # The network identifier.
    network: Network
    # The address of the fund deployer contract.
    address: ChecksumAddress
    # The version (e.g. sulu, encore, phoenix) of the release.
    version: Version
    # The block number at which the fund deployer contract was deployed.
    inception: int
    # Mapping of contract names and their addresses within this release.
    contracts: Contracts
    # The release status (pending, deprecated or live).
    status: Status


Kind = Literal["test", "live"]


class DeploymentNamedTokensArbitrum(TypedDict):
    bal: ChecksumAddress
    comp: ChecksumAddress
    crv: ChecksumAddress
    cvx: ChecksumAddress
    dai: ChecksumAddress
    grt: ChecksumAddress
    mln: ChecksumAddress
    usdt: ChecksumAddress
    weth: ChecksumAddress


class DeploymentNamedTokensBase(TypedDict):
    comp: ChecksumAddress
    dai: ChecksumAddress
    mln: ChecksumAddress
    usdt: ChecksumAddress
    weth: ChecksumAddress


class DeploymentNamedTokensEthereum(TypedDict):
    aave: ChecksumAddress
    bal: ChecksumAddress
    ceth: ChecksumAddress
    comp: ChecksumAddress
    crv: ChecksumAddress
    cvx: ChecksumAddress
    dai: ChecksumAddress
    diva: ChecksumAddress
    ethx: ChecksumAddress
    grt: ChecksumAddress
    idle: ChecksumAddress
    lusd: ChecksumAddress
    mln: ChecksumAddress
    mpl: ChecksumAddress
    paxg: ChecksumAddress
    ptkn_mln: ChecksumAddress
    steth: ChecksumAddress
    sthoundeth: ChecksumAddress
    stkaave: ChecksumAddress
    stusd: ChecksumAddress
    sweth: ChecksumAddress
    uni: ChecksumAddress
    usda: ChecksumAddress
    usdc: ChecksumAddress
    usdt: ChecksumAddress
    weth: ChecksumAddress


class DeploymentNamedTokensPolygon(TypedDict):
    aave: ChecksumAddress
    bal: ChecksumAddress
    comp: ChecksumAddress
    crv: ChecksumAddress
    cvx: ChecksumAddress
    dai: ChecksumAddress
    eure: ChecksumAddress
    grt: ChecksumAddress
    mln: ChecksumAddress
    uni: ChecksumAddress
    usdc: ChecksumAddress
    usdt: ChecksumAddress
    weth: ChecksumAddress


DeploymentNamedTokens = (
    DeploymentNamedTokensArbitrum
    | DeploymentNamedTokensBase
    | DeploymentNamedTokensEthereum
    | DeploymentNamedTokensPolygon
)


class DeploymentNamedTokensAssetsArbitrum(TypedDict):
    bal: PrimitiveAsset
    comp: PrimitiveAsset
    crv: PrimitiveAsset
    cvx: PrimitiveAsset
    dai: PrimitiveAsset
    grt: PrimitiveAsset
    mln: PrimitiveAsset
    native_token_wrapper: PrimitiveAsset
    usdt: PrimitiveAsset
    weth: PrimitiveAsset


class DeploymentNamedTokensAssetsBase(TypedDict):
    comp: PrimitiveAsset
    dai: PrimitiveAsset
    mln: PrimitiveAsset
    native_token_wrapper: PrimitiveAsset
    usdt: PrimitiveAsset
    weth: PrimitiveAsset


class DeploymentNamedTokensAssetsEthereum(TypedDict):
    aave: PrimitiveAsset
    bal: PrimitiveAsset
    ceth: CompoundV2Asset
    comp: PrimitiveAsset
    crv: PrimitiveAsset
    cvx: PrimitiveAsset
    dai: PrimitiveAsset
    diva: PrimitiveAsset
    ethx: PrimitiveAsset
    grt: PrimitiveAsset
    idle: PrimitiveAsset
    lusd: PrimitiveAsset
    mln: PrimitiveAsset
    mpl: PrimitiveAsset
    native_token_wrapper: PrimitiveAsset
    paxg: PrimitiveAsset
    ptkn_mln: PrimitiveAsset
    sthoundeth: PrimitiveAsset
    stkaave: PrimitiveAsset
    steth: PrimitiveAsset
    stusd: ERC4626Asset
    sweth: PrimitiveAsset
    uni: PrimitiveAsset
    usda: PrimitiveAsset
    usdc: PrimitiveAsset
    usdt: PrimitiveAsset
    weth: PrimitiveAsset


class DeploymentNamedTokensAssetsPolygon(TypedDict):
    aave: PrimitiveAsset
    bal: PrimitiveAsset
    comp: PrimitiveAsset
    crv: PrimitiveAsset
    cvx: PrimitiveAsset
    dai: PrimitiveAsset
    eure: PrimitiveAsset
    grt: PrimitiveAsset
    mln: PrimitiveAsset
    native_token_wrapper: PrimitiveAsset
    uni: PrimitiveAsset
    usdc: PrimitiveAsset
    usdt: PrimitiveAsset
    weth: PrimitiveAsset


DeploymentNamedTokensAssets = (
    DeploymentNamedTokensAssetsArbitrum
    | DeploymentNamedTokensAssetsBase
    | DeploymentNamedTokensAssetsEthereum
    | DeploymentNamedTokensAssetsPolygon
)


class CoreSubgraphMapping(TypedDict):
    slug: str
    id: str
    devVersion: str


class AssetsSubgraphMapping(TypedDict):
    slug: str
    id: str


class SharesSubgraphMapping(TypedDict):
    slug: str
    id: str


class BalancesSubgraphMapping(TypedDict):
    slug: str
    id: str


class VaultsSubgraphMapping(TypedDict):
    slug: str
    id: str


class SubgraphMapping(TypedDict):
    core: CoreSubgraphMapping
    assets: AssetsSubgraphMapping
    shares: SharesSubgraphMapping
    balances: BalancesSubgraphMapping
    vaults: VaultsSubgraphMapping


class KnownAddressListIdMapping(TypedDict, total=False):
    noslippage_adapters: int
    adapters: int
    fees: int
    policies: int
    kiln_staking_contracts: int
    non_standard_price_feed_assets: int
    a_tokens: int
    deposit_wrapper_allowed_exchanges: int


class KnownAddressListIdMappingEthereumSpecific(KnownAddressListIdMapping):
    kiln_staking_contracts: int
    zero_lend_rwa_stablecoins_a_tokens: int
    zero_lend_lrt_btc_a_tokens: int


class KnownUintListIdMapping(TypedDict, total=False):
    allowed_morpho_blue_vaults: int


class ExternalContractsMapping(TypedDict):
    aaveUIIncentiveDataProvider: ChecksumAddress
    aaveV2IncentivesController: ChecksumAddress
    aaveV2LendingPoolProvider: ChecksumAddress
    aaveV3LendingPoolProvider: ChecksumAddress
    aaveV3ProtocolDataProvider: ChecksumAddress
    aaveV3RewardsController: ChecksumAddress
    aliceOrderManager: ChecksumAddress
    arrakisV2Helper: ChecksumAddress
    arrakisV2Resolver: ChecksumAddress
    balancerGaugeController: ChecksumAddress
    balancerHelpers: ChecksumAddress
    balancerMinter: ChecksumAddress
    balancerProtocolFeesCollector: ChecksumAddress
    balancerVault: ChecksumAddress
    chainlinkFeedsRegistry: ChecksumAddress
    compoundComptroller: ChecksumAddress
    compoundV3Rewards: ChecksumAddress
    curveChildLiquidityGaugeFactory: ChecksumAddress
    curveMinter: ChecksumAddress
    curveRegistry: ChecksumAddress
    cvxCrvStaking: ChecksumAddress
    gmxV2ChainlinkPriceFeed: ChecksumAddress
    gmxV2DataStore: ChecksumAddress
    gmxV2ExchangeRouter: ChecksumAddress
    gmxV2Reader: ChecksumAddress
    gmxV2ReferralStorage: ChecksumAddress
    kilnStaking: ChecksumAddress
    lidoWithdrawalsQueue: ChecksumAddress
    liquityCollSurplusPool: ChecksumAddress
    liquityHintHelpers: ChecksumAddress
    liquitySortedTroves: ChecksumAddress
    liquityTroveManager: ChecksumAddress
    makerMCDPotAddress: ChecksumAddress
    morphoBlue: ChecksumAddress
    multicall: ChecksumAddress
    paraswapV5AugustusSwapper: ChecksumAddress
    paraswapV5TokenTransferProxy: ChecksumAddress
    pendlePtLpOracle: ChecksumAddress
    staderStakingPoolManager: ChecksumAddress
    staderUserWithdrawManager: ChecksumAddress
    stakeWiseV3KeeperRewards: ChecksumAddress
    theGraphDelegationStakingProxy: ChecksumAddress
    theGraphEpochManagerProxy: ChecksumAddress
    uniswapV3NonFungiblePositionManager: ChecksumAddress
    voteLockedConvexToken: ChecksumAddress
    votiumVoteProxy: ChecksumAddress
    zeroExExchangeProxy: ChecksumAddress
    zeroExV4Exchange: ChecksumAddress
    zeroLendAaveV3UIIncentiveDataProvider: ChecksumAddress
    zeroLendLRTBTCAaveV3LendingPoolProvider: ChecksumAddress
    zeroLendLRTBTCAaveV3ProtocolDataProvider: ChecksumAddress
    zeroLendLRTBTCAaveV3RewardsController: ChecksumAddress
    zeroLendRWAStablecoinsAaveV3LendingPoolProvider: ChecksumAddress
    zeroLendRWAStablecoinsAaveV3ProtocolDataProvider: ChecksumAddress
    zeroLendRWAStablecoinsAaveV3RewardsController: ChecksumAddress


class DeploymentDefinition(TypedDict):
    slug: Deployment
    network: Network
    external_contracts: ExternalContractsMapping
    known_address_lists: (
        KnownAddressListIdMapping | KnownAddressListIdMappingEthereumSpecific
    )
    known_uint_lists: KnownUintListIdMapping
    kind: Kind
    address: ChecksumAddress
    label: str
    inception: int
    assets: list[AssetType]
    named_tokens: DeploymentNamedTokens
    subgraphs: SubgraphMapping
    releases: dict[Version, ReleaseDefinition]


# Release = Literal[
#     "arbitrum.sulu",
#     "base.sulu",
#     "ethereum.sulu",
#     "ethereum.encore",
#     "ethereum.phoenix",
#     "polygon.sulu",
#     "testnet.sulu",
# ] -> defined in types.py to avoid circular import


class ReleasesTypeVersion(TypedDict, total=False):
    sulu: str  # f"{Deployment}.{Version}"
    encore: str  # f"{Deployment}.{Version}"
    phoenix: str  # f"{Deployment}.{Version}"


class ReleasesType(TypedDict):
    arbitrum: ReleasesTypeVersion
    base: ReleasesTypeVersion
    ethereum: ReleasesTypeVersion
    polygon: ReleasesTypeVersion
    testnet: ReleasesTypeVersion


RELEASES: ReleasesType = {
    "arbitrum": {
        "sulu": "arbitrum.sulu",
    },
    "base": {
        "sulu": "base.sulu",
    },
    "ethereum": {
        "sulu": "ethereum.sulu",
        "encore": "ethereum.encore",
        "phoenix": "ethereum.phoenix",
    },
    "polygon": {
        "sulu": "polygon.sulu",
    },
    "testnet": {
        "sulu": "testnet.sulu",
    },
}
