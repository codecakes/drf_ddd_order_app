from __future__ import annotations

import datetime
from typing import List, Optional, Tuple
import pydantic
from pydantic import BaseModel, Field
from authlib import jose

JWT_TOKEN = bytes
TokenTuple = Tuple[JWT_TOKEN, dict]


class JWKHeader(BaseModel, extra=pydantic.Extra.forbid, allow_mutation=False):
    """
    See for more info:
    https://www.scottbrady91.com/python/authlib-python-jwt
    """

    alg: str = Field(default="ES256")
    crv: str = Field(default="P-256")
    key_ops: Optional[List[str]] = Field(default=["verify"])
    kty: str
    x: str
    y: str
    d: Optional[str]
    use: str = Field(default="sig")
    kid: str
    typ: str = Field(default="JWT")

    @classmethod
    def generate_jwk_header(cls) -> JWKHeader:
        jwk = jose.JsonWebKey.generate_key(
            kty="EC",
            crv_or_size="P-256",
            options=dict(use="sig", typ="JWT"),
            is_private=True,
        )
        return cls(**jwk.as_dict(is_private=True))


class JWTPayload(BaseModel, allow_mutation=False):
    iss: pydantic.HttpUrl
    sub: str
    aud: str
    exp: float = Field(
        default_factory=lambda: datetime.datetime.utcnow().timestamp() + 3600
    )
    iat: float = Field(default_factory=lambda: datetime.datetime.utcnow().timestamp())

    @classmethod
    def generate_jwt_payload(
        cls, iss: pydantic.HttpUrl, sub: str, aud: str
    ) -> JWTPayload:
        return cls(iss=iss, sub=sub, aud=aud)

    @classmethod
    def generate_token(cls, iss: pydantic.HttpUrl, sub: str, aud: str) -> TokenTuple:
        """
        Use it like # JWTPayload.generate_token(
        iss="http://0.0.0.0", sub="5be86359073c434bad2da3932222dabe", aud="my_app")
        :param iss:
        :param sub:
        :param aud:
        :return:
        """
        jwk_header = JWKHeader.generate_jwk_header()
        jwk_header_dict = jwk_header.dict()
        jwk_key = jose.JsonWebKey.import_key(jwk_header_dict)
        jwt_payload = cls.generate_jwt_payload(iss=iss, sub=sub, aud=aud)
        return (
            jose.jwt.encode(
                jwk_header_dict, jwt_payload.dict(), jwk_key.as_key(is_private=True)
            ),
            jwk_header_dict,
        )

    @staticmethod
    def verify_token(token: bytes, jwk_header_dict: dict):
        jwk = jose.JsonWebKey.import_key(jwk_header_dict)
        tight_jwt = jose.JsonWebToken(jwk_header_dict["alg"])
        claims_payload = tight_jwt.decode(token, jwk)
        claims_payload.validate()

    @classmethod
    def decode_exp_tm_datetime(
        cls, token: bytes, jwk_header_dict: dict
    ) -> datetime.datetime:
        jwk = jose.JsonWebKey.import_key(jwk_header_dict)
        tight_jwt = jose.JsonWebToken(jwk_header_dict["alg"])
        claims_payload = tight_jwt.decode(token, jwk)
        return datetime.datetime.utcfromtimestamp(
            claims_payload["exp"]).astimezone(
            tz=datetime.timezone(datetime.timedelta(hours=2), "UTC")
        )
