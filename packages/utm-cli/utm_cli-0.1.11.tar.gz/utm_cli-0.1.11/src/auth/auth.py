'''
Author: Tong hetongapp@gmail.com
Date: 2025-02-14 14:29:36
LastEditors: Tong hetongapp@gmail.com
LastEditTime: 2025-02-14 15:16:11
FilePath: /server/src/auth/auth.py
Description: auth token
'''

import datetime
from typing import Dict, List, Optional
import uuid

import jwcrypto.common
import jwcrypto.jwk
import jwcrypto.jws
import jwcrypto.jwt

EPOCH = datetime.datetime.fromtimestamp(0, tz = datetime.timezone.utc)
TOKEN_REFRESH_MARGIN = datetime.timedelta(seconds=15)
CLIENT_TIMEOUT = 60  # seconds

class Auth():
    """Auth adapter that generates tokens without an auth server.
    While no server is used, the access tokens generated are fully valid.
    """
    
    dummy_private_key = jwcrypto.jwk.JWK.from_pem(
        "-----BEGIN RSA PRIVATE KEY-----\n"
        "MIICWwIBAAKBgHkNtpy3GB0YTCl2VCCd22i0rJwIGBSazD4QRKvH6rch0IP4igb+\n"
        "02r7t0X//tuj0VbwtJz3cEICP8OGSqrdTSCGj5Y03Oa2gPkx/0c0V8D0eSXS/CUC\n"
        "0qrYHnAGLqko7eW87HW0rh7nnl2bB4Lu+R8fOmQt5frCJ5eTkzwK5YczAgMBAAEC\n"
        "gYAtSgMjGKEt6XQ9IucQmN6Iiuf1LFYOB2gYZC+88PuQblc7uJWzTk08vlXwG3l3\n"
        "JQ/h7gY0n6JhH8RJW4m96TO8TrlHLx5aVcW8E//CtgayMn3vBgXida3wvIlAXT8G\n"
        "WezsNsWorXLVmz5yov0glu+TIk31iWB5DMs4xXhXdH/t8QJBALQzvF+y5bZEhZin\n"
        "qTXkiKqMsKsJbXjP1Sp/3t52VnYVfbxN3CCb7yDU9kg5QwNa3ungE3cXXNMUr067\n"
        "9zIraekCQQCr+NSeWAXIEutWewPIykYMQilVtiJH4oFfoEpxvecVv7ulw6kM+Jsb\n"
        "o6Pi7x86tMVkwOCzZzy/Uyo/gSHnEZq7AkEAm0hBuU2VuTzOyr8fhvtJ8X2O97QG\n"
        "C6c8j4Tk7lqXIuZeFRga6la091vMZmxBnPB/SpX28BbHvHUEpBpBZ5AVkQJAX7Lq\n"
        "7urg3MPafpeaNYSKkovG4NGoJgSgJgzXIJCjJfE6hTZqvrMh7bGUo9aZtFugdT74\n"
        "TB2pKncnTYuYyDN9vQJACDVr+wvYYA2VdnA9k+/1IyGc1HHd2npQqY9EduCeOGO8\n"
        "rXQedG6rirVOF6ypkefIayc3usipVvfadpqcS5ERhw==\n"
        "-----END RSA PRIVATE KEY-----".encode("UTF-8")
    )

    EXPIRATION = 3600  # seconds

    def __init__(self, sub: str = "uss_noauth"):
        super().__init__()
        self.sub = sub

    # Overrides method in AuthAdapter
    def issue_token(self, intended_audience: str, scopes: List[str]) -> str:
        timestamp = int((datetime.datetime.now(datetime.timezone.utc) - EPOCH).total_seconds())
        jwt = jwcrypto.jwt.JWT(
            header={"typ": "JWT", "alg": "RS256"},
            claims={
                "sub": self.sub,
                "client_id": self.sub,
                "scope": " ".join(scopes),
                "aud": intended_audience,
                "nbf": timestamp - 1,
                "exp": timestamp + Auth.EXPIRATION,
                "iss": "NoAuth",
                "jti": str(uuid.uuid4()),
            },
            algs=["RS256"],
        )
        jwt.make_signed_token(Auth.dummy_private_key)
        return jwt.serialize()

