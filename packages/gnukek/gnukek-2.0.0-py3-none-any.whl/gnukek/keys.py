from types import MappingProxyType
from typing import AsyncIterable, BinaryIO, Callable, Iterable, Iterator, Mapping

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed

from gnukek import helpers, utils
from gnukek.utils import PreprocessedEncryptedStream

from . import constants, exceptions
from .backends import v1
from .backends.decryption import DecryptionBackendFactory
from .backends.encryption import EncryptionBackend
from .exceptions import raises, raises_async

_EncryptionBackendFactory = Callable[[bytes, rsa.RSAPublicKey], EncryptionBackend]


_ENCRYPTION_BACKEND_FACTORIES: Mapping[int, _EncryptionBackendFactory] = (
    MappingProxyType(
        {
            1: v1.Encryptor,
        }
    )
)

_DECRYPTION_BACKEND_FACTORIES: Mapping[int, DecryptionBackendFactory] = (
    MappingProxyType(
        {
            1: v1.DecryptorFactory(),
        }
    )
)


class PublicKey:
    __slots__ = ("_key", "_key_id")

    def __init__(self, key: rsa.RSAPublicKey) -> None:
        self._key = key
        self._key_id: bytes | None = None

    @classmethod
    @raises(exceptions.KeyLoadingError)
    def load(cls, serialized_key: bytes) -> "PublicKey":
        key_type = utils.get_key_type(serialized_key)
        assert key_type == constants.SerializedKeyType.PUBLIC_KEY, "Not a public key"

        public_key = serialization.load_pem_public_key(serialized_key)
        assert isinstance(public_key, rsa.RSAPublicKey), "Not an RSA public key"

        return cls(public_key)

    @property
    def key_size(self) -> int:
        return self._key.key_size

    @property
    @raises(exceptions.KekException, "Failed to compute key id")
    def key_id(self) -> bytes:
        if not self._key_id:
            self._key_id = self._compute_key_id()

        return self._key_id

    def get_encryptor(
        self,
        *,
        version: int = constants.LATEST_KEK_VERSION,
    ) -> EncryptionBackend:
        if version <= 0 or version > constants.LATEST_KEK_VERSION:
            raise ValueError(
                f"Latest supported version is {constants.LATEST_KEK_VERSION}"
            )
        encryption_backend_factory = _ENCRYPTION_BACKEND_FACTORIES[version]
        return encryption_backend_factory(self.key_id, self._key)

    @raises(exceptions.KeySerializationError)
    def serialize(self) -> bytes:
        return self._key.public_bytes(
            constants.KEY_SERIALIZATION_ENCODING,
            constants.PUBLIC_KEY_FORMAT,
        )

    @raises(exceptions.VerificationError)
    def verify(self, signature: bytes, *, message: bytes) -> bool:
        return self._signature_is_valid(signature, message=message)

    @raises(exceptions.VerificationError)
    def verify_stream(
        self,
        signature: bytes,
        *,
        buffer: BinaryIO,
        chunk_length: int = constants.CHUNK_LENGTH,
    ) -> bool:
        hasher = hashes.Hash(constants.SIGNATURE_HASH_ALGORITHM)
        while chunk := buffer.read(chunk_length):
            hasher.update(chunk)
        digest = hasher.finalize()
        return self._signature_is_valid(
            signature,
            message=digest,
            hash_algorithm=Prehashed(constants.SIGNATURE_HASH_ALGORITHM),
        )

    @raises(exceptions.VerificationError)
    def verify_iterable(self, signature: bytes, *, iterable: Iterable[bytes]) -> bool:
        hasher = hashes.Hash(constants.SIGNATURE_HASH_ALGORITHM)
        for chunk in iterable:
            hasher.update(chunk)
        digest = hasher.finalize()
        return self._signature_is_valid(
            signature,
            message=digest,
            hash_algorithm=Prehashed(constants.SIGNATURE_HASH_ALGORITHM),
        )

    @raises_async(exceptions.VerificationError)
    async def verify_async_iterable(
        self,
        signature: bytes,
        *,
        iterable: AsyncIterable[bytes],
    ) -> bool:
        hasher = hashes.Hash(constants.SIGNATURE_HASH_ALGORITHM)
        async for chunk in iterable:
            hasher.update(chunk)
        digest = hasher.finalize()
        return self._signature_is_valid(
            signature,
            message=digest,
            hash_algorithm=Prehashed(constants.SIGNATURE_HASH_ALGORITHM),
        )

    def _compute_key_id(self) -> bytes:
        hasher = hashes.Hash(constants.KEY_ID_HASH_ALGORITHM)
        serialized_key = self.serialize()
        hasher.update(serialized_key)
        digest = hasher.finalize()
        return digest[: constants.KEY_ID_LENGTH]

    def _signature_is_valid(
        self,
        signature: bytes,
        *,
        message: bytes,
        hash_algorithm: (
            Prehashed | hashes.HashAlgorithm
        ) = constants.SIGNATURE_HASH_ALGORITHM,
    ) -> bool:
        try:
            self._key.verify(
                signature,
                message,
                padding=constants.SIGNATURE_PADDING,
                algorithm=hash_algorithm,
            )
        except InvalidSignature:
            return False
        return True


