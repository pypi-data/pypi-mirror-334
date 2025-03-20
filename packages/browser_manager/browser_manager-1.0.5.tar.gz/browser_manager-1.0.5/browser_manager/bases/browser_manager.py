import os
import platform
import subprocess
from abc import ABC
from enum import Enum
from typing import Generic, TypeVar

from browser_manager.bases.browser import Browser
from browser_manager.interfaces.browser_manager import IBrowserManager
from browser_manager.utils.printer import Printer

TBrowser = TypeVar("TBrowser", bound=Browser)


class BrowserManagerBase(
    IBrowserManager[TBrowser],
    ABC,
    Generic[TBrowser],
):

    class BROWSERS(Enum):
        @property
        def value(self) -> type[TBrowser]:
            return self._value_

        @classmethod
        def items(cls):
            return ((browser.name, browser.value) for browser in cls)

    @property
    def browser(self) -> TBrowser:
        if self._browser:
            return self._browser
        return self.select_browser()

    @browser.setter
    def browser(self, value: TBrowser):
        self._browser = value

    def get_installeds(self) -> list[type[TBrowser]]:
        system = platform.system()
        if system == "Windows":
            return self._get_installeds_windows()

        if system == "Linux" or system == "Darwin":
            return self._get_installeds_linux()

        raise AttributeError(f"Unsupported operating system: {system}")

    def _get_installeds_windows(self) -> list[type[TBrowser]]:
        installeds: list[type[TBrowser]] = []

        # Verifica o diretório do Program Files (x86)
        program_files_dirs = [
            os.environ.get("ProgramFiles(x86)"),
            os.environ.get("ProgramFiles"),
        ]
        for _, browser in self.BROWSERS.items():
            for program_files_dir in program_files_dirs:
                for browser_path in browser().win_paths:
                    if program_files_dir:
                        path = os.path.join(program_files_dir, browser_path)

                        if os.path.isfile(path):
                            installeds.append(browser)
                            break
                if browser in installeds:
                    break
            if browser in installeds:
                break

        self.installeds = installeds
        return self.installeds

    def _get_installeds_linux(self) -> list[type[TBrowser]]:
        installeds: list[type[TBrowser]] = []

        for _, browser in self.BROWSERS.items():
            commands = browser().linux_commands
            if any(
                self._is_command_available(command) for command in commands
            ):
                installeds.append(browser)

        self.installeds = installeds
        return self.installeds

    def _is_command_available(self, command: str) -> bool:
        try:
            subprocess.check_output(
                ["which", command], stderr=subprocess.DEVNULL
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def select_browser(
        self,
        preferred_browsers: list[type[TBrowser]] = [],
    ) -> TBrowser:
        installeds = self.get_installeds()

        if not installeds:
            raise AttributeError("No installed browser found.")

        for preferred_browser in preferred_browsers:
            if isinstance(preferred_browser, self.BROWSERS):
                preferred_browser = preferred_browser.value
            if preferred_browser in installeds:
                self._browser = preferred_browser()
                return self._browser

            Printer.warning("Selected browser is not installed.", end="\n\n")

        if len(installeds) == 1:
            self._browser = installeds[0]()
            Printer.info("Only one browser detected:", end=" ")
            Printer.title(self._browser.name, end=".\n")
            Printer.info("It has been automatically selected.", end="\n\n")
            return self._browser

        while True:
            Printer.title("Installed browsers:")
            for i, name in enumerate(installeds, start=1):
                Printer.info(f"{i}. {name}")

            Printer.warning("Choose browser number:")
            selected = input("")
            print()

            try:
                selected = int(selected)
                if 1 <= selected <= len(installeds):
                    self._browser = installeds[selected - 1]()
                    return self._browser
                else:
                    Printer.warning("Invalid browser number.")
            except ValueError:
                Printer.warning("Invalid Input. Please enter a valid number.")
