from typing import Callable, Any
from web3.constants import ADDRESS_ZERO
from web3.types import ChecksumAddress
from .adapters import get_adapters_for_release
from .assets import Asset, AssetType
from .contracts import is_version, Version, VersionContractNames
from .networks import get_network
from .releases import DeploymentDefinition, Version, Deployment


class Environment:
    def __init__(self, deployment: DeploymentDefinition, version: Version):
        self.deployment = deployment
        self.version = version

        release = deployment["releases"][version]
        if not release:
            raise ValueError(
                f"Invalid release {version} for {deployment['slug']} deployment"
            )

        self.external_contracts = deployment["external_contracts"]
        self.known_address_lists = deployment["known_address_lists"]
        self.known_uint_lists = deployment["known_uint_lists"]

        network = deployment["network"]
        assets = [
            asset for asset in deployment["assets"] if asset["network"] == network
        ]

        self.release = release
        self.contracts = release["contracts"]
        self.network = get_network(network)
        self.assets: dict[ChecksumAddress, Asset] = {
            asset["id"]: asset
            | {"network": network, "registered": release["slug"] in asset["releases"]}
            for asset in assets
        }

        self.named_tokens = self._initialize_named_tokens()
        self.adapters = get_adapters_for_release(self.contracts)

    def _initialize_named_tokens(self) -> dict[str, Asset]:
        if self.is_deployment_arbitrum(self):
            return {
                "bal": self.get_asset_as(
                    self.deployment["named_tokens"]["bal"], "primitive"
                ),
                "comp": self.get_asset_as(
                    self.deployment["named_tokens"]["comp"], "primitive"
                ),
                "crv": self.get_asset_as(
                    self.deployment["named_tokens"]["crv"], "primitive"
                ),
                "cvx": self.get_asset_as(
                    self.deployment["named_tokens"]["cvx"], "primitive"
                ),
                "dai": self.get_asset_as(
                    self.deployment["named_tokens"]["dai"], "primitive"
                ),
                "grt": self.get_asset_as(
                    self.deployment["named_tokens"]["grt"], "primitive"
                ),
                "mln": self.get_asset_as(
                    self.deployment["named_tokens"]["mln"], "primitive"
                ),
                "native_token_wrapper": self.get_asset_as(
                    self.network["currency"]["wrapper"], "primitive"
                ),
                "usdt": self.get_asset_as(
                    self.deployment["named_tokens"]["usdt"], "primitive"
                ),
                "weth": self.get_asset_as(
                    self.deployment["named_tokens"]["weth"], "primitive"
                ),
            }
        elif self.is_deployment_base(self):
            return {
                "comp": self.get_asset_as(
                    self.deployment["named_tokens"]["comp"], "primitive"
                ),
                "dai": self.get_asset_as(
                    self.deployment["named_tokens"]["dai"], "primitive"
                ),
                "mln": self.get_asset_as(
                    self.deployment["named_tokens"]["mln"], "primitive"
                ),
                "native_token_wrapper": self.get_asset_as(
                    self.network["currency"]["wrapper"], "primitive"
                ),
                "usdt": self.get_asset_as(
                    self.deployment["named_tokens"]["usdt"], "primitive"
                ),
                "weth": self.get_asset_as(
                    self.deployment["named_tokens"]["weth"], "primitive"
                ),
            }
        elif self.is_deployment_ethereum(self):
            return {
                "aave": self.get_asset_as(
                    self.deployment["named_tokens"]["aave"], "primitive"
                ),
                "bal": self.get_asset_as(
                    self.deployment["named_tokens"]["bal"], "primitive"
                ),
                "ceth": self.get_asset_as(
                    self.deployment["named_tokens"]["ceth"], "compound_v2"
                ),
                "comp": self.get_asset_as(
                    self.deployment["named_tokens"]["comp"], "primitive"
                ),
                "crv": self.get_asset_as(
                    self.deployment["named_tokens"]["crv"], "primitive"
                ),
                "cvx": self.get_asset_as(
                    self.deployment["named_tokens"]["cvx"], "primitive"
                ),
                "dai": self.get_asset_as(
                    self.deployment["named_tokens"]["dai"], "primitive"
                ),
                "diva": self.get_asset_as(
                    self.deployment["named_tokens"]["diva"], "primitive"
                ),
                "ethx": self.get_asset_as(
                    self.deployment["named_tokens"]["ethx"], "primitive"
                ),
                "grt": self.get_asset_as(
                    self.deployment["named_tokens"]["grt"], "primitive"
                ),
                "idle": self.get_asset_as(
                    self.deployment["named_tokens"]["idle"], "primitive"
                ),
                "lusd": self.get_asset_as(
                    self.deployment["named_tokens"]["lusd"], "primitive"
                ),
                "mln": self.get_asset_as(
                    self.deployment["named_tokens"]["mln"], "primitive"
                ),
                "mpl": self.get_asset_as(
                    self.deployment["named_tokens"]["mpl"], "primitive"
                ),
                "native_token_wrapper": self.get_asset_as(
                    self.network["currency"]["wrapper"], "primitive"
                ),
                "paxg": self.get_asset_as(
                    self.deployment["named_tokens"]["paxg"], "primitive"
                ),
                "ptkn_mln": self.get_asset_as(
                    self.deployment["named_tokens"]["ptkn_mln"], "primitive"
                ),
                "sthoundeth": self.get_asset_as(
                    self.deployment["named_tokens"]["sthoundeth"], "primitive"
                ),
                "stkaave": self.get_asset_as(
                    self.deployment["named_tokens"]["stkaave"], "primitive"
                ),
                "steth": self.get_asset_as(
                    self.deployment["named_tokens"]["steth"], "primitive"
                ),
                "stusd": self.get_asset_as(
                    self.deployment["named_tokens"]["stusd"], "erc_4626"
                ),
                "sweth": self.get_asset_as(
                    self.deployment["named_tokens"]["sweth"], "primitive"
                ),
                "uni": self.get_asset_as(
                    self.deployment["named_tokens"]["uni"], "primitive"
                ),
                "usda": self.get_asset_as(
                    self.deployment["named_tokens"]["usda"], "primitive"
                ),
                "usdc": self.get_asset_as(
                    self.deployment["named_tokens"]["usdc"], "primitive"
                ),
                "usdt": self.get_asset_as(
                    self.deployment["named_tokens"]["usdt"], "primitive"
                ),
                "weth": self.get_asset_as(
                    self.deployment["named_tokens"]["weth"], "primitive"
                ),
            }
        elif self.is_deployment_polygon(self) or self.is_deployment_testnet(self):
            return {
                "aave": self.get_asset_as(
                    self.deployment["named_tokens"]["aave"], "primitive"
                ),
                "bal": self.get_asset_as(
                    self.deployment["named_tokens"]["bal"], "primitive"
                ),
                "comp": self.get_asset_as(
                    self.deployment["named_tokens"]["comp"], "primitive"
                ),
                "crv": self.get_asset_as(
                    self.deployment["named_tokens"]["crv"], "primitive"
                ),
                "cvx": self.get_asset_as(
                    self.deployment["named_tokens"]["cvx"], "primitive"
                ),
                "dai": self.get_asset_as(
                    self.deployment["named_tokens"]["dai"], "primitive"
                ),
                "eure": self.get_asset_as(
                    self.deployment["named_tokens"]["eure"], "primitive"
                ),
                "grt": self.get_asset_as(
                    self.deployment["named_tokens"]["grt"], "primitive"
                ),
                "mln": self.get_asset_as(
                    self.deployment["named_tokens"]["mln"], "primitive"
                ),
                "native_token_wrapper": self.get_asset_as(
                    self.network["currency"]["wrapper"], "primitive"
                ),
                "uni": self.get_asset_as(
                    self.deployment["named_tokens"]["uni"], "primitive"
                ),
                "usdc": self.get_asset_as(
                    self.deployment["named_tokens"]["usdc"], "primitive"
                ),
                "usdt": self.get_asset_as(
                    self.deployment["named_tokens"]["usdt"], "primitive"
                ),
                "weth": self.get_asset_as(
                    self.deployment["named_tokens"]["weth"], "primitive"
                ),
            }
        else:
            raise ValueError("Invalid deployment")

    @staticmethod
    def _create_is_version(version: Version) -> Callable[["Environment"], bool]:
        return lambda env: env.release["version"] == version

    is_sulu = staticmethod(_create_is_version("sulu"))
    is_encore = staticmethod(_create_is_version("encore"))
    is_phoenix = staticmethod(_create_is_version("phoenix"))

    @staticmethod
    def is_version(version: Version, environment: "Environment") -> bool:
        return environment.release["version"] == version

    @staticmethod
    def _create_is_deployment(
        deployment: Deployment,
    ) -> Callable[["Environment"], bool]:
        return lambda env: env.deployment["slug"] == deployment

    is_deployment_arbitrum = staticmethod(_create_is_deployment("arbitrum"))
    is_deployment_base = staticmethod(_create_is_deployment("base"))
    is_deployment_ethereum = staticmethod(_create_is_deployment("ethereum"))
    is_deployment_polygon = staticmethod(_create_is_deployment("polygon"))
    is_deployment_testnet = staticmethod(_create_is_deployment("testnet"))

    @staticmethod
    def is_deployment(deployment: Deployment, environment: "Environment") -> bool:
        return environment.deployment["slug"] == deployment

    def has_asset(self, address: ChecksumAddress) -> bool:
        if address == ADDRESS_ZERO:
            raise ValueError(f"Invalid address {address}")
        return address in self.assets

    def get_asset(self, address: ChecksumAddress) -> Asset:
        if not self.has_asset(address):
            raise ValueError(f"Invalid asset {address}")
        return self.assets[address]

    def get_asset_as(self, address: ChecksumAddress, type_: AssetType) -> Asset:
        if not self.has_asset(address):
            raise ValueError(f"Invalid asset {address}")
        asset = self.assets[address]
        if asset["type"] != type_:
            raise ValueError(
                f"Invalid asset type: Expected {type_} but got {asset['type']}"
            )
        return asset

    def get_assets(
        self, filter_: dict[str, bool | list[AssetType]] | None = None
    ) -> list[Asset]:
        filter_ = filter_ or {}
        types = filter_.get("types", [])
        registered = filter_.get("registered")

        assets = list(self.assets.values())

        if types:
            assets = [a for a in assets if a["type"] in types] if types else []

        if registered is not None:
            assets = [a for a in assets if a["registered"] == registered]

        return sorted(assets, key=lambda x: x["name"])

    def has_contract(self, name: VersionContractNames) -> bool:
        return self.contracts.get(name, ADDRESS_ZERO) != ADDRESS_ZERO

    def get_contract(self, name: VersionContractNames) -> ChecksumAddress:
        if not self.has_contract(name):
            raise ValueError(f"Missing contract {name}")
        return self.contracts[name]

    def __str__(self) -> str:
        return f"{self.deployment['slug']}.{self.version}"

    def to_json(self) -> str:
        return self.__str__()


