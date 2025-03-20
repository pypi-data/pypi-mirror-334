from selenium.webdriver import EdgeOptions as Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.webdriver import WebDriver
from webdriver_manager.microsoft import (
    EdgeChromiumDriverManager as DriverManager,
)

from browser_manager.bases.browser_selenium import BrowserSelenium
from browser_manager.browser.msedge import MSEdge as MSEdgeBase


class MSEdge(
    MSEdgeBase,
    BrowserSelenium[DriverManager, Options, Service, WebDriver],
):
    pass


# Usage Example
if __name__ == '__main__':

    basic_example = True

    # Create an instance of the browser
    browser = MSEdge()

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
