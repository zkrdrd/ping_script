"""
Модуль, проверки доступности узлов при помощи команды ping.
"""

from argparse import ArgumentParser
from ipaddress import IPv4Address, ip_address, ip_network
from platform import system
from re import search
from subprocess import PIPE, run
from sys import argv
from typing import List, Union

from tabulate import tabulate


class ExceptionProcessing(Exception):
    """Class custom exception processing"""

    def __init__(self, *args):
        super().__init__(*args)


def ping_ip_addresses(ip_addresses: List[str]) -> List[str] | List[str]:
    """Running the ping command.

    Searching for a string using a regular expression

    The function expects a list of IP addresses as an argument.

    Args:

        The parameter is accepted as a list, for example
            [
                '192.168.0.1',
                '192.168.0.2',
                '192.168.0.3',
                '192.168.0.4',
            ]

    Return:

        Two lists are returned, available and unavailable addresses,
        for example

            1. List of available addresses
                [
                    '192.168.0.1',
                    '192.168.0.2',
                ]

            2. The list of unavailable addresses
                [
                    '192.168.0.3',
                    '192.168.0.4',
                ]
    """

    if ip_addresses is None:
        raise ExceptionProcessing("List is empty")

    active_ip_list = []
    passive_ip_list = []

    operation_system = system()

    for ip in ip_addresses:
        print(f"Check: {ip}")
        match operation_system:
            case "Windows":
                reply = run(
                    ["ping", "-n", "1", ip],
                    stdout=PIPE,
                    check=False,
                )

            case "Linux":
                reply = run(
                    [f"ping -c 1 {ip}"],
                    stdout=PIPE,
                    shell=True,
                    check=False,
                )

            case _:
                raise ExceptionProcessing("Undefined system")

        if search(r"\s(TTL|ttl)", str(reply)):
            active_ip_list.append(ip)
        else:
            passive_ip_list.append(ip)

    return active_ip_list, passive_ip_list


def convert_ranges_to_ip_list(ip: Union[str, list]) -> List[str]:
    """Converts a list of IP addresses in various formats to a list of,
    where each IP address is specified separately.

    Args:

        The parameter is accepted as a string, for example
            1. '192.168.0.1'
            2. '192.168.0.1-4'
            3. '192.168.0.1-192.168.0.4'
            4. '192.168.0.0/16'

        or as a list
            1. ['192.168.0.1', '192.168.0.1-4', '192.168.0.1-192.168.0.4']

    Return:

        A list of ranges from the specified parameters is returned, for example
            [
                '192.168.0.1',
                '192.168.0.2',
                '192.168.0.3',
                '192.168.0.4',
            ]
    """

    def calculate_ip_append_to_list(ip, ip_range_list):
        """Calculates and fills in the list

        Args:
            1. '192.168.0.1-2' or ['192.168.0.1-2',...]
            2. list

        Do:
            Calculate range IP addresses and append
            ['192.168.0.1', '192.168.0.2']
        """

        if search(r"\d\/", ip):

            subnet = ip_network(ip)

            for ips in subnet.hosts():
                ip_range_list.append(str(IPv4Address(getattr(ips, "_ip"))))
        else:
            if search(r"\d\-", ip):
                splitted_ip = ip.split("-")
                arg1 = ip_address(splitted_ip[0])
                if len(splitted_ip) == 1:
                    ip_range_list.append(str(arg1))

                if splitted_ip[1].isdigit():
                    arg2 = splitted_ip[1]
                    for i in range(
                        int(arg1),
                        int(arg1) + int(arg2),
                        1,
                    ):
                        ip_range_list.append(str(IPv4Address(i)))
                else:
                    arg2 = ip_address(splitted_ip[1])
                    for i in range(int(arg1), int(arg2) + 1, 1):
                        ip_range_list.append(str(IPv4Address(i)))
            else:
                ip_range_list.append(ip)

    if ip is None or not ip:
        raise ExceptionProcessing("argument is empty")

    ip_range_list = []

    try:
        if isinstance(ip, list):
            for sub in ip:
                calculate_ip_append_to_list(sub, ip_range_list)
        if isinstance(ip, str):
            calculate_ip_append_to_list(ip, ip_range_list)

    except ValueError as err:
        raise err

    return ip_range_list


def print_ip_table(
    active_ip_list: List[str],
    passive_ip_list: List[str],
) -> None:
    """Information output in tabular format

    Args:
        Accepts two lists, available and unavailable addresses, for example

            1. List of available addresses
                [
                    '192.168.0.1',
                    '192.168.0.2',
                ]

            2. The list of unavailable addresses
                [
                    '192.168.0.3',
                    '192.168.0.4',
                ]

    Print:

        Outputs a message to the console in tabular format

        Reachable    Unreachable
        -----------  -------------
        192.168.0.1  192.168.0.3
        192.168.0.2  192.168.0.4
    """

    addresses = {"Reachable": active_ip_list, "Unreachable": passive_ip_list}
    print("\n" + tabulate(addresses, headers="keys"))


def arg_parse() -> ArgumentParser:
    """Output of the help command"""

    arg = ArgumentParser(description="Ping the list of ip addresses")
    arg.add_argument(
        "ip_address",
        type=list,
        help="""The IP address in the format:
        192.168.0.1,
        192.168.0.1-10,
        192.168.0.1-192.168.0.10,
        192.168.0.0\\16,
        when using a mask, specify the network address""",
    )
    return arg


def main():
    """Main function"""
    try:
        if arg_parse().parse_args():
            ranges = convert_ranges_to_ip_list(argv[1::])
            reachable, unreachable = ping_ip_addresses(ranges)
            print_ip_table(reachable, unreachable)

    except ExceptionProcessing as err:
        raise err
    except ValueError as err:
        raise err


if __name__ == "__main__":
    main()
