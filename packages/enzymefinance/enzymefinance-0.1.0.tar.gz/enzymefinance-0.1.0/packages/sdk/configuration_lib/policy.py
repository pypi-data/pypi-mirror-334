from web3.types import ChecksumAddress
from ..configuration import get_enabled_policies
from ..utils.clients import PublicClient


async def is_enabled(
    client: PublicClient,
    policy: ChecksumAddress,
    policy_manager: ChecksumAddress,
    comptroller_proxy: ChecksumAddress,
) -> bool:
    enabled_policies = await get_enabled_policies(
        client, policy_manager, comptroller_proxy
    )
    return policy in enabled_policies
