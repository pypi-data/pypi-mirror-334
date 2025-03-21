# SPDX-FileCopyrightText: 2025 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-3.0-only
import inspect
import sys

from KMC.configuration.base import KmcConfiguration
from KMC.configuration.base import KmcConfigurationItem
from KMC.configuration.base import ParseValue


class ClientDisplayConfiguration(KmcConfigurationItem):
    def assert_configuration(self):
        super().assert_configuration()
        assert "keymap" in self.configuration

    @property
    def keymap(self):
        return ParseValue.as_string(self.configuration["keymap"])


class ClientDisplayConfigurationDebug(ClientDisplayConfiguration):
    SECTION_IDENTIFIER = "display.debug"


class ClientDisplayConfigurationTCP(ClientDisplayConfiguration):
    SECTION_IDENTIFIER = "display.tcp"
    EXPECTED_CONFIGURATIONS = ["host", "port"]

    @property
    def host(self):
        return ParseValue.as_string(self.configuration["host"])

    @property
    def port(self):
        return ParseValue.as_integer(self.configuration["port"])


class ClientConfiguration(KmcConfiguration):
    def parse_configurations(self, config):
        super().parse_configurations(config)
        
        keymap_configs = [config for config in self.configurations if hasattr(config, "keymap")]
        keymaps = [config.keymap for config in keymap_configs]
        assert (len(set(keymaps)) == len(keymap_configs))


for name, obj in inspect.getmembers(sys.modules[__name__]):
    if inspect.isclass(obj) and issubclass(obj, ClientDisplayConfiguration) and obj is not ClientDisplayConfiguration:
        ClientConfiguration.register_configuration_item_class(obj)
