from abc import ABC, abstractmethod
from typing import Generic, Protocol, TypeVar

from browser_manager.interfaces.browser import IBrowser
from browser_manager.utils.profile import BrowserProfile


class DriverManagerProtocol(Protocol):
    def install(self) -> str: ...


TDriverManager = TypeVar(
    "TDriverManager", bound=DriverManagerProtocol, covariant=True
)
TOptions = TypeVar("TOptions", bound=object, covariant=True)
TService = TypeVar("TService", bound=object, covariant=True)
TDriver = TypeVar("TDriver", bound=object, covariant=True)


class IBrowserSelenium(
    IBrowser,
    ABC,
    Generic[TDriverManager, TOptions, TService, TDriver],
):
    driver_manager_cls: type[TDriverManager]
    options_cls: type[TOptions]
    service_cls: type[TService]
    driver_cls: type[TDriver]

    def __init__(self):
        self._options: TOptions
        self._driver: TDriver

    @property
    @abstractmethod
    def options(self) -> TOptions:
        pass

    @options.setter
    @abstractmethod
    def options(self, options: TOptions):  # type: ignore
        pass

    @property
    @abstractmethod
    def driver(self, options: TOptions | None = None) -> TDriver:
        pass

    @abstractmethod
    def select_profile(
        self, profile_name: str | None = None
    ) -> BrowserProfile:
        pass
