import importlib.util
import subprocess
import sys

selenium_installed = importlib.util.find_spec("selenium") is not None

if selenium_installed:
    from browser_manager.manager.selenium import BrowserManager

    module_path = "browser_manager.manager.selenium.__init__"
else:
    from browser_manager.manager import BrowserManager

    module_path = "browser_manager.manager.__init__"

__all__ = ["BrowserManager"]

if __name__ == "__main__":
    subprocess.run([sys.executable, "-m", module_path])
