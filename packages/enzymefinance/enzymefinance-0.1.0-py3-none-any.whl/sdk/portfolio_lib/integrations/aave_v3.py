import asyncio
from decimal import Decimal
from eth_abi import encode, decode
from web3.types import ChecksumAddress, HexStr, TxParams
from web3 import Web3
from typing import Tuple, TypedDict
from ..._internal import integration_manager as integration_manager_lib
from ..._internal import external_position_manager as external_position_manager_lib
from ...utils.clients import PublicClient
from ...utils.conversion import from_wei
from ...utils.encoding import encoding_to_types
from ... import asset as asset_lib


# --------------------------------------------------------------------------------------------
# LEND
# --------------------------------------------------------------------------------------------


async def lend(*args) -> TxParams:
    """
    Args:
        client: WalletClient
        comptroller_proxy: ChecksumAddress
        integration_manager: ChecksumAddress
        integration_adapter: ChecksumAddress
        call_args: dict[str, ChecksumAddress | int]
            {
                "a_token": ChecksumAddress,
                "deposit_amount": int,
            }
    """
    _lend = integration_manager_lib.make_use(
        integration_manager_lib.SELECTOR["lend"], lend_encode
    )
    return await _lend(*args)


LEND_ENCODING = [
    {
        "type": "address",
        "name": "aToken",
    },
    {
        "type": "uint256",
        "name": "depositAmount",
    },
]


class LendArgs(TypedDict):
    a_token: ChecksumAddress
    deposit_amount: int


def lend_encode(a_token: ChecksumAddress, deposit_amount: int) -> HexStr:
    types = encoding_to_types(LEND_ENCODING)
    values = [a_token, deposit_amount]
    return Web3.to_hex(encode(types, values))


def lend_decode(encoded: HexStr) -> dict[str, ChecksumAddress | int]:
    """
    Returns:
        {
            "a_token": ChecksumAddress,
            "deposit_amount": int,
        }
    """
    types = encoding_to_types(LEND_ENCODING)
    decoded = decode(types, Web3.to_bytes(hexstr=encoded))
    return {
        "a_token": Web3.to_checksum_address(decoded[0]),
        "deposit_amount": decoded[1],
    }


# --------------------------------------------------------------------------------------------
# REDEEM
# --------------------------------------------------------------------------------------------


async def redeem(*args) -> TxParams:
    """
    Args:
        client: WalletClient
        comptroller_proxy: ChecksumAddress
        integration_manager: ChecksumAddress
        integration_adapter: ChecksumAddress
        call_args: dict[str, ChecksumAddress | int]
            {
                "a_token": ChecksumAddress,
                "redeem_amount": int,
            }
    """
    _redeem = integration_manager_lib.make_use(
        integration_manager_lib.SELECTOR["redeem"], redeem_encode
    )
    return await _redeem(*args)


REDEEM_ENCODING = [
    {
        "type": "address",
        "name": "aToken",
    },
    {
        "type": "uint256",
        "name": "redeemAmount",
    },
]


class RedeemArgs(TypedDict):
    a_token: ChecksumAddress
    redeem_amount: int


def redeem_encode(a_token: ChecksumAddress, redeem_amount: int) -> HexStr:
    types = encoding_to_types(REDEEM_ENCODING)
    values = [a_token, redeem_amount]
    return Web3.to_hex(encode(types, values))


def redeem_decode(encoded: HexStr) -> dict[str, ChecksumAddress | int]:
    """
    Returns:
        {
            "a_token": ChecksumAddress,
            "redeem_amount": int,
        }
    """
    types = encoding_to_types(REDEEM_ENCODING)
    decoded = decode(types, Web3.to_bytes(hexstr=encoded))
    return {
        "a_token": Web3.to_checksum_address(decoded[0]),
        "redeem_amount": decoded[1],
    }


# --------------------------------------------------------------------------------------------
# EXTERNAL POSITION
# --------------------------------------------------------------------------------------------


class Action(TypedDict):
    add_collateral: int
    remove_collateral: int
    borrow: int
    repay_borrow: int
    set_e_mode: int
    set_use_reserve_as_collateral: int
    claim_rewards: int
    sweep: int


ACTION = {
    "add_collateral": 0,
    "remove_collateral": 1,
    "borrow": 2,
    "repay_borrow": 3,
    "set_e_mode": 4,
    "set_use_reserve_as_collateral": 5,
    "claim_rewards": 6,
    "sweep": 7,
}

