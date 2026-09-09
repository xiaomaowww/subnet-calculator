"""
subnetcalc.py - Simple IPv4 Subnet Calculator

Takes an IP address + CIDR notation (or dotted-decimal subnet mask) and
outputs network address, broadcast address, usable host range, number of
usable hosts, and subnet mask/wildcard mask.

Usage:
    python3 subnetcalc.py 192.168.1.10/24
    python3 subnetcalc.py 10.0.5.130/26
    python3 subnetcalc.py                # interactive mode, prompts for input
"""

import argparse
import ipaddress
import sys


def calculate_subnet(cidr_input):
    """Takes a string like '192.168.1.10/24' and returns a report dict."""
    try:
        # strict=False allows host bits to be set (e.g. 192.168.1.10/24
        # instead of requiring 192.168.1.0/24)
        interface = ipaddress.ip_interface(cidr_input)
        network = interface.network
    except ValueError as e:
        raise ValueError(f"Invalid input '{cidr_input}': {e}")

    total_addresses = network.num_addresses
    usable_hosts = max(total_addresses - 2, 0) if network.prefixlen < 31 else total_addresses

    if network.prefixlen < 31:
        first_usable = network.network_address + 1
        last_usable = network.broadcast_address - 1
    elif network.prefixlen == 31:
        # point-to-point link, RFC 3021, both addresses usable
        first_usable = network.network_address
        last_usable = network.broadcast_address
    else:
        # /32, single host
        first_usable = network.network_address
        last_usable = network.network_address

    wildcard = ipaddress.IPv4Address(int(network.netmask) ^ int(ipaddress.IPv4Address("255.255.255.255")))

    report = {
        "input_ip": str(interface.ip),
        "cidr": f"/{network.prefixlen}",
        "netmask": str(network.netmask),
        "wildcard_mask": str(wildcard),
        "network_address": str(network.network_address),
        "broadcast_address": str(network.broadcast_address),
        "first_usable": str(first_usable),
        "last_usable": str(last_usable),
        "total_addresses": total_addresses,
        "usable_hosts": usable_hosts,
        "ip_class": get_class(network.network_address),
        "is_private": network.is_private,
        "binary_mask": format(int(network.netmask), "032b"),
    }
    return report


def get_class(ip):
    """Returns the historical IPv4 address class (A/B/C/D/E) for context."""
    first_octet = int(str(ip).split(".")[0])
    if 1 <= first_octet <= 126:
        return "A"
    elif 128 <= first_octet <= 191:
        return "B"
    elif 192 <= first_octet <= 223:
        return "C"
    elif 224 <= first_octet <= 239:
        return "D (Multicast)"
    elif 240 <= first_octet <= 255:
        return "E (Reserved)"
    return "Unknown"


def format_binary_mask(binary_str):
    """Splits a 32-char binary string into dotted octets for readability."""
    return ".".join(binary_str[i:i + 8] for i in range(0, 32, 8))


def print_report(report):
    print("=" * 55)
    print("SUBNET CALCULATION REPORT")
    print("=" * 55)
    print(f"{'Input':<22}: {report['input_ip']}{report['cidr']}")
    print(f"{'IP Class (historical)':<22}: {report['ip_class']}")
    print(f"{'Private/Public':<22}: {'Private' if report['is_private'] else 'Public'}")
    print("-" * 55)
    print(f"{'Subnet Mask':<22}: {report['netmask']}")
    print(f"{'Wildcard Mask':<22}: {report['wildcard_mask']}")
    print(f"{'Mask (binary)':<22}: {format_binary_mask(report['binary_mask'])}")
    print("-" * 55)
    print(f"{'Network Address':<22}: {report['network_address']}")
    print(f"{'Broadcast Address':<22}: {report['broadcast_address']}")
    print(f"{'First Usable Host':<22}: {report['first_usable']}")
    print(f"{'Last Usable Host':<22}: {report['last_usable']}")
    print("-" * 55)
    print(f"{'Total Addresses':<22}: {report['total_addresses']}")
    print(f"{'Usable Hosts':<22}: {report['usable_hosts']}")
    print("=" * 55)


def main():
    parser = argparse.ArgumentParser(
        description="Calculate subnet details from an IP address and CIDR prefix."
    )
    parser.add_argument(
        "target",
        nargs="?",
        help="IP address with CIDR notation, e.g. 192.168.1.10/24",
    )
    args = parser.parse_args()

    target = args.target
    if not target:
        target = input("Enter an IP address with CIDR notation (e.g. 192.168.1.10/24): ").strip()

    try:
        report = calculate_subnet(target)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print_report(report)


if __name__ == "__main__":
    main()
