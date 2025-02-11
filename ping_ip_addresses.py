"""
Модуль, проверки доступности узлов при помощи команды ping.
"""

import ipaddress
import platform
import re
import subprocess
import sys

from tabulate import tabulate


def ping_ip_addresses(ip_addresses: list) -> list | list:
    """Запуск команды пинг. Поск строки по регулярному выражению
    Функция ожидает как аргумент список IP-адресов"""

    if ip_addresses is None:
        print("List is empty")
        exit()

    active_ip_list = []
    passive_ip_list = []

    for ip in ip_addresses:
        match platform.system():
            case "Windows":
                reply = subprocess.run(
                    [f"ping {ip}"],
                    stdout=subprocess.PIPE,
                    check=False,
                )

            case "Linux":
                reply = subprocess.run(
                    [f"ping {ip} -c 4"],
                    stdout=subprocess.PIPE,
                    shell=True,
                    check=False,
                )

            case _:
                print("Unexpected system")
                exit()

        if re.search(r"(\s|\()(\d|\d\d)%", str(reply)):
            active_ip_list.append(ip)
        else:
            passive_ip_list.append(ip)

    return active_ip_list, passive_ip_list


def convert_ranges_to_ip_list(ip: str | list) -> list:
    """Конвертирует список IP-адресов в разных форматах в список,
    где каждый IP-адрес указан отдельно."""

    if ip is None or ip == "":
        print("argument is empty")
        exit()

    ip_range_list = []

    try:
        for sub in ip:
            subnet = ipaddress.ip_network(sub)

            if subnet.prefixlen == 31 or subnet.prefixlen == 32:
                raise ValueError

            for ips in subnet.hosts():
                ip_range_list.append(
                    str(
                        ipaddress.IPv4Address(
                            getattr(
                                ips,
                                "_ip",
                            )
                        )
                    )
                )

    except ValueError:
        match isinstance(ip, str):
            case True:
                splitted_ip = ip.split("-")
                append_list(splitted_ip, ip_range_list)
            case False:
                for list_arg in ip:
                    splitted_ip = list_arg.split("-")
                    append_list(splitted_ip, ip_range_list)

    return ip_range_list


def append_list(splitted_ip: list[str], ip_range_list: list) -> None:
    """Добавление IP в список"""

    arg1 = ipaddress.ip_address(splitted_ip[0])
    if len(splitted_ip) == 1:
        ip_range_list.append(str(arg1))
    else:
        try:
            arg2 = ipaddress.ip_address(splitted_ip[1])
            for i in range(int(arg1), int(arg2) + 1, 1):
                ip_range_list.append(str(ipaddress.IPv4Address(i)))

        except ValueError:
            arg2 = splitted_ip[1]
            for i in range(int(arg1), int(arg1) + int(arg2), 1):
                ip_range_list.append(str(ipaddress.IPv4Address(i)))


def print_ip_table(active_ip_list: list, passive_ip_list: list) -> None:
    """Вывод информации в табличном формате"""

    addresses = {"Reachable": active_ip_list, "Unreachable": passive_ip_list}
    print(tabulate(addresses, headers="keys"))


if __name__ == "__main__":
    ranges = convert_ranges_to_ip_list(sys.argv[1::])
    reachable, unreachable = ping_ip_addresses(ranges)
    print_ip_table(reachable, unreachable)
