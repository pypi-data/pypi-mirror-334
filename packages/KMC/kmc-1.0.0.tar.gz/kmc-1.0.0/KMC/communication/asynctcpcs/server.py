# SPDX-FileCopyrightText: 2025 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-3.0-only

import asyncio

from KMC.communication.asynctcpcs.transferutils import TransferHandler

class ClientConnection(object):
    def __init__(self, server, reader, writer):
        self.server = server
        self.reader = reader
        self.writer = writer
        self.event_idle = asyncio.Event()
        self.event_idle.set()

    async def close(self):
        await self.event_idle.wait()
        await self.server._remove_client_connection(self)
        try:
            self.writer.close()
            await self.writer.wait_closed()
        except ConnectionResetError:
            pass

    async def recv(self):
        return await TransferHandler.recv(self.reader.read)

    async def _recv_loop(self):
        try:
            while True:
                data_bytes = await self.recv()
                if data_bytes is None:
                    break
                await self.server.on_data(self, data_bytes)
        except:
            raise
        finally:
            await self.close()

    async def send(self, data_bytes):
        try:
            self.event_idle.clear()
            await TransferHandler.send(self.writer.write, data_bytes)
            await self.writer.drain()
            self.event_idle.set()
        except:
            self.event_idle.set()
            await self.close()
            raise

class Server(object):
    BACKLOG = 100

    def __init__(self, port, host="0.0.0.0"):
        super().__init__()
        self.port = port
        self.host = host
        self.client_list = []
        self.client_list_mutex = asyncio.Lock()
        self.event_shutdown = asyncio.Event()

    async def start(self):
        if self.event_shutdown.is_set():
            raise Exception("Cannot restart server")

        self.async_server = await asyncio.start_server(self._handle_new_connection, self.host, self.port, backlog=Server.BACKLOG)

        async with self.async_server:
            try:
                await self.async_server.serve_forever()
            except asyncio.CancelledError:
                pass
            finally:
                self.async_server.close()
                await self.async_server.wait_closed()

    async def close(self):
        self.event_shutdown.set()

        for cc in self.client_list:
            await cc.close()
        self.async_server.close()
        await self.async_server.wait_closed()

    async def on_data(self, client_connection, data_bytes):
        raise NotImplementedError()

    async def send(self, data_bytes, client_connections=None):
        if client_connections is None:
            client_connections = self.client_list
        if isinstance(client_connections, list):
            for cc in client_connections:
                await cc.send(data_bytes)
        elif isinstance(client_connections, ClientConnection):
            cc = client_connections
            await cc.send(data_bytes)

    def get_connected_clients(self):
        return list(self.client_list)

    async def _add_client_connection(self, cc):
        async with self.client_list_mutex:
            self.client_list.append(cc)

    async def _remove_client_connection(self, cc):
        async with self.client_list_mutex:
            if cc in self.client_list:
                self.client_list.remove(cc)

    async def _handle_new_connection(self, reader, writer):
        cc = ClientConnection(self, reader, writer)
        await self._add_client_connection(cc)
        await cc._recv_loop()