class EnvironmentGroup:
    def __init__(self, deployment: DeploymentDefinition):
        self.deployment = deployment
        self.network = get_network(deployment["network"])
        self.assets: dict[ChecksumAddress, Asset] = {
            asset["id"]: asset
            for asset in deployment["assets"]
            if asset["network"] == self.network["id"]
        }
        self._environments: dict[Version, Environment] = {}

    def has_environment(self, version_or_address: ChecksumAddress | Version) -> bool:
        if is_version(version_or_address):
            return version_or_address in self.deployment["releases"]
        return any(
            release["address"] == version_or_address
            for release in self.deployment["releases"].values()
        )

    def get_version(self, address: ChecksumAddress) -> Version:
        for release in self.deployment["releases"].values():
            if release["address"] == address:
                return release["version"]
        raise ValueError(f"No release found for address {address}")

    def get_environment(
        self, version_or_address: ChecksumAddress | Version
    ) -> Environment:
        version = (
            version_or_address
            if is_version(version_or_address)
            else self.get_version(version_or_address)
        )

        if version not in self._environments and version in self.deployment["releases"]:
            self._environments[version] = Environment(self.deployment, version)

        if version not in self._environments:
            raise ValueError(
                f"Invalid release {version} for deployment {self.deployment['slug']}"
            )

        return self._environments[version]  # type: ignore

    @property
    def sulu(self) -> Environment:
        return self.get_environment("sulu")

    @property
    def encore(self) -> Environment:
        return self.get_environment("encore")

    @property
    def phoenix(self) -> Environment:
        return self.get_environment("phoenix")
