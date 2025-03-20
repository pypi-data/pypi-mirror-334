from selenium.webdriver.safari.options import Options
from selenium.webdriver.safari.service import Service
from selenium.webdriver.safari.webdriver import WebDriver

from browser_manager.bases.browser_selenium import BrowserSelenium
from browser_manager.browser.safari import Safari as SafariBase
from browser_manager.interfaces.browser_selenium import DriverManagerProtocol


class Safari(
    SafariBase,
    BrowserSelenium[DriverManagerProtocol, Options, Service, WebDriver],
):

    @property
    def driver(self, options: Options | None = None) -> WebDriver:
        if self._driver:
            return self._driver

        if self.is_installed:
            if options:
                self.options = options
            else:
                self.options = self.options

            service = self.service_cls()  # type: ignore

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


# Usage Example
if __name__ == '__main__':

    basic_example = True

    # Create an instance of the browser
    browser = Safari()

    if not basic_example:
        # Select the preferred profile for the chosen browser
        # by passing the profile name "default-release"
        # If it's not available, a selection will be presented.
        # Selecting a profile is optional
        profile = browser.select_profile("default-release")
        print(
            f"Selected profile: {profile.name}"
        )  # Print the name of the selected profile
        print(
            f"Selected profile folder: {profile.path}"
        )  # Print the path of the selected profile

    # Get the driver for the selected browser
    driver = browser.driver
    print(
        f"Driver Path: {browser.driver_path}"
    )  # Print the path of the driver
    print(f"Driver: {driver}")  # Print the driver object

    # Navigate to Google
    driver.get("https://google.com")
    print(driver.title)

    # Wait for user input before closing the browser session
    input("Press Enter to close the browser...")

    # Close the browser session
    driver.quit()
