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

import typing as t

import click

from ..services.service import StellaNowService
from .logger import setup_logging
from .profile_manager import ProfileData, ProfileManager

DEFAULT = "DEFAULT"

T = t.TypeVar("T", bound=StellaNowService)
ServiceType = t.Type[T]
ServiceDict = t.Dict[ServiceType, T]


class StellaNowContext:
    def __init__(self):
        self._profile_manager: ProfileManager = ProfileManager()
        self._profile: str = DEFAULT
        self._verbose: bool = False
        self._services: ServiceDict = {}

    @property
    def profile(self) -> str:
        return self._profile

    @profile.setter
    def profile(self, profile: str) -> None:
        self._profile = profile
        self._profile_manager.profile = profile

    def save_service_config(self, service_name: str, service_config: ProfileData) -> None:
        self._profile_manager.save_service_config(service_name, service_config)

    @property
    def verbose(self) -> bool:
        return self._verbose

    @verbose.setter
    def verbose(self, verbose: bool) -> None:
        self._verbose = verbose
        setup_logging(verbose)

    def service_profile_data(self, service_name: str) -> ProfileData:
        return self._profile_manager.get_service_data(service_name)

    def get_config_value(self, service_name: str, config_key: str, default=None) -> str:
        """Get a specific configuration value for a service."""
        service_data = self.service_profile_data(service_name)
        return service_data.get(config_key, default)

    def get_service(self, service_type: t.Type[T]) -> T:
        service = self._services.get(service_type)
        if service is None:
            raise RuntimeError(f"Service of type {service_type.__name__} not found")
        return service

    def add_service(self, service: StellaNowService):
        self._services[type(service)] = service


pass_stella_context = click.make_pass_decorator(StellaNowContext, ensure=True)
