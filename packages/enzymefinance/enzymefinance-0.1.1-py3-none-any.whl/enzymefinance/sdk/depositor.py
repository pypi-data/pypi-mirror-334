from typing import TypedDict
from web3.types import ChecksumAddress, HexStr, TxParams
from .utils.clients import PublicClient, WalletClient
from .configuration_lib.policy import is_enabled
from ..abis import abis


# --------------------------------------------------------------------------------------------
# DEPOSIT
# --------------------------------------------------------------------------------------------


async def get_shares_action_timelock(
    client: PublicClient,
    comptroller_proxy: ChecksumAddress,
) -> int:
    contract = client.contract(comptroller_proxy, abis.IComptrollerLib)
    function = contract.functions.getSharesActionTimelock()
    return await function.call()


async def get_last_shares_bought_timestamp(
    client: PublicClient,
    depositor: ChecksumAddress,
    comptroller_proxy: ChecksumAddress,
) -> int:
    contract = client.contract(comptroller_proxy, abis.IComptrollerLib)
    function = contract.functions.getLastSharesBoughtTimestampForAccount(depositor)
    return await function.call()


async def get_expected_shares_for_deposit(
    client: PublicClient,
    comptroller_proxy: ChecksumAddress,
    amount: int,
    depositor: ChecksumAddress,
) -> int:
    contract = client.contract(comptroller_proxy, abis.IComptrollerLib)
    function = contract.functions.buyShares(amount, 1)
    return await function.call({"from": depositor})


async def deposit(
    client: PublicClient,
    comptroller_proxy: ChecksumAddress,
    amount: int,
    depositor: ChecksumAddress,
    min_shares_quantity: int,
) -> TxParams:
    contract = client.contract(comptroller_proxy, abis.IComptrollerLib)
    function = contract.functions.buyShares(amount, min_shares_quantity)
    return await client.populated_transaction(function, account=depositor)


# --------------------------------------------------------------------------------------------
# REDEMPTION
# --------------------------------------------------------------------------------------------


class RedeemSharesForSpecificAssetsParams(TypedDict):
    client: PublicClient
    comptroller_proxy: ChecksumAddress
    recipient: ChecksumAddress
    shares_quantity: int
    payout_assets: list[ChecksumAddress]
    payout_percentages: list[int]


async def get_specific_assets_redemption_expected_amounts(
    client: PublicClient,
    comptroller_proxy: ChecksumAddress,
    recipient: ChecksumAddress,
    shares_quantity: int,
    payout_assets: list[ChecksumAddress],
    payout_percentages: list[int],
) -> dict[ChecksumAddress, int]:
    contract = client.contract(comptroller_proxy, abis.IComptrollerLib)
    function = contract.functions.redeemSharesForSpecificAssets(
        recipient, shares_quantity, payout_assets, payout_percentages
    )
    payout_amounts = await function.call({"from": recipient})
    assert all(payout_amount is not None for payout_amount in payout_amounts)
    return dict(zip(payout_assets, payout_amounts))


async def redeem_shares_for_specific_assets(
    client: PublicClient,
    comptroller_proxy: ChecksumAddress,
    recipient: ChecksumAddress,
    shares_quantity: int,
    payout_assets: list[ChecksumAddress],
    payout_percentages: list[int],
) -> TxParams:
    contract = client.contract(comptroller_proxy, abis.IComptrollerLib)
    function = contract.functions.redeemSharesForSpecificAssets(
        recipient, shares_quantity, payout_assets, payout_percentages
    )
    return await client.populated_transaction(function, account=recipient)


async def redeem_shares_in_kind(
    client: PublicClient,
    comptroller_proxy: ChecksumAddress,
    recipient: ChecksumAddress,
    shares_quantity: int,
    additional_assets: list[ChecksumAddress],
    assets_to_skip: list[ChecksumAddress],
) -> TxParams:
    contract = client.contract(comptroller_proxy, abis.IComptrollerLib)
    function = contract.functions.redeemSharesInKind(
        recipient, shares_quantity, additional_assets, assets_to_skip
    )
    return await client.populated_transaction(function, account=recipient)


# --------------------------------------------------------------------------------------------
# DEPOSIT WRAPPER
# --------------------------------------------------------------------------------------------


