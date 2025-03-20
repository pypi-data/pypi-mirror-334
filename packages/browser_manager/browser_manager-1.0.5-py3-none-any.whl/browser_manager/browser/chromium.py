import os

from browser_manager.browser import Chrome


class Chromium(Chrome):
    @property
    def win_paths(self):
        return [os.path.join("Chromium", "Application", "chrome.exe")]

    @property
    def linux_commands(self):
        return ["chromium", "chromium-browser", "chromium-browser-laptop"]

    @property
    def data_paths(self) -> dict[str, str | None]:
        return {
            "Windows": "",
            # Chromium não é suportado no Windows por padrão
            "Linux": os.path.join(self.user_home, ".config", "chromium"),
            "Darwin": "",
            # Chromium não é suportado no macOS por padrão
        }
