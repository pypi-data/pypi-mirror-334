"""
Copyright (C) 2022-2025 Stella Technologies (UK) Limited.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

import configparser
import os
import typing as t

from loguru import logger

STORAGE_FOLDER = ".stellanow"
CONFIG_FILE = "config.ini"


ProfileData = t.Dict[str, t.Any]


class ProfileManager:
    def __init__(self):
        self._loaded = False

        self.config: configparser.ConfigParser = configparser.ConfigParser(interpolation=None)

        self._profile: t.Optional[str] = None
        self.profile_data: ProfileData = {}  # This will store the loaded profile data

    def _load(self) -> None:
        home = os.path.expanduser("~")
        config_file = os.path.join(home, STORAGE_FOLDER, CONFIG_FILE)
        self.config.read(config_file)

        prefix = f"{self.profile}"
        for section in self.config.sections():
            if section.startswith(prefix):
                module_name = section[len(prefix) + 1 :]
                self.profile_data[module_name] = {k: v for k, v in self.config.items(section)}

    def save_service_config(self, service: str, service_data: ProfileData) -> None:
        home = os.path.expanduser("~")
        config_dir = os.path.join(home, STORAGE_FOLDER)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)  # Create the directory if it does not exist

        config_file = os.path.join(config_dir, CONFIG_FILE)
        self.config[f"{self.profile}:{service}"] = service_data

        # Save the updated configuration to the file
        with open(config_file, "w") as configfile:
            self.config.write(configfile)

        logger.success(f"Configuration for profile '{self.profile}' and service '{service}' saved successfully")

    @property
    def profile(self) -> t.Optional[str]:
        """Get the current profile."""
        return self._profile

    @profile.setter
    def profile(self, new_profile: str) -> None:
        """Set a new profile and reload data."""
        self._profile = new_profile
        self._load()  # Reload the data for the new profile

    def get_profile_data(self) -> ProfileData:
        return self.profile_data

    def get_service_data(self, service: str) -> ProfileData:
        return self.profile_data.get(service, {})
