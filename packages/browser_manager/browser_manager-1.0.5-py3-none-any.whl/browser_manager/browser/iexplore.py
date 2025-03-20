import os

from browser_manager.bases.browser import Browser
from browser_manager.utils.profile import BrowserProfile


class IExplore(Browser):
    @property
    def win_paths(self):
        return [os.path.join("Internet Explorer", "iexplore.exe")]

    @property
    def linux_commands(self):
        return ["iexplore"]

    @property
    def data_paths(self) -> dict[str, str | None]:
        return {
            "Windows": os.path.join(
                self.user_home,
                "AppData",
                "Local",
                "Microsoft",
                "Internet Explorer",
            ),
        }

    def list_profiles(self):
        profiles: list[BrowserProfile] = []
        return profiles
