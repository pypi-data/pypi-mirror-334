from browser_manager.bases.browser_manager import BrowserManagerBase
from browser_manager.bases.browser_selenium import BrowserSelenium
from browser_manager.browser.selenium import (
    Chrome,
    Chromium,
    Firefox,
    IExplore,
    MSEdge,
    Opera,
    Safari,
)
from browser_manager.utils.printer import Printer


class BrowserManager(BrowserManagerBase[BrowserSelenium]):
    class BROWSERS(BrowserManagerBase[BrowserSelenium].BROWSERS):
        CHROME = Chrome
        CHROMIUM = Chromium
        FIREFOX = Firefox
        IEXPLORE = IExplore
        MSEDGE = MSEdge
        OPERA = Opera
        SAFARI = Safari


# Usage Example
if __name__ == '__main__':

    basic_example = True

    # Create an instance of the BrowserManager class
    browser_manager = BrowserManager()

    # Select the preferred browser by passing
    # the desired browser class (Firefox)
    # If is not available, a selection will be presented.
    browser = browser_manager.select_browser([Firefox])
    Printer.info(f"Selected browser: {browser.name}")

    if not basic_example:
        # Select the preferred profile for the chosen browser
        # by passing the profile name "default-release"
        # If it's not available, a selection will be presented.
        # Selecting a profile is optional
        profile = browser.select_profile("default-release")
        Printer.info(
            f"Selected profile: {profile.name}"
        )  # Print the name of the selected profile
        Printer.info(
            f"Selected profile folder: {profile.path}", end="\n\n"
        )  # Print the path of the selected profile

    # Get the driver for the selected browser
    driver = browser.driver
    print()

    # Print the path of the driver
    Printer.info("Driver Path:", end=" ")
    Printer.info(browser.driver_path, end="\n")

    # Print the driver object
    Printer.info("Driver:", end=" ")
    Printer.info(f"{driver}", end="\n\n")

    # Navigate to Google
    driver.get("https://google.com")
    Printer.title(f"Page title: {driver.title}")

    # Wait for user input before closing the browser session
    Printer.warning("Press Enter to close the browser...")
    input()

    # Close the browser session
    driver.quit()
