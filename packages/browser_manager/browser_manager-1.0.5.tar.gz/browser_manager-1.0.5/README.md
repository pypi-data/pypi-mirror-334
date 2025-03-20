# BrowserManager Library

## Description

The **BrowserManager Library** simplifies browser automation and management by detecting installed browsers, selecting user profiles, and integrating with Selenium WebDriver for automated testing and tasks. The library abstracts the logic for locating installed browsers on the system, configuring user profiles, and managing drivers, with support for **Windows**, **Linux**, and **macOS**.

## Features

- **Automatic Detection of Installed Browsers**: Supports Chrome, Chromium, Firefox, Microsoft Edge, Safari, Opera, and Internet Explorer.
- **Profile Management**: Lists and selects user profiles for the browsers.
- **Selenium WebDriver Automation**: Easy integration with Selenium for browser automation.

## Installation

To install the library, run:

```bash
pip install browser_manager
```

## Usage Examples

### Example Usage with BrowserManager

Here's a example of how to use the library to automate a browser session:

```python
from browser_manager import BrowserManager
from browser_manager.browser import Firefox

# Create an instance of the BrowserManager class
browser_manager = BrowserManager()

# Select the preferred browser by passing the desired browser class (Firefox)
# If it's not available, a selection will be presented.
browser = browser_manager.select_browser(Firefox)
print(f"Selected browser: {browser.name}")  # Print the name of the selected browser

# Select the preferred profile for the chosen browser by passing the profile name "default-release"
# If it's not available, a selection will be presented.
# Selecting a profile is optional
profile = browser.select_profile("default-release")
print(f"Selected profile: {profile['name']}")  # Print the name of the selected profile
print(f"Selected profile folder: {profile['path']}")  # Print the path of the selected profile

# Get the driver for the selected browser
driver = browser.get_driver()
print(f"Driver Path: {browser.driver_path}")  # Print the path of the driver
print(f"Driver: {driver}")  # Print the driver object

# Navigate to Google
driver.get("https://google.com")
print(driver.title)

# Wait for user input before closing the browser session
input("Press Enter to close the browser...")

# Close the browser session
driver.quit()
```

### Example Usage Directly from Firefox

Here’s how to use the `Firefox` class directly:

```python
from browser_manager.browser import Firefox

# Create an instance of the Firefox browser
browser = Firefox()

# Select the preferred profile for the chosen browser by passing the profile name "default-release"
# If it's not available, a selection will be presented.
# Selecting a profile is optional
profile = browser.select_profile("default-release")
print(f"Selected profile: {profile['name']}")  # Print the name of the selected profile
print(f"Selected profile folder: {profile['path']}")  # Print the path of the selected profile

# Get the driver for the selected browser
driver = browser.get_driver()
print(f"Driver Path: {browser.driver_path}")  # Print the path of the driver
print(f"Driver: {driver}")  # Print the driver object

# Navigate to Google
driver.get("https://google.com")
print(driver.title)

# Wait for user input before closing the browser session
input("Press Enter to close the browser...")

# Close the browser session
driver.quit()
```

### Basic Usage Example

Here’s a simple example of how to directly use the Firefox browser with the BrowserManager library:

```python
from browser_manager.browser import Firefox

# Create an instance of the Firefox browser
driver = Firefox().get_driver()

# Navigate to Google
driver.get("https://google.com")
print(driver.title)

# Wait for user input before closing the browser session
input("Press Enter to close the browser...")

# Close the browser session
driver.quit()
```

## Supported Platforms

- **Windows**
- **Linux**
- **macOS**

## License

This project is licensed under the MIT License.

## Contact

For any inquiries, please contact: [contato@tpereira.com.br](mailto:contato@tpereira.com.br)


## Contributing

Feel free to submit pull requests or open issues to improve the library. Please ensure that your code follows the repository's coding standards and is well-documented.
```