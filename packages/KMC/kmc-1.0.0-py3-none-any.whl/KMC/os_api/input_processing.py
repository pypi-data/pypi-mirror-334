# SPDX-FileCopyrightText: 2025 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-3.0-only
import asyncio
import pynput

from KMC.os_api.input_items import InputItemKeyPress
from KMC.os_api.input_items import InputItemKeyRelease
from KMC.os_api.input_items import InputItemMouseButtonPress
from KMC.os_api.input_items import InputItemMouseButtonRelease
from KMC.os_api.input_items import InputItemMouseMove
from KMC.os_api.input_items import InputItemMouseScroll


class InputProcessorAsync:
    def __init__(self):
        self._mouse_controller = pynput.mouse.Controller()
        self._keyboard_controller = pynput.keyboard.Controller()

        self._cancel_input_items = []

        self.input_item_processor_functions = {
            InputItemMouseMove: self._mouse_move,
            InputItemMouseButtonPress: self._mouse_button_press,
            InputItemMouseButtonRelease: self._mouse_button_release,
            InputItemMouseScroll: self._mouse_scroll,
            InputItemKeyPress: self._key_press,
            InputItemKeyRelease: self._key_release,
        }

    async def process_input_item(self, input_item):
        func = self.input_item_processor_functions.get(input_item.__class__)
        assert func is not None
        await func(input_item)

        if input_item in self._cancel_input_items:
            self._cancel_input_items.remove(input_item)

    async def _mouse_move(self, input_item):
        self._mouse_controller.move(input_item.dx, input_item.dy)

    async def _mouse_button_press(self, input_item):
        button = {
            "left": pynput.mouse.Button.left,
            "middle": pynput.mouse.Button.middle,
            "right": pynput.mouse.Button.right,
        }[input_item.button]
        self._mouse_controller.press(button)

        self._cancel_input_items.append(InputItemMouseButtonPress(input_item.button))

    async def _mouse_button_release(self, input_item):
        button = {
            "left": pynput.mouse.Button.left,
            "middle": pynput.mouse.Button.middle,
            "right": pynput.mouse.Button.right,
        }[input_item.button]
        self._mouse_controller.release(button)

        if input_item in self._cancel_input_items:
            self._cancel_input_items.remove(input_item)

    async def _mouse_scroll(self, input_item):
        self._mouse_controller.scroll(input_item.dx, input_item.dy)

    async def _key_press(self, input_item):
        if input_item.name is not None:
            self._keyboard_controller.press(pynput.keyboard.Key[input_item.name])
        elif input_item.char is not None:
            self._keyboard_controller.press(pynput.keyboard.KeyCode.from_char(input_item.char))
        else:
            self._keyboard_controller.press(pynput.keyboard.KeyCode.from_vk(input_item.vk))

        self._cancel_input_items.append(InputItemKeyRelease(
            name=input_item.name,
            char=input_item.char,
            vk=input_item.vk,
        ))

    async def _key_release(self, input_item):
        if input_item.name is not None:
            self._keyboard_controller.release(pynput.keyboard.Key[input_item.name])
        elif input_item.char is not None:
            self._keyboard_controller.release(pynput.keyboard.KeyCode.from_char(input_item.char))
        else:
            self._keyboard_controller.release(pynput.keyboard.KeyCode.from_vk(input_item.vk))

        if input_item in self._cancel_input_items:
            self._cancel_input_items.remove(input_item)

    async def cancel_inputs(self):
        while len(self._cancel_input_items) > 0:
            input_item = self._cancel_input_items[0]
            await self.process_input_item(input_item)  # input_item gets removed implicitly


if __name__ == "__main__":
    input_processor = InputProcessorAsync()
    asyncio.run(input_processor.process_input_item(InputItemMouseMove(10,10, None, None, True)))
    asyncio.run(input_processor.process_input_item(InputItemMouseScroll(0, 1)))
    asyncio.run(input_processor.process_input_item(InputItemMouseButtonPress("right")))
    asyncio.run(input_processor.process_input_item(InputItemMouseButtonRelease("right")))
    asyncio.run(input_processor.process_input_item(InputItemKeyPress("Key", "esc", None)))
    asyncio.run(input_processor.process_input_item(InputItemKeyRelease("Key", "esc", None)))
