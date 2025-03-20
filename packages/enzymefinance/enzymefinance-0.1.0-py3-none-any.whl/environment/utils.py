from .networks import Network, NetworkSlug, is_network_identifier, get_network
from .releases import Deployment, is_deployment
from .deployments_lib.all import DEPLOYMENTS


def get_deployment(
    deployment_or_network: Deployment | Network | NetworkSlug,
) -> Deployment:
    if is_deployment(deployment_or_network):
        return DEPLOYMENTS[deployment_or_network]
    if is_network_identifier(deployment_or_network):
        network = get_network(deployment_or_network)
        for deployment in DEPLOYMENTS.values():
            if deployment["network"] == network["id"] and deployment["kind"] == "live":
                return deployment
        raise ValueError(f"Missing deployment for network {network['slug']}")
    raise ValueError(f"Invalid deployment or network {deployment_or_network}")
