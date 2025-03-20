import os
from abc import ABC
from typing import Any, Generic, TypeVar

from selenium.webdriver.common.options import ArgOptions
from selenium.webdriver.common.service import Service
from selenium.webdriver.remote.webdriver import WebDriver

from browser_manager.bases.browser import Browser
from browser_manager.interfaces.browser_selenium import (
    DriverManagerProtocol,
    IBrowserSelenium,
)
from browser_manager.utils.printer import Printer

TDriverManager = TypeVar(
    "TDriverManager",
    bound=DriverManagerProtocol,
    default=DriverManagerProtocol,
    covariant=True,
)
TOptions = TypeVar(
    "TOptions", bound=ArgOptions, default=ArgOptions, covariant=True
)
TService = TypeVar("TService", bound=Service, default=Service, covariant=True)
TDriver = TypeVar(
    "TDriver", bound=WebDriver, default=WebDriver, covariant=True
)


class BrowserSelenium(
    Browser,
    IBrowserSelenium[TDriverManager, TOptions, TService, TDriver],
    ABC,
    Generic[TDriverManager, TOptions, TService, TDriver],
):

    def __init_subclass__(cls, **kwargs: dict[str, Any]):
        super().__init_subclass__(**kwargs)
        orig_bases = getattr(cls, "__orig_bases__")

        if orig_bases:

            for bases in orig_bases:
                args = getattr(bases, "__args__", None)
                if args and len(args) == 4:
                    if not hasattr(cls, "driver_manager_cls"):
                        cls.driver_manager_cls = args[0]
                    if not hasattr(cls, "options_cls"):
                        cls.options_cls = args[1]
                    if not hasattr(cls, "service_cls"):
                        cls.service_cls = args[2]
                    if not hasattr(cls, "driver_cls"):
                        cls.driver_cls = args[3]

    def __init__(self):
        super().__init__()
        self._options: TOptions = self.options_cls()
        self._driver: TDriver | None = None

    @property
    def driver_path(self) -> str:
        if not self._driver_path:
            os.environ["WDM_LOG_LEVEL"] = "0"
            Printer.wait("Downloading Browser Driver...")
            driver_manager = self.driver_manager_cls()
            self._driver_path = driver_manager.install()

            Printer.success("Browser Driver downloaded Successfully!")

        return self._driver_path

    @driver_path.setter
    def driver_path(self, path: str):
        self._driver_path = path

    @property
    def options(self) -> TOptions:
        options = self._options

        if self.profile:
            if hasattr(options, "profile"):
                setattr(options, "profile", self.profile.path)

        self._options = options
        return self._options

    @options.setter
    def options(self, options: TOptions):  # type: ignore
        self._options = options

        if self.profile:
            if hasattr(self.options, "profile"):
                setattr(self._options, "profile", self.profile.path)

    @property
    def driver(self, options: TOptions | None = None) -> TDriver:
        if self._driver:
            return self._driver

        if self.is_installed:
            if options:
                self.options = options
            else:
                self.options = self.options

            executable_path = self.driver_path
            service = self.service_cls(
                executable_path=executable_path
            )  # type: ignore

            if self.options:
                if self.binary_location:
                    if hasattr(self.options, "binary_location"):
                        setattr(
                            self._options,
                            "binary_location",
                            self.binary_location,
                        )

                self._driver = self.driver_cls(
                    service=service, options=self.options  # type: ignore
                )

            else:
                self._driver = self.driver_cls(service=service)  # type: ignore

            return self._driver
        else:
            raise ValueError("Browser is not installed.")
