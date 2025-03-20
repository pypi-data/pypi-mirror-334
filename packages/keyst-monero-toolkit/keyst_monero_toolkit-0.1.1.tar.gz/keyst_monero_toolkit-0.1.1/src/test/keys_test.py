import pytest
from bip_utils import Bip32Slip10Secp256k1, Bip39SeedGenerator
from bip_utils.monero.monero_keys import MoneroPrivateKey

from keyst_monero_toolkit import KeyPair, hash_to_scalar, reduce_scalar

TEST_DATA = [
    {
        "bip39_mnemonic": "key stone key stone key stone key stone key stone key stone key stone success",
        "bip39_seed": "45a5056acbe881d7a5f2996558b303e08b4ad1daffacf6ffb757ff2a9705e6b9f806cffe3bd90ff8e3f8e8b629d9af78bcd2ed23e8c711f238308e65b62aa5f0",
        "monero_derivation_path": "m/44'/128'/0'/0/0",
        "derivation_seed": "66ec3ba491849c927c9be0bd8387b0a7215c61c69854d53f6585630d4557e752",
        "monero_mnemonic": "unsafe gables auburn amidst syllabus sayings oval sowed utopia tiger certain iceberg meeting ridges neon irony ticket eluded hedgehog acoustic ginger across organs poverty acoustic",
        "spend_keys": "6c3895c1dfd7c3ed22be481ed5ec7f40e3d8ded84f0a3d65a542915475ca6f0e",
        "view_keys": "17921dbd51b4a1af0b4049bc13dc7048ace1dcd8be9b8669de95b8430924ea09",
    },
    {
        "bip39_mnemonic": "pact receive skate vague shoot door build much manual leisure angry patch",
        "bip39_seed": "a5bc2460d3d62fb44a9d192935d4bbd823bd922a913f7dbbe0094ca1400f9685f4c389705090990f5ad68f61cfa9c0883da1adeb5182d1a81d5d22a792d59294",
        "monero_derivation_path": "m/44'/128'/0'/0/0",
        "derivation_seed": "0ba75e022a5af8467fe1179b5eae509b860854bbc8bd55b32b6c0662aecead52",
        "monero_mnemonic": "july elite zesty zebra lymph guide update water earth doorway fowls cadets ionic onslaught total muffin irritate were empty oozed pulp eels quick rowboat fowls",
        "spend_keys": "d8e589c0c251a9d7ac08fa45c7cc99d42cc06d41f094578abeb805122af0f10a",
        "view_keys": "3d105f97f1ed913d94da768c296b205d702fc4d35cd80fb15a9af30a40345307",
        "major": 0,
    },
]


@pytest.mark.parametrize("data", TEST_DATA)
def test_reduce_scalar(data):
    def my_reduce_scalar(b: bytes) -> bytes:
        if len(b) != 32:
            raise ValueError("Invalid length")
        # 扩展到64字节：后面补32个零字节
        padded = b + bytes(32)
        # 将64字节按小端字节序转换成整数
        num = int.from_bytes(padded, byteorder="little")
        # Ed25519 标量域的阶
        L = 2**252 + 27742317777372353535851937790883648493
        # 取模
        reduced = num % L
        # 转换回32字节的小端表示
        return reduced.to_bytes(32, byteorder="little")

    b = bytes.fromhex(data["derivation_seed"])
    assert reduce_scalar(b) == my_reduce_scalar(b)


@pytest.mark.parametrize("data", TEST_DATA)
def test_mnemonic_to_seed(data):
    # 使用测试数据中的 mnemonic 与预期生成的 seed_hex 对比
    mnemonic = data["bip39_mnemonic"]
    expected_seed_hex = data["bip39_seed"]

    seed = Bip39SeedGenerator(mnemonic).Generate()
    generated_seed_hex = seed.hex()

    assert generated_seed_hex == expected_seed_hex


@pytest.mark.parametrize("data", TEST_DATA)
def test_bip32_derive_key(data):
    # 使用测试数据中的 bip39_seed、monero_derivation_path 与 derivation_seed 进行对比
    seed_hex = data["bip39_seed"]
    seed = bytes.fromhex(seed_hex)
    derivation_path = data["monero_derivation_path"]

    bip32_ctx = Bip32Slip10Secp256k1.FromSeed(seed)
    child_ctx = bip32_ctx.DerivePath(derivation_path)
    derived_priv_key = child_ctx.PrivateKey().Raw().ToHex()

    expected_priv_key = data["derivation_seed"]
    assert derived_priv_key == expected_priv_key


@pytest.mark.parametrize("data", TEST_DATA)
def test_hash_to_scalar(data):
    data_bytes = bytes.fromhex(data["derivation_seed"])
    assert hash_to_scalar(data_bytes).hex() == data["spend_keys"]


@pytest.mark.parametrize("data", TEST_DATA)
def test_from_derivation_private_key(data):
    raw_private_key_hex = data["derivation_seed"]
    kp = KeyPair.from_derivation_private_key(bytes.fromhex(raw_private_key_hex))
    assert kp.spend.Raw().ToHex() == data["spend_keys"]
    assert kp.view.Raw().ToHex() == data["view_keys"]


@pytest.mark.parametrize("data", TEST_DATA)
def test_from_bip39_mnemonic(data):
    mnemonic = data["bip39_mnemonic"]
    kp = KeyPair.from_bip39_mnemonic(mnemonic)
    assert kp.bip39_mnemonic == mnemonic
    assert kp.bip39_seed.hex() == data["bip39_seed"]
    assert kp.spend.Raw().ToHex() == data["spend_keys"]
    assert kp.view.Raw().ToHex() == data["view_keys"]


@pytest.mark.parametrize("data", TEST_DATA)
def test_from_bip39_seed(data):
    seed = bytes.fromhex(data["bip39_seed"])
    kp = KeyPair.from_bip39_seed(seed)
    assert kp.bip39_seed.hex() == data["bip39_seed"]
    assert kp.spend.Raw().ToHex() == data["spend_keys"]
    assert kp.view.Raw().ToHex() == data["view_keys"]
    assert kp.major == data.get("major", 0)


@pytest.mark.parametrize("data", TEST_DATA)
def test_spendkey_to_mnemonic(data):
    kp = KeyPair(None, None)
    kp.spend = MoneroPrivateKey.FromBytes(bytes.fromhex(data["spend_keys"]))
    assert kp._spendkey_to_mnemonic() == data["monero_mnemonic"]
