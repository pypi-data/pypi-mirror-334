import os
from typing import Dict

from browser_manager.bases.browser import Browser
from browser_manager.utils.profile import BrowserProfile


class Firefox(Browser):

    @property
    def win_paths(self):
        return [os.path.join("Mozilla Firefox", "firefox.exe")]

    @property
    def linux_commands(self):
        return ["firefox", "firefox-nightly"]

    @property
    def data_paths(self) -> Dict[str, str | None]:
        return {
            "Windows": os.path.join(
                self.user_home,
                "AppData",
                "Roaming",
                "Mozilla",
                "Firefox",
                "Profiles",
            ),
            "Linux": os.path.join(self.user_home, ".mozilla", "firefox"),
            "Darwin": os.path.join(
                self.user_home, "Library", "Application Support", "Firefox"
            ),
        }

    def list_profiles(self):
        profiles: list[BrowserProfile] = []
        profile_dirs = [
            d
            for d in os.listdir(self.user_data_path)
            if os.path.isdir(os.path.join(self.user_data_path, d))
        ]
        for profile_dir in profile_dirs:
            if os.path.isfile(
                os.path.join(self.user_data_path, profile_dir, "prefs.js")
            ):
                # Use o nome completo do perfil para seleção
                path = os.path.join(self.user_data_path, profile_dir)
                # Use apenas o nome da pasta para montar a URL
                name = profile_dir.split(".")[1]
                profiles.append(BrowserProfile(name=name, path=path))

        return profiles


# Usage Example
if __name__ == '__main__':
    # Create an instance of the Firefox browser
    browser = Firefox()

    # Select the preferred profile for the chosen browser
    # by passing the profile name "default-release"
    # If it's not available, a selection will be presented.
    # Selecting a profile is optional

    profile = browser.select_profile("default-release")
    print(f"Selected profile: {profile.name}")
    print(f"Selected profile folder: {profile.path}")
