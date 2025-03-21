# SPDX-FileCopyrightText: 2025 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-3.0-only
import argparse
import asyncio

from KMC.server.configuration import ServerConfiguration
from KMC.server.communication.receiver_management import KmcReceiverManagerAsync


async def async_run(config):
    server_configuration = ServerConfiguration(config)
    kmc_receiver_manager = KmcReceiverManagerAsync()

    for configuration in server_configuration.configurations:
        kmc_receiver_manager.create_kmc_receiver_container(configuration)

    await kmc_receiver_manager.start_receivers()

    while True:
        await asyncio.sleep(1)

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