create = external_position_manager_lib.create_only


# --------------------------------------------------------------------------------------------
# ADD COLLATERAL
# --------------------------------------------------------------------------------------------


async def add_collateral(*args) -> TxParams:
    """
    Args:
        client: WalletClient
        comptroller_proxy: ChecksumAddress
        external_position_manager: ChecksumAddress
        external_position_proxy: ChecksumAddress
        call_args: dict[str, list[ChecksumAddress] | list[int] | bool]
            {
                "a_tokens": list[ChecksumAddress],
                "amounts": list[int],
                "from_underlying": bool,
            }
    """
    _add_collateral = external_position_manager_lib.make_use(
        ACTION["add_collateral"], add_collateral_encode
    )
    return await _add_collateral(*args)


async def create_and_add_collateral(*args) -> TxParams:
    """
    Args:
        client: WalletClient
        type_id: int
        comptroller_proxy: ChecksumAddress
        external_position_manager: ChecksumAddress
        initialization_data: HexStr
        call_args: dict[str, list[ChecksumAddress] | list[int] | bool]
            {
                "a_tokens": list[ChecksumAddress],
                "amounts": list[int],
                "from_underlying": bool,
            }
    """
    _create_and_add_collateral = external_position_manager_lib.make_create_and_use(
        ACTION["add_collateral"], add_collateral_encode
    )
    return await _create_and_add_collateral(*args)


ADD_COLLATERAL_ENCODING = [
    {
        "type": "address[]",
        "name": "aTokens",
    },
    {
        "type": "uint256[]",
        "name": "amounts",
    },
    {
        "type": "bool",
        "name": "fromUnderlying",
    },
]


class AddCollateralArgs(TypedDict):
    a_tokens: list[ChecksumAddress]
    amounts: list[int]
    from_underlying: bool


def add_collateral_encode(
    a_tokens: list[ChecksumAddress], amounts: list[int], from_underlying: bool
) -> HexStr:
    types = encoding_to_types(ADD_COLLATERAL_ENCODING)
    values = [a_tokens, amounts, from_underlying]
    return Web3.to_hex(encode(types, values))


def add_collateral_decode(
    encoded: HexStr,
) -> dict[str, list[ChecksumAddress] | list[int] | bool]:
    """
    Returns:
        {
            "a_tokens": list[ChecksumAddress],
            "amounts": list[int],
            "from_underlying": bool,
        }
    """
    types = encoding_to_types(ADD_COLLATERAL_ENCODING)
    decoded = decode(types, Web3.to_bytes(hexstr=encoded))
    return {
        "a_tokens": [Web3.to_checksum_address(a_token) for a_token in decoded[0]],
        "amounts": decoded[1],
        "from_underlying": decoded[2],
    }


# --------------------------------------------------------------------------------------------
# REMOVE COLLATERAL
# --------------------------------------------------------------------------------------------


async def remove_collateral(*args) -> TxParams:
    """
    Args:
        client: WalletClient
        comptroller_proxy: ChecksumAddress
        external_position_manager: ChecksumAddress
        external_position_proxy: ChecksumAddress
        call_args: dict[str, list[ChecksumAddress] | list[int] | bool]
            {
                "a_tokens": list[ChecksumAddress],
                "amounts": list[int],
                "to_underlying": bool,
            }
    """
    _remove_collateral = external_position_manager_lib.make_use(
        ACTION["remove_collateral"], remove_collateral_encode
    )
    return await _remove_collateral(*args)


REMOVE_COLLATERAL_ENCODING = [
    {
        "type": "address[]",
        "name": "aTokens",
    },
    {
        "type": "uint256[]",
        "name": "amounts",
    },
    {
        "type": "bool",
        "name": "toUnderlying",
    },
]


class RemoveCollateralArgs(TypedDict):
    a_tokens: list[ChecksumAddress]
    amounts: list[int]
    to_underlying: bool


def remove_collateral_encode(
    a_tokens: list[ChecksumAddress], amounts: list[int], to_underlying: bool
) -> HexStr:
    types = encoding_to_types(REMOVE_COLLATERAL_ENCODING)
    values = [a_tokens, amounts, to_underlying]
    return Web3.to_hex(encode(types, values))


