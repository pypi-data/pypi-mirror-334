# SPDX-FileCopyrightText: 2025 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-3.0-only
from KMC.communication.tcpip import KmcTransmitterTcpIpAsync
from KMC.client.communication.base import KmcTransmitterContainer


class ClientKmcTransmitterContainerTcpIpAsync(KmcTransmitterContainer):
    def __init__(self, configuration):
        transmitter = KmcTransmitterTcpIpAsync(configuration.port, configuration.host)
        super().__init__(configuration, transmitter)
