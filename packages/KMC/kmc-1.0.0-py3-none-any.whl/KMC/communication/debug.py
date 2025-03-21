# SPDX-FileCopyrightText: 2025 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-3.0-only

from KMC.communication.base import KmcTransmitterAsync
from KMC.communication.base import KmcReceiverAsync
from KMC.os_api.input_processing import InputProcessorAsync


class KmcConnectionDebugAsync:
    def __init__(self):
        self._kmc_transmitter = None
        self._kmc_receiver = None

    async def connect(self, kmc_transmitter, kmc_receiver):
        assert isinstance(kmc_transmitter, KmcTransmitterDebugAsync)
        assert isinstance(kmc_receiver, KmcReceiverDebugAsync)
        self._kmc_transmitter = kmc_transmitter
        self._kmc_receiver = kmc_receiver

    async def transfer_message(self, kmc_message):
        assert self._kmc_transmitter is not None
        assert self._kmc_receiver is not None
        await self._kmc_receiver.on_message(kmc_message)


class KmcTransmitterDebugAsync(KmcTransmitterAsync):
    def __init__(self):
        self._connection = None

    async def start(self):
        kmc_receiver = KmcReceiverDebugAsync(InputProcessorAsync())
        self._connection = KmcConnectionDebugAsync()
        await self._connection.connect(self, kmc_receiver)

    async def send_message(self, kmc_message):
        assert self._connection is not None
        await self._connection.transfer_message(kmc_message)


class KmcReceiverDebugAsync(KmcReceiverAsync):
    def __init__(self, input_processor):
        super().__init__(input_processor)
