from abc import ABC, abstractmethod

from browser_manager.utils.profile import BrowserProfile


class IBrowser(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def profile(self) -> BrowserProfile | None:
        pass

    @profile.setter
    @abstractmethod
    def profile(self, value: BrowserProfile):
        pass

    @profile.setter
    @abstractmethod
    def profile(self, value: BrowserProfile):
        pass

    @property
    @abstractmethod
    def binary_location(self) -> str | None:
        pass

    @binary_location.setter
    @abstractmethod
    def binary_location(self, value: str):
        pass

    @property
    @abstractmethod
    def user_home(self) -> str:
        pass

    @property
    @abstractmethod
    def system(self) -> str:
        pass

    @property
    @abstractmethod
    def user_data_path(self) -> str:
        pass

    @property
    @abstractmethod
    def win_paths(self) -> list[str]:
        pass

    @property
    @abstractmethod
    def linux_commands(self) -> list[str]:
        pass

    @property
    @abstractmethod
    def data_paths(self) -> dict[str, str | None]:
        pass

    @abstractmethod
    def list_profiles(self) -> list[BrowserProfile]:
        pass

    @property
    @abstractmethod
    def is_installed(self) -> bool:
        pass

    @property
    @abstractmethod
    def _is_installed_windows(self) -> bool:
        pass

    @property
    @abstractmethod
    def _is_installed_linux(self) -> bool:
        pass

    @abstractmethod
    def _is_linux_command_available(self, command: str) -> bool:
        pass

    @property
    @abstractmethod
    def driver_path(self) -> str:
        pass

    @driver_path.setter
    @abstractmethod
    def driver_path(self, path: str):
        pass

    @abstractmethod
    def select_profile(
        self, profile_name: str | None = None
    ) -> BrowserProfile:
        pass