def remove_collateral_decode(
    encoded: HexStr,
) -> dict[str, list[ChecksumAddress] | list[int] | bool]:
    """
    Returns:
        {
            "a_tokens": list[ChecksumAddress],
            "amounts": list[int],
            "to_underlying": bool,
        }
    """
    types = encoding_to_types(REMOVE_COLLATERAL_ENCODING)
    decoded = decode(types, Web3.to_bytes(hexstr=encoded))
    return {
        "a_tokens": [Web3.to_checksum_address(a_token) for a_token in decoded[0]],
        "amounts": decoded[1],
        "to_underlying": decoded[2],
    }


# --------------------------------------------------------------------------------------------
# BORROW
# --------------------------------------------------------------------------------------------


async def borrow(*args) -> TxParams:
    """
    Args:
        client: WalletClient
        comptroller_proxy: ChecksumAddress
        external_position_manager: ChecksumAddress
        external_position_proxy: ChecksumAddress
        call_args: dict[str, list[ChecksumAddress] | list[int]]
            {
                "underlying_tokens": list[ChecksumAddress],
                "amounts": list[int],
            }
    """
    _borrow = external_position_manager_lib.make_use(ACTION["borrow"], borrow_encode)
    return await _borrow(*args)


async def create_and_borrow(*args) -> TxParams:
    """
    Args:
        client: WalletClient
        type_id: int
        comptroller_proxy: ChecksumAddress
        external_position_manager: ChecksumAddress
        initialization_data: HexStr
        call_args: dict[str, list[ChecksumAddress] | list[int]]
            {
                "underlying_tokens": list[ChecksumAddress],
                "amounts": list[int],
            }
    """
    _create_and_borrow = external_position_manager_lib.make_create_and_use(
        ACTION["borrow"], borrow_encode
    )
    return await _create_and_borrow(*args)


BORROW_ENCODING = [
    {
        "type": "address[]",
        "name": "underlyingTokens",
    },
    {
        "type": "uint256[]",
        "name": "amounts",
    },
]


class BorrowArgs(TypedDict):
    underlying_tokens: list[ChecksumAddress]
    amounts: list[int]


def borrow_encode(
    underlying_tokens: list[ChecksumAddress], amounts: list[int]
) -> HexStr:
    types = encoding_to_types(BORROW_ENCODING)
    values = [underlying_tokens, amounts]
    return Web3.to_hex(encode(types, values))


def borrow_decode(encoded: HexStr) -> dict[str, list[ChecksumAddress] | list[int]]:
    """
    Returns:
        {
            "underlying_tokens": list[ChecksumAddress],
            "amounts": list[int],
        }
    """
    types = encoding_to_types(BORROW_ENCODING)
    decoded = decode(types, Web3.to_bytes(hexstr=encoded))
    return {
        "underlying_tokens": [
            Web3.to_checksum_address(underlying_token)
            for underlying_token in decoded[0]
        ],
        "amounts": decoded[1],
    }


# --------------------------------------------------------------------------------------------
# REPAY BORROW
# --------------------------------------------------------------------------------------------


async def repay_borrow(*args) -> TxParams:
    """
    Args:
        client: WalletClient
        comptroller_proxy: ChecksumAddress
        external_position_manager: ChecksumAddress
        external_position_proxy: ChecksumAddress
        call_args: dict[str, list[ChecksumAddress] | list[int]]
            {
                "underlying_tokens": list[ChecksumAddress],
                "amounts": list[int],
            }
    """
    _repay_borrow = external_position_manager_lib.make_use(
        ACTION["repay_borrow"], repay_borrow_encode
    )
    return await _repay_borrow(*args)


REPAY_BORROW_ENCODING = [
    {
        "type": "address[]",
        "name": "underlyingTokens",
    },
    {
        "type": "uint256[]",
        "name": "amounts",
    },
]


class RepayBorrowArgs(TypedDict):
    underlying_tokens: list[ChecksumAddress]
    amounts: list[int]


def repay_borrow_encode(
    underlying_tokens: list[ChecksumAddress], amounts: list[int]
) -> HexStr:
    types = encoding_to_types(REPAY_BORROW_ENCODING)
    values = [underlying_tokens, amounts]
    return Web3.to_hex(encode(types, values))


