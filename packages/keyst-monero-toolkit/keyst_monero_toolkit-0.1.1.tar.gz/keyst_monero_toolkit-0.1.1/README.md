# Keystone3 Monero Key Toolkit

## Introduction

The Keystone3 Monero Key Toolkit is a tool designed for Keystone3 hardware wallet users to convert standard BIP39 mnemonics into the 25-word Monero mnemonic.

This tool is designed to provide a way to recover and transfer Monero assets in the event that the hardware wallet is damaged, lost or stolen.

## Usage example

```bash
pip install keyst-monero-toolkit
```

```bash
# bip39 mnemonic
keyst-monero-toolkit -m key stone key stone key stone key stone key stone key stone key stone success

# bip39 seed
keyst-monero-toolkit -s 45a5056acbe881d7a5f2996558b303e08b4ad1daffacf6ffb757ff2a9705e6b9f806cffe3bd90ff8e3f8e8b629d9af78bcd2ed23e8c711f238308e65b62aa5f0
```

output exmaple:

```json
{
    "bip39_mnemonic": "key stone key stone key stone key stone key stone key stone key stone success",
    "bip39_seed": "45a5056acbe881d7a5f2996558b303e08b4ad1daffacf6ffb757ff2a9705e6b9f806cffe3bd90ff8e3f8e8b629d9af78bcd2ed23e8c711f238308e65b62aa5f0",
    "monero_derivation_path": "m/44'/128'/0'/0/0",
    "derivation_seed": "66ec3ba491849c927c9be0bd8387b0a7215c61c69854d53f6585630d4557e752",
    "monero_mnemonic": "unsafe gables auburn amidst syllabus sayings oval sowed utopia tiger certain iceberg meeting ridges neon irony ticket eluded hedgehog acoustic ginger across organs poverty acoustic",
    "spend_keys": "6c3895c1dfd7c3ed22be481ed5ec7f40e3d8ded84f0a3d65a542915475ca6f0e",
    "view_keys": "17921dbd51b4a1af0b4049bc13dc7048ace1dcd8be9b8669de95b8430924ea09",
    "major": 0
}
```

### Example of Python code usage

```python
from keyst_monero_toolkit import KeyPair

bip39_mnemonic = "key stone key stone key stone key stone key stone key stone key stone success"
key_pair = KeyPair.from_bip39_mnemonic(bip39_mnemonic)

monero_mnemonic = key_pair.monero_mnemonic
print(f"Monero mnemonic: {monero_mnemonic}")
# Monero mnemonic: unsafe gables auburn amidst syllabus sayings oval sowed utopia tiger certain iceberg meeting ridges neon irony ticket eluded hedgehog acoustic ginger across organs poverty acoustic

spend_key = key_pair.spend.Raw().ToHex()
print(f"Monero spend_key: {spend_key}")
# Monero spend_key: 6c3895c1dfd7c3ed22be481ed5ec7f40e3d8ded84f0a3d65a542915475ca6f0e

view_key = key_pair.view.Raw().ToHex()
print(f"Monero view_key: {view_key}")
# Monero view_key: 17921dbd51b4a1af0b4049bc13dc7048ace1dcd8be9b8669de95b8430924ea09
```

## Disclaimer

This tool is only for educational or emergency recovery purposes. 

**User should use it at his/her own risk and the developer is not responsible for any loss of assets**.



