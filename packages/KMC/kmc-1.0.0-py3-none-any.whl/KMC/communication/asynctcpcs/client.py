# SPDX-FileCopyrightText: 2025 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-3.0-only

import asyncio

from KMC.communication.asynctcpcs.transferutils import TransferHandler

class Client(object):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.event_connected = asyncio.Event()
        self.event_idle = asyncio.Event()
        self.event_idle.set()

    def is_connected(self):
        return self.event_connected.is_set()

    async def connect(self, timeout=5):
        self.reader,self.writer = await asyncio.wait_for(asyncio.open_connection(self.host, self.port), timeout=timeout)
        self.event_connected.set()

    async def close(self):
        await self.event_idle.wait()
        try:
            self.event_connected.clear()
            self.writer.close()
            await self.writer.wait_closed()
        except:
            pass

    async def _recv(self):
        return await TransferHandler.recv(self.reader.read)

    async def _recv_loop(self, on_data):
        try:
            while True:
                data_bytes = await self._recv()
                if data_bytes is None:
                    break
                await on_data(data_bytes)
        except:
            raise
        finally:
            await self.close()

    async def start_receive_loop(self, on_data):
        asyncio.create_task(self._recv_loop(on_data))

    async def send(self, data_bytes, timeout=5):
        try:
            self.event_idle.clear()
            await asyncio.wait_for(TransferHandler.send(self.writer.write, data_bytes), timeout=timeout)
            await self.writer.drain()
            self.event_idle.set()
        except:
            self.event_idle.set()
            await self.close()
            raise