class NativeDepositArgs(TypedDict):
    client: PublicClient
    deposit_wrapper: ChecksumAddress
    comptroller_proxy: ChecksumAddress
    exchange: ChecksumAddress
    exchange_approve_target: ChecksumAddress
    exchange_data: HexStr
    min_investment_amount: int
    amount: int


async def get_expected_shares_for_native_token_deposit(
    client: PublicClient,
    deposit_wrapper: ChecksumAddress,
    comptroller_proxy: ChecksumAddress,
    exchange: ChecksumAddress,
    exchange_approve_target: ChecksumAddress,
    exchange_data: HexStr,
    min_investment_amount: int,
    amount: int,
    depositor: ChecksumAddress,
) -> int:
    contract = client.contract(deposit_wrapper, abis.IDepositWrapper)
    function = contract.functions.exchangeEthAndBuyShares(
        comptroller_proxy,
        1,
        exchange,
        exchange_approve_target,
        exchange_data,
        min_investment_amount,
    )
    return await function.call({"from": depositor, "value": amount})


async def deposit_native_token(
    client: WalletClient,
    deposit_wrapper: ChecksumAddress,
    comptroller_proxy: ChecksumAddress,
    exchange: ChecksumAddress,
    exchange_approve_target: ChecksumAddress,
    exchange_data: HexStr,
    min_investment_amount: int,
    amount: int,
    min_shares_quantity: int,
) -> TxParams:
    contract = client.contract(deposit_wrapper, abis.IDepositWrapper)
    function = contract.functions.exchangeEthAndBuyShares(
        comptroller_proxy,
        min_shares_quantity,
        exchange,
        exchange_approve_target,
        exchange_data,
        min_investment_amount,
    )
    return await client.populated_transaction(function, value=amount)


class ERC20DepositArgs(TypedDict):
    client: WalletClient
    deposit_wrapper: ChecksumAddress
    comptroller_proxy: ChecksumAddress
    input_asset: ChecksumAddress
    max_input_asset_amount: int
    exchange: ChecksumAddress
    exchange_approve_target: ChecksumAddress
    exchange_data: HexStr
    exchange_min_received: int


async def get_expected_shares_for_erc20_deposit(
    client: PublicClient,
    deposit_wrapper: ChecksumAddress,
    comptroller_proxy: ChecksumAddress,
    input_asset: ChecksumAddress,
    max_input_asset_amount: int,
    exchange: ChecksumAddress,
    exchange_approve_target: ChecksumAddress,
    exchange_data: HexStr,
    exchange_min_received: int,
    depositor: ChecksumAddress,
) -> int:
    contract = client.contract(deposit_wrapper, abis.IDepositWrapper)
    function = contract.functions.exchangeErc20AndBuyShares(
        comptroller_proxy,
        1,
        input_asset,
        max_input_asset_amount,
        exchange,
        exchange_approve_target,
        exchange_data,
        exchange_min_received,
    )
    return await function.call({"from": depositor})


async def deposit_erc20(
    client: WalletClient,
    deposit_wrapper: ChecksumAddress,
    comptroller_proxy: ChecksumAddress,
    input_asset: ChecksumAddress,
    max_input_asset_amount: int,
    exchange: ChecksumAddress,
    exchange_approve_target: ChecksumAddress,
    exchange_data: HexStr,
    exchange_min_received: int,
    min_shares_quantity: int,
) -> TxParams:
    contract = client.contract(deposit_wrapper, abis.IDepositWrapper)
    function = contract.functions.exchangeErc20AndBuyShares(
        comptroller_proxy,
        min_shares_quantity,
        input_asset,
        max_input_asset_amount,
        exchange,
        exchange_approve_target,
        exchange_data,
        exchange_min_received,
    )
    return await client.populated_transaction(function)


# --------------------------------------------------------------------------------------------
# SHARES WRAPPER DEPOSIT
# --------------------------------------------------------------------------------------------


class SharesWrapperDepositBaseParams(TypedDict):
    client: WalletClient
    shares_wrapper: ChecksumAddress
    deposit_asset: ChecksumAddress
    deposit_amount: int


