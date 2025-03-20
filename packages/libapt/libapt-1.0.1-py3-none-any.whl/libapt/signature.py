"""
Processing of APT Release signature.
"""

import tempfile
import logging
import warnings

from pathlib import Path

from pgpy import PGPMessage, PGPKey, PGPUID
from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm, SymmetricKeyAlgorithm, CompressionAlgorithm


class InvalidSignature(Exception):
    """Raised if there is an issue with the InRelease signature verification."""


def strip_signature(content: str) -> str:
    """
    Strip signature form InRelease content.

    :param content: Content lines of the InRelease file.
    :return: Content without signature wrapping.
    """
    message = PGPMessage.from_blob(content)
    return message.message


def verify_signature(content: str, key: Path) -> str:
    """
    Verify the signature of the InRelease file.

    :param content: Content lines of the InRelease file.
    :param key: Path to the GPG public key file.
    :return: Content without signature wrapping.
    :raises InvalidSignature: Raises an InvalidSignature exception if signature check fails.
    """
    logging.debug("Loading InRelease signing key from: %s", key)
    pub_key, _ = PGPKey.from_file(key)
    logging.debug("Loaded key fingerprint: %s", pub_key.fingerprint)

    message = PGPMessage.from_blob(content)
    logging.debug("Message is signed by: %s", message.signers)

    try:
        with warnings.catch_warnings(action="ignore"):
            result = pub_key.verify(message)
    except Exception as e:
        raise InvalidSignature(e)

    if result:
        logging.debug("Signature check was successful.")
        return message.message
    else:
        raise InvalidSignature("Signature check failed! %s", result)


def generate_key(owner: str, owner_mail: str, folder: Path | None = None) -> tuple[Path, Path]:
    """
    Generate a GPG key pair.

    :param folder: Directory where to put the generated keys.
    :param owner: Name of the key owner.
    :param owner_mail: Email address of the key owner.
    :returns: Tuple of private key and public key.
    """
    key = PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 4096)
    uid = PGPUID.new(owner, comment="", email=owner_mail)
    key.add_uid(
        uid,
        usage={KeyFlags.Sign, KeyFlags.EncryptCommunications, KeyFlags.EncryptStorage},
        hashes=[HashAlgorithm.SHA256, HashAlgorithm.SHA384, HashAlgorithm.SHA512, HashAlgorithm.SHA224],
        ciphers=[SymmetricKeyAlgorithm.AES256, SymmetricKeyAlgorithm.AES192, SymmetricKeyAlgorithm.AES128],
        compression=[
            CompressionAlgorithm.ZLIB,
            CompressionAlgorithm.BZ2,
            CompressionAlgorithm.ZIP,
            CompressionAlgorithm.Uncompressed,
        ],
    )

    if folder is None:
        folder = Path(tempfile.mkdtemp())

    priv_key = folder / "private_key"
    with open(priv_key, "w", encoding="utf-8") as f:
        f.write(str(key))

    pub_key = folder / "public_key"
    with open(pub_key, "w", encoding="utf-8") as f:
        f.write(str(key.pubkey))

    return (priv_key, pub_key)


def sign_content(content: str, private_key: Path) -> str:
    """
    Sign a message using the given private key.

    :param content: Content to sign.
    :param private_key: Path to the GPG private key file.
    :returns: Content with signature wrapping or non in case of errors.
    """
    logging.debug("Loading signing key from: %s", private_key)
    priv_key, _ = PGPKey.from_file(private_key)
    logging.debug("Loaded key fingerprint: %s", priv_key.fingerprint)

    message = PGPMessage.new(content, cleartext=True)
    with warnings.catch_warnings(action="ignore"):
        message |= priv_key.sign(message)

    logging.debug("Message is signed by: %s", message.signers)

    return str(message)