def repay_borrow_decode(
    encoded: HexStr,
) -> dict[str, list[ChecksumAddress] | list[int]]:
    """
    Returns:
        {
            "underlying_tokens": list[ChecksumAddress],
            "amounts": list[int],
        }
    """
    types = encoding_to_types(REPAY_BORROW_ENCODING)
    decoded = decode(types, Web3.to_bytes(hexstr=encoded))
    return {
        "underlying_tokens": [
            Web3.to_checksum_address(underlying_token)
            for underlying_token in decoded[0]
        ],
        "amounts": decoded[1],
    }


# --------------------------------------------------------------------------------------------
# SET E-MODE
# --------------------------------------------------------------------------------------------


async def set_e_mode(*args) -> TxParams:
    """
    Args:
        client: WalletClient
        comptroller_proxy: ChecksumAddress
        external_position_manager: ChecksumAddress
        external_position_proxy: ChecksumAddress
        call_args: dict[str, int]
            {
                "category_id": int,
            }
    """
    _set_e_mode = external_position_manager_lib.make_use(
        ACTION["set_e_mode"], set_e_mode_encode
    )
    return await _set_e_mode(*args)


SET_EMODE_ENCODING = [
    {
        "type": "uint8",
        "name": "categoryId",
    },
]


class SetEModeArgs(TypedDict):
    category_id: int


def set_e_mode_encode(category_id: int) -> HexStr:
    types = encoding_to_types(SET_EMODE_ENCODING)
    values = [category_id]
    return Web3.to_hex(encode(types, values))


def set_e_mode_decode(encoded: HexStr) -> dict[str, int]:
    """
    Returns:
        {
            "category_id": int,
        }
    """
    types = encoding_to_types(SET_EMODE_ENCODING)
    decoded = decode(types, Web3.to_bytes(hexstr=encoded))
    return {
        "category_id": decoded[0],
    }


# --------------------------------------------------------------------------------------------
# SET USE RESERVE AS COLLATERAL
# --------------------------------------------------------------------------------------------


async def set_use_reserve_as_collateral(*args) -> TxParams:
    """
    Args:
        client: WalletClient
        comptroller_proxy: ChecksumAddress
        external_position_manager: ChecksumAddress
        external_position_proxy: ChecksumAddress
        call_args: dict[str, ChecksumAddress | bool]
            {
                "underlying": ChecksumAddress,
                "use_as_collateral": bool,
            }
    """
    _set_use_reserve_as_collateral = external_position_manager_lib.make_use(
        ACTION["set_use_reserve_as_collateral"], set_use_reserve_as_collateral_encode
    )
    return await _set_use_reserve_as_collateral(*args)


SET_USE_RESERVE_AS_COLLATERAL_ENCODING = [
    {
        "type": "address",
        "name": "underlying",
    },
    {
        "type": "bool",
        "name": "useAsCollateral",
    },
]


class SetUseReserveAsCollateralArgs(TypedDict):
    underlying: ChecksumAddress
    use_as_collateral: bool


def set_use_reserve_as_collateral_encode(
    underlying: ChecksumAddress, use_as_collateral: bool
) -> HexStr:
    types = encoding_to_types(SET_USE_RESERVE_AS_COLLATERAL_ENCODING)
    values = [underlying, use_as_collateral]
    return Web3.to_hex(encode(types, values))


def set_use_reserve_as_collateral_decode(
    encoded: HexStr,
) -> dict[str, ChecksumAddress | bool]:
    """
    Returns:
        {
            "underlying": ChecksumAddress,
            "use_as_collateral": bool,
        }
    """
    types = encoding_to_types(SET_USE_RESERVE_AS_COLLATERAL_ENCODING)
    decoded = decode(types, Web3.to_bytes(hexstr=encoded))
    return {
        "underlying": decoded[0],
        "use_as_collateral": decoded[1],
    }


# --------------------------------------------------------------------------------------------
# CLAIM REWARDS
# --------------------------------------------------------------------------------------------


async def claim_rewards(*args) -> TxParams:
    """
    Args:
        client: WalletClient
        comptroller_proxy: ChecksumAddress
        external_position_manager: ChecksumAddress
        external_position_proxy: ChecksumAddress
        call_args: dict[str, list[ChecksumAddress] | int | ChecksumAddress]
            {
                "assets": list[ChecksumAddress],
                "amount": int,
                "reward_token": ChecksumAddress,
            }
    """
    _claim_rewards = external_position_manager_lib.make_use(
        ACTION["claim_rewards"], claim_rewards_encode
    )
    return await _claim_rewards(*args)


