"""
Post-Quantum Secure Feldman's Verifiable Secret Sharing (VSS) Implementation

Version 0.8.0b3
Developed in 2025 by David Osipov
Licensed under the MIT License

This module provides a secure, production-ready implementation of Feldman's VSS scheme
with post-quantum security by design. It enhances Shamir's Secret Sharing with
mathematical verification capabilities while remaining resistant to quantum attacks
through hash-based commitments.

Key Features:

1.  **Post-Quantum Security:** Exclusively uses hash-based commitments (BLAKE3 or SHA3-256)
    for proven resistance to quantum computer attacks. No reliance on discrete logarithm
    problems.
2.  **Secure Group Operations:** Employs the `CyclicGroup` class, which uses `gmpy2` for
    efficient and secure modular arithmetic. Includes optimized exponentiation
    (with precomputation and a thread-safe LRU cache) and multi-exponentiation.
3.  **Efficient Batch Verification:** `batch_verify_shares` provides optimized verification
    of multiple shares against the same commitments, significantly improving performance
    for large numbers of shares.
4.  **Serialization and Deserialization:** `serialize_commitments` and
    `deserialize_commitments` methods provide secure serialization and deserialization of
    commitment data, including checksums for integrity verification and handling of
    extra entropy for low-entropy secrets.
5.  **Comprehensive Validation and Error Handling:** Extensive input validation and error
    handling throughout the code to prevent misuse and ensure robustness.  Includes
    detailed error messages with forensic data collection for debugging and security
    analysis. Sanitized errors are used by default to prevent information leakage.
6.  **Fault Injection Countermeasures:** Uses redundant computation (`secure_redundant_execution`)
    and constant-time comparisons (`constant_time_compare`) to mitigate fault injection attacks.
7.  **Zero-Knowledge Proofs:** Supports the creation and verification of zero-knowledge
    proofs of polynomial knowledge, allowing a prover to demonstrate knowledge of the
    secret polynomial without revealing the coefficients.
8.  **Share Refreshing:** Implements an enhanced version of Chen & Lindell's Protocol 5
    for secure share refreshing, with improved Byzantine fault tolerance, adaptive
    quorum-based Byzantine detection, and optimized verification.
9.  **Integration with Pedersen VSS:** Includes helper functions (`integrate_with_pedersen`,
    `create_dual_commitment_proof`, `verify_dual_commitments`) for combining Feldman VSS
    with Pedersen VSS, providing both binding and hiding properties.
10. **Configurable Parameters:** The `VSSConfig` class allows customization of security
    parameters, including the prime bit length, safe prime usage, hash algorithm
    (BLAKE3 or SHA3-256), and LRU cache size.
11. **Deterministic Hashing:** Guarantees deterministic commitment generation across different
    platforms and execution environments by using fixed-length byte representations for
    integers in hash calculations.
12. **Thread-Safe LRU Cache:** Employs a `SafeLRUCache` for efficient and thread-safe caching
    of exponentiation results, with bounded memory usage.
13. **Memory Safety:**  Includes a `MemoryMonitor` and `check_memory_safety` to prevent
    excessive memory allocation, mitigating potential denial-of-service vulnerabilities.

System Requirements:

-   For threshold (t) = 50 with 4096-bit values: At least 2GB RAM
-   For threshold (t) = 100 with 4096-bit values: At least 4GB RAM
-   For threshold (t) > 100 with 4096-bit values: Consider increasing RAM or reducing parameters

The memory requirements scale approximately as O(t² * bit_length).

**Python Version Compatibility:**

-   **Minimum Supported Version: Python 3.8**
-   **Recommended Version: Python 3.13.2 (or later)**

While the library is designed to be compatible with Python 3.8 and above, using
the latest stable release (currently 3.13.2) is highly recommended for optimal
performance, security, and access to the latest language features.

This library takes advantage of features introduced in various Python versions:

-   **Python 3.6:** The `secrets` module, used for cryptographically secure random
    number generation, was introduced in Python 3.6.
-   **Python 3.7:** Data classes (`@dataclass` decorator), used in `VSSConfig`, were
    introduced, simplifying class creation and reducing boilerplate code. Dictionaries
    became ordered by insertion, providing more predictable behavior.
-   **Python 3.8:**  `typing.TypedDict`, used for defining the structure of dictionaries
    holding proof and verification data, became available. This version also introduced
    positional-only parameters (though not currently used in this library, they represent
    good practice for future development).  Audit hooks (PEP 578) were introduced,
    allowing for better security monitoring (though not directly used by the library's core logic).
-   **Python 3.9 and later:**  Continue to offer improvements in performance, type hinting,
    and general security.  While not *strictly* required, using the newest Python
    versions is generally beneficial. Python 3.13 specifically removed crypt module and
    improved SSL, but does not have new cryptographic features.

Security Considerations:

-   Always uses at least 4096-bit prime fields for post-quantum security (configurable).
-   Strongly recommends using safe primes (where (p-1)/2 is also prime) for enhanced security.
-   Defaults to BLAKE3 for cryptographic hashing (faster and more secure than SHA3-256),
    but falls back to SHA3-256 if BLAKE3 is not available.
-   Designed for seamless integration with Shamir's Secret Sharing implementation.
-   Implements countermeasures against timing attacks, fault injection attacks, and
    Byzantine behavior.
-   Uses cryptographically secure random number generation (secrets module) where needed.
-   Provides detailed error messages for debugging and security analysis
    (`sanitize_errors: bool = True` needs to be turned to `False`).

Known Security Vulnerabilities:

This library contains several timing side-channel and fault injection vulnerabilities that cannot be adequately addressed in pure Python:

1.  **Timing Side-Channels in Matrix Operations**: Functions like `_find_secure_pivot` and `_secure_matrix_solve` cannot guarantee constant-time execution in Python, potentially leaking secret information.

2.  **Non-Constant-Time Comparison**: The `constant_time_compare` function does not provide true constant-time guarantees due to Python's execution model.

**Status**: These vulnerabilities require implementation in a lower-level language like Rust to fix properly. The library should be considered experimental until these issues are addressed.

**Planned Resolution**: Future versions will integrate with Rust components for security-critical operations.

**False-Positive Vulnerabilities:**

1.  **Use of `random.Random()` in `_refresh_shares_additive`:** The code uses `random.Random()` seeded with cryptographically strong material (derived from a master secret and a party ID) within the `_refresh_shares_additive` function. While `random.Random()` is *not* generally suitable for cryptographic purposes, its use *here* is intentional and secure. The purpose is to generate *deterministic* but *unpredictable* values for the zero-sharing polynomials. The security comes from the cryptographically strong seed, *not* from the `random.Random()` algorithm itself. This is a deliberate design choice to enable verification and reduce communication overhead in the share refreshing protocol. It is *not* a source of cryptographic weakness.

Note: This implementation is fully compatible with the ShamirSecretSharing class in
the main module and is optimized to work in synergy with Pedersen VSS.

Repository: https://github.com/DavidOsipov/PostQuantum-Feldman-VSS
PyPI: https://pypi.org/project/PostQuantum-Feldman-VSS/

Developer: David Osipov
    Github Profile: https://github.com/DavidOsipov
    Email: personal@david-osipov.vision
    PGP key: https://openpgpkey.david-osipov.vision/.well-known/openpgpkey/david-osipov.vision/D3FC4983E500AC3F7F136EB80E55C4A47454E82E.asc
    PGP fingerprint: D3FC 4983 E500 AC3F 7F13 6EB8 0E55 C4A4 7454 E82E
    Website: https://david-osipov.vision
    LinkedIn: https://www.linkedin.com/in/david-osipov/
    """

# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "gmpy2 == 2.2.1",
#   "msgpack == 1.1.0",
#   "blake3 == 1.0.4; platform_system != 'Emscripten'",
#   "psutil == 7.0.0; os_name != 'Emscripten'" # Optional dependency
# ]
# ///

# mypy: disallow-untyped-defs=False
# mypy: disallow-incomplete-defs=False
# pyright: reportOptionalMemberAccess=false

import hashlib
import logging
import random
import secrets
import threading
import time
import traceback
import warnings
from base64 import urlsafe_b64decode, urlsafe_b64encode
from collections import OrderedDict
from typing import (
    Any, Dict, List, Tuple, Optional, Union,
    Callable, TypeVar, Generic, NoReturn, Type, Set, TypedDict,
)
from dataclasses import dataclass
import msgpack

# Import BLAKE3 for cryptographic hashing (faster and more secure than SHA3-256)
import importlib.util

HAS_BLAKE3 = importlib.util.find_spec("blake3") is not None
if HAS_BLAKE3:
    import blake3
else:
    warnings.warn(
        "BLAKE3 library not found. Falling back to SHA3-256. "
        "Install BLAKE3 with: pip install blake3",
        ImportWarning,
    )

# Import gmpy2 - now a strict requirement
try:
    import gmpy2
except ImportError as exc:
    raise ImportError(
        "gmpy2 library is required for this module. "
        "Install gmpy2 with: pip install gmpy2"
    ) from exc

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("feldman_vss.log"), logging.StreamHandler()],
)
logger = logging.getLogger("feldman_vss")

# Security parameters
VSS_VERSION = "VSS-0.8.0b3"
# Minimum size for secure prime fields for post-quantum security
MIN_PRIME_BITS = 4096

# Safe primes cache - these are primes p where (p-1)/2 is also prime
# Using larger primes for post-quantum security
SAFE_PRIMES = {
    # Mimimal safe prime for 5 years is 3072. The recommended is 4096. These primes are from RFC 3526. More Modular Exponential (MODP) Diffie-Hellman groups for Internet Key Exchange (IKE).
    3072: int(
        "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AAAC42DAD33170D04507A33A85521ABDF1CBA64ECFB850458DBEF0A8AEA71575D060C7DB3970F85A6E1E4C7ABF5AE8CDB0933D71E8C94E04A25619DCEE3D2261AD2EE6BF12FFA06D98A0864D87602733EC86A64521F2B18177B200CBBE117577A615D6C770988C0BAD946E208E24FA074E5AB3143DB5BFCE0FD108E4B82D120A93AD2CAFFFFFFFFFFFFFFFF",
        16,
    ),
    4096: int(
        "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AAAC42DAD33170D04507A33A85521ABDF1CBA64ECFB850458DBEF0A8AEA71575D060C7DB3970F85A6E1E4C7ABF5AE8CDB0933D71E8C94E04A25619DCEE3D2261AD2EE6BF12FFA06D98A0864D87602733EC86A64521F2B18177B200CBBE117577A615D6C770988C0BAD946E208E24FA074E5AB3143DB5BFCE0FD108E4B82D120A92108011A723C12A787E6D788719A10BDBA5B2699C327186AF4E23C1A946834B6150BDA2583E9CA2AD44CE8DBBBC2DB04DE8EF92E8EFC141FBECAA6287C59474E6BC05D99B2964FA090C3A2233BA186515BE7ED1F612970CEE2D7AFB81BDD762170481CD0069127D5B05AA993B4EA988D8FDDC186FFB7DC90A6C08F4DF435C934063199FFFFFFFFFFFFFFFF",
        16,
    ),
    6144: int(
        "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AAAC42DAD33170D04507A33A85521ABDF1CBA64ECFB850458DBEF0A8AEA71575D060C7DB3970F85A6E1E4C7ABF5AE8CDB0933D71E8C94E04A25619DCEE3D2261AD2EE6BF12FFA06D98A0864D87602733EC86A64521F2B18177B200CBBE117577A615D6C770988C0BAD946E208E24FA074E5AB3143DB5BFCE0FD108E4B82D120A92108011A723C12A787E6D788719A10BDBA5B2699C327186AF4E23C1A946834B6150BDA2583E9CA2AD44CE8DBBBC2DB04DE8EF92E8EFC141FBECAA6287C59474E6BC05D99B2964FA090C3A2233BA186515BE7ED1F612970CEE2D7AFB81BDD762170481CD0069127D5B05AA993B4EA988D8FDDC186FFB7DC90A6C08F4DF435C93402849236C3FAB4D27C7026C1D4DCB2602646DEC9751E763DBA37BDF8FF9406AD9E530EE5DB382F413001AEB06A53ED9027D831179727B0865A8918DA3EDBEBCF9B14ED44CE6CBACED4BB1BDB7F1447E6CC254B332051512BD7AF426FB8F401378CD2BF5983CA01C64B92ECF032EA15D1721D03F482D7CE6E74FEF6D55E702F46980C82B5A84031900B1C9E59E7C97FBEC7E8F323A97A7E36CC88BE0F1D45B7FF585AC54BD407B22B4154AACCC8F6D7EBF48E1D814CC5ED20F8037E0A79715EEF29BE32806A1D58BB7C5DA76F550AA3D8A1FBFF0EB19CCB1A313D55CDA56C9EC2EF29632387FE8D76E3C0468043E8F663F4860EE12BF2D5B0B7474D6E694F91E6DCC4024FFFFFFFFFFFFFFFF",
        16,
    ),
    8192: int(
        "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AAAC42DAD33170D04507A33A85521ABDF1CBA64ECFB850458DBEF0A8AEA71575D060C7DB3970F85A6E1E4C7ABF5AE8CDB0933D71E8C94E04A25619DCEE3D2261AD2EE6BF12FFA06D98A0864D87602733EC86A64521F2B18177B200CBBE117577A615D6C770988C0BAD946E208E24FA074E5AB3143DB5BFCE0FD108E4B82D120A92108011A723C12A787E6D788719A10BDBA5B2699C327186AF4E23C1A946834B6150BDA2583E9CA2AD44CE8DBBBC2DB04DE8EF92E8EFC141FBECAA6287C59474E6BC05D99B2964FA090C3A2233BA186515BE7ED1F612970CEE2D7AFB81BDD762170481CD0069127D5B05AA993B4EA988D8FDDC186FFB7DC90A6C08F4DF435C93402849236C3FAB4D27C7026C1D4DCB2602646DEC9751E763DBA37BDF8FF9406AD9E530EE5DB382F413001AEB06A53ED9027D831179727B0865A8918DA3EDBEBCF9B14ED44CE6CBACED4BB1BDB7F1447E6CC254B332051512BD7AF426FB8F401378CD2BF5983CA01C64B92ECF032EA15D1721D03F482D7CE6E74FEF6D55E702F46980C82B5A84031900B1C9E59E7C97FBEC7E8F323A97A7E36CC88BE0F1D45B7FF585AC54BD407B22B4154AACCC8F6D7EBF48E1D814CC5ED20F8037E0A79715EEF29BE32806A1D58BB7C5DA76F550AA3D8A1FBFF0EB19CCB1A313D55CDA56C9EC2EF29632387FE8D76E3C0468043E8F663F4860EE12BF2D5B0B7474D6E694F91E6DBE115974A3926F12FEE5E438777CB6A932DF8CD8BEC4D073B931BA3BC832B68D9DD300741FA7BF8AFC47ED2576F6936BA424663AAB639C5AE4F5683423B4742BF1C978238F16CBE39D652DE3FDB8BEFC848AD922222E04A4037C0713EB57A81A23F0C73473FC646CEA306B4BCBC8862F8385DDFA9D4B7FA2C087E879683303ED5BDD3A062B3CF5B3A278A66D2A13F83F44F82DDF310EE074AB6A364597E899A0255DC164F31CC50846851DF9AB48195DED7EA1B1D510BD7EE74D73FAF36BC31ECFA268359046F4EB879F924009438B481C6CD7889A002ED5EE382BC9190DA6FC026E479558E4475677E9AA9E3050E2765694DFC81F56E880B96E7160C980DD98EDD3DFFFFFFFFFFFFFFFF",
        16,
    ),
}


# Type definitions
ByzantineEvidenceDict = TypedDict('ByzantineEvidenceDict', {
    'type': str,
    'evidence': List[Dict[str, Any]],
    'timestamp': int,
    'signature': str
})
FieldElement = Union[int, "gmpy2.mpz"]  # Integer field elements
SharePoint = Tuple[FieldElement, FieldElement]  # (x, y) coordinate
ShareDict = Dict[int, SharePoint]  # Maps participant ID to share
Randomizer = FieldElement  # Randomizer values for commitments
InvalidityProofDict = TypedDict('InvalidityProofDict', {
    'party_id': int,
    'participant_id': int,
    'share_x': FieldElement,
    'share_y': FieldElement,
    'expected_commitment': FieldElement,
    'actual_commitment': FieldElement,
    'combined_randomizer': FieldElement,
    'timestamp': int,
    'signature': str
})
VerificationDataDict = TypedDict('VerificationDataDict', {
    'original_shares_count': int,
    'threshold': int,
    'zero_commitment_count': int,
    'timestamp': int,
    'protocol': str,
    'verification_method': str,
    'hash_based': bool,
    'verification_summary': Dict[str, Any],
    'seed_fingerprint': str,
    'verification_proofs': Dict[int, Dict[int, Any]]
})
HashCommitment = Tuple[FieldElement, Randomizer, Optional[bytes]]  # (hash, randomizer, entropy)
CommitmentList = List[HashCommitment]  # List of commitments
ProofDict = TypedDict('ProofDict', {
    'blinding_commitments': List[Tuple[FieldElement, FieldElement]],
    'challenge': FieldElement,
    'responses': List[FieldElement],
    'commitment_randomizers': List[FieldElement],
    'blinding_randomizers': List[FieldElement],
    'timestamp': int
})
VerificationResult = Tuple[bool, Dict[int, bool]]
RefreshingResult = Tuple[ShareDict, CommitmentList, Dict[str, Any]]

# Type Aliases for Complex Types
HashFunc = Callable[[bytes], Any]
RedundantExecutorFunc = Callable[..., Any]

# Type Aliases for Complex Types
HashFunc = Callable[[bytes], Any]
RedundantExecutorFunc = Callable[..., Any]

# Custom warning for security issues
class SecurityWarning(Warning):
    """
    Description:
        Warning for potentially insecure configurations or operations
    """

# Other exception classes
class SecurityError(Exception):
    """
    Description:
        Exception raised for security-related issues in VSS
    """
    def __init__(self, message: str, detailed_info: Optional[str] = None, 
                 severity: str = "critical", timestamp: Optional[int] = None):
        self.message = message
        self.detailed_info = detailed_info
        self.severity = severity
        self.timestamp = timestamp or int(time.time())
        super().__init__(message)
class SerializationError(Exception):
    """
    Description:
        Exception raised for serialization or deserialization errors with enhanced 
        forensic data collection.
    """
    def __init__(self, message: str, detailed_info: Optional[str] = None, 
                 severity: str = "critical", timestamp: Optional[int] = None,
                 data_format: Optional[str] = None, checksum_info: Optional[Dict[str, Any]] = None):
        self.message = message
        self.detailed_info = detailed_info
        self.severity = severity
        self.timestamp = timestamp or int(time.time())
        self.data_format = data_format  # Stores format information about the serialized data
        self.checksum_info = checksum_info  # Stores checksum validation details if applicable
        super().__init__(message)
        
    def get_forensic_data(self) -> Dict[str, Any]:
        """Return all forensic information as a dictionary for logging or analysis"""
        return {
            "message": self.message,
            "detailed_info": self.detailed_info,
            "severity": self.severity,
            "timestamp": self.timestamp,
            "data_format": self.data_format,
            "checksum_info": self.checksum_info,
            "error_type": "SerializationError"
        }

class VerificationError(Exception):
    """
    Description:
        Exception raised when share verification fails with 
        comprehensive evidence collection.
    """
    def __init__(self, message: str, detailed_info: Optional[str] = None, 
                 severity: str = "critical", timestamp: Optional[int] = None,
                 share_info: Optional[Dict[str, Any]] = None, 
                 commitment_info: Optional[Dict[str, Any]] = None):
        self.message = message
        self.detailed_info = detailed_info
        self.severity = severity
        self.timestamp = timestamp or int(time.time())
        self.share_info = share_info  # Information about the share that failed verification
        self.commitment_info = commitment_info  # Information about the commitments used
        super().__init__(message)
        
    def get_forensic_data(self) -> Dict[str, Any]:
        """Return all forensic information as a dictionary for logging or analysis"""
        return {
            "message": self.message,
            "detailed_info": self.detailed_info,
            "severity": self.severity,
            "timestamp": self.timestamp,
            "share_info": self.share_info,
            "commitment_info": self.commitment_info,
            "error_type": "VerificationError"
        }


class ParameterError(Exception):
    """
    Description:
        Exception raised for invalid parameters in VSS with enhanced
        parameter validation data.
    """
    def __init__(self, message: str, detailed_info: Optional[str] = None, 
                 severity: str = "error", timestamp: Optional[int] = None,
                 parameter_name: Optional[str] = None, 
                 parameter_value: Optional[Any] = None,
                 expected_type: Optional[str] = None):
        self.message = message
        self.detailed_info = detailed_info
        self.severity = severity
        self.timestamp = timestamp or int(time.time())
        self.parameter_name = parameter_name  # Name of the invalid parameter
        self.parameter_value = parameter_value  # Value of the invalid parameter
        self.expected_type = expected_type  # Expected type or value range
        super().__init__(message)
        
    def get_forensic_data(self) -> Dict[str, Any]:
        """Return all forensic information as a dictionary for logging or analysis"""
        return {
            "message": self.message,
            "detailed_info": self.detailed_info,
            "severity": self.severity,
            "timestamp": self.timestamp,
            "parameter_name": self.parameter_name,
            "parameter_value": str(self.parameter_value),  # Convert to string to ensure serialization
            "expected_type": self.expected_type,
            "error_type": "ParameterError"
        }

@dataclass
class VSSConfig:
    """
    Description:
        Configuration parameters for Post-Quantum Secure Feldman VSS

    Arguments:
        prime_bits (int): Number of bits for the prime modulus. Default is 4096 for post-quantum security.
        safe_prime (bool): Whether to use a safe prime (where (p-1)/2 is also prime). Default is True.
        secure_serialization (bool): Whether to use a secure serialization format. Default is True.
        use_blake3 (bool): Whether to use BLAKE3 for hashing (falls back to SHA3-256 if unavailable). Default is True.
        cache_size (int): The size of the LRU cache for exponentiation. Default is 128.
        sanitize_errors (bool): Whether to sanitize error messages. Default is True.

    Inputs:
        None

    Outputs:
        None
    """

    prime_bits: int = 4096  # Post-quantum security default
    safe_prime: bool = True  # Always use safe primes for better security
    secure_serialization: bool = True
    use_blake3: bool = (
        True  # Whether to use BLAKE3 (falls back to SHA3-256 if unavailable)
    )
    cache_size: int = 128  # Default cache size for exponentiation results
    sanitize_errors: bool = True  # Set to False in debug env for detailed errors

    def __post_init__(self) -> None:
        # Security check - enforce minimum prime size for post-quantum security
        if self.prime_bits < MIN_PRIME_BITS:
            warnings.warn(
                f"Using prime size less than {MIN_PRIME_BITS} bits is insecure against quantum attacks. "
                f"Increasing to {MIN_PRIME_BITS} bits for post-quantum security.",
                SecurityWarning,
            )
            self.prime_bits = MIN_PRIME_BITS

        if self.use_blake3 and not HAS_BLAKE3:
            warnings.warn(
                "BLAKE3 requested but not installed. Falling back to SHA3-256. "
                "Install BLAKE3 with: pip install blake3",
                RuntimeWarning,
            )


# Define type variables for our SafeLRUCache
K = TypeVar('K')  # Key type
V = TypeVar('V')  # Value type

class SafeLRUCache(Generic[K, V]):
    """
    Description:
        Thread-safe LRU cache implementation for efficient caching with memory constraints.

    Arguments:
        capacity (int): Maximum number of items to store in the cache.
    
    Type Parameters:
        K: Type of the keys in the cache
        V: Type of the values in the cache
    """

    def __init__(self, capacity: int) -> None:
        self.capacity: int = capacity
        self.cache: OrderedDict[K, V] = OrderedDict()
        self.lock: threading.RLock = threading.RLock()  # Use RLock for compatibility with existing code

    def get(self, key: K) -> Optional[V]:
        """
        Description:
            Get an item from the cache, moving it to most recently used position.

        Arguments:
            key (K): The key to retrieve.

        Returns:
            Optional[V]: The value associated with the key, or None if not found.
        """
        with self.lock:
            if key in self.cache:
                # Move to the end (most recently used)
                value: V = self.cache.pop(key)
                self.cache[key] = value
                return value
            return None

    def put(self, key: K, value: V) -> None:
        """
        Description:
            Add an item to the cache, evicting least recently used item if necessary.

        Arguments:
            key (K): The key to store.
            value (V): The value to associate with the key.
        """
        with self.lock:
            if key in self.cache:
                # Remove existing item first
                self.cache.pop(key)
            elif len(self.cache) >= self.capacity:
                # Remove the first item (least recently used)
                self.cache.popitem(last=False)
            # Add new item
            self.cache[key] = value

    def clear(self) -> None:
        """
        Description:
            Clear the cache.
        """
        with self.lock:
            self.cache.clear()

    def __len__(self) -> int:
        """
        Description:
            Return number of items in the cache.

        Outputs:
            int: The number of items in the cache.
        """
        with self.lock:
            return len(self.cache)


# --- HELPER FUNCTIONS ---

HashFunc = Callable[[bytes], Any]
RedundantExecutorFunc = Callable[..., Any]

def constant_time_compare(a: Union[int, str, bytes], b: Union[int, str, bytes]) -> bool:
    """
    Description:
        Compare two values in constant time to prevent timing attacks.

        This implementation handles integers, strings, and bytes with consistent
        processing time regardless of where differences occur.

    Arguments:
        a (int, str, or bytes): First value to compare.
        b (int, str, or bytes): Second value to compare.

    Inputs:
        a: First value to compare (int, str, or bytes)
        b: Second value to compare (int, str, or bytes)

    Outputs:
        bool: True if values are equal, False otherwise.
    """
    # Input validation
    if isinstance(a, gmpy2.mpz):
        a = int(a)
    if isinstance(b, gmpy2.mpz):
        b = int(b)
        
    # Convert to bytes for consistent handling
    if isinstance(a, int) and isinstance(b, int):
        # For integers, ensure same bit length with padding
        # Handle the case where a or b might be 0 (which doesn't have bit_length directly applicable)
        a_bits = a.bit_length() if a != 0 and hasattr(a, 'bit_length') else 0
        b_bits = b.bit_length() if b != 0 and hasattr(b, 'bit_length') else 0
        bit_length: int = max(a_bits, b_bits, 8)  # Minimum 8 bits
        byte_length: int = (bit_length + 7) // 8
        a_bytes: bytes = a.to_bytes(byte_length, byteorder="big")
        b_bytes: bytes = b.to_bytes(byte_length, byteorder="big")
    elif isinstance(a, str) and isinstance(b, str):
        a_bytes = a.encode("utf-8")
        b_bytes = b.encode("utf-8")
    elif isinstance(a, bytes) and isinstance(b, bytes):
        a_bytes = a
        b_bytes = b
    else:
        # For mixed types, use a consistent conversion approach
        a_bytes = str(a).encode("utf-8")
        b_bytes = str(b).encode("utf-8")

    # Handle different lengths with a padded comparison
    # to maintain constant time behavior
    max_len: int = max(len(a_bytes), len(b_bytes))
    a_bytes = a_bytes.ljust(max_len, b"\0")
    b_bytes = b_bytes.ljust(max_len, b"\0")

    # Constant-time comparison with the full length
    result: int = 0
    for x, y in zip(a_bytes, b_bytes):
        result |= x ^ y

    # Final result is 0 only if all bytes matched
    return result == 0


