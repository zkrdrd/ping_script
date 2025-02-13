Запуск тестов
``` shell
pytest
```
Запуск сприпта 

При использовании префикса, указывать адрес сети, 

во время пинга не будут использоваться адреса сети и широковещательные адреса

Не использовать адреса с префиксом и без в 1 запросе
```shell 
python3 ping_ip_addresses.py 1.1.1.1-5 
python3 ping_ip_addresses.py 1.1.1.1-5 2.2.2.2-2.2.2.6 3.3.3.3
python3 ping_ip_addresses.py 192.168.0.0/16 172.16.0.0/16
```

Использование в коде
```python
ranges = convert_ranges_to_ip_list([
            "8.8.8.8",
            "1.1.1.1-1.1.1.3",
            "2.2.2.2-5",
        ])
reachable, unreachable = ping_ip_addresses(ranges)
print_ip_table(reachable, unreachable)
```