# SPDX-FileCopyrightText: 2025 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-3.0-only
from KMC.client.communication.base import KmcTransmitterContainer
from KMC.communication.debug import KmcTransmitterDebugAsync


class ClientKmcTransmitterContainerDebugAsync(KmcTransmitterContainer):
    def __init__(self, configuration):
        transmitter = KmcTransmitterDebugAsync()
        super().__init__(configuration, transmitter)
