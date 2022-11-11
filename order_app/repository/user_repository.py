import abc
from typing import Protocol, Optional

from order_app.domain.user.user import User

UserOrNone = Optional[User]


class AbstractUserRepository(Protocol):

    @abc.abstractmethod
    def get_user(self, username: str, password: str) -> UserOrNone:
        raise NotImplementedError

    @abc.abstractmethod
    def save_user(self, user: User) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def store_user_session(self, username: str, session_token: bytes, jwk_header_dict: dict) -> None:
        raise NotImplementedError
