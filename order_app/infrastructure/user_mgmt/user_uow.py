from __future__ import annotations

import contextlib
from typing import Optional

from django.db import transaction

from order_app.infrastructure.user_mgmt.user_repository import UserRepo
from order_app.repository.uow import AbstractUOW, MakeAbstractUOW


class UserUOW(AbstractUOW):

    def __init__(self, atomic:bool = False) -> None:
        self.user_repo = UserRepo()
        self.__atomic = atomic
        self.atomic_txn: Optional[transaction.atomic] = None

    def __enter__(self) -> AbstractUOW:
        if not self.user_repo:
            raise ValueError("User repository not set")

        if transaction.get_autocommit():
            transaction.set_autocommit(False)

        if self.__atomic:
            stack = contextlib.ExitStack()
            stack.enter_context(transaction.atomic())
            self.atomic_txn = stack
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_val:
            self.rollback()
            if exc_tb:
                raise exc_type from exc_val.with_traceback(exc_tb)
            raise exc_type from exc_val
        if not transaction.get_autocommit():
            transaction.set_autocommit(True)

    def commit(self) -> None:
        """Manually commit a transaction."""
        transaction.commit()

    def rollback(self) -> None:
        if not self.atomic_txn and (rollback := transaction.get_rollback()):
            transaction.set_rollback(rollback)
        else:
            self.atomic_txn.pop_all()
        if not transaction.get_autocommit():
            transaction.set_autocommit(True)


class BuildUOW(MakeAbstractUOW):

    def __call__(self, atomic: bool = False) -> AbstractUOW:
        return UserUOW(atomic=atomic)

