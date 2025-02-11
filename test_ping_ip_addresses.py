import ping_ip_addresses as pia


def test_ping_ip_addresses():
    assert pia.ping_ip_addresses(
        [
            "192.168.0.6",
            "8.8.8.8",
            "127.0.0.1",
        ]
    ) == (
        ["8.8.8.8", "127.0.0.1"],
        ["192.168.0.6"],
    )


def test_convert_ranges_to_ip_list():
    assert pia.convert_ranges_to_ip_list("1.1.1.1") == ["1.1.1.1"]
    assert pia.convert_ranges_to_ip_list("1.1.1.1-4") == [
        "1.1.1.1",
        "1.1.1.2",
        "1.1.1.3",
        "1.1.1.4",
    ]
    assert pia.convert_ranges_to_ip_list("1.1.1.1-1.1.1.3") == [
        "1.1.1.1",
        "1.1.1.2",
        "1.1.1.3",
    ]
    assert pia.convert_ranges_to_ip_list(
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
