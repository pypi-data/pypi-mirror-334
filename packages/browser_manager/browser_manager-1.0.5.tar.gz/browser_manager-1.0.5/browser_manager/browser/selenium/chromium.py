import os

from webdriver_manager.core.os_manager import ChromeType

from browser_manager.browser.selenium.chrome import Chrome
from browser_manager.utils.printer import Printer


class Chromium(Chrome):
    @property
    def driver_path(self) -> str:
        if not self._driver_path:
            os.environ["WDM_LOG_LEVEL"] = "0"
            Printer.wait("Downloading Browser Driver...")
            driver_manager = self.driver_manager_cls(
                chrome_type=ChromeType.CHROMIUM
            )
            self._driver_path = driver_manager.install()

            Printer.success("Browser Driver downloaded Successfully!")

        return self._driver_path

    @driver_path.setter
    def driver_path(self, path: str):
        self._driver_path = path


# Usage Example
if __name__ == '__main__':

    basic_example = True

    # Create an instance of the browser
    browser = Chromium()

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
