# SPDX-FileCopyrightText: 2025 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-3.0-only
import inspect
import sys

from KMC.configuration.base import KmcConfiguration
from KMC.configuration.base import KmcConfigurationItem
from KMC.configuration.base import ParseValue


class ServerDisplayConfiguration(KmcConfigurationItem):
    def assert_configuration(self):
        super().assert_configuration()


class ServerDisplayConfigurationTCP(ServerDisplayConfiguration):
    SECTION_IDENTIFIER = "display.tcp"
    EXPECTED_CONFIGURATIONS = ["host", "port"]

    @property
    def host(self):
        return ParseValue.as_string(self.configuration["host"])

    @property
    def port(self):
        return ParseValue.as_integer(self.configuration["port"])


class ServerConfiguration(KmcConfiguration):
    pass


for name, obj in inspect.getmembers(sys.modules[__name__]):
    if inspect.isclass(obj) and issubclass(obj, ServerDisplayConfiguration) and obj is not ServerDisplayConfiguration:
        ServerConfiguration.register_configuration_item_class(obj)
