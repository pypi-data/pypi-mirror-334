from typing import Callable, Any, TypedDict
from web3.types import ChecksumAddress, HexStr, TxParams
from web3.constants import ADDRESS_ZERO
from eth_abi import encode, decode
from web3 import Web3
from ..utils.clients import WalletClient
from ..utils.encoding import encoding_to_types
from .extensions import call_extension


class Action(TypedDict):
    create_external_position: int
    call_on_external_position: int
    remove_external_position: int
    reactivate_external_position: int


ACTION = {
    "create_external_position": 0,
    "call_on_external_position": 1,
    "remove_external_position": 2,
    "reactivate_external_position": 3,
}


class UseParams(TypedDict):
    client: WalletClient
    comptroller_proxy: ChecksumAddress
    external_position_manager: ChecksumAddress
    external_position_proxy: ChecksumAddress
    call_args: dict[str, Any]


def make_use(action: int, encoder: Callable | None = None) -> Callable:
    async def use_external_position(
        client: WalletClient,
        comptroller_proxy: ChecksumAddress,
        external_position_manager: ChecksumAddress,
        external_position_proxy: ChecksumAddress,
        call_args: dict[str, Any],
    ) -> TxParams:
        return await call(
            client,
            comptroller_proxy,
            external_position_manager,
            external_position_proxy,
            action,
            "0x" if encoder is None else encoder(**call_args),
        )

    return use_external_position


class CreateAndUseParams(TypedDict):
    client: WalletClient
    type_id: int
    comptroller_proxy: ChecksumAddress
    external_position_manager: ChecksumAddress
    initialization_data: HexStr
    call_args: dict[str, Any]


def make_create_and_use(action: int, encoder: Callable | None = None) -> Callable:
    async def create_and_use(
        client: WalletClient,
        type_id: int,
        comptroller_proxy: ChecksumAddress,
        external_position_manager: ChecksumAddress,
        initialization_data: HexStr,
        call_args: dict[str, Any],
    ) -> TxParams:
        return await create(
            client,
            type_id,
            comptroller_proxy,
            external_position_manager,
            initialization_data,
            call_encode(
                ADDRESS_ZERO,
                action,
                "0x" if encoder is None else encoder(**call_args),
            ),
        )

    return create_and_use


# --------------------------------------------------------------------------------------------
# CALL ON EXTERNAL POSITION
# --------------------------------------------------------------------------------------------

CALL_ENCODING = [
    {
        "name": "externalPositionProxy",
        "type": "address",
    },
    {
        "name": "actionId",
        "type": "uint256",
    },
    {
        "name": "actionArgs",
        "type": "bytes",
    },
]


class CallArgs(TypedDict):
    external_position_proxy: ChecksumAddress
    action_id: int
    action_args: HexStr | None


def call_encode(
    external_position_proxy: ChecksumAddress,
    action_id: int,
    action_args: HexStr | None = None,
) -> HexStr:
    types = encoding_to_types(CALL_ENCODING)
    values = [
        external_position_proxy,
        action_id,
        Web3.to_bytes(hexstr=action_args or "0x"),
    ]
    return Web3.to_hex(encode(types, values))


def call_decode(encoded: HexStr) -> dict[str, ChecksumAddress | int | HexStr]:
    """
    Returns:
        {
            "external_position_proxy": ChecksumAddress,
            "action_id": int,
            "action_args": HexStr,
        }
    """
    types = encoding_to_types(CALL_ENCODING)
    decoded = decode(types, Web3.to_bytes(hexstr=encoded))
    return {
        "external_position_proxy": Web3.to_checksum_address(decoded[0]),
        "action_id": decoded[1],
        "action_args": Web3.to_hex(decoded[2]),
    }


class CallParams(TypedDict):
    client: WalletClient
    comptroller_proxy: ChecksumAddress
    external_position_manager: ChecksumAddress
    external_position_proxy: ChecksumAddress
    action_id: int
    action_args: HexStr


async def call(
    client: WalletClient,
    comptroller_proxy: ChecksumAddress,
    external_position_manager: ChecksumAddress,
    external_position_proxy: ChecksumAddress,
    action_id: int,
    action_args: HexStr,
) -> TxParams:
    return await call_extension(
        client,
        comptroller_proxy,
        external_position_manager,
        ACTION["call_on_external_position"],
        call_encode(external_position_proxy, action_id, action_args),
    )


# --------------------------------------------------------------------------------------------
# CREATE EXTERNAL POSITION
# --------------------------------------------------------------------------------------------

CREATE_ENCODING = [
    {
        "name": "typeId",
        "type": "uint256",
    },
    {
        "name": "initializationData",
        "type": "bytes",
    },
    {
        "name": "callOnExternalPositionCallArgs",
        "type": "bytes",
    },
]


class CreateArgs(TypedDict):
    type_id: int
    initialization_data: HexStr | None
    call_on_external_position_call_args: HexStr | None


