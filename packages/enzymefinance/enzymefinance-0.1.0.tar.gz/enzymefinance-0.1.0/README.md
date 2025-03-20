# Enzyme Python SDK

[![License: MIT](https://img.shields.io/github/license/enzymefinance/sdk)](/LICENSE)

This is a work in progress. Your mileage may vary.


## Installation

```bash
pip install enzymefinance
```

## Getting started

We are currently in the process of writing thorough documentation & tutorials. In the meantime, here there are some quick start examples.

### Reading Vault info

```python
import asyncio
from enzymefinance.sdk import vault
from enzymefinance.sdk.utils.clients import PublicClient

async def main():
    client = PublicClient(<RPC_URL>)
    name = await vault.get_name(
        client=client,
        vault_proxy=<VAULT_ADDRESS>,
    )
    print(name)

asyncio.run(main())
```

- `<RPC_URL>`: The RPC URL of the network you want to connect to.
- `<VAULT_ADDRESS>`: The **checksum** address of the vault you want to read.

### Writing Vault info

```python
import asyncio
from enzymefinance.sdk import vault
from enzymefinance.sdk.utils.clients import WalletClient

async def main():
    client = WalletClient(<RPC_URL>, <PRIVATE_KEY>)
    tx_params = await vault.set_name(
        client=client,
        vault_proxy=<VAULT_ADDRESS>,
        name="My new vault",
    )
    tx_hash = await client.send_transaction(tx_params)
    print(tx_hash)

asyncio.run(main())
```

- `<RPC_URL>`: The RPC URL of the network you want to connect to.
- `<VAULT_ADDRESS>`: The **checksum** address of the vault you want to read.
- `<PRIVATE_KEY>`: The private key of the account you want to use to send the transaction.

### Get environment info

```python
from enzymefinance.environment import get_deployment

get_deployment("arbitrum")
```

### Get one specific abi

```python
from enzymefinance.abis import abis

abis.IVaultLib
```

## Community

Check out the following places for support, discussions & feedback:

- Join our [Discord server](https://discord.enzyme.finance)
- Join our [Telegram group](https://telegram.enzyme.finance)
- Join the [Discussions on GitHub](https://github.com/enzymefinance/sdk/discussions)

## Authors

- [@guillemap](https://github.com/guillemap)

## License

[MIT](/LICENSE) License