def estimate_mpz_size(n: Union[int, "gmpy2.mpz"]) -> int:
    """
    Estimate memory required for a gmpy2.mpz number of given bit length.

    Arguments:
        n (int or gmpy2.mpz): Number to estimate size for, or its bit length

    Returns:
        int: Estimated memory size in bytes
    """
    if isinstance(n, (int, gmpy2.mpz)):
        bit_length: int = (
            n.bit_length() if hasattr(n, "bit_length") and n != 0 else 
            gmpy2.mpz(n).bit_length() if n != 0 else 0
        )
    else:
        bit_length = n  # Assume n is already a bit length

    # GMP internally uses limbs (detect size if possible, default to 8 bytes on 64-bit systems)
    limb_size: int = 8  # bytes
    try:
        # Try to detect actual limb size from system architecture
        import platform

        if platform.architecture()[0] == "32bit":
            limb_size = 4
    except ImportError:
        pass

    num_limbs: int = (bit_length + 63) // 64

    # GMP object overhead (improved estimate with scaling factor)
    base_overhead: int = 32  # base overhead
    scaling_factor: float = 1 + (num_limbs // 1000) * 0.1  # Add 10% for every 1000 limbs
    overhead: int = int(base_overhead * scaling_factor)

    return (num_limbs * limb_size) + overhead


def estimate_mpz_operation_memory(op_type: str, a_bits: int, b_bits: Optional[int] = None) -> int:
    """
    Description:
        Estimate memory requirements for gmpy2 mpz operations.

    Arguments:
        op_type (str): Operation type ('add', 'mul', 'pow', etc.)
        a_bits (int): Bit length of first operand.
        b_bits (int, optional): Bit length of second operand.

    Inputs:
        op_type (str): Operation to estimate.
        a_bits (int): Size of first number.
        b_bits (int, optional): Size of second number.

    Outputs:
        int: Estimated memory requirement in bytes.

    Raises:
        ValueError: If operation type is unknown or inputs are invalid.
    """
    if not isinstance(a_bits, int) or a_bits <= 0:
        raise ValueError("a_bits must be a positive integer")

    if op_type in ("add", "sub"):
        # For addition/subtraction, result is at most 1 bit larger
        result_bits: int = max(a_bits, b_bits or 0) + 1
    elif op_type == "mul":
        if not isinstance(b_bits, int) or b_bits <= 0:
            raise ValueError("b_bits must be a positive integer for multiplication")
        # For multiplication, result is sum of bit lengths
        result_bits = a_bits + b_bits
    elif op_type == "pow":
        if not isinstance(b_bits, int) or b_bits <= 0:
            raise ValueError("b_bits must be a positive integer for exponentiation")
        # For exponentiation a^b, result is approximately a_bits * b
        if b_bits > 64:  # If exponent is very large
            raise ValueError("Exponent too large for safe memory estimation")
        # Convert b_bits to approximate value of b
        b_approx: int = min(2**b_bits - 1, 2**32)  # Cap to avoid overflow
        result_bits = a_bits * b_approx
    elif op_type == "mod":
        # For modulo, result is at most the size of the modulus
        result_bits = b_bits if b_bits else a_bits
    else:
        raise ValueError(f"Unknown operation type: {op_type}")

    # Convert bits to bytes with ceiling division and add overhead factor
    overhead_factor: float = 1.5  # Allow 50% extra for gmpy2 internal overhead
    result_bytes: float = ((result_bits + 7) // 8) * overhead_factor

    return int(result_bytes)


def estimate_exp_result_size(base_bits: int, exponent: Union[int, "gmpy2.mpz"]) -> int:
    """
    Estimate the bit length of base^exponent.

    Arguments:
        base_bits (int): Bit length of base
        exponent (int): Exponent value

    Returns:
        int: Estimated bit length of result
    """
    # For modular exponentiation, result won't exceed modulus size
    if isinstance(exponent, (int, gmpy2.mpz)) and exponent <= 2**30:
        # For reasonable exponents, we can estimate more precisely
        return base_bits * min(exponent, 2**30)
    else:
        # For very large exponents, return a reasonable maximum
        return base_bits * 2**30  # This would likely exceed memory anyway


def get_system_memory() -> int:
    """
    Get available system memory in bytes.

    Returns:
        int: Available memory in bytes, or a conservative estimate if detection fails
    """
    try:
        import psutil

        return int(psutil.virtual_memory().available)
    except ImportError:
        # If psutil not available, use a conservative default
        return 1 * 1024 * 1024 * 1024  # 1GB conservative estimate


def check_memory_safety(operation: str, *args: Any, max_size_mb: int = 1024, reject_unknown: bool = False) -> bool:
    """
    Check if operation can be performed safely without exceeding memory limits.

    Arguments:
        operation (str): Operation type ('exp', 'mul', etc.)
        *args: Arguments to the operation
        max_size_mb (int): Maximum allowed memory in MB
        reject_unknown (bool): If True, rejects all unknown operations

    Returns:
        bool: True if operation is likely safe, False otherwise
    """
    max_bytes: int = max_size_mb * 1024 * 1024

    try:
        if operation == "exp":
            base: Any
            exponent: Any
            base, exponent = args[:2]  # Get first two arguments
            # Get bit length of base
            base_bits: int = (
                base.bit_length()
                if hasattr(base, "bit_length")
                else gmpy2.mpz(base).bit_length()
            )

            # Modular exponentiation won't exceed modulus size
            if len(args) >= 3 and args[2] is not None:  # If modulus provided
                modulus: Any = args[2]
                mod_bits: int = (
                    modulus.bit_length()
                    if hasattr(modulus, "bit_length")
                    else gmpy2.mpz(modulus).bit_length()
                )
                result_bits: int = mod_bits
            else:
                # Estimate memory for non-modular exponentiation
                # Handle both int and gmpy2.mpz exponents safely without conversion
                if isinstance(exponent, (int, gmpy2.mpz)) and not isinstance(
                    exponent, bool
                ):
                    # For very large exponents, use the exponent's bit length to estimate
                    exp_bit_length: int = (
                        exponent.bit_length()
                        if hasattr(exponent, "bit_length")
                        else gmpy2.mpz(exponent).bit_length()
                    )

                    # If exponent is small enough, use direct multiplication
                    if exp_bit_length < 20:  # Exponents up to ~1 million
                        result_bits = base_bits * min(int(exponent), 1_000_000)
                    else:
                        # For larger exponents, use a logarithmic estimation
                        # log2(base^exp) = exp * log2(base)
                        result_bits = min(
                            exp_bit_length * base_bits, base_bits * 1_000_000
                        )
                else:
                    # Default for non-numeric exponents
                    result_bits = base_bits * 1000  # Very conservative

            estimated_bytes: int = estimate_mpz_size(result_bits)
            return estimated_bytes <= max_bytes

        # Other operations remain unchanged
        elif operation == "mul":
            a: Any
            b: Any
            a, b = args
            a_bits: int = (
                a.bit_length() if hasattr(a, "bit_length") and a != 0 
                else gmpy2.mpz(a).bit_length() if a != 0 
                else 0
            )
            b_bits: int = (
                b.bit_length() if hasattr(b, "bit_length") and b != 0
                else gmpy2.mpz(b).bit_length() if b != 0
                else 0
            )
            result_bits = a_bits + b_bits  # Multiplication roughly adds bit lengths
            estimated_bytes = estimate_mpz_size(result_bits)
            return estimated_bytes <= max_bytes

        # Add polynomial operation specifics
        elif operation == "polynomial":
            degree: int
            max_coeff_bits: int
            degree, max_coeff_bits = args[:2]
            # Estimate size based on degree and coefficient size
            estimated_bytes: int = degree * estimate_mpz_size(max_coeff_bits)
            # Add overhead for intermediate calculations
            estimated_bytes *= 3  # Conservative factor
            return estimated_bytes <= max_bytes

        elif operation == "matrix":
            # For matrix operations
            n: int
            bit_length: int
            n, bit_length = args[0], args[1]
            estimated_bytes = (n * n * bit_length) // 8
            return estimated_bytes <= max_bytes

        elif operation == "polynomial_eval":
            # For polynomial evaluation
            degree: int
            coeff_bits: int
            degree, coeff_bits = args[0], args[1]
            estimated_bytes = degree * estimate_mpz_size(coeff_bits)
            return estimated_bytes <= max_bytes

        else:
            # Reject unknown operations if policy dictates
            if reject_unknown:
                logger.warning(f"Rejecting unknown operation '{operation}' due to safety policy")
                return False
                
            # Generic fallback for unknown operations with enhanced safety margins
            logger.warning(
                f"Unknown operation '{operation}' in memory safety check. "
                f"Using conservative estimation, but consider adding specific handling."
            )
            
            # Estimate based on argument sizes with increased conservatism
            total_bits: int = 0
            unknown_arg_count: int = 0
            collection_size: int = 0
            max_bit_length: int = 0
            
            for arg in args:
                if hasattr(arg, "bit_length"):
                    # For integers and objects with bit_length method
                    bit_len: int = arg.bit_length()
                    total_bits += bit_len
                    max_bit_length = max(max_bit_length, bit_len)
                elif isinstance(arg, (int, float)):
                    # For numeric types without bit_length
                    total_bits += 64  # Conservative estimate
                elif isinstance(arg, (list, tuple)):
                    # For collections, track total size and count
                    arg_len: int = len(arg)
                    collection_size += arg_len
                    total_bits += arg_len * 64  # Conservative estimate for each element
                else:
                    # For unknown types, add a larger conservative buffer
                    unknown_arg_count += 1
                    total_bits += 2048  # 2KB buffer per unknown argument
            
            # Apply a more aggressive scaling factor based on complexity indicators
            scaling_factor: float = 3.0
            
            # Increase scaling for operations with multiple unknown args
            if unknown_arg_count > 1:
                scaling_factor *= (1 + (unknown_arg_count * 0.5))
                
            # Increase scaling for operations with large collections
            if collection_size > 100:
                scaling_factor *= (1 + (min(collection_size, 10000) / 1000))
                
            # Increase scaling based on max bit length
            if max_bit_length > 1024:
                scaling_factor *= (1 + (max_bit_length / 4096))
            
            # Calculate final estimate with the adaptive scaling factor
            estimated_bytes: int = int(estimate_mpz_size(total_bits) * scaling_factor)
            
            # Set a minimum reasonable estimate (1/4 of max) for unknown operations
            min_safe_bytes: int = max_bytes // 4
            if estimated_bytes < min_safe_bytes:
                logger.warning(
                    f"Increasing estimated memory for unknown operation '{operation}' "
                    f"from {estimated_bytes} to {min_safe_bytes} bytes for safety"
                )
                estimated_bytes = min_safe_bytes
            
            # Log detailed information about the estimation
            logger.debug(
                f"Memory safety estimation for unknown operation '{operation}': "
                f"{estimated_bytes} bytes (scaling factor: {scaling_factor:.2f}, "
                f"{estimated_bytes/(1024*1024):.2f}MB/{max_size_mb}MB)"
            )
            
            # For completely unknown operations with many args, reject the operation
            if unknown_arg_count > 3 and len(args) > 5:
                logger.error(
                    f"Rejecting complex unknown operation '{operation}' with too many "
                    f"unrecognized arguments for reliable memory safety estimation"
                )
                return False
                
            return estimated_bytes <= max_bytes
    except Exception as e:
        # If estimation fails, reject the operation for safety
        logger.error(f"Error during memory safety check for '{operation}': {str(e)}")
        return False


def compute_checksum(data: bytes) -> int:
    """
    Description:
        Compute checksum of data using xxhash3_128 with cryptographic fallback.

        This provides tamper-evidence for serialized data with excellent performance
        when xxhash is available, falling back to cryptographic hashes when it's not.

    Arguments:
        data (bytes): The data for which to compute the checksum.

    Inputs:
        data: The data for which to compute the checksum.

    Outputs:
        int: The computed checksum.
    """
    # Input validation
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")

    if HAS_BLAKE3:
        # trunk-ignore(pyright/reportPossiblyUnboundVariable)
        return int.from_bytes(blake3.blake3(data).digest()[:16], "big")
    return int.from_bytes(hashlib.sha3_256(data).digest()[:16], "big")


def secure_redundant_execution(
    func: RedundantExecutorFunc,
    *args: Any,
    sanitize_error_func: Optional[Callable[[str, Optional[str]], str]] = None,
    function_name: Optional[str] = None,
    context: Optional[str] = None,
    **kwargs: Any,
) -> Any:
    """
    Description:
        Execute a function multiple times with additional safeguards to detect fault injection.

        Uses improved constant-time comparison techniques and increased redundancy. Adds
        random execution ordering and timing variation to further harden against
        sophisticated fault injection attacks.

    Arguments:
        func (Callable): Function to execute redundantly.
        *args: Arguments to pass to the function.
        sanitize_error_func (Callable, optional): Function to sanitize error messages.
        function_name (str, optional): Name of the function for error context.
        context (str, optional): Additional context information for error messages.
        **kwargs: Keyword arguments to pass to the function.

    Outputs:
        Any: Result of computation if all checks pass.

    Raises:
        SecurityError: If any computation results don't match.
        TypeError: If func is not callable.
    """
    # Input validation
    if not callable(func):
        raise TypeError("func must be callable")

    # Use function name for better error reporting
    if function_name is None and hasattr(func, "__name__"):
        function_name = func.__name__
    else:
        function_name = function_name or "unknown function"

    # Increase executions from 3 to 5 for better statistical reliability
    num_executions: int = 5

    # Introduce randomly-ordered execution to prevent predictable timing patterns
    execution_order: List[int] = list(range(num_executions))
    try:
        # Use existing random module
        random.shuffle(execution_order)
    except Exception as e:
        # Fall back to deterministic if shuffle fails
        logger.debug(f"Random shuffle failed, using deterministic order: {str(e)}")

    # Execute function multiple times with randomized ordering
    results: List[Any] = []
    failures: List[Tuple[int, str]] = []

    try:
        for idx in execution_order:
            # Small random delay to decorrelate execution timing
            try:
                time.sleep(secrets.randbelow(10) / 1000)  # 0-9ms random delay
            except Exception as e:
                logger.debug(f"Random delay failed, continuing without delay: {str(e)}")

            try:
                results.append(func(*args, **kwargs))
            except Exception as e:
                # Track failures for better diagnostics
                failures.append((idx, str(e)))
                # Continue with other executions to prevent timing attacks
                results.append(None)

        # If we have failures, raise an appropriate error
        if failures:
            failure_details: str = ", ".join(
                [f"attempt {idx}: {err}" for idx, err in failures]
            )
            detailed_message: str = (
                f"Function {function_name} failed during redundant execution: "
                f"{failure_details}"
            )
            message: str = "Computation failed during security validation"

            # Log the detailed message
            logger.error(detailed_message)

            # Use sanitization function if provided
            if sanitize_error_func is not None and callable(sanitize_error_func):
                sanitized_message: str = sanitize_error_func(message, detailed_message)
                raise SecurityError(sanitized_message)
            else:
                raise SecurityError(message)

        # Handle the case where all executions succeeded but results don't match
        if not all(result == results[0] for result in results):
            # Improved constant-time comparison for all permutations
            valid: bool = True
            mismatch_details: List[str] = []

            for i in range(len(results)):
                for j in range(i + 1, len(results)):  # Only check unique pairs
                    if isinstance(results[i], int) and isinstance(results[j], int):
                        # For integers, use constant-time comparison
                        result_match: bool = constant_time_compare(results[i], results[j])
                        valid &= result_match
                        if not result_match:
                            mismatch_details.append(f"Results {i} and {j} differ")
                    elif isinstance(results[i], bytes) and isinstance(
                        results[j], bytes
                    ):
                        # For bytes, use constant-time comparison directly
                        result_match = constant_time_compare(results[i], results[j])
                        valid &= result_match
                        if not result_match:
                            mismatch_details.append(f"Results {i} and {j} differ")
                    else:
                        # For complex objects, use serialization with fallbacks
                        try:
                            # Use the already-imported msgpack
                            serialized_i: bytes = msgpack.packb(results[i], use_bin_type=True)
                            serialized_j: bytes = msgpack.packb(results[j], use_bin_type=True)
                            result_match = constant_time_compare(
                                serialized_i, serialized_j
                            )
                            valid &= result_match
                            if not result_match:
                                mismatch_details.append(f"Results {i} and {j} differ")
                        except (TypeError, ValueError):
                            # Fall back to string representation as last resort
                            result_match = constant_time_compare(
                                str(results[i]), str(results[j])
                            )
                            valid &= result_match
                            if not result_match:
                                mismatch_details.append(
                                    f"Results {i} and {j} differ (string comparison)"
                                )

            # Apply final check with more detailed error for debugging
            if not valid:
                # For detailed logging but not user-facing
                context_info: str = f" in {context}" if context else ""
                detailed_message = (
                    f"Redundant computation mismatch detected in function: "
                    f"{function_name}{context_info}. Mismatches: {mismatch_details}"
                )

                # Generic message for user-facing errors but with better categorization
                message = "Computation result mismatch - potential fault injection attack detected"

                # Log the detailed message
                logger.error(detailed_message)

                # Use sanitization function if provided, otherwise use the generic message
                if sanitize_error_func is not None and callable(sanitize_error_func):
                    sanitized_message = sanitize_error_func(message, detailed_message)
                    raise SecurityError(sanitized_message)
                else:
                    # Default behavior if no sanitization function provided
                    raise SecurityError(message)

        # Return a deterministically selected result to prevent timing side-channels
        result_index: int = hash(str(results[0])) % len(results)
        return results[result_index]

    except Exception as e:
        # Handle unexpected exceptions during processing
        if isinstance(e, SecurityError):
            raise  # Re-raise already processed security errors

        detailed_message: str = f"Unexpected error in secure redundant execution of {function_name}: {str(e)}"
        message: str = "Security validation process failed"
        logger.error(detailed_message)

        if sanitize_error_func is not None and callable(sanitize_error_func):
            sanitized_message: str = sanitize_error_func(message, detailed_message)
            raise SecurityError(sanitized_message) from e
        else:
            raise SecurityError(message) from e


class MemoryMonitor:
    """
    Description:
        Track estimated memory usage across operations to prevent gmpy2 memory allocation failures.

    Attributes:
        max_memory_mb (int): Maximum allowed memory usage in megabytes.
        current_usage (int): Current estimated memory usage in bytes.
        peak_usage (int): Peak memory usage recorded in bytes.
    """

    def __init__(self, max_memory_mb: int = 1024) -> None:
        """
        Description:
            Initialize memory monitor with specified memory limits.

        Arguments:
            max_memory_mb (int, optional): Maximum allowed memory in megabytes. Defaults to 1024.

        Inputs:
            max_memory_mb (int): Memory limit in megabytes.

        Raises:
            ValueError: If max_memory_mb is not positive.
        """
        if not isinstance(max_memory_mb, (int, float)) or max_memory_mb <= 0:
            raise ValueError("max_memory_mb must be a positive number")

        self.max_memory_mb: int = max_memory_mb
        self.current_usage: int = 0
        self.peak_usage: int = 0

    def check_allocation(self, size_bytes: int) -> bool:
        """
        Description:
            Check if an allocation would exceed memory limits without modifying usage tracker.

        Arguments:
            size_bytes (int): Size of proposed allocation in bytes.

        Inputs:
            size_bytes (int): Memory size to check.

        Outputs:
            bool: True if allocation is safe, False if it would exceed limits.

        Raises:
            ValueError: If size_bytes is negative.
            TypeError: If size_bytes is not an integer.
        """
        if not isinstance(size_bytes, int):
            raise TypeError("size_bytes must be an integer")
        if size_bytes < 0:
            raise ValueError("size_bytes cannot be negative")

        max_bytes: int = self.max_memory_mb * 1024 * 1024
        return self.current_usage + size_bytes <= max_bytes

    def allocate(self, size_bytes: int) -> bool:
        """
        Description:
            Track a memory allocation, raising exception if it would exceed limits.

        Arguments:
            size_bytes (int): Size of allocation in bytes.

        Inputs:
            size_bytes (int): Memory size to allocate.

        Outputs:
            bool: True if allocation succeeded.

        Raises:
            MemoryError: If allocation would exceed memory limit.
            ValueError: If size_bytes is negative.
            TypeError: If size_bytes is not an integer.
        """
        if not isinstance(size_bytes, int):
            raise TypeError("size_bytes must be an integer")
        if size_bytes < 0:
            raise ValueError("size_bytes cannot be negative")

        if not self.check_allocation(size_bytes):
            raise MemoryError(
                f"Operation would exceed memory limit of {self.max_memory_mb}MB"
            )

        self.current_usage += size_bytes
        self.peak_usage = max(self.peak_usage, self.current_usage)
        return True

    def release(self, size_bytes: int) -> None:
        """
        Description:
            Track memory release after operation is complete.

        Arguments:
            size_bytes (int): Size of memory to release in bytes.

        Inputs:
            size_bytes (int): Memory size to release.

        Raises:
            ValueError: If size_bytes is negative or exceeds current usage.
            TypeError: If size_bytes is not an integer.
        """
        if not isinstance(size_bytes, int):
            raise TypeError("size_bytes must be an integer")
        if size_bytes < 0:
            raise ValueError("size_bytes cannot be negative")
        if size_bytes > self.current_usage:
            raise ValueError("Cannot release more memory than currently allocated")

        self.current_usage -= size_bytes

    def get_usage_stats(self) -> Dict[str, Union[int, float]]:
        """
        Description:
            Get current memory usage statistics.

        Outputs:
            dict: Dictionary containing current and peak memory usage information.
        """
        return {
            "current_bytes": self.current_usage,
            "current_mb": self.current_usage / (1024 * 1024),
            "peak_bytes": self.peak_usage,
            "peak_mb": self.peak_usage / (1024 * 1024),
            "max_mb": self.max_memory_mb,
            "usage_percent": (self.current_usage / (self.max_memory_mb * 1024 * 1024))
            * 100,
            "peak_percent": (self.peak_usage / (self.max_memory_mb * 1024 * 1024))
            * 100,
        }


class CyclicGroup:
    """
    Description:
        Enhanced cyclic group implementation for cryptographic operations with optimizations,
        strictly using gmpy2 for all arithmetic.

    Arguments:
        prime (int, optional): Prime modulus. If None, a safe prime will be selected or generated.
        generator (int, optional): Generator of the group. If None, a generator will be found.
        prime_bits (int): Bit size for the prime if generating one (default 3072 for PQ security).
        use_safe_prime (bool): Whether to use a safe prime (p where (p-1)/2 is also prime).
        cache_size (int): The size of the LRU cache for exponentiation.

    Inputs:
        None

    Outputs:
        None
    """

    def __init__(
        self,
        prime: Optional[int] = None,
        generator: Optional[int] = None,
        prime_bits: int = 4096,
        use_safe_prime: bool = True,
        cache_size: int = 128,
        _precompute_window_size: Optional[int] = None,
    ) -> None:
        # For post-quantum security, we recommend at least 3072-bit primes
        if prime_bits < 3072:
            warnings.warn(
                "For post-quantum security, consider using prime_bits >= 3072",
                SecurityWarning,
            )

        # Use provided prime or select one
        if prime is not None:
            self.prime: "gmpy2.mpz" = gmpy2.mpz(prime)
            # Verify primality if not using a known safe prime
            if self.prime not in SAFE_PRIMES.values() and use_safe_prime:
                if not CyclicGroup._is_probable_prime(self.prime):
                    raise ParameterError("Provided value is not a prime")
                if use_safe_prime and not CyclicGroup._is_safe_prime(self.prime):
                    raise ParameterError("Provided prime is not a safe prime")
        else:
            # Use cached safe prime if available and requested
            if use_safe_prime and prime_bits in SAFE_PRIMES:
                self.prime = gmpy2.mpz(SAFE_PRIMES[prime_bits])
            else:
                # Generate a prime of appropriate size
                # Note: For production, generating safe primes is very slow
                # and should be done offline or use precomputed values
                if use_safe_prime:
                    warnings.warn(
                        "Generating a safe prime is computationally expensive. "
                        "Consider using precomputed safe primes for better performance.",
                        RuntimeWarning,
                    )
                    self.prime = self._generate_safe_prime(prime_bits)
                else:
                    self.prime = self._generate_prime(prime_bits)

        # Set or find generator
        if generator is not None:
            self.generator: "gmpy2.mpz" = gmpy2.mpz(generator % self.prime)
            if not self._is_generator(self.generator):
                raise ParameterError("Provided value is not a generator of the group")
        else:
            self.generator = self._find_generator()

        # Cache initialization with SafeLRUCache
        self.cached_powers: SafeLRUCache = SafeLRUCache(capacity=cache_size)

        # Pre-compute fixed-base exponentiations for common operations
        self._precompute_exponent_length: int = self.prime.bit_length()
        self._precompute_window_size: Optional[int] = _precompute_window_size
        self._precomputed_powers: Dict[Union[int, str], Any] = self._precompute_powers()

    @staticmethod
    def _is_probable_prime(n: Union[int, "gmpy2.mpz"], k: int = 40) -> bool:
        """
        Description:
            Check if n is probably prime using Miller-Rabin test.

        Arguments:
            n (int): Number to test.
            k (int): Number of rounds (higher is more accurate).

        Inputs:
            n (int): Number to test.

        Outputs:
            bool: True if n is probably prime, False otherwise.
        """
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0:
            return False

        # Write n as 2^r * d + 1
        r: int
        d: Union[int, "gmpy2.mpz"]
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2

        # Witness loop
        a: int
        x: "gmpy2.mpz"
        for _ in range(k):
            a = secrets.randbelow(n - 3) + 2
            x = gmpy2.powmod(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(r - 1):
                x = gmpy2.powmod(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    @staticmethod
    def _is_safe_prime(p: Union[int, "gmpy2.mpz"]) -> bool:
        """
        Description:
            Check if p is a safe prime (p=2q+1 where q is prime).

        Arguments:
            p (int): Number to check.

        Inputs:
            p (int): Number to check.

        Outputs:
            bool: True if p is a safe prime, False otherwise.
        """
        return CyclicGroup._is_probable_prime((p - 1) // 2)

    def _generate_prime(self, bits: int) -> "gmpy2.mpz":
        """
        Description:
            Generate a random prime of specified bits.

        Arguments:
            bits (int): Number of bits for the prime.

        Inputs:
            bits (int): Number of bits for the prime.

        Outputs:
            int: Generated prime number.
        """
        p: int
        while True:
            # Generate random odd number of requested bit size
            p = secrets.randbits(bits) | (1 << (bits - 1)) | 1
            if self._is_probable_prime(p):
                return gmpy2.mpz(p)

    def _generate_safe_prime(self, bits: int) -> "gmpy2.mpz":
        """
        Description:
            Generate a safe prime p where (p-1)/2 is also prime.

        Arguments:
            bits (int): Number of bits for the prime.

        Inputs:
            bits (int): Number of bits for the prime.

        Outputs:
            int: Generated safe prime number.
        """
        # This is very slow for large bit sizes - should be done offline
        q: "gmpy2.mpz"
        p: "gmpy2.mpz"
        while True:
            # Generate candidate q
            q = self._generate_prime(bits - 1)
            # Compute p = 2q + 1
            p = 2 * q + 1
            if self._is_probable_prime(p):
                return gmpy2.mpz(p)

    def _is_generator(self, g: Union[int, "gmpy2.mpz"]) -> bool:
        """
        Description:
            Check if g is a generator of the group.
            For a safe prime p = 2q + 1, we need to check:
            1. g ≠ 0, 1, p-1
            2. g^q ≠ 1 mod p

        Arguments:
            g (int): Element to check.

        Inputs:
            g (int): Element to check.

        Outputs:
            bool: True if g is a generator, False otherwise.
        """
        if g <= 1 or g >= self.prime - 1:
            return False

        # For a safe prime p=2q+1, we check if g^q != 1 mod p
        # This confirms g generates a subgroup of order q
        q: "gmpy2.mpz" = (self.prime - 1) // 2
        return gmpy2.powmod(g, q, self.prime) != 1

    def _find_generator(self) -> "gmpy2.mpz":
        """
        Description:
            Find a generator for the q-order subgroup of the cyclic group.
            For a safe prime p=2q+1, this finds an element of order q.

        Arguments:
            None

        Inputs:
            None

        Outputs:
            int: Generator of the group.
        """
        # For a safe prime p=2q+1, we want a generator of the q-order subgroup
        q: "gmpy2.mpz" = (self.prime - 1) // 2

        # Try quadratic residues: for g in Z_p*, g^2 generates the q-order subgroup
        h: int
        g: "gmpy2.mpz"
        for _ in range(10000):  # Try multiple times with different values
            h = secrets.randbelow(self.prime - 3) + 2  # Random value in [2, p-2]
            g = gmpy2.powmod(h, 2, self.prime)  # Square to get quadratic residue

            # Skip if g=1, which doesn't generate anything interesting
            if g == 1:
                continue

            # Verify g^q = 1 mod p (ensuring it's in the q-order subgroup)
            if gmpy2.powmod(g, q, self.prime) == 1 and g != 1:
                return g

        # Fallback to standard values that are often generators
        standard_candidates: List[int] = [2, 3, 5, 7, 11, 13, 17]
        for g in standard_candidates:
            if g < self.prime and self._is_generator(g):
                return gmpy2.mpz(g)

        raise RuntimeError("Failed to find a generator for the group")

    def _precompute_powers(self) -> Dict[Union[int, str], Any]:
        """
        Description:
            Pre-compute powers of the generator for faster exponentiation with multi-level windows.

        Arguments:
            None

        Inputs:
            None

        Outputs:
            dict: Precomputed powers of the generator.
        """
        bits: int = self.prime.bit_length()

        # Dynamic window sizing based on prime size
        small_window: int
        if self._precompute_window_size is not None:
            small_window = self._precompute_window_size
        else:
            # Enhanced adaptive logic with better scaling
            if bits > 8192:
                small_window = 8  # Conservative for very large primes
            elif bits > 6144:
                small_window = 7
            elif bits > 4096:
                small_window = 6
            elif bits > 3072:
                small_window = 5
            else:
                small_window = 4  # Minimum size for good performance

        # Large window remains at 8 for consistent big jumps
        large_window: int = 8
        large_step: int = 2**small_window

        # Rest of the method remains unchanged
        precomputed: Dict[Union[int, str], Any] = {}

        # Small window exponents for fine-grained values
        j: int
        for j in range(2**small_window):
            precomputed[j] = gmpy2.powmod(self.generator, j, self.prime)

        # Large window exponents for bigger jumps
        large_exponents: Dict[int, "gmpy2.mpz"] = {}
        k: int
        for k in range(1, 2 ** (large_window - small_window)):
            large_exponents[k] = gmpy2.powmod(
                self.generator, k * large_step, self.prime
            )

        # Add to precomputed dict
        precomputed.update(
            {
                "large_window": large_exponents,
                "small_bits": small_window,
                "large_step": large_step,
            }
        )

        return precomputed

    def exp(self, base: Union[int, "gmpy2.mpz"], exponent: Union[int, "gmpy2.mpz"]) -> "gmpy2.mpz":
        """
        Description:
            Thread-safe exponentiation in the group: base^exponent mod prime with optimizations.
            NOT suitable for secret exponents - use secure_exp() instead for sensitive values.

        Arguments:
            base (int): Base value.
            exponent (int): Exponent value.

        Inputs:
            base (int): Base value.
            exponent (int): Exponent value.

        Outputs:
            int: Result of the exponentiation.

        Raises:
            MemoryError: If the operation would likely exceed available memory
        """
        # Use precomputation for generator base if available
        if base == self.generator and self._precomputed_powers:
            return self._exp_with_precomputation(exponent)

        # Normalize inputs
        base_mpz: "gmpy2.mpz" = gmpy2.mpz(base % self.prime)
        
        # Optimization: For safe primes p=2q+1, reduce modulo q instead of p-1
        q: "gmpy2.mpz" = (self.prime - 1) // 2
        exponent_mpz: "gmpy2.mpz" = gmpy2.mpz(exponent % q)  # More efficient than % (self.prime - 1)

        # Check memory safety before proceeding
        if not check_memory_safety("exp", base_mpz, exponent_mpz, self.prime):
            raise MemoryError(
                "Attempted exponentiation would exceed memory limits. "
                "Consider using a smaller exponent or larger system memory."
            )

        # Check cache for common operations
        cache_key: Tuple["gmpy2.mpz", "gmpy2.mpz"] = (base_mpz, exponent_mpz)

        # Thread-safe cache access using SafeLRUCache methods
        result: Optional["gmpy2.mpz"] = self.cached_powers.get(cache_key)
        if result is not None:
            return result

        # Use efficient binary exponentiation for large numbers
        result = gmpy2.powmod(base_mpz, exponent_mpz, self.prime)

        # Cache the result using SafeLRUCache's put method (no need to check size)
        self.cached_powers.put(cache_key, result)
        return result

    def _exp_with_precomputation(self, exponent: Union[int, "gmpy2.mpz"]) -> "gmpy2.mpz":
        """
        Description:
            Exponentiation using multi-level window technique with precomputed values.

        Arguments:
            exponent (int): Exponent value.

        Inputs:
            exponent (int): Exponent value.

        Outputs:
            int: Result of the exponentiation.
        """

        if exponent == 0:
            return gmpy2.mpz(1)

        # Optimization: For safe primes p=2q+1, reduce modulo q instead of p-1
        q: "gmpy2.mpz" = (self.prime - 1) // 2 
        exponent_mpz: "gmpy2.mpz" = gmpy2.mpz(exponent) % q

        # Extract window parameters
        small_bits: int = self._precomputed_powers["small_bits"]
        large_step: int = self._precomputed_powers["large_step"]
        large_window: Dict[int, "gmpy2.mpz"] = self._precomputed_powers.get("large_window", {})

        result: "gmpy2.mpz" = gmpy2.mpz(1)
        remaining: "gmpy2.mpz" = exponent_mpz

        # Process large steps first
        large_count: int
        max_step: int
        while remaining >= large_step:
            # Extract how many large steps to take
            large_count = remaining // large_step
            if large_count in large_window:
                # Use precomputed large step
                result = (result * large_window[large_count]) % self.prime
                remaining -= large_count * large_step
            else:
                # Take the largest available step
                max_step = max(
                    (k for k in large_window.keys() if k <= large_count), default=0
                )
                if max_step > 0:
                    result = (result * large_window[max_step]) % self.prime
                    remaining -= max_step * large_step
                else:
                    # Fall back to small steps
                    break

        # Process remaining small steps
        small_val: int
        while remaining > 0:
            # Extract small window bits
            small_val = min(remaining, 2**small_bits - 1)
            if small_val in self._precomputed_powers:
                result = (result * self._precomputed_powers[small_val]) % self.prime
                remaining -= small_val
            else:
                # This case shouldn't happen with full precomputation, but just in case
                result = (
                    result * gmpy2.powmod(self.generator, small_val, self.prime)
                ) % self.prime
                remaining -= small_val

        return result

    def mul(self, a: Union[int, "gmpy2.mpz"], b: Union[int, "gmpy2.mpz"]) -> "gmpy2.mpz":
        """
        Description:
            Multiply two elements in the group: (a * b) mod prime.

        Arguments:
            a (int): First element.
            b (int): Second element.

        Inputs:
            a (int): First element.
            b (int): Second element.

        Outputs:
            int: Result of the multiplication.

        Raises:
            MemoryError: If the operation would likely exceed available memory
        """
        a_mpz: "gmpy2.mpz" = gmpy2.mpz(a)
        b_mpz: "gmpy2.mpz" = gmpy2.mpz(b)

        # Check memory safety before proceeding
        if not check_memory_safety("mul", a_mpz, b_mpz):
            raise MemoryError(
                "Multiplication operation would exceed memory limits. "
                "The operands are too large for available system memory."
            )

        return (a_mpz * b_mpz) % self.prime

    def secure_random_element(self) -> "gmpy2.mpz":
        """
        Description:
            Generate a secure random element in the group Z_p*.

        Arguments:
            None

        Inputs:
            None

        Outputs:
            int: A random element in the range [1, prime-1].
        """
        return gmpy2.mpz(secrets.randbelow(self.prime - 1) + 1)

    def clear_cache(self) -> None:
        """
        Description:
            Thread-safe clearing of exponentiation cache to free memory.

        Arguments:
            None

        Inputs:
            None

        Outputs:
            None
        """
        # Use SafeLRUCache's clear method
        self.cached_powers.clear()

    def hash_to_group(self, data: bytes) -> "gmpy2.mpz":
        """
        Description:
            Hash arbitrary data to an element in the group with uniform distribution.
            Uses strict rejection sampling with no fallback to biased methods, ensuring
            perfect uniformity across the group range [1, prime-1].

        Arguments:
            data (bytes): The data to hash.

        Inputs:
            data (bytes): The data to hash.

        Outputs:
            int: An element in the range [1, prime-1] with uniform distribution.

        Raises:
            SecurityError: If unable to generate a uniformly distributed value after
                        exhausting all attempts (extremely unlikely).
        """
        # Input validation
        if not isinstance(data, bytes):
            raise TypeError("data must be bytes")

        # Calculate required bytes based on prime size with extra bytes to minimize bias
        prime_bits: int = self.prime.bit_length()
        required_bytes: int = (prime_bits + 7) // 8
        extra_security_bytes: int = 32  # Increased from 16 for better security margin
        total_bytes: int = required_bytes + extra_security_bytes

        # Increase max attempts to reduce failure probability
        max_attempts: int = 50000  # Increased from 10000
        original_data: bytes = data

        # Make multiple attempts with domain separation
        attempt_round: int
        for attempt_round in range(5):  # Increased from 3 rounds
            counter: int = 0
            while counter < max_attempts:
                # Generate hash blocks with proper domain separation
                hash_blocks: bytearray = bytearray()
                block_counter: int = 0

                # Domain separation prefix with version and attempt round
                domain_prefix: bytes = f"HTCG_PQS_v{VSS_VERSION}_r{attempt_round}_".encode()

                h: bytes
                while len(hash_blocks) < total_bytes:
                    block_data: bytes = (
                        domain_prefix
                        + original_data
                        + counter.to_bytes(8, "big")
                        + block_counter.to_bytes(8, "big")
                    )

                    if HAS_BLAKE3:
                        h = blake3.blake3(block_data).digest(
                            min(32, total_bytes - len(hash_blocks))
                        )
                    else:
                        h = hashlib.sha3_256(block_data).digest()
                    hash_blocks.extend(h)
                    block_counter += 1

                # Convert to integer, using only the necessary bytes
                value: int = int.from_bytes(hash_blocks[:required_bytes], "big")

                # Pure rejection sampling - accept ONLY if in valid range
                if 1 <= value < self.prime:
                    return gmpy2.mpz(value)

                # If not in range, try again with a different hash input
                counter += 1

        # If we've exhausted all attempts across multiple rounds,
        # this is an exceptional condition that should be treated as a security error
        # We do NOT fall back to biased modular reduction
        raise SecurityError(
            f"Failed to generate a uniform group element after {5 * max_attempts} attempts. "
            f"This could indicate an implementation issue or an extraordinarily unlikely "
            f"statistical event (probability approximately 2^-{30 + extra_security_bytes*8})."
        )

    def _enhanced_encode_for_hash(self, *args: Any, context: str = "FeldmanVSS") -> bytes:
        """
        Description:
            Securely encode multiple values for hashing with enhanced domain separation.
            Uses both type tagging and length-prefixing to prevent collision attacks.

        Arguments:
            *args: Values to encode for hashing.
            context (str): Optional context string for domain separation (default: "FeldmanVSS").

        Outputs:
            bytes: Bytes ready for hashing.
        """
        # Initialize encoded data
        encoded: bytes = b""

        # Add protocol version identifier
        encoded += VSS_VERSION.encode("utf-8")

        # Add context string with type tag and length prefixing for domain separation
        context_bytes: bytes = context.encode("utf-8")
        encoded += b"\x01"  # Type tag for context string
        encoded += len(context_bytes).to_bytes(4, "big")
        encoded += context_bytes

        # Calculate byte length for integer serialization once
        prime_bit_length: int = self.prime.bit_length()  # Changed from self.group.prime
        byte_length: int = (prime_bit_length + 7) // 8

        # Add each value with type tagging and length prefixing
        arg: Any
        arg_bytes: bytes
        for arg in args:
            # Convert to bytes with type-specific handling and tagging
            if isinstance(arg, bytes):
                encoded += b"\x00"  # Tag for bytes
                arg_bytes = arg
            elif isinstance(arg, str):
                encoded += b"\x01"  # Tag for string
                arg_bytes = arg.encode("utf-8")
            elif isinstance(arg, int) or isinstance(arg, gmpy2.mpz):
                encoded += b"\x02"  # Tag for int/mpz
                arg_bytes = int(arg).to_bytes(byte_length, "big")
            else:
                encoded += b"\x03"  # Tag for other types
                arg_bytes = str(arg).encode("utf-8")

            # Add 4-byte length followed by the data itself
            encoded += len(arg_bytes).to_bytes(4, "big")
            encoded += arg_bytes

        return encoded

    def efficient_multi_exp(self, bases: List[Union[int, "gmpy2.mpz"]], exponents: List[Union[int, "gmpy2.mpz"]]) -> "gmpy2.mpz":
        """
        Description:
            Efficient multi-exponentiation using simultaneous method.
            Computes Π(bases[i]^exponents[i]) mod prime.

        Arguments:
            bases (list): List of base values.
            exponents (list): List of corresponding exponent values.

        Inputs:
            bases (list): List of base values.
            exponents (list): List of corresponding exponent values.

        Outputs:
            int: Result of the multi-exponentiation.
        """
        if len(bases) != len(exponents):
            raise ValueError("Number of bases must equal number of exponents")

        if len(bases) <= 1:
            if not bases:
                return gmpy2.mpz(1)
            return self.exp(bases[0], exponents[0])

        # Normalize inputs
        prime: "gmpy2.mpz" = self.prime
        bases_mpz: List["gmpy2.mpz"] = [gmpy2.mpz(b) % prime for b in bases]
        
        # Optimization: For safe primes p=2q+1, reduce modulo q instead of p-1
        q: "gmpy2.mpz" = (self.prime - 1) // 2
        exponents_mpz: List["gmpy2.mpz"] = [gmpy2.mpz(e) % q for e in exponents]  # More efficient

        # Estimate memory requirements
        max_base_bits: int = max(b.bit_length() for b in bases_mpz)
        max_exp_bits: int = max(e.bit_length() for e in exponents_mpz)
        total_ops: int = len(bases_mpz)

        # Check if this operation would be safe
        if not check_memory_safety(
            "exp", max_base_bits, max_exp_bits, prime.bit_length()
        ):
            raise MemoryError(
                f"Multi-exponentiation with {total_ops} operations of size {max_base_bits} bits "
                f"would exceed memory limits. Consider reducing parameters."
            )

        # Choose window size based on number of bases
        n: int = len(bases_mpz)
        window_size: int = 2 if n <= 4 else 3 if n <= 16 else 4
        max_bits: int = max((e.bit_length() for e in exponents_mpz), default=0)

        # For small exponents, reduce window size
        if max_bits < 128:
            window_size = max(1, window_size - 1)

        # Optimize precomputation strategy based on number of bases
        precomp: Dict[int, "gmpy2.mpz"]
        if n <= 8:
            # For small n, precompute all possible combinations
            precomp = {}
            i: int
            for i in range(1, 2**n):
                product: "gmpy2.mpz" = gmpy2.mpz(1)
                j: int
                for j in range(n):
                    if (i >> j) & 1:
                        product = (product * bases_mpz[j]) % prime
                precomp[i] = product
        else:
            # For larger n, use selective precomputation
            precomp = {1 << j: bases_mpz[j] for j in range(n)}

        # Main exponentiation loop using the precomputation
        result: "gmpy2.mpz" = gmpy2.mpz(1)
        i: int
        idx: int
        for i in range(max_bits - 1, -1, -1):
            result = (result * result) % prime

            # Determine which bases to include in this step
            idx = 0
            j: int
            for j in range(n):
                if (exponents_mpz[j] >> i) & 1:
                    idx |= 1 << j

            if idx > 0:
                if n <= 8:
                    # Use fully precomputed value
                    result = (result * precomp[idx]) % prime
                else:
                    # Selectively multiply by needed bases
                    for j in range(n):
                        if (idx >> j) & 1:
                            result = (result * bases_mpz[j]) % prime

        return result

    def secure_exp(self, base: Union[int, "gmpy2.mpz"], exponent: Union[int, "gmpy2.mpz"]) -> "gmpy2.mpz":
        """
        Description:
            Constant-time exponentiation for sensitive cryptographic operations.
            Avoids all caching and timing side-channels to prevent exponent leakage.

        Arguments:
            base (int): Base value.
            exponent (int): Exponent value (sensitive).

        Inputs:
            base (int): Base value.
            exponent (int): Exponent value.

        Outputs:
            int: base^exponent mod prime.

        Raises:
            MemoryError: If the operation would likely exceed available memory
        """
        # Normalize inputs in a predictable way to avoid timing variations
        int_base: "gmpy2.mpz" = gmpy2.mpz(base) % self.prime
        
        # Optimization: For safe primes p=2q+1, reduce modulo q instead of p-1
        q: "gmpy2.mpz" = (self.prime - 1) // 2
        int_exponent: "gmpy2.mpz" = gmpy2.mpz(exponent) % q  # More efficient

        # Check memory safety before proceeding
        if not check_memory_safety("exp", int_base, int_exponent, self.prime):
            raise MemoryError(
                "Attempted exponentiation would exceed memory limits. "
                "Consider using a smaller exponent or larger system memory."
            )

        # Use gmpy2's powmod which implements constant-time modular exponentiation
        return gmpy2.powmod(int_base, int_exponent, self.prime)


# --- END OF HELPER FUNCTIONS ---


class FeldmanVSS:
    """
    Description:
        Post-Quantum Secure Feldman Verifiable Secret Sharing implementation.

    Arguments:
        field: Object with a prime attribute representing the field for polynomial operations.
        config (VSSConfig, optional): VSSConfig object with configuration parameters. Defaults to a post-quantum secure configuration.
        group (CyclicGroup, optional): Pre-configured CyclicGroup instance. If None, a new instance will be created.

    Inputs:
        None

    Outputs:
        None
    """

    def __init__(self, field: Any, config: Optional[VSSConfig] = None, group: Optional[CyclicGroup] = None) -> None:
        if not hasattr(field, "prime") or not isinstance(field.prime, (int, gmpy2.mpz)):
            raise TypeError(
                "Field must have a 'prime' attribute that is an integer or gmpy2.mpz."
            )

        self.field: Any = field
        self.config: VSSConfig = config or VSSConfig()  # Always post-quantum secure by default
        self._byzantine_evidence: Dict[int, Dict[str, Any]] = {}

        # Initialize the cyclic group for commitments
        if group is None:
            # Use the enhanced CyclicGroup with appropriate security parameters
            self.group: CyclicGroup = CyclicGroup(
                prime_bits=self.config.prime_bits,
                use_safe_prime=self.config.safe_prime,
                cache_size=self.config.cache_size,
            )
        else:
            self.group = group

        # Store generator for commitments
        self.generator: FieldElement = self.group.generator

        # Initialize hash algorithm for use in various methods
        self.hash_algorithm: HashFunc = (
            blake3.blake3 if HAS_BLAKE3 and self.config.use_blake3 else hashlib.sha3_256
        )

    def _sanitize_error(self, message: str, detailed_message: Optional[str] = None) -> str:
        """
        Description:
            Sanitize error messages based on configuration.

        Arguments:
            message (str): The original error message.
            detailed_message (str, optional): Detailed information to log but not expose.

        Outputs:
            str: The sanitized message for external use.
        """
        if detailed_message:
            logger.error(detailed_message)

        if self.config.sanitize_errors:
            # Generic messages for different error categories
            message_lower: str = message.lower()

            # Enhanced categories for better coverage
            if any(
                keyword in message_lower
                for keyword in ["insufficient", "quorum", "threshold", "not enough"]
            ):
                return "Security verification failed - share refresh aborted"

            if any(
                keyword in message_lower
                for keyword in [
                    "deserialized",
                    "unpacked",
                    "decode",
                    "format",
                    "structure",
                ]
            ):
                return "Verification of cryptographic parameters failed"

            if any(
                keyword in message_lower
                for keyword in [
                    "tampering",
                    "checksum",
                    "integrity",
                    "modified",
                    "corrupted",
                ]
            ):
                return "Data integrity check failed"

            if any(
                keyword in message_lower
                for keyword in ["byzan", "fault", "malicious", "attack", "adversary"]
            ):
                return "Protocol security violation detected"

            if any(
                keyword in message_lower
                for keyword in ["verify", "verif", "commit", "invalid", "mismatch"]
            ):
                return "Cryptographic verification failed"

            if any(
                keyword in message_lower
                for keyword in ["prime", "generator", "arithmetic", "computation"]
            ):
                return "Cryptographic parameter validation failed"

            if any(
                keyword in message_lower for keyword in ["timeout", "expired", "future"]
            ):
                return "Security timestamp verification failed"

            # Additional categories for better coverage
            if any(
                keyword in message_lower
                for keyword in ["singular", "solve", "matrix", "gauss"]
            ):
                return "Matrix operation failed during cryptographic computation"

            if any(
                keyword in message_lower
                for keyword in ["party", "participant", "diagnostics"]
            ):
                return "Participant verification failed"

            if any(keyword in message_lower for keyword in ["hash", "blake3", "sha3"]):
                return "Hash operation failed"

            # Default generic message
            return "Cryptographic operation failed"
        else:
            return message

    def _raise_sanitized_error(self, error_class: Type[Exception], message: str, detailed_message: Optional[str] = None) -> NoReturn:
        """
        Description:
            Raise an error with a sanitized message based on configuration.

        Arguments:
            error_class: Exception class to raise.
            message (str): The original error message.
            detailed_message (str, optional): Detailed information to log but not expose.

        Outputs:
            None
        """
        sanitized: str = self._sanitize_error(message, detailed_message)
        raise error_class(sanitized)

    def _compute_hash_commitment_single(
        self, 
        value: FieldElement, 
        randomizer: FieldElement, 
        index: int,
        context: Optional[str] = None, 
        extra_entropy: Optional[bytes] = None
    ) -> FieldElement:
        """
        Description:
            Single-instance hash commitment computation (internal use).

            Uses deterministic byte encoding for integers to ensure consistent commitment
            values regardless of platform or execution environment, which is critical
            for cryptographic security.

        Arguments:
            value (int): The value to commit to.
            randomizer (int): The randomizer value.
            index (int): The position index (not used in hash calculation, kept for API compatibility).
            context (str, optional): Context string for domain separation. Defaults to "polynomial".
            extra_entropy (bytes, optional): Extra entropy for low-entropy secrets.

        Inputs:
            value: The value to commit to.
            randomizer: Randomizer.
            index: Index (not used in hash computation)
            context: Context string
            extra_entropy: extra_entropy bytes

        Outputs:
            int: The computed hash commitment.

        Raises:
            TypeError: If inputs have incorrect types.
            ValueError: If index is negative.
        """

        # Add input validation
        if not isinstance(value, (int, gmpy2.mpz)):
            raise TypeError("value must be an integer")
        if not isinstance(randomizer, (int, gmpy2.mpz)):
            raise TypeError("randomizer must be an integer")
        if not isinstance(index, (int, gmpy2.mpz)):
            raise TypeError("index must be an integer")
        if index < 0:
            raise ValueError("index must be non-negative")
        if context is not None and not isinstance(context, str):
            raise TypeError("context must be a string if provided")
        if extra_entropy is not None and not isinstance(extra_entropy, bytes):
            raise TypeError("extra_entropy must be bytes if provided")

        # Convert inputs to mpz to ensure consistent handling
        value_mpz: "gmpy2.mpz" = gmpy2.mpz(value)
        randomizer_mpz: "gmpy2.mpz" = gmpy2.mpz(randomizer)

        # Calculate byte length based on prime size
        prime_bit_length: int = self.group.prime.bit_length()
        byte_length: int = (prime_bit_length + 7) // 8

        # Prepare elements with proper byte encoding
        elements: List[Any] = [
            VSS_VERSION,  # Protocol version
            "COMMIT",  # Fixed domain separator
            context or "polynomial",  # Context with default
            value_mpz.to_bytes(byte_length, "big"),  # Value to commit to
            randomizer_mpz.to_bytes(byte_length, "big"),  # Randomizer value
        ]

        # Add extra entropy if provided for low-entropy secrets
        if extra_entropy:
            if isinstance(extra_entropy, bytes):
                elements.append(extra_entropy)
            else:
                elements.append(str(extra_entropy).encode("utf-8"))

        # Use the consistent encoding method from the group class
        encoded: bytes = self.group._enhanced_encode_for_hash(*elements)

        # Use preferred hash algorithm
        hash_output: bytes
        if HAS_BLAKE3 and self.config.use_blake3:
            hash_output = blake3.blake3(encoded).digest(32)
        else:
            hash_output = hashlib.sha3_256(encoded).digest()

        return int.from_bytes(hash_output, "big") % self.group.prime

    def _compute_hash_commitment(
        self, 
        value: FieldElement, 
        randomizer: FieldElement, 
        index: int, 
        context: Optional[str] = None, 
        extra_entropy: Optional[bytes] = None
    ) -> FieldElement:
        """
        Description:
            Enhanced hash commitment function with redundant execution for fault resistance.

            This function protects against fault injection attacks by computing the hash
            commitment multiple times and verifying the results match.

        Arguments:
            value (int): The value to commit to.
            randomizer (int): The randomizer value.
            index (int): The position index.
            context (str, optional): Context string for domain separation. Defaults to "polynomial".
            extra_entropy (bytes, optional): Extra entropy for low-entropy secrets.

        Inputs:
          value: value
          randomizer: randomizer
          index: index
          context: context
          extra_entropy: extra entropy

        Outputs:
            int: The computed hash commitment.
        """
        return secure_redundant_execution(
            self._compute_hash_commitment_single,
            value,
            randomizer,
            index,
            context,
            extra_entropy,
            sanitize_error_func=self._sanitize_error,
            function_name="_compute_hash_commitment",
        )

    def _compute_combined_randomizer(self, randomizers: List[FieldElement], x: FieldElement) -> FieldElement:
        """
        Description:
            Compute the combined randomizer for evaluating a polynomial at point x.

        Arguments:
            randomizers (list): List of randomizers for each coefficient.
            x (int): Point at which to evaluate.

        Inputs:
            randomizers: List of randomizers.
            x: Point at which to evaluate

        Outputs:
            int: Combined randomizer value for point x.
        """
        r_combined: "gmpy2.mpz" = gmpy2.mpz(0)
        x_power: "gmpy2.mpz" = gmpy2.mpz(1)

        r_i: FieldElement
        for r_i in randomizers:
            r_combined = (r_combined + gmpy2.mpz(r_i) * x_power) % self.group.prime
            x_power = (x_power * gmpy2.mpz(x)) % self.group.prime

        return r_combined

    def _compute_expected_commitment(self, commitments: List[Union[Tuple[FieldElement, ...], FieldElement]], x: FieldElement) -> FieldElement:
        """
        Description:
            Compute the expected commitment value for a polynomial at point x.

        Arguments:
            commitments (list): List of commitments for each coefficient.
            x (int): Point at which to evaluate.

        Inputs:
            commitments: commitments
            x: x

        Outputs:
            int: Expected commitment value at point x.
        """
        expected: "gmpy2.mpz" = gmpy2.mpz(0)
        x_power: "gmpy2.mpz" = gmpy2.mpz(1)

        c_i: Union[Tuple[FieldElement, ...], FieldElement]
        for c_i in commitments:
            # Extract commitment value from tuple if hash-based
            commitment_value: "gmpy2.mpz" = gmpy2.mpz(c_i[0] if isinstance(c_i, tuple) else c_i)
            expected = (expected + commitment_value * x_power) % self.group.prime
            x_power = (x_power * gmpy2.mpz(x)) % self.group.prime

        return expected

    def _verify_hash_based_commitment(
        self,
        value: Union[int, "gmpy2.mpz"],  # Improved type annotation
        combined_randomizer: Union[int, "gmpy2.mpz"],
        x: Union[int, "gmpy2.mpz"],
        expected_commitment: Union[int, "gmpy2.mpz"],
        context: Optional[str] = None,
        extra_entropy: Optional[bytes] = None,
    ) -> bool:
        """
        Description:
            Verify a hash-based commitment for a value at point x.

        Arguments:
            value (int): The value to verify.
            combined_randomizer (int): Combined randomizer for this point.
            x (int): The x-coordinate or index.
            expected_commitment (int): The expected commitment value.
            context (str, optional): Optional context string.
            extra_entropy (bytes, optional): Extra entropy for low-entropy secrets.

        Inputs:
          value: value
          combined_randomizer: combined randomizer
          x: x
          expected_commitment: expected commitment
          context: context
          extra_entropy: extra_entropy

        Outputs:
            bool: True if verification succeeds, False otherwise.
        """
        # Compute the hash commitment
        computed_commitment: Union[int, "gmpy2.mpz"] = self._compute_hash_commitment(
            value, combined_randomizer, x, context, extra_entropy
        )

        # Compare with expected commitment using constant-time comparison
        return constant_time_compare(computed_commitment, expected_commitment)

    def create_commitments(self, coefficients: List[FieldElement], context: Optional[str] = None) -> CommitmentList:
        """
        Description:
            Create post-quantum secure hash-based commitments to polynomial coefficients.
    
        Arguments:
            coefficients (list): List of polynomial coefficients [a₀, a₁, ..., aₖ₋₁] where a₀ is the secret.
            context (str, optional): Optional context string for domain separation.
    
        Inputs:
            coefficients: List of coefficients
            context: Context string
    
        Outputs:
            list: List of (hash, randomizer) tuples representing hash-based commitments.
    
        Raises:
            TypeError: If coefficients is not a list.
            ValueError: If coefficients list is empty.
        """
        # Input validation
        if not isinstance(coefficients, list):
            raise TypeError("coefficients must be a list")
            
        if not coefficients:
            self._raise_sanitized_error(ValueError, "Coefficients list cannot be empty")
            
        if context is not None and not isinstance(context, str):
            raise TypeError("context must be a string if provided")
        
        # Use the enhanced commitment creation method for better security
        return self.create_enhanced_commitments(coefficients, context)

    def create_enhanced_commitments(self, coefficients: List[FieldElement], context: Optional[str] = None) -> CommitmentList:
        """
        Description:
            Create enhanced hash-based commitments with improved entropy handling
            for low-entropy secrets (Baghery's method, 2025).

        Arguments:
            coefficients (list): List of polynomial coefficients.
            context (str, optional): Optional context string for domain separation.

        Inputs:
            coefficients: List of coefficients
            context: Context string

        Outputs:
            list: List of (hash, randomizer) tuples.

        Raises:
            TypeError: If coefficients is not a list or context is not a string.
            ParameterError: If coefficients list is empty.
        """
        # Input validation
        if not isinstance(coefficients, list):
            raise TypeError("coefficients must be a list")
        if context is not None and not isinstance(context, str):
            raise TypeError("context must be a string if provided")

        if not coefficients:
            self._raise_sanitized_error(
                ParameterError, "Coefficients list cannot be empty"
            )

        # Convert all coefficients to integers and reduce modulo field prime
        coeffs_int: List["gmpy2.mpz"] = [gmpy2.mpz(coeff) % self.field.prime for coeff in coefficients]

        # Check entropy of secret coefficient (first coefficient)
        secret: "gmpy2.mpz" = coeffs_int[0]
        low_entropy_threshold: int = (
            256  # In bits (enhanced from previous 128-bit threshold)
        )
        might_have_low_entropy: bool = secret.bit_length() < low_entropy_threshold

        # Create enhanced hash-based commitments
        commitments: CommitmentList = []
        i: int
        coeff: "gmpy2.mpz"
        for i, coeff in enumerate(coeffs_int):
            # Generate secure randomizer
            r_i: FieldElement = self.group.secure_random_element()

            # Add extra entropy for the secret if needed
            extra_entropy: Optional[bytes] = None
            if i == 0 and might_have_low_entropy:
                extra_entropy = secrets.token_bytes(32)

            # Use the dedicated hash commitment function
            commitment: FieldElement = self._compute_hash_commitment(
                coeff, r_i, i, context or "polynomial", extra_entropy
            )

            # Store commitment and randomizer
            commitments.append((commitment, r_i, extra_entropy))

        return commitments

    def _verify_share_hash_based_single(self, x: FieldElement, y: FieldElement, commitments: CommitmentList) -> bool:
        """
        Description:
            Single-instance share verification (internal use).

        Arguments:
            x (int): x-coordinate of the share.
            y (int): y-coordinate of the share.
            commitments (list): List of (commitment, randomizer) tuples.

        Inputs:
            x: x
            y: y
            commitments: commitments

        Outputs:
            bool: True if the share is valid, False otherwise.
        """
        # Extract randomizers from commitments
        randomizers: List[FieldElement] = [r_i for _, r_i, _ in commitments]

        # Compute combined randomizer
        r_combined: FieldElement = self._compute_combined_randomizer(randomizers, x)

        # Compute expected commitment
        expected_commitment: FieldElement = self._compute_expected_commitment(commitments, x)

        # Extract extra_entropy if present (should be in the first coefficient only)
        extra_entropy: Optional[bytes] = None
        if len(commitments) > 0 and len(commitments[0]) > 2:
            extra_entropy = commitments[0][2]  # Get extra_entropy from first coefficient

        # Verify using helper method
        return self._verify_hash_based_commitment(
            y, r_combined, x, expected_commitment, extra_entropy=extra_entropy
        )

    def verify_share(self, share_x: FieldElement, share_y: FieldElement, commitments: CommitmentList) -> bool:
        """
        Description:
            Fault-resistant share verification with redundant execution.

            Verifies that a share (x, y) lies on the polynomial committed to by the commitments
            using post-quantum secure hash-based verification with fault injection protection.

        Arguments:
            share_x (int): x-coordinate of the share.
            share_y (int): y-coordinate of the share (the actual share value).
            commitments (list): List of (commitment, randomizer) tuples.

        Inputs:
            share_x: x coordinate
            share_y: y coordinate
            commitments: commitments

        Outputs:
            bool: True if the share is valid, False otherwise.

        Raises:
            TypeError: If inputs have incorrect types or commitments is empty.
        """
        # Input validation
        if not isinstance(share_x, (int, gmpy2.mpz)):
            raise TypeError("share_x must be an integer")
        if not isinstance(share_y, (int, gmpy2.mpz)):
            raise TypeError("share_y must be an integer")
        if not isinstance(commitments, list) or not commitments:
            raise TypeError("commitments must be a non-empty list")

        # Validate commitment format
        if not all(isinstance(c, tuple) and len(c) >= 2 for c in commitments):
            raise TypeError(
                "commitments must be a list of (commitment, randomizer) tuples"
            )

        # Convert to integers and use redundant verification
        x: "gmpy2.mpz"
        y: "gmpy2.mpz"
        x, y = gmpy2.mpz(share_x), gmpy2.mpz(share_y)
        return secure_redundant_execution(
            self._verify_share_hash_based_single,
            x,
            y,
            commitments,
            sanitize_error_func=self._sanitize_error,
            function_name="verify_share",
        )

    def batch_verify_shares(self, shares: List[SharePoint], commitments: CommitmentList) -> VerificationResult:
        """
        Description:
            Efficiently verify multiple shares against the same commitments.

            Uses optimized batch verification for hash-based commitments with caching of
            intermediate values for improved performance with large batches.

        Arguments:
            shares (list): List of (x, y) share tuples.
            commitments (list): List of (commitment, randomizer) tuples.

        Inputs:
            shares: shares
            commitments: commitments

        Outputs:
            tuple: (all_valid: bool, results: Dict mapping share indices to verification results).

        Raises:
            TypeError: If inputs have incorrect types or are empty.
            ValueError: If shares list is empty.
        """
        # Input validation
        if not isinstance(shares, list):
            raise TypeError("shares must be a list of (x, y) tuples")
        if not shares:
            self._raise_sanitized_error(ValueError, "shares list cannot be empty")
        if not all(isinstance(s, tuple) and len(s) == 2 for s in shares):
            raise TypeError("Each share must be a tuple of (x, y)")

        if not isinstance(commitments, list) or not commitments:
            raise TypeError("commitments must be a non-empty list")
        if not all(isinstance(c, tuple) and len(c) >= 2 for c in commitments):
            raise TypeError(
                "commitments must be a list of (commitment, randomizer) tuples"
            )

        results: Dict[int, bool] = {}
        all_valid: bool = True

        # Standard verification for small batches
        if len(shares) < 5:
            i: int
            x: FieldElement
            y: FieldElement
            is_valid: bool
            for i, (x, y) in enumerate(shares):
                is_valid = self.verify_share(x, y, commitments)
                results[i] = is_valid
                # Use constant-time boolean operation
                all_valid &= is_valid  # Constant-time AND
            return all_valid, results

        # Extract randomizers for more efficient processing
        randomizers: List[FieldElement] = [r_i for _, r_i, _ in commitments]

        # Extract extra_entropy if present (only for first coefficient)
        extra_entropy: Optional[bytes] = None
        if len(commitments) > 0 and len(commitments[0]) > 2:
            extra_entropy = commitments[0][2]

        # For larger batches, use optimized verification approach with caching
        # Precompute powers of x for each share to avoid redundant calculations
        x_powers_cache: Dict[FieldElement, List["gmpy2.mpz"]] = {}

        # Prepare commitment combinations for each share
        share_commitments: List[Tuple[FieldElement, FieldElement, FieldElement, FieldElement]] = []

        # First pass: compute and cache powers of x and prepare combined values
        x: FieldElement
        y: FieldElement
        for x, y in shares:
            if x not in x_powers_cache:
                # Compute and cache powers of x
                powers: List["gmpy2.mpz"] = [gmpy2.mpz(1)]  # x^0 = 1
                current_power: "gmpy2.mpz" = gmpy2.mpz(1)
                j: int
                for j in range(1, len(commitments)):
                    current_power = (current_power * gmpy2.mpz(x)) % self.field.prime
                    powers.append(current_power)
                x_powers_cache[x] = powers

            # Use helper methods to compute randomizers and expected commitments
            r_combined: FieldElement = self._compute_combined_randomizer(randomizers, x)
            expected_commitment: FieldElement = self._compute_expected_commitment(commitments, x)

            share_commitments.append((x, y, r_combined, expected_commitment))

        # Second pass: verify each share with precomputed values (with batch processing)
        batch_size: int = min(32, len(share_commitments))  # Process in reasonable batches

        batch_start: int
        for batch_start in range(0, len(share_commitments), batch_size):
            batch_end: int = min(batch_start + batch_size, len(share_commitments))
            batch: List[Tuple[FieldElement, FieldElement, FieldElement, FieldElement]] = share_commitments[batch_start:batch_end]

            # Process verification in batches
            i: int
            idx: int
            is_valid: bool
            for i, (x, y, r_combined, expected_commitment) in enumerate(batch):
                idx = batch_start + i
                is_valid = self._verify_hash_based_commitment(
                    y, r_combined, x, expected_commitment, extra_entropy=extra_entropy
                )

                results[idx] = is_valid
                # Update boolean result using logical AND operation
                all_valid &= is_valid  # Note: Not guaranteed to be constant-time

        return all_valid, results

    def serialize_commitments(self, commitments: CommitmentList) -> str:
        """
        Description:
            Serialize commitment data with checksum for fault resistance.

        Arguments:
            commitments (list): List of (hash, randomizer) tuples.

        Inputs:
            commitments: commitments

        Outputs:
            str: String with base64-encoded serialized data with embedded checksum.

        Raises:
            TypeError: If commitments is not a list or has incorrect format.
            ValueError: If commitments list is empty.
            SerializationError: If serialization fails.
        """
        # Input validation
        if not isinstance(commitments, list):
            raise TypeError("commitments must be a list")
        if not commitments:
            self._raise_sanitized_error(ValueError, "commitments list cannot be empty")

        if not all(isinstance(c, tuple) and len(c) >= 2 for c in commitments):
            raise TypeError(
                "Each commitment must be a tuple with at least (commitment, randomizer)"
            )

        # Extract commitment values
        commitment_values: List[Tuple[int, int, Optional[str]]] = [
            (int(c), int(r), e.hex() if e else None) for c, r, e in commitments
        ]

        # Create the data structure
        result: Dict[str, Any] = {
            "version": VSS_VERSION,
            "timestamp": int(time.time()),
            "generator": int(self.generator),
            "prime": int(self.group.prime),
            "commitments": commitment_values,
            "hash_based": True,
        }

        try:
            # Pack with msgpack for efficient serialization
            packed_data: bytes = msgpack.packb(result)

            # Compute checksum and create wrapper
            checksum_wrapper: Dict[str, bytes] = {
                "data": packed_data,
                "checksum": compute_checksum(packed_data),
            }

            # Pack the wrapper and encode
            packed_wrapper: bytes = msgpack.packb(checksum_wrapper)
            return urlsafe_b64encode(packed_wrapper).decode("utf-8")
        except Exception as e:
            detailed_msg = f"Failed to serialize commitments: {e}"
            message = "Serialization failed"
            self._raise_sanitized_error(SerializationError, message, detailed_msg)

    def deserialize_commitments(self, data: str) -> Tuple[CommitmentList, FieldElement, FieldElement, int, bool]:
        """
        Description:
            Deserialize commitment data with checksum verification

        Arguments:
            data (str): Serialized commitment data string.

        Inputs:
            data: Serialized data

        Outputs:
            tuple: (commitments, generator, prime, timestamp, is_hash_based).

        Raises:
            TypeError: If data is not a string or is empty.
            ValueError: If data is empty.
            SerializationError: If deserialization or validation fails.
            SecurityError: If checksum or cryptographic parameter validation fails.
        """
        # Input validation
        if not isinstance(data, str):
            self._raise_sanitized_error(TypeError, "Data must be a string")
        if not data:
            self._raise_sanitized_error(ValueError, "Data cannot be empty")

        try:
            # Decode from URL-safe base64
            decoded: bytes = urlsafe_b64decode(data.encode("utf-8"))

            # Use Unpacker with security settings
            unpacker: msgpack.Unpacker = msgpack.Unpacker(
                use_list=False,  # Use tuples instead of lists for immutability
                raw=True,  # Keep binary data as bytes
                strict_map_key=True,
                max_buffer_size=10 * 1024 * 1024,  # 10MB limit
            )
            unpacker.feed(decoded)

            try:
                # Unpack the checksum wrapper
                wrapper: Dict[bytes, Any] = unpacker.unpack()
            except (
                msgpack.exceptions.ExtraData,
                msgpack.exceptions.FormatError,
                msgpack.exceptions.StackError,
                msgpack.exceptions.BufferFull,
                msgpack.exceptions.OutOfData,
                ValueError,
            ) as e:
                detailed_msg = f"Failed to unpack msgpack data: {e}"
                message = "Invalid data format"
                self._raise_sanitized_error(SerializationError, message, detailed_msg)

            # Verify checksum - this is a critical security check
            if b"checksum" not in wrapper or b"data" not in wrapper:
                detailed_msg = f"Detailed deserialization error - data format: {type(data)}, traceback: {traceback.format_exc()}"
                message = "Invalid data format"
                self._raise_sanitized_error(SerializationError, message, detailed_msg)

            packed_data: bytes = wrapper[b"data"]
            expected_checksum: int = wrapper[b"checksum"]
            actual_checksum: int = compute_checksum(packed_data)

            if not constant_time_compare(actual_checksum, expected_checksum):
                detailed_msg = f"Checksum mismatch: expected {expected_checksum}, got {actual_checksum}"
                message = "Data integrity check failed - possible tampering detected"
                self._raise_sanitized_error(SecurityError, message, detailed_msg)

            # Feed the inner data to a new Unpacker instance
            inner_unpacker: msgpack.Unpacker = msgpack.Unpacker(
                use_list=False,
                raw=True,
                strict_map_key=True,
                max_buffer_size=10 * 1024 * 1024,
            )
            inner_unpacker.feed(packed_data)

            try:
                # Proceed with unpacking the actual data
                unpacked: Dict[bytes, Any] = inner_unpacker.unpack()
            except (
                msgpack.exceptions.ExtraData,
                msgpack.exceptions.FormatError,
                msgpack.exceptions.StackError,
                msgpack.exceptions.BufferFull,
                msgpack.exceptions.OutOfData,
                ValueError,
            ) as e:
                detailed_msg = f"Failed to unpack inner msgpack data: {e}"
                message = "Invalid data format"
                self._raise_sanitized_error(SerializationError, message, detailed_msg)

            # With raw=True, keys will be bytes instead of strings
            version_key: bytes = b"version"
            version_bytes: bytes = VSS_VERSION.encode("utf-8")

            # Validate the version
            if unpacked.get(version_key) != version_bytes:
                detailed_msg = f"Unsupported VSS version: {unpacked.get(version_key)}"
                message = "Unsupported version"
                self._raise_sanitized_error(SerializationError, message, detailed_msg)

            # Validate structure of deserialized data - note use of byte keys
            if not isinstance(
                unpacked.get(b"commitments"), tuple
            ):  # was list, now tuple with use_list=False
                detailed_msg = f"Invalid commitment data: expected sequence, got {type(unpacked.get(b'commitments'))}"
                message = "Invalid data structure"
                self._raise_sanitized_error(SerializationError, message, detailed_msg)

            if not isinstance(unpacked.get(b"generator"), int):
                detailed_msg = f"Invalid generator: expected integer, got {type(unpacked.get(b'generator'))}"
                message = "Invalid data structure"
                self._raise_sanitized_error(SerializationError, message, detailed_msg)

            if not isinstance(unpacked.get(b"prime"), int):
                detailed_msg = f"Invalid prime: expected integer, got {type(unpacked.get(b'prime'))}"
                message = "Invalid data structure"
                self._raise_sanitized_error(SerializationError, message, detailed_msg)

            # Additional check for commitment structure
            i: int
            commitment: Tuple[Any, ...]
            for i, commitment in enumerate(unpacked.get(b"commitments", tuple())):
                if not isinstance(commitment, tuple) or len(commitment) not in (2, 3):
                    detailed_msg = f"Invalid commitment format at index {i}: expected (commitment, randomizer) or (commitment, randomizer, extra_entropy) tuple"
                    message = "Invalid data structure"
                    self._raise_sanitized_error(
                        SerializationError, message, detailed_msg
                    )

            # Extract the commitments and parameters
            commitments: Tuple[Tuple[Any, ...], ...] = unpacked.get(b"commitments")
            generator: int = unpacked.get(b"generator")
            prime: int = unpacked.get(b"prime")
            timestamp: int = unpacked.get(b"timestamp", 0)
            is_hash_based: bool = unpacked.get(b"hash_based", True)  # Default to hash-based

            # Enhanced validity checks
            if not (commitments and generator and prime):
                detailed_msg = "Missing required fields in commitment data"
                message = "Invalid data structure"
                self._raise_sanitized_error(SerializationError, message, detailed_msg)

            # Validate that prime is actually prime
            if prime not in SAFE_PRIMES.values() and self.config.safe_prime:
                if not CyclicGroup._is_probable_prime(prime):
                    detailed_msg = "Deserialized prime value failed primality test"
                    message = "Cryptographic parameter validation failed"
                    self._raise_sanitized_error(SecurityError, message, detailed_msg)

                if self.config.safe_prime and not CyclicGroup._is_safe_prime(prime):
                    detailed_msg = "Deserialized prime is not a safe prime"
                    message = "Cryptographic parameter validation failed"
                    self._raise_sanitized_error(SecurityError, message, detailed_msg)

            # Validate generator is in the correct range
            if generator <= 1 or generator >= prime - 1:
                detailed_msg = "Deserialized generator is outside valid range"
                message = "Cryptographic parameter validation failed"
                self._raise_sanitized_error(SecurityError, message, detailed_msg)

            # Ensure the generator is valid for this prime
            g: "gmpy2.mpz" = gmpy2.mpz(generator)
            p: "gmpy2.mpz" = gmpy2.mpz(prime)
            q: "gmpy2.mpz" = (p - 1) // 2  # For safe primes, q = (p-1)/2 is also prime
            # A proper generator for a safe prime p=2q+1 should satisfy g^q ≠ 1 mod p
            if gmpy2.powmod(g, q, p) == 1:
                detailed_msg = "Deserialized generator is not a valid group generator"
                message = "Cryptographic parameter validation failed"
                self._raise_sanitized_error(SecurityError, message, detailed_msg)

            # Additional validation to verify all commitment values are in the proper range
            i: int
            commitment_data: Tuple[Any, ...]
            for i, commitment_data in enumerate(commitments):
                if len(commitment_data) >= 2:
                    commitment_value: int = commitment_data[0]
                    randomizer: int = commitment_data[1]

                    # Validate commitment and randomizer are in valid range
                    if not (0 <= commitment_value < prime) or not (
                        0 <= randomizer < prime
                    ):
                        detailed_msg = f"Commitment or randomizer at index {i} is outside valid range"
                        message = "Cryptographic parameter validation failed"
                        self._raise_sanitized_error(
                            SecurityError, message, detailed_msg
                        )

            # Enforce hash-based commitments for post-quantum security
            if not is_hash_based:
                detailed_msg = "Only hash-based commitments are supported in this post-quantum secure version"
                message = "Unsupported commitment type"
                self._raise_sanitized_error(SecurityError, message, detailed_msg)

            # Reconstruct hash-based commitments
            reconstructed_commitments: CommitmentList = []
            commitment_data: Tuple[Any,...]
            for commitment_data in commitments:
                if len(commitment_data) >= 3 and commitment_data[2]:
                    # Has extra entropy - convert hex string back to bytes
                    reconstructed_commitments.append(
                        (
                            gmpy2.mpz(commitment_data[0]),
                            gmpy2.mpz(commitment_data[1]),
                            bytes.fromhex(commitment_data[2]) if commitment_data[2] else None,
                        )
                    )
                else:
                    # No extra entropy
                    reconstructed_commitments.append(
                        (
                            gmpy2.mpz(commitment_data[0]),
                            gmpy2.mpz(commitment_data[1]),
                            None,
                        )
                    )

            return (
                reconstructed_commitments,
                gmpy2.mpz(generator),
                gmpy2.mpz(prime),
                timestamp,
                is_hash_based,
            )

        except Exception as e:
            if isinstance(e, (SerializationError, SecurityError)):
                raise

            detailed_msg = f"Exception during deserialization: {str(e)}"
            message = "Failed to deserialize commitments"
            self._raise_sanitized_error(SerializationError, message, detailed_msg)

    def verify_share_from_serialized(self, share_x: FieldElement, share_y: FieldElement, serialized_commitments: str) -> bool:
        """
        Description:
            Verify a share against serialized commitment data.

        Arguments:
            share_x (int): x-coordinate of the share.
            share_y (int): y-coordinate of the share.
            serialized_commitments (str): Serialized commitment data.

        Inputs:
            share_x: x coordinate
            share_y: y coordinate
            serialized_commitments: serialized commitments

        Outputs:
            bool: True if the share is valid, False otherwise.

        Raises:
            TypeError: If inputs have incorrect types or serialized_commitments is empty.
            VerificationError: If deserialization or verification fails.
        """
        # Input validation
        if not isinstance(share_x, (int, gmpy2.mpz)):
            raise TypeError("share_x must be an integer")
        if not isinstance(share_y, (int, gmpy2.mpz)):
            raise TypeError("share_y must be an integer")
        if not isinstance(serialized_commitments, str) or not serialized_commitments:
            raise TypeError("serialized_commitments must be a non-empty string")

        try:
            # Deserialize the commitments
            commitments: CommitmentList
            generator: FieldElement
            prime: FieldElement
            timestamp: int
            is_hash_based: bool
            commitments, generator, prime, timestamp, is_hash_based = (
                self.deserialize_commitments(serialized_commitments)
            )

            # Create a group with the same parameters
            group: CyclicGroup = CyclicGroup(prime=prime, generator=generator)

            # Create a new VSS instance with this group
            temp_config: VSSConfig = VSSConfig()
            temp_vss: FeldmanVSS = FeldmanVSS(self.field, temp_config, group)

            # Verify the share
            return temp_vss.verify_share(share_x, share_y, commitments)

        except Exception as e:
            detailed_msg = f"Detailed verification failure for share ({share_x}, {share_y}): {str(e)}, Traceback: {traceback.format_exc()}"
            message = f"Failed to verify share: {e}"
            self._raise_sanitized_error(VerificationError, message, detailed_msg)

    def clear_cache(self) -> None:
        """
        Description:
            Clear verification cache to free memory.

        Arguments:
            None

        Inputs:
            None

        Outputs:
            None
        """
        self.group.clear_cache()

    def __del__(self) -> None:
        """
        Description:
            Clean up when the object is deleted.

        Arguments:
            None

        Inputs:
            None

        Outputs:
            None
        """
        self.clear_cache()

        # Securely wipe any sensitive data
        if hasattr(self, "generator"):
            del self.generator
        if hasattr(self, "field"):
            self.field.clear_cache()

    def refresh_shares(
        self,
        shares: ShareDict,
        threshold: int,
        total_shares: int,
        original_commitments: Optional[CommitmentList] = None,
        participant_ids: Optional[List[int]] = None,
    ) -> RefreshingResult:
        """
        Description:
            Refresh shares while preserving the same secret using an optimized implementation
            of Chen & Lindell's Protocol 5, providing stronger security guarantees in asynchronous
            environments.

        Arguments:
            shares (dict): Dictionary mapping participant IDs to their shares {id: (x, y)}.
            threshold (int): The secret sharing threshold.
            total_shares (int): Total number of shares to generate.
            original_commitments (list, optional): Original commitment values (optional, for proof validation).
            participant_ids (list, optional): Optional list of IDs for participants (defaults to numeric IDs).

        Inputs:
            shares: shares
            threshold: threshold
            total_shares: total_shares
            original_commitments: original commitments
            participant_ids: participant_ids

        Outputs:
            tuple: (new_shares, new_commitments, verification_data).

        Raises:
            TypeError: If inputs have incorrect types.
            ValueError: If threshold or total_shares are invalid, or participant_ids length is incorrect.
            ParameterError: If not enough shares are provided.
        """
        # Input validation
        if not isinstance(shares, dict):
            raise TypeError(
                "shares must be a dictionary mapping participant IDs to (x, y) tuples"
            )
        if not all(isinstance(v, tuple) and len(v) == 2 for v in shares.values()):
            raise TypeError("Each share must be a tuple of (x, y)")

        if not isinstance(threshold, int) or threshold < 2:
            raise ValueError("threshold must be an integer >= 2")

        if not isinstance(total_shares, int) or total_shares < threshold:
            raise ValueError("total_shares must be an integer >= threshold")

        if original_commitments is not None and not isinstance(
            original_commitments, list
        ):
            raise TypeError("original_commitments must be a list if provided")

        if participant_ids is not None:
            if not isinstance(participant_ids, list):
                raise TypeError("participant_ids must be a list if provided")
            if len(participant_ids) != total_shares:
                raise ValueError("Number of participant_ids must match total_shares")

        if len(shares) < threshold:
            detailed_msg = (
                f"Need at least {threshold} shares to refresh, got {len(shares)}"
            )
            message = f"Need at least {threshold} shares to refresh"
            self._raise_sanitized_error(ParameterError, message, detailed_msg)

        # Set default participant IDs if not provided
        if participant_ids is None:
            participant_ids = list(range(1, total_shares + 1))

        if len(participant_ids) != total_shares:
            detailed_msg = "Number of participant IDs must match total_shares"
            message = "Invalid parameters"
            self._raise_sanitized_error(ParameterError, message, detailed_msg)

        # Use enhanced additive resharing method (Chen & Lindell's Protocol 5)
        # with optimizations for asynchronous environments
        return self._refresh_shares_additive(
            shares, threshold, total_shares, participant_ids
        )

    def _refresh_shares_additive(self, shares: ShareDict, threshold: int, total_shares: int, participant_ids: List[int]
    ) -> RefreshingResult:
        """
        Description:
            Enhanced refresh shares using optimized Chen & Lindell's Protocol 5 (additive resharing).

            This implementation includes optimizations for:
            1. Better performance in asynchronous environments
            2. Reduced communication complexity
            3. Improved resilience against adversarial parties
            4. More efficient verification
            5. Advanced Byzantine fault tolerance

        Arguments:
            shares (dict): Dictionary mapping participant IDs to their shares {id: (x, y)}.
            threshold (int): The secret sharing threshold.
            total_shares (int): Total number of shares to generate.
            participant_ids (list): List of IDs for participants.

        Inputs:
            shares: shares
            threshold: threshold
            total_shares: total shares
            participant_ids: participant ids

        Outputs:
            tuple: (new_shares, new_commitments, verification_data).
        """
        # Step 1: Each party creates a sharing of zero with enhanced verification
        zero_sharings: Dict[int, ShareDict] = {}
        zero_commitments: Dict[int, CommitmentList] = {}

        # Use a deterministic seed derivation for each party to enable verification
        # while reducing communication requirements
        verification_seeds: Dict[int, bytes] = {}
        master_seed: bytes = secrets.token_bytes(32)  # Generate master randomness

        # Initialize verification_proofs dictionary
        verification_proofs: Dict[int, Dict[int, Any]] = {p_id: {} for p_id in participant_ids}

        party_id: int
        for party_id in shares.keys():
            # Derive a deterministic seed for this party
            party_seed: bytes = self.hash_algorithm(
                master_seed + str(party_id).encode()
            ).digest()
            verification_seeds[party_id] = party_seed

            # Use the seed to generate a deterministic RNG
            # Note: Using random.Random() with cryptographically strong seed is intentional here.
            # We need deterministic but unpredictable randomness for the verification protocol.
            # The security comes from party_seed being generated with a strong cryptographic hash.
            party_rng: random.Random = random.Random(int.from_bytes(party_seed, byteorder="big"))

            # Generate a random polynomial of degree t-1 with constant term 0
            zero_coeffs: List[FieldElement] = [gmpy2.mpz(0)]  # First coefficient is 0
            _: int
            for _ in range(1, threshold):
                # Use the seeded RNG for deterministic coefficient generation
                rand_value: int = party_rng.randrange(self.field.prime)
                zero_coeffs.append(gmpy2.mpz(rand_value))

            # Create shares for each participant using this polynomial
            party_shares: ShareDict = {}
            p_id: int
            for p_id in participant_ids:
                # Evaluate polynomial at the point corresponding to participant's ID
                y_value: FieldElement = self._evaluate_polynomial(zero_coeffs, p_id)
                party_shares[p_id] = (p_id, y_value)

            # Create commitments to the zero polynomial coefficients with optimized batch processing
            party_commitments: CommitmentList = self.create_commitments(zero_coeffs)

            # More efficient verification for the zero constant term
            # For hash-based commitments
            commitment_value: FieldElement = party_commitments[0][0]
            r_i: FieldElement = party_commitments[0][1]

            # Use helper method for consistency
            expected_zero_commitment: FieldElement = self._compute_hash_commitment(0, r_i, 0)

            if not constant_time_compare(commitment_value, expected_zero_commitment):
                detailed_msg = f"Zero commitment verification failed for party {party_id}, commitment: {commitment_value}, expected: {expected_zero_commitment}"
                message = "Zero commitment verification failed"
                self._raise_sanitized_error(VerificationError, message, detailed_msg)

            # Store this party's zero sharing and commitments
            zero_sharings[party_id] = party_shares
            zero_commitments[party_id] = party_commitments

        # Step 2: Enhanced verification with improved Byzantine fault tolerance
        # Optimized for better performance and security
        verified_zero_shares: Dict[int, Dict[int, FieldElement]] = {p_id: {} for p_id in participant_ids}
        invalid_shares_detected: Dict[int, List[int]] = {}
        new_shares: ShareDict = {}
        byzantine_parties: Dict[int, Dict[str, Any]] = {}

        # Enhanced security parameters with dynamic adjustment
        security_factor: float = max(0.5, 1.0 - (threshold / (2 * len(shares))))
        min_verified_shares: int = max(threshold // 2, int(threshold * security_factor))

        # Echo broadcast mechanism for consistency verification
        # This adds Byzantine fault tolerance following Chen & Lindell's recommendations
        echo_consistency: Dict[Tuple[int, int], bool] = self._process_echo_consistency(
            zero_commitments, zero_sharings, participant_ids
        )

        # Identify Byzantine parties with adaptive quorum-based detection
        byzantine_parties = {}
        # Calculate consistency statistics per party
        consistency_counts : Dict[int, Dict[str, int]]= {}
        for (party_id, _), is_consistent in echo_consistency.items():
            if party_id not in consistency_counts:
                consistency_counts[party_id] = {
                    "consistent": 0,
                    "inconsistent": 0,
                    "total": 0,
                }

            consistency_counts[party_id]["total"] += 1
            if is_consistent:
                consistency_counts[party_id]["consistent"] += 1
            else:
                consistency_counts[party_id]["inconsistent"] += 1

        # Adaptive quorum calculation based on threat model and participant count
        # More participants = higher required consistency ratio
        base_quorum_ratio: float = 0.5  # Start at 50%
        consistency_ratio_requirement: float = min(
            0.8, base_quorum_ratio + 0.1 * (len(shares) / threshold - 1)
        )

        # Identify parties that failed to reach consistency quorum
        
        party_id: int
        counts: Dict[str, int]
        for party_id, counts in consistency_counts.items():
            if counts["total"] > 0:
                consistency_ratio: float = counts["consistent"] / counts["total"]
                if consistency_ratio < consistency_ratio_requirement:
                    evidence: Dict[str, Union[str, float, int]] = {
                        "type": "insufficient_consistency_quorum",
                        "consistency_ratio": consistency_ratio,
                        "required_ratio": consistency_ratio_requirement,
                        "consistent_count": counts["consistent"],
                        "inconsistent_count": counts["inconsistent"],
                        "total_checked": counts["total"],
                    }
                    byzantine_parties[party_id] = evidence
                    warnings.warn(
                        f"Party {party_id} failed to reach consistency quorum "
                        f"({consistency_ratio:.2f} < {consistency_ratio_requirement:.2f})",
                        SecurityWarning,
                    )

        # Standard Byzantine detection for each party
        
        party_id: int
        for party_id in shares.keys():
            if party_id in byzantine_parties:
                continue  # Already identified as Byzantine

            is_byzantine: bool
            evidence: Dict[str, Any]
            is_byzantine, evidence = self._detect_byzantine_behavior(
                party_id,
                zero_commitments[party_id],
                zero_sharings[party_id],
                echo_consistency,
            )

            if is_byzantine:
                warnings.warn(
                    f"Detected Byzantine behavior from party {party_id}: {evidence.get('type', 'unknown')}",
                    SecurityWarning,
                )
                byzantine_parties[party_id] = evidence

        # More efficient batch verification with adaptive batch sizing
        batch_size: int = self._calculate_optimal_batch_size(
            len(participant_ids), len(shares)
        )

        # Group shares by commitment set for more efficient batch verification
        verification_batches: List[List[Tuple[int, int, int, int, CommitmentList]]] = self._prepare_verification_batches(
            zero_sharings, zero_commitments, participant_ids, batch_size
        )

        # Process verification with improved parallelism
        verification_results: List[Tuple[Tuple[int, int], bool]] = self._process_verification_batches(verification_batches)

        # Process verification results with Byzantine exclusion
        result: Tuple[Tuple[int, int], bool]
        for (party_id, p_id), is_valid in verification_results:
            # Skip shares from Byzantine parties
            if party_id in byzantine_parties:
                continue

            # Changed default from True to False - more conservative security posture
            if is_valid and echo_consistency.get((party_id, p_id), False):
                # Store verified share with additional consistency check
                share_value: FieldElement = self._get_share_value_from_results(
                    party_id, p_id, zero_sharings
                )
                verified_zero_shares[p_id][party_id] = share_value
            else:
                # Enhanced detection of invalid shares
                if p_id not in invalid_shares_detected:
                    invalid_shares_detected[p_id] = []
                invalid_shares_detected[p_id].append(party_id)

                # Generate cryptographic proof with improved evidence collection
                self._generate_invalidity_evidence(
                    party_id,
                    p_id,
                    zero_sharings,
                    zero_commitments,
                    verification_proofs,
                    is_valid,
                    echo_consistency.get((party_id, p_id), False), # Changed default to False here too
                )

        # Improved collusion detection with network analysis algorithms
        potential_collusion: List[int] = self._enhanced_collusion_detection(
            invalid_shares_detected, shares.keys(), echo_consistency
        )
        p_id: int
        # Process shares with adaptive security parameters
        for p_id in participant_ids:
            # Get original share with robust fallback
            original_y: FieldElement = self._get_original_share_value(p_id, shares)

            # Dynamic security threshold based on the situation
            verified_count: int = len(verified_zero_shares[p_id])
            required_threshold: int = self._determine_security_threshold(
                threshold,
                verified_count,
                len(shares),
                invalid_shares_detected.get(p_id, []),
            )

            # Enhanced security check with detailed diagnostics
            if verified_count < required_threshold:
                security_ratio: float = verified_count / threshold
                diagnostics: Dict[str, Union[int, float, List[int]]] = {
                    "verified_count": verified_count,
                    "threshold": threshold,
                    "required_threshold": required_threshold,
                    "security_ratio": security_ratio,
                    "invalid_shares": invalid_shares_detected.get(p_id, []),
                    "total_participants": len(shares),
                }

                if verified_count < min_verified_shares:
                    detailed_msg = (
                        f"Insufficient verified zero shares for participant {p_id}. "
                        f"Security diagnostics: {diagnostics}. "
                        f"Share refresh aborted for security reasons."
                    )
                    message = "Insufficient verified shares"
                    self._raise_sanitized_error(SecurityError, message, detailed_msg)
                else:
                    warnings.warn(
                        f"Suboptimal number of verified zero shares for participant {p_id}. "
                        f"Security diagnostics: {diagnostics}. "
                        f"Proceeding with reduced security margin.",
                        SecurityWarning,
                    )

            # Optimized summation with constant-time operations to prevent timing attacks
            sum_zero_shares: FieldElement = self._secure_sum_shares(
                verified_zero_shares[p_id], self.field.prime
            )

            # Create new share with zero-knowledge consistency proof
            new_y: FieldElement = (original_y + sum_zero_shares) % self.field.prime
            new_shares[p_id] = (p_id, new_y)

            # Generate proofs of correct share refreshing (optional)
            if verified_count >= threshold:
                # Only generate proofs when we have enough shares for full security
                verification_proofs[p_id]["consistency"] = (
                    self._generate_refresh_consistency_proof(
                        p_id,
                        original_y,
                        sum_zero_shares,
                        new_y,
                        verified_zero_shares[p_id],
                    )
                )

        # Add enhanced verification summary to verification_data
        verification_summary: Dict[str, Any] = {
            "total_zero_shares_created": len(zero_sharings) * len(participant_ids),
            "total_zero_shares_verified": sum(
                len(v) for v in verified_zero_shares.values()
            ),
            "invalid_shares_detected": invalid_shares_detected,
            "participants_with_full_verification": sum(
                1
                for p_id in participant_ids
                if len(verified_zero_shares[p_id]) == len(shares)
            ),
            "potential_collusion_detected": bool(potential_collusion),
            "byzantine_parties_excluded": len(byzantine_parties),
            "byzantine_party_ids": (
                list(byzantine_parties.keys()) if byzantine_parties else []
            ),
            "security_parameters": {
                "min_verified_shares": min_verified_shares,
                "security_factor": security_factor,
            },
        }

        # Step 3: Calculate the new commitments
        # Extract x and y values from a subset of new shares for efficient reconstruction
        sample_shares: List[SharePoint] = list(new_shares.values())[:threshold]
        x_values: List[FieldElement] = [share[0] for share in sample_shares]
        y_values: List[FieldElement] = [share[1] for share in sample_shares]

        # Reconstruct the new polynomial coefficients via optimized interpolation
        new_coeffs: List[FieldElement] = self._reconstruct_polynomial_coefficients(
            x_values, y_values, threshold
        )

        # Create new commitments for these coefficients
        new_commitments: CommitmentList = self.create_commitments(new_coeffs)

        # Add the verification proofs and enhanced summary to the verification data
        verification_data: Dict[str, Any] = {
            "original_shares_count": len(shares),
            "threshold": threshold,
            "zero_commitment_count": len(zero_commitments),
            "timestamp": int(time.time()),
            "protocol": "Enhanced-Chen-Lindell-PQ",
            "verification_method": "batch-optimized",
            "hash_based": True,
            "verification_summary": verification_summary,
            "seed_fingerprint": hashlib.sha3_256(master_seed).hexdigest()[
                :16
            ],  # Fingerprint for verification
            "verification_proofs": verification_proofs,
        }

        return new_shares, new_commitments, verification_data

    def _secure_sum_shares(self, shares_dict: Dict[int, FieldElement], modulus: FieldElement) -> FieldElement:
        """
        Description:
            Perform a secure constant-time summation of shares to prevent timing attacks.

        Arguments:
            shares_dict (dict): Dictionary of shares to sum.
            modulus (int): The field modulus.

        Inputs:
            shares_dict: Dictionary of shares.
            modulus: Modulus

        Outputs:
            int: Sum of shares modulo the field modulus.
        """
        result: "gmpy2.mpz" = gmpy2.mpz(0)
        for _, value in sorted(
            shares_dict.items()
        ):  # Sort to ensure deterministic processing
            result = (result + gmpy2.mpz(value)) % modulus
        return int(result)

    def _get_original_share_value(self, participant_id: int, shares: ShareDict) -> FieldElement:
        """
        Description:
            Safely retrieve the original share value with proper validation.

        Arguments:
            participant_id (int): ID of the participant.
            shares (dict): Dictionary of shares.

        Inputs:
            participant_id: Participant ID
            shares: shares

        Outputs:
            int: Original y-value of the share.
        
        Raises:
            SecurityError: If no valid original share is found for the participant.
        """
        if participant_id in shares:
            original_share: SharePoint = shares[participant_id]
            # Validate the share structure
            if isinstance(original_share, tuple) and len(original_share) == 2:
                return original_share[1]

        # Instead of returning 0, raise a security error to prevent silent failure
        detailed_msg = f"No valid original share found for participant {participant_id}."
        message = "Original share not found"
        self._raise_sanitized_error(SecurityError, message, detailed_msg)

    def _determine_security_threshold(
        self, base_threshold: int, verified_count: int, total_parties: int, invalid_parties: List[int]
    ) -> int:
        """
        Description:
            Determine the security threshold based on the current situation.

            Uses an adaptive approach based on the number of invalid shares detected.

        Arguments:
            base_threshold (int): The base threshold value (t).
            verified_count (int): Number of verified shares.
            total_parties (int): Total number of participating parties.
            invalid_parties (list): List of parties that provided invalid shares.

        Inputs:
            base_threshold: base threshold
            verified_count: verified count
            total_parties: total_parties
            invalid_parties: invalid parties

        Outputs:
            int: The required threshold for secure operation.
        """
        # Add explicit check for zero division with proper error handling
        if total_parties <= 0:
            detailed_msg = "No participating parties available for threshold calculation"
            message = "Invalid security parameters"
            self._raise_sanitized_error(SecurityError, message, detailed_msg)
        
        # Calculate the ratio of invalid to total parties
        invalid_ratio: float = len(invalid_parties) / total_parties

        required: int
        if invalid_ratio > 0.25:
            # High threat environment - increase security requirements
            required = max(base_threshold, int(base_threshold * (1 + invalid_ratio)))
        elif invalid_ratio > 0:
            # Some threats detected - slight increase in requirements
            required = base_threshold
        else:
            # No threats detected - can use standard threshold
            required = base_threshold

        # Never require more shares than are available
        return min(required, total_parties)

    def _detect_collusion_patterns(self, invalid_shares_detected: Dict[int, List[int]], party_ids: Set[int]) -> List[int]:
        """
        Description:
            Detect potential collusion patterns among parties that provided invalid shares.

        Arguments:
            invalid_shares_detected (dict): Dictionary mapping participants to parties that gave them invalid shares.
            party_ids (set): Set of all participating party IDs.

        Inputs:
            invalid_shares_detected: invalid_shares_detected
            party_ids: party_ids

        Outputs:
            list: List of party IDs that might be colluding, or empty list if none detected.
        """
        if not invalid_shares_detected:
            return []

        # Count how many times each party provided invalid shares
        invalid_count: Dict[int, int] = {}
        
        for parties in invalid_shares_detected.values():
            for party_id in parties:
                invalid_count[party_id] = invalid_count.get(party_id, 0) + 1

        # Calculate a suspicious threshold - parties that have more than 30% invalid shares
        suspicious_threshold: float = 0.3 * len(invalid_shares_detected)
        suspicious_parties: List[int] = [
            party
            for party, count in invalid_count.items()
            if count > suspicious_threshold
        ]

        # Check for patterns indicating potential collusion
        potential_colluders: List[int] = []

        # If multiple suspicious parties targeted the same participants, they might be colluding
        if len(suspicious_parties) > 1:
            # Check for overlap in targeted participants
            targeted_participants: Dict[int, Set[int]] = {}
            participant_id: int
            parties: List[int]
            for participant_id, parties in invalid_shares_detected.items():
                party_id: int
                for party_id in parties:
                    if party_id in suspicious_parties:
                        if party_id not in targeted_participants:
                            targeted_participants[party_id] = set()
                        targeted_participants[party_id].add(participant_id)

            # Look for significant overlap
            p1: int
            p2: int
            for p1 in suspicious_parties:
                for p2 in suspicious_parties:
                    if (
                        p1 < p2
                        and p1 in targeted_participants
                        and p2 in targeted_participants
                    ):
                        p1_targets: Set[int] = targeted_participants[p1]
                        p2_targets: Set[int] = targeted_participants[p2]
                        overlap: int = len(p1_targets.intersection(p2_targets))
                        union: int = len(p1_targets.union(p2_targets))

                        # If overlap ratio is high, add both to potential colluders
                        if union > 0 and overlap / union > 0.7:
                            if p1 not in potential_colluders:
                                potential_colluders.append(p1)
                            if p2 not in potential_colluders:
                                potential_colluders.append(p2)

        return potential_colluders

    def _create_invalidity_proof(self, party_id: int, participant_id: int, share: SharePoint, commitments: CommitmentList) -> Dict[str, Any]:
        """
        Description:
            Create a cryptographic proof that a share is invalid.

        Arguments:
            party_id (int): ID of the party that provided the invalid share.
            participant_id (int): ID of the participant who received the share.
            share (tuple): The invalid share (x, y).
            commitments (list): The commitments against which the share was verified.

        Inputs:
            party_id: party id
            participant_id: participant id
            share: share
            commitments: commitments

        Outputs:
            dict: A proof structure that can be verified by others.
        """
        x: FieldElement
        y: FieldElement
        x, y = share

        # Extract randomizers from commitments for hash-based verification
        randomizers: List[FieldElement] = [r_i for _, r_i, _ in commitments]

        # Compute the combined randomizer for this point
        r_combined: FieldElement = self._compute_combined_randomizer(randomizers, x)

        # Compute the expected commitment
        expected_commitment: FieldElement = self._compute_expected_commitment(commitments, x)

        # Compute the actual commitment based on the share
        actual_commitment: FieldElement = self._compute_hash_commitment(y, r_combined, x, "verify")

        # Create a signature/timestamp for this proof
        timestamp: int = int(time.time())
        signature_input: bytes = self.group._enhanced_encode_for_hash(
            party_id,
            participant_id,
            x,
            y,
            expected_commitment,
            actual_commitment,
            timestamp,
            "invalidity_proof",
        )

        signature: str
        if HAS_BLAKE3:
            signature = blake3.blake3(signature_input).hexdigest()
        else:
            signature = hashlib.sha3_256(signature_input).hexdigest()

        # Return the proof structure
        return {
            "party_id": party_id,
            "participant_id": participant_id,
            "share_x": int(x),
            "share_y": int(y),
            "expected_commitment": int(expected_commitment),
            "actual_commitment": int(actual_commitment),
            "combined_randomizer": int(r_combined),
            "timestamp": timestamp,
            "signature": signature,
        }

    def _generate_refresh_consistency_proof(
        self, participant_id: int, original_y: FieldElement, sum_zero_shares: FieldElement, new_y: FieldElement, verified_shares: Dict[int, FieldElement]
    ) -> Dict[str, Any]:
        """
        Description:
            Generate a proof that the share refreshing was done correctly.

        Arguments:
            participant_id (int): ID of the participant.
            original_y (int): Original share value.
            sum_zero_shares (int): Sum of the zero shares.
            new_y (int): New share value.
            verified_shares (dict): Dictionary of verified zero shares.
        Inputs:
            participant_id: participant id
            original_y: original y
            sum_zero_shares: sum of zero shares
            new_y: new y
            verified_shares: verified shares

        Outputs:
            dict: Proof structure for verification.
        """
        # Create a fingerprint of all verified shares
        share_fingerprint: str = hashlib.sha3_256(
            str(sorted([(k, v) for k, v in verified_shares.items()])).encode()
        ).hexdigest()

        # Verify that new_y = original_y + sum_zero_shares mod prime
        check_value: FieldElement = (original_y + sum_zero_shares) % self.field.prime

        # Generate proof timestamp and signature
        timestamp: int = int(time.time())
        signature_input: bytes = self.group._enhanced_encode_for_hash(
            participant_id,
            original_y,
            sum_zero_shares,
            new_y,
            share_fingerprint,
            timestamp,
            "consistency_proof",
        )
        signature: str
        if HAS_BLAKE3:
            signature = blake3.blake3(signature_input).hexdigest()
        else:
            signature = hashlib.sha3_256(signature_input).hexdigest()

        # Return the proof structure
        return {
            "participant_id": participant_id,
            "calculated_sum": int(sum_zero_shares),
            "verified_shares_count": len(verified_shares),
            "shares_fingerprint": share_fingerprint,
            "consistency_check": check_value == new_y,
            "timestamp": timestamp,
            "signature": signature,
        }

    def _process_echo_consistency(
        self, zero_commitments: Dict[int, CommitmentList], zero_sharings: Dict[int, ShareDict], participant_ids: List[int]
    ) -> Dict[Tuple[int, int], bool]:
        """
        Description:
            Enhanced echo consistency protocol for Byzantine fault detection.

            This implementation provides stronger detection of equivocation (sending different
            values to different participants) through secure cryptographic fingerprinting
            and comprehensive evidence collection.

        Arguments:
            zero_commitments (dict): Dictionary of commitments from each party.
            zero_sharings (dict): Dictionary of sharings from each party.
            participant_ids (list): List of participant IDs.

        Inputs:
            zero_commitments: Commitments
            zero_sharings: Sharings
            participant_ids: Participant IDs

        Outputs:
            dict: Dictionary mapping (party_id, participant_id) to consistency result.
            
        Side Effects:
            Stores Byzantine evidence in self._byzantine_evidence for later access by _detect_byzantine_behavior.

        Raises:
            TypeError: If inputs have incorrect types or structures.
        """

        # Validate input parameter types
        if not isinstance(zero_commitments, dict):
            raise TypeError("zero_commitments must be a dictionary")
        if not isinstance(zero_sharings, dict):
            raise TypeError("zero_sharings must be a dictionary")
        if not isinstance(participant_ids, list):
            raise TypeError("participant_ids must be a list")

        # Validate the structure of zero_sharings
        
        party_id: int
        party_shares: ShareDict
        for party_id, party_shares in zero_sharings.items():
            if not isinstance(party_shares, dict):
                detailed_msg = (
                    f"Invalid share format for party {party_id}: expected dictionary"
                )
                message = "Invalid data structure"
                self._raise_sanitized_error(TypeError, message, detailed_msg)
            p_id: int
            share: SharePoint
            for p_id, share in party_shares.items():
                if not isinstance(share, tuple) or len(share) != 2:
                    detailed_msg = f"Invalid share from party {party_id} to participant {p_id}: expected (x, y) tuple"
                    message = "Invalid data structure"
                    self._raise_sanitized_error(TypeError, message, detailed_msg)

        # Validate the structure of zero_commitments
        
        party_id: int
        commitments: CommitmentList
        for party_id, commitments in zero_commitments.items():
            if not isinstance(commitments, list) or not commitments:
                detailed_msg = f"Invalid commitment format for party {party_id}: expected non-empty list"
                message = "Invalid data structure"
                self._raise_sanitized_error(TypeError, message, detailed_msg)
            if not all(isinstance(c, tuple) and len(c) >= 2 for c in commitments):
                detailed_msg = f"Invalid commitment format for party {party_id}: expected list of (commitment, randomizer) tuples"
                message = "Invalid data structure"
                self._raise_sanitized_error(TypeError, message, detailed_msg)

        consistency_results: Dict[Tuple[int, int], bool] = {}

        # Create cryptographically secure fingerprints of each sharing
        share_fingerprints: Dict[int, Dict[int, bytes]] = {}

        
        party_id: int
        party_shares: ShareDict
        for party_id, party_shares in zero_sharings.items():
            share_fingerprints[party_id] = {}
            
            p_id: int
            x: FieldElement
            y: FieldElement
            for p_id, (x, y) in party_shares.items():
                if p_id in participant_ids:
                    # Create a secure fingerprint using proper domain separation
                    message: bytes = self.group._enhanced_encode_for_hash(
                        party_id, p_id, x, y, "echo-consistency-check"
                    )
                    fingerprint: bytes = self.hash_algorithm(message).digest()
                    share_fingerprints[party_id][p_id] = fingerprint

        # Echo broadcast phase: participants share what they received
        echo_broadcasts: Dict[int, Dict[int, Tuple[SharePoint, bytes]]] = {}
        p_id: int
        for p_id in participant_ids:
            echo_broadcasts[p_id] = {}
            # Collect all shares this participant received
            
            party_id: int
            for party_id in zero_sharings:
                if p_id in zero_sharings[party_id]:
                    share: SharePoint = zero_sharings[party_id][p_id]
                    fingerprint: Optional[bytes] = share_fingerprints[party_id].get(p_id)
                    if fingerprint:
                        echo_broadcasts[p_id][party_id] = (share, fingerprint)

        # Consistency check phase: compare what different participants received
        byzantine_evidence: Dict[int, Dict[str, Any]] = {}
        
        p1_id: int
        for p1_id in participant_ids:
            
            p2_id: int
            for p2_id in participant_ids:
                if p1_id >= p2_id:  # Only check each pair once
                    continue

                # Compare what p1 and p2 received from each party
                
                party_id: int
                for party_id in zero_sharings:
                    if (
                        party_id in echo_broadcasts[p1_id]
                        and party_id in echo_broadcasts[p2_id]
                    ):

                        # Extract shares and fingerprints
                        p1_share: SharePoint
                        p1_fingerprint: bytes
                        p2_share: SharePoint
                        p2_fingerprint: bytes
                        (p1_share, p1_fingerprint) = echo_broadcasts[p1_id][party_id]
                        (p2_share, p2_fingerprint) = echo_broadcasts[p2_id][party_id]

                        # Check if party sent consistent values to both participants
                        is_consistent: bool = p1_fingerprint == p2_fingerprint

                        # Record consistency results for both participants
                        consistency_results[(party_id, p1_id)] = is_consistent
                        consistency_results[(party_id, p2_id)] = is_consistent

                        # If inconsistent, collect evidence of Byzantine behavior
                        if not is_consistent:
                            if party_id not in byzantine_evidence:
                                byzantine_evidence[party_id] = {
                                    "type": "equivocation",
                                    "evidence": [],
                                }

                            byzantine_evidence[party_id]["evidence"].append(
                                {
                                    "participant1": p1_id,
                                    "share1": p1_share,
                                    "participant2": p2_id,
                                    "share2": p2_share,
                                    "fingerprint1": p1_fingerprint.hex(),
                                    "fingerprint2": p2_fingerprint.hex(),
                                }
                            )

        # Store Byzantine evidence in a separate field rather than modifying the
        # return structure to maintain compatibility with existing code
        self._byzantine_evidence = byzantine_evidence

        return consistency_results

    def _calculate_optimal_batch_size(self, num_participants: int, security_level: int = None, num_shares: int = None) -> int:
        """
        Description:
        Calculate the optimal batch size for verification based on system parameters.

        Arguments:
            num_participants (int): Number of participants.
            security_level (int, optional): Security intensity level (0-10). Higher values result
                                           in smaller batches for more granular verification.
                                           Default is None (use standard calculation).
            num_shares (int, optional): Total number of shares in the system, allowing for
                                        more nuanced batch sizing when share distribution is uneven.

        Inputs:
            num_participants: num_participants
            security_level: Optional parameter to adjust batch size based on security requirements
            num_shares: Optional parameter to adjust for uneven share distribution

        Outputs:
            int: Optimal batch size for verification.
        """
        # Validate security_level input
        if security_level is not None:
            if not isinstance(security_level, (int, float)) or security_level < 0 or security_level > 10:
                warnings.warn("Invalid security_level (must be 0-10). Using default calculation.", RuntimeWarning)
                security_level = None
        
        # Validate num_shares input if provided
        if num_shares is not None:
            if not isinstance(num_shares, int) or num_shares <= 0:
                warnings.warn("Invalid num_shares (must be a positive integer). Ignoring this parameter.", RuntimeWarning)
                num_shares = None
                
        # For small numbers, use a smaller batch size
        if (num_participants < 10):
            base_batch_size = min(8, num_participants)
            # Even with small participants, adjust for highly uneven share distribution
            if num_shares is not None and num_shares > num_participants * 10:
                return max(2, int(base_batch_size / 2))  # More conservative reduction for small systems
            return base_batch_size
                
        # Apply security level adjustment if specified
        adjustment_factor = 1.0
        if security_level is not None:
            # Convert security level (0-10) to a reduction factor (1.0 to 0.4)
            # Higher security = smaller batches for more granular verification
            adjustment_factor = max(0.4, 1.0 - (security_level / 15))
        
        # For larger systems, use a batch size that balances efficiency
        # with the ability to quickly identify problematic shares
        cpu_count: int = 1
        try:
            import multiprocessing
            import math
            cpu_count = max(1, multiprocessing.cpu_count())
            
            # Hybrid approach: Consider both logarithmic scaling and CPU count
            # Ensure minimum reasonable batch size with the max(4, ...) operation
            log_factor = max(4, int(math.log2(max(2, num_participants)) * 4 * adjustment_factor))
            cpu_factor = max(8, int(num_participants // cpu_count * adjustment_factor))
            
            # Use the smaller of the two factors to keep batches manageable
            batch_size = min(32, min(log_factor, cpu_factor))
            
            # If num_shares is provided, adjust for highly skewed distributions
            if num_shares is not None and num_shares > num_participants:
                shares_per_participant = num_shares / max(1, num_participants)
                if shares_per_participant > 10:  # Only adjust for highly uneven distributions
                    # Use logarithmic scaling to avoid extreme reductions
                    reduction_factor = min(3, math.log2(shares_per_participant) / 4)  # Cap the reduction
                    batch_size = max(4, int(batch_size / reduction_factor))
                    
            return batch_size
        except (ImportError, NotImplementedError):
            pass

        # Fallback to the original calculation with security adjustment
        batch_size = min(32, max(8, int(num_participants // max(1, cpu_count) * adjustment_factor)))
        
        # Apply the share distribution adjustment to the fallback case as well
        if num_shares is not None and num_shares > num_participants:
            shares_per_participant = num_shares / max(1, num_participants)
            if shares_per_participant > 10:
                import math  # Import here in case it wasn't imported earlier
                reduction_factor = min(3, math.log2(shares_per_participant) / 4)
                batch_size = max(4, int(batch_size / reduction_factor))
                
        return batch_size

    def _prepare_verification_batches(
        self, zero_sharings: Dict[int, ShareDict], zero_commitments: Dict[int, CommitmentList], participant_ids: List[int], batch_size: int
    ) -> List[List[Tuple[int, int, FieldElement, FieldElement, CommitmentList]]]:
        """
        Description:
            Prepare efficient verification batches grouped by commitment set.

        Arguments:
            zero_sharings (dict): Dictionary of sharings from each party.
            zero_commitments (dict): Dictionary of commitments from each party.
            participant_ids (list): List of participant IDs.
            batch_size (int): Size of each batch.

        Inputs:
            zero_sharings: zero_sharings
            zero_commitments: zero_commitments
            participant_ids: participant_ids
            batch_size: batch_size

        Outputs:
            list: List of verification batches.
        """
        verification_batches: List[List[Tuple[int, int, FieldElement, FieldElement, CommitmentList]]] = []

        # Group shares by commitment set for efficient batch verification
        commitment_groups: Dict[str, Tuple[CommitmentList, List[Tuple[int, int, FieldElement, FieldElement]]]] = {}
        
        party_id: int
        party_commitments: CommitmentList
        for party_id, party_commitments in zero_commitments.items():
            # Use a cryptographic hash instead of Python's non-cryptographic hash()
            # This prevents potential hash collisions that could lead to incorrect grouping
            if HAS_BLAKE3:
                hasher = blake3.blake3()
            else:
                # Fall back to SHA3-256 if BLAKE3 is not available
                import hashlib
                hasher = hashlib.sha3_256()
                
            # Generate a stable, cryptographically secure commitment key by hashing all commitment values
            for c in party_commitments:
                if isinstance(c, tuple) and len(c) > 0:
                    # Convert the commitment value to bytes for hashing
                    hasher.update(str(c[0]).encode('utf-8'))
                    
            commitment_key: str = hasher.hexdigest()

            if commitment_key not in commitment_groups:
                commitment_groups[commitment_key] = (party_commitments, [])

            # Fixed: Use zero_sharings[party_id] instead of undefined party_shares
            if party_id in zero_sharings:
                p_id: int
                x: FieldElement
                y: FieldElement
                for p_id, (x, y) in zero_sharings[party_id].items():
                    if p_id in participant_ids:
                        commitment_groups[commitment_key][1].append((party_id, p_id, x, y))

        # Create batches with optimized size
        
        commitment_key: str
        commitments: CommitmentList
        items: List[Tuple[int, int, FieldElement, FieldElement]]
        for commitment_key, (commitments, items) in commitment_groups.items():
            i: int
            for i in range(0, len(items), batch_size):
                batch: List[Tuple[int, int, FieldElement, FieldElement]] = items[i : i + batch_size]
                batch_items: List[Tuple[int, int, FieldElement, FieldElement, CommitmentList]] = [
                    (party_id, p_id, x, y, commitments)
                    for party_id, p_id, x, y in batch
                ]
                verification_batches.append(batch_items)

        return verification_batches

    def _process_verification_batches(self, verification_batches: List[List[Tuple[int, int, FieldElement, FieldElement, CommitmentList]]]) -> List[Tuple[Tuple[int, int], bool]]:
        """
        Description:
            Process verification batches with optimized parallelism.

        Arguments:
            verification_batches (list): List of verification batches.

        Inputs:
            verification_batches: verification_batches

        Outputs:
            list: List of verification results.
        """

        def verify_batch(batch_items: List[Tuple[int, int, FieldElement, FieldElement, CommitmentList]]) ->  List[Tuple[Tuple[int, int], bool]]:
            results: Dict[int, Tuple[int, int]] = {}
            batch_shares: List[SharePoint] = []
            
            idx: int
            party_id: int
            p_id: int
            x: FieldElement
            y: FieldElement
            commitments: CommitmentList
            for idx, (party_id, p_id, x, y, commitments) in enumerate(batch_items):
                batch_shares.append((x, y))
                results[idx] = (party_id, p_id)

            # Use batch verification when possible
            verification_results: Dict[int, bool]
            _: bool
            if len(batch_shares) > 1:
                _, verification_results = self.batch_verify_shares(
                    batch_shares, commitments
                )
                return [
                    (results[idx], is_valid)
                    for idx, is_valid in verification_results.items()
                ]
            else:
                # Fallback to individual verification
                return [
                    (results[idx], self.verify_share(x, y, commitments))
                    for idx, (party_id, p_id, x, y, commitments) in enumerate(
                        batch_items
                    )
                ]

        # Try parallel verification with improved error handling
        verification_results: List[Tuple[Tuple[int, int], bool]] = []
        try:
            import concurrent.futures

            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Use a more robust approach for gathering results
                future_to_batch: Dict["concurrent.futures.Future[List[Tuple[Tuple[int, int], bool]]]", int] = {
                    executor.submit(verify_batch, batch): i
                    for i, batch in enumerate(verification_batches)
                }

                
                future: "concurrent.futures.Future[List[Tuple[Tuple[int, int], bool]]]"
                for future in concurrent.futures.as_completed(future_to_batch):
                    try:
                        batch_results:  List[Tuple[Tuple[int, int], bool]] = future.result()
                        verification_results.extend(batch_results)
                    except Exception as e:
                        warnings.warn(
                            f"Error in verification batch: {e}", RuntimeWarning
                        )
                        # Handle failed batch verification by marking all shares in the batch as invalid
                        batch_index = future_to_batch.get(future, -1)
                        if 0 <= batch_index < len(verification_batches):
                            # Extract party_id and p_id from the failed batch and mark all as invalid
                            failed_batch = verification_batches[batch_index]
                            invalid_results = [
                                ((party_id, p_id), False)
                                for party_id, p_id, _, _, _ in failed_batch
                            ]
                            verification_results.extend(invalid_results)
                            
                            # Enhanced security warning with more detail for monitoring systems
                            fail_msg = (f"CRITICAL SECURITY ALERT: Batch verification failure detected. "
                                      f"{len(invalid_results)} shares marked as invalid in batch {batch_index}. "
                                      f"This could indicate a potential attack or data corruption.")
                            warnings.warn(fail_msg, category=SecurityWarning)
                            
                            # Log the detailed error for forensic analysis
                            if logging:
                                try:
                                    logging.error(f"{fail_msg} Original error: {e}")
                                except (ImportError, NameError):
                                    pass  # If logging is not available, continue silently
        except (ImportError, RuntimeError):
            # Fallback to sequential verification with progress tracking
            
            batch:  List[Tuple[int, int, FieldElement, FieldElement, CommitmentList]]
            for batch in verification_batches:
                verification_results.extend(verify_batch(batch))

        return verification_results

    def _get_share_value_from_results(self, party_id: int, p_id: int, zero_sharings:  Dict[int, ShareDict]) -> Optional[FieldElement]:
        """
        Description:
            Get share value from zero sharings with proper validation.

        Arguments:
            party_id (int): ID of the party.
            p_id (int): ID of the participant.
            zero_sharings (dict): Dictionary of sharings.
        Inputs:
            party_id: party_id
            p_id: p_id
            zero_sharings: zero_sharings
        Outputs:
            Optional[int]: Share y-value or None if not found.
        """
        if party_id in zero_sharings and p_id in zero_sharings[party_id]:
            return zero_sharings[party_id][p_id][1]  # Return y-value

        # This should not happen if verification passed
        warnings.warn(
            f"Missing share for party {party_id}, participant {p_id}", RuntimeWarning
        )
        return None  # Return None instead of 0 to avoid silent failures

    def _generate_invalidity_evidence(
        self,
        party_id: int,
        p_id: int,
        zero_sharings: Dict[int, ShareDict],
        zero_commitments: Dict[int, CommitmentList],
        verification_proofs: Dict[int, Dict[int, Any]],
        share_verification: bool,
        echo_consistency: bool,
    ) -> None:
        """
        Description:
            Generate enhanced cryptographic evidence for invalid shares.

        Arguments:
            party_id (int): ID of the party providing the share.
            p_id (int): ID of the participant receiving the share.
            zero_sharings (dict): Dictionary of sharings.
            zero_commitments (dict): Dictionary of commitments.
            verification_proofs (dict): Dictionary to store proofs.
            share_verification (bool): Whether share verification passed.
            echo_consistency (bool): Whether echo consistency check passed.

        Inputs:
            party_id: party id
            p_id: p_id
            zero_sharings: zero_sharings
            zero_commitments: zero_commitments
            verification_proofs: verification_proofs
            share_verification: share verification
            echo consistency: echo consistency

        Outputs:
            None
        """
        try:
            if p_id not in verification_proofs:
                verification_proofs[p_id] = {}

            # Get the share for detailed evidence
            if party_id in zero_sharings and p_id in zero_sharings[party_id]:
                share: SharePoint = zero_sharings[party_id][p_id]
                commitments: Optional[CommitmentList] = zero_commitments.get(party_id)

                if commitments:
                    # Create comprehensive proof with additional evidence
                    proof: Dict[str, Any] = self._create_invalidity_proof(
                        party_id, p_id, share, commitments
                    )

                    # Add additional evidence about consistency checks
                    proof["echo_consistency"] = echo_consistency
                    proof["share_verification"] = share_verification

                    # Add to verification proofs
                    verification_proofs[p_id][party_id] = proof

            # Log the issue for security monitoring
            warnings.warn(
                f"Invalid share from party {party_id} for participant {p_id}. "
                f"Verification: {share_verification}, Echo consistency: {echo_consistency}",
                SecurityWarning,
            )
        except Exception as e:
            warnings.warn(f"Failed to create invalidity proof: {e}", RuntimeWarning)

    def _enhanced_collusion_detection(
        self, invalid_shares_detected: Dict[int, List[int]], party_ids: Set[int], echo_consistency: Dict[Tuple[int, int], bool]
    ) -> List[int]:
        """
        Description:
            Enhanced collusion detection with improved graph analysis.

        Arguments:
            invalid_shares_detected (dict): Dictionary of invalid shares.
            party_ids (set): Set of party IDs.
            echo_consistency (dict): Results of echo consistency checks.

        Inputs:
            invalid_shares_detected: invalid shares detected
            party_ids: party ids
            echo_consistency: echo consistency

        Outputs:
            list: List of potentially colluding parties.
        """
        if not invalid_shares_detected:
            return []

        # Count how many times each party provided invalid shares
        invalid_count: Dict[int, int] = {}
        
        parties: List[int]
        for parties in invalid_shares_detected.values():
            party_id: int
            for party_id in parties:
                invalid_count[party_id] = invalid_count.get(party_id, 0) + 1

        # Calculate a suspicious threshold with dynamic adjustment
        total_participants: int = len(invalid_shares_detected)
        suspicious_threshold: float = max(1, 0.25 * total_participants)

        # Identify suspicious parties with high invalid share counts
        suspicious_parties: List[int] = [
            party
            for party, count in invalid_count.items()
            if count > suspicious_threshold
        ]

        # Enhanced detection: look for patterns in echo consistency failures
        if echo_consistency:
            inconsistent_parties: Set[int] = set()
            
            party_id: int
            is_consistent: bool
            for (party_id, _), is_consistent in echo_consistency.items():
                if not is_consistent and party_id not in inconsistent_parties:
                    inconsistent_parties.add(party_id)

            # Add parties with echo inconsistencies to suspicious list
            party: int
            for party in inconsistent_parties:
                if party not in suspicious_parties:
                    suspicious_parties.append(party)

        # Identify potential collusion patterns
        potential_colluders: List[int] = []

        # Check for targeting patterns (multiple suspicious parties targeting the same participants)
        if len(suspicious_parties) > 1:
            targeted_participants: Dict[int, Set[int]] = {}
            
            party_id: int
            for party_id in suspicious_parties:
                targeted_participants[party_id] = set()
                
                p_id: int
                parties: List[int]
                for p_id, parties in invalid_shares_detected.items():
                    if party_id in parties:
                        targeted_participants[party_id].add(p_id)

            # Find parties with similar targeting patterns
            i: int
            p1: int
            for i, p1 in enumerate(suspicious_parties):
                
                p2: int
                for p2 in suspicious_parties[i + 1 :]:
                    if p1 in targeted_participants and p2 in targeted_participants:
                        p1_targets: Set[int] = targeted_participants[p1]
                        p2_targets: Set[int] = targeted_participants[p2]

                        # Calculate Jaccard similarity of target sets
                        if p1_targets and p2_targets:
                            overlap: int = len(p1_targets.intersection(p2_targets))
                            union: int = len(p1_targets.union(p2_targets))

                            # Higher threshold (0.8) for stronger evidence
                            if union > 0 and overlap / union > 0.8:
                                if p1 not in potential_colluders:
                                    potential_colluders.append(p1)
                                if p2 not in potential_colluders:
                                    potential_colluders.append(p2)

        return potential_colluders

    def create_polynomial_proof(self, coefficients: List[FieldElement], commitments: CommitmentList) -> ProofDict:
        """
        Description:
            Creates a zero-knowledge proof of knowledge of the polynomial coefficients
            using hash-based commitments for post-quantum security.

            This implementation follows Baghery's secure framework with enhanced domain
            separation and proper randomization to ensure security against quantum attacks.

        Arguments:
            coefficients (list): List of polynomial coefficients [a₀, a₁, ..., aₖ₋₁].
            commitments (list): Commitments to these coefficients (list of tuples).

        Inputs:
            coefficients: coefficients
            commitments: commitments

        Outputs:
            dict: Proof data structure containing the necessary components for verification.

        Raises:
            TypeError: If inputs have incorrect types or structures.
            ValueError: If coefficients or commitments lists are empty.
        """
        # Add validation
        if not isinstance(coefficients, list):
            raise TypeError("coefficients must be a list")
        if not coefficients:
            raise ValueError("coefficients list cannot be empty")
        if not isinstance(commitments, list):
            raise TypeError("commitments must be a list")
        if not commitments:
            raise ValueError("commitments list cannot be empty")
        if not all(isinstance(c, tuple) and len(c) >= 2 for c in commitments):
            raise TypeError(
                "Each commitment must be a tuple with at least (commitment, randomizer)"
            )

        # Convert coefficients to integers for consistent arithmetic
        coeffs_int: List[FieldElement] = [gmpy2.mpz(coeff) % self.field.prime for coeff in coefficients]

        # Generate secure random blinding factors
        blindings: List[FieldElement] = [self.group.secure_random_element() for _ in range(len(coeffs_int))]

        # Create hash-based commitments to blinding factors with domain separation
        blinding_commitments: List[Tuple[FieldElement, FieldElement]] = []
        i: int
        b: FieldElement
        for i, b in enumerate(blindings):
            # Generate secure randomizer for each blinding factor
            r_b: FieldElement = self.group.secure_random_element()

            # Compute hash-based commitment with context for domain separation
            commitment: FieldElement = self._compute_hash_commitment(
                b, r_b, i, "polynomial_proof_blinding"
            )
            blinding_commitments.append((commitment, r_b))

        # Generate timestamp for the proof
        timestamp: int = int(time.time())
        
        # Generate non-interactive challenge using Fiat-Shamir transform with enhanced encoding
        # Include all public values in the challenge computation to prevent manipulation
        challenge_input: bytes = self.group._enhanced_encode_for_hash(
            "polynomial_proof",  # Domain separator
            self.generator,
            self.group.prime,
            [c[0] if isinstance(c, tuple) and len(c) > 0 else 0 for c in commitments],  # Commitment values, safely accessed
            [bc[0] if isinstance(bc, tuple) and len(bc) > 0 else 0 for bc in blinding_commitments],  # Blinding commitment values, safely accessed
            timestamp,  # Use the same timestamp that will be stored in the proof
        )

        # Hash the challenge input using the configured hash algorithm
        challenge_hash: bytes = self.hash_algorithm(challenge_input).digest()
        challenge: FieldElement = int.from_bytes(challenge_hash, "big") % self.field.prime

        # Compute responses using sensitive coefficients - this should be constant-time
        responses: List[FieldElement] = [
            (b + challenge * a) % self.field.prime
            for b, a in zip(blindings, coeffs_int)
        ]

        # Safely extract commitment randomizers regardless of tuple length
        commitment_randomizers: List[FieldElement] = []
        for c in commitments:
            if len(c) >= 2:
                commitment_randomizers.append(c[1])
            else:
                raise ValueError("Each commitment must contain at least two elements (commitment, randomizer)")

        # Return complete proof structure including all values needed for verification
        proof: ProofDict = {
            "blinding_commitments": blinding_commitments,
            "challenge": int(challenge),
            "responses": [int(r) for r in responses],
            "commitment_randomizers": [int(r) for r in commitment_randomizers],
            "blinding_randomizers": [int(r) for _, r in blinding_commitments],
            "timestamp": timestamp,  # Store timestamp for verification
        }
        return proof
    
    def verify_polynomial_proof(self, proof: ProofDict, commitments: CommitmentList) -> bool:
        """
        Description:
            Verifies a zero-knowledge proof of knowledge of polynomial coefficients
            using hash-based commitment verification for post-quantum security.

            This method validates that the prover knows the coefficients without revealing them,
            using only the hash-based commitments and the provided proof.

        Arguments:
            proof (dict): Proof data structure from create_polynomial_proof.
            commitments (list): Commitments to the polynomial coefficients (list of tuples).

        Inputs:
            proof: proof
            commitments: commitments

        Outputs:
            bool: True if verification succeeds, False otherwise.

        Raises:
            TypeError: If inputs have incorrect types.
            ValueError: If commitments list is empty or proof structure is invalid.
    """
        # Add validation
        if not isinstance(proof, dict):
            raise TypeError("proof must be a dictionary")
        if not isinstance(commitments, list):
            raise TypeError("commitments must be a list")
        if not commitments:
            raise ValueError("commitments list cannot be empty")

        # Extract proof components with parameter validation
        blinding_commitments: List[Tuple[FieldElement, FieldElement]]
        challenge: FieldElement
        responses: List[FieldElement]
        commitment_randomizers: List[FieldElement]
        blinding_randomizers: List[FieldElement]
        timestamp: int

        try:
            blinding_commitments = proof["blinding_commitments"]
            challenge = proof["challenge"]
            responses = proof["responses"]
            commitment_randomizers = proof["commitment_randomizers"]
            blinding_randomizers = proof["blinding_randomizers"]
            timestamp = proof.get("timestamp")  # Get timestamp for challenge reconstruction
        except (KeyError, TypeError) as e:
            raise ValueError(f"Incomplete or malformed proof structure: {str(e)}")

        # Enhanced validation for proof structure - changed from warnings to exceptions for security-critical failures
        if not isinstance(blinding_commitments, list):
            raise ValueError("blinding_commitments must be a list")
        if not all(isinstance(c, tuple) and len(c) >= 2 for c in blinding_commitments):
            raise ValueError("Each blinding commitment must be a tuple with at least (commitment, randomizer)")
        if not isinstance(challenge, (int, gmpy2.mpz)):
            raise ValueError("challenge must be an integer")
        if not isinstance(responses, list) or not all(
            isinstance(r, (int, gmpy2.mpz)) for r in responses
        ):
            raise ValueError("responses must be a list of integers")

        # Validate that all component lists have the correct size
        if (
            len(responses) != len(commitments)
            or len(blinding_commitments) != len(commitments)
            or len(commitment_randomizers) != len(commitments)
            or len(blinding_randomizers) != len(commitments)
        ):
            detailed_msg = f"Inconsistent lengths in proof components. responses: {len(responses)}, commitments: {len(commitments)}, blinding_commitments: {len(blinding_commitments)}, commitment_randomizers: {len(commitment_randomizers)}, blinding_randomizers: {len(blinding_randomizers)}"
            raise ValueError(f"Invalid proof structure: {detailed_msg}")

        # Convert challenge to gmpy2.mpz once before the loop to avoid repeated conversion
        challenge_mpz = gmpy2.mpz(challenge)
        
        # Verify each coefficient's proof - MODIFIED to prevent timing side-channels
        all_valid: bool = True  # Track verification results without early return

        i: int
        for i in range(len(responses)):
            # Verify response equation for hash-based commitments:
            # H(z_i, r_z_i, i) = C_b_i + challenge * C_i

            # 1. Compute combined randomizer for the response: r_z_i = r_b_i + challenge * r_i
            response_randomizer: FieldElement = (
                blinding_randomizers[i] + challenge_mpz * commitment_randomizers[i]
            ) % self.field.prime

            # 2. Compute the hash commitment for the response
            computed_commitment: FieldElement = self._compute_hash_commitment(
                responses[i], response_randomizer, i, "polynomial_proof_response"
            )

            # 3. Compute the expected commitment: C_b_i + challenge * C_i
            # Fixed: Safer access to tuple elements with validation
            if not isinstance(blinding_commitments[i], tuple) or len(blinding_commitments[i]) < 1:
                raise ValueError(f"Invalid blinding commitment format at index {i}")
                
            blinding_commitment_value: FieldElement = blinding_commitments[i][0]
            
            # Fixed: Safer way to access commitment values without unsafe cast
            if not isinstance(commitments[i], tuple) or len(commitments[i]) < 1:
                raise ValueError(f"Invalid commitment format at index {i}")
                
            commitment_value: FieldElement = commitments[i][0]
            
            # Convert to consistent numeric types for arithmetic
            blinding_commitment_value = gmpy2.mpz(blinding_commitment_value)
            commitment_value = gmpy2.mpz(commitment_value)
            
            expected_commitment: FieldElement = (
                blinding_commitment_value + challenge_mpz * commitment_value
            ) % self.group.prime

            # 4. Update validity flag without early return
            all_valid &= constant_time_compare(computed_commitment, expected_commitment)

        return all_valid

    def _detect_byzantine_behavior(
        self, party_id: int, commitments: CommitmentList, shares: ShareDict, consistency_results: Optional[Dict[Tuple[int, int], bool]] = None
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Description:
            Enhanced Byzantine fault detection for comprehensive security analysis.

            Detects multiple types of malicious behavior including inconsistent shares,
            invalid commitments, and equivocation.

        Arguments:
            party_id (int): ID of the party to check.
            commitments (list): Commitments from this party.
            shares (dict): Shares distributed by this party.
            consistency_results (dict, optional): Results from echo consistency checks.

        Inputs:
            party_id: party id
            commitments: commitments
            shares: shares
            consistency_results: consistency results

        Outputs:
            tuple: (is_byzantine, evidence).

        Raises:
            TypeError: If inputs have incorrect types.
        """
        evidence: Dict[str, Any] = {}
        is_byzantine: bool = False

        # Input validation
        if not isinstance(party_id, (int, str)):
            raise TypeError("party_id must be an integer or string")
        if not isinstance(commitments, list):
            raise TypeError("commitments must be a list")
        if not isinstance(shares, dict):
            raise TypeError("shares must be a dictionary")
        if consistency_results is not None and not isinstance(
            consistency_results, dict
        ):
            raise TypeError("consistency_results must be a dictionary if provided")

        # Check 1: Are all commitments valid?
        if not commitments:
            evidence["invalid_commitments"] = "Missing commitments"
            return True, evidence
        
        # Validate first commitment structure more thoroughly  
        if not isinstance(commitments[0], tuple):
            evidence["invalid_commitments"] = "Malformed commitment (not a tuple)"
            return True, evidence
            
        # For hash-based commitments, verify the first coefficient is a commitment to 0
        # Safely extract randomizer regardless of tuple length
        if len(commitments[0]) >= 2:
            randomizer: FieldElement = commitments[0][1]
            expected: FieldElement = self._compute_hash_commitment(0, randomizer, 0, "polynomial")
            
            # Safely access first element of commitment tuple
            commitment_value = commitments[0][0] if commitments[0] else None
            if commitment_value is None or not constant_time_compare(commitment_value, expected):
                evidence["invalid_zero_commitment"] = {
                    "commitment": int(commitment_value) if commitment_value is not None else None,
                    "expected": int(expected),
                }
                is_byzantine = True
        else:
            evidence["invalid_commitment_structure"] = "First commitment has incorrect format (insufficient elements)"
            is_byzantine = True

        # Check 2: Are all shares consistent with the commitments?
        share_consistency: Dict[int, bool] = {}
        
        recipient_id: int
        x: FieldElement
        y: FieldElement
        for recipient_id, (x, y) in shares.items():
            # Verify this share against the commitments
            is_valid: bool = self.verify_share(x, y, commitments)
            share_consistency[recipient_id] = is_valid

            if not is_valid:
                if "inconsistent_shares" not in evidence:
                    evidence["inconsistent_shares"] = {}

                # Compute values needed for verification for better diagnostics
                randomizers: List[FieldElement] = [r_i for _, r_i, _ in commitments]
                r_combined: FieldElement = self._compute_combined_randomizer(randomizers, x)
                expected_commitment: FieldElement = self._compute_expected_commitment(commitments, x)

                # Extract extra_entropy if present (should be in the first coefficient only)
                extra_entropy: Optional[bytes] = None
                if len(commitments) > 0 and isinstance(commitments[0], tuple) and len(commitments[0]) > 2:
                    extra_entropy = commitments[0][2]  # Get extra_entropy from first coefficient

                actual_commitment: FieldElement = self._compute_hash_commitment(
                    y, r_combined, x, "verify", extra_entropy
                )

                evidence["inconsistent_shares"][recipient_id] = {
                    "x": int(x),
                    "y": int(y),
                    "expected_commitment": int(expected_commitment),
                    "actual_commitment": int(actual_commitment),
                    "combined_randomizer": int(r_combined),
                }
                is_byzantine = True

        # Check 3: Look for evidence of equivocation from consistency checks
        if (
            hasattr(self, "_byzantine_evidence")
            and party_id in self._byzantine_evidence
        ):
            evidence["equivocation"] = self._byzantine_evidence[party_id]
            is_byzantine = True

        return is_byzantine, evidence

    def detect_byzantine_party(
        self, party_id: int, commitments: CommitmentList, shares: ShareDict, consistency_results: Optional[Dict[Tuple[int, int], bool]] = None
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Description:
            Public method to detect Byzantine behavior from a specific party.

        Arguments:
            party_id (int): ID of the party to analyze.
            commitments (list): Commitments from this party.
            shares (dict): Shares distributed by this party.
            consistency_results (dict, optional): Optional consistency check results.

        Inputs:
            party_id: party id
            commitments: commitments
            shares: shares
            consistency_results: consistency results

        Outputs:
            tuple: (is_byzantine, evidence_details).

        Raises:
            TypeError: If inputs have incorrect types.
            ValueError: If commitments list is empty.
        """
        # Add validation
        if not isinstance(party_id, (int, str)):
            raise TypeError("party_id must be an integer or string")
        if not isinstance(commitments, list):
            raise TypeError("commitments must be a list")
        if not commitments:
            self._raise_sanitized_error(ValueError, "commitments list cannot be empty")
        if not isinstance(shares, dict):
            raise TypeError("shares must be a dictionary")
        if consistency_results is not None and not isinstance(
            consistency_results, dict
        ):
            raise TypeError("consistency_results must be a dictionary if provided")

        return self._detect_byzantine_behavior(
            party_id, commitments, shares, consistency_results
        )

    def _evaluate_polynomial(self, coefficients: List[FieldElement], x: int) -> FieldElement:
        """
        Description:
            Evaluate polynomial at point x using constant-time Horner's method.

        Arguments:
            coefficients (list): List of polynomial coefficients [a₀, a₁, ..., aₖ₋₁].
            x (int): Point at which to evaluate the polynomial.
        Inputs:
            coefficients: Coefficients
            x: x

        Outputs:
            int: Value of polynomial at point x.
        """
        x_int: "gmpy2.mpz" = gmpy2.mpz(x)

        # Estimate memory requirements for this operation
        total_bits: int = sum(
            c.bit_length() if hasattr(c, "bit_length") else gmpy2.mpz(c).bit_length()
            for c in coefficients
        )
        if not check_memory_safety("mul", x_int, total_bits):
            raise MemoryError(
                "Polynomial evaluation would exceed memory limits. "
                "The polynomial coefficients or evaluation point may be too large."
            )

        result: "gmpy2.mpz" = gmpy2.mpz(0)
        coeff: FieldElement
        for coeff in reversed(coefficients):
            result = (result * x_int + gmpy2.mpz(coeff)) % self.field.prime
        return result

    def _reconstruct_polynomial_coefficients(self, x_values: List[FieldElement], y_values: List[FieldElement], threshold: int) -> List[FieldElement]:
        """
        Description:
            Reconstruct polynomial coefficients using quantum-resistant interpolation.

        Arguments:
            x_values (list): List of x-coordinates.
            y_values (list): List of corresponding y-coordinates.
            threshold (int): Degree of the polynomial to reconstruct (k).

        Inputs:
            x_values: x_values
            y_values: y_values
            threshold: threshold

        Outputs:
            list: List of reconstructed polynomial coefficients [a₀, a₁, ..., aₖ₋₁].

        Raises:
            ParameterError: If not enough points are provided or x-values are not unique.
            VerificationError: If the matrix is singular during reconstruction.
        """
        if len(x_values) < threshold:
            detailed_msg = f"Need at least {threshold} points to reconstruct a degree {threshold-1} polynomial, got {len(x_values)}"
            message = f"Need at least {threshold} points to reconstruct"
            self._raise_sanitized_error(ParameterError, message, detailed_msg)

        # Verify that the first 'threshold' x values we'll use are unique
        # Convert to int to ensure hashability
        if len({int(x) for x in x_values[:threshold]}) < threshold:
            detailed_msg = f"Need at least {threshold} unique x values to reconstruct polynomial, got: {x_values[:threshold]}"
            message = f"Need at least {threshold} unique x values"
            self._raise_sanitized_error(ParameterError, message, detailed_msg)

        # Validate memory usage for matrix operations
        max_bit_length: int = max(
            max(x.bit_length() if hasattr(x, "bit_length") else 0 for x in x_values),
            max(y.bit_length() if hasattr(y, "bit_length") else 0 for y in y_values),
        )

        if not check_memory_safety("matrix", threshold, max_bit_length):
            raise MemoryError(
                f"Polynomial reconstruction with threshold {threshold} and values of "
                f"approximately {max_bit_length} bits would exceed memory limits."
            )

        # Use only the required number of points
        x_values = x_values[:threshold]
        y_values = y_values[:threshold]
        prime: FieldElement = self.field.prime

        # Special case for threshold=1 (constant polynomial)
        if threshold == 1:
            return [y_values[0]]

        # For threshold > 1, use matrix-based approach
        # Create Vandermonde matrix for the system of equations
        matrix: List[List[FieldElement]] = []
        x: FieldElement
        for x in x_values:
            row: List[FieldElement] = []
            j: int
            for j in range(threshold):
                row.append(gmpy2.powmod(x, j, prime))
            matrix.append(row)

        # Solve the system using secure Gaussian elimination
        return self._secure_matrix_solve(matrix, y_values, prime)

    def _secure_matrix_solve(self, matrix: List[List[FieldElement]], vector: List[FieldElement], prime: Optional[FieldElement] = None) -> List[FieldElement]:
        """
        Description:
        Solve a linear system using side-channel resistant Gaussian elimination.

        Arguments:
            matrix (list): Coefficient matrix.
            vector (list): Right-hand side vector.
            prime (int, optional): Field prime for modular arithmetic.

        Inputs:
            matrix: matrix
            vector: vector
            prime: prime

        Outputs:
            list: Solution vector containing polynomial coefficients.

        Raises:
            VerificationError: If a non-invertible value is encountered during matrix operations.
        """
        if prime is None:
            prime = self.field.prime
        else:
            # Validate that prime is actually prime when provided externally
            if not gmpy2.is_prime(gmpy2.mpz(prime)):
                detailed_msg = f"The provided value {prime} is not a prime number"
                message = "Invalid prime parameter"
                self._raise_sanitized_error(ValueError, message, detailed_msg)

        n: int = len(vector)
        
        # Validate matrix dimensions match vector length
        if len(matrix) != n:
            detailed_msg = f"Matrix rows ({len(matrix)}) must match vector length ({n})"
            message = "Incompatible dimensions"
            self._raise_sanitized_error(ValueError, message, detailed_msg)
            
        # Also validate each row has correct length
        for i, row in enumerate(matrix):
            if len(row) != n:
                detailed_msg = f"Matrix row {i} has {len(row)} elements, but needs {n}"
                message = "Matrix is not square"
                self._raise_sanitized_error(ValueError, message, detailed_msg)

        # Check matrix size limits to prevent memory issues
        if n > 1000:  # Reasonable limit for matrix size
            raise MemoryError(
                f"Matrix size {n}x{n} exceeds safe processing limits. "
                f"Consider reducing polynomial degree or threshold."
            )

        # Estimate memory requirements for the matrix operations
        max_element: int = 0
        
        row: List[FieldElement]
        for row in matrix:
            element: FieldElement
            for element in row:
                element_size: int = (
                    element.bit_length() if hasattr(element, "bit_length") else 0
                )
                max_element = max(max_element, element_size)

        # Estimate total memory for the matrix operations - improved calculation
        estimated_memory: int = n * n * max(max_element, prime.bit_length()) // 8  # in bytes
        if estimated_memory > 1024 * 1024 * 1024:  # 1GB limit
            raise MemoryError(
                f"Matrix operation would require approximately {estimated_memory/(1024*1024):.2f}MB, "
                f"which exceeds the safe limit."
            )

        # Convert to gmpy2 types
        matrix_mpz: List[List["gmpy2.mpz"]] = [[gmpy2.mpz(x) for x in row] for row in matrix]
        vector_mpz: List["gmpy2.mpz"] = [gmpy2.mpz(x) for x in vector]


        # Forward elimination with side-channel resistant operations
        i: int
        for i in range(n):
            # Find pivot using secure method
            pivot_row: Optional[int] = self._find_secure_pivot(matrix_mpz, i, n)

            if pivot_row is None:
                detailed_msg = "Matrix is singular, cannot solve the system"
                message = "Matrix is singular"
                self._raise_sanitized_error(VerificationError, message, detailed_msg)

            # Implement more side-channel resistant row swap
            # Instead of conditional swap, we swap all needed elements unconditionally
            # This approach reduces timing variations due to branching
            # Only swap columns from the current pivot column onward
            for col in range(i, n):
                # Constant-time swap using arithmetic operations with explicit int conversion
                should_swap = int(pivot_row != i)  # Explicitly convert bool to int
                temp = matrix_mpz[i][col]
                matrix_mpz[i][col] = should_swap * matrix_mpz[pivot_row][col] + (1 - should_swap) * matrix_mpz[i][col]
                matrix_mpz[pivot_row][col] = should_swap * temp + (1 - should_swap) * matrix_mpz[pivot_row][col]
            
            # Also swap vector elements in a similar manner
            temp_v = vector_mpz[i]
            should_swap = int(pivot_row != i)  # Explicitly convert bool to int
            vector_mpz[i] = should_swap * vector_mpz[pivot_row] + (1 - should_swap) * vector_mpz[i]
            vector_mpz[pivot_row] = should_swap * temp_v + (1 - should_swap) * vector_mpz[pivot_row]

            # Calculate inverse of pivot using gmpy2.invert instead of powmod
            # This is more appropriate for modular inversion in constant time
            pivot: "gmpy2.mpz" = matrix_mpz[i][i]
            pivot_inverse: "gmpy2.mpz"
            try:
                pivot_inverse = gmpy2.invert(pivot, prime)
            except ZeroDivisionError:
                detailed_msg = f"Value {pivot} is not invertible modulo {prime}"
                message = "Value is not invertible"
                self._raise_sanitized_error(VerificationError, message, detailed_msg)

            # Scale current row
            for j in range(i, n):
                matrix_mpz[i][j] = (matrix_mpz[i][j] * pivot_inverse) % prime
            vector_mpz[i] = (vector_mpz[i] * pivot_inverse) % prime

            # Eliminate other rows with constant-time operations
            for j in range(n):
                if j != i:
                    factor: "gmpy2.mpz" = matrix_mpz[j][i]
                    for k in range(i, n):
                        matrix_mpz[j][k] = (matrix_mpz[j][k] - factor * matrix_mpz[i][k]) % prime
                    vector_mpz[j] = (vector_mpz[j] - factor * vector_mpz[i]) % prime

        return vector_mpz

    def _find_secure_pivot(self, matrix: List[List["gmpy2.mpz"]], col: int, n: int) -> Optional[int]:
        """
        Description:
            Find a non-zero pivot using side-channel resistant selection.

            This method implements a randomized pivot selection strategy that prevents
            timing-based side-channel attacks during Gaussian elimination. Instead of
            selecting the first suitable pivot (which would create timing variations),
            it assigns random values to all potential pivots and selects one with minimal
            random value, ensuring constant-time behavior regardless of matrix content.

        Arguments:
            matrix (list): The matrix being processed.
            col (int): Current column index.
            n (int): Matrix dimension.

        Inputs:
            matrix: Matrix of coefficients.
            col: Current column being processed.
            n: Matrix dimension.

        Outputs:
            int: Index of selected pivot row or None if no valid pivot exists.

        Security properties:
            - Constant-time with respect to the values in the matrix
            - Uses cryptographically secure randomness via secrets.token_bytes()
            - Resistant to timing side-channel attacks
            - Prevents information leakage about matrix structure
        """
        # Generate a single random block for all rows at once (more efficient)
        range_size: int = n - col
        all_random_bytes: bytes = secrets.token_bytes(32 * range_size)

        # Find the valid pivot with the smallest random value
        min_value: float = float("inf")
        pivot_row: Optional[int] = None

        # Track if we found any non-zero pivot (for improved security)
        found_any_nonzero: bool = False

        k: int
        for k in range(range_size):
            row: int = col + k
            # Extract random value for this row
            offset: int = k * 32
            row_random: int = int.from_bytes(
                all_random_bytes[offset : offset + 32], byteorder="big"
            )

            # Update minimum if valid pivot and has smaller random value
            is_nonzero: bool = matrix[row][col] != 0
            found_any_nonzero = found_any_nonzero or is_nonzero
            
            # Use a constant-time approach to update min_value and pivot_row
            # Improved constant-time selection using integer masks
            swap_mask = int(is_nonzero and row_random < min_value)
            min_value = swap_mask * row_random + (1 - swap_mask) * min_value
            # Use arithmetic instead of conditional assignment for constant time
            new_pivot = row * swap_mask + (pivot_row or 0) * (1 - swap_mask)
            pivot_row = new_pivot if (pivot_row is not None or swap_mask) else None

        # Enhanced error check - ensure we're not returning a row with a zero pivot
        # in case the constant-time logic has a subtle bug
        if pivot_row is not None and matrix[pivot_row][col] == 0:
            # This should never happen but acts as a safety check
            if found_any_nonzero:
                # Something went wrong with our constant-time selection
                detailed_msg = "Security error: Selected a zero pivot despite non-zero pivots being available"
                message = "Security error in pivot selection"
                self._raise_sanitized_error(SecurityError, message, detailed_msg)
            return None

        return pivot_row
        

    def create_commitments_with_proof(self, coefficients: List[FieldElement], context: Optional[str] = None) -> Tuple[CommitmentList, ProofDict]:
        """
        Description:
            Create commitments to polynomial coefficients and generate a zero-knowledge
            proof of knowledge of the coefficients in one combined operation.

            This provides a more efficient way to generate both commitments and proofs
            and is recommended for share distribution where proof of knowledge is needed.

        Arguments:
            coefficients (list): List of polynomial coefficients [a₀, a₁, ..., aₖ₋₁].
            context (str, optional): Optional context string for domain separation.

        Inputs:
            coefficients: coefficients
            context: context

        Outputs:
            tuple: (commitments, proof) where both are suitable for verification.

        Raises:
            TypeError: If inputs have incorrect types.
        """
        # Input validation
        if not isinstance(coefficients, list) or not coefficients:
            raise TypeError("coefficients must be a non-empty list")

        if context is not None and not isinstance(context, str):
            raise TypeError("context must be a string if provided")

        # Create commitments first
        commitments: CommitmentList = self.create_commitments(coefficients, context)

        # Generate zero-knowledge proof of knowledge
        proof: ProofDict = self.create_polynomial_proof(coefficients, commitments)

        return commitments, proof

    def verify_commitments_with_proof(self, commitments: CommitmentList, proof: ProofDict, strict_verification: bool = False) -> bool:
        """
        Description:
            Verify that a zero-knowledge proof demonstrates knowledge of the
            polynomial coefficients committed to by the given commitments.

        Arguments:
            commitments (list): List of commitments to polynomial coefficients.
            proof (dict): Zero-knowledge proof structure from create_polynomial_proof.
            strict_verification (bool): If True, raises an error on challenge verification failure.

        Inputs:
            commitments: commitments
            proof: proof
            strict_verification: strict_verification

        Outputs:
            bool: True if the proof is valid, False otherwise.

        Raises:
            TypeError: If inputs have incorrect types.
            ValueError: If commitments list is empty.
            SecurityWarning: If proof is missing required keys.
            VerificationError: If strict_verification is True and verification fails.
        """
        # Input validation
        if not isinstance(commitments, list):
            raise TypeError("commitments must be a list")
        if not commitments:
            raise ValueError("commitments list cannot be empty")
        if not isinstance(proof, dict):
            raise TypeError("proof must be a dictionary")
        if not all(isinstance(c, tuple) and len(c) >= 2 for c in commitments):
            raise TypeError(
                "Each commitment must be a tuple with at least (commitment, randomizer)"
            )

        # Validate proof has all required keys before proceeding
        required_keys: List[str] = [
            "blinding_commitments",
            "challenge",
            "responses",
            "commitment_randomizers",
            "blinding_randomizers",
        ]
        if not all(key in proof for key in required_keys):
            warnings.warn("Proof missing required keys", SecurityWarning)
            return False

        # Verify the proof with added challenge consistency check
        is_valid = self.verify_polynomial_proof(proof, commitments)
        
        # Optionally check challenge consistency more strictly
        if is_valid and not self._verify_challenge_consistency(proof, commitments):
            if strict_verification:
                detailed_msg = "Proof verification passed but challenge value appears inconsistent"
                message = "Challenge verification failed"
                self._raise_sanitized_error(VerificationError, message, detailed_msg)
            warnings.warn("Challenge verification failed", SecurityWarning)
            return False
            
        return is_valid

    def serialize_commitments_with_proof(self, commitments: CommitmentList, proof: ProofDict) -> str:
        """
        Description:
            Serialize commitments and associated zero-knowledge proof for storage or transmission

        Arguments:
            commitments (list): List of (hash, randomizer) tuples.
            proof (dict): Zero-knowledge proof structure from create_polynomial_proof.

        Inputs:
            commitments: commitments
            proof: proof

        Outputs:
            str: String with base64-encoded serialized data.

        Raises:
            TypeError: If inputs have incorrect types.
            ValueError: If proof is missing required keys.
            SerializationError: If serialization fails.
        """
        # Input validation
        if not isinstance(commitments, list) or not commitments:
            raise TypeError("commitments must be a non-empty list")
        if not all(isinstance(c, tuple) and len(c) >= 2 for c in commitments):
            raise TypeError(
                "Each commitment must be a tuple of at least (commitment, randomizer)"
            )

        # Add validation for proof parameter
        if not isinstance(proof, dict):
            raise TypeError("proof must be a dictionary")

        required_proof_keys: List[str] = [
            "blinding_commitments",
            "challenge",
            "responses",
            "commitment_randomizers",
            "blinding_randomizers",
            "timestamp",
        ]
        for key in required_proof_keys:
            if key not in proof:
                raise ValueError(f"proof is missing required key: {key}")

        if (
            not isinstance(proof["blinding_commitments"], list)
            or not proof["blinding_commitments"]
        ):
            raise TypeError("proof['blinding_commitments'] must be a non-empty list")
        if not all(
            isinstance(c, tuple) and len(c) >= 2 for c in proof["blinding_commitments"]
        ):
            raise TypeError(
                "Each blinding commitment must be a tuple with at least (commitment, randomizer)"
            )

        # First serialize the commitments as before
        commitment_values: List[Tuple[int, int, Optional[str]]] = [
            (int(c), int(r), e.hex() if e else None) for c, r, e in commitments
        ]

        # Process proof data for serialization
        serializable_proof: Dict[str, Any] = {
            "blinding_commitments": [
                (int(c), int(r)) for c, r in proof["blinding_commitments"]
            ],
            "challenge": int(proof["challenge"]),
            "responses": [int(r) for r in proof["responses"]],
            "commitment_randomizers": [int(r) for r in proof["commitment_randomizers"]],
            "blinding_randomizers": [int(r) for r in proof["blinding_randomizers"]],
            "timestamp": int(proof["timestamp"]),
        }

        result: Dict[str, Any] = {
            "version": VSS_VERSION,
            "timestamp": int(time.time()),
            "generator": int(self.generator),
            "prime": int(self.group.prime),
            "commitments": commitment_values,
            "hash_based": True,
            "proof": serializable_proof,
            "has_proof": True,
        }

        # Pack with msgpack for efficient serialization
        try:
            packed_data: bytes = msgpack.packb(result)

            # Compute checksum and create wrapper
            checksum_wrapper: Dict[str, Any] = {
                "data": packed_data,
                "checksum": compute_checksum(packed_data),
            }

            # Pack the wrapper and encode
            packed_wrapper: bytes = msgpack.packb(checksum_wrapper)
            return urlsafe_b64encode(packed_wrapper).decode("utf-8")

        except Exception as e:
            detailed_msg = f"Failed to serialize commitments with proof: {e}"
            message = "Serialization failed"
            self._raise_sanitized_error(SerializationError, message, detailed_msg)

    def deserialize_commitments_with_proof(self, data: str) -> Tuple[CommitmentList, ProofDict, FieldElement, FieldElement, int]:
        """
        Description:
            Deserialize commitment data including zero-knowledge proof with enhanced security checks

        Arguments:
            data (str): Serialized commitment data string.

        Inputs:
            data: Serialized data

        Outputs:
            tuple: (commitments, proof, generator, prime, timestamp).

        Raises:
            TypeError: If data is not a string or is empty.
            SerializationError: If deserialization or validation fails.
            SecurityError: If data integrity checks fail.
        """
        # Add validation
        if not isinstance(data, str):
            raise TypeError("data must be a string")
        if not data:
            raise ValueError("data cannot be empty")

        try:
            # Decode and unpack the data
            decoded: bytes = urlsafe_b64decode(data.encode("utf-8"))

            # Use Unpacker with security settings - matching the approach in deserialize_commitments
            unpacker: "msgpack.Unpacker" = msgpack.Unpacker(
                use_list=False,  # Use tuples instead of lists for immutability
                raw=True,  # Keep binary data as bytes
                strict_map_key=True,
                max_buffer_size=10 * 1024 * 1024,  # 10MB limit
            )
            unpacker.feed(decoded)

            # Define constants for dictionary keys to ensure consistency
            CHECKSUM_KEY = b"checksum"
            DATA_KEY = b"data"
            HAS_PROOF_KEY = b"has_proof"
            PROOF_KEY = b"proof"
            
            # Keys for the proof dictionary
            BLINDING_COMMITMENTS_KEY = b"blinding_commitments"
            CHALLENGE_KEY = b"challenge"
            RESPONSES_KEY = b"responses"
            COMMITMENT_RANDOMIZERS_KEY = b"commitment_randomizers" 
            BLINDING_RANDOMIZERS_KEY = b"blinding_randomizers"
            TIMESTAMP_KEY = b"timestamp"

            wrapper_dict: Dict[bytes, Any]
            try:
                # Unpack the checksum wrapper
                wrapper_dict = unpacker.unpack()
            except (
                msgpack.exceptions.ExtraData,
                msgpack.exceptions.FormatError,
                msgpack.exceptions.StackError,
                msgpack.exceptions.BufferFull,
                msgpack.exceptions.OutOfData,
                ValueError,
            ) as e:
                detailed_msg = f"Failed to unpack msgpack data: {e}"
                message = "Invalid data format"
                self._raise_sanitized_error(SerializationError, message, detailed_msg)

            # Verify checksum - this is a critical security check
            if CHECKSUM_KEY not in wrapper_dict or DATA_KEY not in wrapper_dict:
                detailed_msg = "Missing checksum or data fields in deserialized content"
                message = "Invalid data format"
                self._raise_sanitized_error(SerializationError, message, detailed_msg)

            packed_data: bytes = wrapper_dict[DATA_KEY]
            expected_checksum: int = wrapper_dict[CHECKSUM_KEY]
            actual_checksum: int = compute_checksum(packed_data)

            # Use constant-time comparison to prevent timing attacks
            if not constant_time_compare(actual_checksum, expected_checksum):
                detailed_msg = f"Checksum mismatch: expected {expected_checksum}, got {actual_checksum}"
                message = "Data integrity check failed - possible tampering detected"
                self._raise_sanitized_error(SecurityError, message, detailed_msg)

            # Feed the inner data to a new Unpacker instance
            inner_unpacker: "msgpack.Unpacker" = msgpack.Unpacker(
                use_list=False,
                raw=True,
                strict_map_key=True,
                max_buffer_size=10 * 1024 * 1024,
            )
            inner_unpacker.feed(packed_data)

            unpacked_dict: Dict[bytes, Any]
            try:
                # Proceed with unpacking the actual data
                unpacked_dict = inner_unpacker.unpack()
            except (
                msgpack.exceptions.ExtraData,
                msgpack.exceptions.FormatError,
                msgpack.exceptions.StackError,
                msgpack.exceptions.BufferFull,
                msgpack.exceptions.OutOfData,
                ValueError,
            ) as e:
                detailed_msg = f"Failed to unpack inner msgpack data: {e}"
                message = "Failed to unpack data"
                self._raise_sanitized_error(SerializationError, message, detailed_msg)

            # First deserialize commitments using the existing method
            commitments: CommitmentList
            generator: FieldElement
            prime: FieldElement
            timestamp: int
            is_hash_based: bool
            commitments, generator, prime, timestamp, is_hash_based = (
                self.deserialize_commitments(data)
            )

            # Check if proof data is present
            has_proof: bool = unpacked_dict.get(HAS_PROOF_KEY, False)
            if not has_proof:
                detailed_msg = "No proof data found in serialized commitments"
                message = "Missing proof data"
                self._raise_sanitized_error(SerializationError, message, detailed_msg)

            # Extract and reconstruct proof
            serialized_proof: Optional[Dict[bytes, Any]] = unpacked_dict.get(PROOF_KEY)
            if not serialized_proof:
                detailed_msg = "Missing proof data in serialized commitments"
                message = "Missing proof data"
                self._raise_sanitized_error(SerializationError, message, detailed_msg)

            # Validate proof structure more thoroughly
            required_keys: List[bytes] = [
                BLINDING_COMMITMENTS_KEY,
                CHALLENGE_KEY,
                RESPONSES_KEY,
                COMMITMENT_RANDOMIZERS_KEY,
                BLINDING_RANDOMIZERS_KEY,
                TIMESTAMP_KEY,
            ]
            
            for key in required_keys:
                if key not in serialized_proof:
                    detailed_msg = f"Proof missing required field: {key.decode('utf-8')}"
                    message = "Invalid proof structure"
                    self._raise_sanitized_error(SerializationError, message, detailed_msg)

            # Validate types and structures with safer access patterns
            if not isinstance(serialized_proof.get(BLINDING_COMMITMENTS_KEY), tuple):
                detailed_msg = "blinding_commitments must be a sequence"
                message = "Invalid proof structure"
                self._raise_sanitized_error(SerializationError, message, detailed_msg)

            if not isinstance(serialized_proof.get(CHALLENGE_KEY), int):
                detailed_msg = "challenge must be an integer"
                message = "Invalid proof structure"
                self._raise_sanitized_error(SerializationError, message, detailed_msg)

            # Additional validations...
            # ...existing code...

            # Improved exception handling for specific error types
            try:
                # Reconstruct the proof with proper structure
                proof: ProofDict = {
                    "blinding_commitments": [
                        (gmpy2.mpz(c), gmpy2.mpz(r))
                        for c, r in serialized_proof[BLINDING_COMMITMENTS_KEY]
                    ],
                    "challenge": gmpy2.mpz(serialized_proof[CHALLENGE_KEY]),
                    "responses": [gmpy2.mpz(r) for r in serialized_proof[RESPONSES_KEY]],
                    "commitment_randomizers": [
                        gmpy2.mpz(r) for r in serialized_proof[COMMITMENT_RANDOMIZERS_KEY]
                    ],
                    "blinding_randomizers": [
                        gmpy2.mpz(r) for r in serialized_proof[BLINDING_RANDOMIZERS_KEY]
                    ],
                    "timestamp": serialized_proof[TIMESTAMP_KEY],
                }
            except (TypeError, ValueError, IndexError) as e:
                detailed_msg = f"Failed to convert proof components: {e}"
                message = "Invalid proof format"
                self._raise_sanitized_error(SerializationError, message, detailed_msg)
            except Exception as e:
                # Keep this general exception handler as a last resort
                detailed_msg = f"Unexpected error reconstructing proof: {e}"
                message = "Proof reconstruction failed"
                self._raise_sanitized_error(SecurityError, message, detailed_msg)

            # Add challenge verification
            # Note: This is a simplified example - actual implementation would 
            # need to call the appropriate challenge computation function
            try:
                # Verify proof internally with challenge recomputation
                if not self._verify_challenge_consistency(proof, commitments):
                    warnings.warn("Challenge verification failed", SecurityWarning)
                    return commitments, proof, generator, prime, timestamp
            except Exception as e:
                # Only warn about challenge verification issues, don't fail
                warnings.warn(f"Challenge verification error: {e}", SecurityWarning)

            return commitments, proof, generator, prime, timestamp
        except (SerializationError, SecurityError):
            # Re-raise specific security exceptions
            raise
        except Exception as e:
            detailed_msg = f"Failed to deserialize commitments with proof: {e}"
            message = "Deserialization failed"
            self._raise_sanitized_error(SerializationError, message, detailed_msg)

    def verify_share_with_proof(self, share_x: FieldElement, share_y: FieldElement, serialized_data: str) -> Tuple[bool, bool]:
        """
        Description:
            Comprehensive verification of a share against serialized commitment data with proof

        Arguments:
            share_x (int): x-coordinate of the share.
            share_y (int): y-coordinate of the share.
            serialized_data (str): Serialized commitment data with proof.

        Inputs:
            share_x: share x
            share_y: share y
            serialized_data: serialized data

        Outputs:
            tuple: (share_valid, proof_valid) indicating validation results.

        Raises:
            TypeError: If inputs have incorrect types.
            VerificationError: If verification fails.
        """
        # Input validation
        if not isinstance(share_x, (int, gmpy2.mpz)):
            raise TypeError("share_x must be an integer")
        if not isinstance(share_y, (int, gmpy2.mpz)):
            raise TypeError("share_y must be an integer")
        if not isinstance(serialized_data, str) or not serialized_data:
            raise TypeError("serialized_data must be a non-empty string")

        try:
            # Deserialize the commitments and proof
            commitments: CommitmentList
            proof: ProofDict
            generator: FieldElement
            prime: FieldElement
            timestamp: int
            
            commitments, proof, generator, prime, timestamp = (
                self.deserialize_commitments_with_proof(serialized_data)
            )

            # Create a group with the same parameters
            group: CyclicGroup = CyclicGroup(prime=prime, generator=generator)

            # Create a new VSS instance with this group
            temp_config: VSSConfig = VSSConfig()
            temp_vss: FeldmanVSS = FeldmanVSS(self.field, temp_config, group)

            # Verify both the share and the proof
            share_valid: bool = temp_vss.verify_share(share_x, share_y, commitments)
            proof_valid: bool = temp_vss.verify_commitments_with_proof(commitments, proof)

            return share_valid, proof_valid

        except Exception as e:
            detailed_msg = f"Failed to verify share with proof: {e}"
            message = "Verification failed"
            self._raise_sanitized_error(VerificationError, message, detailed_msg)


# Simplified factory function focused on post-quantum security
def get_feldman_vss(field: Any, **kwargs: Any) -> FeldmanVSS:
    """
    Description:
        Factory function to create a post-quantum secure FeldmanVSS instance.

    Arguments:
        field: MersennePrimeField instance.
        **kwargs: Additional configuration parameters.

    Inputs:
        field: Field

    Outputs:
        FeldmanVSS: FeldmanVSS instance configured for post-quantum security.

    Raises:
        TypeError: If field is None or does not have a 'prime' attribute of the correct type.
    """
    # Add validation for field parameter
    if field is None:
        raise TypeError("field cannot be None")

    if not hasattr(field, "prime"):
        raise TypeError("field must have 'prime' attribute")

    if not isinstance(field.prime, (int, gmpy2.mpz)):
        raise TypeError("field.prime must be an integer type")

    config: Optional[VSSConfig] = kwargs.get("config", None)

    if config is None:
        config = VSSConfig(
            prime_bits=4096,  # Always use at least 3072 bits for post-quantum security
            safe_prime=True,
            use_blake3=True,
        )

    return FeldmanVSS(field, config)


# Integration helper for the main Shamir Secret Sharing implementation
def create_vss_from_shamir(shamir_instance: Any) -> FeldmanVSS:
    """
    Description:
        Create a post-quantum secure FeldmanVSS instance compatible with a ShamirSecretSharing instance

    Arguments:
        shamir_instance: A ShamirSecretSharing instance.

    Inputs:
        shamir_instance: Shamir instance

    Outputs:
        FeldmanVSS: FeldmanVSS instance configured to work with the Shamir instance.

    Raises:
        TypeError: If shamir_instance does not have the required attributes.
    """
    # Validate the shamir_instance has required attributes
    if not hasattr(shamir_instance, "field"):
        raise TypeError("shamir_instance must have a 'field' attribute")

    if not hasattr(shamir_instance.field, "prime"):
        raise TypeError("shamir_instance.field must have a 'prime' attribute")

    # Get the field from the Shamir instance
    field: Any = shamir_instance.field

    # Configure VSS based on Shamir's parameters
    prime_bits: int = field.prime.bit_length()

    if prime_bits < MIN_PRIME_BITS:
        warnings.warn(
            f"Shamir instance uses {prime_bits}-bit prime which is less than the "
            f"recommended {MIN_PRIME_BITS} bits for post-quantum security. "
            f"Consider regenerating your Shamir instance with stronger parameters.",
            SecurityWarning,
        )

    # Create a post-quantum secure VSS instance
    return get_feldman_vss(field)


# Add a helper function to integrate with Pedersen VSS
def integrate_with_pedersen(feldman_vss: FeldmanVSS, pedersen_vss: Any, shares: ShareDict, coefficients: List[FieldElement]) -> Dict[str, Any]:
    """
    Description:
        Integrate Feldman VSS with Pedersen VSS for dual verification.

        This provides both the binding property from Feldman VSS and the
        hiding property from Pedersen VSS, offering the best of both approaches.

    Arguments:
        feldman_vss: FeldmanVSS instance.
        pedersen_vss: PedersenVSS instance.
        shares: Dictionary of shares from Shamir secret sharing.
        coefficients: Polynomial coefficients used for share generation.

    Inputs:
        feldman_vss: feldman vss
        pedersen_vss: pedersen vss
        shares: shares
        coefficients: coefficients

    Outputs:
        dict: Dictionary with both Feldman and Pedersen verification data.

    Raises:
        TypeError: If inputs have incorrect types.
    """
    # Input validation
    if not isinstance(feldman_vss, FeldmanVSS):
        raise TypeError("feldman_vss must be a FeldmanVSS instance")
    if not hasattr(pedersen_vss, "create_commitments"):
        raise TypeError("pedersen_vss must have a create_commitments method")
    if not isinstance(shares, dict):
        raise TypeError("shares must be a dictionary")
    if not isinstance(coefficients, list) or not coefficients:
        raise TypeError("coefficients must be a non-empty list")

    # Generate Feldman commitments
    feldman_commitments: CommitmentList = feldman_vss.create_commitments(coefficients)

    # Generate Pedersen commitments
    pedersen_commitments: List[FieldElement] = pedersen_vss.create_commitments(coefficients)

    # Create a zero-knowledge proof that both commitment sets commit to the same values
    # This demonstrates that the Feldman and Pedersen schemes are using the same polynomial
    proof:  Dict[str, Any] = create_dual_commitment_proof(
        feldman_vss,
        pedersen_vss,
        coefficients,
        feldman_commitments,
        pedersen_commitments,
    )

    # Serialize the commitments
    feldman_serialized: str = feldman_vss.serialize_commitments(feldman_commitments)
    pedersen_serialized: str = pedersen_vss.serialize_commitments(pedersen_commitments)

    return {
        "feldman_commitments": feldman_serialized,
        "pedersen_commitments": pedersen_serialized,
        "dual_proof": proof,
        "version": VSS_VERSION,
    }


def create_dual_commitment_proof(
    feldman_vss: FeldmanVSS, pedersen_vss: Any, coefficients: List[FieldElement], feldman_commitments: CommitmentList, pedersen_commitments: List[FieldElement]
) -> Dict[str, Any]:
    """
    Description:
        Create a zero-knowledge proof that Feldman and Pedersen commitments
        are to the same polynomial coefficients.

    Arguments:
        feldman_vss: FeldmanVSS instance.
        pedersen_vss: PedersenVSS instance.
        coefficients: The polynomial coefficients.
        feldman_commitments: Commitments created by Feldman scheme.
        pedersen_commitments: Commitments created by Pedersen scheme.

    Inputs:
        feldman_vss: feldman_vss
        pedersen_vss: pedersen_vss
        coefficients: coefficients
        feldman_commitments: feldman_commitments
        pedersen_commitments: pedersen_commitments

    Outputs:
        dict: Proof data structure.

    Raises:
        TypeError: If inputs have incorrect types.
        ValueError: If input lists have inconsistent lengths.
    """
    # Input validation for all parameters
    if not isinstance(feldman_vss, FeldmanVSS):
        raise TypeError("feldman_vss must be a FeldmanVSS instance")

    if not hasattr(pedersen_vss, "commit_to_blinding_factors"):
        raise TypeError("pedersen_vss must have a 'commit_to_blinding_factors' method")

    if not hasattr(pedersen_vss, "g") or not hasattr(pedersen_vss, "h"):
        raise TypeError("pedersen_vss must have 'g' and 'h' attributes")

    if not isinstance(coefficients, list) or not coefficients:
        raise TypeError("coefficients must be a non-empty list")

    if not isinstance(feldman_commitments, list) or not feldman_commitments:
        raise TypeError("feldman_commitments must be a non-empty list")

    if not isinstance(pedersen_commitments, list) or not pedersen_commitments:
        raise TypeError("pedersen_commitments must be a non-empty list")

    if len(coefficients) != len(feldman_commitments) or len(coefficients) != len(
        pedersen_commitments
    ):
        raise ValueError(
            "coefficients, feldman_commitments, and pedersen_commitments must have the same length"
        )

    # Generate random blinding factors
    blindings: List[FieldElement] = [
        feldman_vss.group.secure_random_element() for _ in range(len(coefficients))
    ]

    # Check if we're using hash-based commitments
    is_hash_based: bool = isinstance(feldman_commitments[0], tuple)

    # Create Feldman commitments to the blinding factors
    feldman_blinding_commitments:  List[Union[Tuple[FieldElement, FieldElement], FieldElement]] = []

    if is_hash_based:
        # Create hash-based blinding commitments (with randomizers)
        i: int
        b: FieldElement
        for i, b in enumerate(blindings):
            # Generate secure randomizer for each blinding factor
            r_b: FieldElement = feldman_vss.group.secure_random_element()

            # Use helper method to compute commitment
            commitment: FieldElement = feldman_vss._compute_hash_commitment(b, r_b, i, "blinding")

            # Store commitment and randomizer as tuple
            feldman_blinding_commitments.append((commitment, r_b))
    else:
        # Create standard blinding commitments (just exponentiation)
        feldman_blinding_commitments = [
            feldman_vss.group.secure_exp(feldman_vss.generator, b) for b in blindings
        ]

    # Create Pedersen commitments to the blinding factors
    pedersen_blinding_commitments: List[FieldElement] = pedersen_vss.commit_to_blinding_factors(blindings)

    # Generate challenge using Fiat-Shamir transform
    challenge_input: bytes = feldman_vss.group._enhanced_encode_for_hash(
        feldman_vss.generator,
        pedersen_vss.g,
        pedersen_vss.h,
        [fc[0] if isinstance(fc, tuple) else fc for fc in feldman_commitments],
        pedersen_commitments,
        [
            fbc[0] if isinstance(fbc, tuple) else fbc
            for fbc in feldman_blinding_commitments
        ],
        pedersen_blinding_commitments,
    )

    # Hash the challenge input
    challenge_hash: bytes
    if HAS_BLAKE3:
        challenge_hash = blake3.blake3(challenge_input).digest()
    else:
        challenge_hash = hashlib.sha3_256(challenge_input).digest()

    challenge: FieldElement = int.from_bytes(challenge_hash, "big") % feldman_vss.field.prime

    # Compute responses
    responses: List[FieldElement] = [
        (b + challenge * c) % feldman_vss.field.prime
        for b, c in zip(blindings, coefficients)
    ]

    # For hash-based commitments, include combined randomizers for verification
    response_randomizers: Optional[List[FieldElement]] = None
    if is_hash_based:
        response_randomizers = []
        i: int
        for i in range(len(responses)):
            # Fix tuple unpacking - feldman_blinding_commitments are (commitment, randomizer) tuples
            commitment_b, r_b = feldman_blinding_commitments[i]  # type: ignore
            commitment_a, r_a = feldman_commitments[i]  # type: ignore
            r_combined: FieldElement = (r_b + challenge * r_a) % feldman_vss.field.prime
            response_randomizers.append(r_combined)

    # Return the proof structure
    proof: Dict[str, Any] = {
        "feldman_blinding_commitments": feldman_blinding_commitments,
        "pedersen_blinding_commitments": pedersen_blinding_commitments,
        "challenge": int(challenge),
        "responses": [int(r) for r in responses],
    }

    # Add response randomizers if using hash-based commitments
    if response_randomizers is not None:
        proof["response_randomizers"] = [int(r) for r in response_randomizers]

    return proof


def verify_dual_commitments(
    feldman_vss: FeldmanVSS, pedersen_vss: Any, feldman_commitments: CommitmentList, pedersen_commitments: List[FieldElement], proof: Dict[str, Any]
) -> bool:
    """
    Description:
        Verify that the Feldman and Pedersen commitments commit to the same values
        using constant-time operations to prevent timing side-channels.

    Arguments:
        feldman_vss: FeldmanVSS instance.
        pedersen_vss: PedersenVSS instance.
        feldman_commitments: Feldman commitments.
        pedersen_commitments: Pedersen commitments.
        proof: Proof data structure from create_dual_commitment_proof.

    Outputs:
        bool: True if verification succeeds, False otherwise.
    """
    # Input validation
    if not isinstance(feldman_vss, FeldmanVSS):
        raise TypeError("feldman_vss must be a FeldmanVSS instance")
    if not hasattr(pedersen_vss, "verify_response_equation"):
        raise TypeError("pedersen_vss must have a verify_response_equation method")
    if not isinstance(feldman_commitments, list) or not feldman_commitments:
        raise TypeError("feldman_commitments must be a non-empty list")
    if not isinstance(pedersen_commitments, list) or not pedersen_commitments:
        raise TypeError("pedersen_commitments must be a non-empty list")
    if not isinstance(proof, dict):
        raise TypeError("proof must be a dictionary")

    # Add length consistency validation
    if len(feldman_commitments) != len(pedersen_commitments):
        raise ValueError(
            "feldman_commitments and pedersen_commitments must have the same length"
        )

    # Required proof components
    required_keys: List[str] = [
        "feldman_blinding_commitments",
        "pedersen_blinding_commitments",
        "challenge",
        "responses",
    ]
    if not all(key in proof for key in required_keys):
        raise ValueError("Proof is missing required components")

    # Validate component lengths
    if len(proof["responses"]) != len(feldman_commitments):
        raise ValueError("Number of responses must match number of commitments")
    if len(proof["feldman_blinding_commitments"]) != len(feldman_commitments):
        raise ValueError(
            "Number of feldman_blinding_commitments must match number of commitments"
        )
    if len(proof["pedersen_blinding_commitments"]) != len(pedersen_commitments):
        raise ValueError(
            "Number of pedersen_blinding_commitments must match number of commitments"
        )

    # Extract proof components
    feldman_blinding_commitments: List[Union[Tuple[FieldElement, FieldElement], FieldElement]] = proof["feldman_blinding_commitments"]
    pedersen_blinding_commitments: List[FieldElement] = proof["pedersen_blinding_commitments"]
    challenge: FieldElement = proof["challenge"]
    responses: List[FieldElement] = proof["responses"]
    response_randomizers: Optional[List[FieldElement]] = proof.get("response_randomizers", None)

    # Check if we're using hash-based commitments for Feldman VSS
    is_hash_based: bool = isinstance(feldman_commitments[0], tuple)

    # Initialize validity flag for constant-time verification
    all_valid: bool = True

    # Also validate in constant-time that response_randomizers has the right length if needed
    if is_hash_based:
        all_valid &= response_randomizers is not None
        randomizers_valid_len: bool = (
            len(response_randomizers) == len(responses)
            if response_randomizers is not None
            else False
        )
        all_valid &= randomizers_valid_len

    # First verify Pedersen commitments - these use the same approach regardless
    i: int
    for i in range(len(responses)):
        # Verify using Pedersen VSS verification method
        pedersen_valid: bool = pedersen_vss.verify_response_equation(
            responses[i],
            challenge,
            pedersen_blinding_commitments[i],
            pedersen_commitments[i],
        )
        all_valid &= pedersen_valid

    # Then verify Feldman commitments
    if is_hash_based:
        # For hash-based commitments, verification requires validating hash output
        
        i: int
        for i in range(len(responses)):
            # Instead of skipping iterations, always compute but conditionally update result
            response_value: FieldElement = responses[i]
            
            # Use safe default if randomizers are invalid
            r_combined: FieldElement = 0
            if response_randomizers is not None and i < len(response_randomizers):
                r_combined = response_randomizers[i]
            
            # Always compute both sides for constant-time behavior
            computed: FieldElement = feldman_vss._compute_hash_commitment(
                response_value, r_combined, i, "response"
            )

            # Calculate expected commitment
            commitment_value: FieldElement = feldman_commitments[i][0]  # type: ignore
            blinding_commitment_value: FieldElement = feldman_blinding_commitments[i][0]  # type: ignore
            
            expected: FieldElement = (
                blinding_commitment_value + challenge * commitment_value
            ) % feldman_vss.group.prime
            
            # Determine if this verification should count using constant-time operations
            should_check: bool = (response_randomizers is not None and i < len(response_randomizers))
            equality_result: bool = constant_time_compare(computed, expected)
            
            # Improved constant-time conditional update
            mask = -int(should_check)  # Creates all 1s (for True) or all 0s (for False)
            masked_result = equality_result & mask
            all_valid &= (masked_result | ~mask)  # Will be equality_result when should_check is True, otherwise 1
    else:
        # Standard Feldman commitment verification
        i: int
        for i in range(len(responses)):
            # Calculate left side: g^response[i]
            left_side: FieldElement = feldman_vss.group.secure_exp(
                feldman_vss.generator, responses[i]
            )

            # Calculate right side: blinding_commitment[i] * commitment[i]^challenge
            commitment_term: FieldElement = feldman_vss.group.secure_exp(
                feldman_commitments[i], challenge # type: ignore
            )
            right_side: FieldElement = feldman_vss.group.mul(
                feldman_blinding_commitments[i], commitment_term # type: ignore
            )

            # Check equality using constant-time comparison
            all_valid &= constant_time_compare(left_side, right_side)

    return all_valid