def create_encode(
    type_id: int,
    initialization_data: HexStr | None,
    call_on_external_position_call_args: HexStr | None,
) -> HexStr:
    types = encoding_to_types(CREATE_ENCODING)
    values = [
        type_id,
        Web3.to_bytes(hexstr=initialization_data or "0x"),
        Web3.to_bytes(hexstr=call_on_external_position_call_args or "0x"),
    ]
    return Web3.to_hex(encode(types, values))


def create_decode(encoded: HexStr) -> dict[str, int | HexStr | HexStr]:
    """
    Returns:
        {
            "type_id": int,
            "initialization_data": HexStr,
            "call_on_external_position_call_args": HexStr,
        }
    """
    types = encoding_to_types(CREATE_ENCODING)
    decoded = decode(types, Web3.to_bytes(hexstr=encoded))
    return {
        "type_id": decoded[0],
        "initialization_data": Web3.to_hex(decoded[1]),
        "call_on_external_position_call_args": Web3.to_hex(decoded[2]),
    }


class CreateParams(TypedDict):
    client: WalletClient
    type_id: int
    comptroller_proxy: ChecksumAddress
    external_position_manager: ChecksumAddress
    initialization_data: HexStr | None
    call_args: HexStr | None


async def create(
    client: WalletClient,
    type_id: int,
    comptroller_proxy: ChecksumAddress,
    external_position_manager: ChecksumAddress,
    initialization_data: HexStr | None,
    call_args: HexStr | None,
) -> TxParams:
    return await call_extension(
        client,
        comptroller_proxy,
        external_position_manager,
        ACTION["create_external_position"],
        create_encode(type_id, initialization_data or "0x", call_args or "0x"),
    )


async def create_only(
    client: WalletClient,
    type_id: int,
    comptroller_proxy: ChecksumAddress,
    external_position_manager: ChecksumAddress,
    initialization_data: HexStr | None,
) -> TxParams:
    return await create(*locals().values(), None)


# --------------------------------------------------------------------------------------------
# REACTIVATE EXTERNAL POSITION
# --------------------------------------------------------------------------------------------

REACTIVATE_ENCODING = [
    {
        "name": "externalPosition",
        "type": "address",
    },
]


class ReactivateArgs(TypedDict):
    external_position: ChecksumAddress


def reactivate_encode(external_position: ChecksumAddress) -> HexStr:
    types = encoding_to_types(REACTIVATE_ENCODING)
    values = [external_position]
    return Web3.to_hex(encode(types, values))


def reactivate_decode(encoded: HexStr) -> dict[str, ChecksumAddress]:
    """
    Returns:
        {
            "external_position": ChecksumAddress,
        }
    """
    types = encoding_to_types(REACTIVATE_ENCODING)
    decoded = decode(types, Web3.to_bytes(hexstr=encoded))
    return {
        "external_position": Web3.to_checksum_address(decoded[0]),
    }


class ReactivateParams(TypedDict):
    client: WalletClient
    comptroller_proxy: ChecksumAddress
    external_position_manager: ChecksumAddress
    external_position_proxy: ChecksumAddress


async def reactivate(
    client: WalletClient,
    comptroller_proxy: ChecksumAddress,
    external_position_manager: ChecksumAddress,
    external_position_proxy: ChecksumAddress,
) -> TxParams:
    return await call_extension(
        client,
        comptroller_proxy,
        external_position_manager,
        ACTION["reactivate_external_position"],
        reactivate_encode(external_position_proxy),
    )


# --------------------------------------------------------------------------------------------
# REMOVE EXTERNAL POSITION
# --------------------------------------------------------------------------------------------

REMOVE_ENCODING = [
    {
        "name": "externalPositionProxy",
        "type": "address",
    },
]


class RemoveArgs(TypedDict):
    external_position_proxy: ChecksumAddress


def remove_encode(external_position_proxy: ChecksumAddress) -> HexStr:
    types = encoding_to_types(REMOVE_ENCODING)
    values = [external_position_proxy]
    return Web3.to_hex(encode(types, values))


def remove_decode(encoded: HexStr) -> dict[str, ChecksumAddress]:
    """
    Returns:
        {
            "external_position_proxy": ChecksumAddress,
        }
    """
    types = encoding_to_types(REMOVE_ENCODING)
    decoded = decode(types, Web3.to_bytes(hexstr=encoded))
    return {
        "external_position_proxy": Web3.to_checksum_address(decoded[0]),
    }


class RemoveParams(TypedDict):
    client: WalletClient
    comptroller_proxy: ChecksumAddress
    external_position_manager: ChecksumAddress
    external_position_proxy: ChecksumAddress


async def remove(
    client: WalletClient,
    comptroller_proxy: ChecksumAddress,
    external_position_manager: ChecksumAddress,
    external_position_proxy: ChecksumAddress,
) -> TxParams:
    return await call_extension(
        client,
        comptroller_proxy,
        external_position_manager,
        ACTION["remove_external_position"],
        remove_encode(external_position_proxy),
    )