class KeyPair:
    __slots__ = ("_rsa_private_key", "_public_key")

    def __init__(self, private_key: rsa.RSAPrivateKey) -> None:
        self._rsa_private_key = private_key
        self._public_key = PublicKey(private_key.public_key())

    @classmethod
    @raises(exceptions.KeyGenerationError)
    def generate(cls, key_size: constants.KeySize) -> "KeyPair":
        if key_size not in constants.SUPPORTED_KEY_SIZES:
            raise ValueError("Invalid key size")
        rsa_private_key = rsa.generate_private_key(
            constants.RSA_PUBLIC_EXPONENT,
            key_size,
        )
        return cls(rsa_private_key)

    @classmethod
    @raises(exceptions.KeyLoadingError)
    def load(cls, serialized_key: bytes, *, password: bytes | None = None) -> "KeyPair":
        key_type = utils.get_key_type(serialized_key)
        assert key_type in (
            constants.SerializedKeyType.PRIVATE_KEY,
            constants.SerializedKeyType.ENCRYPTED_PRIVATE_KEY,
        ), "Not a private key"

        private_key = serialization.load_pem_private_key(serialized_key, password)
        assert isinstance(private_key, rsa.RSAPrivateKey), "Not an RSA private key"

        return cls(private_key)

    @property
    def key_size(self) -> int:
        return self._rsa_private_key.key_size

    @property
    def key_id(self) -> bytes:
        return self._public_key.key_id

    @property
    def public_key(self) -> PublicKey:
        return self._public_key

    @raises(exceptions.KeySerializationError)
    def serialize(self, *, password: bytes | None = None) -> bytes:
        if password:
            encryption_algorithm: serialization.KeySerializationEncryption = (
                serialization.BestAvailableEncryption(password)
            )
        else:
            encryption_algorithm = serialization.NoEncryption()
        return self._rsa_private_key.private_bytes(
            encoding=constants.KEY_SERIALIZATION_ENCODING,
            format=constants.PRIVATE_KEY_FORMAT,
            encryption_algorithm=encryption_algorithm,
        )

    @raises(exceptions.SigningError)
    def sign(self, message: bytes) -> bytes:
        return self._create_signature(message)

    @raises(exceptions.SigningError)
    def sign_stream(
        self,
        message: BinaryIO,
        *,
        chunk_size: int = constants.CHUNK_LENGTH,
    ) -> bytes:
        hasher = hashes.Hash(constants.SIGNATURE_HASH_ALGORITHM)
        while chunk := message.read(chunk_size):
            hasher.update(chunk)
        digest = hasher.finalize()
        return self._create_signature(
            digest,
            hash_algorithm=Prehashed(constants.SIGNATURE_HASH_ALGORITHM),
        )

    @raises(exceptions.SigningError)
    def sign_iterable(self, message: Iterable[bytes]) -> bytes:
        hasher = hashes.Hash(constants.SIGNATURE_HASH_ALGORITHM)
        for chunk in message:
            hasher.update(chunk)
        digest = hasher.finalize()
        return self._create_signature(
            digest,
            hash_algorithm=Prehashed(constants.SIGNATURE_HASH_ALGORITHM),
        )

    @raises_async(exceptions.SigningError)
    async def sign_async_iterable(self, message: AsyncIterable[bytes]) -> bytes:
        hasher = hashes.Hash(constants.SIGNATURE_HASH_ALGORITHM)
        async for chunk in message:
            hasher.update(chunk)
        digest = hasher.finalize()
        return self._create_signature(
            digest,
            hash_algorithm=Prehashed(constants.SIGNATURE_HASH_ALGORITHM),
        )

    @raises(exceptions.DecryptionError)
    def decrypt(self, message: bytes) -> bytes:
        algorithm_version = message[0]
        helpers.validate_supported_algorithm_version(algorithm_version)
        encryption_key_id = utils.extract_key_id(message)
        self._validate_key_id(encryption_key_id)

        decryptor_factory = _DECRYPTION_BACKEND_FACTORIES[algorithm_version]
        decryptor = decryptor_factory.get_decryptor(
            message, private_key=self._rsa_private_key
        )
        return decryptor.decrypt()

    @raises(exceptions.DecryptionError)
    def decrypt_stream(
        self,
        message: BinaryIO | PreprocessedEncryptedStream,
        *,
        chunk_length: int = constants.CHUNK_LENGTH,
    ) -> Iterator[bytes]:
        if isinstance(message, PreprocessedEncryptedStream):
            algorithm_version = message.algorithm_version
            key_id = message.key_id
            stream = message.original_stream
        else:
            header = message.read(constants.KEY_ID_SLICE.stop)
            algorithm_version = header[0]
            key_id = utils.extract_key_id(header)
            stream = message

        helpers.validate_supported_algorithm_version(algorithm_version)
        self._validate_key_id(key_id)

        decryptor_factory = _DECRYPTION_BACKEND_FACTORIES[algorithm_version]
        stream_decryptor = decryptor_factory.get_stream_decryptor(
            stream, private_key=self._rsa_private_key
        )
        return stream_decryptor.decrypt_stream(chunk_length=chunk_length)

    def __eq__(self, obj: object) -> bool:
        if not isinstance(obj, KeyPair):
            raise TypeError(f"Unsupported type: {type(obj)}")
        return obj.key_id == self.key_id

    def __contains__(self, obj: object) -> bool:
        if isinstance(obj, PublicKey):
            return obj.key_id == self.key_id
        elif isinstance(obj, bytes):
            return obj == self.key_id
        raise TypeError(f"Unsupported type: {type(obj)}")

    def _create_signature(
        self,
        message: bytes,
        *,
        hash_algorithm: (
            Prehashed | hashes.HashAlgorithm
        ) = constants.SIGNATURE_HASH_ALGORITHM,
    ) -> bytes:
        return self._rsa_private_key.sign(
            message,
            padding=constants.SIGNATURE_PADDING,
            algorithm=hash_algorithm,
        )

    def _validate_key_id(self, encryption_key_id: bytes) -> None:
        """Check if encryption key id matches current key id."""
        if encryption_key_id != self.key_id:
            raise exceptions.DecryptionError("Data is encrypted with different key")
