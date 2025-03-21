# SPDX-FileCopyrightText: 2025 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-3.0-only
from KMC.os_api.input_items import InputItem
from KMC.communication.control_items import ControlItem
from KMC.communication.control_items import InputCancelItem


class KmcMessage:
    def __init__(self, display, input_item=None, control_item=None):
        self.display = display
        self.input_item = input_item
        self.control_item = control_item

    def serialize(self):
        out = {"display": self.display}

        if self.input_item is not None:
            out["input_item"] = self.input_item.serialize()

        if self.control_item is not None:
            out["control_item"] = self.control_item.serialize()

        return out

    @classmethod
    def deserialize(cls, serialized_kmc_message):
        display = serialized_kmc_message["display"]
        input_item = None
        control_item = None

        if "input_item" in serialized_kmc_message:
            input_item = InputItem.deserialize(serialized_kmc_message["input_item"])

        if "control_item" in serialized_kmc_message:
            control_item = ControlItem.deserialize(serialized_kmc_message["control_item"])

        return cls(display, input_item=input_item, control_item=control_item)


class KmcTransmitterAsync:
    async def start(self):
        pass

    async def stop(self):
        pass

    async def send_message(self, kmc_message):
        raise NotImplementedError


class KmcReceiverAsync:
    def __init__(self, input_processor):
        self._input_processor = input_processor

    async def start(self):
        pass

    async def stop(self):
        pass

    async def on_message(self, kmc_message):
        display = kmc_message.display
        if kmc_message.input_item is not None:
            await self._input_processor.process_input_item(kmc_message.input_item)

        if kmc_message.control_item is not None:
            control_item = kmc_message.control_item
            if isinstance(control_item, InputCancelItem):
                await self._input_processor.cancel_inputs()
