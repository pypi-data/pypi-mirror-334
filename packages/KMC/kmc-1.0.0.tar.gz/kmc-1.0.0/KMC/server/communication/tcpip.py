# SPDX-FileCopyrightText: 2025 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-3.0-only
from KMC.os_api.input_processing import InputProcessorAsync
from KMC.communication.tcpip import KmcReceiverTcpIpAsync
from KMC.server.communication.base import KmcReceiverContainer


class ServerKmcReceiverContainerTcpIpAsync(KmcReceiverContainer):
    def __init__(self, configuration):
        input_processor = InputProcessorAsync()
        receiver = KmcReceiverTcpIpAsync(input_processor, configuration.port, configuration.host)
        super().__init__(configuration, receiver)


if __name__ == "__main__":
    import asyncio
    from KMC.os_api.input_items import InputItemMouseMove
    from KMC.communication.base import KmcMessage
    from KMC.communication.tcpip import KmcTransmitterTcpIpAsync

    class DummyConfiguration:
        def __init__(self):
            self.host = "localhost"
            self.port = 12345
            self.name = "test"

    transmitter = KmcTransmitterTcpIpAsync(12345)
    receiver_container = ServerKmcReceiverContainerTcpIpAsync(DummyConfiguration())

    async def run():
        await receiver_container.receiver.start()
        await asyncio.sleep(0.1)
        await transmitter.start()
        kmc_message = KmcMessage("abc", InputItemMouseMove(100, 100, None, None, True))
        await transmitter.send_message(kmc_message)
        await asyncio.sleep(0.1)

        await receiver_container.receiver.stop()
        await transmitter.stop()

    asyncio.run(run())
