"""Main module for the Monero Toolkit CLI."""

import click
import pytest

from .keys import KeyPair


@click.command()
@click.option("-s", "--seed", is_flag=True, help="Select seed mode")
@click.option("-m", "--mnemonic", is_flag=True, help="Select mnemonic mode")
@click.argument("values", nargs=-1)
def cli(seed, mnemonic, values):
    """Monero Toolkit CLI. Parsed arguments by Click."""
    # Check
    if seed == mnemonic:  # either both True or both False
        raise click.BadParameter("Exactly one tag must be provided: -s or -m")

    # Ensure that argument values are provided
    if not values:
        raise click.BadParameter("Corresponding parameter values must be provided")

    if seed:
        if len(values) != 1:
            raise click.BadParameter(
                "When using -s, only one seed parameter is allowed"
            )
        click.echo("Using bip39 seed:")
        kp = KeyPair.from_bip39_seed(bytes.fromhex(values[0]), 0)
        click.echo(message=kp)
    else:
        words = []
        for word in values:
            words.extend(word.split())
        click.echo("Using bip39 mnemonic: ")
        kp = KeyPair.from_bip39_mnemonic(" ".join(words))
        click.echo(message=kp)


def main():
    """Entry point"""
    pytest.main(["-q"])
    cli()  # pylint: disable=no-value-for-parameter
