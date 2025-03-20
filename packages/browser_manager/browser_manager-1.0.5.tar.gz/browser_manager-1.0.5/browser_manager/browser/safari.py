import os

from browser_manager.bases.browser import Browser
from browser_manager.utils.profile import BrowserProfile


class Safari(Browser):
    @property
    def win_paths(self):
        return [os.path.join("Safari", "safari.exe")]

    @property
    def linux_commands(self):
        return ["safari"]

    @property
    def data_paths(self) -> dict[str, str | None]:
        return {
            "Darwin": os.path.join(self.user_home, "Library", "Safari"),
        }

    def list_profiles(self):
        profiles: list[BrowserProfile] = []
        safari_profiles_path = os.path.join(self.user_data_path, "Profiles")

        if os.path.exists(safari_profiles_path) and os.path.isdir(
            safari_profiles_path
        ):
            profile_dirs = [
                d
                for d in os.listdir(safari_profiles_path)
                if os.path.isdir(os.path.join(safari_profiles_path, d))
            ]
            for profile_dir in profile_dirs:
                path = os.path.join(safari_profiles_path, profile_dir)
                profiles.append(BrowserProfile(name=profile_dir, path=path))

        return profiles


# Usage Example
if __name__ == '__main__':
    # Create an instance of the Firefox browser
    browser = Safari()

    # Select the preferred profile for the chosen browser
    # by passing the profile name "default-release"
    # If it's not available, a selection will be presented.
    # Selecting a profile is optional

    profile = browser.select_profile("default-release")
    print(f"Selected profile: {profile.name}")
    print(f"Selected profile folder: {profile.path}")
