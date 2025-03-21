# SPDX-FileCopyrightText: 2025 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-3.0-only

from KMC.server.configuration import ServerDisplayConfigurationTCP
from KMC.server.communication.tcpip import ServerKmcReceiverContainerTcpIpAsync


class KmcReceiverManagerAsync:
    def __init__(self):
        self.kmc_receiver_containers = list()
        self._active_kmc_receiver_container = None

    def create_kmc_receiver_container(self, configuration):
        kmc_receiver_container_cls = {
            ServerDisplayConfigurationTCP: ServerKmcReceiverContainerTcpIpAsync
        }.get(configuration.__class__)

        if kmc_receiver_container_cls is None:
            return

        self.kmc_receiver_containers.append(kmc_receiver_container_cls(configuration))

    async def start_receivers(self):
        for kmc_receiver_container in self.kmc_receiver_containers:
            await kmc_receiver_container.receiver.start()

    async def stop_receivers(self):
        for kmc_receiver_container in self.kmc_receiver_containers:
            await kmc_receiver_container.receiver.stop()
