from typing import Type, TypeAlias, Union

from order_app.domain.user.user import User
from order_app.utility.jwt import JWT_TOKEN
from order_app.repository.uow import AbstractUOW, MakeAbstractUOW
from order_app.repository.user_repository import UserOrNone

# See: https://github.com/python/mypy/pull/13785
UOWType: TypeAlias = Type[AbstractUOW]


# Application Service
class UserMgmtAppService:

    @classmethod
    def register_user(cls, uow: MakeAbstractUOW, **user_kwargs) -> JWT_TOKEN:
        UserService.register_user(uow, **user_kwargs)
        return cls.start_session(uow, **user_kwargs)


    @classmethod
    def start_session(cls, uow: MakeAbstractUOW, **user_kwargs) -> JWT_TOKEN:
        """Logs in a user and starts their session."""
        user = UserService.login_user(uow, **user_kwargs)
        session_token, jwk_header_dict = user.generate_authentication_token()
        with uow(atomic=True) as uow_ctx:
            with uow_ctx.atomic_txn:
                uow_ctx.user_repo.store_user_session(user.username, session_token, jwk_header_dict)
            uow_ctx.commit()
        return session_token


# Domain service
class UserService:
    @classmethod
    def register_user(cls, uow: MakeAbstractUOW, **user_kwargs):
        """Register a valid new user."""

        if cls.verify_user_exists(uow, **user_kwargs):  # type: ignore[type-abstract]
            raise ValueError("User already exists.")
        user = User.store(
            username=user_kwargs.get("username"),
            encrypted_password=user_kwargs.get("password")
        )
        with uow(atomic=True) as uow_ctx:
            with uow_ctx.atomic_txn:
                uow_ctx.user_repo.save_user(user)
            uow_ctx.commit()

    @classmethod
    def login_user(cls, uow: MakeAbstractUOW, **user_kwargs) -> User:
        """Login a legit user with an authentication token."""

        if not (user := cls.verify_user_exists(uow, **user_kwargs)):  # type: ignore[type-abstract]
            raise ValueError("Invalid credentials.")
        return user

    @classmethod
    def verify_user_exists(cls, uow: MakeAbstractUOW, **user_kwargs) -> UserOrNone:
        """Verify a user."""
        return user if (user := cls._validate_user(uow, **user_kwargs)) else None  # type: ignore[type-abstract]

    @classmethod
    def _validate_user(cls, uow: MakeAbstractUOW, **user_kwargs) -> UserOrNone:
        """Validate if user exists."""
        if not (
                (username := user_kwargs.get("username")) and
                (password := user_kwargs.get("password"))
        ):
            raise ValueError("Missing credential.")
        with uow() as uow_ctx:
            return uow_ctx.user_repo.get_user(username, password)
