# SPDX-FileCopyrightText: 2025 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-3.0-only

from KMC.client.configuration import ClientDisplayConfigurationDebug
from KMC.client.configuration import ClientDisplayConfigurationTCP
from KMC.client.communication.debug import ClientKmcTransmitterContainerDebugAsync
from KMC.client.communication.tcpip import ClientKmcTransmitterContainerTcpIpAsync
from KMC.communication.base import KmcMessage
from KMC.communication.control_items import InputCancelItem


class KmcTransmitterManagerAsync:
    def __init__(self):
        self.kmc_transmitter_containers = list()
        self._active_kmc_transmitter_container = None

    def create_kmc_transmitter_container(self, configuration):
        kmc_transmitter_container_cls = {
            ClientDisplayConfigurationDebug: ClientKmcTransmitterContainerDebugAsync,
            ClientDisplayConfigurationTCP: ClientKmcTransmitterContainerTcpIpAsync,
        }.get(configuration.__class__)

        if kmc_transmitter_container_cls is None:
            return

        self.kmc_transmitter_containers.append(kmc_transmitter_container_cls(configuration))

    async def set_active_kmc_transmitter_container(self, kmc_transmitter_container):
        if ((kmc_transmitter_container in self.kmc_transmitter_containers) or
            (kmc_transmitter_container is None)):
            self._active_kmc_transmitter_container = kmc_transmitter_container

    async def send_input_cancel(self):
        kmc_transmitter_container = self._active_kmc_transmitter_container
        if kmc_transmitter_container is not None:
            kmc_message = KmcMessage(kmc_transmitter_container.configuration.name, control_item=InputCancelItem())
            await kmc_transmitter_container.transmitter.send_message(kmc_message)

    async def send_input_item(self, input_item):
        kmc_transmitter_container = self._active_kmc_transmitter_container
        if kmc_transmitter_container is not None:
            kmc_message = KmcMessage(kmc_transmitter_container.configuration.name, input_item=input_item)
            await kmc_transmitter_container.transmitter.send_message(kmc_message)

    async def start_transmitters(self):
        for kmc_transmitter_container in self.kmc_transmitter_containers:
            await kmc_transmitter_container.transmitter.start()

    async def stop_transmitters(self):
        for kmc_transmitter_container in self.kmc_transmitter_containers:
            await kmc_transmitter_container.transmitter.stop()