CLAIM_REWARDS_ENCODING = [
    {
        "type": "address[]",
        "name": "assets",
    },
    {
        "type": "uint256",
        "name": "amount",
    },
    {
        "type": "address",
        "name": "rewardToken",
    },
]


class ClaimRewardsArgs(TypedDict):
    assets: list[ChecksumAddress]
    amount: int
    reward_token: ChecksumAddress


def claim_rewards_encode(
    assets: list[ChecksumAddress], amount: int, reward_token: ChecksumAddress
) -> HexStr:
    types = encoding_to_types(CLAIM_REWARDS_ENCODING)
    values = [assets, amount, reward_token]
    return Web3.to_hex(encode(types, values))


def claim_rewards_decode(
    encoded: HexStr,
) -> dict[str, list[ChecksumAddress] | int | ChecksumAddress]:
    """
    Returns:
        {
            "assets": list[ChecksumAddress],
            "amount": int,
            "reward_token": ChecksumAddress,
        }
    """
    types = encoding_to_types(CLAIM_REWARDS_ENCODING)
    decoded = decode(types, Web3.to_bytes(hexstr=encoded))
    return {
        "assets": [Web3.to_checksum_address(asset) for asset in decoded[0]],
        "amount": decoded[1],
        "reward_token": Web3.to_checksum_address(decoded[2]),
    }


# --------------------------------------------------------------------------------------------
# SWEEP
# --------------------------------------------------------------------------------------------


async def sweep(*args) -> TxParams:
    """
    Args:
        client: WalletClient
        comptroller_proxy: ChecksumAddress
        external_position_manager: ChecksumAddress
        external_position_proxy: ChecksumAddress
        call_args: dict[str, list[ChecksumAddress]]
            {
                "assets": list[ChecksumAddress],
            }
    """
    _sweep = external_position_manager_lib.make_use(ACTION["sweep"], sweep_encode)
    return await _sweep(*args)


SWEEP_ENCODING = [
    {
        "type": "address[]",
        "name": "assets",
    },
]


class SweepArgs(TypedDict):
    assets: list[ChecksumAddress]


def sweep_encode(assets: list[ChecksumAddress]) -> HexStr:
    types = encoding_to_types(SWEEP_ENCODING)
    values = [assets]
    return Web3.to_hex(encode(types, values))


def sweep_decode(encoded: HexStr) -> dict[str, list[ChecksumAddress]]:
    """
    Returns:
        {
            "assets": list[ChecksumAddress],
        }
    """
    types = encoding_to_types(SWEEP_ENCODING)
    decoded = decode(types, Web3.to_bytes(hexstr=encoded))
    return {
        "assets": [Web3.to_checksum_address(asset) for asset in decoded[0]],
    }


# --------------------------------------------------------------------------------------------
# THIRD PARTY READ FUNCTIONS
# --------------------------------------------------------------------------------------------


