from __future__ import annotations

import abc
import contextlib
from typing import Protocol, Optional

from order_app.repository.user_repository import AbstractUserRepository


class AbstractUOW(Protocol):

    user_repo: AbstractUserRepository
    atomic_txn: Optional[contextlib.AbstractContextManager]

    @abc.abstractmethod
    def __enter__(self) -> AbstractUOW:
        raise NotImplementedError

    @abc.abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError


# Cannot instantiate a class protocol with arguments passed
# as it does not recognize. See here for workaround:
#     https://stackoverflow.com/a/61737894
class MakeAbstractUOW(Protocol):
    def __call__(self, atomic: bool = False) -> AbstractUOW:
        raise NotImplementedError
