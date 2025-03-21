# SPDX-FileCopyrightText: 2025 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-3.0-only

class TransferHandler(object):
    packetSizeHeaderBytes = 4
    packetByteOrder = "big"

    @staticmethod
    async def send(write_cb, data_bytes):
        size = TransferHandler.packetSizeHeaderBytes
        order = TransferHandler.packetByteOrder
        packetSize = len(data_bytes).to_bytes(size, order)
        packet = packetSize + data_bytes
        write_cb(packet)

    @staticmethod
    async def recv(recv_cb):
        headerBytes = await recv_cb(TransferHandler.packetSizeHeaderBytes)
        if len(headerBytes) == 0:
            return None
        numDataBytes = int.from_bytes(headerBytes, TransferHandler.packetByteOrder)

        data_bytes = bytes()
        numReceivedBytes = 0
        while numDataBytes > numReceivedBytes:
            recvBufferSize      = numDataBytes-numReceivedBytes
            recvBytes           = await recv_cb(recvBufferSize)
            data_bytes           += recvBytes
            numReceivedBytes    += len(recvBytes)
            if len(recvBytes) == 0:
                return None
        return data_bytes
