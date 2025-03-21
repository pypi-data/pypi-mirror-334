# SPDX-FileCopyrightText: 2025 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-3.0-only

import pynput


class InfiniteMouseMotionManager:
    def __init__(self, center_x, center_y):
        self._mouse_controller = pynput.mouse.Controller()
        self._center_x = center_x
        self._center_y = center_y
        self._original_position = None
        self._active = False

    @property
    def active(self):
        return self._active

    def set_mouse_to_center(self):
        self._mouse_controller.position = (self._center_x, self._center_y)

    def activate(self):
        if self._original_position is not None:
            self.deactivate()
        self._original_position = self._mouse_controller.position
        self.set_mouse_to_center()
        self._active = True

    def deactivate(self):
        if self._original_position is not None:
            self._mouse_controller.position = self._original_position
            self._original_position = None
        self._active = False

    def get_relative_mouse_movement(self):
        if self.active:
            current_x, current_y = self._mouse_controller.position
            if (current_x, current_y) == (self._center_x, self._center_y):
                return
            dx = current_x - self._center_x
            dy = current_y - self._center_y
            self.set_mouse_to_center()
            return (dx, dy)
