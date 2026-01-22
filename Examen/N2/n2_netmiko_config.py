from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "192.168.1.10",   # <-- pas aan
    "username": "admin",      # <-- pas aan
    "password": "cisco",      # <-- pas aan
    "secret": "cisco",        # <-- pas aan (enable)
}

config_commands = [
    "hostname N2-DEVICE",
    "interface loopback 99",
    "ip address 10.99.99.1 255.255.255.255",
    "description NETMIKO_N2_TEST",
]

conn = ConnectHandler(**device)
conn.enable()

print("=== CONFIG PUSH ===")
print(conn.send_config_set(config_commands))

print("=== SAVE CONFIG ===")
print(conn.save_config())

print("=== VERIFY ===")
print(conn.send_command("show ip interface brief"))
print(conn.send_command("show running-config | section interface Loopback99"))
print(conn.send_command("show running-config | include hostname"))

conn.disconnect()
