"""Dependency injector plane to plug ports to adapters."""
from __future__ import annotations

from order_app.infrastructure.user_mgmt.user_uow import BuildUOW
from order_app.repository.uow import MakeAbstractUOW, AbstractUOW
from order_app.utility.singleton import Singleton


class Bootstrap:
    """Bootstrap the application with the dependencies."""

    def __init__(self, uow: AbstractUOW):
        self.__UOW = uow

    @property
    def uow(self) -> AbstractUOW:
        return self.__UOW

    @classmethod
    def build(cls, uow_factory: MakeAbstractUOW) -> Bootstrap:
        return cls(
            uow_factory()
        )


start_bootstrap = Bootstrap.build(BuildUOW)
