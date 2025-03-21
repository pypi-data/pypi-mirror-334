# SPDX-FileCopyrightText: 2025 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-3.0-only

import asyncio
import threading
import time

import pynput

from KMC.os_api.infinite_mouse_manager import InfiniteMouseMotionManager
from KMC.os_api.input_items import InputItemKeyPress
from KMC.os_api.input_items import InputItemKeyRelease
from KMC.os_api.input_items import InputItemMouseButtonPress
from KMC.os_api.input_items import InputItemMouseButtonRelease
from KMC.os_api.input_items import InputItemMouseMove
from KMC.os_api.input_items import InputItemMouseScroll


class MouseListener:
    class MovePollListener(threading.Thread):
        FAST_POLL_INTERVAL = 1/100  # 100 times per second
        SLOW_POLL_INTERVAL = 1/10  # 10 times per second
        SLOW_POLL_SWITCH_TIME = 10  # 10 seconds

        def __init__(self, on_move):
            super().__init__()
            self._on_move = on_move
            self._stop_event = threading.Event()
            self._mouse_position_reader = pynput.mouse.Controller()
            self._poll_interval = MouseListener.MovePollListener.FAST_POLL_INTERVAL

        def set_high_poll_rate(self):
            self._poll_interval = MouseListener.MovePollListener.FAST_POLL_INTERVAL

        def run(self):
            old_x, old_y = None, None
            slow_poll_switch_time = (time.time() + MouseListener.MovePollListener.SLOW_POLL_SWITCH_TIME)
            t_next = time.time()
            while not self._stop_event.is_set():
                t_next += self._poll_interval
                time.sleep(max((t_next - time.time()), 0))
                x, y = self._mouse_position_reader.position
                if old_x != x or old_y != y:
                    old_x, old_y = x, y
                    self._on_move(x, y)
                    slow_poll_switch_time = (time.time() + MouseListener.MovePollListener.SLOW_POLL_SWITCH_TIME)
                    self.set_high_poll_rate()
                elif time.time() > slow_poll_switch_time:
                    self._poll_interval = MouseListener.MovePollListener.SLOW_POLL_INTERVAL

        def stop(self):
            self._stop_event.set()

    def __init__(self, on_move, on_click, on_scroll, suppress):
        self._mouse_move_listener = MouseListener.MovePollListener(on_move=on_move)
        self._mouse_action_listener = pynput.mouse.Listener(on_click=on_click, on_scroll=on_scroll, suppress=suppress)

    def start(self):
        self._mouse_move_listener.start()
        self._mouse_action_listener.start()

    def stop(self):
        self._mouse_move_listener.stop()
        self._mouse_action_listener.stop()

    def join(self):
        self._mouse_move_listener.join()
        self._mouse_action_listener.join()


class InputGrabberBase:
    def __init__(self):
        self._stop_event = threading.Event()

        self._global_hotkey_listener = None
        self._mouse_listener = None
        self._keyboard_listener = None
        self._global_hotkey_listener_setup = ([], {})

        self._infinite_mouse_motion_manager = InfiniteMouseMotionManager(200, 200)
        self._last_mouse_position = pynput.mouse.Controller().position

    def setup_global_hotkey_listener(self, *args, **kwargs):
        self._global_hotkey_listener_setup = (args, kwargs)

    def activate_global_hotkey_listener(self):
        self.deactivate_global_hotkey_listener()
        args, kwargs = self._global_hotkey_listener_setup
        self._global_hotkey_listener = pynput.keyboard.GlobalHotKeys(*args, **kwargs)
        self._global_hotkey_listener.start()

    def activate_mouse_listener(self):
        self.deactivate_mouse_listener()
        self._mouse_listener = MouseListener(
            on_move=self._on_mouse_move_callback,
            on_click=self._on_mouse_click_callback,
            on_scroll=self._on_mouse_scroll_callback,
            suppress=True,
        )
        self._mouse_listener.start()

    def activate_keyboard_listener(self):
        self.deactivate_keyboard_listener()
        self._keyboard_listener = pynput.keyboard.Listener(
            on_press=self._on_key_press_callback,
            on_release=self._on_key_release_callback,
            suppress=True,
        )
        self._keyboard_listener.start()

    def activate_infinite_mouse_motion(self):
        self._infinite_mouse_motion_manager.activate()

    def deactivate_global_hotkey_listener(self, join=True):
        if self._global_hotkey_listener is not None:
            self._global_hotkey_listener.stop()
            if join:
                self._join_global_hotkey_listener()

    def deactivate_mouse_listener(self, join=True):
        if self._mouse_listener is not None:
            self._mouse_listener.stop()
            if join:
                self._join_mouse_listener()

    def deactivate_keyboard_listener(self, join=True):
        if self._keyboard_listener is not None:
            self._keyboard_listener.stop()
            if join:
                self._join_keyboard_listener()

    def deactivate_infinite_mouse_motion(self):
        self._infinite_mouse_motion_manager.deactivate()

    def _start(self):
        pass

    def _stop(self):
        self._stop_event.set()
        self.deactivate_global_hotkey_listener(join=False)
        self.deactivate_mouse_listener(join=False)
        self.deactivate_keyboard_listener(join=False)

    def _join_global_hotkey_listener(self):
        if self._global_hotkey_listener is not None:
            self._global_hotkey_listener.join()
            self._global_hotkey_listener = None

    def _join_mouse_listener(self):
        if self._mouse_listener is not None:
            # The mouse listener does not join until the mouse moves a little bit.
            # We create a little movement to enable the mouse listener to join directly.
            def _mouse_move():
                time.sleep(0.1)
                mouse_controller = pynput.mouse.Controller()
                x, y = mouse_controller.position
                mouse_controller.position = x+1, y
                mouse_controller.position = x, y
            workaround_thread = threading.Thread(target=_mouse_move)
            workaround_thread.start()
            workaround_thread.join()
            self._mouse_listener.join()
            self._mouse_listener = None

    def _join_keyboard_listener(self):
        if self._keyboard_listener is not None:
            self._keyboard_listener.join()
            self._keyboard_listener = None

    def _join(self, join_listeners=True):
        self._stop_event.wait()
        if join_listeners:
            self._join_global_hotkey_listener()
            self._join_mouse_listener()
            self._join_keyboard_listener()

    def _on_mouse_move_callback(self, x, y):
        raise NotImplementedError

    def _on_mouse_click_callback(self, x, y, button, pressed):
        raise NotImplementedError

    def _on_mouse_scroll_callback(self, x, y, dx, dy):
        raise NotImplementedError

    def _on_key_press_callback(self, key):
        raise NotImplementedError

    def _on_key_release_callback(self, key):
        raise NotImplementedError

    def _on_mouse_move(self, x, y):
        if self._infinite_mouse_motion_manager.active:
            dxdy = self._infinite_mouse_motion_manager.get_relative_mouse_movement()
            if dxdy is None:
                return
            dx, dy = dxdy
            return InputItemMouseMove(dx, dy, None, None, infinite_mode=True)
        else:
            old_x, old_y = self._last_mouse_position
            dx, dy = (x - old_x, y - old_y)
            return InputItemMouseMove(dx, dy, x, y, infinite_mode=False)

    def _on_mouse_click(self, x, y, button, pressed):
        if pressed:
            return InputItemMouseButtonPress(button.name)
        else:
            return InputItemMouseButtonRelease(button.name)

    def _on_mouse_scroll(self, x, y, dx, dy):
        return InputItemMouseScroll(dx, dy)

    def _on_key_press(self, key):
        if isinstance(key, pynput.keyboard.Key):
            return InputItemKeyPress(name=key.name)
        else:
            if key.char is not None:
                return InputItemKeyPress(char=key.char)
            else:
                return InputItemKeyPress(vk=key.vk)

    def _on_key_release(self, key):
        if isinstance(key, pynput.keyboard.Key):
            return InputItemKeyRelease(name=key.name)
        else:
            if key.char is not None:
                return InputItemKeyRelease(char=key.char)
            else:
                return InputItemKeyRelease(vk=key.vk)


