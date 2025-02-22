"""
Тестирование модуля ping_ip_address
"""

from ping_ip_domain import convert_ranges_to_ip_list, ping_ip_addresses


def test_ping_ip_addresses():
    """Проверка функции пинга

    Args:
        ["192.168.0.6", "8.8.8.8", "127.0.0.1"]

    Result:
        ["8.8.8.8", "127.0.0.1"]
        ["192.168.0.6"]
    """

    assert ping_ip_addresses(
        [
            "192.168.0.6",
            "8.8.8.8",
            "127.0.0.1",
        ]
    ) == (
        ["8.8.8.8", "127.0.0.1"],
        ["192.168.0.6"],
    )


def test_ping_domain_name():
    """Проверка функции пинга

    Args:
        ["google.com", "ya.ru", "NotAdomain"]

    Result:
        ["google.com", "ya.ru"]
        ["NotAdomain"]
    """

    assert ping_ip_addresses(
        [
            "google.com",
            "ya.ru",
            "NotAdomain",
        ]
    ) == (
        ["google.com", "ya.ru"],
        ["NotAdomain"],
    )


def test_convert_ranges_to_ip_list():
    """Проверка функции получения диапозона ip аресов

    Args:

        Принимается параметр в виде строки, например
            1. '192.168.0.1'
            2. '192.168.0.1-4'
            3. '192.168.0.1-192.168.0.1-4'
            4. '192.168.0.0/16'

        или в виде списка
            1. ['192.168.0.1', '192.168.0.1-4', '192.168.0.1-192.168.0.4']

    Result:

        Возвращается список диапозонов из заданых параметров, например
            [
                '192.168.0.1',
                '192.168.0.2',
                '192.168.0.3',
                '192.168.0.4',
            ]

    """

    assert convert_ranges_to_ip_list("1.1.1.1") == ["1.1.1.1"]
    assert convert_ranges_to_ip_list(
        [
            "192.168.0.0/29",
            "172.16.0.0/29",
        ]
    ) == [
        "192.168.0.1",
        "192.168.0.2",
        "192.168.0.3",
        "192.168.0.4",
        "192.168.0.5",
        "192.168.0.6",
        "172.16.0.1",
        "172.16.0.2",
        "172.16.0.3",
        "172.16.0.4",
        "172.16.0.5",
        "172.16.0.6",
    ]
    assert convert_ranges_to_ip_list("1.1.1.1-4") == [
        "1.1.1.1",
        "1.1.1.2",
        "1.1.1.3",
        "1.1.1.4",
    ]
    assert convert_ranges_to_ip_list("1.1.1.1-1.1.1.3") == [
        "1.1.1.1",
        "1.1.1.2",
        "1.1.1.3",
    ]
    assert convert_ranges_to_ip_list(
        [
            "8.8.8.8",
            "1.1.1.1-1.1.1.3",
            "2.2.2.2-5",
        ]
    ) == [
        "8.8.8.8",
        "1.1.1.1",
        "1.1.1.2",
        "1.1.1.3",
        "2.2.2.2",
        "2.2.2.3",
        "2.2.2.4",
        "2.2.2.5",
        "2.2.2.6",
    ]
