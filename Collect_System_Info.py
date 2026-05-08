#pip install psutil

import socket
import psutil
import csv
from datetime import datetime


def get_hostname():
    return socket.gethostname()


def get_local_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "Unknown"


def get_network_interfaces():
    interfaces = []

    for interface_name, addresses in psutil.net_if_addrs().items():
        for address in addresses:
            if address.family == socket.AF_INET:
                interfaces.append({
                    "interface": interface_name,
                    "ip_address": address.address
                })

    return interfaces


def save_to_csv(filename="system_network_log.csv"):
    hostname = get_hostname()
    interfaces = get_network_interfaces()

    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)

        for interface in interfaces:
            writer.writerow([
                datetime.now(),
                hostname,
                interface["interface"],
                interface["ip_address"]
            ])


def main():
    print("=== System Network Info ===")
    print("Hostname:", get_hostname())
    print("Main Local IP:", get_local_ip())

    print("\nNetwork Interfaces:")
    for interface in get_network_interfaces():
        print(interface)

    save_to_csv()
    print("\nNetwork info saved to system_network_log.csv")


if __name__ == "__main__":
    main()