import json
import os

from browser_manager.bases.browser import Browser
from browser_manager.utils.profile import BrowserProfile


class MSEdge(Browser):
    @property
    def win_paths(self):
        return [
            os.path.join("Microsoft", "Edge", "Application", "msedge.exe")
        ]

    @property
    def linux_commands(self):
        return ["msedge", "MicrosoftEdge"]

    @property
    def data_paths(self) -> dict[str, str | None]:
        return {
            "Windows": os.path.join(
                self.user_home,
                "AppData",
                "Local",
                "Microsoft",
                "Edge",
                "User Data",
            ),
        }

    def list_profiles(self):
        profiles: list[BrowserProfile] = []
        local_state_path = os.path.join(self.user_data_path, "Local State")

        if os.path.isfile(local_state_path):
            with open(
                local_state_path, "r", encoding="utf-8"
            ) as local_state_file:
                local_state = json.load(local_state_file)
                if "profile" in local_state:
                    profiles_order = local_state["profile"].get(
                        "profiles_order", []
                    )
                    info_cache = local_state["profile"].get("info_cache", {})

                    for id in sorted(
                        profiles_order,
                        key=lambda x: info_cache[x].get("name", ""),
                    ):
                        if id in info_cache:
                            info = info_cache[id]
                            path = os.path.join(self.user_data_path, id)
                            if "name" in info:
                                name = info["name"]
                                profiles.append(
                                    BrowserProfile(name=name, path=path)
                                )

        profiles.sort(key=lambda profile: profile.name)
        return profiles
