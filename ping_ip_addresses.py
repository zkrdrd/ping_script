"""
Модуль, проверки доступности узлов при помощи команды ping.
"""

from ipaddress import IPv4Address, ip_address, ip_network
from platform import system
from re import search
from subprocess import PIPE, run
from sys import argv
from typing import List, Tuple, Union

from tabulate import tabulate


def ping_ip_addresses(ip_addresses: List[str]) -> Tuple[List[str]]:
    """Запуск команды пинг. Поск строки по регулярному выражению
    Функция ожидает как аргумент список IP-адресов

    Args:

        Принимается параметр в виде списка, например
            [
                '192.168.0.1',
                '192.168.0.2',
                '192.168.0.3',
                '192.168.0.4',
            ]

    Return:

        Возвращается два списока, доступные и недоступные адреса, например

            1. Список доступных адресов
                [
                    '192.168.0.1',
                    '192.168.0.2',
                ]

            2. Список недоступых адресов
                [
                    '192.168.0.3',
                    '192.168.0.4',
                ]
    """

    if ip_addresses is None:
        exit("List is empty")

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
                exit("Undefined system")

        if search(r"\s(TTL|ttl)", str(reply)):
            active_ip_list.append(ip)
        else:
            passive_ip_list.append(ip)

    return active_ip_list, passive_ip_list


def convert_ranges_to_ip_list(ip: Union[str, list]) -> List[str]:
    """Конвертирует список IP-адресов в разных форматах в список,
    где каждый IP-адрес указан отдельно.

    Args:

        Принимается параметр в виде строки, например
            1. '192.168.0.1'
            2. '192.168.0.1-4'
            3. '192.168.0.1-192.168.0.1-4'
            4. '192.168.0.0/16'

        или в виде списка
            1. ['192.168.0.1', '192.168.0.1-4', '192.168.0.1-192.168.0.4']

    Return:

        Возвращается список диапозонов из заданых параметров, например
            [
                '192.168.0.1',
                '192.168.0.2',
                '192.168.0.3',
                '192.168.0.4',
            ]
    """

    if ip is None or ip == "":
        exit("argument is empty")

    ip_range_list = []

    try:
        for sub in ip:
            try:
                subnet = ip_network(sub)
            except ValueError as ve:
                raise ValueError from ve

            if subnet.prefixlen == 31 or subnet.prefixlen == 32:
                raise ValueError

            for ips in subnet.hosts():
                ip_range_list.append(str(IPv4Address(getattr(ips, "_ip"))))

    except ValueError:
        if isinstance(ip, str):
            splitted_ip = ip.split("-")
            append_list(splitted_ip, ip_range_list)
        else:
            for list_arg in ip:
                splitted_ip = list_arg.split("-")
                append_list(splitted_ip, ip_range_list)

    return ip_range_list


def append_list(
    splitted_ip: List[str],
    ip_range_list: List[str],
) -> None:
    """Добавление IP в список

    Args:
        1. Разделеный список аргументов
        2. Список куда заполняеется диапозон ip адресов

    Если второй аргумент в списке в формате ip адреса (1.1.1.1)
    то высчитывается диапозон ip адресов в блоке try

    Если второй аргумент в списке число в формате строки (4)
    то высчитывается диапозон ip адресов в блоке except
    """

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


def print_ip_table(
    active_ip_list: List[str],
    passive_ip_list: List[str],
) -> None:
    """Вывод информации в табличном формате

    Args:
        Принимает два списока, доступные и недоступные адреса, например

            1. Список доступных адресов
                [
                    '192.168.0.1',
                    '192.168.0.2',
                ]

            2. Список недоступых адресов
                [
                    '192.168.0.3',
                    '192.168.0.4',
                ]

    Print:

        Выводит сообщение в консоль в табличном формате

        Reachable    Unreachable
        -----------  -------------
        192.168.0.1  192.168.0.3
        192.168.0.2  192.168.0.4
    """

    addresses = {"Reachable": active_ip_list, "Unreachable": passive_ip_list}
    print(tabulate(addresses, headers="keys"))


if __name__ == "__main__":
    ranges = convert_ranges_to_ip_list(argv[1::])
    reachable, unreachable = ping_ip_addresses(ranges)
    print_ip_table(reachable, unreachable)
