# SPDX-FileCopyrightText: 2025 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-3.0-only

import inspect
import sys


class ControlItem:
    REGISTERED_CONTROL_ITEM_CLASSES = dict()

    def __eq__(self, other):
        return self.__class__ == other.__class__

    @classmethod
    def serialize(cls, serialized_control_item):
        assert "type" not in serialized_control_item
        key = cls.__name__
        assert key in cls.REGISTERED_CONTROL_ITEM_CLASSES
        serialized_control_item["type"] = key
        return serialized_control_item

    @classmethod
    def deserialize(cls, serialized_control_item):
        key = serialized_control_item["type"]
        return cls.REGISTERED_CONTROL_ITEM_CLASSES[key].deserialize(serialized_control_item)

    @classmethod
    def register_control_item_class(cls, control_item_cls):
        key = control_item_cls.__name__
        assert key not in cls.REGISTERED_CONTROL_ITEM_CLASSES
        cls.REGISTERED_CONTROL_ITEM_CLASSES[key] = control_item_cls


class EmptyControlItem(ControlItem):
    def serialize(self):
        return super().serialize({})

    @classmethod
    def deserialize(cls, serialized_input_item):
        return cls()


class InputCancelItem(EmptyControlItem):
    pass


for name, obj in inspect.getmembers(sys.modules[__name__]):
    if inspect.isclass(obj) and issubclass(obj, ControlItem) and obj is not ControlItem:
        ControlItem.register_control_item_class(obj)
