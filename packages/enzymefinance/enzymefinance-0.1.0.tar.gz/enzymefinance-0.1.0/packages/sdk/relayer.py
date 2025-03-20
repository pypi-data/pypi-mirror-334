from typing import TypedDict
from web3 import Web3
from web3.types import ChecksumAddress, TxParams, HexStr
from web3.constants import ADDRESS_ZERO
from .utils.clients import PublicClient, WalletClient
from ..abis import abis


RELAY_HUB_ABI = [
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "maxAcceptanceBudget",
                "type": "uint256",
            },
            {
                "components": [
                    {
                        "components": [
                            {
                                "internalType": "address",
                                "name": "from",
                                "type": "address",
                            },
                            {
                                "internalType": "address",
                                "name": "to",
                                "type": "address",
                            },
                            {
                                "internalType": "uint256",
                                "name": "value",
                                "type": "uint256",
                            },
                            {
                                "internalType": "uint256",
                                "name": "gas",
                                "type": "uint256",
                            },
                            {
                                "internalType": "uint256",
                                "name": "nonce",
                                "type": "uint256",
                            },
                            {"internalType": "bytes", "name": "data", "type": "bytes"},
                            {
                                "internalType": "uint256",
                                "name": "validUntil",
                                "type": "uint256",
                            },
                        ],
                        "internalType": "struct IForwarder.ForwardRequest",
                        "name": "request",
                        "type": "tuple",
                    },
                    {
                        "components": [
                            {
                                "internalType": "uint256",
                                "name": "gasPrice",
                                "type": "uint256",
                            },
                            {
                                "internalType": "uint256",
                                "name": "pctRelayFee",
                                "type": "uint256",
                            },
                            {
                                "internalType": "uint256",
                                "name": "baseRelayFee",
                                "type": "uint256",
                            },
                            {
                                "internalType": "address",
                                "name": "relayWorker",
                                "type": "address",
                            },
                            {
                                "internalType": "address",
                                "name": "paymaster",
                                "type": "address",
                            },
                            {
                                "internalType": "address",
                                "name": "forwarder",
                                "type": "address",
                            },
                            {
                                "internalType": "bytes",
                                "name": "paymasterData",
                                "type": "bytes",
                            },
                            {
                                "internalType": "uint256",
                                "name": "clientId",
                                "type": "uint256",
                            },
                        ],
                        "internalType": "struct GsnTypes.RelayData",
                        "name": "relayData",
                        "type": "tuple",
                    },
                ],
                "internalType": "struct GsnTypes.RelayRequest",
                "name": "relayRequest",
                "type": "tuple",
            },
            {"internalType": "bytes", "name": "signature", "type": "bytes"},
            {"internalType": "bytes", "name": "approvalData", "type": "bytes"},
            {"internalType": "uint256", "name": "externalGasLimit", "type": "uint256"},
        ],
        "name": "relayCall",
        "outputs": [
            {"internalType": "bool", "name": "paymasterAccepted", "type": "bool"},
            {"internalType": "bytes", "name": "returnValue", "type": "bytes"},
        ],
        "stateMutability": "nonpayable",
        "type": "function",
    },
]

RELAY_REQUEST_TYPES = {
    "RelayData": [
        {"name": "gasPrice", "type": "uint256"},
        {"name": "pctRelayFee", "type": "uint256"},
        {"name": "baseRelayFee", "type": "uint256"},
        {"name": "relayWorker", "type": "address"},
        {"name": "paymaster", "type": "address"},
        {"name": "forwarder", "type": "address"},
        {"name": "paymasterData", "type": "bytes"},
        {"name": "clientId", "type": "uint256"},
    ],
    "RelayRequest": [
        {"name": "from", "type": "address"},
        {"name": "to", "type": "address"},
        {"name": "value", "type": "uint256"},
        {"name": "gas", "type": "uint256"},
        {"name": "nonce", "type": "uint256"},
        {"name": "data", "type": "bytes"},
        {"name": "validUntil", "type": "uint256"},
        {"name": "relayData", "type": "RelayData"},
    ],
}


# --------------------------------------------------------------------------------------------
# TRANSACTIONS
# --------------------------------------------------------------------------------------------


