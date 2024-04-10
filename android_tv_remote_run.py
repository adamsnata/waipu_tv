import argparse
import asyncio
import json
import logging
import sys

from androidtvremote2 import AndroidTVRemote, ConnectionClosed, InvalidAuth, CannotConnect

_LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def _pair(remote: AndroidTVRemote) -> None:
    name, mac = await remote.async_get_name_and_mac()
    if (
            input(
                f"Do you want to pair with {remote.host} {name} {mac}"
                " (this will turn on the Android TV)? y/n: "
            )
            != "y"
    ):
        exit()
    await remote.async_start_pairing()
    while True:
        pairing_code = input("Enter pairing code: ")
        try:
            return await remote.async_finish_pairing(pairing_code)
        except InvalidAuth as exc:
            _LOGGER.error("Invalid pairing code. Error: %s", exc)
            continue
        except ConnectionClosed as exc:
            _LOGGER.error("Initialize pair again. Error: %s", exc)
            return await _pair(remote)


async def connect(remote):
    if await remote.async_generate_cert_if_missing():
        print("Generated new certificate")
        await _pair(remote)

    while True:
        try:
            await remote.async_connect()
            break
        except InvalidAuth as exc:
            _LOGGER.error("Need to pair again. Error: %s", exc)
            await _pair(remote)
        except (CannotConnect, ConnectionClosed) as exc:
            _LOGGER.error("Cannot connect, exiting. Error: %s", exc)
            return

    remote.keep_reconnecting()

    _LOGGER.info("device_info: %s", remote.device_info)
    _LOGGER.info("is_on: %s", remote.is_on)
    _LOGGER.info("current_app: %s", remote.current_app)
    _LOGGER.info("volume_info: %s", remote.volume_info)

    def is_on_updated(is_on: bool) -> None:
        _LOGGER.info("Notified that is_on: %s", is_on)

    def current_app_updated(current_app: str) -> None:
        _LOGGER.info("Notified that current_app: %s", current_app)

    def volume_info_updated(volume_info: dict[str, str | bool]) -> None:
        _LOGGER.info("Notified that volume_info: %s", volume_info)

    def is_available_updated(is_available: bool) -> None:
        _LOGGER.info("Notified that is_available: %s", is_available)

    remote.add_is_on_updated_callback(is_on_updated)
    remote.add_current_app_updated_callback(current_app_updated)
    remote.add_volume_info_updated_callback(volume_info_updated)
    remote.add_is_available_updated_callback(is_available_updated)


async def execute_commands(commands, remote):
    for command in commands:
        if command['action'] == 'SendKey':
            _LOGGER.info(command['keyname'])
            try:
                remote.send_key_command(command['keyname'])
            except ConnectionClosed as e:
                _LOGGER.error("Connection error:", e)
        elif command['action'] == 'Pause':
            await asyncio.sleep(command['time'] / 1000)
        elif command['action'] == 'Repeat':
            _LOGGER.info('\n Repeat')
            for _ in range(command['count']):
                await execute_commands(command['commands'], remote)


async def _main(ip, cert, commands):
    remote = AndroidTVRemote(client_name="Waipu TV",
                             certfile=cert,
                             keyfile="filename that contains the public key in PEM format key.pem",
                             host=ip)
    await connect(remote)

    await execute_commands(commands, remote)

    remote.disconnect()


def load_commands(filename):
    with open(filename, 'r') as file:
        return json.load(file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process command line arguments.')

    parser.add_argument('-c', '--config', help='Path to the configuration file.')
    parser.add_argument('--commands_file', help='Path to the commands file.')
    parser.add_argument('--ip', help='IP address to connect to.')
    parser.add_argument('--cert', help='Path to the certificate file.')

    args = parser.parse_args()

    if args.config:
        with open(args.config, 'r') as file:
            config = json.load(file)
        commands_file = config.get('commands_file')
        ip = config.get('ip')
        cert = config.get('cert')
    else:
        commands_file = args.commands_file
        ip = args.ip
        cert = args.cert

    if not commands_file or not ip or not cert:
        sys.exit("Error message")

    commands = load_commands(commands_file)
    asyncio.run(_main(ip, cert, commands))