class InputGrabber(InputGrabberBase):
    def __init__(self):
        super().__init__()

    def _on_mouse_move_callback(self, x, y):
        input_item = self._on_mouse_move(x, y)
        self.on_input(input_item)

    def _on_mouse_click_callback(self, x, y, button, pressed):
        input_item = self._on_mouse_click(x, y, button, pressed)
        self.on_input(input_item)

    def _on_mouse_scroll_callback(self, x, y, dx, dy):
        input_item = self._on_mouse_scroll(x, y, dx, dy)
        self.on_input(input_item)

    def _on_key_press_callback(self, key):
        input_item = self._on_key_press(key)
        self.on_input(input_item)

    def _on_key_release_callback(self, key):
        input_item = self._on_key_release(key)
        self.on_input(input_item)

    def start(self):
        self._start()
    def stop(self):
        self._stop()
    def join(self, join_listeners=True):
        self._join(join_listeners=join_listeners)

    def on_input(self, input_item):
        raise NotImplementedError


class InputGrabberAsync(InputGrabberBase):
    def __init__(self, async_loop):
        super().__init__()
        self._async_loop = async_loop

    def _on_mouse_move_callback(self, x, y):
        input_item = self._on_mouse_move(x, y)
        asyncio.run_coroutine_threadsafe(self.on_input(input_item), self._async_loop)

    def _on_mouse_click_callback(self, x, y, button, pressed):
        input_item = self._on_mouse_click(x, y, button, pressed)
        asyncio.run_coroutine_threadsafe(self.on_input(input_item), self._async_loop)

    def _on_mouse_scroll_callback(self, x, y, dx, dy):
        input_item = self._on_mouse_scroll(x, y, dx, dy)
        asyncio.run_coroutine_threadsafe(self.on_input(input_item), self._async_loop)

    def _on_key_press_callback(self, key):
        input_item = self._on_key_press(key)
        asyncio.run_coroutine_threadsafe(self.on_input(input_item), self._async_loop)

    def _on_key_release_callback(self, key):
        input_item = self._on_key_release(key)
        asyncio.run_coroutine_threadsafe(self.on_input(input_item), self._async_loop)

    async def start(self):
        self._start()

    async def stop(self):
        self._stop()

    async def join(self, join_listeners=True):
        # With async, the main thread (running the async loop) might wants to join
        # this instance. As the callbacks push the execution into the async loop, the
        # async loop must not block to allow itself to stop ('await self.stop()').
        join_event = threading.Event()
        def _join_func():
            self._join(join_listeners=join_listeners)
            join_event.set()
        join_thread = threading.Thread(target=_join_func)
        join_thread.daemon = True
        join_thread.start()
        while not join_event.is_set():
            await asyncio.sleep(0.1)

    async def on_input(self, input_item):
        raise NotImplementedError


if __name__ == "__main__":
    class TestInputGrabber(InputGrabber):
        def on_input(self, input_item):
            if input_item is None:
                return
            print(input_item.serialize())

    input_grabber = TestInputGrabber()
    input_grabber.start()
    input_grabber.setup_global_hotkey_listener({"x": lambda: input_grabber.stop()})
    input_grabber.activate_global_hotkey_listener()
    input_grabber.activate_mouse_listener()
    input_grabber.activate_keyboard_listener()
    input_grabber.join()
