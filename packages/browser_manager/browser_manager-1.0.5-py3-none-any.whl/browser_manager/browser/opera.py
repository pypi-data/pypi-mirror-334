import os

from browser_manager.utils.profile import BrowserProfile

from . import Chrome


class Opera(Chrome):
    @property
    def win_paths(self):
        return [os.path.join("Opera", "launcher.exe")]

    @property
    def linux_commands(self):
        return ["opera"]

    @property
    def data_paths(self) -> dict[str, str | None]:
        return {
            "Windows": os.path.join(
                self.user_home,
                "AppData",
                "Roaming",
                "Opera Software",
                "Opera Stable",
            ),
            "Linux": os.path.join(self.user_home, ".config", "opera"),
            "Darwin": os.path.join(
                self.user_home,
                "Library",
                "Application Support",
                "com.operasoftware.Opera",
            ),
        }

    def list_profiles(self):
        profiles: list[BrowserProfile] = []
        opera_profile_path = os.path.join(
            self.user_data_path, "Opera Software", "Opera Stable"
        )

        if os.path.exists(opera_profile_path) and os.path.isdir(
            opera_profile_path
        ):
            profile_dirs = [
                d
                for d in os.listdir(opera_profile_path)
                if os.path.isdir(os.path.join(opera_profile_path, d))
            ]
            for profile_dir in profile_dirs:
                path = os.path.join(opera_profile_path, profile_dir)
                profiles.append(BrowserProfile(name=profile_dir, path=path))

        return profiles


# Usage Example
if __name__ == '__main__':
    # Create an instance of the Firefox browser
    browser = Opera()

    # Select the preferred profile for the chosen browser
    # by passing the profile name "default-release"
    # If it's not available, a selection will be presented.
    # Selecting a profile is optional

    profile = browser.select_profile("default-release")
    print(f"Selected profile: {profile.name}")
    print(f"Selected profile folder: {profile.path}")
