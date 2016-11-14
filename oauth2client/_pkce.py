# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Utility functions for implementing Proof Key for Code Exchange (PKCE) by OAuth
Public Clients

See RFC7636.
"""

import base64
import hashlib
import os


def code_verifier(n_bytes=64):
    """
    Generates a 'code_verifier' as described in section 4.1 of RFC 7636.

    This is a 'high-entropy cryptographic random string' that will be
    impractical for an attacker to guess.

    Args:
        n_bytes: integer between 31 and 96, inclusive. default: 64
            number of bytes of entropy to include in verifier.

    Returns:
        Bytestring, representing urlsafe base64-encoded random data.
    """
    verifier = base64.urlsafe_b64encode(os.urandom(n_bytes))
    # https://tools.ietf.org/html/rfc7636#section-4.1
    # minimum length of 43 characters and a maximum length of 128 characters.
    if len(verifier) < 43:
        raise ValueError("Verifier too short. n_bytes must be > 30.")
    elif len(verifier) > 128:
        raise ValueError("Verifier too long. n_bytes must be < 97.")
    else:
        return verifier


def code_challenge(verifier):
    """
    Creates a 'code_challenge' as described in section 4.2 of RFC 7636
    by taking the sha256 hash of the verifier and then urlsafe
    base64-encoding it.

    Args:
        verifier: bytestring, representing a code_verifier as generated by
            code_verifier().

    Returns:
        Bytestring, representing a urlsafe base64-encoded sha256 hash digest.
    """
    return base64.urlsafe_b64encode(hashlib.sha256(verifier).digest()).rstrip(b'=')
