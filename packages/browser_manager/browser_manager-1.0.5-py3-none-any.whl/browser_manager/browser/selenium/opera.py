from webdriver_manager.opera import OperaDriverManager as DriverManager

from browser_manager.browser.opera import Opera as OperaBase
from browser_manager.browser.selenium.chrome import Chrome


class Opera(OperaBase, Chrome):
    driver_manager_cls = DriverManager


# Usage Example
if __name__ == '__main__':

    basic_example = True

    # Create an instance of the browser
    browser = Opera()

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
