# SPDX-FileCopyrightText: 2025 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-3.0-only
import asyncio
import json

from KMC.communication.asynctcpcs.server import Server
from KMC.communication.asynctcpcs.client import Client
from KMC.communication.base import KmcMessage
from KMC.communication.base import KmcReceiverAsync
from KMC.communication.base import KmcTransmitterAsync


class KmcClient(Client):
    def __init__(self, port, host):
        super().__init__(host, port)


class KmcTransmitterTcpIpAsync(KmcTransmitterAsync):
    def __init__(self, port, host="localhost"):
        self._client = KmcClient(port, host)

    async def start(self):
        await self._client.connect()

    async def stop(self):
        await self._client.close()

    async def send_message(self, kmc_message):
        assert self._client is not None
        kmc_message_serialized = kmc_message.serialize()
        kmc_message_serialized_bytes = json.dumps(kmc_message_serialized).encode("utf-8")
        await self._client.send(kmc_message_serialized_bytes)


class KmcServer(Server):
    def __init__(self, port, host):
        super().__init__(port, host)
        self._on_kmc_message_callbacks = []

    def register_on_message_callback(self, callback):
        self._on_kmc_message_callbacks.append(callback)

    def unregister_on_message_callback(self, callback):
        self._on_kmc_message_callbacks.remove(callback)

    async def on_data(self, client_connection, data_bytes):
        try:
            for kmc_message_callback in self._on_kmc_message_callbacks:
                await kmc_message_callback(data_bytes)
        except Exception:
            raise


class KmcReceiverTcpIpAsync(KmcReceiverAsync):
    def __init__(self, input_processor, port, host="localhost"):
        super().__init__(input_processor)
        self._server = KmcServer(port, host)
        self._server.register_on_message_callback(self.on_message_serialized_bytes)
        self._server_task = None

    async def start(self):
        self._server_task = asyncio.create_task(self._server.start())

    async def stop(self):
        assert self._server_task is not None
        await self._server.close()
        await self._server_task

    async def on_message_serialized_bytes(self, kmc_message_serialized_bytes):
        kmc_message_serialized = json.loads(kmc_message_serialized_bytes.decode("utf-8"))
        kmc_message = KmcMessage.deserialize(kmc_message_serialized)
        await self.on_message(kmc_message)


if __name__ == "__main__":
    from KMC.os_api.input_processing import InputProcessorAsync
    from KMC.os_api.input_items import InputItemMouseMove
    transmitter = KmcTransmitterTcpIpAsync(12345)
    receiver = KmcReceiverTcpIpAsync(InputProcessorAsync(), 12345)

    async def run():
        await receiver.start()
        await asyncio.sleep(1)
        await transmitter.start()
        kmc_message = KmcMessage("abc", InputItemMouseMove(100, 100, None, None, True))
        await transmitter.send_message(kmc_message)
        await asyncio.sleep(1)

        await receiver.stop()
        await transmitter.stop()

    asyncio.run(run())
