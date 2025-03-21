# SPDX-FileCopyrightText: 2025 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-3.0-only
import asyncio

from KMC.os_api.input_grabbing import InputGrabberAsync


class ClientInputGrabberAsync(InputGrabberAsync):
    def __init__(self, kmc_transmitter_manager, async_loop):
        super().__init__(async_loop)
        self.kmc_transmitter_manager = kmc_transmitter_manager

        self._set_active_kmc_transmitter_container(None)

        self.setup_global_hotkey_listener()

    def setup_global_hotkey_listener(self):
        global_hotkey_listener_setup = {
            kmc_transmitter_container.configuration.keymap : lambda: self._set_active_kmc_transmitter_container(kmc_transmitter_container)
            for kmc_transmitter_container
            in self.kmc_transmitter_manager.kmc_transmitter_containers
        }
        global_hotkey_listener_setup["<shift>+<ctrl>+<space>"] = lambda: self._set_active_kmc_transmitter_container(None)
        global_hotkey_listener_setup["<shift>+<ctrl>+<esc>"] = lambda: self.stop_sync()

        super().setup_global_hotkey_listener(global_hotkey_listener_setup)

    async def start(self):
        await self.kmc_transmitter_manager.start_transmitters()
        self.activate_global_hotkey_listener()

    def stop_sync(self):
        asyncio.run_coroutine_threadsafe(self.stop(), self._async_loop)

    async def on_input(self, input_item):
        if input_item is None:
            return
        await self.kmc_transmitter_manager.send_input_item(input_item)

    def _set_active_kmc_transmitter_container(self, kmc_transmitter_container):
        asyncio.run_coroutine_threadsafe(self.set_active_kmc_transmitter_container(kmc_transmitter_container), self._async_loop)

    async def set_active_kmc_transmitter_container(self, kmc_transmitter_container):
        if kmc_transmitter_container is None:
            self.deactivate_infinite_mouse_motion()
            self.deactivate_mouse_listener(join=False)
            self.deactivate_keyboard_listener(join=False)
        else:
            self.activate_infinite_mouse_motion()
            self.activate_mouse_listener()
            self.activate_keyboard_listener()

        await self.kmc_transmitter_manager.send_input_cancel()
        await self.kmc_transmitter_manager.set_active_kmc_transmitter_container(kmc_transmitter_container)
