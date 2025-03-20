from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from browser_manager.interfaces.browser import IBrowser

TBrowser = TypeVar("TBrowser", bound=IBrowser)


class IBrowserManager(ABC, Generic[TBrowser]):
    def __init__(self):
        self.installeds = None
        self._browser: TBrowser | None = None

    @property
    @abstractmethod
    def browser(self) -> TBrowser:
        pass

    @browser.setter
    @abstractmethod
    def browser(self, value: TBrowser):
        pass

    @abstractmethod
    def get_installeds(self) -> list[type[TBrowser]]:
        pass

    @abstractmethod
    def _get_installeds_windows(self) -> list[type[TBrowser]]:
        pass

    @abstractmethod
    def _get_installeds_linux(self) -> list[type[TBrowser]]:
        pass

    @abstractmethod
    def _is_command_available(self, command: str) -> bool:
        pass

    @abstractmethod
    def select_browser(
        self, preferred_browsers: list[type[TBrowser]] = []
    ) -> TBrowser:
        pass
