# SPDX-FileCopyrightText: 2025 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-3.0-only
import ast
import configparser


class ParseValue:
    @staticmethod
    def as_string(value):
        value = value.strip()
        return value

    @staticmethod
    def as_integer(value):
        value = value.strip()
        return int(value)

    @staticmethod
    def as_boolean(value):
        value = value.strip().lower()
        assert value in ["true", "false", "yes", "no", "1", "0"]
        return value in ["true", "yes", "1"]

    @staticmethod
    def as_python_list(value):
        value = value.strip()
        return ast.literal_eval(value)


class KmcConfigurationItem:
    SECTION_IDENTIFIER = None
    EXPECTED_CONFIGURATIONS = []

    def __init__(self, name, configuration):
        self._name = name
        self.configuration = configuration
        self.assert_configuration()

    def assert_configuration(self):
        for key in self.EXPECTED_CONFIGURATIONS:
            assert key in self.configuration

    @property
    def name(self):
        return self._name


class KmcConfiguration:
    REGISTERED_CONFIGURATION_ITEM_CLASSES = list()

    def __init__(self, config_filename):
        self._config = configparser.ConfigParser()
        self._config.read(config_filename)

        self.configurations = list()

        self.parse_configurations(self._config)

    def parse_configurations(self, config):
        for config_key, configuration in config.items():
            for configuration_cls in self.REGISTERED_CONFIGURATION_ITEM_CLASSES:
                if config_key.startswith(configuration_cls.SECTION_IDENTIFIER):
                    configuration_name = config_key[len(configuration_cls.SECTION_IDENTIFIER):].lstrip(".")
                    self.configurations.append(configuration_cls(configuration_name, configuration))

    @classmethod
    def register_configuration_item_class(cls, configuration_item_cls):
        cls.REGISTERED_CONFIGURATION_ITEM_CLASSES.append(configuration_item_cls)
