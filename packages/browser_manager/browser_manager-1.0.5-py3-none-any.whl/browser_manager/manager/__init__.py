from browser_manager.bases.browser import Browser
from browser_manager.bases.browser_manager import BrowserManagerBase
from browser_manager.browser import (
    Chrome,
    Chromium,
    Firefox,
    IExplore,
    MSEdge,
    Opera,
    Safari,
)
from browser_manager.utils.printer import Printer


class BrowserManager(BrowserManagerBase[Browser]):
    class BROWSERS(BrowserManagerBase[Browser].BROWSERS):
        CHROME = Chrome
        CHROMIUM = Chromium
        FIREFOX = Firefox
        IEXPLORE = IExplore
        MSEDGE = MSEdge
        OPERA = Opera
        SAFARI = Safari


# Usage Example
if __name__ == '__main__':
    # Create an instance of the BrowserManager class
    browser_manager = BrowserManager()

    # Select the preferred browser by passing
    # the desired browser class (Firefox)
    # If is not available, a selection will be presented.
    browser = browser_manager.select_browser([Firefox])
    Printer.info(f"Selected browser: {browser.name}")

    # Select the preferred profile for the chosen browser by
    # passing the profile name "default-release"
    # If is not available, a selection will be presented.
    # Selecting a profile is optional
    profile = browser.select_profile("default-release")
    Printer.info(f"Selected profile: {profile.name}")
    Printer.info(f"Selected profile folder: {profile.path}", end="\n\n")
