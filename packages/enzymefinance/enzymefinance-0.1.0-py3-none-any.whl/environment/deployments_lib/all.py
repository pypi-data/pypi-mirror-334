from web3 import Web3
from web3.constants import ADDRESS_ZERO
from eth_typing import ChecksumAddress
from ..contracts import Version, is_version
from ..environment import Environment, EnvironmentGroup
from ..releases import Deployment, Release, is_deployment
from ..networks import Network, NetworkSlug, get_network, is_network_identifier
from .arbitrum import DEPLOYMENT as ARBITRUM
from .base import DEPLOYMENT as BASE
from .ethereum import DEPLOYMENT as ETHEREUM
from .polygon import DEPLOYMENT as POLYGON
from .testnet import DEPLOYMENT as TESTNET


DEPLOYMENTS = {
    "arbitrum": ARBITRUM,
    "base": BASE,
    "ethereum": ETHEREUM,
    "polygon": POLYGON,
    "testnet": TESTNET,
}


def get_environment_group(deployment: Deployment) -> EnvironmentGroup:
    return EnvironmentGroup(DEPLOYMENTS[deployment])


def get_environment_for_release(release: Release) -> Environment:
    deployment, version = release.split(".")
    if is_deployment(deployment) and is_version(version):
        return get_environment(deployment, version)
    raise ValueError(f"Unknown release {release}")


def get_environment(
    deployment_or_network: Deployment | Network | NetworkSlug,
    version_or_address: Version | ChecksumAddress,
) -> Environment:
    if is_deployment(deployment_or_network):
        deployment = DEPLOYMENTS[deployment_or_network]
    elif is_network_identifier(deployment_or_network):
        network = get_network(deployment_or_network)
        deployment = next(
            (
                deployment
                for deployment in DEPLOYMENTS.values()
                if deployment["kind"] == "live"
                and deployment["network"] == network["id"]
            ),
            None,
        )

        if deployment is None:
            raise ValueError(f"Failed to find deployment for network {network['slug']}")

    else:
        raise ValueError(f"Failed to find deployment {deployment_or_network}")

    if is_version(version_or_address):
        release = deployment["releases"].get(version_or_address)

        if release is not None:
            return Environment(deployment, release["version"])
    elif (
        Web3.is_checksum_address(version_or_address)
        and version_or_address != ADDRESS_ZERO
    ):
        release = next(
            (
                release
                for release in deployment["releases"].values()
                if release["address"] == version_or_address
            ),
            None,
        )
        if release is not None:
            return Environment(deployment, release["version"])

    raise ValueError(
        f"Failed to find {version_or_address} release on deployment {deployment['slug']}"
    )
