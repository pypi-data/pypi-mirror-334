import json
import os

from browser_manager.bases.browser import Browser
from browser_manager.utils.profile import BrowserProfile


class Chrome(Browser):
    @property
    def win_paths(self):
        return [os.path.join("Google", "Chrome", "Application", "chrome.exe")]

    @property
    def linux_commands(self):
        return ["google-chrome", "google-chrome-stable"]

    @property
    def data_paths(self) -> dict[str, str | None]:
        return {
            "Windows": os.path.join(
                self.user_home,
                "AppData",
                "Local",
                "Google",
                "Chrome",
                "User Data",
            ),
            "Linux": os.path.join(self.user_home, ".config", "google-chrome"),
            "Darwin": os.path.join(
                self.user_home,
                "Library",
                "Application Support",
                "Google",
                "Chrome",
            ),
        }

    def list_profiles(self) -> list[BrowserProfile]:
        profiles: list[BrowserProfile] = []
        local_state_path = os.path.join(self.user_data_path, "Local State")

        if os.path.isfile(local_state_path):
            with open(
                local_state_path, "r", encoding="utf-8"
            ) as local_state_file:
                local_state = json.load(local_state_file)
                if "profile" in local_state:
                    info_cache = local_state["profile"].get("info_cache", {})

                    for id, info in info_cache.items():
                        if "name" in info:
                            name = info["name"]
                            path = os.path.join(self.user_data_path, id)
                            profiles.append(
                                BrowserProfile(name=name, path=path)
                            )

        profiles.sort(key=lambda profile: profile.name)
        return profiles


# Usage Example
if __name__ == '__main__':
    # Create an instance of the Firefox browser
    browser = Chrome()

    # Select the preferred profile for the chosen browser
    # by passing the profile name "default-release"
    # If it's not available, a selection will be presented.
    # Selecting a profile is optional

    profile = browser.select_profile("default-release")
    print(f"Selected profile: {profile.name}")
    print(f"Selected profile folder: {profile.path}")
