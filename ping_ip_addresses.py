"""
Модуль, проверки доступности узлов при помощи команды ping.
"""

from ipaddress import IPv4Address, ip_address, ip_network
from platform import system
from re import search
from subprocess import PIPE, run
from sys import argv

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
        match system():
            case "Windows":
                reply = run(
                    ["ping", {ip}],
                    stdout=PIPE,
                    check=False,
                )

            case "Linux":
                reply = run(
                    [f"ping -c 4 {ip}"],
                    stdout=PIPE,
                    shell=True,
                    check=False,
                )

            case _:
                print("Unexpected system")
                exit()

        if search(r"\s(TTL|ttl)", str(reply)):
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
            subnet = ip_network(sub)

            if subnet.prefixlen == 31 or subnet.prefixlen == 32:
                raise ValueError

            for ips in subnet.hosts():
                ip_range_list.append(str(IPv4Address(getattr(ips, "_ip"))))

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

    arg1 = ip_address(splitted_ip[0])
    if len(splitted_ip) == 1:
        ip_range_list.append(str(arg1))
    else:
        try:
            arg2 = ip_address(splitted_ip[1])
            for i in range(int(arg1), int(arg2) + 1, 1):
                ip_range_list.append(str(IPv4Address(i)))

        except ValueError:
            arg2 = splitted_ip[1]
            for i in range(int(arg1), int(arg1) + int(arg2), 1):
                ip_range_list.append(str(IPv4Address(i)))


def print_ip_table(active_ip_list: list, passive_ip_list: list) -> None:
    """Вывод информации в табличном формате"""

    addresses = {"Reachable": active_ip_list, "Unreachable": passive_ip_list}
    print(tabulate(addresses, headers="keys"))


if __name__ == "__main__":
    ranges = convert_ranges_to_ip_list(argv[1::])
    reachable, unreachable = ping_ip_addresses(ranges)
    print_ip_table(reachable, unreachable)
