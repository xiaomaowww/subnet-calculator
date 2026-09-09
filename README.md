# Subnet Calculator (subnetcalc.py)

A command-line IPv4 subnet calculator. Give it an IP address with CIDR
notation and it returns the network address, broadcast address, usable
host range, subnet mask, wildcard mask, and total/usable host counts.

## Why this is useful

Subnetting is one of those networking fundamentals everyone in IT is
expected to be comfortable with, but those people (myself included) still
double check with a calculator in the real world. This tool takes a
single input and returns everything you'd need for network planning,
troubleshooting, or documenting an IP scheme — the same information
you'd calculate by hand for a Network+ exam or a real subnetting task,
just automated.

## Features

- Accepts standard CIDR notation (e.g. `192.168.1.10/24`)
- Works even if you give it a host address rather than the network
  address itself (e.g. `192.168.1.10/24` correctly resolves to the
  `192.168.1.0/24` network)
- Outputs:
  - Network address & broadcast address
  - First/last usable host
  - Subnet mask & wildcard mask (decimal and binary)
  - Total addresses vs. usable hosts
  - Historical address class (A/B/C/D/E) for reference
  - Private vs. public address indication
- Handles edge cases correctly: `/31` point-to-point links and `/32`
  single-host routes
- Validates input and reports clear errors for malformed addresses

## Requirements

- Python 3.7+ (uses only the standard library — no external
  dependencies)

## Usage

Pass the address directly as an argument:

```bash
python3 subnetcalc.py 192.168.1.10/24
```

Or run with no arguments to be prompted interactively:

```bash
python3 subnetcalc.py
```

## Sample Output

```
=======================================================
SUBNET CALCULATION REPORT
=======================================================
Input                 : 10.0.5.130/26
IP Class (historical) : A
Private/Public        : Private
-------------------------------------------------------
Subnet Mask           : 255.255.255.192
Wildcard Mask         : 0.0.0.63
Mask (binary)         : 11111111.11111111.11111111.11000000
-------------------------------------------------------
Network Address       : 10.0.5.128
Broadcast Address     : 10.0.5.191
First Usable Host     : 10.0.5.129
Last Usable Host      : 10.0.5.190
-------------------------------------------------------
Total Addresses       : 64
Usable Hosts          : 62
=======================================================
```

## How it works

The script leans on Python's built-in `ipaddress` module to do the
underlying math (rather than reimplementing bitwise subnetting logic from
scratch), and focuses on presenting that information clearly and
validating input properly — including the historical address class,
wildcard mask, and binary representation of the subnet mask, which
`ipaddress` doesn't surface directly.

## Possible extensions

- Add support for splitting a network into N equal subnets (VLSM planning)
- Add IPv6 support
- Build a simple web front end using Flask so it's usable without a terminal
- Add a "how many subnets/hosts do I need" reverse mode

## What I learned building this

Working with Python's `ipaddress` module for IP arithmetic, handling the
difference between a host address and its containing network (`strict`
mode in `ip_interface`), and correctly handling the special-case `/31`
and `/32` subnets that don't follow the normal "first and last address
reserved" rule.
