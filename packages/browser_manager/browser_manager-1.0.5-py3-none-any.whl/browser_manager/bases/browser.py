import os
import platform
import subprocess
from abc import ABC, abstractmethod

from browser_manager.interfaces.browser import IBrowser
from browser_manager.utils.printer import Printer
from browser_manager.utils.profile import BrowserProfile


class Browser(IBrowser, ABC):
    def __init__(self):
        self._profile: BrowserProfile | None = None
        self._driver_path: str | None = None
        self._binary_location: str | None = None

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def profile(self) -> BrowserProfile | None:
        return self._profile

    @profile.setter
    def profile(self, value: BrowserProfile):
        self._profile = value

    @property
    def binary_location(self) -> str | None:
        return self._binary_location

    @binary_location.setter
    def binary_location(self, value: str):
        self._binary_location = value

    @property
    def user_home(self) -> str:
        return os.path.expanduser("~")

    @property
    def system(self) -> str:
        return platform.system()

    @property
    def user_data_path(self) -> str:
        if self.system in self.data_paths:
            data_path = self.data_paths[self.system]
            if isinstance(data_path, str):
                return data_path

        raise ValueError(
            "Unsupported browser or operating system: {} on {}".format(
                self.__class__.__name__, self.system
            )
        )

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
    def is_installed(self) -> bool:
        if platform.system() == "Windows":
            return self._is_installed_windows

        if platform.system() == "Linux" or platform.system() == "Darwin":
            return self._is_installed_linux

        raise AttributeError("Platform not supported")

    @property
    def _is_installed_windows(self) -> bool:
        # Verifica o diretório do Program Files (x86)
        program_files_dirs = [
            os.environ.get("ProgramFiles(x86)"),
            os.environ.get("ProgramFiles"),
        ]

        for program_files_dir in program_files_dirs:
            if program_files_dir:
                for path in self.win_paths:
                    path = os.path.join(program_files_dir, path)
                    if os.path.isfile(path):
                        return True
        return False

    @property
    def _is_installed_linux(self) -> bool:
        if any(
            self._is_linux_command_available(command)
            for command in self.linux_commands
        ):
            return True

        return False

    def _is_linux_command_available(self, command: str):
        try:
            command_path = (
                subprocess.check_output(
                    ["which", command], stderr=subprocess.DEVNULL
                )
                .decode()
                .strip()
            )
            self.binary_location = command_path
            return True
        except subprocess.CalledProcessError:
            return False

    @property
    def driver_path(self) -> str:
        if not self._driver_path:
            raise AttributeError("webdriver_manager not installed")

        return self._driver_path

    @driver_path.setter
    def driver_path(self, path: str):
        self._driver_path = path

    def select_profile(self, profile_name: str | None = None):
        profiles = self.list_profiles()
        print()

        if not profiles:
            raise AttributeError("Profiles not found")

        if profile_name:
            matched_profile = next(
                (
                    profile
                    for profile in profiles
                    if profile.name == profile_name
                    or profile.path == profile_name
                ),
                None,
            )
            if matched_profile:
                profile = matched_profile
                self.profile = matched_profile
                return matched_profile

            Printer.warning("Selected profile is not find.")

        if len(profiles) == 1:
            profile = profiles[0]
            self.profile = profile
            print(
                f"\
Only one profile detected: {profile.name}. \
It has been automatically selected."
            )
            return profile

        while True:
            Printer.title("Available profiles:")
            for i, profile in enumerate(profiles, start=1):
                print(f"{i}. {profile.name}")

            Printer.info("Choose the profile number you want to use: ")
            selected = input()
            print()

            try:
                selected = int(selected)
                if 1 <= selected <= len(profiles):
                    profile = profiles[selected - 1]
                    self.profile = profile
                    return profile
                else:
                    Printer.warning(
                        "Invalid profile number. Please choose a valid number."
                    )
            except ValueError:
                Printer.warning("Invalid Input. Please enter a valid number.")