async def deploy_gas_relay_paymaster(
    client: WalletClient,
    comptroller_proxy: ChecksumAddress,
) -> TxParams:
    contract = client.contract(comptroller_proxy, abis.IComptrollerLib)
    function = contract.functions.deployGasRelayPaymaster()
    return await client.populated_transaction(function)


async def deposit_to_gas_relay_paymaster(
    client: WalletClient,
    comptroller_proxy: ChecksumAddress,
) -> TxParams:
    contract = client.contract(comptroller_proxy, abis.IComptrollerLib)
    function = contract.functions.depositToGasRelayPaymaster()
    return await client.populated_transaction(function)


async def shutdown_gas_relay_paymaster(
    client: WalletClient,
    comptroller_proxy: ChecksumAddress,
) -> TxParams:
    contract = client.contract(comptroller_proxy, abis.IComptrollerLib)
    function = contract.functions.shutdownGasRelayPaymaster()
    return await client.populated_transaction(function)


# --------------------------------------------------------------------------------------------
# READ FUNCTIONS
# --------------------------------------------------------------------------------------------


async def is_relayer_enabled(
    client: PublicClient,
    comptroller_proxy: ChecksumAddress,
) -> bool:
    contract = client.contract(comptroller_proxy, abis.IComptrollerLib)
    function = contract.functions.getGasRelayPaymaster()
    gas_relay_paymaster_address = await function.call()
    return gas_relay_paymaster_address != ADDRESS_ZERO


async def get_gas_relay_paymaster(
    client: PublicClient,
    comptroller_proxy: ChecksumAddress,
) -> ChecksumAddress:
    contract = client.contract(comptroller_proxy, abis.IComptrollerLib)
    function = contract.functions.getGasRelayPaymaster()
    return await function.call()


async def get_relayer_balance(
    client: PublicClient,
    gas_relay_paymaster: ChecksumAddress,
) -> int:
    contract = client.contract(gas_relay_paymaster, abis.IGasRelayPaymasterLib)
    function = contract.functions.getRelayHubDeposit()
    return await function.call()


async def get_trusted_forwarder(
    client: PublicClient,
    gas_relay_paymaster: ChecksumAddress,
) -> ChecksumAddress:
    contract = client.contract(gas_relay_paymaster, abis.IGasRelayPaymasterLib)
    function = contract.functions.trustedForwarder()
    return await function.call()


async def get_nonce(
    client: PublicClient,
    trusted_forwarder: ChecksumAddress,
    sender: ChecksumAddress,
) -> int:
    contract = client.contract(trusted_forwarder, abis.IForwarder)
    function = contract.functions.getNonce(sender)
    return await function.call()


class Request(TypedDict):
    from_: ChecksumAddress
    to: ChecksumAddress
    value: int
    gas: int
    nonce: int
    data: HexStr
    validUntil: int


class RelayData(TypedDict):
    gasPrice: int
    pctRelayFee: int
    baseRelayFee: int
    relayWorker: ChecksumAddress
    paymaster: ChecksumAddress
    forwarder: ChecksumAddress
    paymasterData: HexStr
    clientId: int


class RelayRequest(TypedDict):
    request: Request
    relayData: RelayData


def encode_relay_call_data(
    max_acceptance_budget: int,
    relay_request: RelayRequest,
    signature: HexStr,
    approval_data: HexStr,
    gas_limit: int,
) -> HexStr:
    """
    Args:
        relay_request:
            {
                "request": {
                    "from": ChecksumAddress,
                    "to": ChecksumAddress,
                    "value": int,
                    "gas": int,
                    "nonce": int,
                    "data": HexStr,
                    "validUntil": int,
                },
                "relayData": {
                    "gasPrice": int,
                    "pctRelayFee": int,
                    "baseRelayFee": int,
                    "relayWorker": ChecksumAddress,
                    "paymaster": ChecksumAddress,
                    "forwarder": ChecksumAddress,
                    "paymasterData": HexStr,
                }
            }
    """
    contract = Web3().eth.contract(abi=RELAY_HUB_ABI)
    return contract.encode_abi(
        "relayCall",
        [
            max_acceptance_budget,
            relay_request,
            signature,
            approval_data,
            gas_limit,
        ],
    )
