# SPDX-FileCopyrightText: 2025 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-3.0-only
import argparse
import asyncio

from KMC.client.configuration import ClientConfiguration
from KMC.client.input_grabbing import ClientInputGrabberAsync
from KMC.client.communication.transmitter_management import KmcTransmitterManagerAsync


async def async_run(config):
    async_loop = asyncio.get_running_loop()

    client_configuration = ClientConfiguration(config)
    kmc_transmitter_manager = KmcTransmitterManagerAsync()

    for configuration in client_configuration.configurations:
        kmc_transmitter_manager.create_kmc_transmitter_container(configuration)

    client_input_grabber = ClientInputGrabberAsync(kmc_transmitter_manager, async_loop)
    await client_input_grabber.start()
    await client_input_grabber.join()

def run():
    parser = argparse.ArgumentParser(description="KMC client application.")

    parser.add_argument(
        "-c",
        "--config",
        type=str,
        required=True,
        help="client configuration file.",
    )

    args = parser.parse_args()

    asyncio.run(async_run(config=args.config))


if __name__ == "__main__":
    run()
