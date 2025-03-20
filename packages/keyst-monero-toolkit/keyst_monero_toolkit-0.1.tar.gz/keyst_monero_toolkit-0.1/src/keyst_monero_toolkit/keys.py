"""Implementation of algorithms and KeyPair class."""

import json

from bip_utils import Bip32Slip10Secp256k1, Bip39SeedGenerator
from bip_utils.monero import mnemonic
from bip_utils.monero.monero_keys import MoneroPrivateKey
from Crypto.Hash import keccak
from nacl.bindings import (
    crypto_core_ed25519_scalar_reduce,
)


def keccak256(data: bytes) -> bytes:
    k = keccak.new(digest_bits=256)
    k.update(data)
    return k.digest()


def reduce_scalar(b: bytes) -> bytes:
    assert len(b) == 32, "Invalid length"
    padded = b + bytes(32)  # 扩展到64字节
    return crypto_core_ed25519_scalar_reduce(padded)


def hash_to_scalar(data: bytes) -> bytes:
    return reduce_scalar(keccak256(data))


class KeyPair:
    """
    A class to represent a Monero key pair and the mapping with BIP39.

    Attributes:
    -----------
    spend : MoneroPrivateKey
        The private spend key.
    view : MoneroPrivateKey
        The private view key.
    monero_mnemonic : str
        The Monero mnemonic representation of the spend key.
    bip39_mnemonic : str
        The BIP39 mnemonic.
    bip39_seed : bytes
        The BIP39 seed.
    drivation_path : str
        The derivation path used to generate the keys.
    derivation_seed : bytes
        The seed used for derivation.
    major : int
        The major version used for derivation.

    Methods:
    --------
    _to_dict():
        Returns a dictionary representation of the key pair.
    __repr__():
        Returns a JSON string representation of the key pair.
    from_derivation_private_key(raw_private_key: bytes) -> "KeyPair":
        Creates a KeyPair instance from a raw private key.
    from_bip39_mnemonic(bip39_mnemonic: str) -> "KeyPair":
        Creates a KeyPair instance from a BIP39 mnemonic.
    from_bip39_seed(seed: bytes, major: int = 0) -> "KeyPair":
        Creates a KeyPair instance from a BIP39 seed.
    _spendkey_to_words_list():
        Converts the spend key to a list of mnemonic words.
    _spendkey_to_mnemonic():
        Converts the spend key to a mnemonic string.
    """

    def __init__(self, spend: MoneroPrivateKey, view: MoneroPrivateKey):
        self.spend: MoneroPrivateKey = spend
        self.view: MoneroPrivateKey = view
        self.monero_mnemonic: str = ""
        # ---
        self.bip39_mnemonic: str = ""
        self.bip39_seed: bytes = None
        self.drivation_path: str = ""
        self.derivation_seed: bytes = None

        self.major: int = 0

    def _to_dict(self):
        return {
            "bip39_mnemonic": self.bip39_mnemonic,
            "bip39_seed": self.bip39_seed.hex() if self.bip39_seed else None,
            "monero_derivation_path": self.drivation_path,
            "derivation_seed": self.derivation_seed.hex()
            if self.derivation_seed
            else None,
            "monero_mnemonic": self.monero_mnemonic,
            "spend_keys": self.spend.Raw().ToHex(),
            "view_keys": self.view.Raw().ToHex(),
            "major": self.major,
        }

    def __repr__(self):
        return str(json.dumps(self._to_dict(), indent=4))

    @classmethod
    def from_derivation_private_key(cls, raw_private_key: bytes) -> "KeyPair":
        secret_spend = hash_to_scalar(raw_private_key)
        view_key = hash_to_scalar(secret_spend)
        kp = cls(
            MoneroPrivateKey.FromBytes(secret_spend),
            MoneroPrivateKey.FromBytes(view_key),
        )
        kp.derivation_seed = raw_private_key
        kp._spendkey_to_mnemonic()
        return kp

    @classmethod
    def from_bip39_mnemonic(cls, bip39_mnemonic: str) -> "KeyPair":
        seed = Bip39SeedGenerator(bip39_mnemonic).Generate()

        kp = cls.from_bip39_seed(seed)
        kp.bip39_mnemonic = bip39_mnemonic

        return kp

    @classmethod
    def from_bip39_seed(cls, seed: bytes, major: int = 0) -> "KeyPair":
        """
        警告: major 参数仅用于测试，不应在生产环境中使用, KeyStone 生成的地址为 major = 0
        WARNING: major parameter is only for testing, should not be used in production,
                 KeyStone generated address is major = 0
        """
        assert 0 <= major < 2**31, "Invalid major"
        derivation_path = f"m/44'/128'/{major}'/0/0"

        bip32_ctx = Bip32Slip10Secp256k1.FromSeed(seed)
        child_ctx = bip32_ctx.DerivePath(derivation_path)
        derivation_private_key = child_ctx.PrivateKey().Raw().ToBytes()

        kp = cls.from_derivation_private_key(derivation_private_key)
        kp.bip39_seed = seed
        kp.drivation_path = derivation_path
        kp.major = major

        return kp

    def _spendkey_to_words_list(self):
        seed = self.spend.Raw().ToBytes()
        lang = mnemonic.MoneroLanguages.ENGLISH
        encoder = mnemonic.MoneroMnemonicWithChecksumEncoder(lang)
        return encoder.Encode(seed).ToList()

    def _spendkey_to_mnemonic(self):
        self.monero_mnemonic = " ".join(self._spendkey_to_words_list())
        return self.monero_mnemonic
