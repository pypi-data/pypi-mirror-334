# SPDX-FileCopyrightText: 2025 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-3.0-only
import inspect
import sys


class InputItem:
    REGISTERED_INPUT_ITEM_CLASSES = dict()

    def __eq__(self, other):
        return self.__class__ == other.__class__

    @classmethod
    def serialize(cls, serialized_input_item):
        assert "type" not in serialized_input_item
        key = cls.__name__
        assert key in cls.REGISTERED_INPUT_ITEM_CLASSES
        serialized_input_item["type"] = key
        return serialized_input_item

    @classmethod
    def deserialize(cls, serialized_input_item):
        key = serialized_input_item["type"]
        return cls.REGISTERED_INPUT_ITEM_CLASSES[key].deserialize(serialized_input_item)

    @classmethod
    def register_input_item_class(cls, input_item_cls):
        key = input_item_cls.__name__
        assert key not in cls.REGISTERED_INPUT_ITEM_CLASSES
        cls.REGISTERED_INPUT_ITEM_CLASSES[key] = input_item_cls


class InputItemMouseMove(InputItem):
    def __init__(self, dx, dy, x, y, infinite_mode):
        self.dx = dx
        self.dy = dy
        self.x = x
        self.y = y
        self.infinite_mode = infinite_mode

    def __eq__(self, other):
        return (
            super().__eq__(other) and
            self.dx == other.dx and
            self.dy == other.dy and
            self.x == other.x and
            self.y == other.y and
            self.infinite_mode == other.infinite_mode
        )

    def serialize(self):
        return super().serialize({
            "dx": self.dx,
            "dy": self.dy,
            "x": self.x,
            "y": self.y,
            "infinite_mode": self.infinite_mode,
        })

    @classmethod
    def deserialize(cls, serialized_input_item):
        dx = serialized_input_item["dx"]
        dy = serialized_input_item["dy"]
        x = serialized_input_item["x"]
        y = serialized_input_item["y"]
        infinite_mode = serialized_input_item["infinite_mode"]
        return cls(dx, dy, x, y, infinite_mode=infinite_mode)


class InputItemMouseButton(InputItem):
    def __init__(self, button):
        self.button = button

    def __eq__(self, other):
        return (
            super().__eq__(other) and
            self.button == other.button
        )

    def serialize(self):
        return super().serialize({
            "button": self.button,
        })

    @classmethod
    def deserialize(cls, serialized_input_item):
        button = serialized_input_item["button"]
        return cls(button)


class InputItemMouseButtonPress(InputItemMouseButton):
    pass


class InputItemMouseButtonRelease(InputItemMouseButton):
    pass


class InputItemMouseScroll(InputItem):
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def __eq__(self, other):
        return (
            super().__eq__(other) and
            self.dx == other.dx and
            self.dy == other.dy
        )

    def serialize(self):
        return super().serialize({
            "dx": self.dx,
            "dy": self.dy,
        })

    @classmethod
    def deserialize(cls, serialized_input_item):
        dx = serialized_input_item["dx"]
        dy = serialized_input_item["dy"]
        return cls(dx, dy)


class InputItemKey(InputItem):
    def __init__(self, name=None, char=None, vk=None):
        assert any(v is not None for v in (name, char, vk))
        self.name = name
        self.char = char
        self.vk = vk

    def __eq__(self, other):
        return (
            super().__eq__(other) and
            self.name == other.name and
            self.char == other.char and
            self.vk == other.vk
        )

    def serialize(self):
        return super().serialize({
            "name": self.name,
            "char": self.char,
            "vk": self.vk,
        })

    @classmethod
    def deserialize(cls, serialized_input_item):
        name = serialized_input_item["name"]
        char = serialized_input_item["char"]
        vk = serialized_input_item["vk"]
        return cls(name=name, char=char, vk=vk)


class InputItemKeyPress(InputItemKey):
    pass


class InputItemKeyRelease(InputItemKey):
    pass


for name, obj in inspect.getmembers(sys.modules[__name__]):
    if inspect.isclass(obj) and issubclass(obj, InputItem) and obj is not InputItem:
        InputItem.register_input_item_class(obj)
