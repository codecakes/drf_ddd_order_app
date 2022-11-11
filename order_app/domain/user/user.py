from __future__ import annotations
import pydantic

from order_app.utility.jwt import JWTPayload, TokenTuple


class User(pydantic.BaseModel):
    username: str
    encrypted_password: str

    @classmethod
    def store(cls, username: str, encrypted_password: str) -> User:
        return cls(username=username, encrypted_password=encrypted_password)

    @staticmethod
    def generate_authentication_token() -> TokenTuple:
        # TODO: get values from configuration
        return JWTPayload.generate_token(
            iss=pydantic.HttpUrl("http://0.0.0.0", scheme="http"),
            sub="5be86359073c434bad2da3932222dabe",
            aud="order_app",
        )