POOL_ADDRESS_PROVIDER_ABI = [
    {
        "inputs": [],
        "name": "getPool",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
]


async def get_pool(
    client: PublicClient,
    pool_address_provider: ChecksumAddress,
) -> ChecksumAddress:
    contract = client.contract(pool_address_provider, POOL_ADDRESS_PROVIDER_ABI)
    function = contract.functions.getPool()
    return await function.call()


POOL_ABI = [
    {
        "inputs": [{"internalType": "uint8", "name": "id", "type": "uint8"}],
        "name": "getEModeCategoryData",
        "outputs": [
            {
                "components": [
                    {"internalType": "uint16", "name": "ltv", "type": "uint16"},
                    {
                        "internalType": "uint16",
                        "name": "liquidationThreshold",
                        "type": "uint16",
                    },
                    {
                        "internalType": "uint16",
                        "name": "liquidationBonus",
                        "type": "uint16",
                    },
                    {
                        "internalType": "address",
                        "name": "priceSource",
                        "type": "address",
                    },
                    {"internalType": "string", "name": "label", "type": "string"},
                ],
                "internalType": "struct DataTypes.EModeCategory",
                "name": "",
                "type": "tuple",
            },
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
        "name": "getUserAccountData",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "totalCollateralBase",
                "type": "uint256",
            },
            {"internalType": "uint256", "name": "totalDebtBase", "type": "uint256"},
            {
                "internalType": "uint256",
                "name": "availableBorrowsBase",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "currentLiquidationThreshold",
                "type": "uint256",
            },
            {"internalType": "uint256", "name": "ltv", "type": "uint256"},
            {"internalType": "uint256", "name": "healthFactor", "type": "uint256"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
]


async def get_e_mode_category_data(
    client: PublicClient,
    pool: ChecksumAddress,
    category_id: int,
) -> Tuple[int, int, int, ChecksumAddress, str]:
    """
    Returns:
        (
            ltv: int,
            liquidation_threshold: int,
            liquidation_bonus: int,
            price_source: ChecksumAddress,
            label: str,
        )
    """
    contract = client.contract(pool, POOL_ABI)
    function = contract.functions.getEModeCategoryData(category_id)
    return await function.call()


async def get_user_account_data(
    client: PublicClient,
    pool: ChecksumAddress,
    user: ChecksumAddress,
) -> Tuple[int, int, int, int, int, int]:
    """
    Returns:
        (
            total_collateral_base: int,
            total_debt_base: int,
            available_borrows_base: int,
            current_liquidation_threshold: int,
            ltv: int,
            health_factor: int,
        )
    """
    contract = client.contract(pool, POOL_ABI)
    function = contract.functions.getUserAccountData(user)
    return await function.call()


REWARDS_CONTROLLER_ABI = [
    {
        "inputs": [
            {"internalType": "address[]", "name": "assets", "type": "address[]"},
            {"internalType": "address", "name": "user", "type": "address"},
        ],
        "name": "getAllUserRewards",
        "outputs": [
            {"internalType": "address[]", "name": "rewardsList", "type": "address[]"},
            {
                "internalType": "uint256[]",
                "name": "unclaimedAmounts",
                "type": "uint256[]",
            },
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "asset", "type": "address"}],
        "name": "getRewardsByAsset",
        "outputs": [{"internalType": "address[]", "name": "", "type": "address[]"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "asset", "type": "address"},
            {"internalType": "address", "name": "reward", "type": "address"},
        ],
        "name": "getRewardsData",
        "outputs": [
            {"internalType": "uint256", "name": "index", "type": "uint256"},
            {"internalType": "uint256", "name": "emissionPerSecond", "type": "uint256"},
            {
                "internalType": "uint256",
                "name": "lastUpdateTimestamp",
                "type": "uint256",
            },
            {"internalType": "uint256", "name": "distributionEnd", "type": "uint256"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
]


async def get_all_user_rewards(
    client: PublicClient,
    rewards_controller: ChecksumAddress,
    assets: list[ChecksumAddress],
    user: ChecksumAddress,
) -> Tuple[list[ChecksumAddress], list[int]]:
    """
    Returns:
        (
            rewards_list: list[ChecksumAddress],
            unclaimed_amounts: list[int],
        )
    """
    contract = client.contract(rewards_controller, REWARDS_CONTROLLER_ABI)
    function = contract.functions.getAllUserRewards(assets, user)
    return await function.call()


async def get_rewards_by_asset(
    client: PublicClient,
    rewards_controller: ChecksumAddress,
    asset: ChecksumAddress,
) -> list[ChecksumAddress]:
    """
    Returns:
        rewards_list: list[ChecksumAddress]
    """
    contract = client.contract(rewards_controller, REWARDS_CONTROLLER_ABI)
    function = contract.functions.getRewardsByAsset(asset)
    return await function.call()


async def get_rewards_data(
    client: PublicClient,
    rewards_controller: ChecksumAddress,
    asset: ChecksumAddress,
    reward: ChecksumAddress,
) -> Tuple[int, int, int, int]:
    """
    Returns:
        (
            index: int,
            emission_per_second: int,
            last_update_timestamp: int,
            distribution_end: int,
        )
    """
    contract = client.contract(rewards_controller, REWARDS_CONTROLLER_ABI)
    function = contract.functions.getRewardsData(asset, reward)
    return await function.call()


PROTOCOL_DATA_PROVIDER_ABI = [
    {
        "inputs": [{"internalType": "address", "name": "asset", "type": "address"}],
        "name": "getReserveCaps",
        "outputs": [
            {"internalType": "uint256", "name": "supplyCap", "type": "uint256"},
            {"internalType": "uint256", "name": "borrowCap", "type": "uint256"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "asset", "type": "address"}],
        "name": "getReserveData",
        "outputs": [
            {"internalType": "uint256", "name": "unbacked", "type": "uint256"},
            {
                "internalType": "uint256",
                "name": "accruedToTreasuryScaled",
                "type": "uint256",
            },
            {"internalType": "uint256", "name": "totalAToken", "type": "uint256"},
            {"internalType": "uint256", "name": "totalStableDebt", "type": "uint256"},
            {"internalType": "uint256", "name": "totalVariableDebt", "type": "uint256"},
            {"internalType": "uint256", "name": "liquidityRate", "type": "uint256"},
            {
                "internalType": "uint256",
                "name": "variableBorrowRate",
                "type": "uint256",
            },
            {"internalType": "uint256", "name": "stableBorrowRate", "type": "uint256"},
            {
                "internalType": "uint256",
                "name": "averageStableBorrowRate",
                "type": "uint256",
            },
            {"internalType": "uint256", "name": "liquidityIndex", "type": "uint256"},
            {
                "internalType": "uint256",
                "name": "variableBorrowIndex",
                "type": "uint256",
            },
            {"internalType": "uint40", "name": "lastUpdateTimestamp", "type": "uint40"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
]


async def get_reserve_caps(
    client: PublicClient,
    protocol_data_provider: ChecksumAddress,
    asset: ChecksumAddress,
) -> Tuple[Decimal, Decimal]:
    """
    Returns:
        (
            supply_cap: Decimal,
            borrow_cap: Decimal,
        )
    """
    contract = client.contract(protocol_data_provider, PROTOCOL_DATA_PROVIDER_ABI)
    function = contract.functions.getReserveCaps(asset)
    reserve_caps, decimals = await asyncio.gather(
        function.call(),
        asset_lib.get_decimals(client, asset),
    )
    return (
        from_wei(reserve_caps[0], decimals),
        from_wei(reserve_caps[1], decimals),
    )


async def get_reserve_data(
    client: PublicClient,
    protocol_data_provider: ChecksumAddress,
    asset: ChecksumAddress,
) -> Tuple[int, int, int, int, int, int, int, int, int, int, int]:
    """
    Returns:
        (
            unbacked: int,
            accrued_to_treasury_scaled: int,
            total_a_token: int,
            total_stable_debt: int,
            total_variable_debt: int,
            liquidity_rate: int,
            variable_borrow_rate: int,
            stable_borrow_rate: int,
            average_stable_borrow_rate: int,
            liquidity_index: int,
            variable_borrow_index: int,
            last_update_timestamp: int,
        )
    """
    contract = client.contract(protocol_data_provider, PROTOCOL_DATA_PROVIDER_ABI)
    function = contract.functions.getReserveData(asset)
    return await function.call()


async def get_available_supply_amount(
    client: PublicClient,
    protocol_data_provider: ChecksumAddress,
    asset: ChecksumAddress,
    decimals: int,
) -> Decimal:
    reserve_caps, reserve_data = await asyncio.gather(
        get_reserve_caps(client, protocol_data_provider, asset),
        get_reserve_data(client, protocol_data_provider, asset),
    )
    return reserve_caps[1] - from_wei(reserve_data[2], decimals)


async def get_available_variable_debt_amount(
    client: PublicClient,
    protocol_data_provider: ChecksumAddress,
    asset: ChecksumAddress,
    decimals: int,
) -> Decimal:
    reserve_caps, reserve_data = await asyncio.gather(
        get_reserve_caps(client, protocol_data_provider, asset),
        get_reserve_data(client, protocol_data_provider, asset),
    )
    return reserve_caps[0] - from_wei(reserve_data[4], decimals)


UI_INCENTIVE_DATA_PROVIDER_ABI = [
    {
        "inputs": [{"internalType": "address", "name": "provider", "type": "address"}],
        "name": "getReservesIncentivesData",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "address",
                        "name": "underlyingAsset",
                        "type": "address",
                    },
                    {
                        "components": [
                            {
                                "internalType": "address",
                                "name": "tokenAddress",
                                "type": "address",
                            },
                            {
                                "internalType": "address",
                                "name": "incentiveControllerAddress",
                                "type": "address",
                            },
                            {
                                "components": [
                                    {
                                        "internalType": "string",
                                        "name": "rewardTokenSymbol",
                                        "type": "string",
                                    },
                                    {
                                        "internalType": "address",
                                        "name": "rewardTokenAddress",
                                        "type": "address",
                                    },
                                    {
                                        "internalType": "address",
                                        "name": "rewardOracleAddress",
                                        "type": "address",
                                    },
                                    {
                                        "internalType": "uint256",
                                        "name": "emissionPerSecond",
                                        "type": "uint256",
                                    },
                                    {
                                        "internalType": "uint256",
                                        "name": "incentivesLastUpdateTimestamp",
                                        "type": "uint256",
                                    },
                                    {
                                        "internalType": "uint256",
                                        "name": "tokenIncentivesIndex",
                                        "type": "uint256",
                                    },
                                    {
                                        "internalType": "uint256",
                                        "name": "emissionEndTimestamp",
                                        "type": "uint256",
                                    },
                                    {
                                        "internalType": "int256",
                                        "name": "rewardPriceFeed",
                                        "type": "int256",
                                    },
                                    {
                                        "internalType": "uint8",
                                        "name": "rewardTokenDecimals",
                                        "type": "uint8",
                                    },
                                    {
                                        "internalType": "uint8",
                                        "name": "precision",
                                        "type": "uint8",
                                    },
                                    {
                                        "internalType": "uint8",
                                        "name": "priceFeedDecimals",
                                        "type": "uint8",
                                    },
                                ],
                                "internalType": "struct IUiIncentiveDataProviderV3.RewardInfo[]",
                                "name": "rewardsTokenInformation",
                                "type": "tuple[]",
                            },
                        ],
                        "internalType": "struct IUiIncentiveDataProviderV3.IncentiveData",
                        "name": "aIncentiveData",
                        "type": "tuple",
                    },
                    {
                        "components": [
                            {
                                "internalType": "address",
                                "name": "tokenAddress",
                                "type": "address",
                            },
                            {
                                "internalType": "address",
                                "name": "incentiveControllerAddress",
                                "type": "address",
                            },
                            {
                                "components": [
                                    {
                                        "internalType": "string",
                                        "name": "rewardTokenSymbol",
                                        "type": "string",
                                    },
                                    {
                                        "internalType": "address",
                                        "name": "rewardTokenAddress",
                                        "type": "address",
                                    },
                                    {
                                        "internalType": "address",
                                        "name": "rewardOracleAddress",
                                        "type": "address",
                                    },
                                    {
                                        "internalType": "uint256",
                                        "name": "emissionPerSecond",
                                        "type": "uint256",
                                    },
                                    {
                                        "internalType": "uint256",
                                        "name": "incentivesLastUpdateTimestamp",
                                        "type": "uint256",
                                    },
                                    {
                                        "internalType": "uint256",
                                        "name": "tokenIncentivesIndex",
                                        "type": "uint256",
                                    },
                                    {
                                        "internalType": "uint256",
                                        "name": "emissionEndTimestamp",
                                        "type": "uint256",
                                    },
                                    {
                                        "internalType": "int256",
                                        "name": "rewardPriceFeed",
                                        "type": "int256",
                                    },
                                    {
                                        "internalType": "uint8",
                                        "name": "rewardTokenDecimals",
                                        "type": "uint8",
                                    },
                                    {
                                        "internalType": "uint8",
                                        "name": "precision",
                                        "type": "uint8",
                                    },
                                    {
                                        "internalType": "uint8",
                                        "name": "priceFeedDecimals",
                                        "type": "uint8",
                                    },
                                ],
                                "internalType": "struct IUiIncentiveDataProviderV3.RewardInfo[]",
                                "name": "rewardsTokenInformation",
                                "type": "tuple[]",
                            },
                        ],
                        "internalType": "struct IUiIncentiveDataProviderV3.IncentiveData",
                        "name": "vIncentiveData",
                        "type": "tuple",
                    },
                ],
                "internalType": "struct IUiIncentiveDataProviderV3.AggregatedReserveIncentiveData[]",
                "name": "",
                "type": "tuple[]",
            },
        ],
        "stateMutability": "view",
        "type": "function",
    },
]


async def get_reserves_incentives_data(
    client: PublicClient,
    ui_incentive_data_provider: ChecksumAddress,
    pool_address_provider: ChecksumAddress,
):
    # TODO: unknown return type
    contract = client.contract(
        ui_incentive_data_provider, UI_INCENTIVE_DATA_PROVIDER_ABI
    )
    function = contract.functions.getReservesIncentivesData(pool_address_provider)
    return await function.call()