async def get_expected_shares_for_shares_wrapper_deposit(
    client: PublicClient,
    shares_wrapper: ChecksumAddress,
    deposit_asset: ChecksumAddress,
    deposit_amount: int,
    depositor: ChecksumAddress,
) -> int:
    contract = client.contract(shares_wrapper, abis.IGatedRedemptionQueueSharesWrapperLib)
    function = contract.functions.deposit(deposit_asset, deposit_amount, 1)
    return await function.call({"from": depositor})


async def shares_wrapper_deposit(
    client: WalletClient,
    shares_wrapper: ChecksumAddress,
    deposit_asset: ChecksumAddress,
    deposit_amount: int,
    min_shares_amount: int,
) -> TxParams:
    contract = client.contract(shares_wrapper, abis.IGatedRedemptionQueueSharesWrapperLib)
    function = contract.functions.deposit(
        deposit_asset, deposit_amount, min_shares_amount
    )
    return await client.populated_transaction(function)


async def shares_wrapper_request_deposit(
    client: WalletClient,
    shares_wrapper: ChecksumAddress,
    deposit_asset: ChecksumAddress,
    deposit_amount: int,
) -> TxParams:
    contract = client.contract(shares_wrapper, abis.IGatedRedemptionQueueSharesWrapperLib)
    function = contract.functions.requestDeposit(deposit_asset, deposit_amount)
    return await client.populated_transaction(function)


async def shares_wrapper_cancel_request_deposit(
    client: WalletClient,
    shares_wrapper: ChecksumAddress,
    deposit_asset: ChecksumAddress,
) -> TxParams:
    contract = client.contract(shares_wrapper, abis.IGatedRedemptionQueueSharesWrapperLib)
    function = contract.functions.cancelRequestDeposit(deposit_asset)
    return await client.populated_transaction(function)


# --------------------------------------------------------------------------------------------
# SHARES WRAPPER REDEMPTION
# --------------------------------------------------------------------------------------------


async def shares_wrapper_request_redeem(
    client: WalletClient,
    shares_wrapper: ChecksumAddress,
    amount: int,
) -> TxParams:
    contract = client.contract(shares_wrapper, abis.IGatedRedemptionQueueSharesWrapperLib)
    function = contract.functions.requestRedeem(amount)
    return await client.populated_transaction(function)


async def shares_wrapper_cancel_request_redeem(
    client: WalletClient,
    shares_wrapper: ChecksumAddress,
) -> TxParams:
    contract = client.contract(shares_wrapper, abis.IGatedRedemptionQueueSharesWrapperLib)
    function = contract.functions.cancelRequestRedeem()
    return await client.populated_transaction(function)


# --------------------------------------------------------------------------------------------
# SINGLE ASSET REDEMPTION QUEUE
# --------------------------------------------------------------------------------------------


async def redemption_queue_request_redeem(
    client: WalletClient,
    redemption_queue: ChecksumAddress,
    amount: int,
) -> TxParams:
    contract = client.contract(redemption_queue, abis.ISingleAssetRedemptionQueueLib)
    function = contract.functions.requestRedeem(amount)
    return await client.populated_transaction(function)


async def redemption_queue_withdraw_request(
    client: WalletClient,
    redemption_queue: ChecksumAddress,
    request_id: int,
) -> TxParams:
    contract = client.contract(redemption_queue, abis.ISingleAssetRedemptionQueueLib)
    function = contract.functions.withdrawRequest(request_id)
    return await client.populated_transaction(function)


# --------------------------------------------------------------------------------------------
# POLICY CHECK
# --------------------------------------------------------------------------------------------


async def is_allowed_depositor(
    client: PublicClient,
    allowed_deposit_recipients_policy: ChecksumAddress,
    comptroller_proxy: ChecksumAddress,
    policy_manager: ChecksumAddress,
    depositor: ChecksumAddress,
) -> bool:
    has_allowed_depositor_policy = await is_enabled(
        client, allowed_deposit_recipients_policy, policy_manager, comptroller_proxy
    )

    if not has_allowed_depositor_policy:
        return True

    contract = client.contract(
        allowed_deposit_recipients_policy, abis.IAllowedDepositRecipientsPolicy
    )
    function = contract.functions.passesRule(comptroller_proxy, depositor)
    return await function.call()
